# Bugzilla Triage Learnings

This file captures insights and patterns discovered during bug triage to improve future analyses.

## API Tool Selection
- **Tool**: Always use `curl` for Bugzilla REST API calls, not `fetch_webpage`
- **Reason**: `fetch_webpage` is designed for HTML parsing; it cannot handle authentication headers properly and returns login pages on auth failures. APIs require precise control and JSON responses.
- **Usage**:
  - Bug details: `curl -s "https://bugzilla.olympus.f5net.com/rest/bug/<BUG_ID>?api_key=$BUGZILLA_API_KEY"`
  - Comments: `curl -s "https://bugzilla.olympus.f5net.com/rest/bug/<BUG_ID>/comment?api_key=$BUGZILLA_API_KEY"`

### REST API authentication
- `api_key=<KEY>` in the URL query string works **only** for `/rest/` endpoints
- `buglist.cgi?api_key=...` does **NOT** work — returns a login HTML page regardless of key
- `buglist.cgi?Bugzilla_api_key=...` also does NOT work for machine auth
- `X-BUGZILLA-API-KEY` header also rejected by `buglist.cgi` — session cookie auth only

## Component Mapping Patterns
- Bugs in `tm_daemon/mcp/sys/validation/` should map to `a_MCP_FRAMEWORK`, not to specific feature components (e.g., not `a_MCP_LTM`)
- Transaction/validation issues are framework-level, even if they affect LTM resources (HTTP Monitors, Pools, etc.)
- Always verify source file location before assigning component

## Transaction / Application Service Issues
- **Error "contains objects owned by other application service"**: Often a race condition in folder ownership validation
- **Root cause location**: `tm_daemon/mcp/sys/validation/AppInstance.cpp` — `check_folder_object_ownership_modified()`
- **Pattern**: Validation runs before newly created objects are fully visible to the query engine
- **Workaround**: Create folder in separate transaction from child resources

## Duplicate Detection Strategy

### Verified Working Approach: REST content= with intersection

**Tested against bug 2162845 on 2026-04-23.**

The correct approach for backtrace-based duplicate search is:
1. Use `/rest/bug?product=BIG-IP&content=<TERM>&api_key=$BUGZILLA_API_KEY` for full-text search
2. Run one query per distinctive function name (3 queries total)
3. Intersect the result ID sets in code to get AND behaviour

#### What works and what doesn't

| Approach | Result |
|---|---|
| `buglist.cgi?api_key=...` | ❌ Returns login page |
| `/rest/bug?long_desc=...&long_desc_type=allwordssubstr` | ❌ Returns 0 results (wrong param) |
| `/rest/bug?content=term1+term2` | ❌ Does OR, returns too many false positives |
| `/rest/bug?content=<single_term>` | ✅ Works, ~10–20 sec per query |
| **Single-term intersection** | ✅ Precise AND — found bug 2162845 in 2 results |

#### Effective Search Workflow
```
1. From backtrace top 10 frames, pick 3 distinctive function names
2. For each term run:
   curl -s "…/rest/bug?product=BIG-IP&content=<TERM>&api_key=…&include_fields=id,summary"
3. Intersect the 3 result ID sets (Python: set(r1) & set(r2) & set(r3))
4. Fetch comments for each candidate: /rest/bug/<ID>/comment
5. Score: count how many of top 10 function names appear in the text
```

#### Function Name Specificity (from testing)
- `mco_obj_map_get` → 5 results (extremedb C functions are very specific — best first pick)
- `bandwidth_gain_stat_request` → 49 results (feature-class names are good second pick)
- `EdbCompositeObj` → 164 results (general Cave/EDB class names are broader — use as third)
- **Best strategy**: start with the innermost non-library C function (fewest results), then add a feature-level class name
- **Never** include file:line pairs in search — line numbers change between releases and cause false negatives

#### Verified: Bug 2162845
- Bug summary: "HA going to Disconnected state intermittently on a CP longevity system" — contains NO function names
- Summary search would never find it; comment search is the only effective approach
- Found by: `mco_obj_map_get` (5 results) ∩ `bandwidth_gain_stat_request` (49 results) = **2 bugs**
- Scoring the 2 candidates confirmed #2162845 as exact match (full backtrace present in comment #10)

### Matching / Scoring Rules
- **Exact match**: all top 10 function names found in bug text (line numbers ignored)
- **Strong match**: 7–9 of top 10 function names found → report as duplicate candidate
- **Possible match**: 3–6 of top 10 function names found → list with confidence score
- Always report ALL exact and strong matches, not just the first

## RFC Analysis Edge Cases
- **Internal implementation bugs** (transaction processing, config validation, DB interactions, REST API handling, clustering): RFC section must NOT appear in report — omit completely; do not write "No RFC applicable"
- **Network protocol bugs** (TLS, OCSP, LDAP, etc.): Include RFC section with verdict
- Common mistake: Writing "RFC / Standard Compliance — No RFC applicable" — this is WRONG; either include the section with a verdict or omit it entirely

