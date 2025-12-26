---
name: codebase-documenter
description: Comprehensive codebase documentation generator using hierarchical multi-agent analysis. Spawns 5+ parallel agents for codebase analysis (structure, tech stack, APIs, architecture, config) and 6 parallel agents for document generation (README, CONTRIBUTING, ARCHITECTURE, API, DEPLOYMENT, CHANGELOG, TROUBLESHOOTING). Use when documenting projects, generating README, creating technical documentation, or onboarding new developers. Triggers on "document codebase", "generate docs", "create README", "project documentation", "technical writing".
---

# Codebase Documenter

Hierarchical multi-agent documentation generator for web applications.

## Architecture

```
┌────────────────────────────────────────────────────────┐
│          PHASE 1: CODEBASE ANALYSIS (5 agents)         │
│  Structure │ TechStack │ API │ Architecture │ Config   │
├────────────────────────────────────────────────────────┤
│          PHASE 2: DOC GENERATION (6 agents)            │
│  README │ CONTRIBUTING │ ARCHITECTURE │ API │          │
│  DEPLOYMENT │ CHANGELOG+TROUBLESHOOTING               │
├────────────────────────────────────────────────────────┤
│          PHASE 3: VALIDATION (1 agent)                 │
│  Link Validator & Cross-Referencer                     │
└────────────────────────────────────────────────────────┘
```

## Quick Start

1. Navigate to project root
2. Run `/docs` or say "document this codebase"
3. Wait for parallel analysis and generation
4. Review generated documents in `docs/` directory

## Workflow

### Phase 1: Parallel Codebase Analysis

Launch 5 analysis agents simultaneously:

```markdown
# Agent 1: Project Structure Analyzer

Task(subagent_type='Explore', model='haiku', run_in_background=true,
prompt='Analyze project structure: directory layout, entry points, build config,
module organization. Return: tree structure, key directories, file purposes.')

# Agent 2: Tech Stack Detector

Task(subagent_type='Explore', model='haiku', run_in_background=true,
prompt='Detect tech stack from package.json, requirements.txt, go.mod, Cargo.toml.
Return: languages, frameworks, databases, versions, dependencies.')

# Agent 3: API Endpoint Extractor

Task(subagent_type='Explore', model='haiku', run_in_background=true,
prompt='Extract API endpoints: routes, methods, request/response schemas.
Search for Express, FastAPI, Spring patterns. Return: endpoint catalog.')

# Agent 4: Architecture Analyzer

Task(subagent_type='Explore', model='haiku', run_in_background=true,
prompt='Analyze architecture: design patterns, component relationships, data flow.
Identify MVC, microservices, monolith patterns. Return: architecture summary.')

# Agent 5: Configuration Scanner

Task(subagent_type='Explore', model='haiku', run_in_background=true,
prompt='Scan configuration: .env.example, config files, environment variables.
Return: required env vars, config options, secrets placeholders.')
```

### Phase 2: Parallel Document Generation

After Phase 1 completes, launch 6 document generators:

```markdown
# Use analysis results to generate documents in parallel

# See references/agent_prompts.md for full prompts

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
prompt='Generate README.md with: {analysis_results}. Follow template in assets/')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
prompt='Generate CONTRIBUTING.md with: {analysis_results}.')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
prompt='Generate ARCHITECTURE.md with: {analysis_results}. Include Mermaid diagrams.')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
prompt='Generate API.md with: {api_endpoints}.')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
prompt='Generate DEPLOYMENT.md with: {config_results}.')

Task(subagent_type='general-purpose', model='sonnet', run_in_background=true,
prompt='Generate CHANGELOG.md and TROUBLESHOOTING.md templates.')
```

### Phase 3: Validation

```markdown
Task(subagent_type='general-purpose', model='haiku',
prompt='Validate generated docs: check links, cross-references, consistency.
Fix broken references. Generate summary report.')
```

## Output Documents

| Document           | Purpose           | Key Sections                    |
| ------------------ | ----------------- | ------------------------------- |
| README.md          | Project overview  | Badges, Quick start, Tech stack |
| CONTRIBUTING.md    | Contributor guide | Setup, Style guide, PR process  |
| ARCHITECTURE.md    | System design     | Diagrams, Components, Data flow |
| API.md             | API reference     | Endpoints, Auth, Examples       |
| DEPLOYMENT.md      | Deploy guide      | Environments, Steps, Rollback   |
| CHANGELOG.md       | Version history   | Keep a Changelog format         |
| TROUBLESHOOTING.md | Common issues     | FAQ, Debug tips                 |

## Quality Standards

- **Style**: Google Developer Documentation Style Guide
- **Diagrams**: Mermaid syntax for GitHub/GitLab rendering
- **Markers**: `[ASSUMPTION]` for inferred info, `[NEEDS INPUT]` for missing data
- **Cross-refs**: All documents link to each other
- **Examples**: Include copy-paste ready code blocks

## Document Templates

See [references/doc_templates.md](references/doc_templates.md) for full templates.

See [assets/mermaid_templates.md](assets/mermaid_templates.md) for diagram examples.

## Agent Prompts

See [references/agent_prompts.md](references/agent_prompts.md) for complete agent prompts.

## Analysis Scripts

### Analyze Codebase Structure

```bash
python scripts/analyze_codebase.py /path/to/project
```

Returns JSON with:

- Directory tree
- File type distribution
- Entry points
- Build configuration

### Validate Documentation

```bash
python scripts/validate_docs.py /path/to/docs
```

Checks:

- Broken links
- Missing cross-references
- Inconsistent formatting
- TOC accuracy

## Customization

### Adding Custom Sections

Edit `references/doc_templates.md` to add project-specific sections.

### Changing Diagram Style

Edit `assets/mermaid_templates.md` to customize diagram themes.

### Adjusting Agent Count

Reduce agents for smaller projects by combining analysis tasks.

## Trigger Phrases

- "document this codebase"
- "generate project documentation"
- "create README and docs"
- "write technical documentation"
- "document for onboarding"
- "/docs" (slash command)
