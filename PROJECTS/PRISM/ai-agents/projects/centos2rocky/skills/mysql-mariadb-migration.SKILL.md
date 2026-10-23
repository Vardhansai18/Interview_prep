---
name: mysql-mariadb-migration
description: Domain knowledge for migrating TMOS applications from MySQL Enterprise 5.5.53 to MariaDB 10.11.10 on Rocky Linux 8.10. Covers RPM spec file changes, C/C++ client API differences, library linking, SQL compatibility, configuration changes, and build system updates.
applyTo: ["**/*.c", "**/*.cpp", "**/*.cc", "**/*.h", "**/*.hpp", "**/*.spec", "**/Makefile*", "**/*.mk", "**/*.cmake", "**/CMakeLists.txt", "**/*.sql", "**/*.cnf", "**/*.cfg", "**/*.conf"]
---

# MySQL to MariaDB Migration Guide: MySQL Enterprise 5.5.53 → MariaDB 10.11.10

This skill provides comprehensive guidance for migrating TMOS applications from MySQL Enterprise 5.5.53 to MariaDB 10.11.10 on Rocky Linux 8.10, covering breaking changes, API updates, spec file modifications, build system changes, and SQL compatibility.

## Overview

### Why MariaDB on Rocky Linux 8.10

Rocky Linux 8.10 does not ship MySQL Enterprise. MariaDB 10.11.10 is the supported drop-in replacement available through the standard Rocky Linux 8.10 repositories (AppStream). MariaDB 10.11 is a Long-Term Support (LTS) release and maintains high compatibility with MySQL 5.5 at the C client API level, but has key differences that require source-level changes.

### Version Comparison Summary

| Feature | MySQL Enterprise 5.5.53 | MariaDB 10.11.10 |
|---|---|---|
| Default charset | `latin1` | `utf8mb4` |
| Default sql_mode | (permissive) | STRICT + `ONLY_FULL_GROUP_BY` |
| Client library | `libmysqlclient.so.18` | `libmariadb.so.3` |
| pkg-config name | `mysql` | `mariadb` |
| devel package | `mysql-enterprise-devel` | `mariadb-connector-c-devel` |
| Header path | `/usr/include/mysql/` | `/usr/include/mariadb/` |
| Socket default | `/var/lib/mysql/mysql.sock` | `/var/lib/mysql/mysql.sock` (same) |
| Auth plugin default | `mysql_native_password` | `mysql_native_password` (same) |
| `INFORMATION_SCHEMA` | Partial | Extended |
| `SHOW EXPLAIN` | No | Yes |

---

## 1. RPM Spec File Changes (MANDATORY)

Every `.spec` file that depends on MySQL Enterprise must be updated with the following three changes.

### 1a. BuildRequires — Replace MySQL devel with MariaDB Connector/C

**Before:**
```spec
BuildRequires: mysql-enterprise-devel
BuildRequires: mysql-enterprise-devel >= 5.5
BuildRequires: MySQL-devel
BuildRequires: mysql-devel
```

**After:**
```spec
BuildRequires: mariadb-connector-c-devel >= 3.0
```

> **Note:** `mariadb-connector-c-devel` provides `mysql/mysql.h` as a compatibility header at `/usr/include/mysql/mysql.h` via a symlink to `/usr/include/mariadb/mysql.h`. Most source code including `<mysql/mysql.h>` will continue to compile without changes.

### 1b. Runtime Requires — Replace MySQL libs with MariaDB libs

**Before:**
```spec
Requires: mysql-enterprise-libs
Requires: mysql-enterprise-shared
Requires: MySQL-shared
Requires: mysql-libs
```

**After:**
```spec
Requires: mariadb-connector-c >= 3.0
```

### 1c. Remove MySQL Enterprise-specific Requires

Remove any references to MySQL Enterprise-specific packages that do not exist on Rocky Linux:

