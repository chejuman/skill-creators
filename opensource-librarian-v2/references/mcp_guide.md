# MCP Integration Guide

Complete guide for gitmvp and context7 MCP tool usage.

## gitmvp MCP Server

### Tool: search_repositories

Find GitHub repositories by query.

```bash
mcp-cli call gitmvp/search_repositories '{
  "query": "fastapi framework",
  "sort": "stars",
  "order": "desc",
  "per_page": 10
}'
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Search query |
| sort | string | No | stars, forks, updated |
| order | string | No | asc, desc |
| per_page | number | No | 1-100 (default 30) |

### Tool: get_file_tree

Get repository structure.

```bash
mcp-cli call gitmvp/get_file_tree '{
  "owner": "fastapi",
  "repo": "fastapi",
  "format": "tree"
}'
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| owner | string | Yes | Repo owner |
| repo | string | Yes | Repo name |
| branch | string | No | Branch (default: main) |
| format | string | No | tree, json |

### Tool: search_code

Search code across all GitHub.

```bash
mcp-cli call gitmvp/search_code '{
  "query": "def dependency_injection language:python",
  "per_page": 20
}'
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Code search query |
| per_page | number | No | 1-100 |
| sort | string | No | indexed |

### Tool: search_code_in_repo

Search code within specific repository.

```bash
mcp-cli call gitmvp/search_code_in_repo '{
  "owner": "fastapi",
  "repo": "fastapi",
  "query": "Depends class"
}'
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| owner | string | Yes | Repo owner |
| repo | string | Yes | Repo name |
| query | string | Yes | Search query |
| per_page | number | No | 1-100 |

### Tool: read_repository

Read file(s) from repository.

```bash
mcp-cli call gitmvp/read_repository '{
  "owner": "fastapi",
  "repo": "fastapi",
  "path": "fastapi/dependencies/utils.py",
  "branch": "main"
}'
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| owner | string | Yes | Repo owner |
| repo | string | Yes | Repo name |
| path | string/array | Yes | File path(s) |
| branch | string | No | Branch (default: main) |

### Tool: get_estimated_tokens

Estimate token count for repository.

```bash
mcp-cli call gitmvp/get_estimated_tokens '{
  "owner": "fastapi",
  "repo": "fastapi"
}'
```

## context7 MCP Server

### Tool: resolve-library-id

Get library identifier for documentation queries.

```bash
mcp-cli call plugin_context7_context7/resolve-library-id '{
  "libraryName": "fastapi"
}'
```

**Common Library IDs:**
| Library | ID |
|---------|---|
| React | /facebook/react |
| Next.js | /vercel/next.js |
| FastAPI | /tiangolo/fastapi |
| Django | /django/django |
| Vue | /vuejs/vue |
| Express | /expressjs/express |

### Tool: query-docs

Query library documentation.

```bash
mcp-cli call plugin_context7_context7/query-docs '{
  "libraryId": "/tiangolo/fastapi",
  "query": "dependency injection Depends",
  "tokens": 5000
}'
```

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| libraryId | string | Yes | Library identifier |
| query | string | Yes | Documentation query |
| tokens | number | No | Max tokens (default: 5000) |

## SHA Acquisition

After finding code, acquire commit SHA for permalinks:

```bash
# Get HEAD commit SHA
gh api repos/[owner]/[repo]/commits/HEAD --jq '.sha'

# Get specific file's last commit SHA
gh api repos/[owner]/[repo]/commits?path=[file]&per_page=1 --jq '.[0].sha'
```

## Permalink Construction

```
https://github.com/{owner}/{repo}/blob/{SHA}/{path}#L{start}-L{end}
```

**Examples:**

```
# Single line
https://github.com/fastapi/fastapi/blob/abc123/fastapi/routing.py#L45

# Line range
https://github.com/fastapi/fastapi/blob/abc123/fastapi/routing.py#L45-L67
```

## Rate Limit Handling

GitHub API limits:

- Authenticated: 5000 requests/hour
- Unauthenticated: 60 requests/hour

**Detection:**

```bash
gh api rate_limit --jq '.resources.core'
```

**Recovery:**

1. Report remaining quota
2. Suggest retry timing
3. Cache previous results
4. Use conditional requests (If-None-Match)

## Error Recovery Matrix

| Error            | Recovery Strategy                 |
| ---------------- | --------------------------------- |
| 404 Repository   | Try `master` branch, search forks |
| 403 Rate Limited | Wait, report timing               |
| 422 Search Limit | Paginate, narrow query            |
| 500 Server Error | Retry with backoff                |
| Connection Error | Retry 3 times                     |
