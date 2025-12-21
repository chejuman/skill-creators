# Requirements Questions Templates

AskUserQuestion templates for gathering skill requirements.

## Core Questions

### Q1: Skill Domain & Purpose

```python
AskUserQuestion(questions=[{
  "question": "What is the primary purpose of this multi-agent skill?",
  "header": "Purpose",
  "options": [
    {"label": "Research/Analysis", "description": "Gather and synthesize information from multiple sources"},
    {"label": "Code/Development", "description": "Code review, testing, refactoring, generation"},
    {"label": "Security/Audit", "description": "Vulnerability scanning, compliance, threat detection"},
    {"label": "Content/Docs", "description": "Documentation, content generation, translation"}
  ],
  "multiSelect": False
}])
```

### Q2: Worker Agent Selection

```python
AskUserQuestion(questions=[{
  "question": "Which worker agents should be included? (Select all that apply)",
  "header": "Workers",
  "options": [
    {"label": "Researcher", "description": "Web search, data gathering, source collection"},
    {"label": "Analyzer", "description": "Data analysis, pattern detection, insights"},
    {"label": "Validator", "description": "Fact-checking, verification, quality assurance"},
    {"label": "Reporter", "description": "Report generation, summarization, visualization"}
  ],
  "multiSelect": True
}])
```

### Q3: Depth Level Configuration

```python
AskUserQuestion(questions=[{
  "question": "What default depth level should the skill use?",
  "header": "Depth",
  "options": [
    {"label": "Level 3 (Recommended)", "description": "Balanced: 3 workers, detailed output"},
    {"label": "Level 1-2 (Quick)", "description": "Fast: 1-2 workers, basic output"},
    {"label": "Level 4-5 (Deep)", "description": "Thorough: 4-5+ workers, comprehensive"}
  ],
  "multiSelect": False
}])
```

### Q4: Output Format

```python
AskUserQuestion(questions=[{
  "question": "What output formats should be supported?",
  "header": "Output",
  "options": [
    {"label": "Markdown + HTML (Recommended)", "description": "Rich reports with styling"},
    {"label": "JSON only", "description": "Structured data for programmatic use"},
    {"label": "All formats", "description": "MD, HTML, and JSON outputs"}
  ],
  "multiSelect": False
}])
```

## Domain-Specific Questions

### Research Skills

```python
AskUserQuestion(questions=[{
  "question": "What research methodology should be used?",
  "header": "Method",
  "options": [
    {"label": "Web Search + Analysis", "description": "Search web, extract insights"},
    {"label": "Academic Research", "description": "Focus on papers, citations"},
    {"label": "Competitive Analysis", "description": "Market, competitor focus"},
    {"label": "Technical Research", "description": "Docs, APIs, specifications"}
  ],
  "multiSelect": False
}])
```

### Security Skills

```python
AskUserQuestion(questions=[{
  "question": "Which security scan types to include?",
  "header": "Scans",
  "options": [
    {"label": "Vulnerability", "description": "CVE detection, known vulnerabilities"},
    {"label": "Secrets", "description": "API keys, passwords, credentials"},
    {"label": "Configuration", "description": "Misconfigurations, hardening"},
    {"label": "Dependencies", "description": "Outdated packages, supply chain"}
  ],
  "multiSelect": True
}])
```

### Code Review Skills

```python
AskUserQuestion(questions=[{
  "question": "Which code review aspects to cover?",
  "header": "Aspects",
  "options": [
    {"label": "Security", "description": "Vulnerabilities, injection, auth issues"},
    {"label": "Performance", "description": "Bottlenecks, optimization opportunities"},
    {"label": "Style", "description": "Conventions, formatting, readability"},
    {"label": "Logic", "description": "Bugs, edge cases, correctness"}
  ],
  "multiSelect": True
}])
```

## Advanced Questions

### Automation Level

```python
AskUserQuestion(questions=[{
  "question": "What level of automation for the skill?",
  "header": "Automation",
  "options": [
    {"label": "Interactive", "description": "Ask for confirmation at each step"},
    {"label": "Semi-auto", "description": "Ask only for critical decisions"},
    {"label": "Fully automated", "description": "Execute without interruption"}
  ],
  "multiSelect": False
}])
```

### Integration Requirements

```python
AskUserQuestion(questions=[{
  "question": "Any external integrations needed?",
  "header": "Integrations",
  "options": [
    {"label": "None", "description": "Standalone skill, no external deps"},
    {"label": "Web APIs", "description": "REST APIs, webhooks"},
    {"label": "MCP Servers", "description": "Database, file system, custom tools"},
    {"label": "CLI Tools", "description": "npm, pip, docker, git, etc."}
  ],
  "multiSelect": True
}])
```

## Question Flow Strategy

### Minimal Flow (3 questions)
1. Purpose → Workers → Output

### Standard Flow (4 questions)
1. Purpose → Workers → Depth → Output

### Comprehensive Flow (6+ questions)
1. Purpose → Workers → Depth → Output → Automation → Integrations

## Best Practices

1. **Start broad, then narrow** - Begin with purpose, refine with specifics
2. **Limit to 4 questions** - AskUserQuestion supports max 4 questions per call
3. **Use multiSelect wisely** - For worker selection, allow multiple
4. **Provide recommended option** - Add "(Recommended)" to default choice
5. **Clear descriptions** - Each option needs context explanation

## Example: Complete Question Sequence

```python
# Question batch 1: Core requirements
AskUserQuestion(questions=[
  {
    "question": "What is the skill's primary purpose?",
    "header": "Purpose",
    "options": [...],
    "multiSelect": False
  },
  {
    "question": "Which worker agents to include?",
    "header": "Workers",
    "options": [...],
    "multiSelect": True
  }
])

# Question batch 2: Configuration
AskUserQuestion(questions=[
  {
    "question": "Default depth level?",
    "header": "Depth",
    "options": [...],
    "multiSelect": False
  },
  {
    "question": "Output formats?",
    "header": "Output",
    "options": [...],
    "multiSelect": False
  }
])
```