```spec
# REMOVE these lines entirely:
Requires: mysql-enterprise-server
Requires: mysql-enterprise-client
BuildRequires: mysql-enterprise-server
BuildRequires: mysql-enterprise-client
```

If the application needs a running MySQL/MariaDB **server** at runtime (not just the client library), use:
```spec
Requires: mariadb-server >= 10.3
```

### 1d. Full Spec Example — Before and After

**Before:**
```spec
%package devel
Summary: Development files for %{name}
BuildRequires: mysql-enterprise-devel >= 5.5.53
BuildRequires: mysql-enterprise-shared >= 5.5.53
Requires: mysql-enterprise-libs >= 5.5

%build
MYSQL_CFLAGS=$(mysql_config --cflags)
MYSQL_LIBS=$(mysql_config --libs)
```

**After:**
```spec
%package devel
Summary: Development files for %{name}
BuildRequires: mariadb-connector-c-devel >= 3.0

%build
MYSQL_CFLAGS=$(mariadb_config --cflags)
MYSQL_LIBS=$(mariadb_config --libs)
```

---

## 2. C/C++ Header Changes

### 2a. Include Path Compatibility

MariaDB Connector/C provides compatibility headers. The following includes work with **no change** required in most cases:

```c
/* These still work — MariaDB provides compat symlinks */
#include <mysql/mysql.h>
#include <mysql/mysql_version.h>
#include <mysql/errmsg.h>
#include <mysql/mysqld_error.h>
```

If the source uses the native MariaDB path directly, use:
```c
/* Native MariaDB path (also acceptable) */
#include <mariadb/mysql.h>
```

**Action required only if:** the include path is hardcoded to a MySQL Enterprise-specific location such as `/usr/local/mysql/include/` or `/opt/mysql/include/`.

**Fix:**
```c
/* BEFORE — hardcoded MySQL Enterprise path */
#include "/usr/local/mysql/include/mysql.h"

/* AFTER — use system include */
#include <mysql/mysql.h>
```

### 2b. Version Macros

MySQL-specific version macros that may be used in `#ifdef` guards:

| Old Macro | MariaDB Equivalent | Notes |
|---|---|---|
| `MYSQL_VERSION_ID` | `MYSQL_VERSION_ID` | Still present, value differs |
| `MYSQL_SERVER_VERSION` | `MYSQL_SERVER_VERSION` | Still present |
| `LIBMYSQL_VERSION` | `MARIADB_CLIENT_VERSION_STR` | Use for client library version |
| `LIBMYSQL_VERSION_ID` | `MARIADB_CLIENT_VERSION` | Numeric version |

**Version check migration:**
```c
/* BEFORE — MySQL Enterprise version guard */
#if MYSQL_VERSION_ID >= 50553
    /* MySQL 5.5.53 specific code */
#endif

/* AFTER — MariaDB has MYSQL_VERSION_ID = 100 * major*100 + minor*100 + patch */
/* MariaDB 10.11.10 MYSQL_VERSION_ID = 101110 */
#if defined(MARIADB_BASE_VERSION)
    /* MariaDB-specific code path */
#elif MYSQL_VERSION_ID >= 50553
    /* MySQL-specific code path */
#endif
```

To detect MariaDB at compile time:
```c
#ifdef MARIADB_BASE_VERSION
    /* Compiled against MariaDB Connector/C */
#endif
```

---

## 3. C/C++ API Changes

### 3a. Functions Removed or Changed

The following MySQL 5.5 functions require attention when migrating to MariaDB 10.11:

#### `mysql_num_fields()` on `MYSQL*`

MySQL 5.5 allowed passing a `MYSQL*` connection handle to `mysql_num_fields()` to get the number of fields from the last result. MariaDB requires a `MYSQL_RES*`.

