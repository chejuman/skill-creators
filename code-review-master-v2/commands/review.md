---
description: Expert multi-agent code review with Security, Performance, Architecture, and Best Practices analysis
argument-hint: [path|--staged|--pr NUMBER] [--depth 1-5]
---

# Code Review Command

You are now executing the Code Review Master V2 workflow.

## Arguments Received

```
$ARGUMENTS
```

## Current Context

- Git status: !`git status --short 2>/dev/null | head -20`
- Current branch: !`git branch --show-current 2>/dev/null`

## Workflow Execution

Follow these steps precisely:

### Step 1: Analyze Scope

Run the diff analysis script to understand the review scope:

```bash
python3 ~/.claude/skills/code-review-master-v2/scripts/analyze_diff.py $ARGUMENTS
```

Parse the output to determine:

- Files to review
- Languages detected
- Suggested depth level
- Which agents to spawn

### Step 2: Read Changed Files

Based on the analysis, read each changed file to get the full context.
Use the Read tool for each file that will be reviewed.

### Step 3: Launch Parallel Review Agents

**CRITICAL: Launch ALL agents in a SINGLE message with multiple Task tool calls.**

Based on the depth level, spawn the appropriate agents from `references/agent_prompts.md`:

**Depth 1-2:**

- Combined or Security + Practices agents

**Depth 3-5:**

- Security Agent
- Performance Agent
- Architecture Agent
- Best Practices Agent

Each agent receives:

- The code diff
- Language context
- Framework context

### Step 4: Collect Results

Wait for all agents to complete using TaskOutput.
Collect findings from each agent.

### Step 5: Synthesize Report

1. Deduplicate overlapping findings
2. Sort by severity (Critical > High > Medium > Low > Info)
3. Group by file
4. Generate executive summary

### Step 6: Output

Generate TWO outputs:

**1. Inline Comments (display immediately)**

Format:

```
📍 file.ts:42
🔴 [Security/Critical] SQL Injection
   Current: db.query(`SELECT * FROM users WHERE id = ${userId}`)
   Suggested: db.query('SELECT * FROM users WHERE id = $1', [userId])
```

**2. Markdown Report (save to file)**

Save to `./review-report-{timestamp}.md` using the template from:
`~/.claude/skills/code-review-master-v2/assets/report_template.md`

### Step 7: Summary

Provide a brief summary:

- Total findings by severity
- Top 3 most important issues
- Verdict (Approve / Request Changes / Needs Discussion)
- Offer to explain any finding in detail

## Severity Guide

| Emoji | Level    | Action                |
| ----- | -------- | --------------------- |
| 🔴    | Critical | Must fix before merge |
| 🟠    | High     | Should fix            |
| 🟡    | Medium   | Should address        |
| 🟢    | Low      | Nice to have          |
| 💡    | Info     | FYI only              |
| 🎉    | Praise   | Good work             |

## Notes

- For large diffs (>500 lines), suggest splitting into smaller reviews
- For depth 4-5, perform extra verification passes
- Always include at least one praise item for good practices found
- If no issues found, confirm with explicit "Clean review" message
