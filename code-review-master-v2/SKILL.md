---
name: code-review-master-v2
description: Expert multi-agent code review system with parallel analysis. Spawns 4 specialized agents (Security, Performance, Architecture, Best Practices) for comprehensive review. Generates detailed Markdown reports with inline comments. Use when reviewing PRs, code changes, or conducting thorough code audits. Triggers on "code review", "review this", "PR review", "audit code", "코드 리뷰", "리뷰해줘".
---

# Code Review Master V2

Multi-agent expert code review system with parallel analysis across 4 domains.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    REVIEW ORCHESTRATOR                          │
├─────────────────────────────────────────────────────────────────┤
│ Phase 1: Context ──► Analyze diff, identify scope               │
│ Phase 2: Parallel Review ──► 4 specialized agents               │
│   ├── Security Agent (OWASP, vulnerabilities)                   │
│   ├── Performance Agent (complexity, bottlenecks)               │
│   ├── Architecture Agent (SOLID, patterns, design)              │
│   └── Best Practices Agent (style, maintainability)             │
│ Phase 3: Synthesis ──► Merge findings, prioritize               │
│ Phase 4: Output ──► Report + inline comments                    │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Review staged changes
/review

# Review specific files
/review src/auth/*.ts

# Review with depth level (1-5)
/review --depth 4

# Review PR
/review --pr 123
```

## Workflow

### Phase 1: Context Gathering

Analyze the review scope:

```python
# Run diff analysis script
python3 scripts/analyze_diff.py [files|--staged|--pr PR_NUMBER]
```

The script outputs:

- Changed files list with line counts
- Complexity score (1-5)
- Language detection
- Suggested review depth

### Phase 2: Parallel Agent Review

Launch 4 specialized review agents in parallel:

```
# CRITICAL: Launch all 4 agents in a SINGLE message with multiple Task calls
Task(subagent_type='general-purpose', prompt=SECURITY_PROMPT, model='sonnet', run_in_background=true)
Task(subagent_type='general-purpose', prompt=PERFORMANCE_PROMPT, model='sonnet', run_in_background=true)
Task(subagent_type='general-purpose', prompt=ARCHITECTURE_PROMPT, model='sonnet', run_in_background=true)
Task(subagent_type='general-purpose', prompt=PRACTICES_PROMPT, model='sonnet', run_in_background=true)
```

Agent prompts: See [references/agent_prompts.md](references/agent_prompts.md)

### Phase 3: Synthesis

After all agents complete:

1. Collect findings from all 4 agents using TaskOutput
2. Deduplicate overlapping issues
3. Prioritize by severity (Critical > High > Medium > Low > Info)
4. Map issues to specific file:line locations

### Phase 4: Output Generation

Generate two outputs:

**1. Markdown Report** (saved to `./review-report-{timestamp}.md`)

Use template: [assets/report_template.md](assets/report_template.md)

**2. Inline Comments** (displayed in response)

Format each finding as:

```
📍 file.ts:42
🔴 [Security/Critical] SQL injection vulnerability
   Current: db.query(`SELECT * FROM users WHERE id = ${userId}`)
   Suggested: db.query('SELECT * FROM users WHERE id = $1', [userId])
```

## Severity Labels

| Level    | Label        | Emoji | Description                              |
| -------- | ------------ | ----- | ---------------------------------------- |
| Critical | `[Critical]` | 🔴    | Security vulnerability, data loss risk   |
| High     | `[High]`     | 🟠    | Major bug, significant performance issue |
| Medium   | `[Medium]`   | 🟡    | Should fix, code smell, maintainability  |
| Low      | `[Low]`      | 🟢    | Nice to have, minor improvement          |
| Info     | `[Info]`     | 💡    | Educational, alternative approach        |
| Praise   | `[Praise]`   | 🎉    | Good work, best practice followed        |

## Review Depth Levels

| Level | Focus               | Agents                   | Time    |
| ----- | ------------------- | ------------------------ | ------- |
| 1     | Quick scan          | 1 (combined)             | ~1 min  |
| 2     | Basic review        | 2 (security + practices) | ~2 min  |
| 3     | Standard review     | 4 (all parallel)         | ~3 min  |
| 4     | Deep review         | 4 + extra passes         | ~5 min  |
| 5     | Comprehensive audit | 4 + manual verification  | ~10 min |

## Language Support

Multi-language analysis with language-specific patterns:

| Language      | Security Focus                 | Performance Focus       |
| ------------- | ------------------------------ | ----------------------- |
| TypeScript/JS | XSS, prototype pollution, eval | Bundle size, re-renders |
| Python        | Injection, pickle, exec        | N+1 queries, GIL        |
| Go            | Race conditions, panic         | Goroutine leaks         |
| Java          | Deserialization, JNDI          | Memory, GC pressure     |
| Rust          | Unsafe blocks, lifetimes       | Clone overhead          |

## Integration

### As Skill (Auto-trigger)

Activates when:

- User mentions "review", "코드 리뷰", "PR review"
- User pastes code and asks for feedback
- Working with git diff or PR context

### As Command

```bash
/review                    # Review staged changes
/review src/               # Review specific path
/review --pr 42            # Review GitHub PR
/review --depth 5          # Maximum depth
```

### As Hook (Auto-review)

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash(git commit:*)",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "A commit was just made. Offer to review the changes with /review"
          }
        ]
      }
    ]
  }
}
```

## Resources

- [Agent Prompts](references/agent_prompts.md) - Specialized agent instructions
- [Security Checklist](references/security_checklist.md) - OWASP and vulnerability patterns
- [Performance Patterns](references/performance_patterns.md) - Performance anti-patterns
- [Architecture Guide](references/architecture_guide.md) - SOLID and design patterns
- [Report Template](assets/report_template.md) - Markdown report format
- [Severity Labels](assets/severity_labels.md) - Issue classification guide

## Example Output

```markdown
# Code Review Report

**Reviewed:** 2024-12-24 15:30 KST
**Files:** 8 files, 342 lines changed
**Depth:** Level 3 (Standard)

## Summary

| Category       | Critical | High | Medium | Low |
| -------------- | -------- | ---- | ------ | --- |
| Security       | 1        | 2    | 0      | 1   |
| Performance    | 0        | 1    | 3      | 2   |
| Architecture   | 0        | 0    | 2      | 4   |
| Best Practices | 0        | 0    | 1      | 5   |

## Critical Issues

### 🔴 SQL Injection Vulnerability

**File:** src/db/users.ts:42
**Agent:** Security
...
```
