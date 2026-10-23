# 📁 codereview

## Description

The **Code Review Agent** is an automated code review tool that downloads diffs from Review Board and performs comprehensive analysis of code changes. It identifies potential issues across multiple dimensions including regression risks, performance concerns, architectural problems, security vulnerabilities, and coding guideline violations. It generates structured Markdown reports with every issue traceable to a specific file, function, and line number.

For full usage details, see [USER_MANUAL.md](USER_MANUAL.md).

## 📋 Folder Structure

```
codereview/
├── agents/                          # Main AI agent: code_review_agent.agent.md
├── subagents/                       # (reserved for future subagents)
├── skills/                          # (reserved for domain knowledge skill files)
├── instructions/                    # (reserved for project-specific instruction files)
├── input/                           # Input files and resources used by the agent
├── output/                          # Final review reports (review_{rb_id}_report.md)
├── logs/                            # Temp files, diffs, metadata, analysis logs
├── scripts/                         # Scripts needed by agents/subagents
├── USER_MANUAL.md                   # Detailed usage guide
└── README.md                        # This file
```

## 📂 Directory Details

| Directory       | Purpose                                                                                       |
|-----------------|-----------------------------------------------------------------------------------------------|
| `agents/`       | Main agent file: `code_review_agent.agent.md`                                                 |
| `subagents/`    | Reserved for subagents called from the main agent                                             |
| `skills/`       | Reserved for project-specific `*.SKILL.md` domain knowledge files                             |
| `instructions/` | Reserved for project-specific `*.instructions.md` files                                       |
| `input/`        | Source/input files used by the agent                                                          |
| `output/`       | **Final reports only** — `review_{rb_id}_report.md` and `review_{rb_id}_summary.txt`          |
| `logs/`         | **Temp/intermediate files** — downloaded diffs, metadata JSON, analysis logs                  |
| `scripts/`      | Store scripts that are used by agents/subagents                                               |

## 🤖 Agent: `code_review_agent`

| Field            | Value                                                                                                   |
|------------------|---------------------------------------------------------------------------------------------------------|
| **Agent File**   | `agents/code_review_agent.agent.md`                                                                     |
| **Model**        | Claude Sonnet 4.6                                                                                       |
| **Invocation**   | `Review code changes from Review Board <RB-ID> with diff version <diff-version> using API token <token>`|
| **Review Board** | `https://reviewboard.olympus.f5net.com`                                                                 |

### What It Does

1. Downloads review metadata and the raw diff patch from Review Board via its REST API
2. Parses all changed files, functions, and line numbers from the diff
3. Analyzes changes across five dimensions: Regression, Performance, Architecture, Security, Coding Guidelines
4. Produces a detailed Markdown report and a concise Review Board summary

### Key Capabilities

- **Multi-language analysis** — C/C++, Python, Shell, Java, JavaScript/TypeScript, Makefile, YAML, RPM Spec
- **64-bit migration checks** — detects type truncation, format specifier mismatches, alignment unsafe casts
- **Security scanning** — buffer overflows, unchecked API returns, format string vulnerabilities
- **Severity classification** — Critical / High / Medium / Low with mandatory File + Function + Line attribution
- **Traceable issues** — every issue links to the exact file path, function name, and line number in the diff

### Output Files

| File Pattern                             | Location  | Description                                         |
|------------------------------------------|-----------|-----------------------------------------------------|
| `review_{rb_id}_report.md`               | `output/` | Full structured review with all categorized issues  |
| `review_{rb_id}_summary.txt`             | `output/` | Condensed summary for posting to Review Board       |
| `review_{rb_id}_diff.patch`              | `logs/`   | Downloaded raw diff patch                           |
| `review_{rb_id}_metadata.json`           | `logs/`   | Downloaded RB metadata (description, submitter, etc)|
| `review_{rb_id}_analysis.log`            | `logs/`   | Intermediate analysis notes                         |

### Critical Folder Rules (enforced in agent)

- `logs/` — ALL temporary and intermediate files go here; **never `/tmp/`**
- `output/` — ONLY final reports (`review_{rb_id}_report.md` and `review_{rb_id}_summary.txt`)
- No files may be written outside these two folders

## 📝 Quick Start

```
Review code changes from Review Board 340482 with diff version 1 using API token <your-token>
```

The agent will:
1. Save the diff to `logs/review_340482_diff.patch`
2. Save metadata to `logs/review_340482_metadata.json`
3. Write intermediate analysis to `logs/review_340482_analysis.log`
4. Write the final report to `output/review_340482_report.md`
5. Write the RB-ready summary to `output/review_340482_summary.txt`

## ℹ️ Metadata

| Field        | Value                        |
|--------------|------------------------------|
| Folder Name  | codereview                   |
| Full Path    | `./projects/codereview`      |
| Created By   | kramasubramanian             |
| Created On   | 2026-03-17 22:52:40          |
| Generated By | ai-template-create.sh        |
| Last Updated | 2026-03-20                   |
