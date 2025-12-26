#!/usr/bin/env python3
"""Codebase analyzer for documentation generation.

Analyzes project structure, tech stack, and configuration to support
documentation generation workflow.

Usage:
    python analyze_codebase.py /path/to/project [--output json|text]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


def get_directory_tree(path: Path, max_depth: int = 4, prefix: str = "") -> str:
    """Generate ASCII directory tree."""
    if max_depth == 0:
        return ""

    entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    tree_lines = []

    # Filter out common ignored directories
    ignored = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next"}
    entries = [e for e in entries if e.name not in ignored]

    for i, entry in enumerate(entries[:20]):  # Limit entries
        is_last = i == len(entries[:20]) - 1
        connector = "└── " if is_last else "├── "
        tree_lines.append(f"{prefix}{connector}{entry.name}")

        if entry.is_dir() and max_depth > 1:
            extension = "    " if is_last else "│   "
            subtree = get_directory_tree(entry, max_depth - 1, prefix + extension)
            if subtree:
                tree_lines.append(subtree)

    return "\n".join(tree_lines)


def detect_tech_stack(path: Path) -> dict[str, Any]:
    """Detect technology stack from config files."""
    stack = {"languages": [], "frameworks": [], "databases": [], "dependencies": []}

    # Node.js / JavaScript
    package_json = path / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text())
            stack["languages"].append({"name": "JavaScript/TypeScript", "version": "N/A"})

            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

            # Detect frameworks
            frameworks = {
                "next": "Next.js", "react": "React", "vue": "Vue.js",
                "express": "Express", "fastify": "Fastify", "nestjs": "NestJS",
                "nuxt": "Nuxt.js", "svelte": "Svelte"
            }
            for dep, name in frameworks.items():
                if dep in deps:
                    stack["frameworks"].append({"name": name, "version": deps[dep]})

            # Detect databases
            databases = {
                "prisma": "Prisma", "mongoose": "MongoDB", "pg": "PostgreSQL",
                "mysql2": "MySQL", "redis": "Redis", "typeorm": "TypeORM"
            }
            for dep, name in databases.items():
                if dep in deps:
                    stack["databases"].append({"name": name, "version": deps[dep]})

        except (json.JSONDecodeError, KeyError):
            pass

    # Python
    requirements = path / "requirements.txt"
    pyproject = path / "pyproject.toml"

    if requirements.exists() or pyproject.exists():
        stack["languages"].append({"name": "Python", "version": "3.x"})

        if requirements.exists():
            content = requirements.read_text()
            python_frameworks = {
                "fastapi": "FastAPI", "django": "Django", "flask": "Flask",
                "starlette": "Starlette", "tornado": "Tornado"
            }
            for pkg, name in python_frameworks.items():
                if pkg in content.lower():
                    stack["frameworks"].append({"name": name, "version": "N/A"})

    # Go
    if (path / "go.mod").exists():
        stack["languages"].append({"name": "Go", "version": "N/A"})

    # Rust
    if (path / "Cargo.toml").exists():
        stack["languages"].append({"name": "Rust", "version": "N/A"})

    # Docker
    if (path / "Dockerfile").exists() or (path / "docker-compose.yml").exists():
        stack["dependencies"].append({"name": "Docker", "purpose": "Containerization"})

    return stack


def find_entry_points(path: Path) -> list[dict[str, str]]:
    """Find application entry points."""
    entry_points = []
    entry_patterns = [
        ("main.py", "Python main"), ("app.py", "Flask/Python app"),
        ("server.py", "Python server"), ("index.js", "Node.js entry"),
        ("index.ts", "TypeScript entry"), ("main.go", "Go main"),
        ("main.rs", "Rust main"), ("server.js", "Node.js server"),
        ("app.js", "Express app")
    ]

    for pattern, desc in entry_patterns:
        matches = list(path.rglob(pattern))
        for match in matches[:3]:  # Limit matches
            if "node_modules" not in str(match) and ".git" not in str(match):
                entry_points.append({
                    "file": str(match.relative_to(path)),
                    "type": desc
                })

    return entry_points


def scan_env_variables(path: Path) -> list[dict[str, Any]]:
    """Scan for environment variables."""
    env_vars = []
    env_files = [".env.example", ".env.sample", ".env.template"]

    for env_file in env_files:
        env_path = path / env_file
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key = line.split("=")[0].strip()
                    env_vars.append({
                        "name": key,
                        "required": True,
                        "source": env_file
                    })
            break

    return env_vars


def analyze_codebase(project_path: str) -> dict[str, Any]:
    """Main analysis function."""
    path = Path(project_path).resolve()

    if not path.exists():
        return {"error": f"Path does not exist: {project_path}"}

    if not path.is_dir():
        return {"error": f"Path is not a directory: {project_path}"}

    return {
        "project_name": path.name,
        "project_path": str(path),
        "structure": {
            "tree": get_directory_tree(path),
            "key_directories": [
                d.name for d in path.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ][:10]
        },
        "tech_stack": detect_tech_stack(path),
        "entry_points": find_entry_points(path),
        "environment": scan_env_variables(path),
        "has_tests": (path / "tests").exists() or (path / "test").exists(),
        "has_docs": (path / "docs").exists() or (path / "README.md").exists(),
        "has_ci": (path / ".github" / "workflows").exists() or (path / ".gitlab-ci.yml").exists()
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze codebase for documentation")
    parser.add_argument("path", help="Path to project directory")
    parser.add_argument("--output", choices=["json", "text"], default="json")

    args = parser.parse_args()
    result = analyze_codebase(args.path)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Project: {result.get('project_name', 'Unknown')}")
        print(f"\nStructure:\n{result.get('structure', {}).get('tree', 'N/A')}")
        print(f"\nTech Stack: {result.get('tech_stack', {})}")
        print(f"\nEntry Points: {result.get('entry_points', [])}")


if __name__ == "__main__":
    main()
