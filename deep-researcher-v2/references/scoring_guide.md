# Relevance Scoring Guide

Detailed criteria for scoring research findings.

## Scoring Scale (0.0 - 1.0)

### 0.9 - 1.0: Critical Relevance
**Directly answers the research question**

Criteria:
- Provides definitive answer to core query
- Contains primary evidence or quantitative data
- From authoritative source (official docs, peer-reviewed)
- Recent and accurate information (2024-2025)

Examples:
- Official benchmark results for queried product
- Direct feature comparison from vendor documentation
- Published research findings on exact topic
- Government statistics on specific market

### 0.7 - 0.8: High Relevance
**Strongly supports or relates to topic**

Criteria:
- Provides substantial supporting information
- Addresses major aspect of query
- Contains useful quantitative data
- From credible source

Examples:
- Case study demonstrating claimed capability
- Expert analysis of related technology
- Community benchmarks and comparisons
- Industry analyst reports

### 0.5 - 0.6: Moderate Relevance
**Provides useful context**

Criteria:
- Offers background information
- Explains related concepts
- Historical context or evolution
- May require inference to connect to query

Examples:
- Overview article on broader topic
- Historical development of technology
- Related but not directly queried information
- General market trend analysis

### 0.3 - 0.4: Low Relevance
**Tangentially related**

Criteria:
- Loosely connected to topic
- Requires significant interpretation
- May be outdated or preliminary
- Limited actionable value

Examples:
- Mentions topic briefly in passing
- Discusses competing but different technology
- Early announcements without details
- Opinion pieces without data

### 0.0 - 0.2: Minimal Relevance
**Not relevant or unreliable**

Criteria:
- Does not address research question
- From unreliable source
- Significantly outdated (>2 years)
- Contains obvious inaccuracies

Examples:
- Spam or promotional content
- Unrelated article from keyword match
- Outdated information (pre-major updates)
- Broken links or paywalled content

## Scoring Modifiers

### Source Credibility (+/- 0.1)
| Source Type | Modifier |
|-------------|----------|
| Official documentation | +0.1 |
| Peer-reviewed research | +0.1 |
| Recognized expert/analyst | +0.05 |
| Major news outlet | 0 |
| Unknown blog | -0.05 |
| Unverified claim | -0.1 |

### Recency (+/- 0.1)
| Age | Modifier |
|-----|----------|
| Within 3 months | +0.1 |
| Within 1 year | +0.05 |
| 1-2 years old | 0 |
| Over 2 years | -0.05 |
| Over 5 years | -0.1 |

### Evidence Quality (+/- 0.1)
| Quality | Modifier |
|---------|----------|
| Quantitative data with methodology | +0.1 |
| Reproducible methodology | +0.05 |
| Anecdotal only | -0.05 |
| No evidence provided | -0.1 |

### Cross-Reference (+/- 0.05)
| Validation | Modifier |
|------------|----------|
| Confirmed by 3+ sources | +0.05 |
| Confirmed by 2 sources | 0 |
| Single source only | -0.05 |
| Contradicted by other sources | -0.1 |

## Aggregation Rules

### When multiple insights cover same topic:
1. Keep highest-scored version
2. Note corroboration in report
3. Average scores if combining insights

### When sources conflict:
1. Flag contradiction in report
2. Score each insight independently
3. Note which source is more authoritative
4. Explain the discrepancy

## Threshold Guidelines

| Report Section | Minimum Score |
|----------------|---------------|
| Key Findings | 0.8 |
| Supporting Info | 0.5 |
| Include in Report | 0.3 |
| Discard | < 0.3 |

## Quality Metrics by Research Level

| Level | Min High-Relevance | Min Total Sources | Quality Threshold |
|-------|-------------------|-------------------|-------------------|
| 1 | 1 | 3 | 0.6 |
| 2 | 2 | 5 | 0.65 |
| 3 | 3 | 10 | 0.7 |
| 4 | 5 | 15 | 0.75 |
| 5 | 8 | 25 | 0.8 |

## Confidence Levels

Based on source quality and corroboration:

| Confidence | Criteria |
|------------|----------|
| **High** | 3+ credible sources agree, quantitative data available |
| **Medium** | 2 sources agree OR 1 highly authoritative source |
| **Low** | Single source, no corroboration, or conflicting info |

## Data Quality Score Calculation

```
data_quality = (
  avg_relevance_score * 0.4 +
  source_credibility_avg * 0.3 +
  recency_score * 0.2 +
  cross_reference_rate * 0.1
)
```

## Coverage Score Calculation

```
coverage = (
  subtasks_with_findings / total_subtasks * 0.5 +
  gaps_addressed / total_gaps * 0.3 +
  contradictions_resolved / total_contradictions * 0.2
)
```
