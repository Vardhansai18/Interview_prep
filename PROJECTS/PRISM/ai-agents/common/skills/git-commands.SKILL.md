---
name: git-commands
description: Essential Git commands and workflows for software development. Covers repository management, branching, merging, remote operations, stashing, and collaboration workflows for distributed version control with Git.
applyTo: ["**/.git/**", "**/.gitignore", "**/.gitattributes", "**/.gitmodules", "**/.gitconfig"]
---

# Git Essential Commands Guide

This skill provides comprehensive guidance for using Git distributed version control system in software development, covering essential commands, workflows, and best practices.

## Overview

**Git** is a distributed version control system widely used for source code management. Every developer has a complete copy of the repository history, enabling offline work and flexible workflows.

### Key Concepts

- **Repository (Repo)**: Complete project history and working directory
- **Commit**: Snapshot of changes at a point in time
- **Branch**: Independent line of development
- **Remote**: Reference to repository on another machine (e.g., GitHub, GitLab)
- **Working Directory**: Local files you're editing
- **Staging Area (Index)**: Files prepared for next commit
- **HEAD**: Pointer to current branch/commit

### Git Workflow Stages

```
Working Directory → Staging Area → Local Repository → Remote Repository
     (edit)      →    (add)     →     (commit)     →     (push)
```

## Initial Setup

### Configuration

**Set user identity (required):**
```bash
# Set name (used in commits)
git config --global user.name "Your Name"

# Set email (used in commits)
git config --global user.email "your.email@company.com"

# Set default editor
git config --global core.editor "vim"

# Set default branch name
git config --global init.defaultBranch main

# Enable colored output
git config --global color.ui auto
```

**View configuration:**
```bash
# View all settings
git config --list

# View specific setting
git config user.name

# View with origin (where setting is from)
git config --list --show-origin

# Edit global config file
git config --global --edit
```

**Configuration levels:**
```bash
# System-wide (all users)
git config --system

# User-level (current user)
git config --global

# Repository-level (current repo only)
git config --local
```

### SSH Key Setup

**Generate SSH key for Git hosting:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@company.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key (add to GitHub/GitLab)
cat ~/.ssh/id_ed25519.pub
```

**Test connection:**
```bash
# Test GitHub connection
ssh -T git@github.com

# Test GitLab connection
ssh -T git@gitlab.com
```

## Repository Operations

### Creating Repositories

**Initialize new repository:**
```bash
# Create new repository in current directory
git init

# Create new repository in specific directory
git init my-project

# Create bare repository (for server)
git init --bare project.git

# Initialize with specific branch name
git init -b main
```

**Clone existing repository:**
```bash
# Clone repository
git clone https://github.com/user/repo.git

# Clone to specific directory
git clone https://github.com/user/repo.git my-folder

# Clone specific branch
git clone -b develop https://github.com/user/repo.git

# Clone with depth (shallow clone)
git clone --depth 1 https://github.com/user/repo.git

# Clone specific tag
git clone --branch v1.0 https://github.com/user/repo.git
```

### Repository Information

**Check repository status:**
```bash
# Show status of working directory
git status

# Short status format
git status -s

# Show branch information
git status -sb

# Show ignored files
git status --ignored
```

**View repository details:**
```bash
# Show commit history
git log

# Show compact history
git log --oneline

# Show with graph
git log --graph --oneline --all

# Show last N commits
git log -n 5

# Show commits by author
git log --author="John"

# Show commits with specific message
git log --grep="bugfix"

# Show commits between dates
git log --since="2024-01-01" --until="2024-12-31"

# Show file changes
git log --stat

# Show patch (actual changes)
git log -p
```

## Basic File Operations

### Adding Files to Staging

**Stage files for commit:**
```bash
# Add specific file
git add file.txt

# Add multiple files
git add file1.txt file2.txt

# Add all files in directory
git add src/

# Add all modified and new files
git add .

