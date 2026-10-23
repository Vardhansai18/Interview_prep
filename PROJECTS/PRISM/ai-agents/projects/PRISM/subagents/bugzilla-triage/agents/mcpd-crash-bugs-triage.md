# mcpd Crash Bugs — Fixed Issues & Fix Patterns

> **Purpose**: Reference guide for resolving mcpd crash bugs — each entry shows the issue pattern and how it was fixed
>
> **Generated**: 2026-05-12
>
> **Filter**: resolution=FIXED only (Verified/FIXED + Not Verified/FIXED + Resolved/FIXED)
>
> **Total**: 42 bugs across 9 categories

## Category Overview

| Category | Name | Fixed Bugs |
|----------|------|-----------|
| `CAT-GEN` | Generic Core / Crash (type unknown) | 13 |
| `CAT-WORKER` | Worker Thread Crash | 7 |
| `CAT-CFG` | Config / UCS / Boot / Upgrade Crash | 6 |
| `CAT-HA` | HA / Clustering Crash | 5 |
| `CAT-ABT` | SIGABRT / Assertion Failure | 4 |
| `CAT-SEG` | SIGSEGV / Null Dereference | 2 |
| `CAT-RACE` | Race Condition / Thread Safety | 2 |
| `CAT-SSL` | SSL / Certificate Triggered Crash | 2 |
| `CAT-SNMP` | SNMP-Triggered Crash | 1 |
| | **Total** | **42** |

---

## CAT-GEN — Generic Core / Crash (type unknown)

**Common fix patterns in this category**: Varies — requires backtrace analysis. Frequent patterns: DB iterator invalidation, assert on unexpected state, null pointer in config apply path.

### [Bug 2228917](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2228917) — MCPD core with __assert_fail_base() from /usr/lib64/libc.so.6 and __evMainLoop()

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- NFC to attach bugs from tmos-bugs-staging branch for Release Pandora

### [Bug 2220101](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2220101) — MCPD core : __assert_fail_base () when doing load sys config file <filename>

**Component**: FRAMEWORK  
**Status**: Resolved/FIXED

**Fix pattern**:
- Initializing the outstanding requests in all the connection constructor

### [Bug 2218921](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2218921) — Continuous MCPD core observed after bigstart restart mcpd on an active-active sy

**Component**: FRAMEWORK  
**Status**: Not Verified/FIXED

**Fix pattern**:
- Fixed dead lock issue in extreme db caused by transaction commit exception
- Description: Fixed dead lock issue in extreme db caused by transaction commit exception

### [Bug 2200561](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2200561) — Continuous MCPD core observed after bigstart restart mcpd on an active-active sy

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2162497](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2162497) — mcpd core - CaveInternals::EdbTreeIterator::prefetch

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2162409](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2162409) — mcpd core - MCPDBManager::close_transaction

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- SCI is integrating 1 changelist from Bug2162409

### [Bug 2131789](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2131789) — mcpd core found during reboot with afm config on viprion

**Component**: FRAMEWORK  
**Status**: Not Verified/FIXED

**Fix pattern**:
- Update 'p4gf_config'.

### [Bug 2122905](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2122905) — MCPD core encountered during a system reboot when system is with large configura

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- Extremdb patch

### [Bug 2119493](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2119493) — (DNS-Orion - 21.0.0) mcp core generated during gtm wideip regression

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 1848993](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1848993) — GuestAgentDaemon core on clustered guest during __memput_record

**Component**: FRAMEWORK  
**Status**: Not Verified/FIXED

**Fix pattern**:
- SCI is submitting the fix for Bug904401-7
- SCI is integrating 1 changelist from Bug904401-7
- Integrate Change: 3892168, for EHF case: 01141973, Bug 904401-7

### [Bug 1848989](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1848989) — GuestAgentDaemon core on clustered guest during __memput_record

**Component**: FRAMEWORK  
**Status**: Not Verified/FIXED

**Fix pattern**:
- 2168:gcc -falign-functions=16 -D_REENTRANT -mtune=core2 -fdebug-prefix-map=/home/f5cm/cm/user/1547909/f5_build/devfs_x86_64/usr=/usr -fdebug-prefix-map=/home/f5cm/cm/user/1547909/f5_build=
- SCI is integrating 1 changelist from Bug904401-6
- SCI is submitting the fix for Bug904401-6

### [Bug 1286797](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1286797) — mcpd core while processing a node stats query when there are thousands of FQDN n

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- SCI is integrating 1 changelist from Bug964125-7
- NFC to attach bugs from bigip17.1.x-bugs
- NFC to attach bugs

