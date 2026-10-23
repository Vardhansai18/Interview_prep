# TMOS AI-Agent Framework
## Accelerating Development with Intelligent Automation

---

## Slide 1: Title Slide
**TMOS AI-Agent Framework**  
**Intelligent Automation for TMOS Development**

_Presented by: TMOS AI Team_  
_Date: March 18, 2026_

---

## Slide 2: Agenda

1. **Need for Generic AI-Agent Framework**
2. **Framework Architecture & Directory Structure**
3. **Creating New Projects with ai-template-create.sh**
4. **Currently Supported Agents**
5. **Agent Workflows & Capabilities**
6. **Best Practices & Future Roadmap**

---

## Slide 3: The Challenge - Why AI-Agent Framework?

### **Current TMOS Development Pain Points:**

❌ **Manual Migration Efforts**
- CentOS to Rocky Linux migration across 1000+ modules
- 32-bit to 64-bit architecture transitions
- GCC version upgrades, OpenSSL migrations

❌ **Time-Consuming Code Reviews**
- Manual review of large codebases
- Inconsistent review standards
- Limited bandwidth for thorough analysis

❌ **Repetitive Tasks**
- Similar code changes across multiple modules
- Documentation updates
- Build configuration modifications

---

## Slide 4: The Solution - Generic AI-Agent Framework

### **What is the TMOS AI-Agent Framework?**

✅ **Intelligent Automation System**
- AI-powered agents that understand TMOS architecture
- Autonomous execution of complex, multi-step tasks
- Consistent application of best practices

✅ **Scalability**
- Reusable across multiple projects
- Extensible through skills and instructions
- Supports hierarchical agent structures (main agents + subagents)

✅ **Productivity Boost**
- Automate repetitive tasks
- Reduce human error
- Accelerate migration timelines

---

## Slide 5: Framework Benefits

### **Key Advantages:**

📈 **Efficiency**
- 10x faster than manual migration
- Parallel processing capabilities
- 24/7 autonomous operation

🎯 **Consistency**
- Standardized approach across all modules
- Knowledge base (skills) ensures best practices
- Automated compliance checks

📊 **Traceability**
- Comprehensive logs for every action
- Detailed reports with rationales
- Version control integration

🔄 **Reusability**
- Project templates for quick setup
- Common skills shared across projects
- Proven patterns and workflows

---

## Slide 6: Framework Architecture

### **Three-Tier Structure:**

```
ai-agents/
├── common/                 # Shared resources
│   ├── agents/            # Reusable agents
│   ├── skills/            # Domain knowledge base
│   ├── instructions/      # Global guidelines
│   └── ...
├── projects/              # Project-specific implementations
│   ├── centos2rocky/     # Rocky Linux migration
│   ├── codereview/       # Code review automation
│   └── ...
└── ai-template-create.sh  # Project scaffolding tool
```

**Design Principles:**
- **Common**: Shared knowledge and reusable components
- **Projects**: Specific implementations and workflows
- **Separation**: Clear boundaries between global and project-specific

---

## Slide 7: Directory Structure - Common

### **Common Resources (Shared Across All Projects)**

```
ai-agents/common/
├── agents/              # Generic, reusable agents
├── subagents/           # Shared subagents
├── skills/              # Universal domain knowledge
│   ├── coding-guidelines.SKILL.md
│   ├── git-commands.SKILL.md
│   ├── perforce-commands.SKILL.md
│   └── tmos-compilation.SKILL.md
├── instructions/        # Global operating principles
│   └── general.instructions.md
├── input/               # Shared input files
├── output/              # Common outputs
└── logs/                # Shared execution logs
```

**Purpose:** Centralized knowledge base accessible to all projects

---

## Slide 8: Directory Structure - Projects

### **Project-Specific Structure**

```
ai-agents/projects/<project_name>/
├── agents/              # Main orchestrator agents
├── subagents/           # Specialized subagents
├── skills/              # Project-specific knowledge
├── instructions/        # Project-specific guidelines
├── input/               # Input data and configurations
│   └── 32bit-modules.txt
├── output/              # Generated reports and artifacts
├── logs/                # Execution logs and traces
└── README.md            # Project documentation
```

