# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a **skill development workspace** for creating new Claude Code skills. It is NOT a skill itself - it's a workspace where new skills are developed, tested, and packaged before installation to `~/.claude/skills/`.

**Purpose:**
- Develop new Claude Code skills using the skill-creator workflow
- Test and iterate on skills before distribution
- Package completed skills for installation

**Critical:** All completed skills MUST be installed to `~/.claude/skills/` to be usable by Claude Code. This workspace is only for development.

## Skill Development Workflow

Follow this complete workflow when creating a new skill:

### 1. Initialize New Skill

```bash
# Create new skill from template
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <skill-name> --path .

# Example:
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py my-api-helper --path .
```

This creates:
- `<skill-name>/SKILL.md` with frontmatter and TODO placeholders
- `<skill-name>/scripts/example.py` (executable code)
- `<skill-name>/references/api_reference.md` (documentation)
- `<skill-name>/assets/example_asset.txt` (output templates/files)

**Naming requirements:**
- Hyphen-case only (e.g., `data-analyzer`)
- Lowercase letters, digits, hyphens only
- Max 40 characters
- No leading/trailing hyphens, no consecutive hyphens

### 2. Develop Skill Contents

**Order of development:**
1. Create/modify bundled resources first (`scripts/`, `references/`, `assets/`)
2. Delete unused example files
3. Update SKILL.md with clear instructions and references to resources

**SKILL.md requirements:**
- YAML frontmatter with `name` and `description` (required)
- Description must explain WHAT the skill does and WHEN to use it
- Under 200 lines total
- Use imperative/infinitive form (e.g., "To rotate PDF, use..." not "You should...")
- Each script/reference file also under 200 lines (split if needed)

**Resource types:**
- `scripts/` - Executable code (Python/Bash) for deterministic tasks
- `references/` - Documentation loaded into context as needed
- `assets/` - Files used in output (templates, images, fonts, boilerplate)

### 3. Validate Skill

```bash
# Quick validation check
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py ./<skill-name>
```

Validates:
- SKILL.md exists with proper YAML frontmatter
- Required fields: `name`, `description`
- Naming conventions (hyphen-case)
- No angle brackets in description

### 4. Package Skill

```bash
# Package into distributable zip (includes validation)
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./<skill-name> .

# Output: <skill-name>.zip in current directory
```

The packager automatically validates before creating the zip file.

### 5. Install to Claude Code

**CRITICAL STEP:** Skills must be installed to `~/.claude/skills/` to be usable.

```bash
# Extract to Claude Code skills directory
unzip -o <skill-name>.zip -d ~/.claude/skills/

# Make scripts executable (if skill has scripts)
chmod +x ~/.claude/skills/<skill-name>/scripts/*.py
chmod +x ~/.claude/skills/<skill-name>/scripts/*.sh
```

**Verification:**
```bash
# Confirm installation
ls -la ~/.claude/skills/<skill-name>/
```

### 6. Test and Iterate

After installation:
1. Test the skill with real use cases in Claude Code
2. Identify issues or improvements needed
3. Return to this workspace, modify the skill
4. Re-package and re-install (steps 4-5)
5. Repeat until satisfied

## Workspace Structure

```
skill-creators/
├── CLAUDE.md                      # This file - workspace guidance
├── README.md                      # User-facing documentation (optional)
├── <skill-name-1>/                # Skill under development
│   ├── SKILL.md                   # Skill documentation (required)
│   ├── scripts/                   # Executable code (optional)
│   ├── references/                # Reference documentation (optional)
│   └── assets/                    # Output templates/files (optional)
├── <skill-name-2>/                # Another skill under development
└── *.zip                          # Packaged skills ready for installation
```

**Note:** Example skills like `iterm-control/` or `workdir/` are development artifacts and testing examples. They are NOT part of the skill-creator workflow - they're just previous work stored in this workspace.

## Skill-Creator Architecture

### Core Scripts

Located at `~/.claude/skills/skill-creator/scripts/`:

1. **init_skill.py** - Initialize new skill from template
   - Creates skill directory with SKILL.md
   - Generates example files in scripts/, references/, assets/
   - Sets up proper YAML frontmatter structure
   - Usage: `init_skill.py <skill-name> --path <output-dir>`

2. **package_skill.py** - Package skill into distributable zip
   - Validates skill structure automatically
   - Creates <skill-name>.zip with proper directory structure
   - Includes all files from skill directory
   - Usage: `package_skill.py <skill-path> [output-dir]`

3. **quick_validate.py** - Validate skill structure
   - Checks SKILL.md exists
   - Validates YAML frontmatter format
   - Verifies required fields (name, description)
   - Checks naming conventions
   - Usage: `quick_validate.py <skill-directory>`

### Progressive Disclosure Pattern

Skills use three-level loading for context efficiency:

1. **Metadata (name + description)** - Always in context (~100 words)
   - Determines when Claude activates the skill
   - Must be specific about scenarios and triggers

2. **SKILL.md body** - Loaded when skill is triggered (<5k words)
   - Main instructions and workflow guidance
   - References to bundled resources

