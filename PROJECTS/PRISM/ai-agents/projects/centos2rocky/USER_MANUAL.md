# TMOS Rocky Migration Agents — User Manual

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Prerequisites](#prerequisites)
4. [Quick Start Guide](#quick-start-guide)
5. [Agent Architecture](#agent-architecture)
6. [Migration Workflow](#migration-workflow)
7. [Orchestrator Workflow](#orchestrator-workflow)
8. [Rocky Migration Status File](#rocky-migration-status-file)
9. [Migration Domains](#migration-domains)
10. [Input Parameters Reference](#input-parameters-reference)
11. [Output Files Reference](#output-files-reference)
12. [Build Commands Reference](#build-commands-reference)
13. [Perforce Commands Reference](#perforce-commands-reference)
14. [Understanding the Report](#understanding-the-report)
15. [Examples](#examples)
16. [Best Practices](#best-practices)
17. [Troubleshooting](#troubleshooting)
18. [FAQs](#faqs)
19. [Reference: File Locations](#reference-file-locations)

---

## Overview

This manual covers two AI-powered agents for migrating TMOS modules from CentOS 6/7 to Rocky Linux 8.10.

### tmos_rocky_migrator — Single-Module Migration Agent

The **TMOS Rocky Migration Agent** (`tmos_rocky_migrator`) migrates a single TMOS module. It analyses module source code, applies technology-specific migration fixes, and produces a comprehensive migration report.

**What it does:**
- Validates the module name against the TMOS build system
- Sets up or connects to an existing TMOS workspace
- Automatically detects whether the module needs 32-bit → 64-bit architecture migration
- Applies Rocky Linux 8.10 compatibility changes across all relevant technology stacks (GCC 11, OpenSSL 1.1.1k, Java JDK 21, Python 3, Perl 5.26+)
- Automatically detects and applies MySQL Enterprise 5.5.53 → MariaDB 10.11.10 migration when the module depends on MariaDB/MySQL
- Automatically detects and applies MySQL Connector/J → MariaDB Connector/J migration when the module depends on `mysql-connector-java`
- Makes mandatory spec file modifications to enable GCC 11 toolchain
- Compiles the module iteratively, fixing warnings and errors until zero defects
- Collects RPM disk space and binary static memory analysis after a successful build: installed size per RPM and `text`/`data`/`bss` segment breakdown per ELF binary
- Captures AI learnings from each migration and appends them to a shared learnings file
- Generates a comprehensive migration report to `output/<module_name>/`

### rocky-migration-orchestor — Full-Stack Orchestration Agent

The **Rocky Migration Orchestrator** (`rocky-migration-orchestor`) operates in two modes:

**Mode 1 — Query mode**: Lists all daemons/applications with their Rocky migration status from the shared `daemons_apps_status.txt` registry. Triggered by keywords like "show", "list", or "display". Saves a Markdown query report to `output/query_resp/`.

**Mode 2 — Migration mode**: Automates migration of a TMOS application or daemon module **and all of its transitive dependencies**, processing them in the correct dependency-level order.

**What it does (migration mode):**
- Validates the module name against both the `daemons_apps_status.txt` registry and the TMOS build system
- Resolves the full dependency tree using `./show-parallel-levels`
- Checks the shared Rocky migration status file (`rocky_status.txt`) to skip already-migrated modules
- Invokes `tmos_rocky_migrator` for each `NotStarted` module, level by level
- Handles concurrent runs safely using a file-locking mechanism on both status files
- Creates a dedicated Perforce changelist and posts a Review Board draft for each migrated module
- Submits changelists automatically after each module's migration is verified
- Merges AI learnings from each module migration into the shared SKILL knowledge base (`rocky-migration-ai-learnings.SKILL.md`)
- Generates a comprehensive orchestration report including per-module CL/RB table and AI performance summary

### Which Agent Should I Use?

| Scenario | Use This Agent |
|---|---|
| Migrate a single identified module | `tmos_rocky_migrator` |
| Migrate a full application or daemon and all its dependencies | `rocky-migration-orchestor` |
| Re-run migration for one module that previously failed | `tmos_rocky_migrator` |
| Coordinate migration with other users working concurrently | `rocky-migration-orchestor` |
| List all daemons/applications and their Rocky migration status | `rocky-migration-orchestor` (query mode) |

**Who should use these agents:**
- Developers migrating TMOS modules to Rocky Linux 8.10
- Team leads orchestrating full application stack migrations
- Build engineers validating Rocky Linux compatibility

---

## Key Features

### 🔍 Technology Stack Detection
- Automatically identifies which migration domains apply (C/C++, Java, Python, Perl, OpenSSL, MySQL/MariaDB)
- Detects Perl and Python scripts by shebang line (`#!/usr/bin/perl`, `#!/usr/bin/python`) in addition to file extensions
- Applies only relevant migration knowledge to each module

### 🏗️ Automated 64-bit Migration
- Reads `input/32bit-modules.txt` to determine if a module needs architecture migration
- Invokes the `tmos_rocky_64bit_migrator` subagent automatically for 32-bit modules
- Verifies subagent success before proceeding — does not silently continue on failure
- 64-bit migration artifacts are isolated under `logs/<module_name>_64bit/` and `output/<module_name>_64bit/`

### 🔧 Spec File Management
- Applies three mandatory GCC 11 spec file modifications automatically:
  1. `%global debug_package %{nil}`
  2. `%include %{_topdir}/gcc-toolchain.inc`
  3. `%{gcc_toolset_enable}` in `%build` and `%install` sections
- Verifies all modifications are present before triggering a build

### 🔗 MySQL / MariaDB Migration
- Automatically checks whether the module depends on `mysql-enterprise` or `mariadb` via the module's `depends` field in `.def.inc` files
- Applies MySQL Enterprise 5.5.53 → MariaDB 10.11.10 migration (C/C++ client API, spec file) using `mysql-mariadb-migration.SKILL.md`
- Automatically detects MySQL Connector/J usage via `pom.xml`, `build.gradle`, spec files, and Java source imports
- Applies MySQL Connector/J → MariaDB Connector/J migration (Java driver class, JDBC URL, DataSource, connection properties) using `mysql-connector-java-to-mariadb-migration.SKILL.md`
- Both checks are independent: a module may require one, both, or neither

### 🔄 Iterative Build and Fix
- Compiles with full logs redirected to `logs/<module_name>/`
- Analyzes each warning and error against the correct migration skill domain
- Resolves missing DEVFS headers and libraries by identifying responsible dependent modules, adding `Provides: interface(devfs)` to their spec files, and recompiling them
- Applies fixes and rebuilds until zero warnings and zero errors
- After a successful build, captures RPM disk space and binary static memory analysis (`text`, `data`, `bss` per ELF file)

### 📊 Comprehensive Reporting
- Generates a structured Markdown report covering all migration domains applied
- Report saved to `output/<module_name>/tmos_rocky_migrator_<module_name>_report.md`
- Includes executive summary, file-by-file changes, RPM disk/memory analysis, Perforce status, and next steps
- Appends new learnings captured during migration to `ai-learnings/rocky_migration_learnings.md` for use in future migrations

### 🎛️ Full-Stack Dependency Orchestration (`rocky-migration-orchestor`)
- Supports **query mode**: lists daemons/applications with their Rocky migration status from `/vol/3/share/rocky_migration/daemons_apps_status.txt` and saves the formatted table to `output/query_resp/`
- Resolves the full transitive dependency tree of a TMOS application via `./show-parallel-levels`
- Validates the module name against the `daemons_apps_status.txt` registry before running a build-system check
- Processes all dependencies in build order (level-0 first, target module last)
- Reads and writes two shared Rocky migration status files (`rocky_status.txt` and `daemons_apps_status.txt`) to track progress across multiple users
- Invokes `tmos_rocky_migrator` for each module that has not yet been migrated
- Waits for modules that are `InProgress` by other concurrent agents before advancing to the next dependency level
- Creates a dedicated Perforce changelist, posts a Review Board draft, and submits for each migrated module
- Merges AI learnings from each completed module migration into the shared SKILL knowledge base, then submits the updated SKILL file as a separate CL
- Produces a per-run orchestration report with timestamps, changelists, Review Board URLs, submit status, and AI performance metrics (token estimates per module)

### 🔐 Concurrent-Safe File Locking
- All reads and writes to the shared status files are protected by an exclusive file lock (`ai-agents/common/scripts/file_lock.py`)
- Lock is acquired before and released immediately after each read or write
- Stale lock detection: if a lock is held by the same user (crashed run), it is removed automatically; if held by a different user, the agent waits indefinitely (1-second retry)
- The SKILL file lock escalates to the user after 15 minutes if held by another agent
- Multiple orchestrator instances from different users can run simultaneously without data corruption

---

## Prerequisites

### Required Information
1. **Module Name** — the TMOS module to migrate (e.g., `tamdlib`, `keymgmtd`, `fflag`)
2. **Workspace** — either:
   - Path to an existing TMOS workspace, OR
   - A branch name to create a new workspace

### Required Access
- Shell access to a build machine with the TMOS build system
- Perforce client configured and authenticated (`p4 info` should succeed)
- Permission to run `schroot -c rocky8.1064` (Rocky Linux chroot)

### TMOS Build System
- Valid TMOS workspace with `build` script present
- Build environment set up (`./build -setup latest` + `./build -prebuilt`)
- For new workspaces: access to `~/create_ws <branch-name>` script

### What You Do NOT Need
- Manual identification of migration issues — the agent finds them
- Knowledge of spec file syntax — the agent applies all required changes
- Manual invocation of the 64-bit subagent — triggered automatically when needed

---

## Quick Start Guide

### Most Common Use Case: Migrate a Module (Existing Workspace)

```
Migrate TMOS module tamdlib to Rocky Linux.
Workspace: /local/kramasubramanian/sources/tmos-rocky-ws2
```

The agent will ask clarifying questions, validate the module and workspace, and proceed through the migration automatically.

---

### New Workspace Migration

```
Migrate TMOS module keymgmtd to Rocky Linux.
Create a new workspace from branch: tmos-rocky-8.10
```

The agent will create the workspace at `/local/$USER/sources/`, set up the build environment, and then proceed with migration.

---

### Orchestrate Full Application or Daemon Migration

```
Migrate TMOS application or daemon tamd and all its dependencies to Rocky Linux.
```

The orchestrator uses the **existing workspace** — no workspace path or setup step is needed. It resolves the full dependency tree, migrates each module in level order, creates Perforce changelists, posts Review Board drafts, and submits automatically.

---

### Step-by-Step for First-Time Users (`tmos_rocky_migrator`)

1. **Start the agent** — type your migration request in the chat
2. **Provide module name** when prompted (or include it in the initial prompt)
3. **Confirm workspace** — specify existing path or provide branch name for new
4. **Confirm build environment** — agent will offer to set it up or update if needed
5. **Wait for 64-bit check** — agent automatically checks `32bit-modules.txt`; if the module is listed, the 64-bit subagent runs first
6. **Review spec changes** — agent shows all spec file modifications before applying
7. **Monitor build** — agent compiles, analyzes errors, applies fixes, and rebuilds iteratively
8. **Review the report** — written to `output/<module_name>/tmos_rocky_migrator_<module>_report.md`

---

## Agent Architecture

```
User Request
     │
     │  (full application/daemon migration or status query)
     ├─────────────────────────└
     │                         │
     │                         ▼
     │          rocky-migration-orchestor   ← agents/rocky-migration-orchestor.agent.md
     │                         │
     │                         ├── [Mode 1 — Query] Read daemons_apps_status.txt, build table, save to output/query_resp/
     │                         │
     │                         ├── [Mode 2 — Migration]
     │                         ├── Validate module in daemons_apps_status.txt
     │                         ├── Validate module (./build -print_pkgs)
     │                         ├── Generate dependency levels (./show-parallel-levels)
     │                         ├── Check rocky_status.txt (with file locking)
     │                         ├── Sync workspace (p4 sync + p4 resolve -am)
     │                         ├── Mark module InProgress in rocky_status.txt + daemons_apps_status.txt
     │                         ├── Invoke tmos_rocky_migrator (per module, see below)
     │                         ├── Verify RPM; retry once on failure; prompt user if needed
     │                         ├── Mark module Completed in rocky_status.txt + daemons_apps_status.txt
     │                         ├── Create Perforce CL, post Review Board draft, submit
     │                         ├── Merge AI learnings into rocky-migration-ai-learnings.SKILL.md (separate CL)
     │                         └── Write: logs/orchestor_<module>_<ts>/orchestor_run.log
     │                                   output/orchestor_<module>_<ts>/orchestor_report_<module>.md
     │
     │  (single module migration)
     └─────────────────────────┐
                               │
                               ▼
          tmos_rocky_migrator (Main Agent)   ← agents/tmos_rocky_migrator.agent.md
                               │
                               ├── Validate module name (./build -print_pkgs)
                               ├── Set up / validate workspace
                               │
                               ├── [IF module in 32bit-modules.txt]
                               │       │
                               │       └── tmos_rocky_64bit_migrator (Subagent)  ← subagents/tmos_rocky_64bit_migrator.agent.md
                               │               │
                               │               ├── Analyze source for 32→64 bit issues
                               │               ├── Apply pointer/int/format fixes
                               │               ├── Compile and verify
                               │               └── Write: logs/<module_name>_64bit/tmos_rocky_64bit_migrator_<module>.log
                               │                         output/<module_name>_64bit/tmos_rocky_64bit_migrator_<module>_report.md
                               │
                               ├── Verify 64-bit subagent success (if run)
                               ├── Check MySQL/MariaDB dependency (def.inc + spec file)
                               ├── Check MySQL Connector/J dependency (pom.xml, build.gradle, Java sources)
                               ├── Set up build environment (TASK-1)
                               ├── Checkout code (./build -p4)
                               ├── Apply mandatory spec file modifications
                               ├── Verify spec file changes
                               ├── Apply source code fixes (GCC 11, OpenSSL, Python, Perl, Java, MySQL/MariaDB)
                               ├── Compile iteratively until zero warnings/errors (TASK-2)
                               ├── Collect RPM disk space + binary static memory analysis
                               ├── Append AI learnings to ai-learnings/rocky_migration_learnings.md
                               └── Write: logs/<module_name>/tmos_rocky_migrator_<module>.log
                                         output/<module_name>/tmos_rocky_migrator_<module>_report.md
```

### Safety Constraints

The 64-bit subagent (`tmos_rocky_64bit_migrator`) has the following tools explicitly **denied** to prevent accidental damage:

| Denied Tool | Reason |
|---|---|
| `rm`, `delete`, `rmdir` | No file deletion |
| `shutdown`, `reboot`, `halt`, `poweroff` | No system operations |
| `build` | Build is orchestrated by the main agent only |

The main agent requires **explicit user permission** before:
- Modifying any source code
- Modifying makefiles
- Modifying the build environment
- Adding compiler flags
- Deleting any files

---

## Migration Workflow

The agent follows four sequential phases. Each phase must complete successfully before the next begins.

### Phase 0 (Conditional): 32-bit → 64-bit Architecture Migration

**Triggered when:** the module name appears in `input/32bit-modules.txt`

| Step | Action |
|---|---|
| 1 | Inform user that module requires 64-bit migration |
| 2 | Invoke `tmos_rocky_64bit_migrator` subagent |
| 3 | Wait for subagent completion |
| 4 | Verify: log file exists, report shows `✅ Success`, zero warnings after fixes |
| 5 | **ABORT** if any verification fails — do not proceed to Phase 1 |

**Verification checklist (automated):**
- `logs/<module_name>_64bit/tmos_rocky_64bit_migrator_<module>.log` exists and > 1 KB
- `output/<module_name>_64bit/tmos_rocky_64bit_migrator_<module>_report.md` exists and > 5 KB
- Report Executive Summary shows `✅ Success`
- Log shows `SUCCESS CRITERIA MET: Zero warnings and zero errors`

---

### Phase 1 (TASK-1): Build Environment Setup

| Step | Action |
|---|---|
| 1 | Confirm workspace type (existing path or new branch) |
| 2 | Create workspace with `~/create_ws <branch>` if new |
| 3 | Validate workspace is a valid TMOS workspace |
| 4 | Offer to run `./build -setup latest` + `./build -prebuilt` if needed |
| 5 | Abort and report if environment setup fails |

---

### Phase 2 (TASK-2): Code Migration and Compilation

| Step | Action |
|---|---|
| 1 | Checkout module with `./build -p4 <module>` |
| 2 | Log in to Rocky 8.10 chroot: `schroot -c rocky8.1064` |
| 3 | Locate spec file via module definition (`.def.inc` files in workspace root) |
| 4 | Check for MySQL Enterprise/MariaDB dependency in `depends` field and spec file |
| 4b | Check for MySQL Connector/J dependency in `pom.xml`, `build.gradle`, spec files, and Java sources |
| 5 | Apply **3 mandatory spec file modifications** (see below) |
| 6 | **Verify** all 3 modifications are present with `grep` checks |
| 7 | Scan source for Rocky 8.10 incompatibilities across all applicable migration domains |
| 8 | Apply source code and spec fixes per applicable migration domains (GCC 11, OpenSSL, Python, Perl, Java, MySQL→MariaDB, MySQL Connector/J→MariaDB Connector/J) |
| 9 | **Pre-build verification** — all spec changes confirmed, 64-bit migration verified |
| 10 | Compile: `./build --override BLD_ENV_BRANCH_NAME:tmos-rocky -arch=x86_64 <module> -j 64` |
| 11 | Analyze warnings/errors against migration skill domains |
| 12 | Apply fixes and repeat steps 10–11 until zero warnings and zero errors |
| 13 | Collect RPM disk space and binary static memory analysis (text/data/bss per ELF file) |
| 14 | Generate migration report to `output/<module_name>/` |
| 15 | Append AI learnings to `ai-learnings/rocky_migration_learnings.md` |
| 16 | Inform user with summary and next steps |
| 17 | Clean up intermediate files (keep log and report) |

#### Mandatory Spec File Modifications

All three modifications are **required** before any build attempt. The agent will abort the build if any are missing.

**Modification 1 — After spec header (Name/Version/Release/License):**
```spec
%global debug_package %{nil}
# Include GCC toolchain configuration
%include %{_topdir}/gcc-toolchain.inc
```

**Modification 2 — First line of `%build` section:**
```spec
%build
%{gcc_toolset_enable}
```

**Modification 3 — First line of `%install` section:**
```spec
%install
%{gcc_toolset_enable}
```

---

## Orchestrator Workflow

The **Rocky Migration Orchestrator** (`rocky-migration-orchestor`) automates Rocky Linux 8.10 migration of a TMOS application or daemon module **and all of its transitive dependencies**, processing them in the correct build order. Use this agent when you want to migrate an entire application stack rather than a single module.

### Orchestrator Phases

#### Step 0: Initialize Run Folder

At startup the orchestrator captures a timestamp and creates isolated, timestamped directories for all files produced by this run:

```bash
logs/orchestor_<module>_<YYYYMMDD_HHMMSS>/   # all logs, tracking files, per-module diffs
output/orchestor_<module>_<YYYYMMDD_HHMMSS>/ # final report only
```

All intermediate and output files are stored under these per-run directories. Nothing is written directly to the parent `logs/` or `output/` directories. The run log `orchestor_run.log` inside the log folder captures all steps with timestamps.

The following constants are also initialized at Step 0 and used throughout the run:

| Variable | Value |
|---|---|
| `LOCK_SCRIPT` | `ai-agents/common/scripts/file_lock.py` |
| `STATUS_FILE` | `/vol/3/share/rocky_migration/rocky_status.txt` |
| `DAEMON_APPS_FILE` | `/vol/3/share/rocky_migration/daemons_apps_status.txt` |
| `QUERY_OUT_DIR` | `ai-agents/projects/centos2rocky/output/query_resp` |
| `TMP_DIR` | `${LOG_DIR}/tmp` (per-run scratch folder; never `/tmp`) |
| `AGENT_OWNER` | Value of `$USER` at startup |

The `AGENT_OWNER` variable is used as the owner field in both status files in the form `ByAgent-<username>` whenever this agent writes a status update. It is the 5th field in `rocky_status.txt` and the 6th field in `daemons_apps_status.txt`.

#### Step 1: Determine User Intent

The orchestrator supports two modes:

**Mode 1 — Query mode** — triggered by keywords like "show", "list", "display", "what are", or "give me" combined with "daemons", "applications", or "apps". Reads `/vol/3/share/rocky_migration/daemons_apps_status.txt` and displays a formatted Markdown table (all statuses, or filtered by `NotStarted`, `Completed`, `InProgress`, or `NotApplicable`). Query output is saved to `output/query_resp/query_<type>_<YYYYMMDD_HHMMSS>.md`. No migration is performed.

**Mode 2 — Migration mode** — triggered when the user provides a daemon/application name and uses words like "migrate", "run migration for", or "start migration of". Proceeds to Step 2.

**No input / ambiguous** — displays the `NotStarted` list sorted by priority (ascending) and prompts the user to choose.

#### Step 2: Validate Module Name

First, the module name is looked up in `/vol/3/share/rocky_migration/daemons_apps_status.txt` (with file locking). If the status is `Completed`, `NotApplicable`, or `InProgress` by another user, the orchestrator informs the user and aborts. If `NotStarted`, the orchestrator immediately marks it `InProgress` in both `daemons_apps_status.txt` and `rocky_status.txt`.

Then, the build-system name is confirmed with `./build -print_pkgs <module>`. If invalid, both status files are reverted to `NotStarted`. The timestamped run folders are created after this step, using the validated module name.

#### Step 3: Generate Dependency Levels

Runs `./show-parallel-levels -q <module>` to build the full ordered dependency tree and saves the output to `${LOG_DIR}/deps_<module>.txt`:

```
level-0: module_a, module_b, module_c
level-1: module_d, module_e
level-2: module_f
...
level-N: <target_module>
```

All modules are processed from `level-0` through `level-N`, inclusive of the target module itself. Architecture suffixes (`:i686`, `:x86_64`, `:noarch`) are stripped when looking up status or invoking migration.

#### Step 4: Check Migration Status of All Dependencies

For each module across all levels, the orchestrator reads the shared Rocky migration status file (with file locking — see [Rocky Migration Status File](#rocky-migration-status-file)) and classifies modules into four tracking files in the run log folder:

| File | Content |
|---|---|
| `${LOG_DIR}/status_NotStarted.txt` | `level-N,<module>` — modules needing migration |
| `${LOG_DIR}/status_Completed.txt` | `level-N,<module>` — already migrated |
| `${LOG_DIR}/status_NotApplicable.txt` | `level-N,<module>` — migration not required |
| `${LOG_DIR}/status_InProgress.txt` | `level-N,<module>,<owner>` — being migrated by another agent |

Modules with status `Completed` or `NotApplicable` are skipped. Modules with no row in `rocky_status.txt` are treated as `NotStarted`.

#### Step 5: Migrate Modules Level-by-Level

Processes each dependency level in order. For each module in a level:

| Module Status | Action |
|---|---|
| `Completed` / `NotApplicable` | Skip silently |
| `InProgress` | Log the owning agent; skip for now; wait at end of level |
| `NotStarted` | Run sub-steps 5a–5f |

**After all `NotStarted` modules in a level are migrated**, the orchestrator waits for any `InProgress` modules from that same level (set by other concurrent agents) to reach `Completed` or `NotApplicable`, polling `rocky_status.txt` every 5 minutes. Only then does it advance to the next level.

**Before picking up each new level** — and also immediately before each individual module migration — the orchestrator runs `p4 sync` + `p4 resolve -am` to pull in changes submitted by other users.

**For each `NotStarted` module**, the following sub-steps execute in sequence:

| Sub-step | Action |
|---|---|
| **5a** | Sync workspace: `p4 sync` + `p4 resolve -am`; prompt user if merge conflicts cannot be auto-resolved |
| **5b** | Mark module `InProgress,ByAgent-${AGENT_OWNER}` in `rocky_status.txt` and `daemons_apps_status.txt`; snapshot currently open Perforce files (`p4 opened`) |
| **5c** | Invoke `tmos_rocky_migrator`: `migrate tmos module <module> for rocky using the existing workspace` |
| **5d** | Verify RPM generation under `RPMS/`; retry invocation once on failure; prompt user if retry also fails |
| **5e** | (Status is updated to `Completed` only after CL submit in step 5f) |
| **5f** | Compute diff of opened files vs. pre-migration snapshot; create dedicated Perforce changelist (only truly modified files); post Review Board draft via `/build/cm/bin/post`; submit; mark module `Completed` in both `rocky_status.txt` and `daemons_apps_status.txt`; record in `${LOG_DIR}/review_tracking.csv` |
| **5g** | Merge AI learnings from `ai-learnings/rocky_migration_learnings.md` into `skills/rocky-migration-ai-learnings.SKILL.md`; submit as a dedicated CL; archive source learnings file |

> **Note on Step 5f:** `/build/cm/bin/post create <CL>` must be run **outside the schroot session** (in the host shell). The per-module diff report is saved to `${LOG_DIR}/diff_report_<module>.txt` and records MODIFIED vs. UNMODIFIED status for every opened file. If no files were modified, the module is marked `Completed` directly with `N/A` for the CL and Review Board URL.

> **Note on Step 5g:** The SKILL file is a shared Perforce resource protected by its own lock (`/vol/3/share/rocky_migration/rocky-migration-ai-learnings-update`). The lock timeout is 15 minutes; if another agent holds it longer the orchestrator escalates to the user.

#### Step 6: Generate Orchestration Report

Writes the final report to `${OUT_DIR}/orchestor_report_<module>.md`. The report includes:

1. **Run Summary** — target module, timestamps, `LOG_DIR`/`OUT_DIR` paths, module counts (migrated / skipped / failed), overall status
2. **Per-Module CL and Review Board Tracking** — rendered from `${LOG_DIR}/review_tracking.csv` as a Markdown table:

   | Module | Dependency Level | Perforce CL | Review Board URL | Migration Status | Submit Status | Start Time | End Time | Duration |
   |---|---|---|---|---|---|---|---|---|
   | module_a | level-0 | 123456 | https://rb.example.com/r/789/ | Completed | Submitted | 2026-04-17_10:30:00 | 2026-04-17_11:45:00 | 75m 0s |

3. **Issues and Resolutions** — modules where RPM generation or submit failed and how they were resolved
4. **Artifacts** — paths to run log, review tracking CSV, per-module diff reports, and the report itself
5. **AI Performance Summary** — per-module table of migration start time, end time, duration, estimated input/output token counts, and optimization suggestions to reduce AI token usage in future runs

---

### Concurrent Migration Support

The orchestrator is designed to run simultaneously with other users migrating the same dependency graph:

- All reads and writes to `rocky_status.txt` and `daemons_apps_status.txt` use an exclusive file lock (`ai-agents/common/scripts/file_lock.py`). The lock is acquired immediately before and released immediately after each operation.
- **Stale lock detection**: if the lock is held by the same user (crashed run), the lock file is removed and acquisition is retried. If held by a different user, the agent waits and retries every 1 second — it never removes another user's lock.
- If a module is `InProgress` by another agent, this agent waits (polling every 5 minutes) until the module reaches `Completed` or `NotApplicable` before advancing to the next dependency level.
- Each successfully migrated module gets its own **dedicated Perforce changelist** — files from multiple modules are never mixed.
- The SKILL file (`rocky-migration-ai-learnings.SKILL.md`) uses a separate lock with a 15-minute escalation timeout to accommodate the time needed for LLM-based merge processing.

---

## Rocky Migration Status File

The orchestrator tracks per-module migration progress in a shared status file:

```
/vol/3/share/rocky_migration/rocky_status.txt
```

A separate file tracks the high-level migration status of each daemon/application:

```
/vol/3/share/rocky_migration/daemons_apps_status.txt
```

### `rocky_status.txt` File Format

Each row represents one TMOS module:

```
<module_name>,<field2>,<field3>,<status>,<owner>[,<start_ts>[,<end_ts>[,<cl_num>[,<rb_url>]]]]
```

| Field | Description | Values |
|---|---|---|
| 1 | Module name | Exact TMOS module name |
| 2 | (reserved) | Reserved for future use |
| 3 | (reserved) | Reserved for future use |
| 4 | Migration status | `NotStarted`, `Completed`, `NotApplicable`, `InProgress` |
| 5 | Owner | Username or `ByAgent-<username>` identifying who set this status |
| 6 | Start timestamp | Format `YYYY-MM-DD_HH:MM:SS`; set when status changes to `InProgress` |
| 7 | End timestamp | Format `YYYY-MM-DD_HH:MM:SS`; set when status changes to `Completed` |
| 8 | CL number | Perforce changelist number; `N/A` if no code changes were needed |
| 9 | Review Board URL | Review Board review URL; `N/A` if no code changes were needed |

### `daemons_apps_status.txt` File Format

Each row represents one top-level TMOS daemon or application:

```
<name>,<build_system_name>,<category>,<priority>,<status>,<owner>[,<start_ts>[,<end_ts>[,<cl_num>[,<rb_url>]]]]
```

| Field | Description | Values |
|---|---|---|
| 1 | Display name | Human-readable name of the daemon or application |
| 2 | Build system name | The exact name used in `./build` commands |
| 3 | Category | `daemon` or `application` |
| 4 | Priority | Numeric value; lower = higher priority |
| 5 | Migration status | `NotStarted`, `Completed`, `NotApplicable`, `InProgress` |
| 6 | Owner | Username or `ByAgent-<username>` identifying who set this status |
| 7 | Start timestamp | Set when status changes to `InProgress` |
| 8 | End timestamp | Set when status changes to `Completed` |
| 9 | CL number | Perforce changelist number; `N/A` if no changes needed |
| 10 | Review Board URL | Review Board review URL; `N/A` if no changes needed |

### Status Values

| Status | Meaning |
|---|---|
| `NotStarted` | Module has not yet been migrated |
| `Completed` | Migration is done; field 5 shows who completed it |
| `NotApplicable` | Module does not require Rocky Linux migration |
| `InProgress` | Currently being migrated; field 5 shows `ByAgent-<username>` |

If a module has no row in the file, the orchestrator treats it as `NotStarted`.

### File Locking

Both status files are **shared resources** — multiple orchestrator instances from different users may access them simultaneously. All reads and writes are protected by the lock script:

```
ai-agents/common/scripts/file_lock.py
```

Do not edit these files manually while any orchestration run is active.

### Perforce Tracking

`rocky_status.txt` is tracked in Perforce. The orchestrator opens it for edit (`p4 edit`) before writing, and the updated file is submitted as part of each module's changelist workflow. `daemons_apps_status.txt` follows the same pattern.

---

## Migration Domains

The agent applies nine migration knowledge domains. All are codified in the `skills/` folder.

### 1. 32-bit → 64-bit Architecture (`32bit-to-64bit-migration.SKILL.md`)

Applied when module is listed in `input/32bit-modules.txt`. Handled by the 64-bit subagent.

| Issue | Fix |
|---|---|
| `int` used for pointer storage | Change to `intptr_t`, `uintptr_t`, or `size_t` |
| `%d`/`%x` for pointer in printf | Change to `%p`, `%zu`, `PRId64`, `PRIx64` |
| `(int)ptr` casts | Use `(intptr_t)ptr` or `(uintptr_t)ptr` |
| `1 << 32` overflow | Change to `1ULL << 32` |
| Mixed `int`/`size_t` arithmetic | Use consistent `size_t` for sizes and indices |
| Unaligned pointer dereference | Replace with `memcpy()` |

### 2. GCC 11.2.x (`gcc-migration-11.SKILL.md`)

| Issue | Fix |
|---|---|
| `std::auto_ptr` | Replace with `std::unique_ptr` |
| `register` keyword | Remove (illegal in C++17) |
| `throw()` exception specs | Replace with `noexcept` |
| `std::random_shuffle` | Replace with `std::shuffle` |
| Implicit fallthrough in `switch` | Add `[[fallthrough]]` or comment |
| Narrowing conversion warnings | Add explicit casts |
| Misleading indentation | Fix indentation or add braces |
| Shared libraries without `-fPIC` | Add `-fPIC` flag (with user permission) |

### 3. OpenSSL 1.1.1k (`openssl111k-migration.SKILL.md`)

| Issue | Fix |
|---|---|
| Direct struct member access (`rsa->n`) | Use accessor API (`RSA_get0_key()`) |
| Stack-allocated contexts (`EVP_MD_CTX ctx`) | Use heap API (`EVP_MD_CTX_new()`) |
| `EVP_MD_CTX_cleanup()` | Replace with `EVP_MD_CTX_free()` |
| `SSLv23_method()` | Replace with `TLS_method()` |
| `RSA_generate_key()` | Replace with `RSA_generate_key_ex()` |
| Manual `SSL_library_init()` | Remove — automatic in 1.1.1k |

### 4. Java JDK 21 (`java-migration-jdk21.SKILL.md`)

| Issue | Fix |
|---|---|
| JAXB not available | Add `javax.xml.bind:jaxb-api` dependency |
| JAX-WS not available | Add `javax.xml.ws:jaxws-api` dependency |
| `sun.misc.Unsafe` usage | Use `VarHandle` / `MethodHandles` |
| CORBA usage | Remove or replace with alternative |
| `sun.*` internal APIs | Add `--add-exports` or migrate to public API |
| CMS GC flags | Remove or replace with G1GC flags |

### 5. Python 3 (`python3-migration.SKILL.md`)

**Applies to:** Python files (`*.py`), and any file with a `#!/usr/bin/python` or `#!/usr/bin/env python` shebang line regardless of file extension.

| Issue | Fix |
|---|---|
| `print "text"` | Change to `print("text")` |
| `raw_input()` | Replace with `input()` |
| `xrange()` | Replace with `range()` |
| `dict.iterkeys()` | Replace with `dict.keys()` |
| `except ExcType, e:` | Change to `except ExcType as e:` |
| `urllib2` imports | Change to `urllib.request` / `urllib.error` |
| `ConfigParser` | Change to `configparser` |
| Integer division `/` | Use `//` where integer result is required |

### 6. Perl 5.26+ (`perl-migration-rocky.SKILL.md`)

**Applies to:** Perl scripts (`*.pl`, `*.pm`, `*.t`), and any file with a `#!/usr/bin/perl` or `#!/usr/bin/env perl` shebang line regardless of file extension.

| Issue | Fix |
|---|---|
| `require "mylib.pl"` fails | Change to `require "./mylib.pl"` |
| Missing modules from `@INC` | Add `use lib '.';` or `use FindBin; use lib $Bin;` |
| `CGI` not available | User must install `perl-CGI` package |
| `Module::Build` not available | User must install `perl-Module-Build` package |
| `defined(@array)` deprecated | Change to `if (@array)` |
| Bareword file handles | Replace with lexical file handles |
| Two-argument `open` | Replace with three-argument `open` |
| Unescaped `{` in regex | Escape as `\{` |

### 7. MySQL Enterprise → MariaDB 10.11.10 (`mysql-mariadb-migration.SKILL.md`)

**Triggered when** `mariadb` or `mysql-enterprise` (or any `mysql*` variant) is found in the module's `depends` field or spec file.

| Issue | Fix |
|---|---|
| `mysql-enterprise-devel` in `BuildRequires` | Replace with `mariadb-connector-c-devel >= 3.0` |
| `mysql-enterprise-libs`/`-shared` in `Requires` | Replace with `mariadb-connector-c >= 3.0` |
| `my_bool` type in C/C++ source | Replace with `int` |
| `mysql_num_fields(MYSQL*)` call | Change argument to `MYSQL_RES*` |
| `-lmysqlclient` link flag | Change to `-lmariadb` or `$(mariadb_config --libs)` |
| `pkg-config --cflags mysql` in Makefiles | Change to `pkg-config --cflags mariadb` |

### 8. MySQL Connector/J → MariaDB Connector/J (`mysql-connector-java-to-mariadb-migration.SKILL.md`)

**Triggered when** `mysql-connector-java`, `mysql-enterprise-java`, or `com.mysql.jdbc`/`com.mysql.cj.jdbc` references are found in the module.

| Issue | Fix |
|---|---|
| `mysql:mysql-connector-java` in `pom.xml` | Replace with `org.mariadb.jdbc:mariadb-java-client:3.3.3` |
| `mysql-connector-java.jar` classpath in spec | Replace with `mariadb-java-client.jar` |
| `com.mysql.jdbc.Driver` / `com.mysql.cj.jdbc.Driver` | Replace with `org.mariadb.jdbc.Driver` (or remove `Class.forName()`) |
| `MysqlDataSource` | Replace with `org.mariadb.jdbc.MariaDbDataSource` |
| `jdbc:mysql://` JDBC URL | Replace with `jdbc:mariadb://` |
| `useSSL=false` connection property | Replace with `sslMode=disable` |
| `com.mysql.jdbc.exceptions.*` | Replace with standard JDBC exceptions |

### 9. DEVFS Missing Header / Library Resolution

**Triggered when** a build error reports a missing header or shared library where the include or library path points into `$(DEVFS)` / `devfs_x86_64/`.

| Step | Action |
|---|---|
| Identify missing file | Confirm Makefile uses `$(DEVFS)` / `devfs_x86_64` paths |
| Locate responsible module | Search `depends` field and `rpm -qf` for the module that should install the file |
| Check spec file | Look for `Provides: interface(devfs)` in the dependent module's spec |
| If missing | Add `Provides: interface(devfs)` to the dependent module's spec and recompile it |
| Verify | Confirm the missing file now exists in `devfs_x86_64/` before retrying the original build |

---

## Input Parameters Reference

### `tmos_rocky_migrator` Parameters

| Parameter | Required | Description | Example |
|---|---|---|---|
| Module name | Yes | Exact TMOS module name | `tamdlib`, `keymgmtd`, `fflag` |
| Workspace type | Yes | `existing` or `new` | `existing` |
| Workspace path | If existing | Full path to workspace | `/local/kramasubramanian/sources/tmos-rocky-ws2` |
| Branch name | If new | Perforce branch for new workspace | `tmos-rocky-8.10` |
| Build environment | Optional | Whether to set up / update | Agent will ask |

### `rocky-migration-orchestor` Parameters

| Parameter | Required | Description | Example |
|---|---|---|---|
| Query request | Mode 1 | Ask to list/show daemons or applications | `"show all daemons"`, `"list notstarted apps"` |
| Module name | Mode 2 | TMOS application or daemon module name (build-system name, column 2 of `daemons_apps_status.txt`) | `tamd`, `mcpd`, `tmrouted` |
| Workspace | Implicit | Uses the **existing** workspace in the current directory — no path needed | — |

> **Note:** The orchestrator does not create or set up workspaces. It requires a valid, fully set-up TMOS workspace to already be active.

### Validating Module Name

Both agents verify the module name with:
```bash
./build -print_pkgs
```

> **Note:** Module names are case-sensitive. Be precise — `mcplib`, `mcplib_common`, and `tamd` are all different modules.

---

## Output Files Reference

All output is written to `ai-agents/projects/centos2rocky/` subdirectories.

### `tmos_rocky_migrator` Outputs

| File | Location | Description |
|---|---|---|
| `tmos_rocky_migrator_<module>_report.md` | `output/<module_name>/` | Main migration report (Markdown) |
| `tmos_rocky_migrator_<module>.log` | `logs/<module_name>/` | Full build log for the Rocky migration |
| `tmos_rocky_64bit_migrator_<module>_report.md` | `output/<module_name>_64bit/` | 64-bit subagent report (if module was 32-bit) |
| `tmos_rocky_64bit_migrator_<module>.log` | `logs/<module_name>_64bit/` | 64-bit migration build log (if applicable) |
| `rpm_analysis_<module>.txt` | `logs/<module_name>/` | RPM disk space and binary static memory analysis |
| Intermediate files | `logs/<module_name>/tmp/` | Temporary files during analysis (cleaned up after run) |

### `rocky-migration-orchestor` Outputs

All orchestrator migration files are isolated in a timestamped run folder created at startup. Query mode output goes to a dedicated `query_resp/` folder.

| File | Location | Description |
|---|---|---|
| `orchestor_report_<module>.md` | `output/orchestor_<module>_<ts>/` | Final orchestration report with CL/RB table and AI performance summary |
| `orchestor_run.log` | `logs/orchestor_<module>_<ts>/` | Full timestamped run log for all steps |
| `deps_<module>.txt` | `logs/orchestor_<module>_<ts>/` | Raw output of `./show-parallel-levels` |
| `status_NotStarted.txt` | `logs/orchestor_<module>_<ts>/` | Modules requiring migration |
| `status_Completed.txt` | `logs/orchestor_<module>_<ts>/` | Already-migrated modules |
| `status_NotApplicable.txt` | `logs/orchestor_<module>_<ts>/` | Modules not requiring migration |
| `status_InProgress.txt` | `logs/orchestor_<module>_<ts>/` | Modules being migrated by other agents |
| `pre_opened_<module>.txt` | `logs/orchestor_<module>_<ts>/` | Snapshot of `p4 opened` before each module migration |
| `post_opened_<module>.txt` | `logs/orchestor_<module>_<ts>/` | Snapshot of `p4 opened` after each module migration |
| `diff_report_<module>.txt` | `logs/orchestor_<module>_<ts>/` | Per-module diff report (MODIFIED/UNMODIFIED per file) |
| `module_files_<module>.txt` | `logs/orchestor_<module>_<ts>/` | List of modified depot paths included in the CL |
| `review_tracking.csv` | `logs/orchestor_<module>_<ts>/` | Module, dep level, CL, Review Board URL, status, submit, start/end/duration (one row per module) |
| `ai_self_learnings_<module>_<ts>.log` | `logs/ai-self-learnings/` | Audit log for SKILL file merge per module |
| `query_<type>_<YYYYMMDD_HHMMSS>.md` | `output/query_resp/` | Query mode output (all / notstarted / inprogress / completed) |

> **Important:** Neither agent ever writes to `/tmp/` or other locations. All temporary files go to `logs/<module_name>/tmp/` (per module) or `logs/orchestor_<module>_<ts>/tmp/` (per orchestrator run).

---

## Build Commands Reference

| Command | Purpose |
|---|---|
| `./build -print_pkgs` | List all valid TMOS module names |
| `./build -print_pkgs <module>` | Validate a specific module name |
| `./build -print_depends 50 <module>` | Show module's dependent modules |
| `./show-parallel-levels -q <module>` | Generate full dependency tree with parallel build levels (used by orchestrator) |
| `./build <module> -j 64` | Build module with dependency check |
| `./build -nodep <module> -j 64` | Build module without dependency check |
| `./build -clean <module> -j 64` | Clean module and its dependents |
| `./build -nodep -clean <module> -j 64` | Clean module only |
| `./build -p4 <module>` | Checkout module source code from Perforce |
| `./build -setup latest` | Set up build environment to latest stable |
| `./build -prebuilt` | Install pre-built dependencies |
| `./build --override BLD_ENV_BRANCH_NAME:tmos-rocky -arch=x86_64 <module> -j 64` | Build for Rocky Linux 8.10 (x86_64) |
| `~/create_ws <branch-name>` | Create new TMOS workspace from branch |
| `/build/cm/bin/post create <CL#>` | Post a draft review on Review Board for a changelist (run **outside schroot**) |

---

## Perforce Commands Reference

Common Perforce commands used during migration:

| Command | Purpose |
|---|---|
| `p4 edit <file>` | Open file for editing (required before any change) |
| `./build -p4 <module>` | Checkout all module files for edit |
| `p4 opened` | List all currently open (checked out) files |
| `p4 diff <file>` | Show diff of local changes |
| `p4 diff -du <file>` | Unified diff format |
| `p4 revert <file>` | Undo changes to a file |
| `p4 revert -a` | Revert all unchanged files |
| `p4 change` | Create a new changelist |
| `p4 reopen -c <cl#> //...` | Move all open files to a changelist |
| `p4 describe <cl#>` | Show contents of a changelist |
| `p4 submit -c <cl#>` | Submit a changelist |
| `p4 sync` | Sync workspace to latest |
| `p4 resolve -am` | Auto-merge non-conflicting changes after sync (used by orchestrator between levels) |
| `p4 resolve -n` | List files that still need manual conflict resolution |
| `p4 annotate <file>` | Show per-line authorship (blame) |

### Typical Perforce Workflow for a Migration

```bash
# 1. Checkout module files
./build -p4 <module_name>

# 2. Make changes (agent handles this)

# 3. Review what will be submitted
p4 diff
p4 opened

# 4. Create a changelist
p4 change
# Write description: "Rocky Linux 8.10 migration for <module_name>"

# 5. Move all open files to the changelist
p4 reopen -c <changelist#> //...

# 6. Submit after successful build and testing
p4 submit -c <changelist#>
```

---

## Understanding the Report

### Single-Module Migration Report (`tmos_rocky_migrator`)

Each completed single-module migration produces a report at:
```
output/<module_name>/tmos_rocky_migrator_<module_name>_report.md
```

### Report Structure

| Section | Content |
|---|---|
| **Executive Summary** | Migration status (✅ / ❌), file count, build status, complexity rating |
| **Migration Assessment** | Which technology stacks were detected and which needed changes |
| **Files Modified** | Complete list of changed files with change types |
| **64-bit Architecture Changes** | Pointer/int fixes, format specifiers, structure alignment (if applicable) |
| **GCC 11 Changes** | C++ ABI changes, removed features, compiler warning fixes, spec file |
| **OpenSSL 1.1.1k Changes** | Opaque structure fixes, context allocation updates |
| **Java JDK 21 Changes** | Module system, removed Java EE modules, internal API access |
| **Python 3 Changes** | Print statements, unicode, iterator conversions |
| **Perl 5.26+ Changes** | `@INC` fixes, core module removals, file handle modernisation |
| **MySQL → MariaDB Changes** | Spec file, C/C++ client API changes, `my_bool`, library linking (if applicable) |
| **MySQL Connector/J → MariaDB Changes** | Driver class, JDBC URL, DataSource, connection properties (if applicable) |
| **DEVFS Resolution** | Dependent module spec changes and recompile (if applicable) |
| **Compilation Results** | Build command, status, RPMs generated, warning/error counts |
| **RPM Disk Space and Binary Static Memory Analysis** | Installed size per RPM; `text`/`data`/`bss` breakdown per ELF binary |
| **Perforce Status** | Files opened, changelist info, next steps |
| **Testing and Validation** | Recommended tests, integration verification |
| **Impact Assessment** | Functional impact, ABI compatibility, performance |
| **Recommendations** | Testing steps, documentation, dependent modules to check |
| **References** | Log file path, skill domains applied |

### Migration Status Values

| Status | Meaning |
|---|---|
| `✅ Success` | Zero warnings, zero errors, RPM generated |
| `⚠️ Partial` | Build succeeded with warnings remaining |
| `❌ Failed` | Build failed; report captures all errors for manual review |

### Complexity Ratings

| Rating | Meaning |
|---|---|
| `Low` | Spec file changes only, no source changes needed |
| `Medium` | Source changes required in 1–2 migration domains |
| `High` | Multiple migration domains affected; architecture migration or complex API changes |

### Orchestration Report (`rocky-migration-orchestor`)

Each orchestration run produces a report at:
```
output/orchestor_<module>_<YYYYMMDD_HHMMSS>/orchestor_report_<module>.md
```

| Section | Content |
|---|---|
| **Run Summary** | Target module, run timestamp, `LOG_DIR`/`OUT_DIR` paths, total modules discovered, migrated by this run, skipped, requiring user intervention, overall status |
| **Per-Module CL and Review Board Tracking** | Markdown table rendered from `review_tracking.csv`: module, dependency level, Perforce CL number, Review Board URL, migration status, submit status, start/end/duration |
| **Issues and Resolutions** | Modules where RPM generation or CL submit failed and how they were resolved |
| **Artifacts** | Paths to `orchestor_run.log`, `review_tracking.csv`, per-module diff reports, and this report |
| **AI Performance Summary** | Per-module start time, end time, duration, estimated token counts, and optimization suggestions |

---

## Examples

### Example 1: Migrate `tamdlib` (32-bit module, existing workspace)

```
Migrate TMOS module tamdlib to Rocky Linux.
Workspace: /local/kramasubramanian/sources/tmos-rocky-ws2
```

**What happens:**
1. Agent validates `tamdlib` with `./build -print_pkgs` ✅
2. Agent finds `tamdlib` in `input/32bit-modules.txt`
3. Invokes `tmos_rocky_64bit_migrator` subagent — handles pointer/int/size_t fixes
4. Verifies subagent success: reads `output/tamdlib_64bit/tmos_rocky_64bit_migrator_tamdlib_report.md`
5. Proceeds to Rocky Linux migration: spec file modifications, GCC 11 fixes
6. Compiles, fixes any remaining errors, and generates final report

**Output:**
- `logs/tamdlib_64bit/tmos_rocky_64bit_migrator_tamdlib.log`
- `output/tamdlib_64bit/tmos_rocky_64bit_migrator_tamdlib_report.md`
- `logs/tamdlib/tmos_rocky_migrator_tamdlib.log`
- `output/tamdlib/tmos_rocky_migrator_tamdlib_report.md`

---

### Example 2: Migrate `fflag` (64-bit module, new workspace)

```
Migrate TMOS module fflag to Rocky Linux.
Create a new workspace from branch: tmos-rocky-8.10
```

**What happens:**
1. Agent creates workspace at `/local/$USER/sources/` from branch `tmos-rocky-8.10`
2. Runs `./build -setup latest` and `./build -prebuilt`
3. Validates `fflag` — NOT in `32bit-modules.txt`, skips 64-bit subagent
4. Applies spec file modifications, GCC 11 source fixes
5. Compiles and generates report

**Output:**
- `logs/fflag/tmos_rocky_migrator_fflag.log`
- `output/fflag/tmos_rocky_migrator_fflag_report.md`

---

### Example 3: Module requires Java migration

```
Migrate TMOS module app-template-java to Rocky Linux.
Workspace: /local/kramasubramanian/sources/tmos-rocky-ws2
```

**What happens:**
1. Agent detects Java source files (`*.java`, `pom.xml`)
2. Applies `java-migration-jdk21.SKILL.md` knowledge
3. Fixes JAXB/JAX-WS module removals, internal API restrictions
4. Updates build descriptors if needed (pom.xml / build.gradle)
5. Compiles and generates report

---

### Example 4: Orchestrate full daemon migration

```
Migrate TMOS application or daemon tamd and all its dependencies to Rocky Linux.
```

**What happens:**
1. Orchestrator checks `/vol/3/share/rocky_migration/daemons_apps_status.txt`: `tamd` is `NotStarted` ✅, marks it `InProgress`
2. Validates `tamd` with `./build -print_pkgs` ✅
3. Runs `./show-parallel-levels -q tamd` — discovers 12 modules across 4 dependency levels
4. Reads `rocky_status.txt`: 8 modules are `Completed`, 4 are `NotStarted`
5. Processes level-0: both `NotStarted` modules — invokes `tmos_rocky_migrator` for each, creates dedicated CLs (e.g. `CL 123456`, `CL 123457`), posts Review Board drafts, submits
6. Merges AI learnings for each completed module into `rocky-migration-ai-learnings.SKILL.md`
7. Syncs workspace (`p4 sync`) before advancing to level-1
8. Processes levels 1–3 similarly, skipping `Completed` modules
9. Processes level-N: migrates `tamd` itself; marks `tamd` `Completed` in both status files
10. Generates `output/orchestor_tamd_<ts>/orchestor_report_tamd.md` with full CL/RB table and AI performance summary

**Output:**
- `logs/orchestor_tamd_<ts>/orchestor_run.log`
- `logs/orchestor_tamd_<ts>/review_tracking.csv`
- `logs/orchestor_tamd_<ts>/diff_report_<module>.txt` (one per migrated module)
- `output/orchestor_tamd_<ts>/orchestor_report_tamd.md`

---

### Example 5: Query migration status (query mode)

```
Show all daemons and applications and their Rocky migration status.
```

or

```
List all not-started daemons available for migration.
```

**What happens:**
1. Orchestrator detects query intent (keywords: "show", "list", "display")
2. Reads `/vol/3/share/rocky_migration/daemons_apps_status.txt` with file locking
3. Builds a complete formatted Markdown table in memory (all statuses, or filtered)
4. Displays the table at once and saves it to `output/query_resp/query_all_<YYYYMMDD_HHMMSS>.md`
5. No migration is performed

**Output:**
- `output/query_resp/query_all_<YYYYMMDD_HHMMSS>.md` (or `query_notstarted_`, `query_inprogress_`, `query_completed_` for filtered queries)

---

## Best Practices

### Before Starting
- Ensure your Perforce client is authenticated (`p4 info`)
- Confirm you have access to `schroot -c rocky8.1064`
- Use an existing Rocky-compatible workspace if available — avoids rebuild time
- Include the full workspace path in your initial prompt to skip the question

### During Migration
- **Do not interrupt the agent mid-task** — especially during compilation loops
- If the 64-bit subagent is running, wait for it to finish before proceeding manually
- Review spec file changes before confirming — the agent will show them to you
- If a build fails repeatedly on the same error, provide additional context about the module to help the agent apply the right fix

### After Migration
- Read the Executive Summary section of the report first for a quick pass/fail
- Check the Perforce Status section for which files are open and need a changelist
- Run the recommended tests from the Testing section before submitting
- Check dependent modules with `./build -print_depends 50 <module>` and verify they still build

### Managing Changelists
- Create a dedicated Perforce changelist per module: clear description, single purpose
- Use `p4 diff` to review all changes before submitting
- Do not mix Rocky migration changes with unrelated fixes in the same changelist

---

## Troubleshooting

### Agent stops with "64-bit migration did not complete successfully"

The 64-bit subagent returned a failure status. Check:
```bash
cat ai-agents/projects/centos2rocky/output/<module_name>_64bit/tmos_rocky_64bit_migrator_<module>_report.md
grep -i "warning:\|error:" ai-agents/projects/centos2rocky/logs/<module_name>_64bit/tmos_rocky_64bit_migrator_<module>.log | tail -30
```

Options:
- Ask the agent to retry the 64-bit migration
- Review the log manually and fix issues, then re-run

### Build fails with "file not open for edit"

A source file was changed without Perforce checkout. Run:
```bash
p4 edit <file_path>
```
Then re-run the build.

### Module name not found in `./build -print_pkgs`

- Check spelling and case: `tamdlib` not `TamdLib`
- Some modules have multiple variants (e.g., `mcplib`, `mcplib_common`) — confirm the exact name with your team
- Module may not exist in the current workspace branch

### Spec file modifications verified but build still fails with toolchain errors

Ensure you are inside the Rocky Linux chroot:
```bash
schroot -c rocky8.1064
```
The `gcc_toolset_enable` macro only resolves inside the Rocky chroot.

### Build environment setup hangs on `./build -prebuilt`

This step downloads pre-built dependencies and can take 15–30 minutes on first run. Wait for it to complete. If it fails:
- Check network connectivity to the F5 build server
- Check disk space: `df -h`
- Check if a proxy is required for your environment

### Agent modifies wrong spec file

The agent locates the spec file from the module definition in `.def.inc` files at the workspace root. If the module's `perforce_path` in the `.def.inc` file is incorrect, the wrong spec file may be found. In this case:
- Manually provide the correct spec file path to the agent
- Ask the agent to verify with `grep -r "<module_name>.spec" *.def.inc`

### Orchestrator stops mid-run with a lock error

The lock script retries indefinitely on lock contention. A permanent lock error means the lock daemon process crashed without releasing the lock. To recover:
```bash
rm -f /vol/3/share/rocky_migration/rocky_status.txt.lock
```
For the daemons/apps status file:
```bash
rm -f /vol/3/share/rocky_migration/daemons_apps_status.txt.lock
```
Verify no other user's orchestrator is actively running before doing this.

### Orchestrator marks a module InProgress but never completes it

If the orchestrator was interrupted (e.g., VS Code session closed) while a module was `InProgress`, the status file keeps that module as `InProgress` indefinitely. To recover:
```bash
# Manually reset the stale InProgress entry to NotStarted in rocky_status.txt
p4 edit /vol/3/share/rocky_migration/rocky_status.txt
sed -i 's/^<module_name>,\([^,]*\),\([^,]*\),InProgress,.*/\1,\2,NotStarted,/' /vol/3/share/rocky_migration/rocky_status.txt

# Also reset in daemons_apps_status.txt if the top-level daemon is affected
p4 edit /vol/3/share/rocky_migration/daemons_apps_status.txt
awk -F, -v OFS=, -v name='<module_name>' '$2==name { $5="NotStarted"; $6=""; $7=""; $8="" } { print }' \
    /vol/3/share/rocky_migration/daemons_apps_status.txt > /tmp/da_tmp.txt && \
    mv /tmp/da_tmp.txt /vol/3/share/rocky_migration/daemons_apps_status.txt
```
Then re-run the orchestrator. The module will be picked up again as `NotStarted`.

### `./show-parallel-levels` not found or fails

Ensure the workspace root is in `$PATH` or run as `./show-parallel-levels`. The command is located in the workspace root alongside `./build`. If it fails, confirm you are running from inside the TMOS workspace root directory.

---

## FAQs

**Q: Does the agent submit my changes to Perforce automatically?**
A: No. The agent opens files for edit and makes changes, but it never calls `p4 submit` without your explicit confirmation. Review the changes and create/submit a changelist manually after reviewing the report.

**Q: Can I run the agent on multiple modules at once?**
A: No. Start a separate conversation for each module. Each migration is an independent session.

**Q: What if my module is in `32bit-modules.txt` but I believe it doesn't need 64-bit migration?**
A: Inform the agent. It will ask for confirmation before proceeding. You can choose to skip the 64-bit subagent, though this is not recommended — unresolved 32-bit issues will surface as compiler warnings on GCC 11 under Rocky.

**Q: What if the module has no `.spec` file?**
A: Inform the agent. It will look for alternative spec file locations or ask you to provide the path. Some modules share a spec file or use a meta-package spec.

**Q: Can the agent handle modules with multiple sub-components (e.g., shared library + daemon)?**
A: Yes. The agent migrates the module as a whole — all source files under the module's directory are analysed. If individual sub-components need separate treatment, inform the agent.

**Q: What OpenSSL version is on Rocky Linux 8.10?**
A: OpenSSL 1.1.1k. The agent applies the `openssl111k-migration.SKILL.md` knowledge which covers all API changes from OpenSSL 1.0.x to 1.1.1k.

**Q: My module uses Python 2. Will the agent migrate it to Python 3?**
A: Yes — the agent applies `python3-migration.SKILL.md` for Python files. However, complex Python migrations (custom C extensions, large codebases) may require manual review. The agent will flag any patterns it cannot automatically resolve.

**Q: Where do build logs end up?**
A: All logs go to `ai-agents/projects/centos2rocky/logs/<module_name>/` for the main migrator and `logs/<module_name>_64bit/` for the 64-bit subagent. The agent never writes to `/tmp/` or other system paths.

**Q: What is the difference between `tmos_rocky_migrator` and `tmos_rocky_migrator__local`?**
A: `tmos_rocky_migrator` is the production agent (current). `tmos_rocky_migrator__local` is a local development variant. Use `tmos_rocky_migrator` for all migration work.

**Q: What is `rocky-migration-orchestor` and when should I use it?**
A: `rocky-migration-orchestor` is the full-stack orchestration agent. Use it when you want to migrate a TMOS application or daemon **and all of its dependencies** in one automated run. It invokes `tmos_rocky_migrator` internally for each module and handles Perforce changelists, Review Board posts, and submissions automatically.

**Q: Does the orchestrator submit Perforce changelists automatically?**
A: Yes. The orchestrator creates a dedicated changelist for each migrated module, posts a Review Board draft, and then calls `p4 submit` automatically. It also submits a separate CL for the SKILL file merge after each module. If either submit fails, it pauses and asks the user how to proceed.

**Q: Can I use the orchestrator to just list what daemons/applications are available to migrate?**
A: Yes. Use the query mode: ask the orchestrator to "show all daemons" or "list not-started applications". It reads `daemons_apps_status.txt` and displays a formatted table without performing any migration.

**Q: Can I run the orchestrator and `tmos_rocky_migrator` on overlapping modules at the same time?**
A: Yes, safely. Both agents read and write `rocky_status.txt` and `daemons_apps_status.txt` using the file-lock mechanism. If the manual `tmos_rocky_migrator` run sets a module's status to `Completed`, the orchestrator will skip it automatically.

**Q: My module uses MySQL Enterprise. Will the agent migrate it to MariaDB?**
A: Yes — when `mysql-enterprise` or `mariadb` appears in the module's `depends` field, the agent automatically applies `mysql-mariadb-migration.SKILL.md`, which covers spec file changes, C/C++ API changes (`my_bool`, `mysql_num_fields`, library linking), and SQL compatibility.

**Q: My Java module uses MySQL Connector/J. Will the agent migrate it to MariaDB Connector/J?**
A: Yes — when `mysql-connector-java` is detected in `pom.xml`, `build.gradle`, spec files, or Java source imports, the agent automatically applies `mysql-connector-java-to-mariadb-migration.SKILL.md`, which covers driver class, DataSource, JDBC URL, connection properties, and exception class updates.

**Q: What happens if the orchestrator is interrupted mid-run (e.g. VS Code crashes)?**
A: The run can be restarted. Modules already marked `Completed` in `rocky_status.txt` will be skipped. Any module stuck at `InProgress` from the crashed run must be manually reset to `NotStarted` (see Troubleshooting). The new run will create a fresh timestamped folder.

**Q: Can I run the orchestrator on a module that is already fully migrated?**
A: Yes. Every module already `Completed` or `NotApplicable` in `rocky_status.txt` is silently skipped. If all modules are already done, the orchestrator generates a report showing zero new migrations and exits cleanly.

**Q: Where does the orchestrator write its logs and report?**
A: All files go to timestamped subdirectories under `ai-agents/projects/centos2rocky/logs/` and `ai-agents/projects/centos2rocky/output/`. The exact paths are printed at the end of the run.

---

## Reference: File Locations

All paths are relative to `ai-agents/projects/centos2rocky/` unless otherwise noted.

| File / Directory | Purpose |
|---|---|
| `agents/tmos_rocky_migrator.agent.md` | Single-module migration agent definition |
| `agents/rocky-migration-orchestor.agent.md` | Full-stack orchestration agent definition (query + migration modes) |
| `subagents/tmos_rocky_64bit_migrator.agent.md` | 64-bit migration subagent definition |
| `skills/gcc-migration-11.SKILL.md` | GCC 4.8.5 → GCC 11 migration knowledge |
| `skills/openssl111k-migration.SKILL.md` | OpenSSL 1.0.x → 1.1.1k migration knowledge |
| `skills/java-migration-jdk21.SKILL.md` | JDK 1.8 → JDK 21 migration knowledge |
| `skills/python3-migration.SKILL.md` | Python 2 → Python 3 migration knowledge |
| `skills/perl-migration-rocky.SKILL.md` | Perl migration knowledge for Rocky Linux |
| `skills/mysql-mariadb-migration.SKILL.md` | MySQL Enterprise 5.5.53 → MariaDB 10.11.10 migration knowledge (C/C++) |
| `skills/mysql-connector-java-to-mariadb-migration.SKILL.md` | MySQL Connector/J → MariaDB Connector/J migration knowledge (Java) |
| `skills/rocky-migration-ai-learnings.SKILL.md` | Shared AI learnings accumulated across all module migrations |
| `ai-learnings/rocky_migration_learnings.md` | Per-run learnings written by `tmos_rocky_migrator` before SKILL merge |
| `ai-learnings/rocky_64bit_migration_learnings.md` | Per-run 64-bit learnings written by `tmos_rocky_migrator` before SKILL merge |
| `input/32bit-modules.txt` | List of modules requiring 64-bit migration |
| `output/<module_name>/` | Final migration report for single-module runs |
| `output/<module_name>_64bit/` | 64-bit subagent report (if module was 32-bit) |
| `output/orchestor_<module>_<ts>/` | Final orchestration report (per run) |
| `output/query_resp/` | Query mode output files (Markdown tables) |
| `logs/<module_name>/` | Build logs for single-module runs |
| `logs/<module_name>_64bit/` | 64-bit subagent build logs |
| `logs/orchestor_<module>_<ts>/` | Orchestration run logs and tracking files |
| `logs/ai-self-learnings/` | Audit logs for SKILL file merge operations |
| `ai-agents/common/instructions/general.instructions.md` | Core operating principles for all agents |
| `ai-agents/common/skills/tmos-compilation.SKILL.md` | TMOS workspace creation and build knowledge |
| `ai-agents/common/scripts/file_lock.py` | File-locking utility protecting all shared status files |
| `/vol/3/share/rocky_migration/rocky_status.txt` | Shared per-module Rocky migration status file |
| `/vol/3/share/rocky_migration/daemons_apps_status.txt` | Shared daemon/application migration registry with priority and timestamps |

---

*This manual covers agent versions as of 2026-04-22. For the latest agent capabilities, review `agents/tmos_rocky_migrator.agent.md` and `agents/rocky-migration-orchestor.agent.md` directly.*
