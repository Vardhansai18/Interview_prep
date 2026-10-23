# mcpd Bug Triage Report — Strategy-Oriented

**Generated:** 2026-05-05  
**Scope:** 100 most recent parent bugs (non-clone, non-duplicate) across mcpd components  
**Components:** a_MCP_FRAMEWORK, a_MCP_LTM, a_MCP_NET, a_MCP_AUTH, a_MCP_APM, a_MCP_GTM, CGN_MCP  
**Source:** https://bugzilla.olympus.f5net.com

Bugs are grouped into **13 strategy categories**. Each category maps to a distinct resolution workflow.

---

## Category Overview

| # | Category | Count | Priority |
|---|----------|-------|----------|
| 1 | 🔴 Crash / Core Dump | 3 | CRITICAL |
| 3 | 🟠 Memory Safety / Security Risk | 21 | HIGH |
| 4 | 🟡 Null Dereference / Uninitialized Variable | 36 | MEDIUM |
| 5 | 🟡 Dead Code / Unchecked Return Value | 20 | LOW |
| 7 | 🟠 Config Load / State Corruption | 6 | HIGH |
| 8 | 🟠 Transaction / Concurrency | 1 | HIGH |
| 9 | 🟠 Authentication / Security Policy | 6 | HIGH |
| 10 | 🟢 Error Message / Usability / Logging | 1 | LOW |
| 11 | 🔵 RFE / Enhancement | 1 | BACKLOG |
| 12 | ⚪ Build / Test Infrastructure | 4 | IMMEDIATE |
| 13 | ⚪ Miscellaneous / Bucket | 1 | LOW |
| | **Total** | **100** | |

> 74 of 100 bugs are from a bulk Coverity scan (656xxx), split across CAT3-CAT5 by risk.
> Active operational bugs are in the 659xxx-663xxx range.

---

## 🔴 Crash / Core Dump (3)

Crash bugs are split into **8 sub-types** with distinct resolution approaches.
The sub-type determines the investigation workflow — do not treat all crashes identically.

### Sub-type Taxonomy

| Sub-type | Signal | Evidence | Complexity | Core File? |
|----------|--------|----------|------------|------------|
| **CAT1a** Null Pointer / SIGSEGV | SIGSEGV (11) | Dereference of null/0x0 in backtrace | Low–Med | ✅ Yes |
| **CAT1b** Assertion Failure / SIGABRT | SIGABRT (6) | `__assert_fail` / `abort()` in backtrace | Low–Med | ✅ Yes |
| **CAT1c** Memory Corruption / UAF | SIGSEGV or SIGABRT | Corrupted heap, no obvious null; Valgrind/ASan needed | High | ✅ Yes |
| **CAT1d** Stack Overflow / Recursion | SIGSEGV (11) | Same function repeating in backtrace; guard-page SEGV | Medium | ✅ Yes |
| **CAT1e** OOM Kill | — (no signal) | `/var/log/messages`: `oom_kill_process`; RSS growing without bound | High | ❌ No |
| **CAT1f** SOD Watchdog / High CPU Kill | SIGKILL from sod | `/var/log/ltm`: `sod: mcpd not responding` or CPU limit exceeded | High | ❌ No |
| **CAT1g** Restart Loop | varies | mcpd restarts repeatedly; same last log line each cycle | Medium | ✅ Sometimes |
| **CAT1h** Deadlock / Hung | — (no crash) | Process alive but unresponsive to tmsh/REST; all threads blocked on mutex | High | ❌ Use gcore |

### Resolution Strategy by Sub-type

**CAT1a (Null Pointer):** Read source at crash frame → find the null pointer origin one frame up → add null guard or fix upstream return value. Add unit test.

**CAT1b (Assertion):** Extract the assertion expression → determine which invariant was violated → fix caller that violated it (never remove the assertion). Add test.

**CAT1c (Memory Corruption / UAF):** Trace object ownership through alloc/free/reference chain → fix lifetime with smart pointer or deferred free → confirm with ASan (`-fsanitize=address`).

**CAT1d (Stack Overflow):** Find the repeating frame → locate missing recursion termination condition → add cycle detection or convert to iterative. Add edge-case test.

