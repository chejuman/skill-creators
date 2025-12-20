---
name: deep-researcher-v2
description: Conduct comprehensive deep research using a hierarchical multi-agent system with HTML visualization. Spawns parallel Research Agents for web search, Analysis Agents for insight extraction, Synthesis Agents for report generation, and Visualization Agent for HTML output. Use when performing in-depth research, competitive analysis, market research, technical investigations, or when user mentions "deep research", "thorough investigation", research levels (1-5), or needs synthesized multi-source reports with visual HTML output.
---

# Deep Researcher v2.0

True hierarchical multi-agent research system with parallel agent execution and HTML visualization.

## Architecture

```
Orchestrator (this skill)
    │
    ├─► Planning Agent ──► Query decomposition & strategy
    │
    ├─► Research Agents (parallel) ──► Web search & extraction
    │       ├── Research Agent #1: Subtopic A
    │       ├── Research Agent #2: Subtopic B
    │       └── Research Agent #3: Subtopic C
    │
    ├─► Analysis Agent ──► Insight scoring & synthesis
    │
    ├─► Synthesis Agent ──► Final report generation (Markdown)
    │
    └─► Visualization Agent ──► HTML report with styling
```

## Research Levels

| Level | Depth | Agents | Sources | Use Case |
|-------|-------|--------|---------|----------|
| 1 | Quick | 1 | 3-5 | Fast fact-checking |
| 2 | Standard | 2 | 5-10 | General research |
| 3 | Thorough | 3 | 10-15 | Business analysis |
| 4 | Deep | 4 | 15-25 | Market research |
| 5 | Exhaustive | 5+ | 25+ | Academic/strategic |

## Execution Workflow

### Step 1: Planning Phase

Spawn Planning Agent to decompose query:

```
Task(
  subagent_type='Plan',
  prompt='Decompose this research query into 3-5 parallel subtasks...',
  description='Decompose research query'
)
```

**Planning Agent Output Format:**
```json
{
  "original_query": "...",
  "subtasks": [
    {"id": 1, "query": "...", "focus": "..."},
    {"id": 2, "query": "...", "focus": "..."}
  ],
  "search_strategy": "...",
  "expected_sources": 10
}
```

### Step 2: Parallel Research Phase

Spawn multiple Research Agents simultaneously using a SINGLE message with multiple Task tool calls:

```
# CRITICAL: All Task calls in ONE message for true parallelism
Task(subagent_type='Explore', prompt='Research subtask 1...', description='Research subtask 1')
Task(subagent_type='Explore', prompt='Research subtask 2...', description='Research subtask 2')
Task(subagent_type='Explore', prompt='Research subtask 3...', description='Research subtask 3')
```

**Research Agent Prompt Template:**
```
You are a specialized Research Agent. Your task:

RESEARCH FOCUS: {subtask.focus}
SEARCH QUERY: {subtask.query}

Instructions:
1. Use WebSearch to find 3-5 high-quality sources
2. Use WebFetch to extract key information from top sources
3. Return findings in this JSON format:

{
  "subtask_id": {id},
  "sources": [
    {
      "url": "...",
      "title": "...",
      "key_findings": ["...", "..."],
      "relevance_score": 0.0-1.0
    }
  ],
  "summary": "...",
  "gaps": ["..."]
}

Focus only on your assigned subtask. Be thorough but efficient.
```

### Step 3: Analysis Phase

Spawn Analysis Agent to process all research results:

```
Task(
  subagent_type='general-purpose',
  prompt='Analyze and synthesize these research findings...',
  description='Analyze research findings'
)
```

**Analysis Agent Tasks:**
- Score relevance (0.0-1.0) for each finding
- Identify contradictions between sources
- Detect information gaps
- Rank findings by importance
- Cross-reference claims

