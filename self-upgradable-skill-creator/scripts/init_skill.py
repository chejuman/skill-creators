#!/usr/bin/env python3
"""
Enhanced Skill Initializer - Creates new skills with latest Claude Code patterns.

Features:
- Template with latest SKILL.md format
- Support for hooks integration
- MCP-aware structure
- Proper progressive disclosure setup

Usage:
    init_skill.py <skill-name> --path <output-directory> [--pattern <pattern>]

Patterns: workflow, task, reference, capabilities
"""

import sys
import argparse
from pathlib import Path

SKILL_TEMPLATES = {
    "default": """---
name: {skill_name}
description: {description}
---

# {skill_title}

## Overview

{overview}

## Quick Start

{quick_start}

## Usage

{usage}

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `example.py` | Example script (customize or delete) |

## Resources

- [API Reference](references/api_reference.md) - Detailed API documentation
""",

    "workflow": """---
name: {skill_name}
description: {description}
---

# {skill_title}

## Overview

{overview}

## Workflow Decision Tree

```
Start
├── Condition A? → Step 1
├── Condition B? → Step 2
└── Default → Step 3
```

## Step 1: [Action Name]

[Step 1 instructions]

## Step 2: [Action Name]

[Step 2 instructions]

## Step 3: [Action Name]

[Step 3 instructions]

## Resources

- [Workflow Guide](references/workflow_guide.md) - Detailed workflow documentation
""",

    "task": """---
name: {skill_name}
description: {description}
---

# {skill_title}

## Overview

{overview}

## Quick Start

To get started quickly:
```bash
# Example command
python3 scripts/example.py input output
```

## Task: [Task Name 1]

[Task 1 instructions]

## Task: [Task Name 2]

[Task 2 instructions]

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `task1.py` | Performs task 1 |
| `task2.py` | Performs task 2 |
""",

    "reference": """---
name: {skill_name}
description: {description}
---

# {skill_title}

## Overview

{overview}

## Guidelines

[Core guidelines and principles]

## Specifications

[Detailed specifications]

## Usage Examples

[Practical examples]

## Resources

- [Full Reference](references/full_reference.md) - Complete reference documentation
""",

    "capabilities": """---
name: {skill_name}
description: {description}
---

# {skill_title}

## Overview

{overview}

## Core Capabilities

### 1. [Capability Name]

[Capability description and usage]

### 2. [Capability Name]

[Capability description and usage]

### 3. [Capability Name]

[Capability description and usage]

## Integration

[How capabilities work together]
"""
}

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example script for {skill_name}

Replace with actual implementation or delete if not needed.
"""

import sys
from pathlib import Path


def main():
    """Main entry point."""
    print(f"Running {skill_name} example script")
    # TODO: Add implementation
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

EXAMPLE_REFERENCE = """# API Reference for {skill_title}

## Overview

Reference documentation for {skill_name}.

## API Endpoints / Functions

### function_name()

Description of the function.

**Parameters:**
- `param1` (type): Description

**Returns:**
- type: Description

## Examples

```python
# Example usage
result = function_name(param1)
```
"""


def title_case(name: str) -> str:
    """Convert hyphen-case to Title Case."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def validate_name(name: str) -> tuple[bool, str]:
    """Validate skill name format."""
    import re
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Use hyphen-case (lowercase, digits, hyphens)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, "No leading/trailing/consecutive hyphens"
    if len(name) > 40:
        return False, "Max 40 characters"
    return True, "Valid"


def init_skill(name: str, path: str, pattern: str = "default") -> Path:
    """Initialize a new skill directory."""
    valid, msg = validate_name(name)
    if not valid:
        print(f"❌ Invalid name: {msg}")
        return None

    skill_dir = Path(path).resolve() / name

    if skill_dir.exists():
        print(f"❌ Directory exists: {skill_dir}")
        return None

    # Create directory structure
    skill_dir.mkdir(parents=True)
    (skill_dir / "scripts").mkdir()
    (skill_dir / "references").mkdir()
    (skill_dir / "assets").mkdir()

    title = title_case(name)

    # Create SKILL.md from template
    template = SKILL_TEMPLATES.get(pattern, SKILL_TEMPLATES["default"])
    content = template.format(
        skill_name=name,
        skill_title=title,
        description=f"[TODO: Describe what {title} does and when to use it]",
        overview=f"[TODO: 1-2 sentences about {title}]",
        quick_start="[TODO: Quick start instructions]",
        usage="[TODO: Usage instructions]"
    )
    (skill_dir / "SKILL.md").write_text(content)
    print(f"✅ Created SKILL.md ({pattern} pattern)")

    # Create example script
    script = EXAMPLE_SCRIPT.format(skill_name=name)
    script_path = skill_dir / "scripts" / "example.py"
    script_path.write_text(script)
    script_path.chmod(0o755)
    print("✅ Created scripts/example.py")

    # Create example reference
    ref = EXAMPLE_REFERENCE.format(skill_name=name, skill_title=title)
    (skill_dir / "references" / "api_reference.md").write_text(ref)
    print("✅ Created references/api_reference.md")

    print(f"\n✅ Skill '{name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Update SKILL.md TODO items")
    print("2. Add/modify scripts and references")
    print("3. Run: python3 scripts/quick_validate.py " + str(skill_dir))

    return skill_dir


def main():
    parser = argparse.ArgumentParser(description="Initialize a new skill")
    parser.add_argument("name", help="Skill name (hyphen-case)")
    parser.add_argument("--path", required=True, help="Output directory")
    parser.add_argument("--pattern", default="default",
                        choices=["default", "workflow", "task", "reference", "capabilities"],
                        help="Structure pattern")

    args = parser.parse_args()

    print(f"🚀 Initializing skill: {args.name}")
    print(f"   Pattern: {args.pattern}")
    print(f"   Location: {args.path}\n")

    result = init_skill(args.name, args.path, args.pattern)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