# Add all files including deleted
git add -A
git add --all

# Add only modified files (not new)
git add -u
git add --update

# Interactive add
git add -i

# Add parts of file (patch mode)
git add -p file.txt
```

### Committing Changes

**Create commits:**
```bash
# Commit staged changes
git commit

# Commit with message
git commit -m "Fix bug in parser"

# Commit with detailed message
git commit -m "Fix bug" -m "Detailed explanation here"

# Commit all modified files (skip staging)
git commit -a -m "Update all tracked files"

# Amend last commit (change message or add files)
git commit --amend

# Amend without changing message
git commit --amend --no-edit

# Empty commit (trigger CI without changes)
git commit --allow-empty -m "Trigger CI"
```

**Commit message best practices:**
```bash
# Good commit message format:
# <type>: <subject>
#
# <body>
#
# <footer>

# Example:
git commit -m "feat: Add user authentication

Implemented JWT-based authentication system.
Added login, logout, and token refresh endpoints.

Closes #123"
```

### Removing Files

**Delete files:**
```bash
# Remove file from working directory and staging
git rm file.txt

# Remove from Git but keep locally
git rm --cached file.txt

# Remove directory
git rm -r directory/

# Force remove (even if modified)
git rm -f file.txt

# Remove files matching pattern
git rm '*.log'
```

### Moving/Renaming Files

**Rename or move files:**
```bash
# Rename file
git mv oldname.txt newname.txt

# Move file to directory
git mv file.txt src/

# Equivalent to:
# mv oldname.txt newname.txt
# git rm oldname.txt
# git add newname.txt
```

### Viewing Changes

**Show differences:**
```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --cached
git diff --staged

# Show changes in specific file
git diff file.txt

# Show changes between commits
git diff commit1 commit2

# Show changes between branches
git diff main feature

# Show word-level diff
git diff --word-diff

# Show summary only
git diff --stat

# Compare with remote
git diff main origin/main
```

## Branch Management

### Creating and Switching Branches

**Branch operations:**
```bash
# List branches
git branch

# List all branches (including remote)
git branch -a

# List remote branches
git branch -r

# Create new branch
git branch feature-login

# Create and switch to branch
git checkout -b feature-login
# Or with newer syntax:
git switch -c feature-login

# Switch to existing branch
git checkout main
git switch main

# Switch to previous branch
git checkout -
git switch -

# Create branch from specific commit
git branch feature abc123

# Create branch from tag
git branch release-fix v1.0.0
```

### Branch Information

**View branch details:**
```bash
# Show current branch
git branch --show-current

# Show branches with last commit
git branch -v

# Show merged branches
git branch --merged

# Show unmerged branches
git branch --no-merged

# Show branches containing commit
git branch --contains abc123

# Track remote branch
git branch -vv
```

### Deleting Branches

**Remove branches:**
```bash
# Delete merged branch
git branch -d feature-login

# Force delete (even if unmerged)
git branch -D feature-login

# Delete remote branch
git push origin --delete feature-login

# Prune deleted remote branches
git fetch --prune
git remote prune origin
```

### Renaming Branches

**Rename branch:**
```bash
# Rename current branch
git branch -m new-name

# Rename specific branch
git branch -m old-name new-name

# Rename and update remote
git branch -m old-name new-name
git push origin :old-name new-name
git push origin -u new-name
```

## Merging and Rebasing

### Merging Branches

**Merge operations:**
```bash
# Merge branch into current branch
git merge feature-branch

# Merge with commit message
git merge feature-branch -m "Merge feature"

# No fast-forward (always create merge commit)
git merge --no-ff feature-branch

# Fast-forward only (fail if not possible)
git merge --ff-only feature-branch

# Abort merge
git merge --abort

# Continue after resolving conflicts
git merge --continue
```

**Merge strategies:**
```bash
# Default recursive strategy
git merge feature

# Ours (keep our version on conflict)
git merge -X ours feature

