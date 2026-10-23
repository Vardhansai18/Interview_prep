# Rocky Linux 8.10 Migration Report — `failover` Daemon

**Module**: `failover`  
**RPM produced**: `sod`  
**Migration date**: 2026-05-27 → 2026-06-10  
**Perforce CL**: 3906962  
**Branch**: `//depot/tmos/rocky-sandbox/`  
**Migrated by**: ByAgent-jiddigi  
**Final status**: ✅ Completed — BUILD_EXIT=0 (Build 4)

---

## 1. Overview

The `failover` daemon (builds to the `sod` RPM) handles system HA state management and MariaDB HA monitoring in TMOS. Migration required 4 build attempts:
- Build 1–2: Missing devfs headers, wrong MariaDB include path, runsm1 Makefile issues
- Build 3: First successful build (original `mysqlhad` binary name)
- Build 4: Successful after `mysqlhad` → `mariadbhad` rename + errdefs registry update

---

## 2. RPM Artifacts (Build 4 — Final)

| RPM | Size | Location |
|-----|------|----------|
| `sod-22.0.0-0.0.103.x86_64.rpm` | 4.2 MB | `RPMS/x86_64/` |
| `sod-coverage-22.0.0-0.0.103.x86_64.rpm` | 6 KB | `RPMS/x86_64/` |

---

## 3. Dependencies Pre-built

| Module | RPMs |
|--------|------|
| `ha_table` | `ha_table-22.0.0-0.0.94.x86_64.rpm`, `ha_table-devel-22.0.0-0.0.94.x86_64.rpm` |
| `mariadb` | Headers at `devfs_x86_64/usr/include/mysql/`, libs at `devfs_x86_64/usr/lib64/` |
| `errdefs` | Rebuilt after `globals.c` registry rename to pick up `BIGIP_MARIADBHAD` subset |

---

## 4. Build Attempts

### Build 1 — FAILED
Missing devfs headers — `ha_table.h` and `mysql.h` not yet in `devfs_x86_64`.
```
fatal error: ha_table/ha_table.h: No such file or directory
fatal error: mysql.h: No such file or directory
```
**Fix**: Built `ha_table` and `mariadb` dependencies first.

---

### Build 2 — FAILED

**Issue 1 — `mysqlha/Makefile`**: Wrong MariaDB include path.
On Rocky 8.10, `mariadb-devel` headers are at `usr/include/mysql/` (backward-compat). `usr/include/mariadb/` does not exist.
```
fatal error: mysql/mysql.h: No such file or directory
```

**Issue 2 — `runsm1/Makefile`**: Four problems:
1. `$(TOPDIR)/devfs` used instead of `$(DEVFS)` — wrong (32-bit/CentOS 7) devfs
2. Missing `-I$(DEVFS)/usr/include/ha_table` — header is in a named subdirectory
3. Missing `-I$(DEVFS)/usr/include/mcp/schema_headers`
4. `-L$(DESTDIR)/usr/lib` instead of `-L$(DEVFS)/usr/$(LIB_DIR)` — Rocky 8.10 uses `lib64`
```
fatal error: ha_table/ha_table.h: No such file or directory
/usr/bin/ld: cannot find -lha_table
```

---

### Build 3 — SUCCESS ✅ (pre-rename)

Result: `BUILD_EXIT=0`
```
Wrote: RPMS/x86_64/sod-22.0.0-0.0.91.x86_64.rpm
```

---

### Build 4 — SUCCESS ✅ (final, post-rename)

Result: `BUILD_EXIT=0`
```
Wrote: RPMS/x86_64/sod-22.0.0-0.0.103.x86_64.rpm
Wrote: RPMS/x86_64/sod-coverage-22.0.0-0.0.103.x86_64.rpm
```

---

## 5. Code Changes

### `tm_daemon/failover/mariadbha/Makefile` (formerly `mysqlha/Makefile`)

MariaDB include path fix:
```makefile
# Before (CentOS 7):
EXTRA_CFLAGS += -I$(DEVFS)/usr/include/mariadb ...

# After (Rocky 8.10):
EXTRA_CFLAGS += -I$(DEVFS)/usr/include/mysql ...
```

### `tm_daemon/failover/runsm1/Makefile`

devfs path, include dirs, lib path:
```makefile
# Before (CentOS 7):
EXTRA_CFLAGS += -I. -I$(TOPDIR)/devfs/usr/include -Wall -DNEEDS_MCPMSG_AUTO
LIBS = -L$(DESTDIR)/usr/lib -lmcpmsg -lmcp -lcpp -lbss -lpthread -lha_table -lrt -lerrdefs

# After (Rocky 8.10):
EXTRA_CFLAGS += -I. -I$(DEVFS)/usr/include -I$(DEVFS)/usr/include/ha_table \
                -I$(DEVFS)/usr/include/mcp/schema_headers -Wall -DNEEDS_MCPMSG_AUTO
LIBS = -L$(DEVFS)/usr/$(LIB_DIR) -lmcpmsg -lmcp -lcpp -lbss -lpthread -lha_table -lrt -lerrdefs
```

