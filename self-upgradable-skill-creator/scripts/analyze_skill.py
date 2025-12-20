#!/usr/bin/env python3
"""
Skill Analyzer - Analyzes existing skills and suggests improvements.

Checks:
- SKILL.md format and quality
- Description effectiveness
- Progressive disclosure compliance
- Script quality
- Missing best practices

Usage:
    python3 analyze_skill.py <skill-path>
"""

import sys
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Issue:
    severity: str  # "error", "warning", "suggestion"
    category: str
    message: str
    fix: str = ""


def count_lines(path: Path) -> int:
    """Count lines in a file."""
    if not path.exists():
        return 0
    return len(path.read_text().splitlines())


def analyze_frontmatter(content: str) -> list[Issue]:
    """Analyze YAML frontmatter quality."""
    issues = []

    if not content.startswith('---'):
        issues.append(Issue("error", "format", "Missing YAML frontmatter",
                            "Add frontmatter: ---\\nname: ...\\ndescription: ...\\n---"))
        return issues

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        issues.append(Issue("error", "format", "Invalid frontmatter format"))
        return issues

    fm = match.group(1)

    # Check name
    name_match = re.search(r'name:\s*(.+)', fm)
    if not name_match:
        issues.append(Issue("error", "required", "Missing 'name' field"))
    else:
        name = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            issues.append(Issue("error", "naming", f"Name '{name}' must be hyphen-case"))

    # Check description
    desc_match = re.search(r'description:\s*(.+)', fm)
    if not desc_match:
        issues.append(Issue("error", "required", "Missing 'description' field"))
    else:
        desc = desc_match.group(1).strip()
        if len(desc) < 50:
            issues.append(Issue("warning", "quality",
                                "Description too short (<50 chars)",
                                "Add WHAT the skill does and WHEN to use it"))
        if '<' in desc or '>' in desc:
            issues.append(Issue("error", "format", "Description has angle brackets"))
        if 'TODO' in desc:
            issues.append(Issue("error", "incomplete", "Description has TODO placeholder"))

    return issues


def analyze_content(content: str, skill_path: Path) -> list[Issue]:
    """Analyze SKILL.md content quality."""
    issues = []
    lines = content.splitlines()

    # Check line count
    if len(lines) > 200:
        issues.append(Issue("warning", "size",
                            f"SKILL.md has {len(lines)} lines (>200)",
                            "Move detailed content to references/"))

    # Check for TODOs
    todo_count = content.count('TODO')
    if todo_count > 0:
        issues.append(Issue("warning", "incomplete",
                            f"Found {todo_count} TODO items"))

    # Check writing style
    second_person = len(re.findall(r'\b[Yy]ou should\b', content))
    if second_person > 0:
        issues.append(Issue("suggestion", "style",
                            f"Found {second_person} 'you should' phrases",
                            "Use imperative form: 'To X, do Y'"))

    # Check for resource references
    has_scripts = (skill_path / "scripts").exists()
    has_refs = (skill_path / "references").exists()

    if has_scripts and 'scripts/' not in content:
        issues.append(Issue("suggestion", "completeness",
                            "scripts/ exists but not referenced in SKILL.md"))

    if has_refs and 'references/' not in content:
        issues.append(Issue("suggestion", "completeness",
                            "references/ exists but not referenced in SKILL.md"))

    return issues


def analyze_scripts(skill_path: Path) -> list[Issue]:
    """Analyze script files."""
    issues = []
    scripts_dir = skill_path / "scripts"

    if not scripts_dir.exists():
        return issues

    for script in scripts_dir.glob("*.py"):
        lines = count_lines(script)
        if lines > 200:
            issues.append(Issue("warning", "size",
                                f"{script.name} has {lines} lines (>200)",
                                "Split into multiple files"))

        content = script.read_text()
        if '#!/usr/bin/env python3' not in content:
            issues.append(Issue("suggestion", "quality",
                                f"{script.name} missing shebang"))

    # Check for requirements.txt
    has_imports = False
    for script in scripts_dir.glob("*.py"):
        content = script.read_text()
        if re.search(r'^import (?!sys|os|re|json|pathlib)', content, re.M):
            has_imports = True
            break

    if has_imports and not (skill_path / "requirements.txt").exists():
        issues.append(Issue("suggestion", "completeness",
                            "Scripts have external imports but no requirements.txt"))

    return issues


def analyze_skill(skill_path: Path) -> list[Issue]:
    """Run full analysis on a skill."""
    issues = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append(Issue("error", "required", "SKILL.md not found"))
        return issues

    content = skill_md.read_text()
    issues.extend(analyze_frontmatter(content))
    issues.extend(analyze_content(content, skill_path))
    issues.extend(analyze_scripts(skill_path))

    return issues


def print_report(issues: list[Issue], skill_path: Path):
    """Print analysis report."""
    print(f"\n📊 Skill Analysis: {skill_path.name}")
    print("=" * 50)

    if not issues:
        print("✅ No issues found!")
        return

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    suggestions = [i for i in issues if i.severity == "suggestion"]

    for label, items, icon in [
        ("Errors", errors, "❌"),
        ("Warnings", warnings, "⚠️"),
        ("Suggestions", suggestions, "💡")
    ]:
        if items:
            print(f"\n{icon} {label}:")
            for issue in items:
                print(f"   [{issue.category}] {issue.message}")
                if issue.fix:
                    print(f"      Fix: {issue.fix}")

    print(f"\nSummary: {len(errors)} errors, {len(warnings)} warnings, {len(suggestions)} suggestions")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_skill.py <skill-path>")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    if not skill_path.exists():
        print(f"❌ Path not found: {skill_path}")
        sys.exit(1)

    issues = analyze_skill(skill_path)
    print_report(issues, skill_path)

    errors = [i for i in issues if i.severity == "error"]
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
