#!/usr/bin/env python3
"""
Analyze codebase structure and generate analysis report.

Usage:
    python analyze_codebase.py
    python analyze_codebase.py --path /path/to/project
    python analyze_codebase.py --output ~/coding-tutor-tutorials/codebase_analysis.md
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_repo_name(path: Path) -> str:
    """Get git repository name."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=path, capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split('/')[-1]
    except Exception:
        pass
    return path.name


def detect_languages(path: Path) -> dict:
    """Detect programming languages used."""
    extensions = {
        '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
        '.tsx': 'TypeScript React', '.jsx': 'JavaScript React',
        '.go': 'Go', '.rs': 'Rust', '.java': 'Java',
        '.rb': 'Ruby', '.php': 'PHP', '.swift': 'Swift',
        '.kt': 'Kotlin', '.dart': 'Dart', '.vue': 'Vue',
    }

    counts = {}
    for ext, lang in extensions.items():
        files = list(path.rglob(f'*{ext}'))
        files = [f for f in files if 'node_modules' not in str(f) and '.git' not in str(f)]
        if files:
            counts[lang] = len(files)

    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def detect_frameworks(path: Path) -> list:
    """Detect frameworks from config files."""
    frameworks = []

    # Check package.json for JS/TS frameworks
    pkg_json = path / 'package.json'
    if pkg_json.exists():
        try:
            pkg = json.loads(pkg_json.read_text())
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

            if 'next' in deps:
                frameworks.append(f"Next.js {deps['next']}")
            if 'react' in deps:
                frameworks.append(f"React {deps['react']}")
            if 'vue' in deps:
                frameworks.append(f"Vue {deps['vue']}")
            if 'express' in deps:
                frameworks.append(f"Express {deps['express']}")
            if 'fastify' in deps:
                frameworks.append(f"Fastify {deps['fastify']}")
        except Exception:
            pass

    # Check requirements.txt for Python frameworks
    req_txt = path / 'requirements.txt'
    if req_txt.exists():
        try:
            content = req_txt.read_text().lower()
            if 'django' in content:
                frameworks.append('Django')
            if 'flask' in content:
                frameworks.append('Flask')
            if 'fastapi' in content:
                frameworks.append('FastAPI')
            if 'pytorch' in content or 'torch' in content:
                frameworks.append('PyTorch')
        except Exception:
            pass

    # Check pyproject.toml
    pyproject = path / 'pyproject.toml'
    if pyproject.exists():
        try:
            content = pyproject.read_text().lower()
            if 'django' in content:
                frameworks.append('Django')
            if 'fastapi' in content:
                frameworks.append('FastAPI')
        except Exception:
            pass

    # Check go.mod
    go_mod = path / 'go.mod'
    if go_mod.exists():
        frameworks.append('Go Modules')

    # Check pubspec.yaml for Flutter
    pubspec = path / 'pubspec.yaml'
    if pubspec.exists():
        frameworks.append('Flutter')

    return list(set(frameworks))


def detect_architecture(path: Path) -> str:
    """Detect architectural pattern based on folder structure."""
    dirs = [d.name for d in path.iterdir() if d.is_dir() and not d.name.startswith('.')]

    if 'app' in dirs and 'components' in dirs:
        return 'Next.js App Router'
    if 'pages' in dirs and 'components' in dirs:
        return 'Next.js Pages Router'
    if 'src' in dirs:
        src_dirs = [d.name for d in (path / 'src').iterdir() if d.is_dir()]
        if 'domain' in src_dirs or 'application' in src_dirs:
            return 'Clean Architecture'
        if 'controllers' in src_dirs and 'models' in src_dirs:
            return 'MVC'
        if 'features' in src_dirs:
            return 'Feature-based'
    if 'lib' in dirs:
        return 'Flutter/Dart'
    if 'cmd' in dirs and 'pkg' in dirs:
        return 'Go Standard Layout'

    return 'Custom'


def generate_analysis(path: Path) -> str:
    """Generate codebase analysis markdown."""
    repo_name = get_repo_name(path)
    languages = detect_languages(path)
    frameworks = detect_frameworks(path)
    architecture = detect_architecture(path)

    date_str = datetime.now().strftime("%d-%m-%Y")

    primary_lang = list(languages.keys())[0] if languages else "Unknown"

    output = f"""---
repo_name: {repo_name}
analyzed_at: {date_str}
primary_language: {primary_lang}
---

# Codebase Analysis: {repo_name}

## Languages Detected
"""

    for lang, count in languages.items():
        output += f"- **{lang}**: {count} files\n"

    output += "\n## Frameworks & Libraries\n"
    if frameworks:
        for fw in frameworks:
            output += f"- {fw}\n"
    else:
        output += "- No major frameworks detected\n"

    output += f"\n## Architecture Pattern\n- {architecture}\n"

    output += """
## Learning Opportunities

Based on this codebase, recommended learning topics:

1. [High Priority] Understanding the {primary} patterns used
2. [Medium] Deep dive into {framework} best practices
3. [Medium] Code organization and architecture patterns
4. [Optional] Testing strategies in this stack

## Next Steps

Run `/teach-me` to start learning based on this analysis.
""".format(primary=primary_lang, framework=frameworks[0] if frameworks else primary_lang)

    return output


def main():
    parser = argparse.ArgumentParser(description="Analyze codebase structure")
    parser.add_argument("--path", default=".", help="Path to analyze")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    path = Path(args.path).resolve()

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        return 1

    analysis = generate_analysis(path)

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(analysis)
        print(f"Analysis saved to: {output_path}")
    else:
        print(analysis)

    return 0


if __name__ == "__main__":
    sys.exit(main())
