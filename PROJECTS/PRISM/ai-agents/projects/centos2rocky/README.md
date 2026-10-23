# 📁 centos2rocky

## Description

The **TMOS Rocky Migrator** is an AI agent system for migrating TMOS modules from CentOS 6/7 to Rocky Linux 8.10. It handles the full migration lifecycle: workspace setup, build validation, and applying fixes across GCC 11, OpenSSL 1.1.1k, Java JDK 21, Python 3, Perl 5.26+, MySQL Enterprise 5.5.53 → MariaDB 10.11.10, and MySQL Connector/J → MariaDB Connector/J. For modules listed in `input/32bit-modules.txt`, it automatically invokes the 64-bit migration subagent to handle `int`/pointer width incompatibilities, format specifier fixes, and alignment-unsafe casts.

For migrating full application or daemon stacks, the **Rocky Migration Orchestrator** (`rocky-migration-orchestor`) automates the end-to-end workflow: it supports two modes — **Query Mode** (list daemons/applications and their Rocky migration status) and **Migration Mode** (orchestrate full Rocky Linux 8.10 migration of a daemon/application and all its dependencies). In Migration Mode it resolves the full transitive dependency tree, checks the shared Rocky migration status file to skip already-migrated modules, invokes `tmos_rocky_migrator` level-by-level, and creates a dedicated Perforce changelist with a Review Board draft for each migrated module.

## 📋 Folder Structure

```
centos2rocky/
├── agents/
│   ├── tmos_rocky_migrator.agent.md                    # Single-module migration agent
│   └── rocky-migration-orchestor.agent.md              # Full-stack dependency orchestration agent
├── subagents/
│   └── tmos_rocky_64bit_migrator.agent.md              # 32-bit → 64-bit migration subagent
├── skills/
│   ├── gcc-migration-11.SKILL.md                       # GCC 4.8.5 → GCC 11.2.x migration knowledge
│   ├── openssl111k-migration.SKILL.md                  # OpenSSL 1.0.1 → 1.1.1k migration knowledge
│   ├── java-migration-jdk21.SKILL.md                   # JDK 1.8 → JDK 21 migration knowledge
│   ├── python3-migration.SKILL.md                      # Python 2 → Python 3 migration knowledge
│   ├── perl-migration-rocky.SKILL.md                   # Perl migration knowledge for Rocky
│   ├── mysql-mariadb-migration.SKILL.md                # MySQL Enterprise 5.5.53 → MariaDB 10.11.10 migration knowledge
│   ├── mysql-connector-java-to-mariadb-migration.SKILL.md  # MySQL Connector/J → MariaDB Connector/J migration knowledge
│   └── rocky-migration-ai-learnings.SKILL.md           # Self-healing knowledge base (auto-updated by agents)
├── ai-learnings/                                       # Archived per-module AI learning artifacts
├── instructions/                                       # (reserved for project-specific instruction files)
├── input/
│   └── 32bit-modules.txt                               # List of modules requiring 64-bit migration
├── output/
│   └── query_resp/                                     # Query mode responses (daemons/apps status listings)
├── reports/                                            # (reserved for additional reports)
├── logs/                                               # Execution logs and debug info
├── scripts/                                            # Scripts needed by agents/subagents
├── USER_MANUAL.md                                      # Detailed usage guide
└── README.md                                           # This file
```

## 📂 Directory Details

