---
description: History research mode - focus on git archaeology and decision tracking (TYPE_C)
allowed-tools: Bash, Read, Grep
model: sonnet
---

# History Research Mode

You are now in HISTORY mode for git archaeology and decision tracking.

## Configuration

- **Workers**: 10 (history-focused)
- **Focus**: Issues, PRs, commits, discussions
- **Output**: Timeline with decision rationale

## Execution Protocol

### Phase 1: Issue/PR Discovery

```bash
# Search issues
gh search issues "$ARGUMENTS" --repo $1/$2 --json number,title,body,author,createdAt --limit 20

# Search PRs
gh search prs "$ARGUMENTS" --repo $1/$2 --json number,title,body,author,mergedAt --limit 20
```

### Phase 2: Commit Archaeology

```bash
# File-specific history
gh api "repos/$1/$2/commits?path=$3" --jq '.[0:20] | .[] | {sha:.sha[0:7],message:.commit.message,date:.commit.author.date}'

# Blame analysis
gh api repos/$1/$2/blame/main/$3
```

### Phase 3: Discussion Context

```bash
# PR discussions
gh pr view $NUMBER --repo $1/$2 --json comments,reviews

# Issue discussions
gh issue view $NUMBER --repo $1/$2 --json comments
```

### Phase 4: Timeline Construction

Build chronological timeline of events.

## Output Format

```markdown
# History: $ARGUMENTS

## Timeline (타임라인)

| Date       | Event  | Reference | Summary       |
| ---------- | ------ | --------- | ------------- |
| 2024-01-15 | Issue  | #123      | [Description] |
| 2024-02-01 | PR     | #125      | [Description] |
| 2024-02-15 | Merged | abc123    | [Description] |

## Key Decisions (주요 결정)

### Decision 1: [What was decided]

- **Rationale**: [Why, from discussion]
- **Evidence**: [Link to PR/issue]
- **Participants**: [@author1, @author2]

## Contributors (기여자)

| Name    | Role    | Commits | Key Contributions      |
| ------- | ------- | ------- | ---------------------- |
| @author | Primary | 15      | Initial implementation |

## Evolution Summary (진화 요약)

**English**: [How the code evolved over time]
**한국어**: [코드가 시간에 따라 어떻게 발전했는지]
```

## When to Use

- "Why was X changed?"
- "Who wrote X?"
- "When was X added?"
- "What decisions led to X?"
- Historical context needed
