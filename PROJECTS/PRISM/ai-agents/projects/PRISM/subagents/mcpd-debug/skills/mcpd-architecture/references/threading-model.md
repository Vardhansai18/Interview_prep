# MCPD Threading Model — Full Detail

## Legacy: Single-Threaded (Pre-20.x)

In versions prior to 20.x, MCPD was **entirely single-threaded**. The main thread ran an eventlib-based event loop (`evMainLoop()`) and handled everything:

- Accepting connections
- Receiving requests
- Processing queries AND mutations
- Sending responses
- Database transactions
- HA sync
- Post-transaction kernel operations

**Problem**: When the main thread was occupied with large configurations or processing-intensive requests, clients (SNMP, TMUI, etc.) would **timeout** waiting for responses.

**Key implication for debugging**: The original codebase had **ingrained single-threaded assumptions** about concurrent access. There was no global synchronization because none was needed.

## Multi-Threaded Introduction (20.x)

Version 20.x introduced **worker threads** alongside the main thread:

```
┌─────────────────────────────────────────────────────┐
│                    MCPD PROCESS (20.x)               │
│                                                      │
│  ┌──────────────────────────────────┐                │
│  │     MAIN THREAD (eventlib)       │                │
│  │  ┌─────────────────────────┐     │                │
│  │  │ evMainLoop()            │     │                │
│  │  │  ├─ Socket listeners    │     │                │
│  │  │  ├─ Timer callbacks     │     │                │
│  │  │  ├─ Signal handling     │     │                │
│  │  │  ├─ DB transactions     │     │                │
│  │  │  └─ Validation pipeline │     │                │
│  │  └─────────────────────────┘     │                │
│  └──────────────┬───────────────────┘                │
│                 │ eventfd + lock-free queues          │
│    ┌────────────┼────────────┬──────────┐            │
│    ▼            ▼            ▼          ▼            │
│  ┌──────┐  ┌──────┐   ┌──────┐   ┌──────┐          │
│  │ W-0  │  │ W-1  │   │ W-2  │   │ W-3  │          │
│  │      │  │      │   │      │   │      │          │
│  └──────┘  └──────┘   └──────┘   └──────┘          │
│         Worker threads (default 4)                   │
└─────────────────────────────────────────────────────┘
```

**How it worked in 20.x:**

1. MCPD listens on **port 666 (AF_INET)** and **UNIX socket** (`/var/run/mcp`)
2. **All connections managed by the main thread**
3. Main thread classifies requests as **queries** or **non-queries** (create/modify/delete)
4. **Queries** → offloaded to worker queue → worker threads process → response queue
5. **Non-queries** → handled directly by the main thread (shared object modifications)
6. Main thread sends responses back to clients

**Concurrency model**:
- MVCC in eXtremeDB enables concurrent read + write
- Reads (queries) proceed in parallel on worker threads
- Writes remain serialized on main thread
- Thread-local `MCPDBManager` per thread

**Limitation**: Main thread still owned ALL connections → still a bottleneck for sending responses.

## Dedicated Worker Socket Architecture (21.0+) — COREBIP-35046