### `f5lib/errdefs/globals.c`

Renamed errdefs subset from `MYSQLHAD` to `MARIADBHAD` (same code point `0x4E`):
```c
// Before:
MKGLOBAL("BIGIP_MYSQLHAD",   BIGIP, 0x4E, LOG_LOCAL0, LOG_INFO),
// After:
MKGLOBAL("BIGIP_MARIADBHAD", BIGIP, 0x4E, LOG_LOCAL0, LOG_INFO),
```

### `f5_build/ltm.def.inc`

- Added `context: arch=x86_64` to `failover` build target (x86_64-only)
- Removed spurious `f5py` dependency
- Fixed `libf5daemon` entry indentation

---

## 6. `mysqlhad` → `mariadbhad` Rename

Directory: `tm_daemon/failover/mysqlha/` → `tm_daemon/failover/mariadbha/`

| Old name | New name |
|----------|----------|
| `mysqlhad.cpp` | `mariadbhad.cpp` |
| `mysqlhad_common.h` | `mariadbhad_common.h` |
| `mysql_monitor.cpp` | `mariadb_monitor.cpp` |
| `mysql_monitor.h` | `mariadb_monitor.h` |
| `bigip_mysqlhad_error_defs.in` | `bigip_mariadbhad_error_defs.in` |
| `run_mysqlhad` | `run_mariadbhad` |

Content substitutions:
- `mysqlhad` → `mariadbhad` (binary name, macros, log/shm paths)
- `MYSQLHAD` → `MARIADBHAD` (preprocessor macros and errdefs subset)
- `mysql_monitor.*` → `mariadb_monitor.*` (includes and object targets)

**Note on BigDB keys**: `mcp_listener.cpp` retains `DB_MYSQLHAD_*` macro names because the BigDB runtime key strings (`"mysqlhad.debug"` etc.) are schema-registered and cannot be changed without a separate BigDB migration CL. Only the C macro names that map to `BIGIP_MARIADBHAD` in errdefs were updated.

Other files updated:
- `tm_daemon/failover/Makefile`: `MYSQLHA = mysqlha` → `MYSQLHA = mariadbha`
- `tm_daemon/failover/failover.spec`: `/usr/share/mariadb/mariadbhad`, `bigip_mariadbhad_error_maps.h`

---

## 7. `ha_table` Dependency

Required no source code changes for Rocky 8.10. BUILD_EXIT=0.

| RPMs | `ha_table-22.0.0-0.0.94.x86_64.rpm`, `ha_table-devel-22.0.0-0.0.94.x86_64.rpm` |
|---|---|
| Code changes | `ha_enforcement.c`: `int` → `ssize_t`/`size_t`; `table_util.c`: explicit `(int)` casts |

---

## 8. CL 3906962 Final Contents (71 files)

| Group | Files | Notes |
|-------|-------|-------|
| `f5lib/errdefs/globals.c` | 1 | BIGIP_MYSQLHAD → BIGIP_MARIADBHAD rename |
| `f5_build/ltm.def.inc` | 1 | failover build target fix |
| `tm_daemon/failover/` | 52 | source + mariadbha move/add + mysqlha move/del + runsm1 |
| `tm_lib/ha_table/` | 2 | GCC 11 type fixes |

---

## 9. Key Rocky 8.10 Patterns

| Pattern | CentOS 7 | Rocky 8.10 |
|---------|----------|------------|
| MariaDB headers | `usr/include/mariadb/` | `usr/include/mysql/` |
| devfs variable | `$(TOPDIR)/devfs` | `$(DEVFS)` (= `devfs_x86_64`) |
| Lib path | `usr/lib` | `usr/lib64` (via `$(LIB_DIR)`) |
| Subdirectory headers | `-I/usr/include` | `-I$(DEVFS)/usr/include/ha_table` etc. explicitly |
| Errdefs subset rename | Requires rebuild of `errdefs` module to update devfs headers |

---

## 10. Build Logs

| Attempt | Log | Result |
|---------|-----|--------|
| Build 1 | `logs/orchestor_failover_20260527_234420/failover_build1.log` | FAILED |
| Build 2 | `logs/orchestor_failover_20260527_234420/failover_build2.log` | FAILED |
| Build 3 | `logs/orchestor_failover_20260527_234420/failover_build3.log` | ✅ SUCCESS (pre-rename) |
| Build 4 | `logs/orchestor_failover_20260527_234420/failover_build4.log` | ✅ SUCCESS (final) |
