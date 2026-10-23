---
name: component-mapping
description: "Domain knowledge for mapping BIG-IP source file paths to Bugzilla components. USE FOR tasks involving validating Bugzilla component assignments, extracting source paths from backtraces, looking up the mcpd component map CSV, and understanding the mcpd subdirectory structure. Provides the CSV format, key mappings, mcpd directory reference, and extraction rules for both backtrace formats."
---

## COMPONENT MAPPING OVERVIEW

The component mapping file maps BIG-IP source file paths to Bugzilla component names. It is the **source of truth** for validating whether a bug is assigned to the correct component.

**File location:** `shared/component_mappings/bigip_component_map.csv`

**CSV format:**
```
<source_path_prefix>,<bugzilla_component>
```

Example entries:
```
tm_daemon/mcp/,a_MCP_FRAMEWORK
tm_daemon/mcp/apm/,a_MCP_APM
tm_daemon/mcp/authz/,a_MCP_AUTH
tm_daemon/mcp/ltm/,LTM
tm_daemon/mcp/sys/,SYS
tm_daemon/mcp/net/,NET
tm_daemon/mcp/gtm/,GTM_DNS
```

**Matching rule:** Use the **longest prefix match** from the CSV. More specific paths override general ones.

Example:
- `tm_daemon/mcp/apm/APMConfig.cpp` → matches `tm_daemon/mcp/apm/` → `a_MCP_APM` ✓
- `tm_daemon/mcp/framework/MCPConnection.cpp` → matches `tm_daemon/mcp/` → `a_MCP_FRAMEWORK` ✓

---

## KEY MCPD COMPONENT MAPPINGS

| Source Path | Bugzilla Component | Subsystem Description |
|-------------|-------------------|----------------------|
| `tm_daemon/mcp/` | `a_MCP_FRAMEWORK` | Default mcpd — core framework, message handling, DB layer |
| `tm_daemon/mcp/framework/` | `a_MCP_FRAMEWORK` | MCPConnection, request_group, db_modify_request |
| `tm_daemon/mcp/apm/` | `a_MCP_APM` | Access Policy Manager config objects |
| `tm_daemon/mcp/authz/` | `a_MCP_AUTH` | Authorization, user management, audit |
| `tm_daemon/mcp/ltm/` | `LTM` | Virtual servers, pools, profiles, monitors |
| `tm_daemon/mcp/sys/` | `SYS` | System provisioning, platform, SNMP |
| `tm_daemon/mcp/net/` | `NET` | Interfaces, VLANs, routes, tunnels, ARP |
| `tm_daemon/mcp/gtm/` | `GTM_DNS` | Global Traffic Manager, DNS, Wide IPs |
| `tm_daemon/mcp/clustering/` | `a_MCP_CLUST` | HA clustering, failover, config sync |
| `tm_daemon/mcp/firewall/` | `AFM` | Advanced Firewall Manager (AFM) policies |
| `tm_daemon/mcp/asm/` | `ASM` | Application Security Manager (WAF) |
| `tm_daemon/mcp/pem/` | `PEM` | Policy Enforcement Manager |
| `tm_daemon/mcp/licensing/` | `LIC` | License management |
| `tm_daemon/mcp/validation/` | `a_MCP_FRAMEWORK` | Config validation logic (falls under framework) |
| `tm_daemon/mcp/utils/` | `a_MCP_FRAMEWORK` | Shared utilities (falls under framework) |
| `tm_daemon/mcp/postgres/` | `a_MCP_FRAMEWORK` | Database interaction layer |
| `tm_daemon/mcp/staging/` | `a_MCP_FRAMEWORK` | Staging/transaction handling |

---

## MCPD SUBDIRECTORY REFERENCE

