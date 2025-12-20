#!/usr/bin/env python3
"""
Quick validation script for skills.

Usage:
    python3 quick_validate.py <skill-directory>
"""

import sys
import re
from pathlib import Path


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Validate a skill directory."""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()

    # Check frontmatter exists
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    fm = match.group(1)

    # Check required fields
    if 'name:' not in fm:
        return False, "Missing 'name' in frontmatter"
    if 'description:' not in fm:
        return False, "Missing 'description' in frontmatter"

    # Validate name format
    name_match = re.search(r'name:\s*(.+)', fm)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' must be hyphen-case"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' has invalid hyphens"

    # Validate description
    desc_match = re.search(r'description:\s*(.+)', fm)
    if desc_match:
        desc = desc_match.group(1).strip()
        if '<' in desc or '>' in desc:
            return False, "Description cannot contain angle brackets"
        if 'TODO' in desc or '[TODO' in desc:
            return False, "Description has TODO placeholder"

    # Check line count
    lines = len(content.splitlines())
    if lines > 200:
        return False, f"SKILL.md has {lines} lines (max 200)"

    return True, "Skill is valid!"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 quick_validate.py <skill-directory>")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()

    if not skill_path.exists():
        print(f"❌ Path not found: {skill_path}")
        sys.exit(1)

    valid, message = validate_skill(skill_path)

    if valid:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
