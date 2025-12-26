# /reimpl-start

Start a new legacy code reimplementation project.

## Usage

```
/reimpl-start <repo-a-path> [repo-b-path]
```

## Arguments

- `repo-a-path` (required): Path to the original/legacy codebase
- `repo-b-path` (optional): Path for the new implementation (default: `{repo-a}-reimpl`)

## Workflow

This command executes Phases 0-2 of the reimplementation workflow:

### Phase 0: Self-Upgrade

Fetch latest migration best practices:

```
WebSearch(query='code migration best practices 2025')
WebSearch(query='legacy modernization patterns 2025')
```

### Phase 1: Analysis + Feature Extraction

1. Launch 3 parallel Explore agents:
   - Structure analysis (modules, dependencies)
   - Feature extraction (atomic, testable features)
   - Issue detection (security, deprecated, tech debt)

2. Generate feature list using:

   ```bash
   python3 ~/.claude/skills/legacy-code-reimplementor/scripts/extract_features.py {repo-a-path}
   ```

3. Create initial context:
   ```bash
   python3 ~/.claude/skills/legacy-code-reimplementor/scripts/context_manager.py create {repo-a-path} --repo-b {repo-b-path}
   ```

### Phase 2: Technology Selection

Present technology options using AskUserQuestion:

1. Target language selection
2. Framework selection
3. Architecture pattern selection
4. Confirmation of final stack

### Output

After completion, output:

```
## Reimplementation Initialized

- Session: {session_id}
- Features: {count} extracted
- Tech Stack: {language} + {framework} + {architecture}

### Next Step

Run `/reimpl-continue` to start implementing Feature 1.

Context saved to: .reimpl-context.json
```

## Example

```
User: /reimpl-start ./legacy-java-app
```
