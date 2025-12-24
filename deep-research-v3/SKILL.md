---
name: deep-research-v3
description: Hierarchical multi-agent deep research system for market analysis, competitive intelligence, and trend research. Spawns 5+ parallel research agents, synthesizes multi-source findings, generates HTML/Markdown reports with citations. Use when user asks for deep research, market analysis, competitive analysis, or thorough investigation.
---

# Deep Research V3

Hierarchical multi-agent system for comprehensive research with market/competitive analysis focus.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH ORCHESTRATOR                        │
├─────────────────────────────────────────────────────────────────┤
│ Phase 1: Query Analysis ──► Decompose research question         │
│ Phase 2: Parallel Research ──► 5+ specialized agents            │
│ Phase 3: Validation ──► Cross-reference & fact-check            │
│ Phase 4: Synthesis ──► Combine findings                         │
│ Phase 5: Report Generation ──► Markdown + HTML                  │
│ Phase 6: Follow-up ──► Generate next research directions        │
└─────────────────────────────────────────────────────────────────┘
```

## Depth Levels

| Level | Agents | Time    | Use Case          |
| ----- | ------ | ------- | ----------------- |
| 1-2   | 2      | ~5 min  | Quick fact-check  |
| 3     | 3      | ~15 min | Standard research |
| 4-5   | 5+     | ~30 min | Deep analysis     |

Default: Level 4 (Market/Competitive focus)

## Phase 1: Query Analysis

Decompose research query into sub-questions:

```
Task(
  subagent_type='general-purpose',
  prompt='''Analyze this research query: "{query}"

  1. Identify the core research question
  2. Break into 3-5 sub-questions for parallel research
  3. Determine research domains:
     - Market trends
     - Competitor landscape
     - Technology/product analysis
     - Pricing/business model
     - SWOT factors
  4. Suggest search queries for each sub-question

  Output structured plan with sub-questions and search strategies.
  ''',
  description='Analyze research query',
  model='sonnet'
)
```

## Phase 2: Parallel Research Agents

Launch 5+ specialized agents based on depth level:

### Market Trends Agent

```
Task(
  subagent_type='Explore',
  prompt='''Research market trends for: {topic}

  Search for:
  - Market size and growth projections
  - Key trends and drivers
  - Industry reports and forecasts
  - Regional market variations

  Use WebSearch with queries:
  - "{topic} market size 2025"
  - "{topic} industry trends forecast"
  - "{topic} market growth analysis"

  Return findings with source URLs.
  ''',
  description='Research market trends',
  model='haiku',
  run_in_background=true
)
```

### Competitor Analysis Agent

```
Task(
  subagent_type='Explore',
  prompt='''Analyze competitors for: {topic}

  Research:
  - Major players and market share
  - Product/service offerings
  - Pricing strategies
  - Strengths and weaknesses
  - Recent news and developments

  Use WebSearch with queries:
  - "{topic} top companies market share"
  - "{topic} competitor comparison"
  - "{topic} industry leaders 2025"

  Return competitive landscape with sources.
  ''',
  description='Analyze competitors',
  model='haiku',
  run_in_background=true
)
```

### Technology/Product Agent

```
Task(
  subagent_type='Explore',
  prompt='''Research technology and products for: {topic}

  Focus on:
  - Key technologies and innovations
  - Product features comparison
  - Technology roadmaps
  - Emerging solutions

  Use WebSearch with queries:
  - "{topic} technology comparison"
  - "{topic} product features"
  - "{topic} innovation trends"

  Return technology analysis with sources.
  ''',
  description='Research technology',
  model='haiku',
  run_in_background=true
)
```

### Business Model Agent

```
Task(
  subagent_type='Explore',
  prompt='''Analyze business models for: {topic}

  Research:
  - Revenue models and pricing
  - Go-to-market strategies
  - Customer segments
  - Value propositions

  Use WebSearch with queries:
  - "{topic} business model analysis"
  - "{topic} pricing strategy"
  - "{topic} revenue model"

  Return business model insights with sources.
  ''',
  description='Analyze business models',
  model='haiku',
  run_in_background=true
)
```

### News & Developments Agent

```
Task(
  subagent_type='Explore',
  prompt='''Research recent news for: {topic}

  Find:
  - Latest industry news
  - Recent announcements
  - Partnerships and acquisitions
  - Regulatory changes

  Use WebSearch with queries:
  - "{topic} latest news 2025"
  - "{topic} recent developments"
  - "{topic} industry updates"

  Return news summary with sources and dates.
  ''',
  description='Research recent news',
  model='haiku',
  run_in_background=true
)
```

## Phase 3: Validation

Cross-reference findings across agents:

```
Task(
  subagent_type='general-purpose',
  prompt='''Validate research findings:

  Agent Results: {all_agent_results}

  Tasks:
  1. Cross-reference facts across sources
  2. Identify contradictions or conflicts
  3. Rate source credibility (domain authority, date)
  4. Flag unverified claims
  5. Note knowledge gaps requiring follow-up

  Output validation report with confidence scores.
  ''',
  description='Validate findings',
  model='sonnet'
)
```

## Phase 4: Synthesis

Combine validated findings into coherent analysis:

```
Task(
  subagent_type='general-purpose',
  prompt='''Synthesize research findings:

  Validated Data: {validated_results}
  Original Query: {query}

  Create synthesis:
  1. Executive Summary (2-3 sentences)
  2. Key Findings (bullet points)
  3. Market Overview
  4. Competitive Landscape
  5. Technology Analysis
  6. SWOT Analysis
  7. Recommendations
  8. Knowledge Gaps

  Maintain source citations throughout.
  ''',
  description='Synthesize findings',
  model='sonnet'
)
```

## Phase 5: Report Generation

Generate reports in multiple formats:

### Markdown Report

```markdown
# Deep Research Report: {topic}

