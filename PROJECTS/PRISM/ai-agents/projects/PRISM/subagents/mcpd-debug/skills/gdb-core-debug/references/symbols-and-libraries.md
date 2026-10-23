# Symbols and Libraries Reference

How to set up debug symbols for MCPD core dump analysis on seadev.

## Three Things Must Match

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│ mcpd binary │ ←── │ core dump   │ ←── │ debuginfo RPM    │
│ (rpm -qi)   │     │ (from THIS  │     │ (DWARF symbols   │
│             │     │  binary)    │     │  for THIS binary)│
└─────────────┘     └─────────────┘     └──────────────────┘
       Must be same version+release
```

If mismatched: function names may look correct but **line numbers will be wrong**, struct offsets change → variable values misread → confident, detailed, **wrong** conclusion.

## Verification

```bash
rpm -qi mcpd                              # Binary version+release
cat /etc/PRODUCT_INFO                     # BIG-IP build info
rpm -qa | grep -Ei "mcpd.*(debug|debuginfo)"  # Debuginfo — must match
md5sum /usr/bin/mcpd                      # Binary fingerprint
```

## Getting Debuginfo

```
Option 1: Extract debuginfo RPM on seadev
  mkdir /tmp/debuginfo && cd /tmp/debuginfo
  rpm2cpio mcpd-debuginfo-<matching-version>.rpm | cpio -idmv
  Point GDB: set debug-file-directory /tmp/debuginfo/usr/lib/debug

Option 2: Fetch matching RPM from artifact/build server
  Match Version-Release to mcpd binary
  Extract with rpm2cpio as above

Option 3: Rebuild from matching source
  p4 sync to exact changelist
  make DEBUG=1 (or CFLAGS="-g -O0")

Option 4: Separate .debug file
  objcopy --only-keep-debug mcpd mcpd.debug
  In GDB: symbol-file mcpd.debug
```

## Symbol Status Check

```gdb
(gdb) info sharedlibrary
# "Syms Read" column:
#   Yes = symbols loaded
#   No  = symbols missing for this library
```

**Good output**:
```
#0  MCPConnection::send_response (this=0x..., msg=...) at MCPConnection.cpp:487
```

**Bad output (missing symbols)**:
```
#0  0x00007f4a2b3c4d5e in ?? ()
```

**Partial (common!)**:
```
#0  0x00007f4a1234abcd in ?? ()                    ← libmcpdltm.so, NO symbols
#1  MCPProcessor::process_message (...) at ...     ← mcpd binary, HAS symbols
```

## MCPD Shared Libraries

MCPD is split across 10+ `.so` files. Symbols needed for ALL:

```
mcpd (main binary)
  ├── libmcpdcommon.so       — core framework, connections, processor
  ├── libmcpdltm.so          — LTM validation (virtual servers, pools)
  ├── libmcpdgtm.so          — GTM validation
  ├── libmcpdvalidation.so   — validation pipeline
  ├── libcave*.so            — CAVE/eXtremeDB database layer
  ├── libc.so.6              — C standard library
  ├── libpthread.so.0        — threading
  └── libstdc++.so.6         — C++ standard library
```

If crash is inside `libmcpdltm.so` but you only have symbols for `mcpd`, you'll see the caller but not the crashing function.

## Source Path Mapping

Binary compiled on build server:
```
/build/katkoori/tmos/dns-cp0-64bit-shm/tm_daemon/mcp/framework/MCPProcessor.cpp
```

Your seadev Perforce workspace:
```
/home/katkoori/perforce/katkoori_cp0-shm/depot/tmos/dns-cp0-64bit-shm/tm_daemon/mcp/framework/MCPProcessor.cpp
```

Fix:
```gdb
(gdb) set substitute-path /build/katkoori/tmos /home/katkoori/perforce/katkoori_cp0-shm/depot/tmos
```

Now `(gdb) list` shows local source correctly. Adjust paths based on your actual workspace root.