**Analysis Output Format:**
```json
{
  "high_relevance": [...],    // score >= 0.8
  "medium_relevance": [...],  // 0.5 <= score < 0.8
  "low_relevance": [...],     // score < 0.5
  "contradictions": [...],
  "gaps": [...],
  "key_insights": [...]
}
```

### Step 4: Synthesis Phase

Spawn Synthesis Agent to generate final report:

```
Task(
  subagent_type='general-purpose',
  prompt='Generate a comprehensive research report...',
  description='Generate research report'
)
```

**Report Structure:**
```markdown
# Research Report: {query}

**Generated:** {date}
**Sources:** {count} | **Depth:** Level {level}
**Agents Used:** {agent_count}

## Executive Summary
{2-3 paragraph overview}

## Key Findings (Relevance ≥ 0.8)
{Detailed findings with citations}

## Supporting Information (0.5 ≤ Relevance < 0.8)
{Supporting details}

## Contradictions & Conflicts
{Where sources disagree}

## Research Gaps
{What couldn't be found}

## Recommendations
{Actionable next steps}

## Sources
{Full source list with URLs}
```

### Step 5: Visualization Phase

After generating the Markdown report, convert to styled HTML using the Visualization Agent:

```
Task(
  subagent_type='general-purpose',
  prompt='Convert the generated markdown report to HTML...',
  description='Generate HTML visualization'
)
```

**Visualization Agent Prompt Template:**
```
You are a Visualization Agent. Convert the markdown research report to a styled HTML document.

INPUT: {markdown_report_path}
OUTPUT: {html_output_path}

Instructions:
1. Read the markdown report file
2. Use the md_to_html.py script to convert:
   python3 scripts/md_to_html.py "{input_path}" -o "{output_path}"
3. If script fails, generate HTML inline with these elements:
   - Responsive sidebar with table of contents
   - Professional styling with CSS variables
   - Syntax-highlighted code blocks
   - Styled tables with hover effects
   - Mobile-responsive design
4. Return the output file path

The HTML should include:
- Sticky sidebar navigation
- Clean typography with Korean font support
- Professional color scheme (blue primary)
- Print-friendly styles
```

**HTML Output Features:**
- Responsive layout with collapsible sidebar
- Automatic table of contents from headings
- Syntax highlighting for code blocks
- Styled data tables with zebra striping
- Dark/light theme support
- Mobile-first responsive design
- Print stylesheet for PDF export

**Using the Script Directly:**
```bash
# Basic conversion
python3 scripts/md_to_html.py report.md

# With custom output path
python3 scripts/md_to_html.py report.md -o output.html

# With custom title
python3 scripts/md_to_html.py report.md --title "Market Analysis Report"
```

## Orchestration Rules

### Parallel Execution Pattern

To run agents in TRUE parallel, include ALL Task calls in a SINGLE response:

```python
# CORRECT - True parallel execution
message_with_multiple_tools:
  - Task(subtask1)
  - Task(subtask2)
  - Task(subtask3)

# INCORRECT - Sequential execution
message1: Task(subtask1)
message2: Task(subtask2)
message3: Task(subtask3)
```

### Agent Coordination

1. **Planning Agent** runs FIRST (sequential)
2. **Research Agents** run in PARALLEL (same message)
3. **Analysis Agent** runs after ALL research completes
4. **Synthesis Agent** runs after analysis
5. **Visualization Agent** runs LAST (after markdown saved)

### Scaling by Level

| Level | Planning | Research | Analysis | Synthesis | Visualization |
|-------|----------|----------|----------|-----------|---------------|
| 1 | Skip | 1 agent | Inline | Inline | Optional |
| 2 | Skip | 2 agents | 1 agent | Inline | Optional |
| 3 | 1 agent | 3 agents | 1 agent | 1 agent | 1 agent |
| 4 | 1 agent | 4 agents | 1 agent | 1 agent | 1 agent |
| 5 | 1 agent | 5+ agents | 1 agent | 1 agent | 1 agent |

