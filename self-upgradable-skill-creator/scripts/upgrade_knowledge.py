#!/usr/bin/env python3
"""
Upgrade Knowledge - Fetches latest Claude Code documentation and updates references.

This script is designed to be used by Claude to refresh its knowledge about:
- Agent Skills (SKILL.md format, progressive disclosure)
- Slash Commands (syntax, frontmatter, arguments)
- Agents/Subagents (configuration, built-in types)
- Hooks (events, configuration)
- MCP Integration (servers, tools)

Usage:
    python3 scripts/upgrade_knowledge.py [--output-dir <path>]

The script outputs instructions for Claude to:
1. Use claude-code-guide agent or WebSearch
2. Gather latest documentation
3. Update reference files
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Documentation sources and topics to fetch
KNOWLEDGE_TOPICS = {
    "skills": {
        "title": "Agent Skills",
        "queries": [
            "Claude Code skills SKILL.md format frontmatter",
            "Claude Code skills bundled resources scripts references assets",
            "Claude Code skills progressive disclosure pattern",
            "Claude Code skills best practices 2025"
        ],
        "output_file": "latest_features.md"
    },
    "slash_commands": {
        "title": "Slash Commands",
        "queries": [
            "Claude Code slash commands syntax",
            "Claude Code custom commands frontmatter",
            "Claude Code command arguments $ARGUMENTS"
        ],
        "output_file": "latest_features.md"
    },
    "agents": {
        "title": "Agents/Subagents",
        "queries": [
            "Claude Code subagents configuration",
            "Claude Code built-in agents explore plan",
            "Claude Code custom agents tools model"
        ],
        "output_file": "latest_features.md"
    },
    "hooks": {
        "title": "Hooks",
        "queries": [
            "Claude Code hooks PreToolUse PostToolUse",
            "Claude Code hooks configuration settings.json",
            "Claude Code hooks security best practices"
        ],
        "output_file": "hooks_integration.md"
    },
    "mcp": {
        "title": "MCP Integration",
        "queries": [
            "Claude Code MCP servers installation",
            "Claude Code MCP tools resources prompts",
            "Claude Code MCP configuration scopes"
        ],
        "output_file": "latest_features.md"
    }
}


def generate_upgrade_instructions(output_dir: Path = None) -> str:
    """Generate instructions for Claude to upgrade knowledge."""

    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "references"

    instructions = f"""
# Knowledge Upgrade Instructions

Generated: {datetime.now().isoformat()}
Output Directory: {output_dir}

## Step 1: Fetch Latest Documentation

Use the Task tool with subagent_type='claude-code-guide' to get comprehensive information on:

### Topics to Research:
"""

    for topic_id, topic in KNOWLEDGE_TOPICS.items():
        instructions += f"\n### {topic['title']}\n"
        instructions += "Search queries:\n"
        for query in topic['queries']:
            instructions += f"- {query}\n"

    instructions += """

## Step 2: Update Reference Files

After gathering documentation, update these files:

### references/latest_features.md
- Skills: SKILL.md format, frontmatter, bundled resources
- Slash Commands: syntax, parameters, examples
- Agents: configuration, built-in types, custom agents
- MCP: servers, tools, configuration

### references/hooks_integration.md
- Hook events (PreToolUse, PostToolUse, etc.)
- Configuration format
- Security best practices
- Skill integration patterns

### references/skill_patterns.md
- Workflow-based pattern
- Task-based pattern
- Reference/guidelines pattern
- Capabilities-based pattern

## Step 3: Verify Updates

Ensure all reference files:
- Are under 200 lines each
- Use imperative writing style
- Include practical examples
- Reference official documentation sources

## Automation Note

This script provides upgrade instructions. Claude should:
1. Read these instructions
2. Use claude-code-guide agent or WebSearch
3. Update reference files with latest info
4. Mark upgrade complete with timestamp
"""

    return instructions


def create_upgrade_manifest(output_dir: Path) -> dict:
    """Create a manifest tracking upgrade status."""
    manifest = {
        "last_upgrade": None,
        "topics_updated": [],
        "version": "1.0.0",
        "output_directory": str(output_dir)
    }
    return manifest


def main():
    output_dir = Path(__file__).parent.parent / "references"

    if len(sys.argv) > 2 and sys.argv[1] == "--output-dir":
        output_dir = Path(sys.argv[2])

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate and print upgrade instructions
    instructions = generate_upgrade_instructions(output_dir)
    print(instructions)

    # Create/update manifest
    manifest_path = output_dir / ".upgrade_manifest.json"
    manifest = create_upgrade_manifest(output_dir)

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n✅ Upgrade manifest created at: {manifest_path}")
    print("\n📌 Next: Use claude-code-guide agent to fetch latest documentation")

    return 0


if __name__ == "__main__":
    sys.exit(main())
