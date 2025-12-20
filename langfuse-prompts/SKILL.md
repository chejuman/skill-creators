---
name: langfuse-prompts
description: Manage and use Langfuse prompts in Claude Code. Use when user requests prompt recommendations, wants to search available prompts, needs to retrieve specific prompts from Langfuse, or execute prompts with variable substitution. Provides prompt discovery, local caching, chat/text prompt support, and Mustache template variable handling.
---

# Langfuse Prompt Management

Manage Langfuse prompts efficiently with local caching and intelligent recommendations. Search, discover, and execute prompts with variable substitution.

## Overview

Langfuse prompts integration enables accessing production prompts from Langfuse directly within Claude Code workflows. The skill provides:

- Local caching for fast prompt discovery (1-hour TTL)
- Search and filtering capabilities
- Intelligent prompt recommendations based on task context
- Variable extraction and substitution for both chat and text prompts
- Support for Mustache template syntax (`{{variable}}`)

## When to Use This Skill

Trigger this skill when:
- User explicitly requests prompt recommendations
- User wants to browse or search available prompts
- User needs to retrieve specific prompts from Langfuse
- User wants to execute a prompt with custom variables

## Quick Start

### Installation

After installing to `~/.claude/skills/langfuse-prompts/`:

```bash
cd ~/.claude/skills/langfuse-prompts/scripts
npm install
```

### Environment Setup

Create `.env` file in the skill directory or any parent directory (`.claude/skills/.env` or `.claude/.env`):

```bash
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com  # Optional
PROMPT_CACHE_TTL_SECONDS=3600  # Optional, default: 1 hour
```

Get credentials from: `https://cloud.langfuse.com/project/[your-project]/settings`

### First-Time Cache Initialization

```bash
npx tsx cli.ts list
```

This fetches all production prompts and caches them locally.

## Core Operations

### Discovering Available Prompts

**Command**: `npx tsx cli.ts list`

Fetches all production-labeled prompts from Langfuse and saves them to local cache (`assets/prompts.json`). Displays summary by type (chat/text) and shows all prompts with their variables and tags.

**Output**:
- Total prompt count
- Breakdown by type (chat/text)
- List of all prompts with variables and tags
- Cache confirmation

**When to use**: Initial setup, when new prompts added to Langfuse, or to refresh stale cache.

---

### Searching Prompts

**Command**: `npx tsx cli.ts search <query>`

Searches cached prompts by name, description, or tags. Case-insensitive keyword matching.

**Examples**:
```bash
npx tsx cli.ts search "email"
npx tsx cli.ts search "onboarding"
npx tsx cli.ts search "marketing"
```

**Output**:
- Number of matches
- Prompt details (name, type, variables, tags)

**When to use**: User knows specific keywords but not exact prompt name.

---

### Recommending Prompts for a Task

**Command**: `npx tsx cli.ts recommend "<task-description>"`

Displays all available prompts in structured format for Claude to analyze and recommend. This leverages Claude's semantic understanding to match prompts with the user's task.

**Example**:
```bash
npx tsx cli.ts recommend "user onboarding welcome email"
```

**Output**:
- Task description
- Complete list of prompts with:
  - Name
  - Description
  - Type (chat/text)
  - Required variables
  - Tags
- Request for Claude to analyze and recommend

**Workflow**:
1. User describes their task
2. Run recommend command
3. Claude receives structured prompt data
4. Claude analyzes task context and prompt metadata
5. Claude recommends best-fit prompts
6. User selects a prompt
7. Proceed to get/execute

**When to use**: User needs help finding the right prompt for their task.

---

### Retrieving a Specific Prompt

**Command**: `npx tsx cli.ts get <prompt-name>`

Fetches detailed information about a specific prompt directly from Langfuse.

**Example**:
```bash
npx tsx cli.ts get user-welcome-email
```

**Output**:
- Prompt metadata (name, type, version, labels, tags)
- Required variables list
- Template preview (formatted by type)

**When to use**: User knows the prompt name and wants to see details before execution.

---

### Executing a Prompt with Variables

**Command**: `npx tsx cli.ts execute <prompt-name> <vars>`

Compiles prompt with provided variables. Variables can be JSON string or JSON file path.