**Each project is self-contained with all necessary resources**

---

## Slide 9: What is a "Skill"?

### **Skills = Domain Knowledge Base**

**Definition:** Markdown files containing comprehensive guidance on specific domains

**Purpose:**
- Provide agents with expert-level knowledge
- Ensure consistent application of best practices
- Serve as reference during autonomous operations

**Examples:**
- `coding-guidelines.SKILL.md` - TMOS coding standards
- `perforce-commands.SKILL.md` - Version control workflows
- `tmos-compilation.SKILL.md` - Build system expertise
- `32bit-to-64bit-migration.SKILL.md` - Architecture migration guide

**Format:** Structured markdown with sections for patterns, examples, pitfalls, and checklists

---

## Slide 10: What is an "Instruction"?

### **Instructions = Operating Guidelines**

**Definition:** Files containing mandatory operational principles and constraints

**Purpose:**
- Define how agents should behave
- Set boundaries and safety constraints
- Ensure compliance with policies

**Example: general.instructions.md**
- No hallucination policy
- Permission protocols
- File management rules
- Logging requirements
- Self-improvement mechanisms

**Key Difference from Skills:**
- Skills = "What to do" (domain knowledge)
- Instructions = "How to behave" (operational rules)

---

## Slide 11: Creating New Projects - ai-template-create.sh

### **Automated Project Scaffolding**

**Usage:**
```bash
cd /path/to/tmos-rocky-ws2/ai-agents
./ai-template-create.sh <project_name>
```

**What It Does:**
1. Creates complete directory structure
2. Generates README.md with metadata
3. Sets up all required subdirectories
4. Provides usage guidelines

**Special Case:**
```bash
./ai-template-create.sh common  # Creates in current directory
./ai-template-create.sh myproject  # Creates in projects/ directory
```

**Output:**
```
projects/myproject/
├── agents/
├── subagents/
├── skills/
├── instructions/
├── input/
├── output/
├── logs/
└── README.md [auto-generated]
```

---

## Slide 12: ai-template-create.sh - Features

### **Key Features:**

✅ **Intelligent Path Logic**
- `common` → Created at root level
- Other names → Created in `projects/` directory

✅ **Complete Structure**
- All 7 required subdirectories
- README with documentation template
- Metadata (creator, date, path)

✅ **Color-Coded Output**
- Success messages in green
- Errors in red
- Info in yellow

✅ **Usage Guidelines**
- Best practices included in README
- Directory purpose documentation
- Project-specific customization guide

---

## Slide 13: Currently Supported Agents - Overview

### **Production Agents:**

| Agent | Project | Purpose | Status |
|-------|---------|---------|--------|
| **tmos_rocky_migrator** | centos2rocky | Rocky Linux 8.10 migration | ✅ Active |
| **tmos_rocky_64bit_migrator** | centos2rocky | 32-bit to 64-bit migration | ✅ Active |
| **code_review_agent** | codereview | Automated code review | ✅ Active |

### **Agent Types:**

🎯 **Main Agents (Orchestrators)**
- High-level task coordination
- User-facing interfaces
- Complex workflow management

⚙️ **Subagents (Specialists)**
- Focused, specialized tasks
- Called by main agents
- Autonomous execution

---

## Slide 14: Agent #1 - tmos_rocky_migrator

### **Rocky Linux 8.10 Migration Agent**

**Purpose:** Migrate TMOS modules from CentOS 6/7 to Rocky Linux 8.10

**Key Capabilities:**
- ✅ GCC 4.8.5 → GCC 11.2.x migration
- ✅ OpenSSL 1.0.x → 1.1.1k migration  
- ✅ Java JDK 1.8 → JDK 21 migration
- ✅ Python 2 → Python 3 migration
- ✅ Perl 5.16 → Perl 5.26+ migration
- ✅ Automatic 64-bit subagent invocation
- ✅ Spec file updates for GCC toolchain
- ✅ Build and validation