Version 21.0 introduced a **new listener socket** architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    MCPD PROCESS (21.0+)                      │
│                                                              │
│  ┌──────────────────────────────────────┐                    │
│  │     MAIN THREAD (eventlib)           │                    │
│  │  ┌──────────────────────────────┐    │                    │
│  │  │ evMainLoop()                 │    │                    │
│  │  │  ├─ Port 666 listener        │    │                    │
│  │  │  ├─ /var/run/mcp listener    │    │                    │
│  │  │  ├─ Timer callbacks          │    │                    │
│  │  │  ├─ Signal handling          │    │                    │
│  │  │  ├─ Non-query processing     │    │                    │
│  │  │  │  (create/modify/delete)   │    │                    │
│  │  │  ├─ DB write transactions    │    │                    │
│  │  │  └─ Validation pipeline      │    │                    │
│  │  └──────────────────────────────┘    │                    │
│  └──────────────┬───────────────────────┘                    │
│                 │ Creates dedicated query socket              │
│    ┌────────────┼────────────┬──────────┐                    │
│    ▼            ▼            ▼          ▼                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  W-0     │ │  W-1     │ │  W-2     │ │  W-3     │       │
│  │  epoll   │ │  epoll   │ │  epoll   │ │  epoll   │       │
│  │  ┌─────┐ │ │  ┌─────┐ │ │  ┌─────┐ │ │  ┌─────┐ │       │
│  │  │query│ │ │  │query│ │ │  │query│ │ │  │query│ │       │
│  │  │sock │ │ │  │sock │ │ │  │sock │ │ │  │sock │ │       │
│  │  └─────┘ │ │  └─────┘ │ │  └─────┘ │ │  └─────┘ │       │
│  │  listen  │ │  listen  │ │  listen  │ │  listen  │       │
│  │  accept  │ │  accept  │ │  accept  │ │  accept  │       │
│  │  recv    │ │  recv    │ │  recv    │ │  recv    │       │
│  │  send    │ │  send    │ │  send    │ │  send    │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  Worker threads — each owns dedicated query connections      │
│  Clients connect DIRECTLY to worker threads for queries      │
└─────────────────────────────────────────────────────────────┘
```

**Key changes:**

1. Main thread creates a **dedicated query socket** and assigns it to a worker
2. Worker threads **listen, accept, and manage** their own connections
3. Each worker runs its own **epoll loop** independently
4. **No cross-thread sharing** of connections
5. When a worker exits, its clients **disconnect and retry** on remaining threads
6. Even when main thread is busy, workers **continue independently**
7. Clients send **user-related auth information** on worker connections

**Supported clients for worker socket:**
- SNMPD, TMUI (extensible to others)

**Request routing in 21.0+:**
- **Write requests** → main thread (same as before)
- **Read requests** → worker threads via dedicated query sockets

## Threading Concerns (Steven Fuerst Review Notes)

> "mcpd business logic doesn't do global synchronization. (It was single threaded, so there are ingrained assumptions about concurrent access.)"

**MVCC handles this at the database layer.** Readers see consistent snapshots without app-level locks.

**However**: Threading bugs are real risks — difficult timing constraints to trigger, may require particular configurations to reproduce. Extensive FT testing was conducted; identified bugs were fixed.

## Debugging Implications

### Thread Identification in GDB

```
Thread 1  = Main thread     → evMainLoop(), MCPProcessor::process_*
Thread 2+ = Worker threads  → epoll_wait(), MCPWorkerService::*
Default: 4 worker threads (threads 2-5)
```

### Key GDB Objects Per Thread

**Main thread:**
```gdb
(gdb) p MCPProcessor::m_instance
(gdb) p *MCPProcessor::m_instance
(gdb) p MCPProcessor::m_db_mgr
(gdb) p MCPProcessor::m_request_group
(gdb) p MCPProcessor::m_processing_request_group_connection
```

**Worker thread:**
```gdb
(gdb) thread N
(gdb) p worker_service
(gdb) p worker_service->m_epoll_fd
(gdb) p worker_service->m_connections
```

### Common Multi-Threading Crash Patterns

1. **NULL MCPConnection in Worker**: Connection freed while worker still processing → `MCPConnection::send_response(this=0x0)`
2. **MVCC OID Mismatch**: Using `cid_*_object_id` instead of `obj->object_id()` → silent failure → later crash
3. **writev() EAGAIN Loop**: EAGAIN on first writev(), messages stuck in in-progress list → watchdog kill
4. **Race on shared state**: Application-level data structures shared between main and workers may lack synchronization

### JIRA Reference

| Ticket | Description | Status |
|--------|-------------|--------|
| COREBIP-35046 | TMOS: Multi-threading MCPd - robustness and improvements | Done |
