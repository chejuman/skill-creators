# Tech Stack

## Languages

| Purpose | Language | Version |
|---------|----------|---------|
| Scripts | Python | 3.x |
| Scripts | Node.js | 18+ |
| Scripts | Bash | - |
| Docs | Markdown | - |

## Frameworks

| Layer | Framework | Version |
|-------|-----------|---------|
| Validation | Python stdlib | - |
| Packaging | zipfile (Python) | - |
| Testing | Manual | - |

## Database

- **Primary**: 없음 (파일 기반)
- **Cache**: 없음
- **Search**: 없음

## Infrastructure

- **Hosting**: Local
- **CI/CD**: 없음
- **Monitoring**: 없음

## Dependencies

### Required
- Python 3.x
- PyYAML (스킬 검증용)

### Optional
- Node.js (Node 기반 스킬 개발 시)

## Conventions

### File Structure
```
skill-creators/
├── CLAUDE.md
├── <skill-name>/
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
└── *.zip
```

### Naming Conventions
- Directories: hyphen-case (예: `pdf-editor`)
- Python files: snake_case (예: `init_skill.py`)
- Markdown files: hyphen-case (예: `api-reference.md`)

### Import Order
1. Standard library
2. Third-party packages
3. Local modules

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| - | 현재 필요 없음 | - |

## Development Setup

```bash
# Installation
pip install pyyaml

# Initialize new skill
python3 ~/.claude/skills/skill-creator/scripts/init_skill.py <name> --path .

# Validate skill
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py ./<skill-name>

# Package skill
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./<skill-name> .

# Install skill
unzip -o <skill-name>.zip -d ~/.claude/skills/
```
