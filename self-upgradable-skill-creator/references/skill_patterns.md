# Skill Structure Patterns

Reference for choosing skill structure. Update via `upgrade_knowledge.py`.

## Pattern Selection Guide

| Pattern | Best For | Key Characteristic |
|---------|----------|-------------------|
| Workflow | Sequential processes | Clear step-by-step flow |
| Task | Tool collections | Multiple independent operations |
| Reference | Standards/specs | Guidelines and rules |
| Capabilities | Integrated systems | Features that work together |

## 1. Workflow-Based Pattern

Best for skills with clear sequential processes.

### Structure

```markdown
# Skill Name

## Overview
Brief description

## Workflow Decision Tree
```
Start
├── Condition A? → Step 1
├── Condition B? → Step 2
└── Default → Step 3
```

## Step 1: [Action Name]
Instructions for step 1

## Step 2: [Action Name]
Instructions for step 2
```

### Example Use Cases

- Document editing (read → validate → edit → save)
- Data processing (input → transform → validate → output)
- Build processes (compile → test → deploy)

## 2. Task-Based Pattern

Best for skills offering multiple independent operations.

### Structure

```markdown
# Skill Name

## Overview
Brief description

## Quick Start
Fastest path to common use

## Task: [Task Name 1]
How to perform task 1

## Task: [Task Name 2]
How to perform task 2

## Scripts Reference
| Script | Purpose |
|--------|---------|
| task1.py | Performs task 1 |
```

### Example Use Cases

- PDF operations (merge, split, extract, fill forms)
- File conversions (image formats, document types)
- Code utilities (format, lint, analyze)

## 3. Reference/Guidelines Pattern

Best for standards, specifications, or rules.

### Structure

```markdown
# Skill Name

## Overview
What these guidelines cover

## Guidelines
Core principles and rules

## Specifications
Detailed requirements

## Usage Examples
How to apply the guidelines
```

### Example Use Cases

- Brand guidelines (colors, typography, voice)
- Coding standards (style, patterns, practices)
- API specifications (endpoints, formats)

## 4. Capabilities-Based Pattern

Best for integrated systems with related features.

### Structure

```markdown
# Skill Name

## Overview
System description

## Core Capabilities

### 1. [Capability Name]
What it does and how to use it

### 2. [Capability Name]
What it does and how to use it

## Integration
How capabilities work together
```

### Example Use Cases

- Product management (planning, tracking, reporting)
- Development environments (editing, debugging, testing)
- Analytics platforms (collection, analysis, visualization)

## Mixing Patterns

Patterns can be combined:

```markdown
# PDF Editor (Task + Workflow)

## Quick Start (Task pattern)
Common operations

## Task: Merge PDFs
Simple merge operation

## Task: Complex Form Fill (Workflow pattern)
### Step 1: Analyze form
### Step 2: Map fields
### Step 3: Fill values
```

## Writing Guidelines

### Use Imperative Form

✅ "To rotate PDF, use the rotate script"
✅ "Extract variables with..."
❌ "You should rotate PDFs"
❌ "If you need to extract..."

### Keep Files Small

- SKILL.md: Under 200 lines
- Each script: Under 200 lines
- Each reference: Under 200 lines
- Split larger content into multiple files

### Reference Resources

```markdown
For details, see [api_reference.md](references/api_reference.md).

Run the script:
\`\`\`bash
python3 scripts/rotate.py input.pdf 90
\`\`\`
```

## Version

Last updated: 2025-01

To refresh: Run `python3 scripts/upgrade_knowledge.py`