```c
/* BEFORE — MySQL 5.5 allowed MYSQL* (non-standard usage) */
MYSQL *conn = mysql_init(NULL);
mysql_real_query(conn, query, strlen(query));
unsigned int num = mysql_num_fields(conn);  /* BROKEN in MariaDB */

/* AFTER — always use MYSQL_RES* */
MYSQL *conn = mysql_init(NULL);
mysql_real_query(conn, query, strlen(query));
MYSQL_RES *res = mysql_store_result(conn);
if (res) {
    unsigned int num = mysql_num_fields(res);
    mysql_free_result(res);
}
```

#### `mysql_thread_init()` / `mysql_thread_end()`

Still present in MariaDB but behaviour changed slightly. Both are now effectively no-ops in MariaDB Connector/C 3.x as thread-safety is handled automatically.

```c
/* BEFORE — explicit thread init/end required in MySQL 5.5 */
mysql_thread_init();
/* ... run queries on this thread ... */
mysql_thread_end();

/* AFTER — still safe to call but not required; keep for source compatibility */
/* No change needed if already calling these; they are no-ops in MariaDB 3.x */
```

#### `mysql_library_init()` / `mysql_library_end()`

Still present and required for multi-threaded applications. No change needed.

```c
/* No change required — still works */
if (mysql_library_init(0, NULL, NULL)) {
    fprintf(stderr, "Could not initialize MySQL library\n");
    exit(1);
}
/* ... use MySQL/MariaDB ... */
mysql_library_end();
```

#### `my_bool` Type

MySQL 5.5 used `my_bool` (typedef of `char`) for boolean parameters. MariaDB Connector/C 3.x deprecated `my_bool` in favour of plain `bool`/`int`.

```c
/* BEFORE — MySQL 5.5 */
my_bool reconnect = 1;
mysql_options(conn, MYSQL_OPT_RECONNECT, &reconnect);

/* AFTER — MariaDB 10.11 / Connector/C 3.x */
/* Option 1: Keep my_bool — still defined as a typedef for compatibility */
my_bool reconnect = 1;  /* OK, still compiles */

/* Option 2: Use int or bool — preferred */
int reconnect = 1;
mysql_options(conn, MYSQL_OPT_RECONNECT, &reconnect);
```

> If the compiler emits `-Wdeprecated-declarations` for `my_bool`, change to `int`.

#### `MYSQL_OPT_RECONNECT` Behaviour Change

In MariaDB 10.11, auto-reconnect resets the connection state (prepared statements, transactions, locks, user variables). This was also true in MySQL 5.5 but is worth verifying in application logic.

```c
/* Explicit disable of auto-reconnect (recommended for TMOS daemons) */
int reconnect = 0;
mysql_options(conn, MYSQL_OPT_RECONNECT, &reconnect);
```

### 3b. Functions Behaving Differently

| Function | MySQL 5.5 Behaviour | MariaDB 10.11 Behaviour | Action |
|---|---|---|---|
| `mysql_real_escape_string()` | Escapes for connection charset | Same, but charset may differ if default changed to utf8mb4 | Verify charset at connection time |
| `mysql_affected_rows()` | Returns `(my_ulonglong)-1` on error | Same | No change |
| `mysql_insert_id()` | Returns last AUTO_INCREMENT id | Same | No change |
| `mysql_errno()` | Returns error number | Same | No change |
| `mysql_field_count()` | Returns number of columns in last result | Same | No change |

### 3c. Prepared Statement API

The prepared statement API (`mysql_stmt_*`) is fully compatible. No changes required for:
- `mysql_stmt_init()`
- `mysql_stmt_prepare()`
- `mysql_stmt_bind_param()`
- `mysql_stmt_execute()`
- `mysql_stmt_fetch()`
- `mysql_stmt_close()`

---

## 4. Build System Changes

### 4a. pkg-config

