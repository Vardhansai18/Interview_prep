# P4 Access Setup & Troubleshooting

## Quick Reference

**If p4 commands fail with "Access for user 'X' has not been enabled by 'p4 protect'":**

1. Set P4CONFIG to auto-detect workspace config:
   ```bash
   export P4CONFIG=.p4config
   ```

2. Log in with your password:
   ```bash
   p4 login
   # Enter your password at the prompt
   ```

3. Verify the session is valid:
   ```bash
   p4 login -s
   # Should show: "User <name> ticket expires in N hours"
   ```

## Root Cause

- Without `export P4CONFIG=.p4config`, p4 doesn't read your workspace's `.p4config` file
- The `.p4config` specifies: `P4USER`, `P4PORT`, `P4CLIENT`
- If `P4USER` is not set in the environment or `.p4config`, p4 defaults to your shell login name
- `p4 login` creates a ticket, but it's only valid for the combination of (P4USER, P4PORT, P4CLIENT)
- Mismatches between environment and ticket → "protected namespace - access denied"

## Checking Your Environment

```bash
echo "P4CONFIG=$P4CONFIG"
echo "P4USER=$P4USER"
echo "P4PORT=$P4PORT"
echo "P4CLIENT=$P4CLIENT"
cat .p4config       # Should show all three values
```

## Testing P4 Access

```bash
# Test basic connection
p4 login -s

# Test read access (try a known file)
p4 files tm_daemon/mcp/postgres/PgUtil.cpp

# Test tmos-rocky skill files (protected — may still fail)
p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/postgres_knowledge.SKILL.md"
p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/mcpd_knowledge.SKILL.md"
```

## Permission Limitations

**Known issue on this workspace:**
- The `tmos-rocky` branch is a protected namespace
- User `aaluru` may not have read access to all branches
- If p4 returns "protected namespace - access denied", you need:
  1. **Option A**: Request p4 admin to grant access to the specific branch
  2. **Option B**: Have someone with access provide the skill file content directly
  3. **Option C**: Proceed with local source code analysis (without authoritative skill guidance)

## Making P4 Setup Persistent

Add to your `~/.zshrc`:
```bash
export P4CONFIG=.p4config
```

Then log in once:
```bash
p4 login
```

Future shell sessions will auto-use the correct P4 settings.
