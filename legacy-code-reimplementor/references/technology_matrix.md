# Technology Migration Matrix

Reference guide for recommending target technology stacks based on source analysis.

## Language Migration Paths

| Source     | Recommended Targets    | Rationale                                                     |
| ---------- | ---------------------- | ------------------------------------------------------------- |
| Java       | Python, Go, Kotlin     | Python: ML/Data, Go: Microservices, Kotlin: JVM compatibility |
| PHP        | Python, TypeScript, Go | Python: Simplicity, TS: Type safety, Go: Performance          |
| Ruby       | Python, TypeScript, Go | Similar expressiveness, modern ecosystem                      |
| Python 2   | Python 3               | Direct upgrade path with 2to3 tooling                         |
| JavaScript | TypeScript             | Type safety while maintaining ecosystem                       |
| C#         | Go, Rust, TypeScript   | Go: Cloud-native, Rust: Systems, TS: Web                      |
| Perl       | Python, Go             | Modern alternatives with better tooling                       |

## Framework Migration Paths

### Web Frameworks

| Source             | Target Options                    | Best For                                                 |
| ------------------ | --------------------------------- | -------------------------------------------------------- |
| Spring Boot (Java) | FastAPI (Py), NestJS (TS), Go+Gin | FastAPI: API-first, NestJS: Enterprise, Go: Performance  |
| Django (Python)    | FastAPI, Django 5.x               | FastAPI: Microservices, Django 5: Monolith modernization |
| Rails (Ruby)       | FastAPI, NestJS, Laravel          | Based on team expertise and ecosystem needs              |
| Express (JS)       | Fastify, NestJS, Hono             | Fastify: Performance, NestJS: Structure, Hono: Edge      |
| Laravel (PHP)      | FastAPI, NestJS, Symfony 7        | Modern PHP or complete language shift                    |
| ASP.NET            | FastAPI, Go+Fiber, NestJS         | Cloud-native focus determines choice                     |

### ORM/Data Layer

| Source               | Target Options               |
| -------------------- | ---------------------------- |
| Hibernate (Java)     | SQLAlchemy 2.0, Prisma, GORM |
| ActiveRecord (Rails) | SQLAlchemy, Drizzle, Prisma  |
| Entity Framework     | SQLAlchemy, Prisma, TypeORM  |
| Sequelize            | Prisma, Drizzle, TypeORM     |

## Architecture Patterns

### Monolith to Modern

| Current State    | Recommended Pattern               |
| ---------------- | --------------------------------- |
| Big Ball of Mud  | Clean Architecture (layered)      |
| Layered Monolith | Modular Monolith or Microservices |
| N-tier           | Hexagonal/Ports-Adapters          |
| SOA              | Microservices with Event Sourcing |

### Clean Architecture Template

```
src/
├── domain/           # Business entities, value objects
├── application/      # Use cases, DTOs, interfaces
├── infrastructure/   # Database, external services, frameworks
└── presentation/     # Controllers, views, API handlers
```

### Hexagonal Template

```
src/
├── core/
│   ├── domain/       # Entities, domain logic
│   └── ports/        # Interfaces (in/out)
├── adapters/
│   ├── inbound/      # HTTP, gRPC, CLI
│   └── outbound/     # Database, messaging, external APIs
└── config/           # Dependency injection, configuration
```

## Technology Decision Factors

When presenting options via AskUserQuestion, evaluate:

1. **Team Expertise** - Existing skills reduce learning curve
2. **Ecosystem Maturity** - Library availability, community support
3. **Performance Requirements** - Throughput, latency needs
4. **Deployment Target** - Cloud provider, containerization, serverless
5. **Maintenance Burden** - Long-term support, upgrade paths
6. **Hiring Market** - Developer availability

## Web Search Queries for Updates

```
# For framework recommendations
"{source_framework} to {target_framework} migration guide 2025"
"{target_language} web framework comparison 2025 performance security"

# For best practices
"{target_language} clean architecture best practices 2025"
"microservices {target_language} patterns 2025"

# For security
"{target_framework} security best practices OWASP 2025"
"dependency vulnerability scanning {target_language} 2025"
```

## AskUserQuestion Templates

### Language Selection

```json
{
  "question": "Based on analysis of your {source_lang} codebase, which target language?",
  "header": "Language",
  "options": [
    { "label": "{recommended} (Recommended)", "description": "{reason}" },
    { "label": "{alternative_1}", "description": "{reason_1}" },
    { "label": "{alternative_2}", "description": "{reason_2}" }
  ],
  "multiSelect": false
}
```

### Framework Selection

```json
{
  "question": "Which {target_lang} framework for your {app_type} application?",
  "header": "Framework",
  "options": [
    { "label": "{best_fit} (Recommended)", "description": "{fit_reason}" },
    {
      "label": "{enterprise}",
      "description": "Enterprise-grade, batteries included"
    },
    { "label": "{lightweight}", "description": "Minimal, flexible, fast" }
  ],
  "multiSelect": false
}
```

### Architecture Selection

```json
{
  "question": "What architecture pattern for the new codebase?",
  "header": "Architecture",
  "options": [
    {
      "label": "Clean Architecture (Recommended)",
      "description": "Layered, testable, maintainable"
    },
    {
      "label": "Hexagonal/Ports-Adapters",
      "description": "Domain-centric, pluggable"
    },
    {
      "label": "Microservices",
      "description": "Distributed, independently deployable"
    },
    {
      "label": "Modular Monolith",
      "description": "Organized monolith, future-ready"
    }
  ],
  "multiSelect": false
}
```