| Directory       | Purpose                                                                                          |
|-----------------|--------------------------------------------------------------------------------------------------|
| `agents/`       | `tmos_rocky_migrator.agent.md` — single-module migration agent; `rocky-migration-orchestor.agent.md` — full-stack dependency orchestration agent |
| `subagents/`    | `tmos_rocky_64bit_migrator.agent.md` — invoked automatically for modules in `32bit-modules.txt`  |
| `skills/`       | Domain knowledge skill files for each migration area (GCC, OpenSSL, JDK, Python, Perl, MySQL→MariaDB, MySQL Connector/J→MariaDB Connector/J, AI learnings) |
| `ai-learnings/` | Archived per-module AI learning artifacts generated during migration                             |
| `instructions/` | Reserved for project-specific `*.instructions.md` files                                          |
| `input/`        | `32bit-modules.txt` — list of TMOS modules that need 32-bit → 64-bit migration                   |
| `output/`       | Migration reports generated per module; `query_resp/` subdirectory holds orchestrator query mode responses |
| `reports/`      | Reserved for additional report artifacts                                                         |
| `logs/`         | Agent execution logs, build output captures, and debug info                                      |
| `scripts/`      | Store scripts that are used by agents/subagents                                                  |

## 🤖 Agents

### Orchestration Agent: `rocky-migration-orchestor`

| Field          | Value                                                                                              |
|----------------|-----------------------------------------------------------------------------------------------------|
| **Agent File** | `agents/rocky-migration-orchestor.agent.md`                                                         |
| **Model**      | Claude Sonnet 4.6                                                                                   |
| **Invocation** | `Migrate TMOS application or daemon <module name> and all its dependencies to Rocky Linux` or `List daemons/applications and their Rocky migration status` |
| **Tools**      | execute, read, edit, search, agent, todo, agent/runSubagent                                         |

**What it does:**

This agent operates in two modes:

**Query Mode** — triggered when the user asks to list/show daemons or applications:
1. Reads `/vol/3/share/rocky_migration/daemons_apps_status.txt` (with exclusive file locking)
2. Builds a fully formatted Markdown table in memory (sections: NotStarted, Completed, NotApplicable, InProgress)
3. Displays the table and saves a copy to `output/query_resp/query_<type>_<timestamp>.md`

**Migration Mode** — triggered when the user specifies a daemon/application to migrate:
1. Validates the target module name against the TMOS build system (`./build -print_pkgs`)
2. Checks `/vol/3/share/rocky_migration/daemons_apps_status.txt` — proceeds only if status is `NotStarted`
3. Creates isolated, timestamped run folders under `logs/` and `output/` for all produced files
4. Generates the full transitive dependency tree via `./show-parallel-levels -q <module>`
5. Checks the shared Rocky migration status file (`/vol/3/share/rocky_migration/rocky_status.txt`) — with exclusive file locking — to classify each module as `NotStarted`, `Completed`, `NotApplicable`, or `InProgress`
6. Processes dependency levels in order (level-0 first, target module last); skips `Completed`/`NotApplicable` modules; waits for `InProgress` modules owned by other concurrent agents
7. For each `NotStarted` module: syncs the workspace (`p4 sync` + `p4 resolve -am`), marks the module `InProgress` in the status file, invokes `tmos_rocky_migrator`, verifies RPM generation, marks the module `Completed`, and creates a dedicated Perforce changelist with a Review Board draft and auto-submits
8. Produces a final orchestration report with a per-module Perforce CL / Review Board URL table

**Concurrent-safe:** Multiple orchestrator instances from different users can run simultaneously. All reads and writes to `rocky_status.txt` and `daemons_apps_status.txt` are protected by the file-lock script at `ai-agents/common/scripts/file_lock.py`.

---

### Single-Module Agent: `tmos_rocky_migrator`

| Field          | Value                                                                                    |
|----------------|------------------------------------------------------------------------------------------|
| **Agent File** | `agents/tmos_rocky_migrator.agent.md`                                                    |
| **Model**      | Claude Sonnet 4.6                                                                        |
| **Invocation** | `Migrate TMOS module <module name> to Rocky Linux`                                       |
| **Tools**      | execute, read, edit, search, web, agent, todo, agent/runSubagent                         |

