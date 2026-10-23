---
name: perforce-commands
description: Essential Perforce (p4) commands and workflows for software development. Covers file operations, change management, branching, merging, shelving, and workspace management for version control with Perforce.
applyTo: ["**/*.p4", "**/P4CONFIG", "**/.p4ignore", "**/clientspec", "**/PERFORCE"]
---

# Perforce Essential Commands Guide

This skill provides comprehensive guidance for using Perforce (p4) version control system in software development, covering essential commands, workflows, and best practices.

## Overview

**Perforce (Helix Core)** is a centralized version control system widely used in enterprise environments, especially for large codebases and binary files. This guide covers P4 command-line operations essential for daily development.

### Key Concepts

- **Depot**: Server-side repository (like a remote repository)
- **Workspace (Client)**: Local copy of depot files
- **Changelist**: A set of file revisions submitted together (like a commit)
- **Shelve**: Temporary storage of pending changes on server
- **Sync**: Update workspace with depot files (like pull)
- **Submit**: Send local changes to depot (like push)
- **Integration**: Merge changes between branches

## Environment Setup

### Initial Configuration

**Set environment variables:**
```bash
# Set Perforce server
export P4PORT=perforce.company.com:1666

# Set username
export P4USER=your_username

# Set workspace/client name
export P4CLIENT=your_workspace_name

# Optional: Set editor
export P4EDITOR=vim
```

**Windows PowerShell:**
```powershell
$env:P4PORT = "perforce.company.com:1666"
$env:P4USER = "your_username"
$env:P4CLIENT = "your_workspace_name"
$env:P4EDITOR = "notepad"
```

**Using P4CONFIG file (recommended):**
```bash
# Create P4CONFIG in workspace root
cd /path/to/workspace
cat > P4CONFIG << EOF
P4PORT=perforce.company.com:1666
P4USER=your_username
P4CLIENT=your_workspace_name
EOF

# Tell p4 to use P4CONFIG
export P4CONFIG=P4CONFIG
```

### Login

**Login to Perforce server:**
```bash
# Login (stores ticket)
p4 login

# Login with timeout (specify duration)
p4 login -p

# Check login status
p4 login -s

# Logout
p4 logout
```

## Workspace Management

### Creating a Workspace

**Create new client/workspace:**
```bash
# Create workspace interactively
p4 client

# Create workspace from template
p4 client -t template_name new_workspace

# View current workspace specification
p4 client -o

# Update workspace settings
p4 client workspace_name
```

**Example workspace spec:**
```
Client: username_main_workspace

Owner: username

Description:
    Main development workspace for feature work

Root: /home/username/perforce/main

Options: allwrite noclobber nocompress unlocked nomodtime normdir

SubmitOptions: submitunchanged

LineEnd: local

View:
    //depot/main/... //username_main_workspace/main/...
    //depot/shared/... //username_main_workspace/shared/...
```

### Workspace Operations

**Switch workspace:**
```bash
# List all workspaces for current user
p4 clients

# Set active workspace
export P4CLIENT=workspace_name
# Or
p4 -c workspace_name <command>

# Delete workspace
p4 client -d workspace_name

# Delete workspace and remove files
p4 client -d -f workspace_name
```

**Workspace information:**
```bash
# Show current workspace info
p4 info

# Show workspace specification
p4 client -o

# Show where depot files map to workspace
p4 where //depot/path/...

# Show workspace root
p4 -ztag info | grep clientRoot
```

## File Operations

### 1. Syncing Files (Getting Latest)

**Basic sync commands:**
```bash
# Sync entire workspace to latest
p4 sync

# Sync specific file to latest
p4 sync file.txt

# Sync directory and subdirectories
p4 sync //depot/path/...

# Sync to specific revision
p4 sync file.txt#5

# Sync to specific changelist
p4 sync @12345

# Sync to specific date
p4 sync @2024/03/13

# Force sync (overwrite local changes)
p4 sync -f

# Preview sync (don't actually sync)
p4 sync -n

# Sync and show files updated
p4 sync -v
```