# Theirs (take their version on conflict)
git merge -X theirs feature

# Squash merge (combine all commits)
git merge --squash feature
git commit -m "Merged feature branch"
```

### Resolving Conflicts

**Handle merge conflicts:**
```bash
# 1. See conflicted files
git status

# 2. View conflict
cat conflicted-file.txt
# Shows:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>> feature-branch

# 3. Edit file to resolve

# 4. Mark as resolved
git add conflicted-file.txt

# 5. Complete merge
git commit

# Tools for conflict resolution
git mergetool

# Checkout versions
git checkout --ours file.txt   # Use our version
git checkout --theirs file.txt  # Use their version
```

### Rebasing

**Rebase operations:**
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (edit history)
git rebase -i HEAD~3

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip

# Abort rebase
git rebase --abort

# Rebase onto specific commit
git rebase abc123

# Preserve merge commits
git rebase -p main
```

**Interactive rebase commands:**
```bash
# Rebase last 3 commits
git rebase -i HEAD~3

# Available commands in editor:
# pick   - use commit
# reword - use commit, edit message
# edit   - use commit, stop for amending
# squash - combine with previous commit
# fixup  - like squash, discard message
# drop   - remove commit
```

**Rebase workflow:**
```bash
# Update feature branch with latest main
git checkout feature
git fetch origin
git rebase origin/main

# Or with pull --rebase
git pull --rebase origin main
```

## Remote Operations

### Managing Remotes

**Remote repository operations:**
```bash
# Add remote
git remote add origin https://github.com/user/repo.git

# List remotes
git remote

# List remotes with URLs
git remote -v

# Show remote details
git remote show origin

# Rename remote
git remote rename origin upstream

# Change remote URL
git remote set-url origin https://github.com/user/new-repo.git

# Remove remote
git remote remove origin
```

### Fetching and Pulling

**Get changes from remote:**
```bash
# Fetch all remotes
git fetch

# Fetch specific remote
git fetch origin

# Fetch specific branch
git fetch origin main

# Fetch all branches and tags
git fetch --all

# Fetch and prune deleted branches
git fetch --prune

# Pull (fetch + merge)
git pull

# Pull specific branch
git pull origin main

# Pull with rebase
git pull --rebase

# Pull and fast-forward only
git pull --ff-only
```

### Pushing Changes

**Send changes to remote:**
```bash
# Push to remote
git push

# Push to specific remote and branch
git push origin main

# Push and set upstream
git push -u origin feature-branch

# Push all branches
git push --all

# Push tags
git push --tags

# Force push (overwrite remote)
git push --force
# Safer force push
git push --force-with-lease

# Delete remote branch
git push origin --delete feature-branch

# Push specific tag
git push origin v1.0.0
```

## Stashing Changes

### Save Work in Progress

**Stash operations:**
```bash
# Stash current changes
git stash

# Stash with message
git stash save "WIP: Refactoring parser"
git stash push -m "WIP: Refactoring parser"

# Stash including untracked files
git stash -u
git stash --include-untracked

# Stash including ignored files
git stash -a
git stash --all

# Stash specific files
git stash push path/to/file.txt

# List stashes
git stash list

# Show stash contents
git stash show
git stash show -p stash@{0}

# Apply stash (keep in stack)
git stash apply
git stash apply stash@{1}

# Pop stash (apply and remove)
git stash pop
git stash pop stash@{1}

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear

# Create branch from stash
git stash branch feature-branch stash@{0}
```

## Tags

### Creating and Managing Tags

**Tag operations:**
```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag specific commit
git tag -a v1.0.0 abc123 -m "Release 1.0.0"

# List tags
git tag

# List tags with pattern
git tag -l "v1.*"

# Show tag information
git show v1.0.0

# Push specific tag
git push origin v1.0.0

# Push all tags
git push --tags

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0

# Checkout tag (detached HEAD)
git checkout v1.0.0

# Create branch from tag
git checkout -b release-1.0 v1.0.0
```

