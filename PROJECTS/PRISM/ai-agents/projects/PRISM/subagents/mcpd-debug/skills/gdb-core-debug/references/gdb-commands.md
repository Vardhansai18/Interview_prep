# GDB Commands Reference

Commands organized by purpose for MCPD core dump analysis on seadev.

## Starting GDB

```bash
# Basic
gdb <mcpd-binary> <core-file>

# Full setup in one command
gdb <mcpd-binary> <core-file> \
  -ex "set sysroot /home/<user>/debug/rootfs" \
  -ex "set solib-search-path /home/<user>/debug/rootfs/usr/lib64" \
  -ex "set debug-file-directory /home/<user>/debug/debuginfo/usr/lib/debug" \
  -ex "set substitute-path /build/<user>/tmos /home/<user>/perforce/<ws>/depot/tmos"

# Batch mode (dump to file)
gdb <mcpd-binary> <core-file> -batch \
  -ex "bt" -ex "bt full" -ex "info threads" -ex "thread apply all bt" \
  -ex "info registers" -ex "x/i \$rip" \
  2>&1 | tee /tmp/gdb_analysis.txt
```

## First Commands (Crash Context)

```gdb
(gdb) info signal                   # What signal killed the process
(gdb) bt                            # Crashing thread backtrace
(gdb) bt full                       # With local variables
(gdb) info threads                  # All threads
(gdb) thread apply all bt           # All thread backtraces
(gdb) thread apply all bt 5         # Quick: top 5 frames per thread
```

## Examining the Crash Point

```gdb
(gdb) frame 0                       # Go to crash frame
(gdb) info args                     # Function arguments
(gdb) info locals                   # Local variables
(gdb) list                          # Source code at this point
(gdb) info registers                # All register values
(gdb) x/i $rip                      # Faulting machine instruction
(gdb) p $_siginfo                   # Signal info (si_signo, si_addr)
```

## Memory Examination

```gdb
(gdb) x/8gx <addr>                  # 8 × 64-bit words
(gdb) x/16wx <addr>                 # 16 × 32-bit words
(gdb) x/32bx <addr>                 # 32 raw bytes
(gdb) x/s <addr>                    # Null-terminated string
(gdb) x/10i <addr>                  # Disassemble 10 instructions
(gdb) x/16gx $rsp                   # Stack contents
(gdb) info proc mappings            # Full memory map — is address valid?
```

## Thread Commands

```gdb
(gdb) info threads                   # List threads with current location
(gdb) thread <N>                     # Switch to thread N
(gdb) thread                         # Show current thread
(gdb) thread apply all bt            # Backtrace every thread
(gdb) thread apply all bt full       # Every thread with locals
(gdb) thread apply all bt 5          # Top 5 frames per thread
```

## Frame Navigation

```gdb
(gdb) frame 0                       # Jump to crash point
(gdb) frame 3                       # Jump to frame 3
(gdb) up                            # Move toward caller
(gdb) down                          # Move toward callee
(gdb) up 3                          # Move 3 frames up
(gdb) info args                     # Arguments at current frame
(gdb) info locals                   # Locals at current frame
(gdb) list                          # Source at current frame
```

## Symbol and Library Commands

```gdb
(gdb) info sharedlibrary             # Loaded libraries + symbol status
(gdb) set solib-search-path <path>   # Where to find .so files
(gdb) set sysroot <path>             # Root for library resolution
(gdb) set substitute-path <old> <new># Map build paths to local paths
(gdb) symbol-file <file>             # Load separate .debug file
(gdb) sharedlibrary <pattern>        # Force-load symbols for library
(gdb) set debug-file-directory <dir> # Where to find .debug files
```

## Printing and Evaluating

```gdb
(gdb) p <expr>                       # Print C/C++ expression
(gdb) p *ptr                         # Dereference pointer
(gdb) p/x <expr>                     # Print in hex
(gdb) p (char*)strerror(errno)       # Last errno as string
(gdb) p $_siginfo                    # Signal info structure
```

## Output Settings

```gdb
(gdb) set pagination off             # Don't pause between pages
(gdb) set print pretty on            # Format structs readably
(gdb) set print object on            # Show dynamic C++ types
(gdb) set print demangle on          # Demangled C++ names
(gdb) set confirm off                # Don't ask "are you sure?"
```

## MCPD-Specific Inspections

```gdb
# Processor singleton
(gdb) p *MCPProcessor::m_instance

# Active transaction
(gdb) p *MCPProcessor::m_request_group
(gdb) p MCPProcessor::m_processing_request_group_connection

# Database manager (TLS — check thread first!)
(gdb) p *MCPProcessor::m_db_mgr

# Connection state
(gdb) p conn->m_fd; p conn->m_state; p conn->m_worker_id
(gdb) p conn->m_send_list; p conn->m_in_progress_list

# Worker thread state
(gdb) p worker_service->m_epoll_fd
(gdb) p worker_service->m_connections

# CAVE/eXtremeDB
(gdb) p Cave::DbConnection::c_db_connection
(gdb) p *((Cave::EdbDbConnection*)Cave::DbConnection::c_db_connection)
(gdb) p Cave::TransactionLog::c_tx_log
```

## Version Mismatch Detection

```gdb
(gdb) bt
# If line numbers seem "off by a few" → version mismatch

(gdb) list
# If source doesn't match function name → mismatch

(gdb) info sharedlibrary
# If lib versions differ from rpm -qi → mismatch
```
