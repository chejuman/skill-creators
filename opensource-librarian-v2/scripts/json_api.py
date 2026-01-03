#!/usr/bin/env python3
"""
Open Source Librarian V2 - JSON API v2 Generator

Generates structured, schema-validated JSON API responses.
"""

import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Evidence:
    """Evidence structure for findings."""
    permalink: str
    sha: str
    repository: str
    path: str
    lines: dict


@dataclass
class Finding:
    """Individual finding with bilingual claims."""
    id: str
    claim_en: str
    claim_ko: str
    evidence: Evidence
    snippet: str
    confidence: float


@dataclass
class HistoryEvent:
    """Git history event."""
    date: str
    event_type: str
    reference: str
    title: str
    summary: str
    link: str


@dataclass
class Source:
    """Source reference."""
    type: str
    url: str
    title: str
    relevance: str


def generate_api_response(
    query: str,
    classification: str,
    workers_used: int,
    summary_en: str,
    summary_ko: str,
    findings: list,
    history: dict = None,
    sources: list = None,
    errors: list = None,
    execution_time_ms: int = 0
) -> dict:
    """
    Generate JSON API v2 response.

    Args:
        query: Original user query
        classification: TYPE_A/B/C/D
        workers_used: Number of workers used
        summary_en: English summary
        summary_ko: Korean summary
        findings: List of Finding objects or dicts
        history: Git history dict
        sources: List of Source objects or dicts
        errors: List of error dicts
        execution_time_ms: Execution time in milliseconds

    Returns:
        Complete API response dict
    """
    return {
        "apiVersion": "v2",
        "metadata": {
            "generated": datetime.utcnow().isoformat() + "Z",
            "query": query,
            "classification": classification,
            "workersUsed": workers_used,
            "executionTimeMs": execution_time_ms,
            "language": "bilingual"
        },
        "summary": {
            "en": summary_en[:500] if summary_en else "",
            "ko": summary_ko[:500] if summary_ko else ""
        },
        "findings": [
            {
                "id": f.get("id") if isinstance(f, dict) else f.id,
                "claim": {
                    "en": f.get("claim_en") if isinstance(f, dict) else f.claim_en,
                    "ko": f.get("claim_ko") if isinstance(f, dict) else f.claim_ko
                },
                "evidence": f.get("evidence") if isinstance(f, dict) else asdict(f.evidence),
                "snippet": f.get("snippet") if isinstance(f, dict) else f.snippet,
                "confidence": f.get("confidence") if isinstance(f, dict) else f.confidence
            }
            for f in findings
        ] if findings else [],
        "history": history or {
            "timeline": [],
            "keyDecisions": [],
            "contributors": []
        },
        "sources": [
            {
                "type": s.get("type") if isinstance(s, dict) else s.type,
                "url": s.get("url") if isinstance(s, dict) else s.url,
                "title": s.get("title") if isinstance(s, dict) else s.title,
                "relevance": s.get("relevance") if isinstance(s, dict) else s.relevance
            }
            for s in sources
        ] if sources else [],
        "errors": errors or []
    }


def validate_permalink(permalink: str) -> tuple[bool, str]:
    """
    Validate GitHub permalink has SHA.

    Args:
        permalink: GitHub URL

    Returns:
        (is_valid, error_message)
    """
    if not permalink.startswith("https://github.com/"):
        return False, "Not a GitHub URL"

    parts = permalink.split("/")
    if len(parts) < 7:
        return False, "Incomplete URL structure"

    # Check for blob/SHA pattern
    if "blob" not in parts:
        return False, "Missing blob in URL"

    blob_idx = parts.index("blob")
    if blob_idx + 1 >= len(parts):
        return False, "Missing SHA after blob"

    sha = parts[blob_idx + 1]

    # SHA should be hex and 7-40 chars
    if not sha.replace("-", "").isalnum():
        return False, f"Invalid SHA format: {sha}"

    # Check for branch names instead of SHA
    branch_names = ["main", "master", "develop", "dev", "HEAD"]
    if sha in branch_names:
        return False, f"Branch name '{sha}' used instead of SHA"

    if len(sha) < 7:
        return False, f"SHA too short: {sha}"

    return True, ""