**Advanced sync options:**
```bash
# Safe sync (don't overwrite writable files)
p4 sync -s

# Parallel sync (faster for large syncs)
p4 sync --parallel=threads=4

# Remove files not in depot
p4 sync --no-remove

# Sync only files client doesn't have
p4 sync -k  # Update server records only
```

### 2. Checking Out Files (Edit)

**Edit files:**
```bash
# Open file for edit
p4 edit file.txt

# Open multiple files
p4 edit file1.txt file2.txt

# Open all files in directory
p4 edit src/*.c

# Open with wildcard
p4 edit //depot/main/.../*.cpp

# Open specific file type
p4 edit -t binary image.png

# Change file type
p4 edit -t text+w file.sh  # +w = always writable
```

**Common file types:**
- `text` - Text file with line ending conversion
- `binary` - Binary file, no conversion
- `text+w` - Always writable (even when not open)
- `text+x` - Executable text file
- `text+k` - Keyword expansion (RCS keywords)
- `symlink` - Symbolic link
- `utf16` - Unicode UTF-16

### 3. Adding New Files

**Add files:**
```bash
# Add single file
p4 add newfile.txt

# Add multiple files
p4 add file1.txt file2.txt

# Add all untracked files in directory
p4 add src/...

# Add with specific file type
p4 add -t binary image.jpg

# Recursively add all new files
p4 reconcile -a

# Add and open for edit simultaneously
p4 reconcile
```

### 4. Deleting Files

**Delete files:**
```bash
# Mark file for deletion
p4 delete file.txt

# Delete multiple files
p4 delete src/old_*.c

# Delete directory contents
p4 delete //depot/path/...

# Remove file from perforce but keep local copy
p4 delete -k file.txt

# Delete and remove from workspace
p4 sync -f file.txt#none
```

### 5. Renaming/Moving Files

**Move or rename:**
```bash
# Rename file (preserves history)
p4 move oldname.txt newname.txt

# Move file to different directory
p4 move src/file.c src/new_location/file.c

# Move directory
p4 move //depot/old_dir/... //depot/new_dir/...

# Move and force overwrite
p4 move -f old.txt new.txt
```

### 6. Reverting Changes

**Revert files:**
```bash
# Revert single file (undo checkout)
p4 revert file.txt

# Revert all open files in changelist
p4 revert -c 12345 //...

# Revert all files in workspace
p4 revert //...

# Revert unchanged files only
p4 revert -a

# Revert and delete added files
p4 revert -w file.txt
```

## Changelist Management

### Creating and Managing Changelists

**Create changelist:**
```bash
# Create new pending changelist
p4 change

# Create with description
p4 change -d "Fix bug in parser"

# View pending changelists
p4 changes -s pending

# View submitted changelists
p4 changes

# View changelists for specific user
p4 changes -u username

# View changelists for specific path
p4 changes //depot/main/...
```

**Changelist operations:**
```bash
# Edit changelist description
p4 change 12345

# Delete empty changelist
p4 change -d 12345

# Move files to different changelist
p4 reopen -c 12345 file.txt

# Move files to default changelist
p4 reopen -c default file.txt

# Show files in changelist
p4 describe 12345

# Show files in pending changelist
p4 opened -c 12345
```

### Submitting Changes

**Submit changelist:**
```bash
# Submit default changelist
p4 submit

# Submit with description
p4 submit -d "Fixed null pointer bug"

# Submit specific changelist
p4 submit -c 12345

# Submit and keep files open (reopen)
p4 submit -r

# Preview submit (don't actually submit)
p4 submit -n

# Submit with options
p4 submit -f submitunchanged  # Submit even if no changes
```

**Submit workflow:**
```bash
# 1. Ensure you have latest
p4 sync

# 2. Check what you're submitting
p4 opened

# 3. Review differences
p4 diff

# 4. Run tests/build
make test

# 5. Create changelist with description
p4 change

# 6. Submit
p4 submit -c 12345
```