**Generated:** {date}
**Depth Level:** {level}
**Sources Consulted:** {source_count}

## Executive Summary

{executive_summary}

## Key Findings

{key_findings_bullets}

## Detailed Analysis

### Market Overview

{market_analysis}

### Competitive Landscape

{competitor_analysis}

### Technology & Products

{technology_analysis}

### Business Models

{business_model_analysis}

## SWOT Analysis

| Strengths   | Weaknesses   |
| ----------- | ------------ |
| {strengths} | {weaknesses} |

| Opportunities   | Threats   |
| --------------- | --------- |
| {opportunities} | {threats} |

## Recommendations

{recommendations}

## Knowledge Gaps & Follow-up Questions

{follow_up_questions}

## Sources

{citations_with_urls}

---

_Generated by Deep Research V3_
```

### HTML Report

Use template from `assets/report_template.html`:

- Styled with Tailwind CSS
- Interactive table of contents
- Collapsible sections
- Source links with credibility indicators

## Phase 6: Follow-up Generation

Generate next research directions:

```
Based on this research, suggested follow-up questions:

1. {follow_up_1}
2. {follow_up_2}
3. {follow_up_3}

Would you like me to investigate any of these further?
```

## Citation Management

### Source Tracking

For each source, track:

- **URL**: Full web address
- **Title**: Page/article title
- **Date**: Publication/access date
- **Credibility**: Domain authority score
- **Excerpt**: Relevant quote

### Citation Format

```markdown
[Title](url) - {date}

> "Relevant excerpt from source"
```

### Credibility Scoring

| Score  | Criteria                                |
| ------ | --------------------------------------- |
| High   | Official sources, peer-reviewed, recent |
| Medium | News outlets, industry publications     |
| Low    | Blogs, forums, outdated (>2 years)      |

## Summary Levels

Adjust output verbosity:

| Level    | Output                                      |
| -------- | ------------------------------------------- |
| Brief    | Executive summary only (100-200 words)      |
| Standard | Key findings + summary (500-1000 words)     |
| Detailed | Full report with all sections (2000+ words) |

## Quick Command

**File:** `commands/deep-research.md`

```yaml
---
allowed-tools: WebSearch, WebFetch, Task, Read, Write
argument-hint: [query] [--depth 1-5] [--summary brief|standard|detailed]
description: Run deep research on a topic
---

Run deep research using the deep-research-v3 skill.

Query: $1
Options: $2 $3
```

## Trigger Phrases

- "deep research on..." / "...에 대해 심층 조사해줘"
- "market analysis for..." / "...시장 분석해줘"
- "competitive analysis of..." / "...경쟁사 분석"
- "thorough investigation of..." / "...철저히 조사해줘"
- "research report on..." / "...연구 보고서 작성해줘"

## Resources

- [Agent Prompts](references/agent_prompts.md) - Specialized agent prompts
- [Report Template](assets/report_template.html) - HTML report template
- [Citation Guide](references/citation_guide.md) - Citation best practices