def validate_response(response: dict) -> dict:
    """
    Validate API response against schema.

    Args:
        response: API response dict

    Returns:
        Validation result with issues
    """
    issues = []

    # Check required fields
    required = ["apiVersion", "metadata", "summary", "findings", "sources"]
    for field in required:
        if field not in response:
            issues.append(f"Missing required field: {field}")

    # Validate permalinks in findings
    for i, finding in enumerate(response.get("findings", [])):
        evidence = finding.get("evidence", {})
        permalink = evidence.get("permalink", "")

        is_valid, error = validate_permalink(permalink)
        if not is_valid:
            issues.append(f"Finding {finding.get('id', i)}: {error}")

        # Check confidence range
        confidence = finding.get("confidence", 0)
        if not (0 <= confidence <= 1):
            issues.append(f"Finding {finding.get('id', i)}: Confidence {confidence} not in 0-1 range")

    # Check bilingual content
    summary = response.get("summary", {})
    if not summary.get("en"):
        issues.append("Missing English summary")
    if not summary.get("ko"):
        issues.append("Missing Korean summary")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "checked_findings": len(response.get("findings", [])),
        "checked_sources": len(response.get("sources", []))
    }


def create_finding(
    finding_id: str,
    claim_en: str,
    claim_ko: str,
    permalink: str,
    sha: str,
    repository: str,
    path: str,
    start_line: int,
    end_line: int,
    snippet: str,
    confidence: float
) -> dict:
    """Create a finding dict for the API response."""
    return {
        "id": finding_id,
        "claim_en": claim_en,
        "claim_ko": claim_ko,
        "evidence": {
            "permalink": permalink,
            "sha": sha,
            "repository": repository,
            "path": path,
            "lines": {"start": start_line, "end": end_line}
        },
        "snippet": snippet,
        "confidence": confidence
    }


def create_source(source_type: str, url: str, title: str, relevance: str) -> dict:
    """Create a source dict for the API response."""
    return {
        "type": source_type,
        "url": url,
        "title": title,
        "relevance": relevance
    }


def main():
    """Generate sample API response or validate input."""
    if len(sys.argv) < 2:
        # Generate sample response
        sample = generate_api_response(
            query="How does FastAPI handle dependency injection?",
            classification="TYPE_B",
            workers_used=8,
            summary_en="FastAPI uses Python's type hints and a Depends() function...",
            summary_ko="FastAPI는 Python의 타입 힌트와 Depends() 함수를 사용합니다...",
            findings=[
                create_finding(
                    finding_id="F001",
                    claim_en="FastAPI's Depends class handles dependency resolution",
                    claim_ko="FastAPI의 Depends 클래스가 의존성 해결을 처리합니다",
                    permalink="https://github.com/fastapi/fastapi/blob/abc123def/fastapi/dependencies/utils.py#L45-L67",
                    sha="abc123def456789",
                    repository="fastapi/fastapi",
                    path="fastapi/dependencies/utils.py",
                    start_line=45,
                    end_line=67,
                    snippet="class Depends:\n    def __init__(self, dependency):\n        self.dependency = dependency",
                    confidence=0.95
                )
            ],
            sources=[
                create_source("code", "https://github.com/fastapi/fastapi/blob/abc123def/fastapi/dependencies/utils.py#L45-L67", "utils.py", "Core implementation")
            ],
            execution_time_ms=4523
        )

        print(json.dumps(sample, indent=2, ensure_ascii=False))

    elif sys.argv[1] == "--validate":
        # Validate JSON input
        if len(sys.argv) < 3:
            print(json.dumps({"error": "Provide JSON file path or stdin"}))
            sys.exit(1)

        try:
            with open(sys.argv[2], "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = json.loads(sys.argv[2])

        result = validate_response(data)
        print(json.dumps(result, indent=2))

    else:
        print(json.dumps({
            "usage": [
                "json_api.py                  # Generate sample response",
                "json_api.py --validate FILE  # Validate JSON file"
            ]
        }, indent=2))


if __name__ == "__main__":
    main()
