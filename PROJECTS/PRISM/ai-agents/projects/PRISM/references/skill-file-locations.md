# Module Skill File Locations (tmos-rocky)

## Important: Conditional Availability & Fallback

Skill files **only exist for modules that have a `.spec` file**. Not all modules have corresponding skill files.

**Lookup procedure:**
1. Try module-specific skill file: `//depot/tmos-rocky/tm_daemon/mcp/<module_name>_knowledge.SKILL.md`
2. If "no such file" → try mcp-level fallback: `//depot/tmos-rocky/tm_daemon/mcp/mcp_knowledge.SKILL.md`
3. If both return "no such file" → proceed with local source analysis

**Error codes:**
- "no such file" (both attempts) → neither skill file exists, proceed with local analysis
- "protected namespace - access denied" → skill file exists but you don't have access. Ask user for manual provision or proceed with local analysis

## Naming Convention

When a skill file exists, it follows this pattern:
```
//depot/tmos-rocky/tm_daemon/mcp/<module_name>_knowledge.SKILL.md
```

**Key points:**
- Files are directly in `tm_daemon/mcp/` directory, NOT nested in subdirectories
- Not all modules have skill files (only those with `.spec` files)

## Common Module Skill Files

| Module | Backtrace file example | Skill file path (tmos-rocky) |
|--------|------------------------|------------------------------|
| postgres | `postgres/PgUtil.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/postgres_knowledge.SKILL.md` |
| mcpd | `MCPProcessor.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/mcpd_knowledge.SKILL.md` |
| authz | `authz/UserdbEntry.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/authz_knowledge.SKILL.md` |
| ltm | `ltm/Pool.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/ltm_knowledge.SKILL.md` |
| framework | `framework/ValidationManager.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/framework_knowledge.SKILL.md` |
| sys | `sys/validation/FileObject.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/sys_knowledge.SKILL.md` |
| net | `net/Route.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/net_knowledge.SKILL.md` |
| clustering | `clustering/ClusterManager.cpp` | `//depot/tmos-rocky/tm_daemon/mcp/clustering_knowledge.SKILL.md` |

## How to Find the Skill File for a Crash

1. Look at the backtrace and identify the source file (e.g., `postgres/PgUtil.cpp`)
2. Extract the **first directory component** or **top-level module name** (e.g., `postgres`)
3. Try module-specific skill file: `//depot/tmos-rocky/tm_daemon/mcp/<module_name>_knowledge.SKILL.md`
4. If "no such file", try mcp-level fallback: `//depot/tmos-rocky/tm_daemon/mcp/mcp_knowledge.SKILL.md`

Example workflow:
```
Backtrace shows: postgres/PgUtil.cpp:108 in PgUtil::commit()
                         ↓
Extract module:   postgres
                         ↓
Try:              p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/postgres_knowledge.SKILL.md"
                         ↓
If "no such file": p4 print -q "//depot/tmos-rocky/tm_daemon/mcp/mcp_knowledge.SKILL.md"
                         ↓
If either found: load and reference. If neither found: proceed with local source analysis
```

## Access Issues

If `p4 print` returns "protected namespace - access denied":
1. Check your p4 session: `p4 login -s`
2. If session is valid but access still denied, contact your p4 admin for `//depot/tmos-rocky/tm_daemon/mcp/` read access
3. As a workaround, ask the user to provide the skill file content directly

See [p4-access-setup.md](p4-access-setup.md) for detailed troubleshooting.
