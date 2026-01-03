# MCP Tool Usage Guide

Detailed guide for gitmvp and context7 MCP tools.

## gitmvp MCP Tools

### search_repositories

Search GitHub repositories by query.

```bash
mcp-cli call gitmvp/search_repositories '{
  "query": "fastapi python",
  "per_page": 10,
  "sort": "stars",
  "order": "desc"
}'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Search query (supports GitHub search syntax) |
| per_page | number | No | Results per page (1-100, default: 30) |
| page | number | No | Page number (default: 1) |
| sort | string | No | Sort by: stars, forks, updated |
| order | string | No | asc or desc |

**Query Syntax Examples:**

- `language:python` - Filter by language
- `user:facebook` - Filter by owner
- `stars:>1000` - Filter by stars
- `topic:machine-learning` - Filter by topic

### search_code

Search code across all GitHub repositories.

```bash
mcp-cli call gitmvp/search_code '{
  "query": "def authenticate language:python",
  "per_page": 20
}'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| query | string | Yes | Code search query |
| per_page | number | No | Results per page (1-100) |
| page | number | No | Page number |

**Query Syntax:**

- `function calculateTotal` - Find function
- `class UserController` - Find class
- `import { useState }` - Find import
- `extension:py` - Filter by extension

### search_code_in_repo

Search code within a specific repository.

```bash
mcp-cli call gitmvp/search_code_in_repo '{
  "owner": "tiangolo",
  "repo": "fastapi",
  "query": "Depends"
}'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| query | string | Yes | Search query |
| per_page | number | No | Results per page |

### get_file_tree

Get repository file structure.

```bash
mcp-cli call gitmvp/get_file_tree '{
  "owner": "tiangolo",
  "repo": "fastapi",
  "format": "tree"
}'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| branch | string | No | Branch name (default: main) |
| format | string | No | "tree" or "json" |

### read_repository

Read file contents from repository.

```bash
mcp-cli call gitmvp/read_repository '{
  "owner": "tiangolo",
  "repo": "fastapi",
  "path": "fastapi/dependencies/utils.py",
  "branch": "master"
}'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| path | string/array | Yes | File path(s) to read |
| branch | string | No | Branch name (default: main) |

**Multi-file read:**

```bash
mcp-cli call gitmvp/read_repository '{
  "owner": "tiangolo",
  "repo": "fastapi",
  "path": ["README.md", "setup.py"]
}'
```

### get_estimated_tokens

Estimate token count for repository.

```bash
mcp-cli call gitmvp/get_estimated_tokens '{
  "owner": "tiangolo",
  "repo": "fastapi"
}'
```

## context7 MCP Tools

### resolve-library-id

Resolve library name to context7 ID.

```bash
mcp-cli call plugin_context7_context7/resolve-library-id '{
  "libraryName": "fastapi"
}'
```

**Common Library IDs:**
| Library | ID |
|---------|-----|
| Next.js | /vercel/next.js |
| React | /facebook/react |
| FastAPI | /tiangolo/fastapi |
| Django | /django/django |
| Express | /expressjs/express |
| Vue | /vuejs/vue |
| Angular | /angular/angular |
| Svelte | /sveltejs/svelte |

### query-docs

Query library documentation.

```bash
mcp-cli call plugin_context7_context7/query-docs '{
  "libraryId": "/tiangolo/fastapi",
  "query": "dependency injection",
  "tokens": 5000
}'
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| libraryId | string | Yes | Context7 library ID |
| query | string | Yes | Documentation query |
| tokens | number | No | Max tokens (default: 5000) |

## Best Practices

### Search Strategy

1. **Start specific**: Use `search_code_in_repo` if you know the repo
2. **Broaden if needed**: Fall back to `search_code` for discovery
3. **Explore structure**: Use `get_file_tree` to understand repo layout
4. **Deep read**: Use `read_repository` for full file content

### Rate Limiting

- GitHub API has rate limits
- Use `per_page` wisely (10-30 is usually sufficient)
- Cache results when possible
- Report rate limits to user with retry timing

### Error Recovery

| Error            | Recovery                              |
| ---------------- | ------------------------------------- |
| 404 Not Found    | Try different branch (master vs main) |
| 403 Rate Limited | Wait and retry, report to user        |
| Empty Results    | Broaden search terms                  |
| Timeout          | Reduce per_page, try again            |

### Permalink Construction

Always construct permalinks with commit SHA:

```
https://github.com/{owner}/{repo}/blob/{SHA}/{path}#L{start}-L{end}
```

**Example:**

```
https://github.com/tiangolo/fastapi/blob/abc1234/fastapi/dependencies/utils.py#L45-L67
```

Never use branch names in permalinks (they can change).
