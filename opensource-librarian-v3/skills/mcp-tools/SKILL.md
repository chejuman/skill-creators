---
name: mcp-tools
description: Reference for gitmvp and context7 MCP tool usage. Use when working with GitHub repositories via MCP, searching code, reading files, or fetching documentation. Includes complete tool schemas and examples.
---

# MCP Tools Skill

Complete reference for gitmvp and context7 MCP integration.

## gitmvp MCP Server

### search_repositories

Find GitHub repositories by query.

```bash
mcp-cli call gitmvp/search_repositories '{
  "query": "react hooks",
  "sort": "stars",
  "order": "desc",
  "per_page": 10
}'
```

| Param    | Type   | Required | Values                |
| -------- | ------ | -------- | --------------------- |
| query    | string | Yes      | Search query          |
| sort     | string | No       | stars, forks, updated |
| order    | string | No       | asc, desc             |
| per_page | number | No       | 1-100                 |

### get_file_tree

Get repository structure.

```bash
mcp-cli call gitmvp/get_file_tree '{
  "owner": "facebook",
  "repo": "react",
  "format": "tree"
}'
```

### search_code_in_repo

Search code within specific repository.

```bash
mcp-cli call gitmvp/search_code_in_repo '{
  "owner": "fastapi",
  "repo": "fastapi",
  "query": "class Depends"
}'
```

### read_repository

Read file(s) from repository.

```bash
mcp-cli call gitmvp/read_repository '{
  "owner": "fastapi",
  "repo": "fastapi",
  "path": ["fastapi/routing.py", "fastapi/dependencies/utils.py"],
  "branch": "main"
}'
```

## context7 MCP Server

### resolve-library-id

Get library identifier.

```bash
mcp-cli call plugin_context7_context7/resolve-library-id '{
  "libraryName": "fastapi"
}'
```

**Common IDs:**
| Library | ID |
|---------|---|
| React | /facebook/react |
| Next.js | /vercel/next.js |
| FastAPI | /tiangolo/fastapi |
| Vue | /vuejs/vue |

### query-docs

Query library documentation.

```bash
mcp-cli call plugin_context7_context7/query-docs '{
  "libraryId": "/tiangolo/fastapi",
  "query": "dependency injection",
  "tokens": 5000
}'
```

## SHA Acquisition

**CRITICAL**: Always get commit SHA for permalinks.

```bash
# Get HEAD commit
gh api repos/[owner]/[repo]/commits/HEAD --jq '.sha'

# Get file's last commit
gh api "repos/[owner]/[repo]/commits?path=[file]&per_page=1" --jq '.[0].sha'
```

## Permalink Format

```
https://github.com/{owner}/{repo}/blob/{SHA}/{path}#L{start}-L{end}
```

## Error Handling

| Error            | Recovery                        |
| ---------------- | ------------------------------- |
| 404              | Try master branch, search forks |
| 403 Rate Limited | Wait, report timing             |
| 422 Search Limit | Paginate, narrow query          |
| Timeout          | Retry with smaller scope        |
