# Crash Patterns Reference

Detailed GDB signatures for the most common MCPD crash types.

## MCPD Thread Roles

```
Thread 1 (main thread):
  Backtrace shows: evMainLoop(), MCPProcessor::process_*, request_group::*, validation handlers
  Responsibility: ALL database transactions, validation, post-commit kernel ops
  If crashed: Usually logic bug — bad validation, missing null check, MVCC issue

Threads 2–5 (worker threads):
  Backtrace shows: epoll_wait(), MCPWorkerService::worker_*, MCPConnection::send/recv
  Responsibility: I/O — reading requests, writing responses
  Each connection pinned to ONE worker (no cross-thread sharing)
  If crashed: Usually connection lifecycle bug — use-after-free, stale pointer
```

### Healthy vs Unhealthy Thread States

```
HEALTHY (idle):
  Workers:     epoll_wait() or poll()      — waiting for I/O
  Main:        evMainLoop() / evGetNext()  — waiting for next event

UNHEALTHY:
  All threads: __lll_lock_wait             — deadlock
  Main:        tight loop in writev()      — EAGAIN handling bug
  Worker:      crashed in send/recv        — connection use-after-free
  Main:        mcp_fatal_error → abort()   — database corruption
  Any:         1000+ frame deep backtrace  — stack overflow
```

---

## Pattern 1: NULL Pointer Dereference

**Signal**: SIGSEGV (11)

**GDB signature**:
```
#0  MCPConnection::send_response (this=0x0, msg=...) at MCPConnection.cpp:487
```
Or:
```
(gdb) info registers
rdi            0x0                 0
(gdb) x/i $rip
=> mov    0x8(%rdi),%eax          # tried to read address 0x8 — unmapped
```

**Investigation**:
```gdb
(gdb) frame 0
(gdb) info args          # Is 'this' or an argument 0x0?
(gdb) frame 1
(gdb) info args          # Who passed the NULL value?
(gdb) info locals        # Was it a failed lookup returning NULL?
(gdb) list               # Missing NULL check before the call?
```

**Common MCPD causes**:
- Connection closed between lookup and use
- Database object deleted, cached pointer now NULL
- Missing null check after `get()` / `find()` returns

---

## Pattern 2: Use-After-Free

**Signal**: SIGSEGV (11)

**GDB signature**: Non-null pointer, but fields contain garbage:
```
(gdb) p *this
$1 = {m_fd = 1718579301, m_state = -1412567295, ...}   ← garbage values
```

**Memory inspection**:
```gdb
(gdb) x/8gx <ptr>
0x...: 0xdeadbeefdeadbeef 0xdeadbeefdeadbeef  ← freed memory poison
# Or:
0x...: 0x0000000000000000 0x0000000000000000  ← zeroed after free
# Or:
0x...: 0x00007f4a12345678 0x000000050000001a  ← reused by another allocation
```

**Investigation**:
```gdb
(gdb) info proc mappings     # Is address still mapped?
(gdb) x/8gx <ptr>            # What does memory contain?
(gdb) bt full                 # Where was this pointer obtained?
(gdb) thread apply all bt     # Did another thread free this object?
```

**Common MCPD causes**:
- Connection closed by main thread while worker still has pointer
- Object deleted from DB but cached pointer not cleared
- Iterator invalidated by concurrent modification

---

## Pattern 3: Fatal Database Error

**Signal**: SIGABRT (6)

**GDB signature**:
```
#0  __GI_raise (sig=6)
#1  __GI_abort ()
#2  MCPDBMgr::mcp_fatal_error (this=0x..., err_code=8)
#3  MCPDBMgr::db_checkpoint (this=0x...)
```

**Investigation**:
```gdb
(gdb) frame 2
(gdb) info args              # err_code tells which DB error
(gdb) frame 3
(gdb) info args; info locals # What operation was in progress
```

Error code decoding: `code / 10000 = category`, `code % 10000 = sub-code`

| Base | Category |
|------|----------|
| 100000 | Database internal |
| 130000 | Page memory buffer |
| 150000 | Heap manager |
| 160000 | Object allocator |

**Common causes**: Shared memory corruption, transaction too large, MVCC bug

---

## Pattern 4: Assertion Failure

**Signal**: SIGABRT (6)

**GDB signature**:
```
#0  __GI_raise (sig=6)
#1  __GI_abort ()
#2  __assert_fail (assertion=0x... "conn != NULL", file=0x... "MCPWorkerService.cpp", line=234)
#3  MCPWorkerService::worker_handle_response (this=0x...)
```

**Investigation**:
```gdb
(gdb) frame 2
(gdb) info args     # 'assertion' = condition, 'file'+'line' = location
(gdb) frame 3
(gdb) list           # See assertion in source context
(gdb) info locals    # Check each variable in the assertion
```

**Key**: Assertion tells WHAT was wrong. Call chain tells WHY.

---

## Pattern 5: Worker Thread Connection Crash

**Signal**: SIGSEGV (11) in a worker thread

**GDB signature**:
```
Thread 3 (LWP 12345):
#0  MCPConnection::send_msg (this=0x0, ...) at MCPConnection.cpp:512
#1  MCPWorkerService::worker_handle_write_ready (this=0x..., fd=17)
#2  MCPWorkerService::worker_epoll_loop (this=0x...)
```

**Investigation**:
```gdb
(gdb) p conn                  # NULL? Non-null but freed?
(gdb) p conn->m_fd            # -1 = closed
(gdb) p conn->m_state         # Connection state
(gdb) p conn->m_worker_id     # Matches this worker?
(gdb) thread 1
(gdb) bt                      # Was main thread closing connections?
```

**Root cause**: Main thread frees connection → worker still holds pointer → crash.

---

## Pattern 6: EAGAIN Stuck Loop

**Signal**: SIGKILL (9) from watchdog — or hang

**GDB signature**:
```
Thread 1 (main):
#0  writev()
#1  MCPConnection::send_worker_msg (this=0x...) at MCPConnection.cpp:445
#2  MCPConnection::process_send (this=0x...) at MCPConnection.cpp:398
#3  MCPProcessor::process_pending_sends

Threads 2-5 (workers):
#0  epoll_wait ()    ← workers idle
```

**Investigation**:
```gdb
(gdb) p conn->m_send_list          # Messages waiting
(gdb) p conn->m_in_progress_list   # Messages stuck after EAGAIN
```

**Root cause**: `writev()` returns EAGAIN on first attempt → 0 bytes sent → messages moved to in-progress list but can't be resent.

---

## MVCC OID Trap (Cross-reference)

When examining code in GDB, if you see `cid_*_object_id` being used to fetch an OID that's later passed to `get_log_entry()`, **flag it** as a potential MVCC mismatch:

```
WRONG (stale after save):     obj->get(cid_xxx_object_id, &oid)
RIGHT (always current):       obj->object_id()
```

See the `extremedb-architecture` skill for full MVCC details.
