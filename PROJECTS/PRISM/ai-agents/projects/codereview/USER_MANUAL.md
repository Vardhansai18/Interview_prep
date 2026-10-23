# Code Review Agent - User Manual

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Prerequisites](#prerequisites)
4. [Quick Start Guide](#quick-start-guide)
5. [Detailed Usage Instructions](#detailed-usage-instructions)
6. [Input Parameters Reference](#input-parameters-reference)
7. [Analysis Modes](#analysis-modes)
8. [Understanding the Output](#understanding-the-output)
9. [Examples](#examples)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)
12. [FAQs](#faqs)

---

## Overview

The **Code Review Agent** is an automated code review tool that downloads diffs from Review Board and performs comprehensive analysis of code changes. It identifies potential issues across multiple dimensions including regression risks, performance concerns, architectural problems, security vulnerabilities, and coding guideline violations.

**What it does:**
- Downloads code changes (diffs) from Review Board automatically
- Analyzes changes across any programming/scripting language
- Identifies 5 major categories of issues: Regression, Performance, Architecture, Security, and Coding Guidelines
- Generates detailed reports with actionable recommendations
- Creates Review Board-ready summaries for easy posting

**Who should use it:**
- Developers submitting code for review
- Code reviewers looking for automated assistance
- Team leads ensuring code quality standards
- Security teams performing security audits

---

## Key Features

### 🔍 Multi-Dimensional Analysis
- **Regression Risk Detection** - Identifies changes that might break existing functionality
- **Performance Analysis** - Spots inefficient algorithms, memory leaks, and resource issues
- **Architectural Review** - Checks for design patterns, code organization, and maintainability
- **Security Vulnerability Scanning** - Detects injection flaws, authentication issues, cryptographic weaknesses
- **Coding Guideline Compliance** - Verifies adherence to team standards and best practices

### 🌐 Language Support
Supports analysis for:
- C/C++ (including 64-bit compatibility checks)
- Python
- JavaScript/TypeScript
- Shell scripts
- Java, Ruby, Go, Rust
- Configuration files (Makefile, YAML, JSON, RPM Spec)

### 📊 Report Formats
- **Detailed Report** - Complete analysis with file-by-file breakdown (`rb_{id}_review_report.md`)
- **Review Board Summary** - Concise summary ready to paste into Review Board (`rb_{id}_review_summary.txt`)
- **Severity-Ranked Issues** - Critical, High, Medium, and Low priority categorization

### 🔐 Two Analysis Modes
1. **Diff-Only Mode** - Analyzes based solely on the diff (works anywhere)
2. **Remote Session Mode** - Deep analysis with full source code access (recommended for complex changes)

---

## Prerequisites

Before using the Code Review Agent, ensure you have:

### Required Information
1. **Review Board ID (RB ID)** - The numeric identifier of your review request
   - Example: `340168`
   - Found in the Review Board URL: `https://reviewboard.olympus.f5net.com/r/340168/`

2. **API Token** - Your Review Board authorization token
   - **How to get it:**
     1. Log in to Review Board
     2. Navigate to: `Account` → `API Tokens` → `Generate New Token`
     3. Give it a name (e.g., "Code Review Agent")
     4. Copy the generated token
   - Keep your token secure - treat it like a password!

### Optional (But Recommended)
3. **Diff Version** - Which revision of the diff to analyze (default: 1)
4. **Review Board URL** - If using a different instance (default: https://reviewboard.olympus.f5net.com)
5. **Source Code Path** - Full path to your workspace for deep analysis (remote session mode only)
6. **Change Context** - Brief description of what you're changing and why

### Access Requirements
- For **diff-only mode**: Just RB ID and API token
- For **remote session mode**: SSH/terminal access to a machine with the full codebase

---

## Quick Start Guide

### Most Common Use Case: Basic Diff Review

1. **Get your Review Board ID**
   - Example: Your review is at `https://reviewboard.olympus.f5net.com/r/340168/`
   - Your RB ID is: `340168`

2. **Get your API token** (one-time setup)
   - Go to Review Board → Account → API Tokens → Generate New Token
   - Copy the token and save it somewhere secure

3. **Invoke the agent**
   ```
   @code_review_agent review RB 340168
   ```

4. **Provide the information when prompted:**
   - RB ID: `340168`
   - API Token: `[paste your token]`
   - Diff version: `1` (or press Enter for default)
   - Review Board URL: Press Enter for default
   - Remote session: `no` (for quick analysis)
   - Change context: `Fixing memory leak in module X`

5. **Wait for analysis** (typically 1-3 minutes depending on diff size)

6. **Review the results:**
   - Check the console output for immediate findings
   - Open `rb_340168_review_report.md` for detailed analysis
   - Copy content from `rb_340168_review_summary.txt` to post on Review Board

**That's it!** You now have automated code review feedback.

---

## Detailed Usage Instructions

### Step 1: Prepare Your Information

Before starting, gather:
- ✅ Review Board ID (from your review URL)
- ✅ API Token (from Review Board → API Tokens)
- ✅ Diff version number (usually `1` for first submission)
- ✅ Brief description of your changes

### Step 2: Invoke the Agent

**Option A: Quick Invocation**
```
@code_review_agent review RB 340168
```

**Option B: Detailed Invocation**
```
Review code changes from Review Board 340168 with diff version 1 using my API token
```

**Option C: With Context**
```
@code_review_agent review RB 340168 - analyzing changes for 64-bit migration
```

### Step 3: Interactive Dialog

The agent will ask you a series of questions. Here's what to expect:

#### Question 1: Review Board ID
```
Please provide the Review Board ID (RB ID) you want to analyze:
```
**Answer:** Enter the numeric ID (e.g., `340168`)

#### Question 2: Authorization Token
```
Please provide your Review Board authorization token or API key:
```
**Answer:** Paste your API token
**Tip:** The token will be masked for security (only first 4 and last 4 characters shown in confirmations)

#### Question 3: Diff Version
```
Which diff version do you want to review? (Press Enter for default: 1)
```
**Answer:** Enter the version number or press Enter for version 1
**Tip:** Check Review Board to see available diff versions if you've updated your review

#### Question 4: Review Board URL
```
Review Board URL? (Press Enter for default: https://reviewboard.olympus.f5net.com)
```
**Answer:** Press Enter for default or provide custom URL

#### Question 5: Remote Session Access
```
Are you running in a remote session with access to the complete source code repository? (yes/no)
```
**Answer:** 
- `yes` - If you're on a machine with the full codebase (recommended for thorough analysis)
- `no` - If you only want diff-based analysis (faster but less comprehensive)

#### Question 6 (if yes to Q5): Codebase Path
```
Please provide the full path to the codebase:
```
**Answer:** Enter the full path, examples:
- `/local/username/sources/tmos-rocky-workspace`
- `/home/dev/projects/myproject`

The agent will verify this path exists.

#### Question 7: Change Context
```
Please provide a brief summary of the reason for these changes:
```
**Answer:** Describe what you're changing and why, examples:
- `Fixing memory leak in connection pool module`
- `Adding 64-bit architecture support for mcplib`
- `Migrating from OpenSSL 1.0.1 to 1.1.1k`
- `Refactoring authentication logic for better testability`

**Why this matters:** Context helps the agent understand your intent and provide more relevant feedback.

### Step 4: Confirm and Proceed

The agent will display a confirmation:
```
Review Board ID: 340168
Diff version: 1
Review Board URL: https://reviewboard.olympus.f5net.com
Authorization token: abc*****xyz (masked)
Remote session mode: yes
Codebase path: /local/username/sources/workspace
Change context: Fixing memory leak in module X

Please confirm to proceed (yes/no):
```

Type `yes` to start the analysis.

### Step 5: Analysis Phase

The agent will now:
1. ✅ Download the diff from Review Board
2. 📊 Parse and categorize changes
3. 🔍 Analyze for regression risks
4. ⚡ Check for performance issues
5. 🏗️ Review architectural concerns
6. 🔐 Scan for security vulnerabilities
7. 📋 Verify coding guideline compliance
8. 📝 Generate comprehensive reports

**Progress updates** will appear in the console.

### Step 6: Review Results

When complete, you'll receive:

**Console Output:** High-level summary and critical findings

**Generated Files:**
- `rb_340168_review_report.md` - Full detailed report
- `rb_340168_review_summary.txt` - Concise Review Board summary
- `rb_340168_diff.patch` - Downloaded diff (for reference)

---

## Input Parameters Reference

| Parameter | Required | Default | Description | Example |
|-----------|----------|---------|-------------|---------|
| **Review Board ID** | ✅ Yes | None | Numeric identifier of the review request | `340168` |
| **API Token** | ✅ Yes | None | Review Board authentication token | `abc123def456...` |
| **Diff Version** | No | `1` | Which revision of the diff to analyze | `1`, `2`, `3` |
| **Review Board URL** | No | `https://reviewboard.olympus.f5net.com` | Base URL of Review Board instance | Custom URL |
| **Remote Session** | No | `no` | Whether running with full source code access | `yes` or `no` |
| **Codebase Path** | Conditional | None | Full path to source repository (required if remote session = yes) | `/local/user/sources/workspace` |
| **Change Context** | No | Inferred | Brief description of changes and purpose | `Fixing bug #12345` |

---

## Analysis Modes

### Diff-Only Mode (Default)

**When to use:**
- Quick reviews
- Small, isolated changes
- Changes that don't affect many other files
- When source code access isn't available

**What it analyzes:**
- Changes visible in the diff
- Logic within modified functions
- Code patterns and best practices
- Security issues in changed code
- Coding style compliance

**Limitations:**
- Cannot check cross-file dependencies
- Cannot verify impact on calling code
- Cannot search for similar patterns in other files
- Limited context for complex refactoring

**Example:**
```
Remote session mode: no
Codebase path: Not provided - analysis based on diff only
```

### Remote Session Mode (Recommended for Complex Changes)

**When to use:**
- Large refactoring across multiple files
- Changes to public APIs or interfaces
- Modifications to shared data structures
- When you need to verify calling code
- Complex architectural changes

**What it analyzes (in addition to diff-only):**
- Cross-file dependencies and references
- Impact on calling code across the codebase
- Similar patterns that might need the same fix
- Complete function implementations for context
- Related files affected by interface changes

**Requirements:**
- Terminal/SSH access to a machine with the full codebase
- Valid path to the source code repository
- Read permissions on the source files

**Example:**
```
Remote session mode: yes
Codebase path: /local/jdoe/sources/tmos-rocky-workspace

Additional analysis performed:
- Searched for all callers of modified functions
- Verified interface compatibility across 47 files
- Found 3 similar patterns requiring the same fix
```

### Choosing the Right Mode

| Your Scenario | Recommended Mode | Why |
|---------------|------------------|-----|
| Fixing a typo in a comment | Diff-Only | Simple, no impact analysis needed |
| Changing a private function | Diff-Only | Internal to the file |
| Modifying a public API | Remote Session | Need to check all callers |
| Refactoring across 10+ files | Remote Session | Complex dependencies |
| Changing a data structure | Remote Session | Need to verify all usages |
| Fixing a simple bug | Diff-Only | Unless bug exists elsewhere |
| Migrating to new library version | Remote Session | Wide-ranging impact |

---

## Understanding the Output

### Report Structure

#### 1. Executive Summary
Located at the top of `rb_{id}_review_report.md`:

```markdown
## Code Review Summary

**Overall Assessment:** Approved with Comments
**Analysis Mode:** Remote session with full codebase access
**Change Context:** Fixing memory leak in connection pool

**Statistics:**
- Files Changed: 5
- Lines Added: 127 | Lines Removed: 83
- Issues Found: 12 (Critical: 1, High: 3, Medium: 5, Low: 3)
```

**What it means:**
- **Overall Assessment:**
  - ✅ **Approved** - No significant issues, ready to merge
  - ⚠️ **Approved with Comments** - Minor issues, can merge after addressing
  - 🛑 **Needs Work** - Significant issues must be fixed before merge
  - ❌ **Rejected** - Critical issues, major rework required

- **Analysis Mode:** Tells you if deep analysis was performed

- **Statistics:** Quick overview of changes and issues

#### 2. Issue Breakdown by File

For each modified file:

```markdown
## File: src/connection_pool.c

### Regression Issues
- [HIGH] Line 145: Removed null check before pointer dereference
  - Impact: Could cause segmentation fault if pool is not initialized
  - Suggested fix: Add null check before accessing pool->connections

### Performance Issues
- [MEDIUM] Line 203: Nested loop with O(n²) complexity
  - Impact: Performance degrades significantly with large connection pools
  - Suggested fix: Use hash map for O(1) connection lookup

### Security Vulnerabilities
- [CRITICAL] Line 267: Buffer overflow in strcpy operation
  - Vulnerability Type: CWE-120 Buffer Copy without Checking Size
  - Attack Scenario: Attacker can provide oversized input to overflow buffer
  - Impact: Remote code execution, memory corruption
  - Remediation: Replace strcpy with strncpy or use safe string functions
  - Reference: OWASP Top 10 - A03:2021 Injection
```

#### 3. Severity Levels

| Severity | Symbol | Definition | Action Required |
|----------|--------|------------|-----------------|
| **Critical** | 🔴 | Security vulnerabilities, data loss risks, system failures | Fix immediately, block merge |
| **High** | 🟠 | Functionality issues, major bugs, high-risk changes | Fix before merge |
| **Medium** | 🟡 | Code quality issues, moderate risks, technical debt | Fix soon, can merge with plan |
| **Low** | 🟢 | Style issues, minor improvements, suggestions | Nice to have, optional |

#### 4. Review Board Summary

The `rb_{id}_review_summary.txt` file contains a concise version perfect for posting to Review Board:

```markdown
## Code Review Summary

**Overall Assessment:** Needs Work

**Issues Found:** 12 (Critical: 1, High: 3, Medium: 5, Low: 3)

**Critical Issues:** [1 found]
- src/connection_pool.c:267 - Buffer overflow in strcpy operation (CWE-120)

**High Priority Issues:** [3 found]
- src/connection_pool.c:145 - Removed null check before pointer dereference
- src/auth_handler.c:89 - SQL injection vulnerability in query construction
- src/memory_manager.c:234 - Memory leak in error path

**Recommendations:**
1. Fix buffer overflow in connection_pool.c using strncpy
2. Restore null check at line 145
3. Use parameterized queries for database access
4. Address memory leak in memory_manager.c error handling
5. Consider adding unit tests for error paths

**Details:** Full report available at: rb_340168_review_report.md
```

**How to use it:**
1. Open `rb_{id}_review_summary.txt`
2. Copy the entire content
3. Go to your Review Board page
4. Paste into a new comment
5. Submit

---

## Examples

### Example 1: Simple Bug Fix Review

**Scenario:** You fixed a null pointer dereference in a utility function

**Steps:**
1. Submit your changes to Review Board (creates RB #340170)
2. Invoke agent: `@code_review_agent review RB 340170`
3. Provide:
   - RB ID: `340170`
   - API Token: `[your token]`
   - Diff version: `1`
   - Remote session: `no`
   - Context: `Fixed null pointer dereference in string utility`

**Agent Output Summary:**
```
✅ Overall Assessment: Approved with Comments

📊 Statistics:
- Files Changed: 1 (src/utils/string_utils.c)
- Lines Added: 3 | Lines Removed: 1
- Issues Found: 2 (Medium: 1, Low: 1)

⚠️ Issues:
- [MEDIUM] Missing test case for the bug fix
- [LOW] Consider using assert for debug builds

💡 Recommendations:
1. Add unit test to verify null pointer handling
2. Add assertion to catch null inputs during development
```

**What you do next:**
- Add a test case
- Update the diff
- Post the agent's summary to Review Board

---

### Example 2: Large Refactoring with Remote Session

**Scenario:** You're refactoring authentication logic across multiple files

**Steps:**
1. Submit changes to Review Board (creates RB #340175)
2. SSH into your development machine with the codebase
3. Invoke agent: `@code_review_agent review RB 340175`
4. Provide:
   - RB ID: `340175`
   - API Token: `[your token]`
   - Diff version: `1`
   - Remote session: `yes`
   - Codebase path: `/local/jsmith/sources/main-workspace`
   - Context: `Refactoring authentication to use OAuth2 instead of custom tokens`

**Agent Output Summary:**
```
✅ Overall Assessment: Approved with Comments

🔍 Analysis Mode: Remote session with full codebase access

📊 Statistics:
- Files Changed: 12
- Lines Added: 456 | Lines Removed: 389
- Issues Found: 18 (High: 2, Medium: 9, Low: 7)

🔎 Deep Analysis Performed:
- Found 23 callers of modified authentication functions
- Verified compatibility across all call sites
- Identified 5 test files requiring updates
- Detected 3 similar patterns in unmodified code that may need updating

🟠 High Priority Issues:
- auth_handler.c:234 - Session expiration not implemented in new flow
- api_endpoints.c:567 - API endpoint still uses old token validation

💡 Recommendations:
1. Implement session expiration in OAuth2 flow
2. Update all API endpoints to use new authentication
3. Update test files to cover OAuth2 scenarios
4. Consider updating similar authentication patterns in: user_mgmt.c, admin_api.c, client_auth.c
5. Add migration guide for existing users
```

**What you do next:**
- Fix the session expiration issue
- Update API endpoints
- Update tests
- Consider the similar patterns identified
- Add migration documentation

---

### Example 3: Security-Focused Review

**Scenario:** Reviewing changes in a security-sensitive module

**Steps:**
1. Submit changes to Review Board (creates RB #340180)
2. Invoke agent: `@code_review_agent review RB 340180`
3. Provide:
   - RB ID: `340180`
   - API Token: `[your token]`
   - Diff version: `1`
   - Remote session: `no` (quick security scan)
   - Context: `Implementing password reset functionality`

**Agent Output Summary:**
```
🛑 Overall Assessment: Needs Work

📊 Statistics:
- Files Changed: 3
- Lines Added: 234 | Lines Removed: 45
- Issues Found: 8 (Critical: 2, High: 3, Medium: 2, Low: 1)

🔴 Critical Security Issues:
1. password_reset.c:89 - Hard-coded encryption key in source code
   - Vulnerability: CWE-321 Use of Hard-coded Credentials
   - Impact: All password reset tokens can be decrypted by anyone with source access
   - Remediation: Move encryption key to secure configuration, use key management service

2. password_reset.c:145 - Insufficient random number generation
   - Vulnerability: CWE-338 Use of Cryptographically Weak PRNG
   - Impact: Password reset tokens are predictable, attackers can guess tokens
   - Remediation: Use cryptographically secure random number generator (urandom, CryptGenRandom)

🟠 High Priority Security Issues:
1. password_reset.c:234 - Password reset token valid indefinitely
2. email_sender.c:78 - Reset URL sent over unencrypted email without HTTPS
3. database_handler.c:156 - SQL query vulnerable to injection

💡 Immediate Actions Required:
1. ❌ BLOCK MERGE - Remove hard-coded encryption key
2. ❌ BLOCK MERGE - Use crypto-secure RNG for tokens
3. Implement token expiration (suggested: 15-30 minutes)
4. Ensure reset URLs use HTTPS
5. Use parameterized queries for database access
```

**What you do next:**
- **Critical:** Fix the hard-coded key immediately
- **Critical:** Switch to secure random generation
- Fix all high-priority security issues
- Re-submit for review
- Consider security testing after fixes

---

### Example 4: 64-bit Architecture Migration Review

**Scenario:** Migrating a module from 32-bit to 64-bit architecture

**Steps:**
1. Submit changes to Review Board (creates RB #340185)
2. Invoke agent: `@code_review_agent review RB 340185`
3. Provide:
   - RB ID: `340185`
   - API Token: `[your token]`
   - Diff version: `1`
   - Remote session: `yes`
   - Codebase path: `/local/dev/sources/rocky-migration`
   - Context: `Migrating mcplib module to 64-bit for Rocky Linux 8.10`

**Agent Output Summary:**
```
⚠️ Overall Assessment: Approved with Comments

📊 Statistics:
- Files Changed: 8
- Lines Added: 287 | Lines Removed: 213
- Issues Found: 15 (High: 1, Medium: 8, Low: 6)

🎯 64-bit Migration Analysis:

✅ Proper Fixes Found:
- Replaced pointer-to-int casts with intptr_t (6 instances)
- Updated printf format specifiers to %zu, %p (23 instances)
- Changed array indices from int to size_t (12 instances)
- Fixed structure alignment issues (3 structures)

🟠 High Priority Issue:
- data_structures.c:145 - Structure still using 'long' instead of fixed-width type
  - Problem: 'long' is 4 bytes on Windows 64-bit, 8 bytes on Linux 64-bit
  - Impact: Binary incompatibility between platforms
  - Fix: Replace with int64_t or int32_t depending on requirement

🟡 Medium Priority Issues:
- Various printf statements still using %d instead of %zu for size_t
- Some hardcoded sizeof() assumptions need verification
- Missing static_assert checks for structure sizes

💡 Recommendations:
1. Replace 'long' with int64_t in data_structures.c
2. Add compile-time checks with _Static_assert for critical structures
3. Run 64-bit compilation test to verify all fixes
4. Consider adding 64-bit specific test cases
```

**What you do next:**
- Fix the 'long' type issue
- Address printf format issues
- Add static assertions
- Compile and test on 64-bit platform

---

## Best Practices

### Before Submitting for Review

1. **Self-Review First**
   - Run the agent on your own changes before submitting to Review Board
   - Fix obvious issues the agent identifies
   - This saves review cycles and demonstrates thoroughness

2. **Provide Context**
   - Always fill in the "Change Context" when invoking the agent
   - Good context example: `"Fixing memory leak in connection pool (Bug #12345) by implementing proper cleanup in error paths"`
   - Poor context example: `"bug fix"`

3. **Choose the Right Mode**
   - For API changes, refactoring, or complex changes: Use **Remote Session Mode**
   - For small bug fixes or isolated changes: **Diff-Only Mode** is sufficient

### During Review

4. **Read the Full Report**
   - Don't just rely on the summary
   - Check the detailed report (`rb_{id}_review_report.md`) for complete analysis
   - Each issue includes "why it matters" and "how to fix it"

5. **Prioritize by Severity**
   - **Critical**: Must fix before merge, no exceptions
   - **High**: Fix before merge unless exceptional circumstances
   - **Medium**: Fix or create follow-up ticket
   - **Low**: Nice to have, optional

6. **Use the Agent Output in Review Board**
   - Copy the Review Board summary to your review comments
   - Link to the full report if you've shared it (internal wiki, etc.)
   - Respond to each issue in Review Board comments

### After Review

7. **Address Feedback Systematically**
   - Create a checklist from the agent's findings
   - Mark each issue as you fix it
   - Re-run the agent on your updated diff to verify fixes

8. **Learn from Patterns**
   - If the agent finds similar issues repeatedly, update your coding habits
   - Share common findings with your team
   - Consider updating coding guidelines based on frequent issues

### For Reviewers

9. **Use as a Starting Point**
   - The agent catches common issues, you focus on business logic
   - Don't skip manual review - the agent enhances, not replaces human review
   - Look for things the agent can't catch: requirements mismatch, user experience, etc.

10. **Provide Additional Context**
    - If the agent missed something important, note why
    - If the agent flagged a false positive, explain why it's actually correct
    - This feedback helps improve the agent

---

## Troubleshooting

### Problem: Authentication Failed (401/403)

**Symptom:**
```
❌ Error: HTTP 401 - Authentication Failed
Unable to download diff from Review Board
```

**Solutions:**
1. **Verify your API token is current**
   - Go to Review Board → Account → API Tokens
   - Check if your token is still active
   - Generate a new token if needed

2. **Check token format**
   - Ensure you copied the entire token
   - No extra spaces at beginning or end
   - No line breaks in the middle

3. **Verify Review Board access**
   - Can you access the review in your browser?
   - Are you logged in to Review Board?

### Problem: Review Board ID Not Found (404)

**Symptom:**
```
❌ Error: HTTP 404 - Review Request Not Found
RB ID 340999 does not exist
```

**Solutions:**
1. **Verify the RB ID**
   - Check the URL: `https://reviewboard.olympus.f5net.com/r/340999/`
   - The number after `/r/` is your RB ID
   - Make sure you entered it correctly

2. **Check if review is published**
   - Draft reviews are not accessible via API
   - Publish your review first, then run the agent

3. **Verify access permissions**
   - Do you have permission to view this review?
   - Is it in a private repository you don't have access to?

### Problem: Diff Download Fails

**Symptom:**
```
❌ Error: Failed to download diff content
Received empty response from server
```

**Solutions:**
1. **Check diff version**
   - Does diff version 1 exist?
   - Try checking in Review Board UI

2. **Manual fallback**
   - Download the diff manually from Review Board
   - Save it as `rb_{id}_diff.patch`
   - Place it in the working directory
   - The agent can analyze the local file

3. **Network issues**
   - Check if you can access Review Board in browser
   - Try from a different network if possible
   - Check with IT if there are firewall issues

### Problem: Codebase Path Not Found (Remote Session Mode)

**Symptom:**
```
❌ Error: Codebase path not found or not accessible
Path: /local/username/sources/workspace
```

**Solutions:**
1. **Verify the path**
   - Run: `ls -la /local/username/sources/workspace`
   - Make sure the path exists

2. **Check permissions**
   - Do you have read access to the directory?
   - Run: `test -r /local/username/sources/workspace && echo "OK"`

3. **Use absolute path**
   - Don't use `~` or relative paths
   - Use full path: `/local/$USER/sources/workspace` (with $USER expanded)

4. **Fall back to diff-only mode**
   - If path issues persist, switch to `Remote session: no`
   - Analysis will be less comprehensive but still valuable

### Problem: Analysis Takes Too Long

**Symptom:**
Agent appears stuck or running for more than 10 minutes

**Solutions:**
1. **Check diff size**
   - Very large diffs (thousands of lines) take longer
   - Consider reviewing in smaller chunks

2. **Remote session overhead**
   - Remote session mode takes longer due to codebase scanning
   - This is normal for large codebases

3. **Be patient**
   - Initial analysis of large diffs can take 5-10 minutes
   - Progress updates appear in console

4. **Restart if truly stuck**
   - If no progress after 15 minutes, interrupt and restart
   - Try diff-only mode first to see if that completes

### Problem: Too Many False Positives

**Symptom:**
Agent reports issues that aren't actually problems

**Solutions:**
1. **Understand the context**
   - The agent doesn't have full business logic context
   - It reports potential issues - you decide if they apply

2. **Provide better change context**
   - More detailed explanation helps the agent understand intent
   - Example: Instead of "refactoring", say "refactoring to consolidate duplicate logic - temporary complexity is intentional"

3. **Check severity levels**
   - Low severity findings are suggestions, not requirements
   - Focus on High and Critical findings

4. **Use report sections selectively**
   - If coding style warnings are too strict, focus on Security and Regression sections
   - Each section is clearly separated in the report

---

## FAQs

### General Questions

**Q: How long does a code review take?**
A: Typically 1-5 minutes depending on:
- Diff size (small: <1 min, large: 5+ min)
- Analysis mode (diff-only: faster, remote session: slower)
- Network speed (for Review Board download)

**Q: Does the agent replace human code reviewers?**
A: No! The agent is a **tool to assist reviewers**, not replace them. It catches common issues automatically, freeing human reviewers to focus on business logic, design decisions, and user experience. Always have human review in addition to the agent.

**Q: Can I use this for any programming language?**
A: The agent supports many languages (C, C++, Python, JavaScript, Shell, Java, Go, etc.) with varying levels of depth. Language-specific analysis depth:
- **Excellent**: C, C++, Python, Shell scripts
- **Good**: JavaScript, Java
- **Basic**: Ruby, Go, Rust, others

**Q: Is my API token secure?**
A: Yes, the agent:
- Never displays your full token (only first/last 4 characters)
- Doesn't store the token permanently
- Uses it only for the current analysis
- Best practice: Generate a dedicated token for the agent, revoke it when not needed

**Q: Can I review changes before they're submitted to Review Board?**
A: Not directly. The agent requires a Review Board ID to function. However, you can:
1. Create a draft review in Review Board
2. Run the agent on the draft
3. Fix issues before publishing the review

### Technical Questions

**Q: What's the difference between diff-only and remote session mode?**
A: 
- **Diff-Only**: Analyzes only what changed in the diff. Faster, works anywhere, but can't check dependencies.
- **Remote Session**: Has access to the complete codebase. Can check callers, verify interfaces, find similar patterns. Slower but much more thorough.

**Q: How do I know if I need remote session mode?**
A: Use remote session if:
- Changing public APIs or interfaces
- Refactoring across multiple files
- Modifying shared data structures
- Need to verify calling code
- Making complex architectural changes

Use diff-only if:
- Small, isolated bug fixes
- Changes to private functions
- Documentation updates
- Simple logic fixes

**Q: Can the agent access my private Review Board instance?**
A: Yes, if you provide the custom URL. Example:
```
Review Board URL: https://mycompany-rb.internal.com
```
Make sure the agent can reach that URL from where it's running.

**Q: Why does the agent miss some issues?**
A: The agent may miss issues if:
- The issue requires business or domain knowledge
- The problem is only apparent with runtime data
- The issue involves complex multi-file interactions (in diff-only mode)
- The problem requires understanding user intentions
- The codebase uses custom libraries/frameworks the agent doesn't know

This is why human review is essential!

**Q: Can I customize what the agent checks for?**
A: Currently, the agent uses built-in rules. However, you can:
- Provide coding guidelines files (it will check against them)
- Give detailed change context to help it focus
- Ignore Low severity findings if they're not relevant
- Request specific types of analysis in your change context

### Workflow Questions

**Q: When should I run the agent in my workflow?**
A: Recommended workflow:
1. **Before submitting**: Run agent on your changes locally (saves time)
2. **After submitting**: Run agent to generate summary for reviewers
3. **After updates**: Re-run agent on updated diffs to verify fixes
4. **Before merging**: Final check to ensure all issues are addressed

**Q: How do I share the agent's findings with my team?**
A: Multiple options:
1. Copy Review Board summary to RB comments (most common)
2. Attach full report to Review Board review
3. Share reports on internal wiki/confluence
4. Include key findings in commit messages
5. Discuss in team meetings for complex issues

**Q: Should I fix all issues the agent finds?**
A: Not necessarily:
- **Critical & High**: Yes, fix these before merging
- **Medium**: Fix or create follow-up tickets
- **Low**: Optional, use your judgment
- **False positives**: Document why they're false positives in your response

**Q: Can I run the agent multiple times on the same review?**
A: Yes! Common scenarios:
- Run on diff version 1, fix issues, update to diff version 2, run again
- Run in diff-only mode first (quick check), then remote session mode (thorough check)
- Run again after addressing feedback to verify fixes

### Error and Issue Questions

**Q: What should I do if the agent reports a false positive?**
A: 
1. Verify it's truly a false positive (not a real issue you missed)
2. Document why it's not an issue in your Review Board response
3. Explain the context that the agent couldn't know
4. Continue with the review process
5. Consider if the code could be clearer to avoid confusion

**Q: The agent found a security vulnerability - what do I do?**
A: 
1. **Critical vulnerabilities**: Fix immediately, do not merge
2. Verify the finding (is it a real vulnerability?)
3. Fix the issue following the agent's remediation guidance
4. If needed, consult your security team
5. Add test cases to prevent regression
6. Consider if similar issues exist elsewhere in the codebase

**Q: The agent analysis failed - how do I recover?**
A:
1. Check the error message for specific details
2. Verify your inputs (RB ID, token, etc.)
3. Try the fallback: download diff manually and analyze locally
4. Try diff-only mode if remote session mode fails
5. Review the troubleshooting section above
6. If all else fails, perform manual review and report the issue

---

## Quick Reference Card

### Invocation Commands
```
@code_review_agent review RB {id}
@code_review_agent review RB {id} diff version {version}
Review code changes from Review Board {id} with diff version {version}
```

### Required Information Checklist
- [ ] Review Board ID
- [ ] API Token
- [ ] Diff version (or use default 1)
- [ ] Change context description

### Common File Patterns
```
Input: RB ID, API Token, parameters
Output: 
  - rb_{id}_review_report.md (detailed)
  - rb_{id}_review_summary.txt (for Review Board)
  - rb_{id}_diff.patch (downloaded diff)
```

### Analysis Categories
1. 🔄 Regression Risk Detection
2. ⚡ Performance Analysis
3. 🏗️ Architectural Review
4. 🔐 Security Vulnerability Scanning
5. 📋 Coding Guideline Compliance

### Severity Guide
- 🔴 **Critical**: Block merge, fix immediately
- 🟠 **High**: Fix before merge
- 🟡 **Medium**: Fix or create ticket
- 🟢 **Low**: Optional improvement

### Mode Selection
- **Diff-Only**: Fast, works anywhere, limited context
- **Remote Session**: Slow, requires codebase access, comprehensive

---

## Support and Feedback

### Getting Help
- Check this manual first (especially Troubleshooting and FAQs)
- Consult with your team lead or code review champion
- Review example scenarios that match your use case

### Reporting Issues
If you encounter bugs or unexpected behavior:
1. Note the RB ID that caused the issue
2. Save the error message and console output
3. Document what you expected vs. what happened
4. Share with the agent maintainer team

### Feature Requests
Have ideas for improvement? Consider:
- What additional checks would be valuable?
- What languages need better support?
- What workflow improvements would help?
- Share feedback with the development team

---

## Conclusion

The Code Review Agent is a powerful tool to enhance your code review process. It helps catch common issues automatically, allowing human reviewers to focus on higher-level concerns like architecture, business logic, and user experience.

**Remember:**
- ✅ Run the agent early and often
- 🤝 Use it to assist, not replace, human review
- 📚 Learn from the patterns it identifies
- 🔄 Iterate: fix issues, re-run, verify
- 🎯 Focus on Critical and High severity issues first

**Happy reviewing! 🚀**

---

*Last Updated: March 2026*
*Version: 1.0*