**Location:** `projects/centos2rocky/agents/tmos_rocky_migrator.agent.md`

---

## Slide 15: tmos_rocky_migrator - Workflow

### **Migration Workflow:**

```
1. Validate Input
   └─> Check module name, workspace path
   
2. Check 64-bit Requirement
   └─> Read 32bit-modules.txt
   └─> Invoke tmos_rocky_64bit_migrator if needed ← AUTOMATIC
   
3. Update Spec Files
   └─> Add GCC 11 toolchain configuration
   └─> Add gcc_toolset_enable directives
   
4. Analyze & Fix Code
   └─> Scan for deprecated features
   └─> Apply migration patterns from skills
   
5. Build & Validate
   └─> Compile with Rocky Linux GCC 11
   └─> Fix warnings and errors iteratively
   
6. Generate Reports
   └─> Comprehensive migration report
   └─> Build logs
   └─> Files modified with rationale
```

---

## Slide 16: tmos_rocky_migrator - Technology Stack

### **Handles Multiple Technology Migrations:**

| Technology | From | To | Skill Reference |
|------------|------|-----|----------------|
| **GCC** | 4.8.5 | 11.2.x | gcc-migration-11 |
| **OpenSSL** | 1.0.x | 1.1.1k | openssl-migration |
| **Java** | JDK 1.8 | JDK 21 | java-migration-jdk21 |
| **Python** | 2.x | 3.x | python-migration |
| **Perl** | 5.16 | 5.26+ | perl-migration-rocky |
| **Architecture** | 32-bit | 64-bit | 32bit-to-64bit-migration |

**Each migration domain has dedicated SKILL file with:**
- Critical breaking changes
- Migration patterns
- Code examples
- Best practices
- Common pitfalls

---

## Slide 17: Agent #2 - tmos_rocky_64bit_migrator

### **32-bit to 64-bit Architecture Migration Subagent**

**Purpose:** Migrate TMOS modules from 32-bit (i686) to 64-bit (x86_64)

**Key Capabilities:**
- ✅ Module definition updates (arch=x86_64)
- ✅ Makefile flag analysis (-m32 → -m64)
- ✅ Data type migration (int → size_t, intptr_t)
- ✅ Pointer arithmetic fixes
- ✅ GCC static analysis (gcc -fsyntax-only -m64)
- ✅ **Automatic issue fixing** (not just reporting)
- ✅ Re-verification until clean (zero warnings/errors)
- ✅ Comprehensive 64-bit compatibility report

**Invoked by:** tmos_rocky_migrator (when module in 32bit-modules.txt)

**Location:** `projects/centos2rocky/subagents/tmos_rocky_64bit_migrator.agent.md`

---

## Slide 18: tmos_rocky_64bit_migrator - Workflow

### **64-bit Migration Workflow:**

```
1. Update Module Definition
   └─> Add context: arch=x86_64 to *.inc file
   
2. Analyze Build Files
   └─> Check Makefile for -m32 flags
   └─> Update paths (lib → lib64, devfs variables)
   └─> Update spec files (%{_libdir})
   
3. Static Analysis (gcc -fsyntax-only -m64)
   └─> Analyze ALL source files in parallel
   └─> Generate warnings report by category
   
4. FIX All Issues ← NEW: Agent fixes, not just reports
   └─> size_t conversions (unsigned int → size_t)
   └─> Pointer storage (int → intptr_t)
   └─> Sign conversions (int → uint32_t)
   └─> Format specifiers (%d → %zu, %p)
   
5. Re-verify Fixes
   └─> Re-run static analysis
   └─> Ensure ZERO warnings, ZERO errors
   └─> Iterate until clean
   
6. Generate Report
   └─> Before/after metrics
   └─> All fixes documented
   └─> Verification status
```

---

## Slide 19: tmos_rocky_64bit_migrator - Fix Strategies

### **Intelligent Fix Application:**

