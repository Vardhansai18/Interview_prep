# Test Plan Template

Load this file during Phase 6.

## Test Case Format

```
TC-N: <Short descriptive name>
Type: [Positive / Negative / Regression / Boundary]
Purpose: <What this test verifies — one sentence>
Setup:
  <exact tmsh/bash commands to configure the prerequisite state>
Steps:
  <exact commands to trigger the behavior under test>
Expected Result:
  <exact observable outcome — specific log lines, tmsh output, or absence of crash>
Pass Criteria:
  <how to confirm pass — e.g., "no file in /var/core/", "mcpd log contains X">
```

## Required Test Categories

Every fix MUST have at least one test case in each applicable category:

| Category | What to cover | When to skip |
|---|---|---|
| **Regression** | Reproduce the exact bug scenario → confirm it no longer fails | Never skip |
| **Positive path** | Normal operation still works correctly after the fix | Never skip |
| **Boundary / edge** | Test the exact boundary the fix handles | Never skip |
| **Error path** | Confirm error is handled gracefully (logged, no crash) | Never skip |
| **Concurrent access** | Simultaneous operations on shared state | Skip if fix doesn't touch shared state |
| **HA / clustering** | Behavior on standby after failover, config-sync | Skip if fix doesn't affect synced objects |
| **Scale** | Many objects/users/connections | Skip if fix is a simple null-check |

## Verification Commands (include in every test plan)

```bash
# Check for core dumps
ls -la /var/core/

# Verify mcpd is running
bigstart status mcpd

# Check mcpd logs for errors
grep -i "err\|crit\|panic" /var/log/ltm | tail -20

# Check if sod killed anything
grep -i "sod\|SIGABRT" /var/log/ltm | tail -10
```

## Rollback Procedure Template

```
1. SSH to the device
2. Restore original binary:
   cp /path/to/backup/mcpd /usr/bin/mcpd
3. Restart:
   bigstart restart mcpd
4. Verify:
   bigstart status mcpd
   tmsh show sys version
```
