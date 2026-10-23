# MCPD Key Components & Source Map

## Component Table

| Component | Source File(s) | Responsibility |
|-----------|---------------|----------------|
| Entry point | `framework/MCPMain.cpp` | `main()`, signal setup, init sequence |
| Event processor | `framework/MCPProcessor.cpp` | Singleton — processes all requests |
| Connections | `framework/MCPConnection.cpp` | IPC connections, send/recv, writev() |
| Worker threads | `framework/MCPWorkerService.cpp` | Per-thread epoll, signal masking, query socket |
| DB manager | `framework/MCPDBMgr.cpp` | eXtremeDB/CAVE init/shutdown, fatal error handler |
| Request handling | `framework/request.cpp` | Base request class |
| Request groups | `framework/request_group.cpp` | Batched transaction processing |
| Validation | `framework/ValidationManager.cpp` | N-stage validation pipeline |
| Post-transaction | `framework/PostTransMgr.cpp` | Kernel operations after DB commit |
| HA manager | `framework/MCPHAMgr.cpp` | High availability sync |
| Pub/Sub | `framework/MCPPubSub.cpp` | Config change notifications |
| Listeners | `framework/MCPListener.cpp` | Socket listeners (main + query) |
| Epoll wrapper | `framework/epoll.cpp` | EpollManager for workers |
| Schema manager | `framework/CfgSchemaClassMgr.cpp` | CAVE schema validation |
| Debug/Assertions | `framework/DebugCheck.cpp/.h` | mcpd_assert(), debug checks |
| Audit | `framework/audit_request.cpp` | Audit logging |
| Folder mgr | `framework/FolderMgr.cpp` | Folder/partition management |
| Error codes | `bigip_mcpd_error_defs.in` | ALL error code definitions (~4540 lines) |

## Codebase Directory Structure

```
tm_daemon/mcp/
│
├── framework/                          # ★ CORE (start here for most crashes)
│   ├── MCPMain.cpp                     # main(), signal handlers
│   ├── MCPProcessor.cpp/.h             # Event loop, request dispatch
│   ├── MCPConnection.cpp/.h            # Connections, send/recv
│   ├── MCPWorkerService.cpp/.h         # Worker threads, query socket (21.0+)
│   ├── MCPDBMgr.cpp/.h                # Database, fatal error handler
│   ├── request_group.cpp/.h            # Transaction processing
│   ├── db_modify_request.cpp/.h        # CRUD operations
│   ├── ValidationManager.cpp/.h        # Validation pipeline
│   ├── PostTransMgr.cpp/.h             # Post-commit kernel ops
│   ├── MCPHAMgr.cpp/.h                # HA management
│   ├── MCPPubSub.cpp/.h               # Pub/Sub notifications
│   ├── MCPListener.cpp/.h              # Socket listeners
│   ├── epoll.cpp/.h                    # Epoll wrapper
│   ├── DebugCheck.cpp/.h               # Assertions
│   ├── CfgSchemaClassMgr.cpp/.h        # Schema management
│   └── ... (50+ more files)
│
├── net/validation/                      # Network objects
│   ├── RouteMgmtEntry.cpp/.h           # Management routes
│   ├── RouteStaticEntry.cpp/.h         # Static routes
│   ├── RouteDomain.cpp/.h              # Route domains
│   ├── Tunnel.cpp/.h                   # Tunnels (MVCC bug-prone)
│   ├── Vlan.cpp/.h                     # VLANs (MVCC bug-prone)
│   ├── SelfIp.cpp/.h                   # Self IPs
│   └── routing.cpp                     # VnicMgr
│
├── ltm/validation/                      # LTM objects
│   ├── VirtualServer*.cpp/.h
│   ├── Pool*.cpp/.h
│   ├── Monitor*.cpp/.h
│   ├── Rule*.cpp/.h
│   └── Profile*.cpp/.h
│
├── sys/validation/                      # System objects
│   ├── DbVariable*.cpp/.h
│   ├── Interface.cpp/.h
│   └── AdminIp.cpp/.h
│
├── centmgmt/validation/                 # Central management
│   └── Device.cpp/.h
│
└── clustering/                          # Clustering
    └── Cluster.cpp/.h
```