**Before (MySQL Enterprise):**
```makefile
# MySQL Enterprise provided mysql_config or pkg-config 'mysql'
MYSQL_CFLAGS := $(shell mysql_config --cflags)
MYSQL_LIBS   := $(shell mysql_config --libs)

# Or via pkg-config
MYSQL_CFLAGS := $(shell pkg-config --cflags mysql)
MYSQL_LIBS   := $(shell pkg-config --libs mysql)
```

**After (MariaDB):**
```makefile
# MariaDB provides mariadb_config and pkg-config 'mariadb'
MYSQL_CFLAGS := $(shell mariadb_config --cflags)
MYSQL_LIBS   := $(shell mariadb_config --libs)

# Or via pkg-config
MYSQL_CFLAGS := $(shell pkg-config --cflags mariadb)
MYSQL_LIBS   := $(shell pkg-config --libs mariadb)
```

> **Compatibility note:** `mysql_config` is also provided by `mariadb-connector-c-devel` as a wrapper script. Existing Makefiles using `mysql_config` will continue to work **without changes** as long as `mariadb-connector-c-devel` is installed and `mysql-enterprise-devel` is not.

### 4b. Linker Flags

**Before:**
```makefile
LDLIBS += -lmysqlclient
# or
LDLIBS += -lmysqlclient_r   # thread-safe variant (deprecated in MySQL 5.5.3+)
```

**After:**
```makefile
# Option 1: Use mariadb_config (preferred)
LDLIBS += $(shell mariadb_config --libs)

# Option 2: Direct — MariaDB provides libmariadb and a compatibility symlink libmysqlclient
LDLIBS += -lmariadb

# Option 3: -lmysqlclient still works if mariadb-connector-c installs compat symlink
LDLIBS += -lmysqlclient
```

> Check if `/usr/lib64/libmysqlclient.so` exists after installing `mariadb-connector-c`. If it does, `-lmysqlclient` works with no linker change.

```bash
# Verify compat symlinks after installing mariadb-connector-c-devel
ls -la /usr/lib64/libmysqlclient* /usr/lib64/libmariadb*
```

### 4c. CMake-based Builds

**Before:**
```cmake
find_package(MySQL REQUIRED)
include_directories(${MYSQL_INCLUDE_DIR})
target_link_libraries(mytarget ${MYSQL_LIBRARIES})
```

**After:**
```cmake
# Option 1: Use pkg-config
find_package(PkgConfig REQUIRED)
pkg_check_modules(MARIADB REQUIRED mariadb)
include_directories(${MARIADB_INCLUDE_DIRS})
target_link_libraries(mytarget ${MARIADB_LIBRARIES})

# Option 2: Direct path (if find_package(MySQL) still resolves via compat headers)
find_package(MySQL REQUIRED)  # May still work if compat package installed
include_directories(${MYSQL_INCLUDE_DIR})
target_link_libraries(mytarget ${MYSQL_LIBRARIES})
```

---

## 5. SQL Compatibility Changes

### 5a. Default sql_mode (Critical)

This is the most common source of runtime failures when migrating from MySQL 5.5 to MariaDB 10.11.

**MySQL 5.5.53 default sql_mode:** (effectively empty — very permissive)

**MariaDB 10.11 default sql_mode:**
```
STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

**Impact on existing SQL:**

```sql
-- MySQL 5.5: Inserts empty string silently
-- MariaDB 10.11 STRICT mode: ERROR — Data too long / invalid value
INSERT INTO t (int_col) VALUES ('');

-- MySQL 5.5: Inserts 0 for out-of-range
-- MariaDB 10.11 STRICT mode: ERROR — Out of range
INSERT INTO t (tinyint_col) VALUES (999);