**What it does:**
1. Validates the module name against the TMOS build system (`./build -print_pkgs`)
2. Sets up or validates the workspace (new branch or existing path)
3. Reads general instructions from `ai-agents/common/instructions/general.instructions.md`
4. Checks if module depends on MySQL/MariaDB → applies MySQL Enterprise 5.5.53 → MariaDB 10.11.10 migration using `mysql-mariadb-migration.SKILL.md`
5. Checks if module depends on MySQL Connector/J → applies MySQL Connector/J → MariaDB Connector/J migration using `mysql-connector-java-to-mariadb-migration.SKILL.md`
6. Applies Rocky Linux 8.10 migration fixes across all relevant technology stacks (GCC 11, OpenSSL 1.1.1k, JDK 21, Python 3, Perl 5.26+)
7. Automatically invokes `tmos_rocky_64bit_migrator` subagent for modules in `32bit-modules.txt`
8. Produces a per-module migration report in `output/`

### Subagent: `tmos_rocky_64bit_migrator`

| Field              | Value                                                                           |
|--------------------|---------------------------------------------------------------------------------|
| **Agent File**     | `subagents/tmos_rocky_64bit_migrator.agent.md`                                  |
| **Model**          | Claude Opus 4.6                                                                 |
| **User-invocable** | No — invoked only by the main agent                                             |
| **Denied Tools**   | rm, delete, rmdir, shutdown, reboot, halt, poweroff, build (safety constraints) |

**What it does:**
- Analyzes source code for 32-bit to 64-bit incompatibilities using `32bit-to-64bit-migration.SKILL.md`
- Identifies `int`/`long` pointer width mismatches, `%lu`/`%ld` format specifiers, unaligned memory accesses
- Guides fixes for `size_t`, `uint64_t`, `PRIu64`/`PRIx64` macro adoption
- Reports all issues with file, function, and line attribution before making any changes

## 📚 Skills

| Skill File                                          | Covers                                                                                         |
|-----------------------------------------------------|------------------------------------------------------------------------------------------------|
| `gcc-migration-11.SKILL.md`                         | GCC 4.8.5 → GCC 11.2.x: compiler warnings, deprecated features, C++ standard changes          |
| `openssl111k-migration.SKILL.md`                    | OpenSSL 1.0.1 → 1.1.1k: API changes, opaque structures, deprecated functions                  |
| `java-migration-jdk21.SKILL.md`                     | JDK 1.8 → JDK 21: module system, removed APIs, language enhancements                          |
| `python3-migration.SKILL.md`                        | Python 2 → Python 3: syntax, standard library, encoding changes                               |
| `perl-migration-rocky.SKILL.md`                     | Perl migration for Rocky Linux 8.10 / Perl 5.26+                                              |
| `mysql-mariadb-migration.SKILL.md`                  | MySQL Enterprise 5.5.53 → MariaDB 10.11.10: C/C++ API, spec file, library linking, SQL changes |
| `mysql-connector-java-to-mariadb-migration.SKILL.md` | MySQL Connector/J 5.1.x → MariaDB Connector/J: Maven/Gradle deps, JDBC URL, driver class changes |
| `rocky-migration-ai-learnings.SKILL.md`             | Self-healing knowledge base auto-updated by agents after each successful module migration       |

## 📝 Quick Start

**Migrate a single module using an existing workspace:**
```
Migrate TMOS module tamdlib to Rocky Linux.
Workspace: /local/kramasubramanian/sources/tmos-rocky-ws2
```

**Migrate a single module with a new workspace:**
```
Migrate TMOS module keymgmtd to Rocky Linux.
Create a new workspace from branch: tmos-rocky-8.10
```

The `tmos_rocky_migrator` agent will:
1. Validate the module name and workspace
2. Check if the module is in `input/32bit-modules.txt` → invoke 64-bit subagent if so
3. Check if module depends on MySQL/MariaDB or MySQL Connector/J → apply relevant migration
4. Apply all relevant Rocky Linux migration fixes
5. Generate a report to `output/tmos_rocky_migrator_{module}_report.md`