## Viewing Information

### File Status and History

**Check file status:**
```bash
# Show files open in workspace
p4 opened

# Show files open by all users
p4 opened -a

# Show files open in specific path
p4 opened //depot/main/...

# Show files by user
p4 opened -u username

# Have vs opened
p4 have  # Files synced to workspace
p4 opened  # Files currently checked out
```

**File history:**
```bash
# Show file history
p4 filelog file.txt

# Show detailed history
p4 filelog -l file.txt

# Show history with diffs
p4 filelog -i file.txt

# Show history for all files
p4 filelog //depot/main/...

# Limit number of revisions
p4 filelog -m 10 file.txt
```

**File information:**
```bash
# Show file details
p4 fstat file.txt

# Show detailed file stats
p4 fstat -Ol file.txt

# Show if file needs resolve
p4 resolve -n

# Show file annotations (blame)
p4 annotate file.txt

# Print file at specific revision
p4 print file.txt#5

# Print file at specific changelist
p4 print file.txt@12345
```

### Differences

**Compare files:**
```bash
# Show diff of open file vs depot
p4 diff file.txt

# Show diff with context
p4 diff -du file.txt

# Show diff for all open files
p4 diff

# Diff between revisions
p4 diff file.txt#4 file.txt#5

# Diff between branches
p4 diff2 //depot/main/file.txt //depot/release/file.txt

# Show summary of differences
p4 diff -s

# Show only changed files
p4 diff -sl  # Modified locally
p4 diff -se  # Identical to depot
```

### Search and Browse

**Search depot:**
```bash
# List files in depot
p4 files //depot/main/...

# List files with details
p4 fstat //depot/main/...

# Search for text in files
p4 grep "search_term" //depot/...

# Search with regex
p4 grep -e "regex_pattern" //depot/...

# Search in specific file types
p4 grep "TODO" //depot/.../*.cpp

# Case-insensitive search
p4 grep -i "fixme" //depot/...
```

**Browse directories:**
```bash
# List directories
p4 dirs //depot/*

# List subdirectories
p4 dirs //depot/main/*

# Show directory tree
p4 files //depot/main/...
```

## Branching and Merging

### Branch Operations

**Create branch:**
```bash
# Create branch mapping
p4 branch branch_name

# Copy files to new branch (integrate)
p4 integrate -b branch_name

# Submit branch creation
p4 submit

# Alternative: Direct integration
p4 integrate //depot/main/... //depot/feature_branch/...
p4 submit -d "Created feature branch"
```

**Branch specification example:**
```
Branch: main_to_release

Owner: username

Description:
    Integration path from main to release branch

View:
    //depot/main/... //depot/release/...
```

### Integration (Merging)

**Integrate changes between branches:**
```bash
# Integrate from one branch to another
p4 integrate //depot/source/... //depot/target/...

# Integrate specific changelist
p4 integrate -c 12345 //depot/main/... //depot/release/...

# Integrate using branch spec
p4 integrate -b branch_name

# Reverse integrate
p4 integrate -b branch_name -r

# Preview integration
p4 integrate -n //depot/main/... //depot/release/...

# Force integration (copy all)
p4 integrate -f //depot/main/... //depot/release/...

# Integrate specific files
p4 integrate //depot/main/file.txt //depot/release/file.txt
```

**Integration workflow:**
```bash
# 1. Sync target branch
p4 sync //depot/release/...

# 2. Preview integration
p4 integrate -n //depot/main/... //depot/release/...

# 3. Perform integration
p4 integrate //depot/main/... //depot/release/...

# 4. Resolve conflicts (if any)
p4 resolve

# 5. Build and test
make test

# 6. Submit integration
p4 submit -d "Integrated changes from main to release"
```

### Resolving Conflicts

**Resolve operations:**
```bash
# Auto-merge safe changes
p4 resolve -am

# Auto-accept yours (keep your version)
p4 resolve -ay

# Auto-accept theirs (use depot version)
p4 resolve -at

# Interactive resolve
p4 resolve

# Preview resolve
p4 resolve -n

# Force accept yours for all
p4 resolve -ay //...

# Force accept theirs for all
p4 resolve -at //...

# Show files needing resolve
p4 resolve -n
```

