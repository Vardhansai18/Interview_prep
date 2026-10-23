---
name: gdb-core-debug
description: "GDB core dump analysis for MCPD on F5 BIG-IP. Use when: opening a core dump in GDB, examining backtraces, checking symbols, analyzing crash signals (SIGSEGV SIGABRT SIGBUS), inspecting thread state, reading registers, diagnosing NULL pointer dereference use-after-free assertion failure fatal database error EAGAIN stuck loop worker thread crash patterns. Environment: seadev Linux server, x86_64, 64-bit ELF."
argument-hint: "Describe the crash symptom, signal, or GDB output you need help interpreting"
---

# GDB Core Dump Analysis Skill

Everything needed to analyze MCPD core dumps using GDB on a seadev server.

## When to Use

- Opening an MCPD core dump for the first time
- Interpreting GDB output (backtraces, registers, memory dumps)
- Diagnosing crash signals (SIGSEGV, SIGABRT, SIGBUS)
- Verifying binary/core/debuginfo version match
- Navigating multi-threaded backtraces
- Identifying common MCPD crash patterns

## Environment

Analysis is always on a **seadev server** (Linux dev machine), NOT on BIG-IP:
- mcpd binary (from BIG-IP or matching build)
- Core file (copied from BIG-IP)
- Debug symbols (debuginfo RPM extracted, or debug build with `-g`)
- Source code (Perforce workspace on the seadev)

```
Architecture:  x86_64 (64-bit always)
Binary:        ELF 64-bit LSB executable
Core:          ELF 64-bit LSB core file
```

## Procedure

### Step 1: Verify Architecture & Versions

```bash
file <mcpd-binary>    # Must say: ELF 64-bit LSB executable, x86-64
file <core-file>      # Must say: ELF 64-bit LSB core file, x86-64
```

Binary, core, and debuginfo RPM must be from the **exact same build**. Version mismatch → wrong line numbers, wrong struct offsets, **wrong conclusions**.

```bash
rpm -qi mcpd                         # Version+Release of binary
rpm -qa | grep -Ei "mcpd.*debug"     # Debuginfo version — must match
```

### Step 2: Launch GDB with Proper Setup

```bash
gdb <mcpd-binary> <core-file> \
  -ex "set sysroot /home/<user>/debug/rootfs" \
  -ex "set solib-search-path /home/<user>/debug/rootfs/usr/lib64" \
  -ex "set debug-file-directory /home/<user>/debug/debuginfo/usr/lib/debug" \
  -ex "set substitute-path /build/<user>/tmos /home/<user>/perforce/<ws>/depot/tmos"
```

### Step 3: Check Symbols

```gdb
(gdb) bt
```

| Output | Meaning |
|--------|---------|
| `function_name() at file.cpp:123` | Symbols working |
| `0x00007f... in ?? ()` | Symbols missing — fix with solib-search-path |
| Partial (some `??`, some named) | Need symbols for specific `.so` — see [shared libraries](./references/symbols-and-libraries.md) |

### Step 4: Identify the Signal

```gdb
(gdb) bt             # Frame 0 reveals signal type
(gdb) p $_siginfo    # Signal details (si_signo, si_addr)
```

| Signal | # | Meaning | Next Action |
|--------|---|---------|-------------|
| SIGSEGV | 11 | Bad memory access | Check `this`, args, registers for NULL/garbage |
| SIGABRT | 6 | Deliberate abort | Look for `__assert_fail` or `mcp_fatal_error` in backtrace |
| SIGBUS | 7 | Alignment/mmap fault | Check `/dev/shm` mappings |
| SIGKILL | 9 | External kill (OOM/watchdog) | Usually no core; check for hang patterns |

### Step 5: Analyze Backtrace — All Threads

```gdb
(gdb) bt full                    # Crashing thread with locals
(gdb) info threads               # Thread list
(gdb) thread apply all bt 5      # Quick overview all threads
```

**Thread roles** (see [full threading details](./references/crash-patterns.md)):
- Thread 1 (main): `evMainLoop()`, `MCPProcessor::*`, validation, DB transactions
- Thread 2+ (workers): `epoll_wait()`, `MCPWorkerService::*`, I/O

### Step 6: Walk Frames to Find Root Cause

```
Frame 0:   WHERE — what instruction faulted
Frame 1-3: WHO/WHY — who passed the bad value
Frame 5+:  CONTEXT — what high-level operation (delete, sync, startup)
```

```gdb
(gdb) frame 0
(gdb) info args; info locals; info registers; x/i $rip
(gdb) frame 1
(gdb) info args; info locals; list
```

### Step 7: Inspect MCPD-Specific State

```gdb
(gdb) p *MCPProcessor::m_instance                          # Processor singleton
(gdb) p *MCPProcessor::m_request_group                     # Active transaction
(gdb) p MCPProcessor::m_processing_request_group_connection # Triggering client
(gdb) p *MCPProcessor::m_db_mgr                            # DB manager
```

**TLS warning**: `__thread` variables differ per thread. Always `(gdb) thread N` first.

### Step 8: Match to Known Crash Pattern

See [crash patterns reference](./references/crash-patterns.md) for detailed signatures:

| Pattern | Signal | Key Indicator |
|---------|--------|---------------|
| NULL pointer deref | SIGSEGV | `this=0x0` or arg=0x0 |
| Use-after-free | SIGSEGV | Non-null ptr, garbage fields (`0xdeadbeef`) |
| Fatal DB error | SIGABRT | `mcp_fatal_error` in backtrace, error code ≥ 100000 |
| Assertion failure | SIGABRT | `__assert_fail` with condition string |
| Worker connection crash | SIGSEGV | Thread 2+ crashed in `MCPConnection::send_*` |
| EAGAIN stuck loop | SIGKILL/hang | Main thread in `writev()` loop, workers idle |

## Quick GDB Command Reference

See [full command reference](./references/gdb-commands.md) organized by purpose.

```gdb
# Essential first commands
bt; bt full; info threads; thread apply all bt
info signal; info registers; x/i $rip

# Memory inspection
x/8gx <addr>; info proc mappings; p $_siginfo

# Navigation
frame N; up; down; thread N

# Symbols
info sharedlibrary; set solib-search-path; set substitute-path

# Output settings
set pagination off; set print pretty on; set print object on
```

## Backtrace → Source File Map

```
MCPProcessor::       → framework/MCPProcessor.cpp
MCPConnection::      → framework/MCPConnection.cpp
MCPWorkerService::   → framework/MCPWorkerService.cpp
request_group::      → framework/request_group.cpp
ValidationManager::  → framework/ValidationManager.cpp
PostTransMgr::       → framework/PostTransMgr.cpp
MCPDBMgr::           → framework/MCPDBMgr.cpp
MCPHAMgr::           → framework/MCPHAMgr.cpp
mco_* / MCO_*        → eXtremeDB library (external, no source)
cave_* / Cave::      → CAVE layer (framework/ directory)
```

## References

- [Crash patterns](./references/crash-patterns.md) — Detailed signatures for 6 common crash types with GDB investigation steps
- [GDB commands](./references/gdb-commands.md) — Commands organized by purpose: startup, crash point, memory, threads, symbols, printing
- [Symbols and libraries](./references/symbols-and-libraries.md) — Debuginfo extraction, symbol fixing, source path mapping, MCPD shared libraries
