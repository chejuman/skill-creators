---
name: workflow-creator-codex
description: Create Codex-ready workflows and automation packages (skills, custom prompts, AGENTS.md, scripts) for DevOps, Security, WebDev, DataOps, Documentation, and Testing. Use when asked to create a workflow, automate a task, make a skill, add a prompt, or migrate a Claude workflow to Codex.
---

# Workflow Creator (Codex)

Build Codex-native workflow packages: skills, custom prompts, AGENTS.md guidance, and script-backed automation.

## Quick triage

1. Identify domain and scope (DevOps, Security, WebDev, DataOps, Documentation, Testing, General).
2. Choose outputs:
   - Skill (shareable, auto or explicit invocation)
   - Custom prompt (explicit `/prompts:<name>`)
   - AGENTS.md (persistent repo or global guidance)
   - Scripts/templates (deterministic steps)
3. Confirm constraints: repo vs user scope, approvals, network access, tool availability.

## Output selection

Use this decision map:
- Needs auto-selection or shareable workflow -> Skill
- Needs explicit slash-style invocation and user-local -> Custom prompt
- Needs persistent repo rules/instructions -> AGENTS.md
- Needs external tools or live docs -> MCP (update `~/.codex/config.toml`)

If multiple are needed, produce a small bundle (skill + custom prompt + AGENTS.md + scripts).

## Claude to Codex mapping

Replace Claude-only mechanisms with Codex-native outputs:
- Task/Subagent orchestration -> role-based passes in one session (see `references/agent_prompts.md`)
- Slash commands -> custom prompts (`/prompts:<name>`)
- Hooks/settings.json -> AGENTS.md or scripts (Codex does not use Claude hooks)

## Workflow (Codex optimized)

1. Discover
   - Read AGENTS.md in scope (if present).
   - List existing skills in repo and user scopes to avoid collisions.
2. Clarify
   - Ask only the minimum questions (domain, output format, complexity, constraints).
3. Design
   - Draft workflow steps and inputs/outputs.
   - Keep SKILL.md concise and imperative.
4. Implement
   - Scaffold with the skill-creator `init_skill.py` when creating a new skill.
   - Add references/templates only when they reduce repeat work.
5. Validate
   - Frontmatter has single-line `name` and `description`.
   - Name <= 100 chars, description <= 500 chars.
6. Install
   - Repo scope: `.codex/skills/<skill-name>`
   - User scope: `~/.codex/skills/<skill-name>`
   - Custom prompts: `~/.codex/prompts/<name>.md` (create the directory if missing)
   - Restart Codex to load updates.
7. Report
   - Provide usage examples and where files were installed.
   - Note any missing dependencies (e.g., PyYAML for validation scripts).

## Quality gates

- Keep SKILL.md under 250 lines unless the workflow is genuinely complex.
- Prefer references for long templates, schemas, or repetitive examples.
- Use scripts for deterministic steps that should not be re-written each run.
- Avoid creating README/INSTALL docs inside the skill.

## Domain questions (ask only when needed)

DevOps: platform, CI/CD tool, environments, rollback needs.
Security: scan types, compliance standards, severity report format.
WebDev: framework, styling system, test framework.
DataOps: sources, pipeline type, storage targets, validation rules.
Documentation: doc types, output format, source of truth.
Testing: test types, frameworks, CI integration.

## Bundle layout (when multiple outputs are requested)

```
workflow-name/
├── workflow-name/                 # Skill
│   ├── SKILL.md
│   └── references/
├── prompts/
│   └── quick-run.md               # Custom prompt
└── AGENTS.md                      # Repo guidance
```

## Codex CLI helpers

- Use `/status` to confirm model, approvals, and writable roots.
- Use `/diff` to review generated files.
- Use `/review` for a quick QA pass.
- Use `/mcp` to confirm external tools are available.

## References

- `references/domain_templates.md` for domain-specific templates.
- `references/format_examples.md` for skill, prompt, and AGENTS.md examples.
- `references/agent_prompts.md` for structured role-based passes.
