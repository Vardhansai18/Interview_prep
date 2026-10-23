---
name: extremedb-architecture
description: "eXtremeDB v8.4 and CAVE layer architecture for MCPD database debugging. Use when: analyzing eXtremeDB crashes, debugging mco_* cave_* Cave:: CfgObj DbConnection TransactionLog EdbDbConnection functions, diagnosing MVCC OID mismatch bugs, interpreting database error codes (MCO_E_NOMEM MCO_E_CONFLICT MCO_E_INVALID_HANDLE), understanding shared memory /dev/shm corruption, examining transaction lifecycle, tracing object handle vs OID divergence, investigating garbage collection or version pinning issues."
argument-hint: "Describe the database-related crash symptom, error code, or eXtremeDB/CAVE function you need help with"
---

# eXtremeDB / CAVE Architecture Skill

Database engine knowledge for debugging MCPD crashes rooted in eXtremeDB or the CAVE abstraction layer.

## When to Use

- Backtrace involves `mco_*`, `cave_*`, `Cave::`, `CfgObj`, `DbConnection`, `TransactionLog`
- Database error codes in crash (MCO_E_*, MCO_ERR_*, fatal codes ≥ 100000)
- MVCC-related symptoms: intermittent failures, OID mismatches, silent post-transaction failures
- Shared memory issues (`/dev/shm/mcp*`)
- Transaction lifecycle bugs (commit, rollback, upgrade failures)

## Architecture Stack

```
┌───────────────────────────────────────────┐
│  MCPD Application Logic                   │
│  (MCPProcessor, request_group, validators)│
├───────────────────────────────────────────┤
│  CAVE Layer (F5-authored)                 │
│  CfgObj · TransactionLog · DbConnection   │
│  QueryEngine · CfgSchema · CfgClass       │
├───────────────────────────────────────────┤
│  eXtremeDB v8.4 (McObject LLC)            │
│  Native C API (mco_*) · MVCC TM          │
│  Page Manager · Index Engines             │
├───────────────────────────────────────────┤
│  Shared Memory (/dev/shm/mcp*)            │
└───────────────────────────────────────────┘
```

**CAVE is NOT eXtremeDB** — it's F5's C++ wrapper. Bugs can exist in either layer; distinguishing which caused a crash is critical.

## Key Facts

| Property | Value |
|----------|-------|
| Engine | eXtremeDB v8.4 by McObject |
| Transaction Manager | MVCC (migrated from MURSIW) |
| Storage | `/dev/shm/mcp*` (shared memory, in-memory only) |
| Schema | Compiled into C/C++ at build time (`mcocomp`) |
| DbConnection | Thread-local (`__thread`), one per thread |
| TransactionLog | Thread-local (`__thread`), tracks per-tx changes |

## MVCC — The Critical Concept

**MVCC** (Multi-Version Concurrency Control): readers never block writers, writers never block readers. Each transaction sees a consistent snapshot.

```
Readers → snapshot isolation (point-in-time view)
Writers → create new versions (old retained for active readers)
```

**Why F5 uses MVCC**: Worker threads (20.x+) need concurrent reads while main thread writes. MURSIW would block all readers during writes.

**The trade-off**: MVCC introduces versioning complexity — handles change, OIDs can diverge, GC is required.

See [full MVCC deep dive](./references/mvcc-and-transactions.md).

## The MVCC OID Mismatch Bug — Most Important Pattern

Under MVCC, when code reads OID from a **schema field** and uses it for **TransactionLog** lookup, the lookup can fail:

```
❌ WRONG (vulnerable to MVCC OID mismatch):
   obj->get(cid_xxx_object_id, &oid);
   TransactionLog::get()->get_log_entry(oid, entry);  // May fail!

✅ CORRECT:
   TransactionLog::get()->get_log_entry(obj->object_id(), entry);
```

