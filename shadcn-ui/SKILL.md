---
name: shadcn-ui
description: Manage shadcn/ui components with discovery, search, recommendations, and integration support. Use when user requests component information, wants to add UI components, needs component recommendations, searches shadcn registry, or asks about shadcn/ui.
---

# shadcn/ui Component Management

Discover, explore, and integrate shadcn/ui components through an intelligent CLI interface. Provides component search, detailed information, usage examples, and AI-powered recommendations.

## When to Use This Skill

Trigger this skill when user:
- Requests information about shadcn/ui components
- Wants to search or browse available components
- Needs component recommendations for a specific UI task
- Wants to see component details, dependencies, or code examples
- Asks how to add shadcn/ui components to their project
- Mentions "shadcn", "shadcn/ui", or UI component libraries

## Quick Start

After installing to `~/.claude/skills/shadcn-ui/`:

```bash
cd ~/.claude/skills/shadcn-ui/scripts
npm install
```

Prerequisites: Node.js, npm/npx, shadcn CLI (via npx)

## Core Commands

### 1. list - List All Components

```bash
npx tsx cli.ts list [registry]
```

Lists all available components from registry with types and descriptions.

### 2. search - Search Components

```bash
npx tsx cli.ts search <query> [registry]
```

Search components by keyword with fuzzy matching. Returns ranked results.

### 3. view - View Component Details

```bash
npx tsx cli.ts view <component>
```

Display name, type, description, dependencies, and file structure.

### 4. examples - Get Usage Examples

```bash
npx tsx cli.ts examples <component>
```

Extract and display complete code examples with syntax highlighting.

### 5. recommend - Component Recommendations

```bash
npx tsx cli.ts recommend "<task description>"
```

Get AI-powered recommendations based on task. Returns top 10 ranked suggestions with scores and reasons for Claude to analyze.

**Algorithm:** Keyword matching (weight: 10-20), category matching (weight: 8), type preference (ui > block > hook).

### 6. add-command - Generate Add Command

```bash
npx tsx cli.ts add-command <component1> [component2] ...
```

Generate shadcn CLI installation command (does not execute).

### 7. registries - Show Project Configuration

```bash
npx tsx cli.ts registries
```

Display project's shadcn configuration from components.json.

### 8. audit - Project Checklist

```bash
npx tsx cli.ts audit
```

Show post-installation checklist and troubleshooting guidance.

## Configuration

Optional environment variables via `.env`:

```bash
SHADCN_DEFAULT_REGISTRY=@shadcn
# SHADCN_CWD=/path/to/project
```

.env hierarchy (highest priority first):
1. `process.env`
2. `.claude/skills/shadcn-ui/.env`
3. `.claude/skills/.env`
4. `.claude/.env`

## Example Workflows

**Find and Add Components:**
```bash
npx tsx cli.ts search "form"
npx tsx cli.ts view form
npx tsx cli.ts examples form
npx tsx cli.ts add-command form input button label
```

**Get Recommendations:**
```bash
npx tsx cli.ts recommend "user profile page with avatar and bio"
# Claude analyzes recommendations
npx tsx cli.ts view avatar card textarea
npx tsx cli.ts add-command avatar card textarea button
```

**Project Setup:**
```bash
npx tsx cli.ts registries
# If not configured: npx shadcn@latest init
npx tsx cli.ts audit
```

## Component Categories

Components are categorized in `assets/component-categories.json`:
- **form**: input, select, checkbox, form
- **data**: table, card, accordion, avatar, badge
- **navigation**: tabs, menu, breadcrumb, command
- **overlay**: dialog, sheet, popover, tooltip
- **feedback**: toast, alert, progress
- **interactive**: button, toggle, slider
- **layout**: card, separator, scroll-area

## Technical Notes

**CLI Wrapper:** Wraps `npx shadcn@latest` commands with no complex dependencies. Parses JSON and table formats. Handles errors with helpful suggestions.

**Error Handling:** Common errors include missing components.json (run `npx shadcn@latest init`), component not found (try search), CLI not found (check npm/npx).

**Performance:** Fast lookups via direct CLI calls, no external APIs, metadata loads once per session.

For detailed component selection guidance, see `references/component-guide.md`.