## Backtrace → Source File Quick Reference

```
IF backtrace contains...            THEN look in...
───────────────────────────────────────────────────────────
MCPMain::                         → framework/MCPMain.cpp
MCPProcessor::                    → framework/MCPProcessor.cpp
MCPConnection::                   → framework/MCPConnection.cpp
MCPWorkerService::                → framework/MCPWorkerService.cpp
request_group::                   → framework/request_group.cpp
db_modify_request::               → framework/db_modify_request.cpp
ValidationManager::               → framework/ValidationManager.cpp
PostTransMgr::                    → framework/PostTransMgr.cpp
MCPDBMgr::                       → framework/MCPDBMgr.cpp
MCPHAMgr::                       → framework/MCPHAMgr.cpp
EpollManager::                    → framework/epoll.cpp
MCPPubSub::                      → framework/MCPPubSub.cpp
FolderMgr::                      → framework/FolderMgr.cpp
CfgSchemaClassMgr::              → framework/CfgSchemaClassMgr.cpp
mco_* / MCO_*                    → eXtremeDB library (external)
cave_* / Cave::                  → CAVE layer (f5lib/cave/lib/)

VirtualServer*::                 → ltm/validation/VirtualServer*.cpp
Pool*::                          → ltm/validation/Pool*.cpp
Monitor*::                       → ltm/validation/Monitor*.cpp
RouteMgmtEntry*::                → net/validation/RouteMgmtEntry.cpp
Tunnel*::                        → net/validation/Tunnel.cpp
Vlan*::                          → net/validation/Vlan.cpp
SelfIp*::                        → net/validation/SelfIp.cpp
DbVariable*::                    → sys/validation/DbVariable*.cpp
Device*::                        → centmgmt/validation/Device.cpp
```

## Communication Channels (IPC)

```
┌──────────┐  /var/run/mcp         ┌──────────────────────┐
│  tmsh    │◄─────────────────────►│                      │
│ iControl │  127.0.0.1:port       │                      │
│  REST    │◄─────────────────────►│     MAIN THREAD      │
│  GUI     │                       │   (port 666 + unix)  │
└──────────┘                       │                      │
                                   │                      │
┌──────────┐  127.2.0.2            │                      │
│   HAL    │◄─────────────────────►│                      │
└──────────┘                       │                      │
                                   │                      │
┌──────────┐  TMM IP addr          │                      │
│   TMM    │◄─────────────────────►│                      │
└──────────┘                       │                      │
                                   │                      │
┌──────────┐  MCP protocol         │                      │
│ clusterd │◄─────────────────────►│                      │
└──────────┘                       └──────────────────────┘

                  21.0+ Query Path:
┌──────────┐  query socket         ┌──────────────────────┐
│  SNMPD   │◄────────────────────►│   WORKER THREAD(s)   │
│  TMUI    │  (direct connection)  │   (epoll, own conns) │
└──────────┘                       └──────────────────────┘
```

## Connection Lifecycle — Main Thread

```
Client connects (port 666 or /var/run/mcp)
    │
    ▼
Main thread accepts → MCPConnection object created
    │
    ▼
Main thread receives message → MCPProcessor::process_message()
    │
    ├── Query? YES → Offload to worker queue (20.x) or redirect to worker socket (21.0+)
    │   NO → Process directly on main thread (create/modify/delete)
    │
    ▼
Response sent back over same connection
```

## Connection Lifecycle — Worker Thread (21.0+)

```
Client connects to worker's dedicated query socket
    │
    ▼
Worker thread accepts via epoll → manages connection
    │
    ▼
Worker receives query → processes (DB read via MVCC) → sends response directly
    │
    (Main thread NOT involved)
```

## MCPConnection State (GDB Fields)

```
MCPConnection:
  m_fd                — Socket file descriptor
  m_state             — Connection state machine
  m_worker_id         — Which worker owns this (-1 = main thread)
  m_send_list         — Messages queued for sending
  m_in_progress_list  — Messages being sent (partial send state)
  m_recv_buf          — Receive buffer
```