**Mechanism**: After `save()`, eXtremeDB may create a work copy at a new physical location → schema field reads stale OID → TransactionLog lookup with stale key → returns NULL → post-transaction kernel op **silently skipped**.

**Known affected**: `Tunnel.cpp`, `Vlan.cpp`, `Vlangroup.cpp`, any validator using `cid_*_object_id` + `get_log_entry()`.

**Why intermittent**: ~1 in 100 — depends on when eXtremeDB relocates work copies (memory pressure, GC, concurrent transactions).

See [full OID mismatch details](./references/mvcc-and-transactions.md#the-mvcc-oid-mismatch-bug-pattern).

## Transaction Lifecycle

```
Main thread (write):
  DbConnection::begin_read_committed_tx()
    → mco_trans_start(db, MCO_READ_WRITE, ...)
  ... CfgObj::create/save/remove ...
  ... TransactionLog tracks all modifications ...
  DbConnection::commit()
    → mco_trans_commit(t)
    → TransactionLog::close_tx_log()

Worker thread (read):
  DbConnection::begin_read_only_tx()
    → mco_trans_start(db, MCO_READ_ONLY, ...)
  ... query via QueryEngine / SQL ...
  DbConnection::commit() or rollback()
```

## Error Code Quick Reference

| Code | Name | Meaning |
|------|------|---------|
| 0 | MCO_S_OK | Success |
| 10 | MCO_S_NOTFOUND | Not found |
| 51 | MCO_E_INVALID_HANDLE | Stale handle (MVCC!) |
| 52 | MCO_E_NOMEM | Shared memory full |
| 53 | MCO_E_ACCESS | Read-only tx tried to write |
| 64 | MCO_E_DELETED | Access to deleted object |
| 80 | MCO_E_SHM_ERROR | Shared memory error |
| 87 | MCO_E_CONFLICT | MVCC write conflict |
| 96 | MCO_E_PINNED_VERSION_LIMIT | Long read tx blocks GC |
| ≥100000 | MCO_ERR_* | Fatal → abort() |

Fatal code decoding: `code / 10000 = category`, `code % 10000 = sub-code`.

See [full error code reference](./references/error-codes-and-fatal-handling.md).

## GDB: Inspecting eXtremeDB State

```gdb
# CAVE DbConnection (thread-local — check thread first!)
(gdb) p Cave::DbConnection::c_db_connection
(gdb) p *((Cave::EdbDbConnection*)Cave::DbConnection::c_db_connection)

# Transaction state
(gdb) p ((Cave::EdbDbConnection*)Cave::DbConnection::c_db_connection)->m_mco_tx

# TransactionLog
(gdb) p Cave::TransactionLog::c_tx_log
(gdb) p *Cave::TransactionLog::c_tx_log
(gdb) p Cave::TransactionLog::c_tx_log->m_modified_objects
(gdb) p Cave::TransactionLog::c_tx_log->m_deleted_objects
```

## Procedure: Database Crash Triage

1. **Check signal**: SIGABRT with `mcp_fatal_error` in backtrace → fatal DB error
2. **Get error code** from `mcp_fatal_error` args → decode category
3. **Check transaction state**: Was a transaction active? Read-only or read-write?
4. **Check thread**: Main thread (write) vs worker (read-only) — worker writing = bug
5. **Check for OID mismatch**: Any `cid_*_object_id` + `get_log_entry()` in call chain?
6. **Check memory**: Is `/dev/shm` healthy? Was `MCO_E_NOMEM` involved?

## References

- [MVCC and transactions](./references/mvcc-and-transactions.md) — MVCC deep dive, versioning, isolation levels, OID mismatch, TransactionLog
- [Error codes and fatal handling](./references/error-codes-and-fatal-handling.md) — Complete error code table, fatal handler chain, GDB inspection
- [CAVE object model](./references/cave-object-model.md) — CfgObj, handles, OIDs, cursors, class hierarchy, type system, source map