**Interactive resolve options:**
```
Resolve options:
  at - Accept theirs (use depot version)
  ay - Accept yours (keep your version)
  am - Auto-merge (safe merge)
  e  - Edit merged version
  d  - Show diff
  m  - Merge manually
  s  - Skip this file
  q  - Quit resolve
```

**Merge strategies:**
```bash
# Three-way merge (recommended)
p4 resolve -am  # Auto-merge what's safe

# Two-way merge (copy theirs)
p4 resolve -at

# Two-way merge (keep yours)
p4 resolve -ay

# Manual merge with diff3
p4 resolve -t  # Use merge tool
```

## Shelving (Temporary Storage)

### Shelve Changes

**Shelving workflow:**
```bash
# Create changelist and shelve
p4 change  # Create numbered changelist
p4 shelve -c 12345

# Shelve with description
p4 shelve -c 12345 -d "WIP: Refactoring parser"

# Shelve specific files
p4 shelve -c 12345 file1.txt file2.txt

# Update existing shelf
p4 shelve -r -c 12345

# Delete shelf
p4 shelve -d -c 12345

# List shelved changes
p4 changes -s shelved
```

### Unshelve Changes

**Restore shelved changes:**
```bash
# Unshelve into workspace
p4 unshelve -s 12345

# Unshelve specific files
p4 unshelve -s 12345 file.txt

# Unshelve to different changelist
p4 unshelve -s 12345 -c 67890

# Force unshelve (overwrite local changes)
p4 unshelve -f -s 12345

# Preview unshelve
p4 unshelve -n -s 12345
```

**Use cases for shelving:**
```bash
# 1. Save work in progress
p4 shelve -c default
p4 revert //...  # Clean workspace

# 2. Code review before submit
p4 shelve -c 12345  # Share for review

# 3. Switch tasks
p4 shelve -c feature_A
p4 revert //...
p4 unshelve -s feature_B

# 4. Backup pending changes
p4 shelve -c 12345 -d "Backup before major refactor"
```

## Advanced Operations

### Locking Files

**Lock files to prevent others from editing:**
```bash
# Lock file (exclusive checkout)
p4 lock file.txt

# Lock all open files
p4 lock

# Unlock file
p4 unlock file.txt

# Unlock all files
p4 unlock

# View locked files
p4 opened -x

# Lock files in changelist
p4 lock -c 12345
```

### File Attributes

**Set file attributes:**
```bash
# Set file type
p4 reopen -t text+x script.sh  # Executable

# Set file type to binary
p4 reopen -t binary image.png

# Keywords expansion
p4 reopen -t text+k file.c  # Enable RCS keywords

# Always writable
p4 reopen -t text+w readme.txt

# Archive attributes
p4 reopen -t text+C file.txt  # Compressed on server
```

**Attribute modifiers:**
- `+x` - Executable
- `+w` - Always writable
- `+k` - RCS keyword expansion
- `+l` - Exclusive open (lock)
- `+C` - Compressed in depot
- `+D` - Delta storage (for large files)
- `+F` - Full file storage

### Reconcile (Detect Local Changes)

**Reconcile workspace with depot:**
```bash
# Detect all local changes
p4 reconcile

# Detect added files only
p4 reconcile -a

# Detect edited files only
p4 reconcile -e

# Detect deleted files only
p4 reconcile -d

# Preview reconcile
p4 reconcile -n

# Reconcile specific path
p4 reconcile //depot/main/src/...

# Reconcile ignoring .p4ignore
p4 reconcile -I
```

### Labels and Tags

**Create and use labels:**
```bash
# Create label
p4 label release-1.0

# Tag current workspace files
p4 tag -l release-1.0

# Sync to labeled version
p4 sync @release-1.0

# List labels
p4 labels

# Delete label
p4 label -d release-1.0

# Show files in label
p4 files @release-1.0
```