## Source Code Investigation Tips
- Use `p4 log -l <file>` to find recent CLs that touched affected files before reading code
- Compare recent change dates against bug report date to identify potential regression commits
- Check Review Board diffs for prior fixes to similar root causes in same file

## Tool Precision
- `grep_search`: Best for finding specific error messages, function names, or code patterns
- `semantic_search`: Best for understanding code relationships and architecture patterns
- `search_subagent`: Best for complex multi-step codebase exploration
- Never use `fetch_webpage` for APIs

## Testing & Verification
- Always include specific reproduction steps in final report
- Note version affected (e.g., "TMOS v17.5.0")
- Distinguish between "always fails" vs "intermittent" bugs — affects root cause analysis


## Known False Positive: Frame-Name-Only Summary Matches

### Incident: 2162497 vs 2162845 (April 23, 2026)

**Mistake**: Agent searched `short_desc=EdbTreeIterator+prefetch` (summary search) after `long_desc` searches returned empty, found Bug 2162497, and immediately reported it as a strong duplicate without scoring. The correct duplicate was Bug 2162845.

**Why it was wrong**:
- Bug 2162497 ("mcpd core - CaveInternals::EdbTreeIterator::prefetch") shares ONE frame name (`EdbTreeIterator::prefetch`) with the submitted backtrace
- Bug 2162845 ("HA going to Disconnected state intermittently on a CP longevity system") contains the **exact full backtrace** including `bandwidth_gain_stat_request::isession_profile_context` and `mco_obj_map_get` — the correct duplicate
- 2162845's summary contains NO crash function names, so it is invisible to summary searches — only `content=` full-text search finds it
- Scoring 2162497 against the top-10 function names would have given it 1/10 (only `EdbTreeIterator::prefetch`); 2162845 scores 10/10 — the scoring step catches this immediately

**Root cause of the mistake**:
1. Agent did not read the learnings file first (the correct `content=` intersection approach was already documented)
2. When `long_desc` REST searches returned empty, agent fell back to `short_desc` instead of switching to `content=`
3. Agent stopped at the first result without the mandatory scoring step

**Rules enforced by this incident**:
- ⛔ `short_desc` / `long_desc` REST searches are NOT valid fallbacks for backtrace mode — use `content=` only
- ⛔ NEVER report a duplicate without scoring it against the top-10 function names
- ✅ A bug whose summary has no crash function names can still be the correct duplicate — `content=` finds these
- ✅ Read the learnings file BEFORE any triage action — it prevents repeating this class of mistake

---

## Known False Negative: `quicksearch=` Misses Comment-Only Backtraces

### Incident: mco_latch_acquire crash — Bug #2240885 missed (April 23, 2026)

**Mistake**: Agent used `quicksearch=check_gtm_status`, `quicksearch=recalculate_pending_status`, and `quicksearch=EdbDbConnection+rollback` for backtrace search. All returned either 0 results or partial results (found Bug #2217657 but NOT Bug #2240885).

**Why it was wrong**:
- Bug #2240885 ("mcpd core at mco_latch_acquire") has an **exact frame-for-frame identical backtrace** to the submitted crash, stored in its comment #0
- Bug #2240885 is `RESOLVED/DUPLICATE` of Bug #2200561 (the canonical fix)
- `quicksearch=` does NOT reliably search all comment text — it silently skips comments for many bugs
- `content=check_gtm_status` would have found BOTH #2217657 and #2240885 because `check_gtm_status` appears in the backtrace text in both bugs' comments
- `content=recalculate_pending_status` would similarly have found both

**Correct search terms for this backtrace**:
- Term 1: `content=check_gtm_status` → {2217657, 2240885, ...}
- Term 2: `content=recalculate_pending_status` → {2217657, 2240885, ...}
- Term 3: `content=VirtualAddressMgr` → broader set, intersect with above two
- Intersection of terms 1 & 2 → {2217657, 2240885} — both correct matches

**When a RESOLVED/DUPLICATE bug is found**: always fetch its parent bug (from resolution comment) and report it. Here, #2240885 is a duplicate of #2200561 — the parent is the canonical fix reference.

**Rules enforced by this incident**:
- ⛔ `quicksearch=` is BANNED for backtrace mode — same as `short_desc` and `long_desc` — unreliable for comment search
- ✅ `content=<single_term>` + intersection is the only reliable approach
- ✅ When an exact/strong match is `RESOLVED/DUPLICATE`, fetch and report the parent bug too
- ✅ Always report ALL matching bugs, not just the first one found

---

**Last updated:** April 23, 2026
**Patterns documented:** API tool selection, REST auth limitations, component mapping, transaction validation, duplicate detection (verified intersection approach), RFC analysis, source code investigation, false-positive frame-name matches (2162497 vs 2162845)
