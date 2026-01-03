# Format Examples (Codex)

## Skill Example

**Location (repo):** `.codex/skills/code-formatter/SKILL.md`

```yaml
---
name: code-formatter
description: Format code using project-specific formatters. Use when asked to format files or enforce code style across the repo.
---

# Code Formatter

## Workflow
1. Detect formatter config (prettier, eslint, black, ruff, gofmt, etc.)
2. Identify target files from user request or git status
3. Run the formatter
4. Summarize changes
```

## Custom Prompt Example

**Location (user):** `~/.codex/prompts/draftpr.md` (create `~/.codex/prompts/` if missing)

```yaml
---
description: Prep a branch, commit, and open a draft PR
argument-hint: [FILES=<paths>] [PR_TITLE="<title>"]
---

Create a branch named `dev/<feature_name>` for this work.
If files are specified, stage them first: $FILES.
Commit the staged changes with a clear message.
Open a draft PR on the same branch. Use $PR_TITLE when supplied; otherwise write a concise summary yourself.
```

Invoke with `/prompts:draftpr`.

## AGENTS.md Example

**Location (repo root):** `AGENTS.md`

```markdown
# Project Instructions

- Prefer `pnpm` for installs and scripts.
- Run `pnpm test` before finishing if tests are relevant.
- Avoid touching `infra/` unless requested.
```

## Install Notes (Codex)

```
# Repo scope skill
mkdir -p .codex/skills
cp -R <skill-folder> .codex/skills/

# User scope skill
mkdir -p ~/.codex/skills
cp -R <skill-folder> ~/.codex/skills/

# User scope prompt
mkdir -p ~/.codex/prompts
cp prompts/<name>.md ~/.codex/prompts/
```
