# Root Cause Confidence Scoring

Load this file during Phase 3 when computing the confidence score.

## Scoring Rubric (100 points)

| Points | Criterion | How to earn |
|--------|-----------|-------------|
| +15 | Crash location identified | Source code at exact `file:line` matches backtrace frame |
| +15 | Faulting variable/condition traced | Show where the bad value originates (assignment, missing check) |
| +10 | Exact trigger condition | Specific input/state that causes the crash (e.g., "when postgres is unresponsive during COMMIT") |
| +10 | All alternatives ruled out | Each H2/H3 has specific evidence disproving it |
| +10 | Evidence chain zero gaps | Every step from entry to crash has a citation |
| +10 | Skill file pattern match | tmos-rocky SKILL.md confirms or rules out known patterns |
| +10 | Code path fully traced | From entry point (tmsh/iControl) through every function to crash |
| +5 | Related bugs confirm | Other bugs report same root cause |
| +5 | No weasel words | Primary hypothesis uses definitive language |
| +5 | Pattern found elsewhere | `grep` shows same bug pattern in other files |
| +5 | Caller analysis confirms | Callers assume the violated invariant |

## Decision Thresholds

| Score | Action |
|-------|--------|
| < 50 | **STOP.** List missing evidence. Ask user for more info. |
| 50–69 | Proceed with caution. Flag gaps in the report. |
| ≥ 70 | Proceed to Phase 4. |

## Evidence Table Format

```
Evidence [N]:
  Type: [Source code | Bugzilla comment | Backtrace frame | Skill file]
  Source: [file:line | Bug #ID comment N | Frame #N | tmos-rocky SKILL.md §Section]
  Content: [exact code snippet or quote — do NOT paraphrase]
  Interpretation: [what this proves about the root cause]
```

## Hypothesis Formation Rules

- **H1 (primary)**: One sentence, no weasel words. Must be falsifiable.
- **H2, H3 (alternatives)**: Each must be plausible enough to investigate.
- **Disproval**: For each alternative, cite specific evidence that rules it out.
- If you cannot rule out H2/H3 → your confidence score drops accordingly.
