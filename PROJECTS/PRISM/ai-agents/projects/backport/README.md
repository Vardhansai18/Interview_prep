# Backport Agent — User Manual

**Version**: 1.1  
**Last Updated**: 2026-06-25

## Overview

The **Backport Agent** automates the F5 BIG-IP SCI 2.0 backport workflow. It takes a
Bugzilla bug ID and a submitted Perforce changelist, then cherry-picks the fix into
all supported version branches via BFO (Branch Fix Only), posting ReviewBoard reviews
for each.

It replaces the manual steps of `autofix --bfo`:
`bfo branch` → `p4 integrate @=<CL>` → `p4 resolve -am` → `/build/cm/bin/post create`

---

## Quick Start

### 1. Prerequisites

Set the following environment variable in your shell (add to `~/.bashrc` for persistence):

```bash
export BUGZILLA_API_KEY='<your-api-key>'
```

Get your API key from: https://bugzilla.f5net.com/userprefs.cgi?tab=apikey

> **Note (seadev servers):** On seadev build servers, you must also run an explicit
> Bugzilla login even if `BUGZILLA_API_KEY` is set. The agent handles this
> automatically, but if you see "log in" errors, verify your API key is valid.

### 2. Invoke the Agent

In VS Code Copilot Chat, type:

```
@backport <BugID> <CL>
```

**Examples:**
```
@backport 1571817 3907003
@backport 2312245 3913522
@backport 2326449-1 3914999
```

Both inputs are **required**:
- **BugID** — The parent Bugzilla bug number (e.g. `1571817`), or a clone alias (e.g. `2326449-1`)
- **CL** — The submitted Perforce changelist number to cherry-pick (e.g. `3907003`)

### 3. What Happens

The agent will automatically:

1. **Login** to Bugzilla (handles seadev auth automatically)
2. **Verify** Bugzilla authentication
3. **Discover** all sub-bug clones and the parent bug's version
4. **Identify** which versions need backporting (skipping the source branch)
5. **For each version**:
   - Find a clean P4 workspace (ws1 through ws5)
   - Create a BFO branch
   - Cherry-pick integrate the source CL
   - Auto-merge resolve
   - Create a numbered changelist with proper description
   - Post a ReviewBoard review
6. **Print a summary** table with all ReviewBoard URLs

### 4. After the Agent Finishes

The agent **does NOT submit** any changelists. You must:

1. Review and publish each ReviewBoard
2. Get approvals from reviewers
3. Submit each CL after approval:
   ```bash
   cd <workspace_path>
   ./hotfix/bfo switch <INDEX>
   /build/cm/bin/post submit <CL>
   ./hotfix/bfo switch
   ```
4. Mark each clone bug as Resolved/STAGED in Bugzilla

---

## Supported Versions

The agent backports to these SCI 2.0 supported versions only:

| Version | Branch Suffix | Depot Base (maint) | BFO Depot |
|---|---|---|---|
| 17.1.x | `bigip17.1.x-bugs` | `//depot/maint/bigip17.1.x-bugs/` | `//depot/bfo/bigip17.1.x-bugs/` |
| 17.5.x | `bigip17.5.x-bugs` | `//depot/maint/bigip17.5.x-bugs/` | `//depot/bfo/bigip17.5.x-bugs/` |
| 21.0.x | `bigip21.0.x-bugs` | `//depot/maint/bigip21.0.x-bugs/` | `//depot/bfo/bigip21.0.x-bugs/` |
| 21.1.x | `bigip21.1.x-bugs` | `//depot/maint/bigip21.1.x-bugs/` | `//depot/bfo/bigip21.1.x-bugs/` |
| Quartz | `tmos-dns-bugs` | `//depot/tmos/dns-bugs/` | `//depot/bfo/dns-bugs/` |

**Unsupported** (never backported): 14.1.x, 15.1.x, 16.1.x

Reference: https://docs.f5net.com/pages/viewpage.action?spaceKey=PDRDT&title=SCI+2.0

---

## Workspace Management

The agent uses P4 workspaces following this naming convention:

```
<USER>-<HOSTNAME>-<BRANCH_SUFFIX>-ws<N>
```

Example: `annam-seadev35-bigip17.5.x-bugs-ws1`

**Workspace root**: `/local/<USER>/<CLIENT_NAME>`

### Workspace Selection Rules

- The agent tries **ws1 through ws5** in order
- Uses the **first workspace with no open files**
- **Never modifies, shelves, or reverts** open files in any workspace
- If all existing workspaces are busy, **creates a new one** from the ws1 template

### After Backport

Each version's workspace will have open files (the posted ReviewBoard CL).
These workspaces are "busy" until you submit or revert those CLs.

---

## How Target Discovery Works

The agent finds backport targets from **two sources**:

### 1. Sub-bug Aliases
Queries Bugzilla for aliases `<BugID>-1`, `<BugID>-2`, ..., `<BugID>-12`.
Each sub-bug's `%{version}` field determines its target branch.

### 2. Parent Bug's Version
Queries the parent bug's own `%{version}` field. If it maps to a supported branch
**different** from the source CL's branch, it's added as a backport target.

**Why this matters**: A fix may be submitted to a clone branch (e.g. 17.1.x) while
the parent bug is filed against a different version (e.g. 17.5.x). Without checking
the parent's version, 17.5.x would be missed.

