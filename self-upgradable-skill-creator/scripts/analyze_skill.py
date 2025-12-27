#!/usr/bin/env python3
"""
Skill Analyzer - 4-D Cognitive Engineering Framework
Analyzes existing skills for improvements.
"""

import json
import sys
import re
from pathlib import Path

def parse_frontmatter(content: str) -> dict:
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip()
    return fm

def count_lines(path: Path) -> int:
    return len(path.read_text().splitlines()) if path.exists() else 0

def analyze(skill_path: Path) -> dict:
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {"error": "SKILL.md not found", "score": 0}

    content = skill_md.read_text()
    fm = parse_frontmatter(content)
    issues, recs = [], []

    # Clarity (25%) - description quality, trigger keywords
    clarity = 5
    if not fm.get('name'):
        issues.append("Missing 'name'"); clarity -= 2
    desc = fm.get('description', '')
    if not desc:
        issues.append("Missing 'description'"); clarity -= 2
    else:
        if len(desc) > 100: clarity += 2  # Detailed description
        if len(desc) > 50: clarity += 1
        if "Use when" in desc or "Includes:" in desc: clarity += 1  # Explicit triggers
        if any(k in desc.lower() for k in ['when', 'trigger', '때', '경우']): clarity += 1

    # Specificity (25%) - structure, examples, references
    lines = count_lines(skill_md)
    specificity = 6
    if lines <= 200: specificity += 1
    if lines > 200: issues.append(f"SKILL.md: {lines} lines (>200)")
    refs = skill_path / "references"
    if refs.exists() and list(refs.glob("*.md")): specificity += 1  # Has references
    if "```" in content: specificity += 1  # Has code examples
    if (skill_path / "scripts" / "requirements.txt").exists(): specificity += 1

    # Actionability (25%) - scripts, commands, one-click
    scripts = skill_path / "scripts"
    actionability = 5
    if scripts.exists():
        py_files = list(scripts.glob("*.py"))
        if py_files: actionability += 2
        if len(py_files) >= 3: actionability += 1  # Multiple scripts
    cmds = skill_path / "commands"
    if cmds.exists() and list(cmds.glob("*.md")): actionability += 1  # Slash command
    if "Quick Start" in content or "One-Click" in content: actionability += 1

    # Automation (25%) - interactive patterns
    automation = 3
    if "AskUserQuestion" in content: automation += 2
    else: recs.append("Add AskUserQuestion")
    if "TodoWrite" in content: automation += 2
    else: recs.append("Add TodoWrite")
    if "Task(" in content or "subagent" in content.lower(): automation += 2
    if "Hook" in content or "hook" in content: automation += 1  # Hook integration

    # Cap at 10
    clarity = min(10, clarity)
    specificity = min(10, specificity)
    actionability = min(10, actionability)
    automation = min(10, automation)

    total = (clarity + specificity + actionability + automation) / 4
    grade = "A" if total >= 9 else "B+" if total >= 8.5 else "B" if total >= 7 else "C" if total >= 5 else "D"

    return {
        "name": skill_path.name,
        "scores": {"clarity": clarity, "specificity": specificity,
                   "actionability": actionability, "automation": automation},
        "total": round(total, 1), "grade": grade,
        "issues": issues, "recommendations": recs
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_skill.py <skill-path>"); sys.exit(1)
    
    result = analyze(Path(sys.argv[1]).resolve())
    
    print(f"\n{'='*50}")
    print(f"ANALYSIS: {result.get('name', 'Unknown')}")
    print(f"{'='*50}")
    
    if "error" in result:
        print(f"Error: {result['error']}"); sys.exit(1)
    
    print(f"\n| Dimension     | Score |")
    print(f"|---------------|-------|")
    for k, v in result['scores'].items():
        print(f"| {k:<13} | {v}/10  |")
    print(f"|---------------|-------|")
    print(f"| TOTAL         | {result['total']}/10 ({result['grade']}) |")
    
    if result['issues']:
        print(f"\n## Issues")
        for i in result['issues']: print(f"- 🔴 {i}")
    if result['recommendations']:
        print(f"\n## Recommendations")
        for r in result['recommendations']: print(f"- 💡 {r}")
    
    if "--json" in sys.argv:
        print(f"\n```json\n{json.dumps(result, indent=2)}\n```")

if __name__ == "__main__":
    main()
