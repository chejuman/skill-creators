#!/usr/bin/env python3
"""
Generate comprehensive analysis report from codebase scan results.
Synthesizes structure, functionality, and issue detection findings.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def count_files_by_extension(path: str) -> dict:
    """Count files grouped by extension."""
    counts = {}
    for root, _, files in os.walk(path):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', 'venv', '.venv']):
            continue
        for f in files:
            ext = Path(f).suffix.lower() or '.noext'
            counts[ext] = counts.get(ext, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def detect_language(file_counts: dict) -> tuple[str, str]:
    """Detect primary language and framework hints."""
    lang_map = {
        '.py': ('Python', 'FastAPI/Django/Flask'),
        '.java': ('Java', 'Spring/Quarkus'),
        '.js': ('JavaScript', 'Express/React/Vue'),
        '.ts': ('TypeScript', 'NestJS/Next.js/Angular'),
        '.go': ('Go', 'Gin/Echo/Fiber'),
        '.rs': ('Rust', 'Actix/Axum/Rocket'),
        '.rb': ('Ruby', 'Rails/Sinatra'),
        '.php': ('PHP', 'Laravel/Symfony'),
        '.cs': ('C#', '.NET/ASP.NET'),
        '.kt': ('Kotlin', 'Spring/Ktor'),
    }
    for ext, (lang, hints) in lang_map.items():
        if ext in file_counts and file_counts[ext] > 0:
            return lang, hints
    return 'Unknown', 'Unknown'


def find_config_files(path: str) -> list[str]:
    """Find configuration and dependency files."""
    configs = []
    config_patterns = [
        'package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml',
        'pom.xml', 'build.gradle', 'Cargo.toml', 'go.mod', 'Gemfile',
        'composer.json', '*.csproj', 'Dockerfile', 'docker-compose.yml',
        '.env.example', 'config.yaml', 'config.json'
    ]
    for root, _, files in os.walk(path):
        if '.git' in root:
            continue
        for f in files:
            if f in config_patterns or any(f.endswith(p.replace('*', '')) for p in config_patterns if '*' in p):
                configs.append(os.path.relpath(os.path.join(root, f), path))
    return configs[:20]  # Limit output


def estimate_complexity(path: str) -> dict:
    """Estimate codebase complexity metrics."""
    total_lines = 0
    total_files = 0
    code_extensions = {'.py', '.java', '.js', '.ts', '.go', '.rs', '.rb', '.php', '.cs', '.kt'}

    for root, _, files in os.walk(path):
        if any(skip in root for skip in ['.git', 'node_modules', '__pycache__', 'venv']):
            continue
        for f in files:
            if Path(f).suffix.lower() in code_extensions:
                total_files += 1
                try:
                    with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as fp:
                        total_lines += sum(1 for _ in fp)
                except:
                    pass

    complexity = 'Simple' if total_lines < 5000 else 'Medium' if total_lines < 20000 else 'Complex' if total_lines < 100000 else 'Enterprise'
    stages = 3 if total_lines < 10000 else 4 if total_lines < 50000 else 5

    return {
        'total_files': total_files,
        'total_lines': total_lines,
        'complexity': complexity,
        'recommended_stages': stages
    }


def generate_report(repo_path: str, output_path: str, agent_findings: dict = None):
    """Generate comprehensive analysis report."""
    file_counts = count_files_by_extension(repo_path)
    language, framework_hints = detect_language(file_counts)
    configs = find_config_files(repo_path)
    complexity = estimate_complexity(repo_path)

    report = f"""# Codebase Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Repository:** {os.path.abspath(repo_path)}

## Executive Summary

| Metric | Value |
|--------|-------|
| Primary Language | {language} |
| Framework Hints | {framework_hints} |
| Total Code Files | {complexity['total_files']} |
| Total Lines | {complexity['total_lines']:,} |
| Complexity Level | {complexity['complexity']} |
| Recommended Stages | {complexity['recommended_stages']} |

## File Distribution

| Extension | Count |
|-----------|-------|
"""
    for ext, count in list(file_counts.items())[:15]:
        report += f"| {ext} | {count} |\n"

    report += f"""
## Configuration Files Detected

```
{chr(10).join(configs) if configs else 'None found'}
```

## Recommended Migration Approach

Based on analysis:
- **Source:** {language} ({framework_hints})
- **Complexity:** {complexity['complexity']} ({complexity['total_lines']:,} lines)
- **Stages:** {complexity['recommended_stages']} implementation phases

### Suggested Stage Breakdown

"""
    stages = complexity['recommended_stages']
    percentages = [25, 50, 75, 90, 100][:stages]
    stage_names = ['Core/Utils/Config', 'Data Layer', 'Business Logic', 'API/Controllers', 'Integration'][:stages]

    for i, (pct, name) in enumerate(zip(percentages, stage_names), 1):
        report += f"- **Stage {i}** ({pct}%): {name}\n"

    if agent_findings:
        report += f"""
## Agent Findings

### Structure Analysis
{agent_findings.get('structure', 'Pending analysis...')}

### Functionality Extraction
{agent_findings.get('functionality', 'Pending analysis...')}

### Issue Detection
{agent_findings.get('issues', 'Pending analysis...')}
"""

    report += """
## Next Steps

1. Review this analysis report
2. Proceed to Technology Selection (Phase 2)
3. Select target language, framework, and architecture
4. Generate detailed architecture design
5. Begin iterative implementation

---
*Generated by legacy-code-reimplementor*
"""

    with open(output_path, 'w') as f:
        f.write(report)

    print(f"Analysis report generated: {output_path}")
    return report


def main():
    parser = argparse.ArgumentParser(description='Generate codebase analysis report')
    parser.add_argument('repo_path', help='Path to repository to analyze')
    parser.add_argument('--output', '-o', default='analysis_report.md', help='Output file path')
    parser.add_argument('--findings', '-f', help='JSON file with agent findings')
    args = parser.parse_args()

    findings = None
    if args.findings and os.path.exists(args.findings):
        with open(args.findings) as f:
            findings = json.load(f)

    generate_report(args.repo_path, args.output, findings)


if __name__ == '__main__':
    main()