## Undoing Changes

### Reverting Changes

**Undo operations:**
```bash
# Discard changes in working directory
git checkout -- file.txt
git restore file.txt

# Discard all changes
git checkout -- .
git restore .

# Unstage file (keep changes)
git reset HEAD file.txt
git restore --staged file.txt

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert commit (create new commit)
git revert abc123

# Revert multiple commits
git revert abc123..def456

# Revert merge commit
git revert -m 1 merge-commit-hash
```

**Reset modes:**
```bash
# Soft: Keep changes in staging
git reset --soft HEAD~1

# Mixed (default): Keep changes in working dir
git reset HEAD~1
git reset --mixed HEAD~1

# Hard: Discard all changes
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard abc123

# Reset to remote state
git reset --hard origin/main
```

### Recovering Lost Commits

**Use reflog to recover:**
```bash
# Show reflog (all HEAD movements)
git reflog

# Show reflog for specific branch
git reflog show feature-branch

# Recover lost commit
git checkout abc123
git cherry-pick abc123
git reset --hard abc123
```

## Advanced Operations

### Cherry-Pick

**Apply specific commits:**
```bash
# Cherry-pick single commit
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick range
git cherry-pick abc123..def456

# Cherry-pick without committing
git cherry-pick -n abc123

# Continue after conflict
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort
```

### Bisect (Find Bug)

**Binary search for bug:**
```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good abc123

# Git will checkout middle commit
# Test and mark:
git bisect good  # If works
git bisect bad   # If fails

# Repeat until bug found

# End bisect
git bisect reset

# Automated bisect
git bisect start HEAD abc123
git bisect run ./test-script.sh
```

### Submodules

**Manage submodules:**
```bash
# Add submodule
git submodule add https://github.com/user/lib.git libs/mylib

# Initialize submodules
git submodule init

# Update submodules
git submodule update

# Clone with submodules
git clone --recurse-submodules https://github.com/user/repo.git

# Update submodules to latest
git submodule update --remote

# Execute command in all submodules
git submodule foreach git pull
```

### Worktrees

**Multiple working directories:**
```bash
# Create worktree
git worktree add ../hotfix hotfix-branch

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../hotfix

# Prune worktrees
git worktree prune
```

### Clean

**Remove untracked files:**
```bash
# Show what would be removed
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Remove ignored files too
git clean -fdx

# Interactive clean
git clean -i
```

## Inspection and Comparison

### Viewing File Content

**Show file at specific revision:**
```bash
# Show file from HEAD
git show HEAD:file.txt

# Show file from specific commit
git show abc123:file.txt

# Show file from branch
git show main:src/app.js

# Show commit details
git show abc123
```

### Blame/Annotate

**Track line changes:**
```bash
# Show who changed each line
git blame file.txt

# Show with commit hashes
git blame -l file.txt

# Show line ranges
git blame -L 10,20 file.txt

# Show blame for specific commit
git blame abc123 file.txt

# Ignore whitespace changes
git blame -w file.txt
```

### Search

**Search repository:**
```bash
# Search in tracked files
git grep "search_term"

# Search with line numbers
git grep -n "search_term"

# Search in specific branch
git grep "search_term" main

# Search for regex
git grep -E "regex.*pattern"

# Show count of matches
git grep -c "search_term"

# Search commit messages
git log --all --grep="search_term"

# Search diffs
git log -S "search_term"

# Search by author
git log --author="John Doe"
```

## Collaboration Workflows

### Feature Branch Workflow

**Typical feature development:**
```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-auth

# 3. Work on feature
git add .
git commit -m "Add login functionality"

# 4. Push to remote
git push -u origin feature/user-auth

# 5. Keep updated with main
git fetch origin
git rebase origin/main

# 6. Create pull request (on GitHub/GitLab)

# 7. After merge, cleanup
git checkout main
git pull origin main
git branch -d feature/user-auth
```