## Performance and Optimization

### Parallel Operations

**Speed up operations:**
```bash
# Parallel sync (faster for many files)
p4 sync --parallel=threads=4,batch=8,batchsize=524288

# Parallel reconcile
p4 reconcile --parallel=threads=4

# Parallel submit
p4 submit --parallel=threads=4
```

### Monitoring

**Performance monitoring:**
```bash
# Show server performance
p4 monitor show

# Show server statistics
p4 ping

# Test connection
p4 info

# Show server time
p4 -ztag info | grep serverDate
```

## Useful Workflows

### Daily Development Workflow

```bash
# Morning: Start work
p4 sync                          # Get latest changes
p4 opened                        # Check for any open files

# During development
p4 edit file.c                   # Check out file
# ... make changes ...
p4 diff file.c                   # Review changes

# Before lunch: Save progress
p4 shelve -c default             # Shelve work
p4 revert //...                  # Clean workspace (optional)

# After lunch: Resume work
p4 unshelve -s 12345             # Restore work

# End of day: Submit
p4 sync                          # Get latest first
p4 reconcile                     # Detect any new/edited files
p4 resolve -am                   # Auto-merge if needed
make && make test                # Build and test
p4 submit -d "Description"       # Submit changes
```

### Code Review Workflow

```bash
# Developer: Prepare for review
p4 change                        # Create changelist
p4 shelve -c 12345              # Shelve changes
# Share changelist number 12345 with reviewer

# Reviewer: Review code
p4 describe -S 12345             # See shelved changes
p4 diff2 -du -S 12345            # Show diffs
p4 unshelve -n -s 12345          # Preview in workspace

# Developer: Submit after approval
p4 submit -c 12345
p4 shelve -d -c 12345            # Clean up shelf
```

### Branch Merge Workflow

```bash
# Prepare for merge
cd /workspace/target_branch
p4 sync                          # Get latest target

# Perform integration
p4 integrate //depot/source/... //depot/target/...
p4 resolve -am                   # Auto-merge safe changes
p4 resolve                       # Manually resolve conflicts

# Test merged code
make clean && make test

# Submit merge
p4 submit -d "Merged changes from source to target"
```

### Hotfix Workflow

```bash
# Create hotfix branch
p4 integrate //depot/release/... //depot/hotfix/...
p4 submit -d "Created hotfix branch"

# Make fix
cd /workspace/hotfix
p4 sync
p4 edit critical_file.c
# ... fix bug ...
p4 submit -d "Fixed critical bug"

# Merge back to release
p4 integrate //depot/hotfix/... //depot/release/...
p4 resolve -am
p4 submit -d "Merged hotfix to release"

# Forward integrate to main
p4 integrate //depot/hotfix/... //depot/main/...
p4 resolve -am
p4 submit -d "Merged hotfix to main"
```

## Troubleshooting

### Common Issues and Solutions

**Issue 1: File not syncing**
```bash
# Force sync
p4 sync -f file.txt

# Update server records
p4 sync -k file.txt
p4 sync file.txt
```

**Issue 2: Can't submit - out of date**
```bash
# Sync and resolve
p4 sync
p4 resolve -am
p4 submit
```

**Issue 3: Permission denied**
```bash
# Check file permissions
ls -l file.txt

# Make writable
chmod +w file.txt

# On Windows
attrib -r file.txt
```

**Issue 4: Orphaned files**
```bash
# Find files not in depot
comm -23 <(find . -type f | sort) <(p4 have | cut -d'#' -f1 | sort)

# Clean workspace
p4 sync -f
p4 clean
```

**Issue 5: Workspace out of sync**
```bash
# Reconcile everything
p4 reconcile -w

# Or clean and re-sync
p4 clean -a
p4 sync -f
```

### Recovery Commands

