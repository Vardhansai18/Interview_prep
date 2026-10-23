# Final Report Output Template

Use this template for the final CP Bug Fix Report.

```markdown
## CP Bug Fix Report — Bug #<ID>

### Phase 1: Triage Summary
- **Component:** <component>
- **Duplicates:** <list or "None found">
- **Related bugs:** <IDs from blocks/depends_on/see_also>
- **RFC verdict:** <if applicable>

### Phase 2: Skill File Guidance
<Key points from tmos-rocky SKILL.md — exact quotes in blockquotes>

### Phase 2.5: Third-Party Upstream Check
- **Library:** <name> v<version>
- **Upstream fix available:** Yes (config param) / Yes (upgrade) / No
- **Config mitigation applied:** <param string or "N/A">
- **Decision:** <config + code / backport / workaround>

### Phase 3: Root Cause Analysis
**Primary Hypothesis (H1):** <one definitive sentence>
**Confidence Score:** <N>/100

**Evidence Chain:**
  Evidence [1]: <type> | <source> | <content> | <interpretation>
  Evidence [2]: ...

**Alternatives Ruled Out:**
  H2: <description> — ruled out because <evidence citation>
  H3: <description> — ruled out because <evidence citation>

### Phase 4: Fix
**File:** `<path>`
**Change:**
```diff
- <old code>
+ <new code>
```
**Rationale:** <why this addresses H1, citing evidence>
**Side-Effect Checklist:** ✅ All 8 items verified

### Phase 5: Cross-Validation
**Verifier Verdict:** PASS / FAIL
**Verifier Details:** <Tier 1 + Tier 2 summary>
**Control Plane Expert Review:**
1. Protocol correctness: ✅/⚠️
2. TMSH/iControl surface: ✅/⚠️ <changes if any>
3. Upgrade safety: ✅/⚠️
4. Scale correctness: ✅/⚠️
5. Error propagation: ✅/⚠️

### Phase 6: Test Plan
<TC-1 through TC-N using the test case format>

### Rollback Procedure
<How to revert the fix>
```
