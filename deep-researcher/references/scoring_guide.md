# Relevance Scoring Guide

Detailed criteria for scoring insights during research.

## Scoring Scale (0.0 - 1.0)

### 0.9 - 1.0: Critical Relevance
**Directly answers the research question**

Criteria:
- Provides definitive answer to core query
- Contains primary evidence or data
- From authoritative source (official docs, peer-reviewed)
- Recent and accurate information

Examples:
- Official benchmark results for queried product
- Direct feature comparison from vendor documentation
- Published research findings on exact topic

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

### 0.0 - 0.2: Minimal Relevance
**Not relevant or unreliable**

Criteria:
- Does not address research question
- From unreliable source
- Significantly outdated
- Contains obvious inaccuracies

Examples:
- Spam or promotional content
- Unrelated article from keyword match
- Outdated information (pre-major updates)

## Scoring Factors

### Source Credibility (+/- 0.1)
- Official documentation: +0.1
- Peer-reviewed research: +0.1
- Recognized expert: +0.05
- Unknown blog: -0.05
- Unverified claim: -0.1

### Recency (+/- 0.1)
- Within last 3 months: +0.1
- Within last year: +0.05
- 1-2 years old: 0
- Over 2 years: -0.05
- Over 5 years: -0.1

### Evidence Quality (+/- 0.1)
- Quantitative data: +0.1
- Reproducible methodology: +0.05
- Anecdotal only: -0.05
- No evidence provided: -0.1

### Specificity (+/- 0.05)
- Directly addresses query terms: +0.05
- Requires interpretation: -0.05

## Aggregation Rules

When multiple insights cover same topic:
1. Keep highest-scored version
2. Note corroboration in report
3. Average scores if combining insights

When sources conflict:
1. Flag contradiction in report
2. Score each insight independently
3. Note which source is more authoritative

## Threshold Guidelines

| Report Section | Minimum Score |
|----------------|---------------|
| Key Findings | 0.8 |
| Supporting Info | 0.5 |
| Include in Report | 0.3 |
| Discard | < 0.3 |

## Quality Metrics

Research is considered complete when:
- At least 3 insights score >= 0.8
- At least 5 insights score >= 0.5
- No major query aspects uncovered
- Contradictions are resolved or noted