**Recover from mistakes:**
```bash
# Undo local changes (revert)
p4 revert //...

# Restore deleted file
p4 sync -f deleted_file.txt#head

# Rollback to previous version
p4 sync file.txt#4
p4 edit file.txt
p4 submit -d "Rolled back to revision 4"

# Undo submit (use obliterate - admin only)
# Contact Perforce admin to obliterate changelist
```

## Best Practices

### 1. Changelist Management
- Create descriptive changelist descriptions
- Keep changelists focused and atomic
- Submit frequently (small, working changes)
- Don't leave files open indefinitely

### 2. Syncing
- Sync before starting work each day
- Sync before submitting
- Use `p4 sync -p` to preview large syncs
- Consider `--parallel` for large workspaces

### 3. File Operations
- Use `p4 move` instead of manual delete/add (preserves history)
- Set correct file types (especially for binaries)
- Use `.p4ignore` for generated files
- Don't check in build artifacts

### 4. Branching
- Use branch specs for complex mappings
- Document branch purposes
- Regularly integrate between branches
- Clean up obsolete branches

### 5. Conflict Resolution
- Resolve conflicts immediately
- Test after resolving
- Use `-am` for safe auto-merges
- Don't blindly accept yours or theirs

### 6. Performance
- Use parallel operations for large syncs
- Keep workspace views focused (don't map entire depot)
- Run `p4 clean` periodically
- Use `p4 reconcile` instead of manual add/edit/delete

## .p4ignore File

**Create `.p4ignore` to exclude files:**
```
# Build artifacts
*.o
*.so
*.a
*.exe
*.dll

# IDE files
.vscode/
.idea/
*.swp
*~

# Build directories
build/
bin/
obj/
dist/

# Logs and temp files
*.log
*.tmp
temp/

# OS files
.DS_Store
Thumbs.db
```

**Enable p4ignore:**
```bash
# Set environment variable
export P4IGNORE=.p4ignore

# Or in P4CONFIG
echo "P4IGNORE=.p4ignore" >> P4CONFIG
```

## Quick Reference Card

### Most Common Commands

```bash
# Setup
p4 login                         # Login to server
p4 client                        # Set up workspace
p4 sync                          # Get latest files

# Daily operations
p4 edit file.txt                 # Check out file
p4 add newfile.txt               # Add new file
p4 delete oldfile.txt            # Delete file
p4 move old.txt new.txt          # Rename/move file
p4 revert file.txt               # Undo checkout
p4 diff                          # Show differences
p4 submit                        # Submit changes

# Status
p4 opened                        # Files checked out
p4 changes                       # Recent changes
p4 filelog file.txt              # File history
p4 info                          # Server/client info

# Shelving
p4 shelve -c 12345               # Shelve changes
p4 unshelve -s 12345             # Restore shelved

# Branching
p4 integrate src/... dest/...    # Merge branches
p4 resolve -am                   # Auto-merge

# Help
p4 help                          # General help
p4 help command                  # Command-specific help
```

## Additional Resources

- Perforce Documentation: https://www.perforce.com/manuals/cmdref/
- P4 Command Reference: https://www.perforce.com/manuals/cmdref/Content/CmdRef/commands.html
- P4V Visual Client: Alternative GUI interface
- Helix Core Best Practices: https://www.perforce.com/resources
- P4 Cheat Sheet: Quick reference for common commands

## Summary

Essential Perforce operations for development:

1. **File Operations**: edit, add, delete, move, revert
2. **Syncing**: Get latest code with p4 sync
3. **Changelist Management**: Organize and submit changes
4. **Branching/Merging**: integrate and resolve between branches
5. **Shelving**: Temporarily save work on server
6. **Status Queries**: opened, changes, filelog, diff
7. **Workspace Management**: client, where, reconcile
8. **Conflict Resolution**: resolve with merge strategies
9. **Advanced**: Labels, locks, parallel operations
10. **Best Practices**: Atomic commits, frequent syncs, descriptive changelists

Perforce provides robust version control for large-scale development with strong support for binary files, branching, and merge tracking. Master these commands to work efficiently in Perforce-based development environments.
