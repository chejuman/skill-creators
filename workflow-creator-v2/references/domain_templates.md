# Domain-Specific Templates

Templates for each supported domain.

## DevOps

### SKILL.md Template

```yaml
---
name: devops-{task}
description: {task} automation for CI/CD pipelines and infrastructure. Use when deploying, configuring, or managing infrastructure.
allowed-tools: Bash(docker:*), Bash(kubectl:*), Bash(terraform:*), Read, Write
---

# DevOps: {Task}

## Workflow
1. Validate configuration
2. Run pre-checks
3. Execute {task}
4. Verify success
5. Rollback on failure

## Scripts
- `scripts/deploy.sh` - Main deployment
- `scripts/rollback.sh` - Automated rollback
- `scripts/validate.py` - Configuration validation
```

### Script Template

```bash
#!/bin/bash
set -euo pipefail

# DevOps automation script
ENVIRONMENT="${1:-staging}"
VERSION="${2:-latest}"

echo "🚀 Deploying version $VERSION to $ENVIRONMENT"

# Pre-checks
kubectl cluster-info || { echo "❌ Cluster not accessible"; exit 1; }

# Deploy
kubectl apply -f manifests/ --namespace="$ENVIRONMENT"

# Verify
kubectl rollout status deployment/app --namespace="$ENVIRONMENT" --timeout=300s

echo "✅ Deployment successful"
```

## Security

### SKILL.md Template

```yaml
---
name: security-{scan-type}
description: {scan-type} security scanning and vulnerability detection. Use when auditing code, scanning dependencies, or checking compliance.
allowed-tools: Bash(snyk:*), Bash(trivy:*), Bash(semgrep:*), Read, Grep
---

# Security: {Scan Type}

## Scan Types
| Type | Tool | Purpose |
|------|------|---------|
| SAST | Semgrep | Static code analysis |
| SCA | Snyk | Dependency scanning |
| Container | Trivy | Image vulnerabilities |

## Workflow
1. Run {scan-type} scan
2. Parse results
3. Categorize by severity
4. Generate report
5. Suggest remediation

## Scripts
- `scripts/scan.py` - Run security scan
- `scripts/report.py` - Generate HTML report
```

### Script Template

```python
#!/usr/bin/env python3
"""Security scanner wrapper."""

import subprocess
import json
import sys

def run_scan(target: str, scan_type: str = "sast") -> dict:
    """Run security scan based on type."""
    scanners = {
        "sast": ["semgrep", "--config", "auto", "--json", target],
        "sca": ["snyk", "test", "--json"],
        "container": ["trivy", "image", "--format", "json", target]
    }

    cmd = scanners.get(scan_type)
    if not cmd:
        return {"error": f"Unknown scan type: {scan_type}"}

    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.stdout else {"raw": result.stderr}

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(run_scan(target), indent=2))
```

## WebDev

### SKILL.md Template

```yaml
---
name: webdev-{component-type}
description: Generate {component-type} components with best practices. Use when creating React/Vue/Next.js components, pages, or API routes.
allowed-tools: Read, Write, Bash(npm:*), Bash(npx:*)
---

# WebDev: {Component Type}

## Supported Frameworks
- React + TypeScript
- Next.js (App Router)
- Vue 3 + Composition API

## Generation Steps
1. Analyze existing patterns in codebase
2. Generate component with proper typing
3. Add tests
4. Update barrel exports

## Templates
- `assets/component.tsx.template`
- `assets/component.test.tsx.template`
- `assets/hook.ts.template`
```

### Component Template

```typescript
// {ComponentName}.tsx
import { FC } from 'react';
import styles from './{ComponentName}.module.css';

interface {ComponentName}Props {
  /** Primary content */
  children?: React.ReactNode;
  /** Optional class name */
  className?: string;
}

export const {ComponentName}: FC<{ComponentName}Props> = ({
  children,
  className,
}) => {
  return (
    <div className={`${styles.container} ${className || ''}`}>
      {children}
    </div>
  );
};

export default {ComponentName};
```

## DataOps

