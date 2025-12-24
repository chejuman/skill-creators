# Agent Prompts for Codebase Analysis

## Codebase Analyzer Agents

Use these prompts with `Task(subagent_type='Explore', ...)` for parallel analysis.

### Agent 1: Language & Framework Detection

```
Analyze languages and frameworks in this codebase:

1. Identify primary programming language(s)
2. Find framework versions from:
   - package.json (Node.js)
   - requirements.txt / pyproject.toml (Python)
   - go.mod (Go)
   - pubspec.yaml (Flutter)
3. List major dependencies with versions
4. Note any deprecated or outdated packages

Output format:
- Primary: [language] [version]
- Framework: [name] [version]
- Key deps: [list]
```

### Agent 2: Architecture Pattern Detection

```
Identify architectural patterns in this codebase:

1. Folder structure analysis:
   - src/ structure
   - Feature vs layer organization
   - Shared/common patterns
2. Pattern identification:
   - MVC, Clean Architecture, Hexagonal
   - Microservices vs Monolith
   - Module boundaries
3. Dependency injection usage
4. Configuration management

Output: Pattern name with evidence from folder structure.
```

### Agent 3: Library Usage Patterns

```
Find key libraries and their usage patterns:

1. State management (Redux, Zustand, MobX, Context)
2. API/HTTP clients (axios, fetch, React Query)
3. Routing solutions
4. Testing frameworks (Jest, Vitest, pytest)
5. Styling (Tailwind, CSS Modules, styled-components)
6. Form handling
7. Validation libraries

For each: Note version and 1-2 usage examples with file paths.
```

### Agent 4: Coding Patterns

```
Discover coding patterns and conventions:

1. Error handling:
   - try/catch patterns
   - Error boundary usage
   - Logging approaches
2. Async patterns:
   - Promises vs async/await
   - Concurrent operations
3. Type usage:
   - TypeScript strictness
   - Type definitions location
4. Naming conventions:
   - Files, functions, variables
   - Constants and enums

Provide examples with file:line references.
```

### Agent 5: Data Flow Mapping

```
Map data flow through the application:

1. API endpoints:
   - REST vs GraphQL
   - Request/response patterns
2. Database interactions:
   - ORM usage
   - Query patterns
3. State management flow:
   - Global vs local state
   - Data synchronization
4. Component hierarchy:
   - Container vs presentational
   - Prop drilling vs context

Create a high-level data flow diagram description.
```

## Usage Example

```python
# Launch all 5 agents in parallel
agents = [
    ("Analyze languages/frameworks", "Agent 1 prompt"),
    ("Detect architecture", "Agent 2 prompt"),
    ("Catalog libraries", "Agent 3 prompt"),
    ("Find coding patterns", "Agent 4 prompt"),
    ("Map data flow", "Agent 5 prompt"),
]

for desc, prompt in agents:
    Task(
        subagent_type='Explore',
        prompt=prompt,
        description=desc,
        model='haiku',
        run_in_background=True
    )

# Collect results after all complete
```

## Result Synthesis

After collecting all agent results, synthesize into:

1. **Tech Stack Summary**: Languages + frameworks + key libs
2. **Architecture Overview**: Pattern + structure + boundaries
3. **Learning Priorities**: What's most important to understand
4. **Curriculum Suggestions**: Ordered topics based on dependencies
