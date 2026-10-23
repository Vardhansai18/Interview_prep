# MCPD Validation Pipeline, Error Codes & HA

## Validation Pipeline

Configuration changes go through a multi-stage validation pipeline before being committed.

### Stages

| Stage | Handler | Purpose |
|-------|---------|---------|
| 1 | CHECKPOINT_HANDLER | Early validation — name parsing, uniqueness, basic sanity |
| 2 | COMMIT_HANDLER | Final validation — address checks, type compatibility, dependency checks |
| 3 | DELETE_HANDLER | Pre-delete — verify no dependencies would break |
| 4 | object_deleted_event() | Post-delete cleanup — remove references, cascade deletes |
| 5 | PostTransMgr | Post-commit kernel ops — TAP create, route add, iptables, etc. |
| 6 | MCPPubSub::publish() | Notification — inform TMM, snmpd, etc. of the change |

### Class Manager Registration

Each configuration object type registers its handlers:
```cpp
REGISTER_CLASS_MGR(VirtualServerClassMgr, cid_virtual_server)
```

This wires up CHECKPOINT, COMMIT, DELETE handlers for that object type.

**Common crash source**: Missing handlers (e.g., missing DELETE_HANDLER leads to dangling references when an object is deleted but its dependents aren't cleaned up).

### Key Source Files

```
framework/ValidationManager.cpp   — Pipeline orchestration
framework/request_group.cpp        — Transaction processing, calls handlers
framework/PostTransMgr.cpp         — Post-commit kernel operations
framework/MCPPubSub.cpp            — Change notification to subscribers
```

## Error Codes

### Key MCPD Error Codes

| Code | Name | Meaning |
|------|------|---------|
| 8 | MCPDERR_FATAL_DATABASE_ERROR | eXtremeDB fatal error → abort() |
| 89 | MCPDERR_FATAL_HA_TABLE_ERROR | HA table corruption → abort() |
| 7 | MCPDERR_SHUTDOWN_SIGNAL | Clean shutdown (not a crash) |
| 930 | MCPDERR_ASSERTION_FAILED | assert() triggered |
| varies | MCPDERR_NULL_POINTER | NULL dereference detected |
| — | MCPDERR_DB_DUPLICATE_KEY | Duplicate key in DB |
| — | MCPDERR_DB_OBJECT_NOT_FOUND | Object missing from DB |
| — | MCPDERR_IO | I/O error on connection |

All error codes defined in: `bigip_mcpd_error_defs.in` (~4540 lines)

### How to Search Error Codes

```bash
# Find where an error code is defined
grep -rn "MCPDERR_FATAL_DATABASE_ERROR" tm_daemon/mcp/

# Find where abort() is called
grep -rn "abort()\|mcp_fatal_error\|mcpd_assert" tm_daemon/mcp/framework/

# Find a specific error code number
grep -rn "error code 8\|MCPDERR.*= 8" tm_daemon/mcp/
```

## Fatal Error Path

```
eXtremeDB error detected
    │
    ▼
MCPDBMgr::handle_fatal_error()  [framework/MCPDBMgr.cpp]
    │
    ▼
mcp_fatal_error() logs error code
    │
    ▼
abort() → SIGABRT → core dump
```

### GDB: Examining Fatal Errors

```gdb
# Check what triggered the fatal handler
(gdb) bt
# Look for: mco_fatal_error / mco_error_handler / MCPDBMgr::handle_fatal_error

# Get the error code
(gdb) frame N   # the handler frame
(gdb) info args

# Check eXtremeDB last error
(gdb) p mco_get_last_error(tx_handle)
(gdb) p Cave::DbConnection::c_db_connection->last_error()
```

## High Availability (HA)

- **MCPHAMgr** (`framework/MCPHAMgr.cpp`) manages HA synchronization between BIG-IP peers
- Configuration changes are replicated to the standby unit
- HA sync can crash when configuration diverges between peers
- During failover, MCPD must handle state transitions cleanly

### HA-Related Crash Indicators in Logs

```bash
grep -i "failover\|standby\|active\|peer\|cluster\|sync" /var/log/ltm | tail -100
```

### HA Error Code

| Code | Name | Meaning |
|------|------|---------|
| 89 | MCPDERR_FATAL_HA_TABLE_ERROR | HA table corruption → abort() |