Complete reference for navigating the mcpd source tree:

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `tm_daemon/mcp/framework/` | Core framework | `MCPConnection.cpp`, `request_group.cpp`, `db_modify_request.cpp`, `MCPDaemon.cpp` |
| `tm_daemon/mcp/authz/` | Authorization & auth | `Audit.cpp`, `UserDB.cpp`, `RoleDB.cpp` |
| `tm_daemon/mcp/ltm/` | LTM objects | `VirtualServer.cpp`, `Pool.cpp`, `Node.cpp`, `Profile*.cpp` |
| `tm_daemon/mcp/sys/` | System objects | `Provision.cpp`, `Platform.cpp`, `SNMP*.cpp` |
| `tm_daemon/mcp/net/` | Network objects | `Interface.cpp`, `Vlan.cpp`, `Route.cpp`, `Tunnel.cpp` |
| `tm_daemon/mcp/gtm/` | GTM/DNS objects | `WideIP.cpp`, `GtmServer.cpp`, `GtmPool.cpp` |
| `tm_daemon/mcp/apm/` | APM objects | `APMPolicy.cpp`, `AccessProfile.cpp` |
| `tm_daemon/mcp/clustering/` | HA/clustering | `CMIDevice.cpp`, `FailoverState.cpp`, `ConfigSync.cpp` |
| `tm_daemon/mcp/firewall/` | AFM firewall | `FirewallPolicy.cpp`, `FirewallRule.cpp` |
| `tm_daemon/mcp/asm/` | ASM/WAF | `ASMPolicy.cpp`, `ASMSignature.cpp` |
| `tm_daemon/mcp/postgres/` | DB layer | `PGConn.cpp`, `PGQuery.cpp` |
| `tm_daemon/mcp/staging/` | Transactions | `StagingDB.cpp`, `Transaction.cpp` |

---

## EXTRACTING SOURCE PATHS FROM BACKTRACES

### Format 1: F5 Custom Backtrace
Pattern: `[ NN ] <library> <function> ( <file>:<line> )`

```
[ 04 ] libmcpdcommon.so    MCPConnection::sendMessage()    ( MCPConnection.cpp:1267 )
```

- The filename is relative to the library's source root
- For `libmcpdcommon.so` frames: prepend `tm_daemon/mcp/` and look up subdirectory by filename
- `MCPConnection.cpp` → `tm_daemon/mcp/framework/MCPConnection.cpp` → `a_MCP_FRAMEWORK`

**Filename to subdirectory hints:**
| Filename pattern | Likely subdirectory |
|-----------------|---------------------|
| `MCPConnection.*`, `request_group.*`, `db_*` | `framework/` |
| `Audit.*`, `UserDB.*`, `RoleDB.*` | `authz/` |
| `VirtualServer.*`, `Pool.*`, `Profile*.*` | `ltm/` |
| `Interface.*`, `Vlan.*`, `Route.*` | `net/` |
| `CMIDevice.*`, `FailoverState.*` | `clustering/` |
| `APM*.*`, `Access*.*` | `apm/` |
| `PGConn.*`, `PGQuery.*` | `postgres/` |

### Format 2: GDB Standard Backtrace
Pattern: `#N ... at <file_path>:<line>`

```
#2  audit_remove_ltcfg_passwords (...) at authz/Audit.cpp:333
#4  db_modify_request::apply_msg_to_db (...) at framework/db_modify_request.cpp:1207
```

- The path after `at` is **already relative to `tm_daemon/mcp/`**
- `authz/Audit.cpp` → `tm_daemon/mcp/authz/Audit.cpp`
- `framework/db_modify_request.cpp` → `tm_daemon/mcp/framework/db_modify_request.cpp`
- Apply longest prefix match against CSV

---

## COMPONENT VALIDATION PROCEDURE

1. **Extract source file paths** from the backtrace (see above)
2. **Read the CSV**: `shared/component_mappings/bigip_component_map.csv`
3. **Find longest matching prefix** for each path
4. **Compare** the found component against the bug's current `<component>` field
5. **Report verdict:**

```
Component assignment is CORRECT: a_MCP_FRAMEWORK
```
or
```
Component should be changed from a_MCP_APM to a_MCP_FRAMEWORK
The crash is in tm_daemon/mcp/framework/MCPConnection.cpp which maps to a_MCP_FRAMEWORK.
```

---

## COMPONENT VALIDATION NOTES

- **When backtrace has multiple components**: use the component of the **earliest unique mcpd frame** (closest to the crash trigger)
- **When no source paths are available**: use the bug description's mentioned features/iControl objects to infer the component. State this is an inference, not a confirmed mapping.
- **`a_MCP_FRAMEWORK`** is the catch-all for generic mcpd crashes where no more specific subdirectory is identified
- **Frames from `libc`, `libpthread`, `libstdc++`**: skip for component mapping — these are system libraries
- **Frames from `libmcpdcommon.so`** with no source path: classify as `a_MCP_FRAMEWORK` by default
