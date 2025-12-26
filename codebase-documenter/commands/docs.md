# /docs Command

Generate comprehensive documentation for the current codebase.

## Usage

```
/docs [options]
```

## Options

- `--full` - Generate all 7 documents (default)
- `--readme` - Generate README.md only
- `--api` - Generate API.md only
- `--quick` - Quick mode with fewer agents (faster)
- `--output <dir>` - Output directory (default: ./docs)

## What This Does

1. **Analyzes your codebase** using 5 parallel agents:
   - Project structure mapping
   - Tech stack detection
   - API endpoint extraction
   - Architecture analysis
   - Configuration scanning

2. **Generates documentation** using 6 parallel agents:
   - README.md - Project overview and quick start
   - CONTRIBUTING.md - Contributor guide
   - ARCHITECTURE.md - System design with Mermaid diagrams
   - API.md - API reference
   - DEPLOYMENT.md - Deployment guide
   - CHANGELOG.md + TROUBLESHOOTING.md

3. **Validates and cross-references** all generated documents

## Examples

```bash
# Generate full documentation suite
/docs

# Quick README generation only
/docs --readme

# Generate to custom directory
/docs --output ./documentation

# Fast mode with fewer parallel agents
/docs --quick
```

## Output

Documents are created in `./docs/` directory:

```
docs/
├── README.md
├── CONTRIBUTING.md
├── ARCHITECTURE.md
├── API.md
├── DEPLOYMENT.md
├── CHANGELOG.md
└── TROUBLESHOOTING.md
```

## Workflow

```mermaid
graph LR
    A[/docs] --> B[Analyze Codebase]
    B --> C[Generate Docs]
    C --> D[Validate Links]
    D --> E[Output Report]
```

## Notes

- Documents include `[ASSUMPTION]` markers for inferred information
- Documents include `[NEEDS INPUT]` markers for missing data
- All Mermaid diagrams are GitHub/GitLab compatible
- Follow Google Developer Documentation Style Guide
