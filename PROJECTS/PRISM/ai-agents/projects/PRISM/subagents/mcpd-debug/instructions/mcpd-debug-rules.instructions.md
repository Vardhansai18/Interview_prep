---
description: "Behavioral rules for MCPD core dump debugging agents. Applies to mcpd-debug and mcpd-verifier agents. Covers: proof-over-assumption policy, analysis logging format, evidence chain requirements, fix safety checklist, source navigation rules, no-assumption golden rule."
applyTo: "**/mcpd-*.agent.md"
---

# MCPD Debug Agent Behavioral Rules

These rules apply to ALL MCPD debug agents (main and verifier).

## Golden Rule: Proof or Ask

Every claim must have proof. If you cannot prove it, ask the user.
- "I think" is NOT acceptable
- "GDB shows X at frame Y" IS acceptable

| Claim | Required Proof |
|-------|----------------|
| "Pointer is NULL" | `(gdb) p pointer` showing `0x0` |
| "Object was freed" | Memory state + free path in backtrace |
| "Race condition" | Two thread backtraces showing conflicting access |
| "Field has wrong value" | `(gdb) p field` + expected value from source |
| "Error code means X" | Citation from error_defs or mco.h |
| "Function does X" | Source code at specific file:line |
| "Fix is safe" | All callers + side effects analyzed |

## Architecture Constants (No Proof Needed)

| Fact | Value |
|------|-------|
| Architecture | x86_64 (64-bit) |
| Pointer size | 8 bytes |
| Database | eXtremeDB v8.4 with MVCC |
| OS | Linux (BIG-IP TMOS) |
| Analysis env | seadev (Linux dev server) |
| Source control | Perforce |

Everything else requires proof.

## Source Navigation

- Backtrace function → READ the actual source file, do not assume
- Variable in GDB → cross-reference with source for type and range
- Error code → look up in `bigip_mcpd_error_defs.in` AND `mco.h`
- Schema field (`cid_*`) → verify in schema definition

## Evidence Format

```
Evidence [N]:
  Type: [GDB output | Log line | Source code | User confirmation]
  Source: [file:line | GDB command | log file + timestamp]
  Content: [exact output, not paraphrased]
  Interpretation: [what this proves]
```

## Fix Safety (Prohibited Actions)

- Do NOT change function signatures unless required
- Do NOT add global/static variables without justification
- Do NOT remove existing error handling or logging
- Do NOT change behavior for non-buggy code paths
- Do NOT introduce new dependencies without justification
- Do NOT "fix" unrelated code while fixing the bug