**CAT1e (OOM Kill):** Profile RSS growth over time via `tmsh show sys memory`. If leak: find un-freed allocation with Valgrind. If config-driven growth: escalate to **CAT6 (Scalability / mcpd-64bit RQ)**. If burst: optimize the specific operation.

**CAT1f (SOD Kill):** Capture `gcore` proactively before SOD kills. Inspect threads: if busy-loop → add backoff/rate-limit; if blocked main thread → add timeout or offload to worker. SOD threshold tuning = workaround only.

**CAT1g (Restart Loop):** Identify last log line before each restart. Deterministic → config-triggered → bisect config to find offending object. Non-deterministic → treat as CAT1c or CAT1h.

**CAT1h (Deadlock):** While hung, run `gcore` immediately. GDB `thread apply all bt` → find blocked threads → identify lock order violation or blocking syscall → fix acquisition order or add timeout.

### Bugs (Current List — Sub-type Assigned)

| Bug ID | Sub-type | Component | Status | Summary |
|--------|----------|-----------|--------|---------|
| [662710](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=662710) | CAT1g Restart Loop | a_MCP_FRAMEWORK | FIXED | WCCPD - Service restart loop in FIPS mode |
| [662399](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=662399) | CAT1b Assertion/SIGABRT | a_MCP_AUTH | FIXED | Mcpd auth-related crash |
| [659428](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=659428) | CAT1d Stack Overflow | a_MCP_FRAMEWORK | FIXED | mcpd SEGV during daemonlib_terminate_handler() processing; some sort of recursion issue |

---

## 🟠 Memory Safety / Security Risk (21)

### Resolution Strategy

