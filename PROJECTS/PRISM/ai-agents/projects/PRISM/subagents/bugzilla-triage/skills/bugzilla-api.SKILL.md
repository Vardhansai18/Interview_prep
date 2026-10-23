---
name: bugzilla-api
description: "Domain knowledge for querying the F5 internal Bugzilla instance at bugzilla.olympus.f5net.com. USE FOR tasks involving searching for bugs, fetching bug details, authenticating with API keys, reading CSV search results, and finding duplicate bugs. Provides URL patterns, field references, search strategies, and output parsing rules."
---

## BUGZILLA API OVERVIEW

The F5 internal Bugzilla instance is at `https://bugzilla.olympus.f5net.com/`. All requests use the standard Bugzilla REST/web API. Authentication is via API key appended to every request URL.

**Base URL:** `https://bugzilla.olympus.f5net.com/`

**SECURITY:** Never log, echo, or print the API key. Never store the API key in any file.

---

## AUTHENTICATION

### Environment Variable (Preferred)
```bash
echo $BUGZILLA_API_KEY
```
If set, append silently to every request: `&api_key=<VALUE_OF_BUGZILLA_API_KEY>`

### User-Provided Key
If `BUGZILLA_API_KEY` is not set, prompt: *"Please provide your Bugzilla API key (generate at https://bugzilla.olympus.f5net.com/userprefs.cgi?tab=apikey)"*

### Appending to URLs
```
https://bugzilla.olympus.f5net.com/show_bug.cgi?id=12345&ctype=xml&api_key=<KEY>
https://bugzilla.olympus.f5net.com/buglist.cgi?...&api_key=<KEY>
```

---

## FETCHING A SINGLE BUG

### XML Format (full details)
```
https://bugzilla.olympus.f5net.com/show_bug.cgi?id=<BUG_ID>&ctype=xml&api_key=<KEY>
```

**Fields extracted from XML response:**
| XML Tag | Description |
|---------|-------------|
| `<bug_id>` | Bugzilla bug number |
| `<short_desc>` | One-line summary |
| `<long_desc>` | Description and comments (multiple `<long_desc>` elements) |
| `<component>` | Bugzilla component (e.g., `a_MCP_FRAMEWORK`) |
| `<product>` | Product name (e.g., `BIG-IP`) |
| `<bug_status>` | Status: `NEW`, `ASSIGNED`, `RESOLVED`, `CLOSED`, etc. |
| `<resolution>` | Resolution: `FIXED`, `DUPLICATE`, `WONTFIX`, `WORKSFORME`, etc. |
| `<assigned_to>` | Engineer assigned to the bug |
| `<severity>` | `blocker`, `critical`, `major`, `normal`, `minor`, `trivial`, `enhancement` |
| `<priority>` | `P1` through `P5` |
| `<version>` | BIG-IP version affected |
| `<cf_found_in_version>` | Custom field: version where bug was first observed |

### Comment extraction from XML
Each `<long_desc>` block contains:
- `<who>` — commenter username
- `<bug_when>` — timestamp
- `<thetext>` — comment body

---

## SEARCHING FOR BUGS

All search results are requested in CSV format (`&ctype=csv`) for easy parsing.

### Summary Search (short description)
```
https://bugzilla.olympus.f5net.com/buglist.cgi?query_format=advanced&short_desc_type=allwordssubstr&short_desc=<KEYWORDS>&product=BIG-IP&ctype=csv&api_key=<KEY>
```

**Tips:**
- Use 3-5 distinctive keywords from the bug summary
- URL-encode spaces as `+` or `%20`
- Avoid stop words (the, a, in, of)

### Full-Text Search (description + comments)
```
https://bugzilla.olympus.f5net.com/buglist.cgi?query_format=advanced&long_desc_type=allwordssubstr&long_desc=<KEYWORDS>&product=BIG-IP&ctype=csv&api_key=<KEY>
```

**Tips:**
- Use exact error message fragments, assertion text, or distinctive log strings
- Example: `long_desc=assert+failed+MCPConnection+sendMessage`

### Combined Summary + Full-Text Search
```
https://bugzilla.olympus.f5net.com/buglist.cgi?query_format=advanced&short_desc_type=allwordssubstr&short_desc=<KW1>&long_desc_type=allwordssubstr&long_desc=<KW2>&product=BIG-IP&ctype=csv&api_key=<KEY>
```

### Status-Filtered Search
Add `&bug_status=NEW&bug_status=ASSIGNED` to restrict to open bugs, or `&bug_status=RESOLVED&resolution=FIXED` for fixed bugs.

---

## PARSING CSV SEARCH RESULTS

CSV output columns (in order):
```
bug_id, product, component, assigned_to, bug_status, resolution, short_desc
```

**Parsing rules:**
- First line is the header row — skip it
- Each subsequent line is one bug
- Fields may be quoted if they contain commas
- `bug_id` is a plain integer — use it to construct the show_bug URL for full details

---

## DUPLICATE DETECTION STRATEGY

Run all three searches and combine unique bug IDs:

### Search 1 — Summary keywords
Extract 3-5 key terms from the bug summary.

### Search 2 — Error/log message full-text
Use the exact error message, assert text, or log line from the bug description.

### Search 3 — Crash signature (backtrace)
Extract the top 3 mcpd-specific function names and search in `long_desc`.

### Evaluating candidates
For each unique bug ID found across all three searches:
1. Fetch full details via `show_bug.cgi?id=<ID>&ctype=xml`
2. Compare against current bug:

| Match Type | Criteria | Confidence |
|------------|----------|------------|
| Strong duplicate | 3+ crash indicators match (same function, same file:line, same error) | HIGH |
| Possible duplicate | 1-2 indicators match | MEDIUM |
| Unrelated | Different error, different codepath | NONE |

**Verdict:**
- Strong match → **"Potential duplicate of Bug #<ID>"** with specific evidence
- No match → **"No duplicates found — this bug appears unique"**

---

## PRODUCT SCOPING

**Always restrict searches to `product=BIG-IP`** unless the user explicitly asks to search other products. Other available products include `BIG-IQ`, `F5OS`, `TMOS-Tools`, etc.

---

## RATE LIMITING AND ERROR HANDLING

- If a search returns an HTTP 4xx error, check that the API key is valid and not expired
- If a search returns an empty CSV (only header row), no matching bugs exist
- Bugzilla may return a 404 for bugs that are restricted — note this to the user and continue
- For very broad searches that return >100 results, refine keywords before fetching all details

---

## COMMON SEARCH PATTERNS

### Find bugs by mcpd function name
```
long_desc=MCPConnection%3A%3AsendMessage+libmcpdcommon
```

### Find bugs by assert message
```
long_desc=Assertion+failed%3A+%22msg%22
```

### Find bugs by BIG-IP version
```
https://bugzilla.olympus.f5net.com/buglist.cgi?query_format=advanced&product=BIG-IP&version=16.1.3&ctype=csv&api_key=<KEY>
```

### Find bugs recently assigned to a component
```
https://bugzilla.olympus.f5net.com/buglist.cgi?query_format=advanced&product=BIG-IP&component=a_MCP_FRAMEWORK&bug_status=NEW&ctype=csv&api_key=<KEY>
```