**Examples**:
```bash
# JSON string
npx tsx cli.ts execute user-welcome-email '{"user_name":"John Doe","company":"Acme Corp","product_name":"Platform"}'

# JSON file
npx tsx cli.ts execute user-welcome-email vars.json
```

**vars.json** example:
```json
{
  "user_name": "John Doe",
  "company": "Acme Corp",
  "product_name": "Platform"
}
```

**Output**:
- Prompt type (chat/text)
- Compiled prompt with variables substituted
- For chat prompts: formatted by role

**Handles**:
- Chat prompts: returns array of messages with roles
- Text prompts: returns single compiled string
- Mustache variables: `{{variable}}` syntax
- Role mapping: normalizes "ai"/"assistant" roles

**When to use**: User wants to use a prompt with specific values.

---

### Cache Management

#### Refresh Cache

**Command**: `npx tsx cli.ts cache-refresh`

Forces immediate cache refresh regardless of TTL.

**When to use**: New prompts added to Langfuse, or cache suspected to be out of sync.

#### Cache Info

**Command**: `npx tsx cli.ts cache-info`

Shows cache status and statistics.

**Output**:
- Cache status (valid/stale)
- Prompt count
- Last updated timestamp
- Cache age
- TTL settings
- Time remaining before expiration

**When to use**: Check cache status, debug caching issues.

---

## Configuration

### Environment Variables

**Required**:
- `LANGFUSE_SECRET_KEY` - Langfuse API secret key
- `LANGFUSE_PUBLIC_KEY` - Langfuse API public key

**Optional**:
- `LANGFUSE_BASE_URL` - Custom Langfuse instance URL (default: `https://cloud.langfuse.com`)
- `PROMPT_CACHE_TTL_SECONDS` - Cache TTL in seconds (default: `3600` = 1 hour)

### .env File Hierarchy

Following skill-creator spec, environment variables are loaded in this order (highest priority first):

1. `process.env` (system environment)
2. `.claude/skills/langfuse-prompts/.env`
3. `.claude/skills/.env`
4. `.claude/.env`

Place `.env` file at the appropriate level based on your needs.

### Cache Settings

Cache is automatically refreshed when:
- Cache file doesn't exist
- Cache is older than TTL
- Cache is empty

Manual refresh available via `cache-refresh` command.

---

## Scripts Reference

All scripts located in `scripts/` directory:

- **cli.ts** - Main CLI interface (commands: list, search, recommend, get, execute, cache-*)
- **langfuse-client.ts** - Langfuse API wrapper (handles authentication, pagination, compilation)
- **cache-manager.ts** - Cache operations (load, save, refresh, validation)
- **utils.ts** - Mustache variable extraction (supports `{{variable}}` syntax)

---

## Example Workflow

**Scenario**: User needs a welcome email for new users

1. **Discovery**:
   ```bash
   npx tsx cli.ts recommend "welcome email for new users"
   ```

2. **Claude analyzes** and recommends:
   > "I found `user-welcome-email` prompt (score: 92%). It has 3 variables: `{{user_name}}`, `{{company}}`, `{{product_name}}`"

3. **Get details**:
   ```bash
   npx tsx cli.ts get user-welcome-email
   ```

4. **Execute with variables**:
   ```bash
   npx tsx cli.ts execute user-welcome-email '{"user_name":"Alice","company":"TechCorp","product_name":"Cloud Suite"}'
   ```

5. **Result**: Compiled prompt ready to use

---

## Technical Notes

### Mustache Variables
- Syntax: `{{variable_name}}`
- Valid names: alphanumeric + underscore, must start with letter
- Automatically extracted from prompts
- Case-sensitive

### Chat vs Text Prompts
- **Chat**: Array of messages with roles (user/assistant)
- **Text**: Single string template
- Fallback: Tries chat first, then text

### Role Normalization
Chat prompt roles are normalized:
- `"ai"` → `"assistant"`
- `"assistant"` → `"assistant"`
- Others → `"user"`

### Error Handling
- Clear error messages for missing credentials
- Graceful degradation if API unavailable
- Cache fallback when possible

### Performance
- Local cache reduces API calls
- Pagination handled automatically
- TTL-based cache invalidation