### SKILL.md Template

```yaml
---
name: dataops-{pipeline-type}
description: {pipeline-type} data pipeline automation. Use when building ETL, data transformation, or analytics pipelines.
allowed-tools: Bash(python:*), Read, Write, Bash(dbt:*)
---

# DataOps: {Pipeline Type}

## Pipeline Stages
1. Extract - Load source data
2. Transform - Apply business logic
3. Load - Write to destination
4. Validate - Check data quality

## Scripts
- `scripts/extract.py` - Data extraction
- `scripts/transform.py` - Transformation logic
- `scripts/validate.py` - Data quality checks
```

### Script Template

```python
#!/usr/bin/env python3
"""ETL pipeline stage."""

import pandas as pd
from pathlib import Path

def extract(source: str) -> pd.DataFrame:
    """Extract data from source."""
    return pd.read_csv(source)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Apply transformations."""
    # Add transformations here
    return df.dropna()

def load(df: pd.DataFrame, destination: str):
    """Load data to destination."""
    df.to_parquet(destination, index=False)

def validate(df: pd.DataFrame) -> bool:
    """Validate data quality."""
    checks = [
        len(df) > 0,
        df.duplicated().sum() == 0,
    ]
    return all(checks)

if __name__ == "__main__":
    df = extract("input.csv")
    df = transform(df)
    if validate(df):
        load(df, "output.parquet")
```

## Documentation

### SKILL.md Template

```yaml
---
name: doc-{doc-type}
description: Generate {doc-type} documentation automatically. Use when updating README, API docs, changelogs, or technical documentation.
allowed-tools: Read, Write, Bash(typedoc:*), Bash(jsdoc:*)
---

# Documentation: {Doc Type}

## Documentation Types
| Type | Tool | Output |
|------|------|--------|
| API | TypeDoc | HTML/Markdown |
| Changelog | git-cliff | CHANGELOG.md |
| README | Custom | README.md |

## Workflow
1. Extract code comments/signatures
2. Generate documentation
3. Update index/TOC
4. Validate links
```

### Script Template

```python
#!/usr/bin/env python3
"""Documentation generator."""

import ast
import sys
from pathlib import Path

def extract_docstrings(file_path: str) -> list[dict]:
    """Extract docstrings from Python file."""
    with open(file_path) as f:
        tree = ast.parse(f.read())

    docs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            docstring = ast.get_docstring(node)
            if docstring:
                docs.append({
                    "name": node.name,
                    "type": type(node).__name__,
                    "docstring": docstring
                })
    return docs

def generate_markdown(docs: list[dict]) -> str:
    """Generate markdown from docstrings."""
    lines = ["# API Reference\n"]
    for doc in docs:
        lines.append(f"## {doc['name']}\n")
        lines.append(f"*{doc['type']}*\n")
        lines.append(f"{doc['docstring']}\n")
    return "\n".join(lines)

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "main.py"
    docs = extract_docstrings(file_path)
    print(generate_markdown(docs))
```

## Testing

### SKILL.md Template

```yaml
---
name: test-{test-type}
description: {test-type} test automation and coverage reporting. Use when writing tests, running test suites, or analyzing coverage.
allowed-tools: Bash(npm test:*), Bash(pytest:*), Bash(vitest:*), Read, Write
---

# Testing: {Test Type}

## Test Types
| Type | Framework | Purpose |
|------|-----------|---------|
| Unit | Jest/Vitest | Function testing |
| Integration | Supertest | API testing |
| E2E | Playwright | Browser testing |

## Workflow
1. Analyze code for testable units
2. Generate test file
3. Run tests
4. Report coverage
```

### Test Template

```typescript
// {ComponentName}.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { {ComponentName} } from './{ComponentName}';

describe('{ComponentName}', () => {
  it('renders without crashing', () => {
    render(<{ComponentName} />);
    expect(screen.getByRole('...'));
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    render(<{ComponentName} />);
    await user.click(screen.getByRole('button'));
    expect(screen.getByText('...')).toBeInTheDocument();
  });
});
```
