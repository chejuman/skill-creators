#!/usr/bin/env python3
"""
Self-Upgrade Knowledge Script

Fetches latest Claude Code documentation and updates references.
Uses claude-code-guide subagent pattern for accurate information.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
REFERENCES_DIR = SKILL_DIR / "references"

KNOWLEDGE_TOPICS = {
    "latest_features.md": [
        "Skills format and SKILL.md structure",
        "Slash Commands syntax and frontmatter", 
        "Agents/Subagents configuration",
        "MCP Integration patterns",
    ],
    "hooks_integration.md": [
        "Hook events (PreToolUse, PostToolUse, etc.)",
        "Hook configuration in settings.json",
        "Exit codes and decision output",
    ],
    "skill_patterns.md": [
        "Workflow-based skill pattern",
        "Task-based skill pattern",
        "Progressive disclosure",
    ],
}

def generate_upgrade_prompt() -> str:
    """Generate prompt for claude-code-guide agent."""
    topics = []
    for file, items in KNOWLEDGE_TOPICS.items():
        topics.append(f"\n## {file}")
        for item in items:
            topics.append(f"- {item}")
    return f"Get latest Claude Code info on:{''.join(topics)}"

def check_knowledge_age():
    """Check age of knowledge files."""
    print("\nKnowledge Status:")
    for file in KNOWLEDGE_TOPICS.keys():
        path = REFERENCES_DIR / file
        if path.exists():
            days = (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).days
            status = "🟢" if days < 7 else "🟡" if days < 30 else "🔴"
            print(f"{status} {file}: {days} days old")
        else:
            print(f"❌ {file}: MISSING")

def main():
    if "--check" in sys.argv:
        check_knowledge_age()
    elif "--prompt" in sys.argv:
        print(generate_upgrade_prompt())
    else:
        print("Self-Upgrade Knowledge Script")
        print("=" * 40)
        print("\nUse claude-code-guide agent to upgrade:")
        print(f"\nTask(subagent_type='claude-code-guide', prompt='{generate_upgrade_prompt()[:100]}...')")
        check_knowledge_age()

if __name__ == "__main__":
    main()
