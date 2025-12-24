# Citation Guide

Best practices for source tracking and citation in research reports.

## Source Tracking Schema

For each source, track:

```json
{
  "id": "src_001",
  "url": "https://example.com/article",
  "title": "Article Title",
  "domain": "example.com",
  "date_published": "2025-01-15",
  "date_accessed": "2025-12-24",
  "author": "Author Name",
  "source_type": "industry_report",
  "credibility_score": 85,
  "excerpt": "Relevant quote from source",
  "findings": ["Finding 1", "Finding 2"]
}
```

## Source Types & Credibility

| Type                | Base Score | Examples                |
| ------------------- | ---------- | ----------------------- |
| Official/Government | 90-95%     | .gov, official company  |
| Peer-Reviewed       | 85-95%     | Academic journals       |
| Industry Reports    | 80-90%     | Gartner, McKinsey, IDC  |
| Major News          | 75-85%     | Reuters, Bloomberg, WSJ |
| Trade Publications  | 70-80%     | TechCrunch, Wired       |
| Company Blogs       | 60-75%     | Official company blogs  |
| Personal Blogs      | 40-60%     | Medium, Substack        |
| Forums/Social       | 30-50%     | Reddit, Twitter/X       |

## Credibility Adjustments

Increase score if:

- Recent publication (within 6 months)
- Multiple corroborating sources
- Author is recognized expert
- Data is verifiable

Decrease score if:

- Outdated (>2 years old)
- Single source claim
- Anonymous author
- Promotional content
- Broken citations

## Citation Formats

### Inline Citation

```markdown
According to [Gartner's 2025 Market Report](https://gartner.com/report),
the market is expected to grow at 15% CAGR.
```

### Block Quote Citation

```markdown
> "The AI market is projected to reach $500B by 2027."
>
> — [IDC Market Forecast](https://idc.com/forecast), January 2025
```

### Reference List Entry

```markdown
## Sources

1. **Gartner** - [AI Market Forecast 2025](https://gartner.com/ai-2025) - Jan 2025 | Credibility: High
2. **TechCrunch** - [Industry Analysis](https://techcrunch.com/analysis) - Dec 2024 | Credibility: Medium
3. **Company Blog** - [Product Announcement](https://company.com/blog) - Nov 2024 | Credibility: Medium
```

## Validation Checklist

Before including a source:

- [ ] URL is accessible
- [ ] Date is within acceptable range
- [ ] Author/organization is identifiable
- [ ] Claims are specific and verifiable
- [ ] No obvious bias or promotional intent
- [ ] Cross-referenced with other sources (if possible)

## Handling Conflicts

When sources disagree:

1. **Note the conflict**: "Sources differ on this point..."
2. **Present both views**: Show different perspectives
3. **Weight by credibility**: Favor higher-credibility sources
4. **Flag uncertainty**: Mark as "disputed" or "uncertain"

Example:

```markdown
### Market Size Estimates

Sources provide varying estimates:

- **Gartner** (High credibility): $150B by 2027
- **Company Report** (Medium credibility): $200B by 2027
- **Industry Blog** (Lower credibility): $180B by 2027

_Note: Variation likely due to different market definitions._
```

## Missing Information

When information is unavailable:

```markdown
**Data Gap**: No reliable sources found for [specific data point].

Suggested follow-up:

- Check industry association reports
- Contact company directly for press kit
- Monitor for upcoming analyst reports
```

## Automated Citation Warnings

Always verify automated citations:

1. **Check URL validity**: Links can break
2. **Verify quote accuracy**: May be paraphrased
3. **Confirm date**: Publication vs access date
4. **Review context**: Ensure quote isn't misrepresented

## Example Full Citation Block

```markdown
## Sources Consulted

### High Credibility

1. [Gartner Magic Quadrant for AI 2025](https://gartner.com/mq-ai-2025)
   - Published: January 2025
   - Key finding: Market leaders identified
   - Cited in: Executive Summary, Competitive Analysis

### Medium Credibility

2. [TechCrunch: AI Market Overview](https://techcrunch.com/ai-overview)
   - Published: December 2024
   - Key finding: Funding trends
   - Cited in: Market Trends section

### Supporting Sources

3. [Company Press Release](https://company.com/pr/2025-01)
   - Published: January 2025
   - Key finding: Product launch details
   - Note: Primary source, potential bias

---

_{N} sources consulted | Average credibility: {score}%_
_Research conducted: {date}_
```