**Size Conversion Issues:**
```c
// Before (32-bit style)
unsigned int len = strlen(str);  // ⚠️ size_t → unsigned int

// After (64-bit compatible)
size_t len = strlen(str);  // ✅ Correct type
```

**Pointer Storage:**
```c
// Before
int ptr_value = (int)pointer_address;  // ⚠️ Truncates on 64-bit

// After
intptr_t ptr_value = (intptr_t)pointer_address;  // ✅ Safe
```

**Network Byte Order:**
```c
// Before
int value = ntohl(*((int*)buffer));  // ⚠️ Sign conversion

// After
uint32_t value = ntohl(*((uint32_t*)buffer));  // ✅ Correct
```

---

## Slide 20: Agent #3 - code_review_agent

### **Automated Code Review Agent**

**Purpose:** Perform comprehensive code reviews following TMOS standards

**Key Capabilities:**
- ✅ Style and formatting checks
- ✅ Best practices validation
- ✅ Security vulnerability detection
- ✅ Performance anti-pattern identification
- ✅ Documentation completeness
- ✅ Adherence to coding guidelines
- ✅ Automated feedback generation

**Use Cases:**
- Pre-commit reviews
- Perforce changelist validation
- Legacy code quality assessment

**Location:** `projects/codereview/agents/code_review_agent.agent.md`

---

## Slide 21: Logging & Reporting Standards

### **All Agents Follow Consistent Patterns:**

**Logging Requirements:**
```
Location: ai-agents/projects/<project>/logs/<agent>_<module>.log
Format:   All commands, outputs, and errors
Naming:   <agent_name>_<module_name>.log
```

**Report Requirements:**
```
Location: ai-agents/projects/<project>/output/<agent>_<module>_report.md
Format:   Comprehensive markdown with sections:
          - Executive Summary
          - Files Modified
          - Changes by Category
          - Validation Status
          - Next Steps
Naming:   <agent_name>_<module_name>_report.md
```

**Benefits:**
- Audit trail for all operations
- Reproducible workflows
- Easy troubleshooting
- Knowledge transfer

---

## Slide 22: Agent Communication Model

### **Hierarchical Agent Structure:**

```
┌─────────────────────────────┐
│  User / Main Agent          │
│  (tmos_rocky_migrator)      │
└──────────────┬──────────────┘
               │ Invokes
               ▼
┌─────────────────────────────┐
│  Subagent                   │
│  (tmos_rocky_64bit_migrator)│
└──────────────┬──────────────┘
               │ Returns report
               ▼
┌─────────────────────────────┐
│  Main Agent                 │
│  (Continues workflow)       │
└─────────────────────────────┘
```

**Communication:**
- Main agent passes context and module name
- Subagent operates autonomously
- Returns structured report
- Main agent incorporates results
- No user interaction required for subagents

---

## Slide 23: Skills System Deep Dive

### **Current Common Skills:**

| Skill File | Purpose | Usage |
|------------|---------|-------|
| **coding-guidelines.SKILL.md** | TMOS coding standards | All agents |
| **git-commands.SKILL.md** | Git workflow reference | Version control |
| **perforce-commands.SKILL.md** | P4 operations guide | File checkout/submit |
| **tmos-compilation.SKILL.md** | Build system knowledge | Compilation tasks |

**Project-Specific Skills (centos2rocky):**
- `32bit-to-64bit-migration.SKILL.md` - Architecture migration patterns
- `gcc-migration-11.SKILL.md` - GCC version upgrade guidance
- `openssl-migration.SKILL.md` - OpenSSL API changes

**Skill Structure:**
- Overview & Concepts
- Critical Breaking Changes
- Migration Patterns
- Code Examples
- Best Practices
- Common Pitfalls
- Checklist

---

## Slide 24: Instructions System Deep Dive

### **general.instructions.md - Core Principles:**

**26 Mandatory Operating Principles:**

