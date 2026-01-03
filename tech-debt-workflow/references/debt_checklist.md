# Technical Debt Checklist

## Categories

- **Complexity**: long functions, deep nesting, unclear branching
- **Duplication**: repeated logic, copy-paste patterns
- **Dead code**: unused functions, stale flags, orphaned files
- **Testing gaps**: missing coverage, flaky tests
- **Dependency risk**: deprecated APIs, outdated libraries
- **Performance**: hot paths, N+1, inefficient loops
- **Design drift**: inconsistent conventions, mixed paradigms

## Common signals

- Files > 500 lines or functions > 80 lines
- Nested conditionals > 4 levels
- Same block appears 3+ times
- TODO/FIXME/HACK clusters in same module
- Tests skipped or disabled
- Warnings from linters or type checkers