-- MySQL 5.5: Allows zero dates
-- MariaDB 10.11 (with NO_ZERO_DATE): WARNING or ERROR
INSERT INTO t (date_col) VALUES ('0000-00-00');
```

**Fix — set sql_mode at connection time in application code:**
```c
/* After connecting, set compatible sql_mode */
const char *sql = "SET SESSION sql_mode = ''";
if (mysql_query(conn, sql)) {
    fprintf(stderr, "Failed to set sql_mode: %s\n", mysql_error(conn));
}
```

**Or in `/etc/my.cnf.d/mariadb-server.cnf`:**
```ini
[mysqld]
sql_mode = NO_ENGINE_SUBSTITUTION
```

### 5b. `ONLY_FULL_GROUP_BY` Enforcement

MariaDB 10.11 enforces `ONLY_FULL_GROUP_BY` by default in some configurations. This causes queries that select non-aggregated columns not present in `GROUP BY` to fail.

```sql
-- MySQL 5.5: OK (permissive GROUP BY)
SELECT id, name, MAX(value)
FROM my_table
GROUP BY id;

-- MariaDB 10.11 with ONLY_FULL_GROUP_BY: ERROR
-- Fix: include all non-aggregated columns in GROUP BY
SELECT id, name, MAX(value)
FROM my_table
GROUP BY id, name;

-- Or use ANY_VALUE() for intentional non-deterministic selection
SELECT id, ANY_VALUE(name), MAX(value)
FROM my_table
GROUP BY id;
```

### 5c. Character Set: `latin1` → `utf8mb4`

**MySQL 5.5:** Default charset is `latin1`.

**MariaDB 10.11:** Default charset is `utf8mb4`.

This affects:
- Column widths (VARCHAR(255) in utf8mb4 uses up to 4 bytes per character vs 1 for latin1)
- Index key length limits (max 767 bytes for InnoDB with `ROW_FORMAT=COMPACT`)
- String comparison and collation

**Fix — explicit charset at connection:**
```c
/* Preserve MySQL 5.5 behaviour — connect with latin1 */
mysql_options(conn, MYSQL_SET_CHARSET_NAME, "latin1");

/* Or set utf8mb4 explicitly if application supports it */
mysql_options(conn, MYSQL_SET_CHARSET_NAME, "utf8mb4");
```

**Or in SQL after connect:**
```c
mysql_query(conn, "SET NAMES 'latin1'");
/* Or: */
mysql_query(conn, "SET NAMES 'utf8mb4'");
```

### 5d. `AUTO_INCREMENT` with `REPLACE`

MySQL 5.5 and MariaDB differ in how `AUTO_INCREMENT` counter advances on `REPLACE INTO`:

```sql
-- MariaDB may increment AUTO_INCREMENT counter differently on REPLACE
-- If application relies on INSERT ID after REPLACE, verify behaviour:
REPLACE INTO t (id, val) VALUES (1, 'new');
SELECT LAST_INSERT_ID();  -- Value may differ between MySQL 5.5 and MariaDB 10.11
```

### 5e. `TIMESTAMP` Default Behaviour

**MySQL 5.5:** First `TIMESTAMP` column in a table auto-gets `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` implicitly.

**MariaDB 10.11:** This implicit behaviour is controlled by `explicit_defaults_for_timestamp` (on by default in strict mode). Explicit `DEFAULT` clauses must be present.

```sql
-- MySQL 5.5: first TIMESTAMP gets implicit defaults
CREATE TABLE t (
    id INT,
    created TIMESTAMP  -- MySQL 5.5 implicitly adds DEFAULT CURRENT_TIMESTAMP
);

