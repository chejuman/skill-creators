# Domain Templates

Use these as starting points. Replace placeholders and trim to user needs.
When a workflow needs explicit invocation, add a custom prompt alongside the skill.

## DevOps

### SKILL.md skeleton

```yaml
---
name: devops-<task>
description: <task> automation for CI/CD pipelines and infrastructure. Use when deploying, configuring, or managing infrastructure.
---

# DevOps: <Task>

## Workflow
1. Validate inputs and environment
2. Run pre-flight checks
3. Execute <task>
4. Verify success
5. Roll back on failure
```

### Custom prompt skeleton (optional)

```yaml
---
description: Run <task> in <env> with optional rollback
argument-hint: [ENV=<env>] [VERSION=<version>]
---

Run <task> with $ENV and $VERSION. If failure occurs, execute rollback steps from the skill.
```

### Script ideas
- `scripts/deploy.sh` for deployment
- `scripts/rollback.sh` for rollback
- `scripts/validate.py` for configuration checks

## Security

### SKILL.md skeleton

```yaml
---
name: security-<scan-type>
description: <scan-type> security scanning and vulnerability detection. Use when auditing code, scanning dependencies, or checking compliance.
---

# Security: <Scan Type>

## Workflow
1. Run <scan-type> scan
2. Parse results
3. Categorize severity
4. Generate report
5. Suggest remediation
```

### Custom prompt skeleton (optional)

```yaml
---
description: Run <scan-type> scan and summarize results
argument-hint: [TARGET=<path>] [SEVERITY=high|medium|low]
---

Run <scan-type> against $TARGET and summarize only $SEVERITY and above.
```

### Script ideas
- `scripts/scan.py` wrapper for scanners
- `scripts/report.py` to format results

## WebDev

### SKILL.md skeleton

```yaml
---
name: webdev-<component-type>
description: Generate <component-type> components with best practices. Use when creating components, pages, or API routes.
---

# WebDev: <Component Type>

## Workflow
1. Analyze existing patterns
2. Generate component with typing
3. Add tests or stories
4. Update exports
```

### Custom prompt skeleton (optional)

```yaml
---
description: Generate a <component-type> component
argument-hint: [NAME=<ComponentName>] [PATH=<dir>]
---

Generate <component-type> named $NAME under $PATH. Update exports and tests if applicable.
```

### Asset ideas
- `assets/component.tsx.template`
- `assets/component.test.tsx.template`

## DataOps

### SKILL.md skeleton

```yaml
---
name: dataops-<pipeline-type>
description: <pipeline-type> data pipeline automation. Use when building ETL, data transformation, or analytics pipelines.
---

# DataOps: <Pipeline Type>

## Workflow
1. Extract data
2. Transform
3. Load
4. Validate
```

### Custom prompt skeleton (optional)

```yaml
---
description: Run <pipeline-type> pipeline on a data source
argument-hint: [SOURCE=<path>] [DEST=<path>]
---

Execute pipeline with $SOURCE and write output to $DEST. Validate before writing.
```

### Script ideas
- `scripts/extract.py`
- `scripts/transform.py`
- `scripts/validate.py`

## Documentation

### SKILL.md skeleton

```yaml
---
name: docs-<doc-type>
description: Generate <doc-type> documentation. Use when updating README, API docs, or changelogs.
---

# Documentation: <Doc Type>

## Workflow
1. Extract sources
2. Generate docs
3. Update TOC/index
4. Validate links
```

### Custom prompt skeleton (optional)

```yaml
---
description: Regenerate <doc-type> documentation
argument-hint: [SCOPE=<path>] [FORMAT=md|html]
---

Regenerate <doc-type> documentation from $SCOPE in $FORMAT and update TOC.
```

### Script ideas
- `scripts/extract.py` for docstrings
- `scripts/render.py` for markdown output

## Testing

### SKILL.md skeleton

```yaml
---
name: test-<test-type>
description: <test-type> test automation and coverage reporting. Use when writing tests or running suites.
---

# Testing: <Test Type>

## Workflow
1. Identify test targets
2. Generate tests
3. Run suite
4. Report coverage
```

### Custom prompt skeleton (optional)

```yaml
---
description: Run <test-type> tests and summarize failures
argument-hint: [TARGET=<path>] [FILTER=<pattern>]
---

Run <test-type> tests for $TARGET with $FILTER and summarize failures only.
```

### Asset ideas
- `assets/test.template.tsx`