1. **No Hallucination** - Facts only, no guessing
2. **Acknowledge Gaps** - Request clarification when unsure
3. **Clear Communication** - Assume no prior knowledge
4. **User-Paced** - Don't rush decisions
5. **Explicit Permission** - Before any modifications
6. **Output Redirection** - To project-specific locations
7. **File Cleanup** - Remove intermediates, keep reports
8-26. **Additional constraints** on makefiles, compiler flags, file operations, etc.

**Special Instructions:**
- File location standards (logs/, output/)
- Report generation requirements
- Logging format specifications
- Workspace validation

---

## Slide 25: Real-World Example - tamdlib Migration

### **Case Study: Rocky Linux Migration of tamdlib Module**

**Challenge:**
- Migrate tamdlib from CentOS 6 to Rocky Linux 8.10
- Module listed in 32bit-modules.txt (32-bit → 64-bit required)
- GCC 4.8 → GCC 11 compatibility

**Solution - Automated Workflow:**

1. **Agent Invocation:**
   ```
   @tmos_rocky_migrator Migrate tamdlib to Rocky Linux
   ```

2. **Automatic 64-bit Check:**
   - Detected in 32bit-modules.txt
   - Invoked tmos_rocky_64bit_migrator subagent

3. **64-bit Migration:**
   - Updated ltm.def.inc (context: arch=x86_64)
   - Static analysis: Found 17 warnings
   - Fixed all size_t conversion issues
   - Re-verified: CLEAN (0 warnings, 0 errors)

4. **Rocky Linux Migration:**
   - Updated tamdlib.spec for GCC 11
   - Fixed uninitialized variable warning
   - Built successfully

**Results:**
- ✅ 2 files modified
- ✅ Zero errors, zero warnings
- ✅ 17 64-bit issues resolved
- ✅ Comprehensive reports generated
- ✅ Ready for Perforce submission

---

## Slide 26: Performance Metrics

### **Efficiency Gains:**

| Metric | Manual | AI-Agent | Improvement |
|--------|--------|----------|-------------|
| **Time per Module** | 4-8 hours | 20-30 mins | **10-15x faster** |
| **Error Rate** | 5-10% | <1% | **10x reduction** |
| **Consistency** | Variable | 100% | **Perfect** |
| **Documentation** | Often missing | Always complete | **100% coverage** |

**Additional Benefits:**
- 24/7 operation capability
- Parallel processing of multiple modules
- Instant knowledge application (skills)
- Reproducible outcomes
- Continuous learning and improvement

**Cost Savings:**
- Reduced engineering time
- Faster time-to-market
- Lower defect rates
- Better resource allocation

---

## Slide 27: Best Practices

### **Developing New Agents:**

✅ **Do:**
- Use ai-template-create.sh for project setup
- Create comprehensive SKILL files for domain knowledge
- Follow logging and reporting standards
- Test thoroughly with sample modules
- Document workflow in agent metadata
- Use subagents for specialized tasks
- Implement error handling and validation
- Generate detailed reports

❌ **Don't:**
- Hardcode paths or module names
- Skip permission checks (from instructions)
- Ignore general.instructions.md requirements
- Make assumptions without documentation
- Proceed without user confirmation (for main agents)
- Mix concerns (keep agents focused)
- Forget to log actions

---

## Slide 28: Quality Assurance

### **Agent Validation Process:**

**Before Deployment:**
1. **Unit Testing** - Test individual components
2. **Integration Testing** - Test full workflows
3. **Dry Run** - Test on non-critical modules
4. **Review** - Peer review of agent logic
5. **Documentation** - Complete README and metadata

**During Operation:**
1. **Logging** - Comprehensive execution logs
2. **Validation** - Verify all changes compile
3. **Reporting** - Detailed change documentation
4. **Error Handling** - Graceful failure with clear messages

**After Execution:**
1. **Verification** - Manual spot-check of changes
2. **Build Testing** - Ensure compilation success
3. **Regression Testing** - Verify no functionality broken
4. **Feedback Loop** - Update skills/instructions based on learnings

---

## Slide 29: Security & Safety

### **Built-in Safety Mechanisms:**

