#!/usr/bin/env python3
"""
Research Utilities for Deep Researcher Skill

Provides helper functions for:
- Query optimization
- Insight scoring
- Report generation
"""

import json
import sys
from datetime import datetime
from typing import List, Dict, Optional

def optimize_query(query: str, context: Optional[str] = None) -> List[str]:
    """
    Generate optimized search queries from original query.

    Args:
        query: Original research query
        context: Optional context (e.g., "technical", "academic", "business")

    Returns:
        List of optimized queries
    """
    current_year = datetime.now().year

    optimized = []

    # Add temporal context
    optimized.append(f"{query} {current_year}")

    # Add specificity
    optimized.append(f"{query} comparison analysis")

    # Add source qualifiers
    optimized.append(f"{query} official documentation")

    if context == "technical":
        optimized.append(f"{query} technical deep dive architecture")
    elif context == "academic":
        optimized.append(f"{query} research paper study")
    elif context == "business":
        optimized.append(f"{query} market analysis industry")

    return optimized


def calculate_relevance_score(
    insight: str,
    query: str,
    source_credibility: float = 0.5,
    recency_months: int = 12,
    has_evidence: bool = True
) -> float:
    """
    Calculate relevance score for an insight.

    Args:
        insight: The insight content
        query: Original research query
        source_credibility: 0.0-1.0 credibility score
        recency_months: How many months old the source is
        has_evidence: Whether insight has supporting evidence

    Returns:
        Relevance score between 0.0 and 1.0
    """
    base_score = 0.5

    # Query term matching (simple heuristic)
    query_terms = set(query.lower().split())
    insight_terms = set(insight.lower().split())
    overlap = len(query_terms & insight_terms) / max(len(query_terms), 1)
    base_score += overlap * 0.2

    # Source credibility adjustment
    base_score += (source_credibility - 0.5) * 0.2

    # Recency adjustment
    if recency_months <= 3:
        base_score += 0.1
    elif recency_months <= 12:
        base_score += 0.05
    elif recency_months > 24:
        base_score -= 0.1

    # Evidence adjustment
    if has_evidence:
        base_score += 0.1
    else:
        base_score -= 0.1

    return max(0.0, min(1.0, base_score))


def categorize_insights(insights: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorize insights by relevance score.

    Args:
        insights: List of insight dicts with 'relevance_score' key

    Returns:
        Dict with categorized insights
    """
    categories = {
        "key_findings": [],      # >= 0.8
        "supporting": [],        # 0.5 - 0.8
        "supplementary": [],     # 0.3 - 0.5
        "discarded": []          # < 0.3
    }

    for insight in insights:
        score = insight.get("relevance_score", 0.5)
        if score >= 0.8:
            categories["key_findings"].append(insight)
        elif score >= 0.5:
            categories["supporting"].append(insight)
        elif score >= 0.3:
            categories["supplementary"].append(insight)
        else:
            categories["discarded"].append(insight)

    # Sort each category by score descending
    for key in categories:
        categories[key].sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

    return categories


def generate_follow_up_queries(
    query: str,
    insights: List[Dict],
    max_queries: int = 3
) -> List[str]:
    """
    Generate follow-up queries based on current insights.

    Args:
        query: Original research query
        insights: Current insights collected
        max_queries: Maximum number of follow-up queries

    Returns:
        List of follow-up query strings
    """
    follow_ups = []

    # If few high-relevance insights, dig deeper
    high_rel = [i for i in insights if i.get("relevance_score", 0) >= 0.8]
    if len(high_rel) < 3:
        follow_ups.append(f"{query} detailed analysis examples")

    # Look for gaps - common follow-up patterns
    follow_ups.append(f"{query} limitations challenges problems")
    follow_ups.append(f"{query} alternatives comparison vs")

    return follow_ups[:max_queries]


def format_report_json(
    query: str,
    insights: List[Dict],
    sources: List[str],
    depth: int = 1
) -> Dict:
    """
    Format research results into structured report JSON.

    Args:
        query: Original research query
        insights: All collected insights
        sources: List of source URLs
        depth: Research depth level reached

    Returns:
        Structured report dictionary
    """
    categorized = categorize_insights(insights)

    return {
        "query": query,
        "generated": datetime.now().isoformat(),
        "source_count": len(sources),
        "depth_levels": depth,
        "insight_count": len(insights),
        "key_findings": categorized["key_findings"],
        "supporting_info": categorized["supporting"],
        "supplementary": categorized["supplementary"],
        "sources": sources
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: research_utils.py <command> [args]")
        print("Commands: optimize, score, categorize, followup, report")
        sys.exit(1)

    command = sys.argv[1]

    if command == "optimize":
        if len(sys.argv) < 3:
            print("Usage: research_utils.py optimize <query> [context]")
            sys.exit(1)
        query = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else None
        result = optimize_query(query, context)
        print(json.dumps(result, indent=2))

    elif command == "score":
        # Read insight and query from stdin as JSON
        data = json.load(sys.stdin)
        score = calculate_relevance_score(
            data.get("insight", ""),
            data.get("query", ""),
            data.get("source_credibility", 0.5),
            data.get("recency_months", 12),
            data.get("has_evidence", True)
        )
        print(json.dumps({"relevance_score": score}))

    elif command == "categorize":
        insights = json.load(sys.stdin)
        result = categorize_insights(insights)
        print(json.dumps(result, indent=2))

    elif command == "followup":
        data = json.load(sys.stdin)
        result = generate_follow_up_queries(
            data.get("query", ""),
            data.get("insights", []),
            data.get("max_queries", 3)
        )
        print(json.dumps(result, indent=2))

    elif command == "report":
        data = json.load(sys.stdin)
        result = format_report_json(
            data.get("query", ""),
            data.get("insights", []),
            data.get("sources", []),
            data.get("depth", 1)
        )
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