### Gitflow Workflow

**Structured branching model:**
```bash
# Main branches: main (production), develop (integration)

# Start feature
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# Finish feature
git checkout develop
git merge --no-ff feature/new-feature
git push origin develop
git branch -d feature/new-feature

# Start release
git checkout -b release/1.0.0 develop
# Make release preparations
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0
git checkout develop
git merge --no-ff release/1.0.0

# Hotfix
git checkout -b hotfix/critical-bug main
# Fix bug
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1
git checkout develop
git merge --no-ff hotfix/critical-bug
```

### Forking Workflow

**Contributing to open source:**
```bash
# 1. Fork repository on GitHub

# 2. Clone your fork
git clone https://github.com/yourusername/repo.git

# 3. Add upstream remote
git remote add upstream https://github.com/original/repo.git

# 4. Create feature branch
git checkout -b feature/improvement

# 5. Make changes and commit
git add .
git commit -m "Improve performance"

# 6. Keep fork updated
git fetch upstream
git rebase upstream/main

# 7. Push to your fork
git push origin feature/improvement

# 8. Create pull request on GitHub

# 9. Update with upstream changes
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

## Configuration Files

### .gitignore

**Ignore files and directories:**
```gitignore
# Build artifacts
*.o
*.so
*.exe
*.dll
*.dylib
build/
dist/
target/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Dependency directories
node_modules/
venv/
.env

# Logs and databases
*.log
*.sql
*.sqlite

# OS files
Thumbs.db
.DS_Store

# Secrets
.env
secrets.yml
*.key
*.pem

# Temporary files
*.tmp
*.temp
tmp/
temp/

# Compiled Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# Java
*.class
*.jar
*.war

# Package files
*.tar.gz
*.zip
```

**Global gitignore:**
```bash
# Create global ignore file
git config --global core.excludesfile ~/.gitignore_global

# Add common patterns
cat >> ~/.gitignore_global << EOF
.DS_Store
*.swp
*~
EOF
```

### .gitattributes

**Control line endings and diffs:**
```gitattributes
# Auto detect text files
* text=auto

# Specific files
*.txt text
*.sh text eol=lf
*.bat text eol=crlf

# Binary files
*.png binary
*.jpg binary

# Language-specific
*.cs text diff=csharp
*.java text diff=java

