# Open Source Librarian V3

Premium Level 7 multi-agent open source code research plugin for Claude Code.

## Features

### 5 Specialized Agents

| Agent                   | Purpose                          | Model  | Auto-Trigger                            |
| ----------------------- | -------------------------------- | ------ | --------------------------------------- |
| `synthesis-coordinator` | Orchestrate 15+ parallel workers | Opus   | Complex research queries                |
| `code-hunter`           | Find implementations via gitmvp  | Sonnet | "show me source", "find implementation" |
| `git-archaeologist`     | Trace history via gh CLI         | Sonnet | "why was changed", "who wrote"          |
| `doc-researcher`        | Fetch docs via context7          | Haiku  | Documentation queries                   |
| `evidence-validator`    | Verify permalinks and claims     | Haiku  | After code/history research             |

### 3 Knowledge Skills

- **code-research** - Research methodology and classification
- **mcp-tools** - gitmvp and context7 MCP reference
- **citation-patterns** - Permalink standards and JSON API v3 schema

### 3 Output Commands

| Command              | Mode            | Workers |
| -------------------- | --------------- | ------- |
| `/librarian:quick`   | Fast lookup     | 3       |
| `/librarian:deep`    | Comprehensive   | 15+     |
| `/librarian:history` | Git archaeology | 10      |

### 6 Automation Hooks

| Hook                 | Trigger          | Action                 |
| -------------------- | ---------------- | ---------------------- |
| `validate-mcp-call`  | PreToolUse:Bash  | Validate MCP syntax    |
| `validate-permalink` | PostToolUse:Bash | Check SHA in URLs      |
| `auto-citation`      | PostToolUse:Bash | Format citations       |
| `log-worker`         | PostToolUse:Task | Track parallel workers |
| `check-mcp-servers`  | SessionStart     | Verify gitmvp/context7 |
| `generate-report`    | Stop             | Session summary        |

## Installation

```bash
# Clone the plugin
git clone https://github.com/skill-creators/opensource-librarian-v3.git

# Run Claude Code with the plugin
claude --plugin-dir ./opensource-librarian-v3
```

## Usage

### Quick Lookup

```
/librarian:quick
How does FastAPI handle routing?
```

### Deep Research

```
/librarian:deep
Analyze the dependency injection system in FastAPI
```

### History Research

```
/librarian:history
Why was the Depends class refactored in FastAPI 0.100?
```

### Auto-Triggered Research

```
User: Show me how React's useState hook works internally

Claude: [Uses code-hunter agent with gitmvp MCP]
        [Returns SHA-based GitHub permalinks]
        [Bilingual EN/KR output]
```

## Request Classification

| Type   | Pattern               | Workers | Focus          |
| ------ | --------------------- | ------- | -------------- |
| TYPE_A | "How do I use X?"     | 5       | Conceptual     |
| TYPE_B | "Show me how X works" | 8       | Implementation |
| TYPE_C | "Why was X changed?"  | 10      | Historical     |
| TYPE_D | Complex multi-part    | 15+     | Comprehensive  |

## MCP Requirements

- **gitmvp** - GitHub repository analysis
- **context7** - Library documentation

## Output Formats

### Bilingual Summary

```markdown
## TL;DR (요약)

**English**: [Summary]
**한국어**: [요약]
```

### JSON API v3

```json
{
  "apiVersion": "v3",
  "metadata": {...},
  "summary": {"en": "...", "ko": "..."},
  "findings": [...],
  "validation": {...}
}
```

## Trigger Phrases

- "opensource librarian" / "오픈소스 라이브러리언"
- "find code implementation" / "코드 구현 찾아줘"
- "show me the source" / "소스 코드 보여줘"
- "how does X work" / "X가 어떻게 동작해"
- "why was this changed" / "왜 변경됐어"

## Requirements

- Claude Code v1.0.33+
- gitmvp MCP server
- context7 MCP server
- GitHub CLI (gh)

## License

MIT