---

**List all daemons/applications and their Rocky migration status:**
```
List all daemons and applications and their Rocky migration status.
```

The `rocky-migration-orchestor` agent will:
1. Read `/vol/3/share/rocky_migration/daemons_apps_status.txt` (with file locking)
2. Build a formatted Markdown table grouped by status (NotStarted, Completed, NotApplicable, InProgress)
3. Save the output to `output/query_resp/query_all_<timestamp>.md`

---

**Migrate a full application or daemon and all its dependencies:**
```
Migrate TMOS application or daemon tamd and all its dependencies to Rocky Linux.
```

The `rocky-migration-orchestor` agent will:
1. Validate the module name and check `daemons_apps_status.txt` (status must be `NotStarted`)
2. Generate the full dependency tree
3. Check `rocky_status.txt` — skip already-migrated modules
4. Invoke `tmos_rocky_migrator` for each `NotStarted` module, level by level
5. Create a dedicated Perforce changelist, post a Review Board draft, and submit for each module
6. Generate a timestamped orchestration report to `output/orchestor_<module>_<ts>/orchestor_report_<module>.md`

## 📋 Input Files

| File                    | Description                                                                     |
|-------------------------|---------------------------------------------------------------------------------|
| `input/32bit-modules.txt` | Alphabetical list of TMOS modules requiring 32-bit → 64-bit migration. The main agent checks this list to decide whether to invoke the 64-bit subagent. |

## 📊 Sample Output Reports

### `tmos_rocky_migrator` outputs

| Report File                                          | Module    | Description                             |
|------------------------------------------------------|-----------|------------------------------------------|
| `output/tmos_rocky_migrator_tamdlib_report.md`       | tamdlib   | Rocky migration report for tamdlib       |
| `output/tmos_rocky_64bit_migrator_tamdlib_report.md` | tamdlib   | 64-bit migration sub-report for tamdlib  |

### `rocky-migration-orchestor` outputs — Query Mode

All query output files are saved under `output/query_resp/`.

| File                              | Location               | Description                                              |
|-----------------------------------|------------------------|----------------------------------------------------------|
| `query_all_<timestamp>.md`        | `output/query_resp/`   | All daemons/applications grouped by status               |
| `query_notstarted_<timestamp>.md` | `output/query_resp/`   | NotStarted entries sorted by priority                    |
| `query_inprogress_<timestamp>.md` | `output/query_resp/`   | InProgress entries with owner and start time             |
| `query_completed_<timestamp>.md`  | `output/query_resp/`   | Completed entries with CL number and Review Board URL    |

### `rocky-migration-orchestor` outputs — Migration Mode

All orchestrator files are placed in isolated, timestamped subdirectories created at run startup.

| File                                                              | Location                              | Description                                              |
|-------------------------------------------------------------------|---------------------------------------|----------------------------------------------------------|
| `orchestor_report_<module>.md`                                    | `output/orchestor_<module>_<ts>/`     | Final report with per-module CL / Review Board URL table |
| `orchestor_run.log`                                               | `logs/orchestor_<module>_<ts>/`       | Full timestamped run log for all orchestration steps     |
| `review_tracking.csv`                                             | `logs/orchestor_<module>_<ts>/`       | Module, CL number, Review Board URL, submit status       |
| `diff_report_<dependent_module>.txt`                              | `logs/orchestor_<module>_<ts>/`       | Per-module diff report (MODIFIED / UNMODIFIED per file)  |

## ℹ️ Metadata

| Field        | Value                        |
|--------------|------------------------------|
| Folder Name  | centos2rocky                 |
| Full Path    | `./projects/centos2rocky`    |
| Created By   | kramasubramanian             |
| Created On   | 2026-03-17 22:51:53          |
| Generated By | ai-template-create.sh        |
| Last Updated | 2026-04-22                   |