### [Bug 1114949](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1114949) — (i15800): mcpd core seen at multiple points during performance regression

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- NFC to attach bugs from bigip15.1.x-ganymede branch for Release 15.1.7
- NFC to attach bugs from 15.1.x branch for Release 15.1.7

---

## CAT-WORKER — Worker Thread Crash

**Common fix patterns in this category**: Worker thread lifecycle issues; connection teardown races; concurrent transaction close.

### [Bug 2252233](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2252233) — mcpd_worker_1 core at MCPConnection::sendMessage()

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- SCI is submitting the fix for Bug2252233
- SCI is integrating 1 changelist from Bug2252233

### [Bug 2230461](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2230461) — mcpd worker core generated after stressing mcpd with SSL virtual objects

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2220993](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2220993) — MCPD core at "MCPProcessor::check_and_adjust_worker_threads" during load sys con

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2190377](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2190377) — mcpd worker core("MCPDBManager::close_transaction") while doing concurrent pools

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2140453](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2140453) — mcpd worker core("MCPDBManager::close_transaction") while doing concurrent pools

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2122977](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2122977) — MCPD/mcpd worker core is seen and system remain in an inoperative state after a 

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- MCPD worker core when mcpd.workerthreads db value changed and rebooted.
- Fix: While handling db change validation, not honored if not in mcp running phase

### [Bug 2053613](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2053613) — CORE FOUND ON 21.0.0. Testing against Pantera High (mcpd_worker.bld0.0.2.core.gz

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- Hopefully, the issue is resolved

---

## CAT-CFG — Config / UCS / Boot / Upgrade Crash

**Common fix patterns in this category**: Missing null/boundary checks during config load; INOPERATIVE state caused by mcpd restart loop on bad config object; platform-migrate license mismatch.

### [Bug 2197449](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2197449) — In V21.0 BIG-IP VE remains INOPERATIVE after cold boot due to MCPD failure.

**Component**: LTM  
**Status**: Not Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 2187365](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2187365) — In V21.0 BIG-IP VE or F5OS tenant remains INOPERATIVE after cold boot, due to MC

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- EngHF for Case 01055247: Bug 2179729-1, Bug 2187365
- [hfh] Integrating hotfix branch
- Description: [hfh] Integrating hotfix branch

### [Bug 2135637](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2135637) — CP i5k : BIGIP went into inoperative state in 'Sizing_LTM-Nodes_16000' tc

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- dbsweeper code changes for cleanup of shared db segments
- Integrate Change: 3853070, for bigip21.0.0
- Inoperative issue got fixed

### [Bug 2078677](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2078677) — Bigip went into inoperative state with tmos-bugs-staging-9733 build in LTM CP Pe

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- SCI is integrating 2 changelists from Bug2078677
- SCI is submitting the fix for Bug2078677

### [Bug 1167709](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1167709) — mcpd crash on secondary blades removing user configured predefined classificatio

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- [hfh] Integrating hotfix branch
- Description: [hfh] Integrating hotfix branch
- NFC to attach bugs to 16.1.4

### [Bug 1166329](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1166329) — mcpd crash on secondary blades removing user configured predefined classificatio

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- tmos-bugs merge to tier2 [Total 67 bug fixes merged]
- If Release Note is Yes and Writeup Status is not Drafted/Blocked, this bug will be published in Bug Tracker, visit http://go/bugtracker and enter the bug ID

---

## CAT-HA — HA / Clustering Crash

**Common fix patterns in this category**: Worker thread count change during failover; shared memory lock contention under high object count; TMM CPU license mismatch.

### [Bug 2259357](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2259357) — mcpd_worker core dumps observed on standby BIG-IP device in HA

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- Removing stop from worker destructor, this is causing a core when main thread exit and when called global destructor
- Description:     Removing stop from worker destructor, this is causing a core when main thread exit and when called global destructor
- Create a BFO and stage a fix, steps can be found at https://go/sci

### [Bug 2258249](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2258249) — mcpd & mcpd_worker core dumps observed on standby BIG-IP device in HA

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- Waiting for the setup to verify as the root cause is same as 2227693
- cgi?id=2259357 resolved this issue also

### [Bug 2220925](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2220925) — MCPD core at "mco_tmgr_shared_lock" found during routing BVT

**Component**: LTM  
**Status**: Not Verified/FIXED