🔒 **Permission Controls:**
- Explicit user confirmation required (main agents)
- Subagents operate with pre-authorized scope
- No access to production systems without approval

🔒 **Change Tracking:**
- All modifications logged
- Perforce integration for version control
- Rollback capability via p4 revert

🔒 **Validation:**
- Static analysis before changes
- Compilation verification after changes
- Re-analysis to confirm fixes

🔒 **Constraints:**
- Cannot modify critical system files
- Cannot delete files without permission
- Cannot bypass build system rules
- Cannot ignore coding guidelines

---

## Slide 30: Future Roadmap

### **Planned Enhancements:**

**Q2 2026:**
- 🎯 Additional migration agents (Ubuntu, Debian)
- 🎯 Performance optimization agent
- 🎯 Documentation generation agent
- 🎯 Test case generation agent

**Q3 2026:**
- 🎯 Multi-module batch processing
- 🎯 Intelligent dependency resolution
- 🎯 Automated regression test selection
- 🎯 CI/CD pipeline integration

**Q4 2026:**
- 🎯 Machine learning model training on TMOS patterns
- 🎯 Predictive issue detection
- 🎯 Auto-optimization of code patterns
- 🎯 Natural language interface for agent invocation

---

## Slide 31: Getting Started

### **How to Use the Framework:**

**For New Projects:**
```bash
cd /path/to/tmos-workspace/ai-agents
./ai-template-create.sh my_new_project
cd projects/my_new_project
# Create your agents, skills, and instructions
```

**For Existing Agents:**
```bash
# Rocky Linux migration
@tmos_rocky_migrator Migrate <module> to Rocky Linux

# Code review
@code_review_agent Review changelist <CL_number>
```

**Resources:**
- Documentation: `ai-agents/README.md`
- Common skills: `ai-agents/common/skills/`
- Examples: Existing projects in `ai-agents/projects/`
- Support: TMOS AI Team

---

## Slide 32: Success Stories

### **Modules Migrated to Date:**

✅ **tamdlib** - Rocky Linux 8.10 + 64-bit migration  
✅ **fflag** - GCC 11 compatibility fixes  
✅ **f5-cpp-json** - Complete migration  
✅ **[Additional modules...]**

**Key Achievements:**
- 🏆 100% success rate in automated migrations
- 🏆 Zero critical bugs introduced
- 🏆 Comprehensive documentation for all changes
- 🏆 Significant time savings per module
- 🏆 Consistent application of best practices

**Testimonials:**
_"The AI agent completed in 30 minutes what would have taken me 2 days manually, and with better consistency."_  
— Development Team Member

---

## Slide 33: Lessons Learned

### **Key Insights from Deployment:**

**What Worked Well:**
✅ Hierarchical agent structure (main + subagents)  
✅ Skills system for domain knowledge  
✅ Automated logging and reporting  
✅ Static analysis before modifications  
✅ Re-verification loops until clean

**Challenges Addressed:**
⚠️ Initial versions didn't fix issues (just reported)  
   → Solution: Enhanced subagents to apply fixes

⚠️ Logs scattered in /tmp directories  
   → Solution: Enforced project-specific log locations

⚠️ Inconsistent report formats  
   → Solution: Standardized templates

⚠️ Silent failures  
   → Solution: Comprehensive error handling

---

## Slide 34: Contributing to the Framework

### **How to Contribute:**

**Adding New Skills:**
1. Create `<domain>.SKILL.md` in appropriate skills/ directory
2. Follow skill template structure
3. Include examples and pitfalls
4. Document in project README

**Creating New Agents:**
1. Use `ai-template-create.sh` for project structure
2. Define agent metadata (name, description, tools, etc.)
3. Document workflow in agent file
4. Create corresponding skills and instructions
5. Test thoroughly before deployment

**Improving Existing Agents:**
1. Review execution logs for patterns
2. Update skills with new learnings
3. Add to instructions if policy changes needed
4. Version control all changes

---

## Slide 35: Q&A - Common Questions

