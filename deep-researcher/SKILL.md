---
name: deep-researcher
description: Conduct comprehensive deep research using a hierarchical multi-agent system with query optimization, multi-source synthesis, and relevance scoring. Use when performing in-depth topic research, competitive analysis, technical investigations, academic research, or when user mentions "deep research", "thorough investigation", or needs information from multiple web sources synthesized into a comprehensive report.
---

# Deep Researcher

Hierarchical multi-agent research system inspired by SkyworkAI/DeepResearchAgent for comprehensive topic investigation.

## Architecture

```
Planning Agent (orchestrator)
    ├── Research Agent (web search + content extraction)
    ├── Analysis Agent (insight extraction + scoring)
    └── Synthesis Agent (report generation)
```

## Research Workflow

Track progress with this checklist:

```
Research Progress:
- [ ] Step 1: Understand and decompose research query
- [ ] Step 2: Optimize search queries
- [ ] Step 3: Execute multi-level web searches
- [ ] Step 4: Extract insights with relevance scoring
- [ ] Step 5: Generate follow-up queries for gaps
- [ ] Step 6: Synthesize findings into report
- [ ] Step 7: Verify citations and completeness
```

## Step 1: Query Decomposition (Planning Agent)

Break down complex queries into sub-tasks:

```
Original: "Latest AI Agent frameworks comparison 2025"
Sub-tasks:
1. Search for major AI agent frameworks released in 2025
2. Identify key features and architectures
3. Find performance benchmarks
4. Gather community adoption metrics
5. Compare pricing and licensing
```

Use Task tool with `subagent_type='Explore'` for initial codebase/topic exploration if needed.

## Step 2: Query Optimization

Optimize queries for better search results:

**Optimization Strategies:**
- Add temporal context: "2025", "latest", "recent"
- Include domain specifics: "LLM", "multi-agent", "framework"
- Use Boolean operators for precision
- Add source qualifiers: "official docs", "benchmarks"

**Example:**
```
Original: "AI agents"
Optimized: "AI agent frameworks comparison 2025 LangGraph AutoGen CrewAI"
```

## Step 3: Multi-Level Web Search

Use WebSearch tool for discovery:

```
Level 1: Broad exploration
  Query: "<topic> overview 2025"
  Purpose: Identify key players and concepts

Level 2: Deep dive
  Query: "<specific aspect> technical details"
  Purpose: Gather detailed information

Level 3: Validation
  Query: "<claim> verification benchmark"
  Purpose: Cross-reference findings
```

## Step 4: Insight Extraction with Relevance Scoring

Use WebFetch to extract content, then score insights:

**Relevance Scoring (0.0 - 1.0):**
- 0.9-1.0: Directly answers research question
- 0.7-0.8: Strongly supports or relates to topic
- 0.5-0.6: Provides useful context
- 0.3-0.4: Tangentially related
- 0.0-0.2: Not relevant

**Insight Format:**
```json
{
  "content": "Key finding or fact",
  "source_url": "https://...",
  "source_title": "Source Title",
  "relevance_score": 0.85
}
```

## Step 5: Follow-Up Query Generation

Identify gaps and generate follow-up queries:

**Gap Analysis Questions:**
- What aspects haven't been covered?
- Are there contradictions that need resolution?
- What deeper details are missing?
- What alternative perspectives exist?

**Follow-Up Strategy:**
- Max 3 follow-up queries per research cycle
- Max depth: 2-3 levels (to prevent infinite exploration)
- Time limit: Consider efficiency

## Step 6: Report Synthesis

Structure final report:

```markdown
# Research: [Query]

**Sources:** [count] | **Depth:** [levels explored]

## Key Findings (relevance >= 0.8)
- Finding 1 with [Source](url)
- Finding 2 with [Source](url)

## Supporting Information (0.5 <= relevance < 0.8)
- Supporting detail with [Source](url)

## Supplementary Context (relevance < 0.5)
- Context detail with [Source](url)

## Contradictions & Gaps
- Areas where sources disagree
- Information gaps identified

## Recommendations
- Next steps based on findings
```

## Step 7: Verification Checklist

Before finalizing:
- [ ] All major claims have source citations
- [ ] Source URLs are valid and accessible
- [ ] Contradictions are noted and explained
- [ ] Research gaps are acknowledged
- [ ] Report follows consistent structure

## Multi-Agent Execution Pattern

Use Task tool to spawn specialized agents:

```
# Research Agent
Task(subagent_type='Explore', prompt='Search for [topic] sources...')

# Analysis Agent (parallel execution)
Task(subagent_type='general-purpose', prompt='Analyze and extract insights...')

# Synthesis Agent
Task(subagent_type='general-purpose', prompt='Synthesize findings into report...')
```

For parallel research on multiple subtopics, spawn multiple Explore agents simultaneously.

## Tool Usage Guide

| Task | Tool | Usage |
|------|------|-------|
| Find sources | WebSearch | `query: "<research topic>"` |
| Extract content | WebFetch | `url: "<source>", prompt: "Extract key findings about..."` |
| Code analysis | Bash | For Python calculations or data processing |
| File exploration | Task(Explore) | For codebase research |
| Deep analysis | Task(general-purpose) | For complex multi-step analysis |

## Resources

- [Research Prompts](references/research_prompts.md) - Optimized prompts for research tasks
- [Scoring Guide](references/scoring_guide.md) - Detailed relevance scoring criteria
- [Report Template](assets/report_template.md) - Research report structure

## Quality Metrics

**Research Depth:**
- Minimum 5 unique sources
- At least 2 depth levels
- 3+ high-relevance insights (score >= 0.8)

**Report Quality:**
- All claims cited
- Contradictions addressed
- Gaps acknowledged
- Actionable recommendations included