### Skip Logic
- **Source branch** — The branch where the CL was submitted (never backport to itself)
- **Unsupported versions** — 14.1.x, 15.1.x, 16.1.x
- **Already backported** — BFO exists with 2+ submitted CLs, or maint files already identical

---

## Safety Guarantees

| Rule | Description |
|---|---|
| **No submits** | Only creates ReviewBoards — never runs `p4 submit` |
| **No patches** | Always uses `p4 integrate @=<CL>` (cherry-pick), never diff/patch |
| **No file edits** | Never hand-edits files — uses P4 integrate + resolve only |
| **No reverts** | Never reverts or modifies open files in any workspace |
| **No clone creation** | Does not create Bugzilla clone bugs — only discovers existing ones |

---

## Troubleshooting

### "BUGZILLA_API_KEY not set" or "log in" errors
Set the environment variable:
```bash
export BUGZILLA_API_KEY='<your-key>'
```
Get a key from: https://bugzilla.f5net.com/userprefs.cgi?tab=apikey

If the key is set but you still get "log in" errors (common on seadev servers), run:
```bash
bugzilla --bugzilla https://bugzilla.f5net.com login --api-key "$BUGZILLA_API_KEY"
```
The agent runs this automatically at startup, but manual login may help if the
cached token has expired.

### "bfo type context has N overlays"
The workspace's client view has leftover BFO overlay mappings. Fix:
```bash
p4 client -o > /tmp/spec.txt
grep -v "//depot/bfo/" /tmp/spec.txt > /tmp/spec_clean.txt
p4 client -i < /tmp/spec_clean.txt
p4 sync -f build.def
```

### "file ... does not exist" during `bfo branch`
The file path is excluded from the client view (common for `el7.3/`, `ports/pam_tacplus/`).
Fix by removing the exclusion:
```bash
p4 client -o > /tmp/spec.txt
# Remove the '-' prefix from the exclusion line for the affected path
sed -i 's|-//depot/.../<path>/...|//depot/.../<path>/...|' /tmp/spec.txt
p4 client -i < /tmp/spec.txt
p4 sync "//depot/.../<path>/..."
```

### "all revision(s) already integrated"
This is normal — `bfo branch` already integrated the file from maint. The cherry-pick
integrate may show this. Check `p4 diff` to verify the fix is applied correctly.

### Workspace has open files (all ws1-ws5 busy)
Either submit/revert CLs in existing workspaces, or increase the workspace limit
in the agent file (search for `for N in 1 2 3 4 5`).

### Merge conflicts after `p4 resolve -am`
If `p4 resolve -n` shows unresolved files after auto-merge, the agent will stop
and ask you to resolve manually:
```bash
cd <workspace_path>
export P4CLIENT=<workspace>
p4 resolve    # interactive resolve
p4 diff       # verify
```

---

## Changelist Format

Each backport CL follows this format:

```
STAGED: Change: <SOURCE_CL>, on <BRANCH>-bugs
======================================================================
Integrate Change: <SOURCE_CL>, for <BRANCH>-bugs

Original description:
     <original CL description>
------------------------------------------------------------
```

The `Jobs:` field references the **clone bug ID** (not the alias).
For versions where no clone exists (e.g. parent's own version), the parent bug ID is used.

---

## Agent File Location

```
~/.vscode-server/data/User/agents/backport.agent.md
```

To modify agent behavior, edit this file directly. Key sections:
- **PERFORMANCE RULES** — Controls command batching strategy
- **Step 0b** — SCI supported version list
- **Step 1** — Target discovery logic
- **Step 3b** — Workspace selection (ws1-ws5 range)
- **Constraints** — Safety rules and limits
- **Known Issues** — Workarounds for common problems

---

## Example Output

After a successful backport, the agent prints:

### ReviewBoard Summary

| Version | Clone Bug ID | CL | ReviewBoard | Status |
|---|---|---|---|---|
| bigip21.0.x-bugs | 2333365 | 3915046 | https://reviewboard.olympus.f5net.com/r/346422/ | RB Posted |
| bigip17.5.x-bugs | 2333369 | 3915056 | https://reviewboard.olympus.f5net.com/r/346424/ | RB Posted |
| bigip17.1.x-bugs | 2333373 | 3915068 | https://reviewboard.olympus.f5net.com/r/346426/ | RB Posted |
| tmos-dns-bugs | 2333377 | 3915076 | https://reviewboard.olympus.f5net.com/r/346428/ | RB Posted |

### Workspace Details

| Version | Workspace Path | P4 Client | BFO Index |
|---|---|---|---|
| 21.0.x | /local/annam/annam-seadev35-bigip21.0.x-bugs-ws1 | annam-seadev35-bigip21.0.x-bugs-ws1 | 201 |
| 17.5.x | /local/annam/annam-seadev35-bigip17.5.x-bugs-ws2 | annam-seadev35-bigip17.5.x-bugs-ws2 | 606 |
| 17.1.x | /local/annam/annam-seadev35-bigip17.1.x-bugs-ws1 | annam-seadev35-bigip17.1.x-bugs-ws1 | 2249 |
| Quartz | /local/annam/annam-seadev35-tmos-dns-bugs-ws1 | annam-seadev35-tmos-dns-bugs-ws1 | 903 |