**Q: Can agents modify production code?**  
A: Only with explicit permission. Main agents require user confirmation. Subagents operate within pre-authorized scope.

**Q: What if an agent makes a mistake?**  
A: All changes are tracked via Perforce. Use `p4 revert` to rollback. Comprehensive logs enable root cause analysis.

**Q: How do I create a new migration agent?**  
A: Use `ai-template-create.sh`, study existing agents (tmos_rocky_migrator), create relevant skills, follow standards.

**Q: Can agents work with other version control systems?**  
A: Currently optimized for Perforce. Git support available through git-commands.SKILL.md. Extensions possible.

**Q: How is agent performance measured?**  
A: Metrics include: time per module, error rate, consistency score, coverage percentage. Logs provide detailed traces.

---

## Slide 36: Resources & Documentation

### **Key Documentation:**

📚 **Framework Documentation:**
- `ai-agents/README.md` - Framework overview
- `ai-agents/common/instructions/general.instructions.md` - Core principles
- Project-specific READMEs - Project details

📚 **Skills Library:**
- `ai-agents/common/skills/` - Global skills
- `ai-agents/projects/*/skills/` - Project skills

📚 **Examples:**
- `ai-agents/projects/centos2rocky/` - Complete migration project
- `ai-agents/projects/codereview/` - Code review automation

📚 **Support:**
- TMOS AI Team - Internal support channel
- Wiki - Detailed guides and tutorials
- Training Sessions - Hands-on workshops

---

## Slide 37: Summary - Key Takeaways

### **TMOS AI-Agent Framework Benefits:**

✅ **Productivity** - 10-15x faster than manual processes  
✅ **Quality** - Consistent application of best practices  
✅ **Scalability** - Reusable across multiple projects  
✅ **Traceability** - Comprehensive logging and reporting  
✅ **Safety** - Built-in validation and rollback  
✅ **Extensibility** - Easy to add new agents and skills

**Current Capabilities:**
- Rocky Linux 8.10 migration (GCC 11, OpenSSL, Java, Python, Perl)
- 32-bit to 64-bit architecture migration
- Automated code review

**Proven Results:**
- Multiple modules successfully migrated
- Zero critical bugs introduced
- Significant time and cost savings

---

## Slide 38: Call to Action

### **Get Started Today!**

**Step 1:** Explore the framework
```bash
cd tmos-workspace/ai-agents
ls -R
```

**Step 2:** Try an existing agent
```bash
@tmos_rocky_migrator Migrate <your_module> to Rocky Linux
```

**Step 3:** Create your own project
```bash
./ai-template-create.sh my_automation_project
```

**Step 4:** Join the AI-Agent Community
- Contribute skills and improvements
- Share success stories
- Help expand capabilities

**Together, we're automating TMOS development! 🚀**

---

## Slide 39: Thank You

### **Questions?**

**Contact:**
- TMOS AI Team
- Email: [team-email]
- Slack: #tmos-ai-agents

**Learn More:**
- Repository: `tmos-workspace/ai-agents/`
- Wiki: [internal-wiki-link]
- Documentation: `ai-agents/README.md`

**Let's accelerate TMOS development with intelligent automation!**

---

## Slide 40: Appendix - Technical Details

### **Agent File Format (.agent.md):**

```yaml
---
name: agent_name
description: Brief description
argument-hint: Usage hint
model: "Claude Sonnet 4.5"
tools: [execute, read, edit, search, web, agent, todo]
allowedSubagents: [subagent1, subagent2]
---

# Agent instructions in markdown
...
```

### **Skill File Format (.SKILL.md):**

```markdown
# Skill Name

## Overview
...

## Critical Changes
...

## Migration Patterns
...

## Best Practices
...
```

**File Naming Conventions:**
- Agents: `<name>.agent.md`
- Skills: `<domain>.SKILL.md`
- Instructions: `<type>.instructions.md`
- Logs: `<agent>_<module>.log`
- Reports: `<agent>_<module>_report.md`

---

_End of Presentation_