3. **Bundled resources** - Loaded as needed by Claude
   - scripts/ - May execute without loading to context
   - references/ - Loaded when Claude needs detailed info
   - assets/ - Never loaded, used in output

## Skill Structure Patterns

Choose the pattern that best fits the skill's purpose:

**1. Workflow-Based** (sequential processes)
- Structure: Overview → Workflow Decision Tree → Step 1 → Step 2...
- Example: Document editing with clear sequential steps

**2. Task-Based** (tool collections)
- Structure: Overview → Quick Start → Task Category 1 → Task Category 2...
- Example: PDF operations (merge, split, extract)

**3. Reference/Guidelines** (standards or specs)
- Structure: Overview → Guidelines → Specifications → Usage...
- Example: Brand guidelines, coding standards

**4. Capabilities-Based** (integrated systems)
- Structure: Overview → Core Capabilities → Feature 1 → Feature 2...
- Example: Product management with multiple features

Patterns can be mixed as needed.

## Critical Requirements

### Installation Location
**ALWAYS install completed skills to `~/.claude/skills/`**

This workspace is ONLY for development. Skills are not functional until installed to the proper location.

### SKILL.md Frontmatter
```yaml
---
name: skill-name
description: Clear explanation of what skill does and when to use it. Include specific scenarios, file types, or tasks that trigger it.
---
```

Required fields:
- `name`: Hyphen-case identifier matching directory name
- `description`: Complete, informative explanation with triggering scenarios

### File Size Limits
- SKILL.md: Under 200 lines
- Each script: Under 200 lines (split into multiple files if needed)
- Each reference: Under 200 lines (split into multiple files if needed)

**Why:** Progressive disclosure - keep each piece digestible for context management.

### Writing Style
Use imperative/infinitive form throughout:
- ✅ "To rotate PDF, use the script..."
- ✅ "Extract variables from Mustache templates..."
- ❌ "You should rotate PDFs..."
- ❌ "If you need to extract variables..."

### Script Best Practices
- Prefer Node.js or Python over Bash (Windows compatibility)
- Include `requirements.txt` for Python dependencies
- Create `.env.example` for required environment variables
- Respect `.env` file hierarchy: `process.env` > `.claude/skills/${SKILL}/.env` > `.claude/skills/.env` > `.claude/.env`
- Write tests for all scripts

## Common Workflows

### Creating a New Skill from Scratch

```bash
# 1. Initialize
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py pdf-editor --path .

# 2. Develop skill contents
cd pdf-editor/
# Edit SKILL.md, add scripts, references, assets
# Delete unused example files

# 3. Validate
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py .

# 4. Package
cd ..
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./pdf-editor .

# 5. Install
unzip -o pdf-editor.zip -d ~/.claude/skills/
chmod +x ~/.claude/skills/pdf-editor/scripts/*.py
```

### Updating an Existing Skill

```bash
# 1. Modify skill in workspace
cd <skill-name>/
# Make changes to SKILL.md, scripts, etc.

# 2. Validate
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py .

# 3. Re-package
cd ..
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./<skill-name> .

# 4. Re-install (overwrites previous version)
unzip -o <skill-name>.zip -d ~/.claude/skills/
```

### Testing Script Executability

```bash
# For Python scripts
python3 ~/.claude/skills/<skill-name>/scripts/<script-name>.py

# For Bash scripts
bash ~/.claude/skills/<skill-name>/scripts/<script-name>.sh

# Or if made executable
~/.claude/skills/<skill-name>/scripts/<script-name>.py
```

## Validation Checklist

Before packaging any skill:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] `name` field matches directory name (hyphen-case)
- [ ] `description` explains WHAT and WHEN (no angle brackets)
- [ ] SKILL.md under 200 lines
- [ ] Each script/reference under 200 lines
- [ ] Unused example files deleted
- [ ] Script files are executable (chmod +x)
- [ ] If Python scripts exist, requirements.txt included
- [ ] If environment variables needed, .env.example included
- [ ] SKILL.md uses imperative/infinitive form
- [ ] All bundled resources are referenced in SKILL.md

## Reference Documentation

- **Skill Creator SKILL.md:** `~/.claude/skills/skill-creator/SKILL.md`
- **Agent Skills Spec:** `~/.claude/skills/agent_skills_spec.md`
- **Online Documentation:**
  - [Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills.md)
  - [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview.md)
  - [Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices.md)

## Important Notes

### This Workspace is NOT a Skill
This repository is a development workspace. Do not attempt to install this entire directory as a skill. Only install individual skill directories from within this workspace.

### Always Install to ~/.claude/skills/
Skills developed here are NOT functional until installed to `~/.claude/skills/`. The installation step is mandatory, not optional.

### Existing Directories (iterm-control, workdir, etc.)
These are development artifacts and examples. They demonstrate previous skill development work but are NOT part of the skill-creator workflow. You can reference them as examples or delete them if not needed.

### Package Before Installing
Always run `package_skill.py` before installation. The packager validates the skill structure and ensures proper formatting. Installing an unvalidated skill may cause issues.

### Script Permissions
After installation, ensure scripts are executable. Use `chmod +x` on all `.py` and `.sh` files in the skill's scripts/ directory.