-- MariaDB 10.11 (explicit_defaults_for_timestamp=ON): no implicit defaults
-- Fix: make defaults explicit
CREATE TABLE t (
    id INT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## 6. Configuration File Changes

### 6a. Server Configuration (`/etc/my.cnf`)

MySQL Enterprise 5.5 configuration keys that changed or were removed in MariaDB 10.11:

| MySQL 5.5 Option | MariaDB 10.11 Equivalent | Notes |
|---|---|---|
| `innodb_additional_mem_pool_size` | **Removed** | Remove from config — no replacement |
| `innodb_file_format` | **Removed** | InnoDB Barracuda is always used |
| `innodb_file_format_max` | **Removed** | Remove from config |
| `innodb_large_prefix` | **Removed** | Always enabled in MariaDB 10.11 |
| `table_cache` | `table_open_cache` | Renamed; old name still accepted |
| `thread_concurrency` | **Removed** (Linux) | Remove from config |
| `skip-locking` | `skip-external-locking` | Renamed |
| `log` | `general_log_file` | Renamed |

**Fix — scan and clean config:**
```bash
# Find and remove deprecated options from my.cnf
grep -n "innodb_additional_mem_pool_size\|innodb_file_format\|innodb_large_prefix\|thread_concurrency" /etc/my.cnf
```

### 6b. Client Configuration (`/etc/my.cnf` `[client]` section)

```ini
# No changes required for basic client configuration
[client]
socket = /var/lib/mysql/mysql.sock
default-character-set = latin1
```

---

## 7. Common Compilation Errors and Fixes

### Error: `mysql_config: command not found`

```
configure: error: mysql_config executable not found
```

**Fix:**
```bash
# Install mariadb-connector-c-devel
sudo dnf install mariadb-connector-c-devel

# Verify mysql_config is available (provided by mariadb-connector-c-devel)
which mysql_config
mysql_config --version
```

### Error: `cannot find -lmysqlclient`

```
/usr/bin/ld: cannot find -lmysqlclient
```

**Fix:**
```bash
# Check if compat symlink exists
ls -la /usr/lib64/libmysqlclient*

# If not present, create symlink or change -lmysqlclient to -lmariadb
# In Makefile:
# BEFORE: LDLIBS += -lmysqlclient
# AFTER:  LDLIBS += -lmariadb
```

### Error: `mysql.h: No such file or directory`

```
fatal error: mysql/mysql.h: No such file or directory
```

**Fix:**
```bash
# Verify mariadb-connector-c-devel is installed
rpm -q mariadb-connector-c-devel

# Check header location
ls /usr/include/mysql/mysql.h
ls /usr/include/mariadb/mysql.h

# If header is only at /usr/include/mariadb/, update include path in Makefile:
# CFLAGS += -I/usr/include/mariadb
```

### Error: `my_bool` deprecated warnings

```
warning: 'my_bool' is deprecated [-Wdeprecated-declarations]
```

**Fix — replace `my_bool` with `int`:**
```c
/* BEFORE */
my_bool flag = 1;

/* AFTER */
int flag = 1;
```

Or suppress for transition period (add to CFLAGS in spec `%build`):
```makefile
CFLAGS += -Wno-deprecated-declarations
```

### Error: `undefined reference to mysql_*`

```
undefined reference to `mysql_init'
undefined reference to `mysql_real_connect'
```

**Fix — ensure -lmariadb or -lmysqlclient is in link flags:**
```makefile
# In Makefile add after existing LDLIBS or LIBS:
LDLIBS += $(shell mariadb_config --libs)
```

### Error: `Package 'mysql' not found` (pkg-config)

```
Package 'mysql' not found
```

**Fix — use 'mariadb' package name for pkg-config:**
```makefile
# BEFORE
CFLAGS += $(shell pkg-config --cflags mysql)

# AFTER
CFLAGS += $(shell pkg-config --cflags mariadb)
```

---

## 8. Migration Checklist

Use this checklist for each TMOS module being migrated from MySQL Enterprise 5.5.53 to MariaDB 10.11.10:

### Spec File
- [ ] Replace `mysql-enterprise-devel` with `mariadb-connector-c-devel` in `BuildRequires`
- [ ] Replace `mysql-enterprise-libs` / `mysql-enterprise-shared` with `mariadb-connector-c` in `Requires`
- [ ] Remove any `mysql-enterprise-server` / `mysql-enterprise-client` references
- [ ] Update `mysql_config` calls to `mariadb_config` if present in `%build` section

### Source Code (C/C++)
- [ ] Verify `#include <mysql/mysql.h>` paths — update if hardcoded to `/opt/mysql` or `/usr/local/mysql`
- [ ] Replace `my_bool` with `int` if `-Wdeprecated-declarations` warnings appear
- [ ] Check all `mysql_num_fields()` calls — ensure they receive `MYSQL_RES*` not `MYSQL*`
- [ ] Verify sql_mode is set explicitly at connection time if application relies on permissive mode
- [ ] Check character set is set explicitly with `mysql_options(conn, MYSQL_SET_CHARSET_NAME, ...)`
- [ ] Replace `-lmysqlclient` with `-lmariadb` or `$(mariadb_config --libs)` if link fails
- [ ] Update `pkg-config mysql` to `pkg-config mariadb` in Makefiles

### Build Verification
- [ ] `mariadb-connector-c-devel` is installed on the build machine
- [ ] `mysql_config --version` or `mariadb_config --version` shows MariaDB version
- [ ] Module compiles without errors
- [ ] RPM is generated successfully
- [ ] No `mysql-enterprise*` RPMs remain in `Requires`/`BuildRequires`

### Runtime Verification
- [ ] Application connects successfully to MariaDB 10.11 server
- [ ] All SQL queries execute without `sql_mode` errors
- [ ] Character encoding is consistent with original MySQL 5.5 behaviour
- [ ] No data truncation or out-of-range errors from STRICT mode

---

## 9. TMOS-Specific Patterns

### 9a. Packages That Typically Depend on MySQL Enterprise in TMOS

Common TMOS modules that may have MySQL Enterprise dependencies:

- `mcpd` — MCP daemon, may use MySQL client for config DB
- `mysql-enterprise` — The MySQL Enterprise package itself (replace with `mariadb`)
- Any module with `MYSQL` or `mysql` in its `BuildRequires` or source includes

### 9b. Finding MySQL Dependencies in Source

```bash
# Find all source files including mysql headers
grep -r "#include.*mysql" --include="*.c" --include="*.cpp" --include="*.h" .

# Find all spec files referencing mysql-enterprise
grep -r "mysql-enterprise\|mysql-devel\|MySQL-devel" --include="*.spec" .

# Find all Makefiles using mysql_config or -lmysqlclient
grep -r "mysql_config\|lmysqlclient\|pkg-config.*mysql" --include="Makefile*" --include="*.mk" .
```

### 9c. Verifying MariaDB Installation on Rocky Linux 8.10

```bash
# Check available MariaDB packages
dnf list mariadb* 2>/dev/null

# Install client library and devel headers
sudo dnf install mariadb-connector-c mariadb-connector-c-devel

# Verify installation
rpm -q mariadb-connector-c mariadb-connector-c-devel
mysql_config --version
pkg-config --modversion mariadb

# Check header and library paths
ls /usr/include/mysql/mysql.h
ls /usr/lib64/libmariadb.so*
ls /usr/lib64/libmysqlclient.so*   # compat symlink, may or may not exist
```

### 9d. Using the `mysql-enterprise` Module Stub Spec

If the build system requires `mysql-enterprise` as a virtual provide (to satisfy other modules' `Requires: mysql-enterprise`), update or create a stub spec that provides the virtual name:

```spec
Name:    mysql-enterprise
Version: 5.5.53
Release: rocky_compat
Summary: Compatibility stub — provides mysql-enterprise virtual package

Provides: mysql-enterprise = %{version}
Provides: mysql-enterprise-libs = %{version}
Provides: mysql-enterprise-shared = %{version}
Requires: mariadb-connector-c >= 3.0

%description
Compatibility stub that provides the mysql-enterprise virtual package name
for TMOS modules migrated to Rocky Linux 8.10, backed by MariaDB Connector/C.
```
