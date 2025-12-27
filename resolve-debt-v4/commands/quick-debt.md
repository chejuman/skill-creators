# Quick Debt Scan

Quick technical debt scan using resolve-debt-v4 at level 1.

## Usage

```
/quick-debt [target]
```

## Workflow

1. Run resolve-debt-v4 at level 1 (quick scan)
2. Focus on critical issues only (security, dependencies)
3. Output summary to console

## Execution

```
Use resolve-debt-v4 skill with:
- level: 1
- format: md
- focus: sec,dep
- cost: false
- autofix: false

Target: {ARGUMENTS} or current directory

Generate concise summary:
- Critical issues count
- Top 3 issues with locations
- Quick fixes available
```

## Output Format

```
## Quick Debt Scan Results

Target: {target}
Scan Time: {duration}ms

### Critical Issues: {count}

1. **{type}**: {description} (`{location}`)
2. **{type}**: {description} (`{location}`)
3. **{type}**: {description} (`{location}`)

### Next Steps
- Run `/resolve-debt-v4 --level 3` for detailed analysis
- Run `/resolve-debt-v4 --cost` for business impact
```