**Fix pattern**:
- Request to mention the perforce CL through which the fix is checked-in and update the branch details as well
- > Request to mention the perforce CL through which the fix is checked-in and update the branch details as well

### [Bug 2131993](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2131993) — pccd core observed while deleting objects in bulk when system is having large co

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- i know this is a resolved bug but should we see this issue as new ? or it will be resolved ? i am just commenting
- Integrate change: 3854334,for bigip21.0.x-current

### [Bug 2107281](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2107281) — MCPD core and mcpd continuous restart after changing worker threads from 4 to 1

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

---

## CAT-ABT — SIGABRT / Assertion Failure

**Common fix patterns in this category**: Assert on partially-deleted GTM object; unhandled state in pool member deletion path.

### [Bug 1194909](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1194909) — MCPD SIGABRT and core happened while deleting GTM pool member

**Component**: GTM  
**Status**: Verified/FIXED

**Fix pattern**:
- Tested with reported configuration by removing gtm pool members multiple times, with different poo
- SCI is submitting the fix for Bug1101453-7
- SCI is integrating 1 changelist from Bug1101453-7

### [Bug 1154229](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1154229) — MCPD SIGABRT and core happened while deleting GTM pool member

**Component**: GTM  
**Status**: Verified/FIXED

**Fix pattern**:
- NFC to attach bugs from 15.1.x-tmos-bugs branch for Release 15.1.9
- NFC to attach bugs from 15.1.x-tmos branch for Release 15.1.9
- NFC to attach bugs from bigip15.1.x-europa branch for Release 15.1.9

### [Bug 1154221](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1154221) — MCPD SIGABRT and core happened while deleting GTM pool member

**Component**: GTM  
**Status**: Verified/FIXED

**Fix pattern**:
- NFC to attach bugs from bigip16.1.x-bugs branch for Release 16.1.4[Merge 1]
- NFC to attach bugs to 16.1.4

### [Bug 1101453](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1101453) — MCPD SIGABRT and core happened while deleting GTM pool member

**Component**: GTM  
**Status**: Verified/FIXED

**Fix pattern**:
- tmos-bugs merge to tier2 [Total 18 bug fixes merged]
- Added test to cover BZ 1101453 : Deleting a pool member from a pool resulting in mcpd crash

---

## CAT-SEG — SIGSEGV / Null Dereference

**Common fix patterns in this category**: Null pool member pointer; freed MKV message buffer accessed after release; invalid iterator on concurrent modification.

### [Bug 2046729](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2046729) — mcpd core  (signal 11, in evaluate_pool_member_status pool_member=)  when runnin

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description

### [Bug 1173625](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1173625) — (coroner): tmm crash SIGSEGV - mkv_free() in ../mcp/mcp_config.c:1619

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- tmos-bugs merge to tier2 [Total 29 bug fixes merged]

---

## CAT-RACE — Race Condition / Thread Safety

**Common fix patterns in this category**: Missing mutex protection in folder manager queue; lock ordering issue during concurrent bulk operations.

### [Bug 2153501](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2153501) — MCPD crash in FolderMgr::validate_deleted_folder_queue due to race condition cle

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- NFC to attach bugs from bigip21.0.x-bugs branch for Release 21.0.0.1
- [hfh] Integrating hotfix branch
- Description: [hfh] Integrating hotfix branch

### [Bug 2153489](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2153489) — MCPD crash in FolderMgr::validate_deleted_folder_queue due to race condition cle

**Component**: FRAMEWORK  
**Status**: Verified/FIXED

**Fix pattern**:
- VERFIXED THE FIX TO BE WORKING FINE, DETAILS TO FOLLOW:
- MCPD/worker cores

---

## CAT-SSL — SSL / Certificate Triggered Crash

**Common fix patterns in this category**: Missing null check on SSL key object during GUI import path.

### [Bug 1081313](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1081313) — Unexpected MCPD core when importing SSL key via GUI

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- NFC to attach bugs

### [Bug 1081201](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=1081201) — Unexpected MCPD core when importing SSL key via GUI

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**:
- 0 @3583321 [averma] Llama 8 bug fixes

---

## CAT-SNMP — SNMP-Triggered Crash

**Common fix patterns in this category**: SNMP handler accessing freed mcpd object under benchmarking load.

### [Bug 2221905](https://bugzilla.olympus.f5net.com/show_bug.cgi?id=2221905) — mcp core generated on running snmp test case from CP benchmarking FOM BVT.

**Component**: LTM  
**Status**: Verified/FIXED

**Fix pattern**: See bug comments for CL description
