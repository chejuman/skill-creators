# Research Prompts Reference

Optimized prompts for each research phase.

## Query Optimization Prompts

### Initial Query Analysis
```
Analyze this research query and identify:
1. Core topic
2. Specific aspects to investigate
3. Time constraints (latest, historical, etc.)
4. Quality requirements (academic, practical, etc.)

Query: {user_query}

Generate 3-5 optimized search queries that will:
- Cover different aspects of the topic
- Use specific keywords for better results
- Include temporal context when relevant
```

### Query Expansion
```
Expand this query with related terms:
Original: {query}

Consider:
- Synonyms and alternative terminology
- Related technologies or concepts
- Specific product/project names
- Industry-specific jargon
```

## Content Extraction Prompts

### WebFetch Insight Extraction
```
Analyze this content and extract key insights related to: {research_query}

For each insight:
1. State the finding clearly
2. Assess relevance (0.0-1.0) to the original query
3. Note any caveats or limitations

Focus on:
- Factual information with evidence
- Quantitative data when available
- Expert opinions with credentials
- Recent developments or changes
```

### Comparative Analysis
```
Compare the following sources on {topic}:

Source 1: {source1_content}
Source 2: {source2_content}

Identify:
1. Points of agreement
2. Contradictions or conflicts
3. Unique information in each
4. Gaps neither source covers
```

## Follow-Up Query Generation

### Gap Identification
```
Based on current research findings on {topic}:

Key insights found:
{insights_list}

Generate 3 follow-up queries to:
1. Address information gaps
2. Resolve contradictions
3. Explore deeper on high-relevance areas
4. Verify uncertain claims

Queries should be specific and actionable.
```

### Depth Exploration
```
For the high-relevance finding: "{finding}"

Generate targeted queries to:
1. Find supporting evidence
2. Explore technical details
3. Identify practical applications
4. Find counterarguments or limitations
```

## Synthesis Prompts

### Report Section Generation
```
Synthesize these insights into a coherent section:

Topic: {section_topic}
Insights:
{insights_with_scores}

Requirements:
- Order by relevance score (highest first)
- Include source citations
- Note confidence level
- Highlight consensus vs. disagreement
```

### Executive Summary
```
Create an executive summary for this research:

Query: {original_query}
Key Findings: {top_5_insights}
Sources: {source_count}
Depth: {research_depth}

Summary should:
- Be 3-5 sentences
- Cover main conclusions
- Note confidence level
- Suggest next steps
```

## Validation Prompts

### Cross-Reference Check
```
Verify this claim across multiple sources:
Claim: "{claim}"
Primary Source: {source}

Search for:
1. Corroborating evidence
2. Contradicting information
3. Original source of claim
4. Expert commentary
```

### Recency Validation
```
Check if this information is still current:
Information: "{info}"
Source Date: {date}

Look for:
1. More recent updates
2. Superseding information
3. Status changes
4. Deprecated or obsolete content
```