Assess if path is reachable from untrusted input (network, REST, config). If yes: treat as security+CVE, engage security team. Fix by type: TOCTOU=atomic op/lock; UAF=lifetime/refcount fix; OOB=bounds check; untrusted data=input validation. WONTFIX only with written reachability justification.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [656694](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656694) | Defect | a_MCP_FRAMEWORK | WONTFIX | f5cpp::Array<char>::reset(unsigned int, bool)(): Use after free |
| [656685](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656685) | Defect | a_MCP_LTM | FIXED | trunk_mbr_lacp_info_stat_request::get_trunk_mbr_lacp_info(std::basic_string<char, std::c |
| [656607](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656607) | Defect | a_MCP_FRAMEWORK | WONTFIX | delete_file(const char *)(): Time of check time of use |
| [656606](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656606) | Defect | a_MCP_FRAMEWORK | WONTFIX | remove_public_key(const std::basic_string<char, std::char_traits<char>, std::allocator<c |
| [656480](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656480) | Defect | a_MCP_FRAMEWORK | WONTFIX | CertificateStoreValidator::ReadFile()(): Ignoring number of bytes read |
| [656428](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656428) | Defect | a_MCP_FRAMEWORK | WONTFIX | CertificateStoreValidator::GetDate(asn1_string_st *, long &)(): Use of untrusted string  |
| [656406](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656406) | Defect | a_MCP_FRAMEWORK | WONTFIX | ProfileSSLValidator::validate_cert_validator(Cave::AutoRef<Cave::CfgObj> &)(): Explicit  |
| [656405](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656405) | Defect | a_MCP_NET | FIXED | VnicMgr::routeDomainCmd(operation_t, unsigned short)(): Argument cannot be negative |
| [656388](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656388) | Defect | a_MCP_LTM | WONTFIX | disk_info_request::process()(): Argument cannot be negative |
| [656363](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656363) | Defect | a_MCP_NET | WONTFIX | interface_stats_request::create_stats()(): Explicit null dereferenced |
| [656357](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656357) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::convert_netmask(const _mcp_ip_address_tag_ &, Cave::IpAddress &)(): Out-of-bounds a |
| [656356](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656356) | Defect | a_MCP_FRAMEWORK | WONTFIX | CertificateSigningRequestValidator::Load()(): Explicit null dereferenced |
| [656348](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656348) | Defect | a_MCP_FRAMEWORK | WONTFIX | CertificateRevocationListValidator::Load()(): Explicit null dereferenced |
| [656345](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656345) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::convert_ip_address(const _mcp_ip_address_tag_ &, Cave::IpAddress &)(): Out-of-bound |
| [656342](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656342) | Defect | a_MCP_FRAMEWORK | WONTFIX | CertificateValidator::Load()(): Explicit null dereferenced |
| [656339](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656339) | Defect | a_MCP_FRAMEWORK | WONTFIX | cave_to_mcp(const Cave::IpAddress &, _mcp_ip_address_tag_ &)(): Out-of-bounds access |
| [656335](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656335) | Defect | a_MCP_FRAMEWORK | WONTFIX | parse_rule_hints(std::basic_string<char, std::char_traits<char>, std::allocator<char>>&, |
| [656333](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656333) | Defect | a_MCP_FRAMEWORK | WONTFIX | <unnamed>::syslog_request::process()(): Argument cannot be negative |
| [656254](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656254) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCP_UNIXListener::MCP_UNIXListener(const char *, int)(): Buffer not null terminated |
| [656252](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656252) | Defect | a_MCP_NET | FIXED | VnicMgr::configTap(const char *, bool)(): Buffer not null terminated |
| [656251](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656251) | Defect | a_MCP_NET | FIXED | VnicMgr::enableInterface(const char *, bool)(): Buffer not null terminated |

---

## 🟡 Null Dereference / Uninitialized Variable (36)

### Resolution Strategy

Check if the uninitialized-field path is reachable at runtime. If yes: initialize to safe default in constructor. If null deref: reorder null check before use. If unreachable: WONTFIX with reason. Batch multiple fixes in one quarterly CL to reduce overhead.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [657254](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=657254) | Defect | a_MCP_LTM | WONTFIX | cluster_mbr_db_handler(): Dereference null return value |
| [657247](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=657247) | Defect | a_MCP_LTM | WONTFIX | cluster_db_handler(): Dereference null return value |
| [656741](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656741) | Defect | a_MCP_LTM | WONTFIX | McpSubscriber::McpSubscriber(const std::basic_string<char, std::char_traits<char>, std:: |
| [656676](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656676) | Defect | a_MCP_FRAMEWORK | WONTFIX | audit_request::audit_request(_mcpmsg_t *, request_group *, unsigned int)(): Uninitialize |
| [656664](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656664) | Defect | a_MCP_FRAMEWORK | WONTFIX | stats_metadata_request::stats_metadata_request(_mcpmsg_t *, request_group *, unsigned in |
| [656661](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656661) | Defect | a_MCP_LTM | WONTFIX | global_serverldap_stats_request::global_serverldap_stats_request(_mcpmsg_t *, request_gr |
| [656630](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656630) | Defect | a_MCP_LTM | WONTFIX | global_classification_urlcat_stats_request::global_classification_urlcat_stats_request(_ |
| [656626](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656626) | Defect | a_MCP_LTM | WONTFIX | policy_stats_request::policy_stats_request(_mcpmsg_t *, request_group *, unsigned int)() |
| [656624](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656624) | Defect | a_MCP_FRAMEWORK | WONTFIX | request::request(_mcpmsg_t *, request_group *, unsigned int)(): Uninitialized scalar fie |
| [656620](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656620) | Defect | a_MCP_FRAMEWORK | FIXED | CVM::CfgSchemaClassMgr::CfgSchemaClassMgr()(): Uninitialized pointer field |
| [656610](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656610) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::VirtualServerProfile::Profiles::Profiles()(): Uninitialized scalar field |
| [656608](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656608) | Defect | a_MCP_NET | FIXED | RDOpContext::RDOpContext(unsigned short)(): Uninitialized pointer field |
| [656602](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656602) | Defect | a_MCP_FRAMEWORK | WONTFIX | forkCommandContext::forkCommandContext(int, int, int, void *, void (*)(void *, std::basi |
| [656599](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656599) | Defect | a_MCP_FRAMEWORK | WONTFIX | WC_QUERY::FolderData::FolderData()(): Uninitialized scalar field |
| [656590](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656590) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCPD_CTX::CMViewMsgParser::CMViewMsgParser()(): Uninitialized scalar field |
| [656564](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656564) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::ValidateProto::EnsureProtoProfile::EnsureProtoProfile(unsigned short, void (*)(CVM: |
| [656559](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656559) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCP_IPListener::MCP_IPListener(int)(): Uninitialized scalar field |
| [656557](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656557) | Defect | a_MCP_LTM | WONTFIX | virtual_address_stats_request::virtual_address_stats_request(_mcpmsg_t *, request_group  |
| [656552](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656552) | Defect | a_MCP_FRAMEWORK | WONTFIX | init_signals()(): Uninitialized scalar variable |
| [656543](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656543) | Defect | a_MCP_FRAMEWORK | WONTFIX | <unnamed>::HwPropMsgParser::HwPropMsgParser()(): Uninitialized scalar field |
| [656527](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656527) | Defect | a_MCP_FRAMEWORK | WONTFIX | <unnamed>::SaveMsgParser::SaveMsgParser()(): Uninitialized scalar field |
| [656526](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656526) | Defect | a_MCP_NET | FIXED | VlanRouteHandler::doVlan(const VlanRouteOp &)(): Uninitialized scalar variable |
| [656524](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656524) | Defect | a_MCP_FRAMEWORK | WONTFIX | <unnamed>::StatusUpdateParser::StatusUpdateParser(unsigned short)(): Uninitialized scala |
| [656432](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656432) | Defect | a_MCP_FRAMEWORK | WONTFIX | WC_QUERY::wildcard_query_request::wildcard_query_request(_mcpmsg_t *, request_group *, u |
| [656430](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656430) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::CfgSchemaClassMgr::PrimaryKeyInfo::PrimaryKeyInfo()(): Uninitialized pointer field |
| [656425](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656425) | Defect | a_MCP_FRAMEWORK | FIXED | MCPProcessor::MCPProcessor()(): Uninitialized scalar field |
| [656414](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656414) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::ValidateProto::EnsureProtoProfile::EnsureProtoProfile(unsigned short)(): Uninitiali |
| [656391](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656391) | Defect | a_MCP_FRAMEWORK | WONTFIX | IndexFilter::IndexFilter(const Cave::SchemaObj *)(): Unchecked dynamic_cast |
| [656382](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656382) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCPProcessor::load_config(unsigned char)(): Resource leak |
| [656378](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656378) | Defect | a_MCP_FRAMEWORK | WONTFIX | CertificateRevocationListValidator::Load()(): Dereference before null check |
| [656374](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656374) | Defect | a_MCP_FRAMEWORK | WONTFIX | ltcfg_field_default_value(Cave::AutoRef<Cave::CfgObj> &)(): Using invalid iterator |
| [656369](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656369) | Defect | a_MCP_NET | WONTFIX | VnicMgr::enableInterface(const char *, bool)(): Resource leak |
| [656367](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656367) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCPProcessor::processRequestNow(request_group *)(): Dereference before null check |
| [656366](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656366) | Defect | a_MCP_FRAMEWORK | WONTFIX | request_group::process()(): Dereference before null check |
| [656360](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656360) | Defect | a_MCP_FRAMEWORK | WONTFIX | config_db_query::check_for_user_spec(const Cave::CfgClass *, const Cave::CfgIdUint16Vect |
| [656344](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656344) | Defect | a_MCP_FRAMEWORK | INVALID | BgSysExeCmd::forkCmdBackground(const std::basic_string<char, std::char_traits<char>, std |

---

## 🟡 Dead Code / Unchecked Return Value (20)

### Resolution Strategy

Dead code/stray semicolons: remove unreachable block. Unchecked returns: assess if failure is fatal; add check+LOG if so. Unchecked dynamic_cast: add assert or check. Batch all into one MCP-Coverity cleanup CL per quarter.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [656692](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656692) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::MsgOrder::initialize()(): Structurally dead code |
| [656517](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656517) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::MonitorInstanceMgr::enabled_event_handler(Cave::AutoRef<Cave::CfgObj> &)(): Uncheck |
| [656509](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656509) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCP_UNIXListener::MCP_UNIXListener(const char *, int)(): Unchecked return value from lib |
| [656490](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656490) | Defect | a_MCP_FRAMEWORK | WONTFIX | LogRequest::LogFile::load_files()(): Unchecked return value from library |
| [656478](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656478) | Defect | a_MCP_FRAMEWORK | WONTFIX | transaction_id_request::add_to_reply(const Cave::CfgIdClass *, unsigned int, unsigned in |
| [656462](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656462) | Defect | a_MCP_FRAMEWORK | WONTFIX | icall_triggered_handler_stat_request::query_one(const std::basic_string<char, std::char_ |
| [656461](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656461) | Defect | a_MCP_FRAMEWORK | WONTFIX | reset_object_stats_request::process()(): Unchecked return value |
| [656450](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656450) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCPListener::setSocketOptions(int)(): Unchecked return value from library |
| [656351](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656351) | Defect | a_MCP_FRAMEWORK | WONTFIX | combine_replies(_mcpmsg_t *, _mcpmsg_t *)(): Stray semicolon |
| [656318](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656318) | Defect | a_MCP_FRAMEWORK | WONTFIX | combine_replies(_mcpmsg_t *, _mcpmsg_t *)(): Logically dead code |
| [656317](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656317) | Defect | a_MCP_FRAMEWORK | WONTFIX | snarf_message_no(const char *&)(): Unchecked return value |
| [656313](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656313) | Defect | a_MCP_FRAMEWORK | WONTFIX | request::construct_reply()(): Unchecked return value |
| [656307](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656307) | Defect | a_MCP_FRAMEWORK | WONTFIX | request_group::construct_reply(const std::basic_string<char, std::char_traits<char>, std |
| [656305](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656305) | Defect | a_MCP_FRAMEWORK | WONTFIX | snarf_object_id(const char *&)(): Unchecked return value |
| [656291](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656291) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCPProcessor::load_config(unsigned char)(): Unchecked return value from library |
| [656290](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656290) | Defect | a_MCP_FRAMEWORK | WONTFIX | CSubscription::initialize()(): Unchecked return value |
| [656268](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656268) | Defect | a_MCP_LTM | WONTFIX | persist_info_request::set_name_attribute(_mcpmsg_t *, char *, unsigned short, const std: |
| [656265](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656265) | Defect | a_MCP_FRAMEWORK | WONTFIX | ProfileSSLValidator::jcv_update()(): Unchecked return value |
| [656264](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656264) | Defect | a_MCP_LTM | WONTFIX | persist_info_request::translate_reply(mco_trans_t_ *, _mcpmsg_t *)(): Unchecked return v |
| [656255](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656255) | Defect | a_MCP_FRAMEWORK | WONTFIX | MCPConnection::ClientReadEvent()(): Unchecked return value |

---

## 🟠 Config Load / State Corruption (6)

### Resolution Strategy

Reproduce with tmsh load sys config or UCS restore. Check for missing files (certs, bundles, templates). Trace load path: framework -> staging -> postgres to find failure point. Add pre-condition validation. Improve error messages to be actionable. Test across upgrade paths.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [663386](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=663386) | Defect | a_MCP_LTM | FIXED | dtdi.crt cannot be found during "tmsh load sys config verify file" command |
| [662384](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=662384) | Defect | a_MCP_FRAMEWORK | FIXED | Integrate platform-migrate simplifcations from bigip12.1.3 to Evergreen |
| [659872](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=659872) | Defect | a_MCP_FRAMEWORK | FAD | Validation framework doesn't check for duplicate entries for joins |
| [658650](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=658650) | Improvement | a_MCP_FRAMEWORK | FIXED | Improve output of platform-migrate with warnings |
| [657459](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=657459) | Defect | a_MCP_LTM | WONTFIX | vADC: setting MGMT GUI Port to 443 on Single Nic not honored on reboot |
| [656343](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656343) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::UrldbFeedListMgr::fixup_config_checkpoint(Cave::AutoRef<Cave::CfgObj> &, const CVM: |

---

## 🟠 Transaction / Concurrency (1)

### Resolution Strategy

Reproduce with debug mcpd all logs. Trace ordering through request_group.cpp and staging/. Add mutex or message-ordering queue for interleaving. Fix atomicity in DB layer for delete+create in same transaction. Verify commit/rollback handles partial application. Add integration test.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [662437](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=662437) | Defect | a_MCP_LTM | WONTFIX | Transaction fails when pool-member is deleted and then created again in this order. |

---

## 🟠 Authentication / Security Policy (6)

### Resolution Strategy

Check RFC compliance (RFC 5246, RFC 5280, FIPS 140-2) first. Reproduce with exact config (FIPS on/off, cipher, cert type). Read tm_daemon/mcp/authz/ and mcp/auth/. Fix: password policy=match GUI to DB schema; FIPS crash=OpenSSL FIPS provider error; cert=validate per RFC 5280. Test in FIPS and non-FIPS modes.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [663136](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=663136) | Usability | a_MCP_FRAMEWORK | WONTFIX | RQ-TMOS-0003550 Usability Issue: Password change usability issue |
| [658406](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=658406) | Defect | a_MCP_AUTH | WONTFIX | GUI - Data field validation for Password Policy settings wrong |
| [656534](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656534) | Defect | a_MCP_FRAMEWORK | WONTFIX | LtcfgRemoteUserCfgVldtrVersion::install(const std::basic_string<char, std::char_traits<c |
| [656392](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656392) | Defect | a_MCP_FRAMEWORK | WONTFIX | reset_object_stats_request::get_db_object(Cave::AutoRef<Cave::CfgObj> &, const Cave::Sch |
| [656380](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656380) | Defect | a_MCP_FRAMEWORK | WONTFIX | remove_public_key(const std::basic_string<char, std::char_traits<char>, std::allocator<c |
| [656340](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656340) | Defect | a_MCP_FRAMEWORK | WONTFIX | CVM::ProfileClientSSL::inherit_certkeychain_obj(Cave::AutoRef<Cave::CfgObj> &, const std |

---

## 🟢 Error Message / Usability / Logging (1)

### Resolution Strategy

Find code emitting the message. Rewrite to be actionable (what+why+what to do). Add log line where missing; include object name, operation, error code. Confirm severity level is correct. Submit as standalone low-risk CL.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [662110](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=662110) | Improvement | a_MCP_LTM | WONTFIX | RFE: Create a db variable to toggle audit log messages from mcpd-primary |

---

## 🔵 RFE / Enhancement (1)

### Resolution Strategy

Assess customer impact. Check for existing workaround. Create RQ if high-impact + no workaround. Define acceptance criteria. Assign to component team for scoping.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [658133](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=658133) | Improvement | a_MCP_LTM | WONTFIX | [RFE] Add listener name to "show sys connection" output |

---

## ⚪ Build / Test Infrastructure (4)

### Resolution Strategy

Immediately identify failing step: compile/link/test-setup/env conflict. Postgres conflict: use dedicated port or mock DB. Missing lib: update LDFLAGS/CMakeLists/.spec. Python import: fix PYTHONPATH/LD_LIBRARY_PATH. Verify in clean build env. Add to CI gate.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [662607](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=662607) | Build Break | a_MCP_FRAMEWORK | FIXED | Running MCP unit tests fails when postgres is already running on the build box |
| [658202](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=658202) | Defect | a_MCP_FRAMEWORK | FIXED | Missing library and build dependencies for libcavecommon and libf5cppcommon |
| [657482](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=657482) | Defect | a_MCP_FRAMEWORK | FIXED | f5py: f5.bss import error: undefined symbol: lfmt |
| [656467](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=656467) | Defect | a_MCP_FRAMEWORK | WONTFIX | XPathCompiler::run(std::basic_string<char, std::char_traits<char>, std::allocator<char>> |

---

## ⚪ Miscellaneous / Bucket (1)

### Resolution Strategy

Read full bug description. Re-classify into a correct category if possible. If bucket bug: ensure all sub-items are filed as individual bugs.

### Bugs

| Bug ID | Type | Component | Status | Summary |
|--------|------|-----------|--------|---------|
| [663801](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=663801) | Defect | a_MCP_FRAMEWORK | FIXED | bucket for minor bugs found while dealing with other issues |

---

## Key Observations

**1. Prioritize live bugs (659xxx-663xxx) over historical Coverity (656xxx)**  
The 656xxx block is a historical scan. Triage active operational bugs first.

**2. CAT3 WONTFIX decisions require written justification**  
Undocumented WONTFIX on security findings (UAF, TOCTOU) creates liability. Document reachability analysis.

**3. CAT4 + CAT5 (55 bugs) suit quarterly batch CLs**  
Low-risk fixes (initializers, null guards, return-value checks). Batch into one CL per quarter.

**4. CAT6 (Scalability) requires the mcpd-64bit RQ, not per-bug patches**  
The 32-bit heap limit is the root cause for all INOPERATIVE/large-config bugs.

**5. CAT12 (Build/Test) always has the highest urgency**  
Build and test failures block all other development. Never allow open CAT12 bugs to persist.