# Generated files
dist/* linguist-generated=true
```

## Useful Aliases

**Create shortcuts:**
```bash
# Status shortcuts
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# Log aliases
git config --global alias.lg "log --oneline --graph --all"
git config --global alias.last "log -1 HEAD"
git config --global alias.unstage "reset HEAD --"

# Diff aliases
git config --global alias.df "diff"
git config --global alias.dc "diff --cached"

# Complex aliases
git config --global alias.lol "log --graph --decorate --pretty=oneline --abbrev-commit --all"
git config --global alias.contributors "shortlog -sn"
```

**Use aliases:**
```bash
git st          # Instead of git status
git co main     # Instead of git checkout main
git lg          # Pretty graph
```

## Troubleshooting

### Common Issues

**Issue 1: Detached HEAD**
```bash
# You're on a commit, not a branch
# Create branch to keep changes
git checkout -b temp-branch

# Or go back to branch
git checkout main
```

**Issue 2: Merge conflicts**
```bash
# See conflicted files
git status

# Abort merge if needed
git merge --abort

# After resolving
git add resolved-file.txt
git commit
```

**Issue 3: Accidentally committed to wrong branch**
```bash
# Move last commit to new branch
git branch new-branch
git reset --hard HEAD~1
git checkout new-branch
```

**Issue 4: Need to undo public commit**
```bash
# Create revert commit (safe for public branches)
git revert abc123

# Don't use reset on public branches!
# git reset --hard HEAD~1  # DANGEROUS if pushed
```

**Issue 5: Large file committed**
```bash
# Remove from history (requires rewriting history)
git filter-branch --tree-filter 'rm -f large-file.zip' HEAD

# Or use BFG Repo-Cleaner
# More info: https://rtyley.github.io/bfg-repo-cleaner/
```

**Issue 6: Wrong commit message**
```bash
# If not pushed
git commit --amend -m "Correct message"

# If already pushed (risky)
git commit --amend -m "Correct message"
git push --force-with-lease
```

## Best Practices

### 1. Commit Practices
- Write clear, descriptive commit messages
- Make small, focused commits (atomic commits)
- Commit working code (builds and tests pass)
- Don't commit secrets or credentials
- Use conventional commit format

### 2. Branch Practices
- Keep branches short-lived
- Use descriptive branch names (feature/, bugfix/, hotfix/)
- Delete merged branches
- Regularly sync with main branch

### 3. Merge vs Rebase
- Use merge for public branches
- Use rebase for local feature branches
- Never rebase public history
- Keep history clean but honest

### 4. Remote Practices
- Pull before pushing
- Use --force-with-lease instead of --force
- Don't rewrite public history
- Push regularly to backup work

### 5. General Tips
- Use .gitignore to exclude build artifacts
- Make frequent small commits
- Write good commit messages
- Review changes before committing (git diff)
- Use branches for new features
- Keep main/master stable

## Quick Reference

### Daily Commands

```bash
# Morning routine
git checkout main
git pull origin main
git checkout -b feature/new-work

# During work
git status
git add .
git commit -m "Description"
git push -u origin feature/new-work

# Update branch
git fetch origin
git rebase origin/main

# End of day
git push origin feature/new-work
```

### Essential Commands

```bash
# Setup
git config --global user.name "Name"
git config --global user.email "email"
git init
git clone <url>

# Basic operations
git status
git add <file>
git commit -m "Message"
git push
git pull

# Branching
git branch
git checkout -b <branch>
git merge <branch>
git branch -d <branch>

# History
git log
git log --oneline --graph
git diff
git show <commit>

# Undo
git restore <file>
git reset HEAD~1
git revert <commit>

# Remote
git remote -v
git fetch
git push origin <branch>
git pull --rebase

# Stash
git stash
git stash pop
git stash list
```

## Git vs Perforce Quick Comparison

| Operation | Git | Perforce |
|-----------|-----|----------|
| Get latest | `git pull` | `p4 sync` |
| Check out | `git add` | `p4 edit` |
| Commit local | `git commit` | N/A |
| Push to server | `git push` | `p4 submit` |
| Create branch | `git branch` | `p4 branch` |
| Switch branch | `git checkout` | `p4 client` |
| Show changes | `git diff` | `p4 diff` |
| Revert | `git restore` | `p4 revert` |
| History | `git log` | `p4 filelog` |

## Additional Resources

- Official Git Documentation: https://git-scm.com/doc
- Pro Git Book (free): https://git-scm.com/book
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf
- Learn Git Branching: https://learngitbranching.js.org/
- GitHub Guides: https://guides.github.com/
- Atlassian Git Tutorials: https://www.atlassian.com/git/tutorials

## Summary

Essential Git operations for development:

1. **Configuration**: Set user info, editor, aliases
2. **File Operations**: add, commit, rm, mv, restore
3. **Branches**: create, switch, merge, delete
4. **Remote Operations**: clone, fetch, pull, push
5. **History**: log, diff, show, blame
6. **Stashing**: Temporarily save work
7. **Undoing**: restore, reset, revert, reflog
8. **Collaboration**: feature branches, pull requests, forks
9. **Advanced**: cherry-pick, rebase, bisect, submodules
10. **Best Practices**: Clear commits, branch workflows, clean history

Git's distributed nature enables flexible workflows, offline work, and powerful branching strategies. Master these commands to collaborate effectively and maintain clean project history.
