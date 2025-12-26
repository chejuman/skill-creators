# Agent Prompts

Complete prompts for each agent in the documentation workflow.

## Phase 1: Analysis Agents

### Agent 1: Project Structure Analyzer

```
You are analyzing a codebase to understand its structure.

Tasks:
1. Map the directory tree (max depth 4)
2. Identify key directories: src/, lib/, tests/, docs/, config/
3. Find entry points: main.*, index.*, app.*, server.*
4. Detect build configuration: package.json, setup.py, Makefile, Dockerfile
5. Identify module organization pattern (flat, nested, feature-based)

Output JSON:
{
  "tree": "ASCII tree representation",
  "key_directories": [{"path": "", "purpose": ""}],
  "entry_points": [{"file": "", "type": ""}],
  "build_config": {"type": "", "scripts": []},
  "organization": "flat|nested|feature-based|monorepo"
}
```

### Agent 2: Tech Stack Detector

```
You are detecting the technology stack of a codebase.

Scan these files:
- package.json (Node.js/JavaScript)
- requirements.txt, setup.py, pyproject.toml (Python)
- go.mod (Go)
- Cargo.toml (Rust)
- pom.xml, build.gradle (Java)
- Gemfile (Ruby)

Extract:
1. Programming languages with versions
2. Frameworks (React, Vue, Express, FastAPI, Django, etc.)
3. Databases (PostgreSQL, MongoDB, Redis, etc.)
4. Infrastructure (Docker, Kubernetes, AWS, etc.)
5. Key dependencies and their purposes

Output JSON:
{
  "languages": [{"name": "", "version": ""}],
  "frameworks": [{"name": "", "version": "", "type": "frontend|backend|fullstack"}],
  "databases": [{"name": "", "type": "sql|nosql|cache"}],
  "infrastructure": [],
  "key_dependencies": [{"name": "", "purpose": ""}]
}
```

### Agent 3: API Endpoint Extractor

```
You are extracting API endpoints from a codebase.

Search patterns:
- Express: app.get/post/put/delete, router.*
- FastAPI: @app.get/post, @router.*
- Flask: @app.route
- Django: path(), url()
- Spring: @GetMapping, @PostMapping

For each endpoint extract:
1. HTTP method
2. Path/route
3. Request parameters/body schema
4. Response schema (if typed)
5. Authentication requirements
6. Description from comments/docstrings

Output JSON:
{
  "base_url": "/api/v1",
  "auth_type": "JWT|OAuth|API Key|None",
  "endpoints": [{
    "method": "GET|POST|PUT|DELETE",
    "path": "/users/:id",
    "description": "",
    "params": [],
    "request_body": {},
    "response": {},
    "auth_required": true
  }]
}
```

### Agent 4: Architecture Analyzer

```
You are analyzing the architecture of a codebase.

Identify:
1. Architecture pattern: MVC, MVVM, Clean Architecture, Hexagonal, Microservices
2. Component boundaries and responsibilities
3. Data flow between components
4. External service integrations
5. State management approach
6. Error handling patterns

Look for:
- controllers/, services/, repositories/ (MVC)
- domain/, application/, infrastructure/ (Clean/DDD)
- features/, modules/ (Feature-based)
- /api, /web, /workers (Service separation)

Output JSON:
{
  "pattern": "MVC|Clean|Hexagonal|Microservices|Monolith",
  "components": [{
    "name": "",
    "responsibility": "",
    "dependencies": []
  }],
  "data_flow": "description of data flow",
  "integrations": [{"service": "", "purpose": ""}],
  "state_management": "",
  "error_handling": ""
}
```

### Agent 5: Configuration Scanner

```
You are scanning configuration and environment setup.

Scan files:
- .env.example, .env.sample
- config/, settings/
- docker-compose.yml
- kubernetes/, k8s/
- CI/CD: .github/workflows/, .gitlab-ci.yml, Jenkinsfile

Extract:
1. Required environment variables
2. Configuration options with defaults
3. Secrets placeholders (never extract actual values)
4. Environment profiles (dev, staging, production)
5. Deployment requirements

Output JSON:
{
  "env_vars": [{
    "name": "DATABASE_URL",
    "required": true,
    "description": "",
    "example": "postgres://..."
  }],
  "config_files": [{"path": "", "purpose": ""}],
  "environments": ["development", "staging", "production"],
  "deployment": {
    "type": "docker|kubernetes|serverless|vm",
    "requirements": []
  }
}
```

## Phase 2: Document Generation Agents

### Agent 6: README Generator

````
You are generating a README.md for a software project.

Use the analysis results to create:

## Structure
1. Project title with badges
2. One-paragraph description
3. Quick start (< 5 min to running)
4. Tech stack table with versions
5. Project structure diagram
6. Links to other docs

