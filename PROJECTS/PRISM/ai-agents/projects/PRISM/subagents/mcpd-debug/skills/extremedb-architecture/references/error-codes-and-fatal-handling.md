# Error Codes and Fatal Handling Reference

Complete eXtremeDB error code reference and fatal error handling chain for MCPD.

## Status Codes (Success / Expected)

| Code | Name | Meaning |
|------|------|---------|
| 0 | `MCO_S_OK` | Success |
| 10 | `MCO_S_NOTFOUND` | Search/lookup found nothing |
| 11 | `MCO_S_CURSOR_END` | Cursor reached end |
| 12 | `MCO_S_CURSOR_EMPTY` | No objects in index |
| 13 | `MCO_S_DUPLICATE` | Unique index violation |
| 15 | `MCO_S_DEAD_CONNECTION` | Connection is dead |

## Common Error Codes

| Code | Name | Meaning | Typical Cause |
|------|------|---------|---------------|
| 51 | `MCO_E_INVALID_HANDLE` | Invalid handle | Stale handle after MVCC versioning, use-after-free |
| 52 | `MCO_E_NOMEM` | No memory | Shared memory full, need `increase_db_size()` |
| 53 | `MCO_E_ACCESS` | Read-only tx for write | Bug: worker thread trying to write |
| 54 | `MCO_E_TRANSACT` | Transaction in error | Previous op failed, tx poisoned |
| 64 | `MCO_E_DELETED` | Update of deleted object | Object deleted then accessed in same tx |
| 67 | `MCO_E_UPGRADE_FAILED` | Tx upgrade failed | Concurrent writer blocks upgrade |
| 80 | `MCO_E_SHM_ERROR` | Shared memory error | `/dev/shm` permissions, space, corruption |
| 87 | `MCO_E_CONFLICT` | MVCC conflict | Two write tx modified same object |
| 96 | `MCO_E_PINNED_VERSION_LIMIT` | Too many pinned versions | Long-running read tx prevents GC |
| 124 | `MCO_E_DISK_CONFLICT` | Disk MVCC conflict | Disk-based MVCC conflict |
| 1012 | `MCO_E_BTREE_CONFLICT` | B-Tree index conflict | Index-level MVCC conflict |

## Fatal Error Codes (≥ 100000)

Fatal errors trigger `abort()` via the registered error handler.

| Base | Name | Category |
|------|------|----------|
| 100000 | `MCO_ERR_DB` | Database internal error |
| 110000 | `MCO_ERR_DICT` | Dictionary error |
| 120000 | `MCO_ERR_CURSOR` | Cursor error |
| 130000 | `MCO_ERR_PMBUF` | Page memory buffer error |
| 140000 | `MCO_ERR_COMMON` | Common routine error |
| 150000 | `MCO_ERR_HEAP` | Heap manager error |
| 160000 | `MCO_ERR_OBJ` | Object allocator error |
| 170000 | `MCO_ERR_BLOB` | Blob operation error |
| 180000 | `MCO_ERR_FREC` | Record allocator error |
| 190000 | `MCO_ERR_VOLUNTARY` | Voluntary index error |
| 200000 | `MCO_ERR_LOADSAVE` | DB save/load error |
| 210000 | `MCO_ERR_PGMEM` | Page memory error |
| 220000 | `MCO_ERR_EV_SYN` | Synchronous event error |

**Decoding**: `error_code / 10000 = category`, `error_code % 10000 = sub-code`

Example: `100042` = `MCO_ERR_DB` base + sub-code 42

---

## Fatal Error Handler Chain

```
eXtremeDB detects unrecoverable error
    │
    ▼
Calls registered fatal error handler
    (set via EdbConnectionInit::fatal_error_handler())
    │
    ▼
MCPD's handler in MCPDBMgr.cpp
    │
    ▼
mcp_fatal_error() logs MCPDERR_FATAL_DATABASE_ERROR (code 8)
    │
    ▼
abort() → SIGABRT → core dump
```

### Handler Registration

```cpp
// In EdbConnectionInit:
void fatal_error_handler(mco_error_handler_f);

// Type:
typedef void (*mco_error_handler_f)(int error_code, ...);
```

---

## GDB: Examining Fatal Error State

```gdb
# 1. Find the fatal handler frame in backtrace
(gdb) bt
# Look for: mco_fatal_error / mco_error_handler / MCPDBMgr::handle_fatal_error / mcp_fatal_error

# 2. Get the error code
(gdb) frame N   # The fatal handler frame
(gdb) info args
# error_code will be >= 100000

# 3. Decode
# error_code / 10000 = category
# error_code % 10000 = sub-code

# 4. Check what operation triggered it
(gdb) frame N+1   # Caller of fatal handler
(gdb) info args; info locals
```

### Common Fatal Error Scenarios

| Backtrace Pattern | Likely Cause |
|-------------------|--------------|
| `MCPDBMgr::db_checkpoint` → `mcp_fatal_error` | Checkpoint failed — shared memory issue |
| `mco_trans_commit` → fatal | Commit corruption |
| `mco_objalloc_*` → fatal (160000+) | Object allocation failed — memory exhaustion |
| `mco_btree_*` → fatal | Index corruption |

### Shared Memory State

**WARNING**: `/dev/shm` state is NOT captured in core dumps.

If you have logs or qkview from the BIG-IP, check:
```bash
ls -la /dev/shm/mcp*          # File sizes
ipcs -m                        # Shared memory segments
grep -i "database\|eXtremeDB\|cave\|mco_" /var/log/ltm
```
