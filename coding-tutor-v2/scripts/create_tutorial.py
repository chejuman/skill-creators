#!/usr/bin/env python3
"""
Create a new tutorial template with YAML frontmatter.

Usage:
    python create_tutorial.py "React Hooks"
    python create_tutorial.py "State Management" --concepts "Zustand,Context,State"
    python create_tutorial.py "API Patterns" --level intermediate
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def get_tutorials_repo_path():
    """Get the tutorials repo path."""
    return Path.home() / "coding-tutor-tutorials"


def get_repo_name():
    """Get current git repository name."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.strip().split('/')[-1]
    except Exception:
        pass
    return "unknown"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    return text.lower().replace(" ", "-").replace("_", "-")


def create_tutorial(topic: str, concepts: str = None, level: str = "intermediate",
                    style: str = "socratic", output_dir: Path = None) -> Path:
    """Create a new tutorial template."""
    if output_dir is None:
        output_dir = get_tutorials_repo_path()
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    date_filename = datetime.now().strftime("%Y-%m-%d")
    date_frontmatter = datetime.now().strftime("%d-%m-%Y")
    slug = slugify(topic)
    filename = f"{date_filename}-{slug}.md"
    filepath = output_dir / filename

    if concepts is None:
        concepts = topic

    repo_name = get_repo_name()

    # Style-specific sections
    style_section = ""
    if style == "socratic":
        style_section = """
## Socratic Exploration

Before we dive in, consider these questions:

1. **[Question about the problem]** What happens when...?
2. **[Question about existing knowledge]** Have you seen this pattern before?
3. **[Question to guide discovery]** What would you expect if...?

Take a moment to think about these. The answers will reveal themselves as we explore.
"""
    elif style == "step-by-step":
        style_section = """
## Step-by-Step Guide

### Step 1: Understanding the Basics
[Detailed explanation of foundational concepts]

### Step 2: Seeing It in Action
[Walkthrough with code examples]

### Step 3: Deeper Understanding
[Advanced concepts building on previous steps]

### Step 4: Putting It Together
[Complete picture with all pieces connected]
"""
    else:  # hands-on
        style_section = """
## Hands-On Exercise

Let's learn by doing. Here's your first task:

### Exercise 1: [Task Name]
**Goal**: [What you'll accomplish]

```
# Your code here
```

**Hints** (only if stuck):
1. [First hint]
2. [Second hint]

### What You Learned
[Explain concepts after the exercise]
"""

    template = f"""---
concepts: [{concepts}]
source_repo: {repo_name}
description: [TODO: One paragraph summary after completing tutorial]
understanding_score: null
last_quizzed: null
prerequisites: []
level: {level}
style: {style}
created: {date_frontmatter}
last_updated: {date_frontmatter}
---

# {topic}

## Why This Matters

[TODO: Connect to learner's goal. Why should they care about {topic}? What problem does it solve in THEIR codebase?]

## The Problem in Your Code

[TODO: Show a real scenario from this codebase where {topic} is relevant]

**Location**: `src/example/file.ts:25-40`

```typescript
// Paste actual code from the repository
```

**The Challenge**: [Explain what's happening and why understanding {topic} helps]
{style_section}
## Key Concepts

[TODO: Build mental models, not just syntax]

### Concept 1: [Name]

**Analogy**: [Real-world comparison]

**In Code**:
```
// Example
```

**Key Insight**: [The "aha" moment]

### Concept 2: [Name]

[Continue pattern...]

## Examples from Your Codebase

### Example 1: [Brief description]

**Location**: `src/components/Example.tsx:10-25`

```typescript
// Actual code from repository
```

**What this demonstrates**: [Explanation of how this code illustrates the concept]

### Example 2: [Brief description]

**Location**: `src/utils/helper.ts:50-65`

```typescript
// Another real example
```

**What this demonstrates**: [Explanation]

## Try It Yourself

**Challenge**: [Specific task they can try in this codebase]

**Where to start**: Look at `src/example/` and try to...

**Success criteria**: You'll know you understand when you can...

## Summary

Key takeaways from this tutorial:

1. **Core concept**: [One sentence summary]
2. **When to use**: [Practical guidance]
3. **Common pitfalls**: [What to avoid]
4. **Connection**: [How this links to their learning journey]

---

## Q&A

[Questions and answers will be added here during learning]

## Quiz History

[Quiz sessions will be recorded here]
"""

    filepath.write_text(template)
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Create a tutorial template")
    parser.add_argument("topic", help="Topic of the tutorial")
    parser.add_argument("--concepts", help="Comma-separated concepts")
    parser.add_argument("--level", choices=["beginner", "intermediate", "advanced"],
                        default="intermediate")
    parser.add_argument("--style", choices=["socratic", "step-by-step", "hands-on"],
                        default="socratic")
    parser.add_argument("--output-dir", help="Output directory")

    args = parser.parse_args()

    try:
        filepath = create_tutorial(
            args.topic, args.concepts, args.level, args.style, args.output_dir
        )
        print(f"Created tutorial: {filepath}")
        print(f"Style: {args.style} | Level: {args.level}")
        print("Edit the file to add content based on codebase analysis.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