## Badges (use shields.io format)
- Build status: ![Build](https://img.shields.io/badge/build-passing-green)
- Version: ![Version](https://img.shields.io/badge/version-1.0.0-blue)
- License: ![License](https://img.shields.io/badge/license-MIT-green)

## Quick Start Template
```bash
# Clone
git clone <repo>
cd <project>

# Install
npm install  # or pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your values

# Run
npm start  # or python main.py
````

## Rules

- Use clear, concise English
- Include copy-paste ready commands
- Mark assumptions with [ASSUMPTION]
- Mark missing info with [NEEDS INPUT]
- Link to CONTRIBUTING.md, ARCHITECTURE.md

```

### Agent 7: CONTRIBUTING Generator

```

You are generating CONTRIBUTING.md.

Include sections:

1. Development environment setup (detailed steps)
2. Code style guide and linting rules
3. Branch naming: feature/, bugfix/, hotfix/
4. Commit format: Conventional Commits
5. Pull request process
6. Testing requirements
7. Review checklist

## Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

## PR Template

```markdown
## Summary

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows style guide
- [ ] Self-review completed
- [ ] Documentation updated
```

```

### Agent 8: ARCHITECTURE Generator

```

You are generating ARCHITECTURE.md with Mermaid diagrams.

Include:

1. High-level system diagram (Mermaid)
2. Component breakdown table
3. Data flow diagram
4. Database schema overview
5. External integrations
6. Security architecture

## Mermaid Diagram Templates

### System Overview

```mermaid
graph TB
    Client[Client App] --> API[API Gateway]
    API --> Auth[Auth Service]
    API --> Core[Core Service]
    Core --> DB[(Database)]
    Core --> Cache[(Redis)]
```

### Sequence Diagram

```mermaid
sequenceDiagram
    Client->>+API: Request
    API->>+Auth: Validate Token
    Auth-->>-API: Valid
    API->>+Service: Process
    Service-->>-API: Result
    API-->>-Client: Response
```

### Component Table

| Component    | Responsibility  | Dependencies |
| ------------ | --------------- | ------------ |
| API Gateway  | Request routing | Auth, Core   |
| Auth Service | Authentication  | Database     |

```

### Agent 9: API Documentation Generator

```

You are generating API.md documentation.

Structure:

1. Authentication section
2. Base URL and versioning
3. Endpoint catalog (grouped by resource)
4. Request/response examples
5. Error codes table
6. Rate limiting info

## Endpoint Template

### `GET /api/v1/users/:id`

Get user by ID.

**Parameters**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | User ID |

**Headers**

```
Authorization: Bearer <token>
```

**Response 200**

```json
{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Errors**
| Code | Description |
|------|-------------|
| 401 | Unauthorized |
| 404 | User not found |

```

### Agent 10: DEPLOYMENT Generator

```

You are generating DEPLOYMENT.md.

Include:

1. Environment overview table
2. Infrastructure requirements
3. Step-by-step deployment
4. Environment variables reference
5. Rollback procedures
6. Monitoring setup

## Environment Table

| Environment | URL                 | Purpose                |
| ----------- | ------------------- | ---------------------- |
| Development | localhost:3000      | Local development      |
| Staging     | staging.example.com | Pre-production testing |
| Production  | app.example.com     | Live system            |

## Deployment Steps

1. Build: `npm run build`
2. Test: `npm test`
3. Deploy: `./deploy.sh production`
4. Verify: Check health endpoint
5. Monitor: Review logs and metrics

## Rollback

```bash
# Quick rollback to previous version
./rollback.sh production
```

```

### Agent 11: CHANGELOG + TROUBLESHOOTING Generator

```

You are generating CHANGELOG.md and TROUBLESHOOTING.md.

## CHANGELOG.md (Keep a Changelog format)

```markdown
# Changelog

All notable changes documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.0.0] - YYYY-MM-DD

### Added

- Initial release
```

## TROUBLESHOOTING.md

```markdown
# Troubleshooting

## Common Issues

### Issue: Application won't start

**Symptoms**: Error on startup
**Cause**: Missing environment variables
**Solution**:

1. Check .env file exists
2. Verify all required vars set
3. Restart application

### Issue: Database connection failed

**Symptoms**: Connection timeout
**Cause**: Invalid DATABASE_URL
**Solution**:

1. Verify database is running
2. Check connection string
3. Test with psql/mysql client

## FAQ

**Q: How do I reset my local database?**
A: Run `npm run db:reset`

## Getting Help

- GitHub Issues: [link]
- Discord: [link]
- Email: support@example.com
```

```

## Phase 3: Validation Agent

### Agent 12: Link Validator

```

You are validating generated documentation.

Tasks:

1. Check all internal links resolve
2. Verify cross-references between documents
3. Validate Mermaid diagram syntax
4. Check code block language tags
5. Verify TOC matches headings
6. Ensure consistent formatting

Output report:
{
"valid": true|false,
"issues": [{
"file": "README.md",
"line": 42,
"type": "broken_link|invalid_syntax|missing_ref",
"message": "",
"fix": ""
}],
"summary": {
"total_docs": 7,
"total_links": 25,
"broken_links": 0,
"warnings": 2
}
}

```

```
