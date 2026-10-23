---
name: mcpd-architecture
description: "MCPD architecture knowledge for F5 BIG-IP core dump analysis. Use when: analyzing MCPD crashes, debugging mcpd core dumps, understanding MCPD threading model, tracing request processing pipeline, identifying connection handling bugs, understanding main thread vs worker thread behavior, examining MCPProcessor MCPConnection MCPWorkerService MCPDBMgr request_group ValidationManager PostTransMgr code paths."
argument-hint: "Describe the crash context or which MCPD subsystem you need architecture knowledge for"
---

# MCPD Architecture Skill

Foundational knowledge for debugging MCPD (Master Control Program Daemon) on F5 BIG-IP TMOS. Load this skill FIRST before any MCPD core dump analysis.

## When to Use

- Analyzing any MCPD core dump or crash
- Tracing a backtrace through MCPD code to understand the execution context
- Determining if a crash is in main thread vs worker thread
- Understanding the request processing pipeline (CHECKPOINT → COMMIT → DELETE → PostTransMgr → PubSub)
- Identifying which source file corresponds to a function in a backtrace
- Understanding how MCPD communicates with TMM, clusterd, SNMPD, TMUI

## What is MCPD

MCPD — **Master Control Program Daemon** — is the central configuration management daemon on F5 BIG-IP TMOS. It is the single source of truth for system configuration.

- Owns the configuration database (eXtremeDB/CAVE in `/dev/shm/`)
- Handles ALL CRUD operations for configuration objects
- Validates changes through a multi-stage pipeline
- Manages HA synchronization between peers
- Communicates with TMM, clusterd, snmpd, and other subsystems
- Executes post-transaction kernel operations (TAP interfaces, routes, etc.)

**An MCPD crash is a P1/Sev1 event.**

```
Architecture:   x86_64 (64-bit, always)
Database:       eXtremeDB v8.4 with MVCC
IPC:            UNIX sockets (/var/run/mcp), TCP port 666, eventfd
Entry point:    framework/MCPMain.cpp → main()
Source:         tm_daemon/mcp/
```

## Threading Model (Summary)

MCPD's threading model evolved across three versions. See [full threading details](./references/threading-model.md).

| Version | Model | Key Characteristic |
|---------|-------|--------------------|
| Pre-20.x | Single-threaded | `evMainLoop()` handles everything; no concurrency |
| 20.x | Main + worker threads | Workers process queries via queue; main thread owns ALL connections |
| 21.0+ | Dedicated worker sockets | Workers listen/accept/send/recv on their own query sockets; SNMPD and TMUI connect directly to workers |

**Thread identification in GDB:**
```
Thread 1  = Main thread    → evMainLoop(), MCPProcessor::process_*
Thread 2+ = Worker threads → epoll_wait(), MCPWorkerService::*
Default: 4 worker threads
```

**Critical rule**: Writes (create/modify/delete) → main thread only. Reads (queries) → worker threads.

## Request Processing Pipeline (Summary)

```
Client Request → MCPProcessor::process_message() → request_group::process()
  │
  ├─ CHECKPOINT_HANDLER  — Early validation (name, uniqueness)
  ├─ COMMIT_HANDLER      — Final validation (addresses, types, deps)
  ├─ DELETE_HANDLER       — Pre-delete dependency check
  ├─ object_deleted_event — Post-delete cleanup
  ├─ PostTransMgr         — Kernel operations (TAP, routes, etc.)
  └─ MCPPubSub::publish() — Notify subscribers (TMM, snmpd)
```

Each object type registers handlers via `REGISTER_CLASS_MGR()`. Missing handlers cause crashes.

## Connection Architecture (Summary)

| Socket | Type | Handled By |
|--------|------|------------|
| Port 666 | AF_INET TCP | Main thread |
| `/var/run/mcp` | AF_UNIX | Main thread |
| Query socket(s) | 21.0+ | Worker threads |

**MCPConnection key fields** (for GDB):
```
m_fd, m_state, m_worker_id, m_send_list, m_in_progress_list, m_recv_buf
```

See [full connection lifecycle and IPC channels](./references/components-source-map.md).

## Database Layer (Summary)

- **eXtremeDB v8.4** with MVCC — concurrent readers + single writer
- **CAVE** — F5's C++ abstraction layer over eXtremeDB
- **Storage**: `/dev/shm/mcp*` (shared memory)
- **Thread-local** `MCPDBManager` instances per thread

```
⚠️  MVCC OID CAVEAT:
    ALWAYS use:  obj->object_id()
    NEVER use:   obj->get(cid_xxx_object_id, &oid)
    The schema field can diverge from runtime OID after save().
```

For deep eXtremeDB/CAVE knowledge, load the `extremedb-architecture` skill.

## Procedure: Using This Skill During Analysis

1. **Identify the crashing thread** — check `(gdb) info threads` against the threading model above
2. **Map the backtrace to source files** — use the [backtrace lookup table](./references/components-source-map.md)
3. **Identify the pipeline stage** — which handler was active? Check the request pipeline
4. **Check for multi-threading implications** — see [threading details](./references/threading-model.md) for connection ownership rules and the 21.0+ architecture
5. **Check error codes** — see [error codes and fatal paths](./references/validation-errors-ha.md)
6. **If crash involves eXtremeDB/CAVE** — load the `extremedb-architecture` skill for MVCC, transaction, and OID knowledge

## Key Error Codes (Quick Reference)

| Code | Name | Meaning |
|------|------|---------|
| 8 | MCPDERR_FATAL_DATABASE_ERROR | eXtremeDB fatal → abort() |
| 89 | MCPDERR_FATAL_HA_TABLE_ERROR | HA table corruption → abort() |
| 7 | MCPDERR_SHUTDOWN_SIGNAL | Clean shutdown (not a crash) |
| 930 | MCPDERR_ASSERTION_FAILED | assert() triggered |

Full error codes and fatal paths: [validation-errors-ha.md](./references/validation-errors-ha.md)

## Reference Files

| File | Content |
|------|---------|
| [threading-model.md](./references/threading-model.md) | Full threading evolution with diagrams (pre-20.x, 20.x, 21.0+/COREBIP-35046), debugging implications |
| [components-source-map.md](./references/components-source-map.md) | 18-component table, directory tree, backtrace→source lookup, IPC diagram |
| [validation-errors-ha.md](./references/validation-errors-ha.md) | Validation pipeline stages, error codes, fatal error path, HA details |