## Tool Usage by Agent Type

| Agent | Tools | Model |
|-------|-------|-------|
| Planning | Glob, Grep, Read | sonnet |
| Research | WebSearch, WebFetch, Grep | haiku (fast) |
| Analysis | Read, Grep | sonnet |
| Synthesis | Read, Write | sonnet |
| Visualization | Read, Bash, Write | haiku |

## Quality Metrics

**Minimum Requirements by Level:**

| Level | Sources | High-Relevance | Agents | HTML Output |
|-------|---------|----------------|--------|-------------|
| 1 | 3 | 1 | 1 | Optional |
| 2 | 5 | 2 | 2 | Optional |
| 3 | 10 | 3 | 4 | Required |
| 4 | 15 | 5 | 5 | Required |
| 5 | 25 | 8 | 6+ | Required |

## Example Execution

**User Request:** "Deep research level 4 on Korean medical AI market with HTML report"

**Orchestrator Actions:**

1. **Parse request** → Level 4, topic: Korean medical AI market, HTML: yes

2. **Spawn Planning Agent:**
```
Task(subagent_type='Plan', prompt='Decompose "Korean medical AI market" into 4 research subtasks...', description='Plan research strategy')
```

3. **Spawn 4 Research Agents in parallel (SINGLE message):**
```
Task(subagent_type='general-purpose', prompt='Research Korean medical AI market size...', description='Research market size', model='haiku')
Task(subagent_type='general-purpose', prompt='Research key Korean medical AI companies...', description='Research key players', model='haiku')
Task(subagent_type='general-purpose', prompt='Research Korean medical AI regulations...', description='Research regulations', model='haiku')
Task(subagent_type='general-purpose', prompt='Research Korean medical AI marketing strategies...', description='Research marketing', model='haiku')
```

4. **Spawn Analysis Agent:**
```
Task(subagent_type='general-purpose', prompt='Analyze findings, score relevance...', description='Analyze findings')
```

5. **Spawn Synthesis Agent:**
```
Task(subagent_type='general-purpose', prompt='Generate comprehensive Level 4 report...', description='Generate report')
```

6. **Save markdown report** using Write tool

7. **Spawn Visualization Agent:**
```
Task(subagent_type='general-purpose', prompt='Convert markdown to HTML using scripts/md_to_html.py...', description='Generate HTML report', model='haiku')
```

8. **Return both files** to user:
   - `report.md` - Markdown source
   - `report.html` - Styled HTML visualization

## Complete Workflow Example

```python
# Full orchestration flow with visualization
async def deep_research_with_visualization(query, level=3):
    # Phase 1: Planning
    plan = await spawn_planning_agent(query, level)

    # Phase 2: Research (parallel)
    research_results = await spawn_research_agents_parallel(plan.subtasks)

    # Phase 3: Analysis
    analysis = await spawn_analysis_agent(research_results)

    # Phase 4: Synthesis
    markdown_path = await spawn_synthesis_agent(analysis, query)

    # Phase 5: Visualization
    html_path = await spawn_visualization_agent(markdown_path)

    return {
        "markdown": markdown_path,
        "html": html_path,
        "sources": len(research_results.sources),
        "agents_used": count_agents(level)
    }
```

## Resources

- [Agent Prompts](references/agent_prompts.md) - Agent prompt templates
- [Scoring Guide](references/scoring_guide.md) - Relevance scoring criteria
- [Report Template](assets/report_template.md) - Markdown output structure
- [MD to HTML Script](scripts/md_to_html.py) - HTML conversion utility

## Trigger Phrases

- "deep research" / "심층 연구"
- "level X research" / "X 레벨 연구"
- "thorough investigation" / "철저한 조사"
- "market research" / "시장 조사"
- "competitive analysis" / "경쟁 분석"
- "with HTML report" / "HTML 보고서로"
- "visualize the report" / "보고서 시각화"
