# Role-Based Passes

Use these short passes to simulate expert agents in a single Codex session. Keep each output compact and deterministic.

## Domain + Complexity Pass

Return:
- domain: DevOps | Security | WebDev | DataOps | Documentation | Testing | General
- complexity: 1-5
- outputs: skill | custom-prompt | agents-md | bundle
- constraints: [repo scope, user scope, approvals, network]
- key_features: [list]

## Format Selection Pass

Return:
- primary_output: skill | custom-prompt | agents-md
- secondary_outputs: [list]
- reason: short rationale

Decision hints:
- Auto-triggered workflow or reusable package -> skill
- Explicit user invocation -> custom prompt
- Persistent repo guidance -> AGENTS.md
- External tools or live data -> MCP (note in plan)

## Research Pass (optional)

If network access is allowed and the user wants it, capture:
- best_practices
- common pitfalls
- recommended tools
- relevant Codex patterns

## Existing Assets Pass

Check for reuse:
- matching skills in `.codex/skills` or `~/.codex/skills`
- prompts in `~/.codex/prompts`
- AGENTS.md in repo or home

Return:
- reuse_candidates: [paths]
- conflicts: [name collisions]
- recommended_reuse: [what to borrow]

## Generation Pass

Produce a concise plan:
- files_to_create
- files_to_update
- install_scope (repo | user)
- validation_steps
- install_steps

## Validation Pass

Return:
- frontmatter_ok: true|false
- name_ok: true|false
- description_ok: true|false
- references_ok: true|false
- missing_deps: [list]
