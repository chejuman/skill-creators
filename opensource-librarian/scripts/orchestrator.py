#!/usr/bin/env python3
"""
Open Source Librarian Orchestrator

Multi-agent coordination script for evidence-based code research.
Classifies requests and dispatches specialized agents in parallel.
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RequestType(Enum):
    """Request classification types."""
    TYPE_A = "conceptual"      # How do I use X?
    TYPE_B = "implementation"  # Show me how X works
    TYPE_C = "context"         # Why was X changed?
    TYPE_D = "comprehensive"   # Complex multi-part


@dataclass
class ClassificationResult:
    """Result of request classification."""
    request_type: RequestType
    reason: str
    min_tools: int
    agents_needed: list[str]


def classify_request(query: str) -> ClassificationResult:
    """
    Classify the user's request into one of four types.

    Args:
        query: User's question or request

    Returns:
        ClassificationResult with type, reason, and agent recommendations
    """
    query_lower = query.lower()

    # TYPE A: Conceptual - "How do I use X?"
    conceptual_patterns = [
        "how do i", "how to", "what is the best way",
        "사용법", "어떻게 사용", "방법"
    ]

    # TYPE B: Implementation - "Show me how X works"
    implementation_patterns = [
        "show me", "source code", "implementation",
        "how does", "내부 구현", "소스", "구현"
    ]

    # TYPE C: Context - "Why was X changed?"
    context_patterns = [
        "why was", "why did", "history", "changed",
        "왜 변경", "히스토리", "이유"
    ]

    # Check patterns
    if any(p in query_lower for p in context_patterns):
        return ClassificationResult(
            request_type=RequestType.TYPE_C,
            reason="Query asks about historical context or reasons for changes",
            min_tools=4,
            agents_needed=["git_history", "code_hunter", "documentation"]
        )

    if any(p in query_lower for p in implementation_patterns):
        return ClassificationResult(
            request_type=RequestType.TYPE_B,
            reason="Query asks about source code or implementation details",
            min_tools=4,
            agents_needed=["code_hunter", "documentation", "git_history"]
        )

    if any(p in query_lower for p in conceptual_patterns):
        return ClassificationResult(
            request_type=RequestType.TYPE_A,
            reason="Query asks about usage or conceptual understanding",
            min_tools=3,
            agents_needed=["documentation", "code_hunter"]
        )

    # Default to TYPE D for complex queries
    return ClassificationResult(
        request_type=RequestType.TYPE_D,
        reason="Complex query requiring comprehensive research",
        min_tools=6,
        agents_needed=["code_hunter", "documentation", "git_history", "citation_synthesizer"]
    )


def search_code(query: str, per_page: int = 20) -> dict:
    """
    Search GitHub code using gitmvp MCP.

    Args:
        query: Search query
        per_page: Number of results

    Returns:
        Search results dict
    """
    cmd = [
        "mcp-cli", "call", "gitmvp/search_code",
        json.dumps({"query": query, "per_page": per_page})
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout) if result.stdout else {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def search_in_repo(owner: str, repo: str, query: str) -> dict:
    """
    Search code within a specific repository.

    Args:
        owner: Repository owner
        repo: Repository name
        query: Search query

    Returns:
        Search results dict
    """
    cmd = [
        "mcp-cli", "call", "gitmvp/search_code_in_repo",
        json.dumps({"owner": owner, "repo": repo, "query": query})
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout) if result.stdout else {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def get_file_tree(owner: str, repo: str) -> dict:
    """
    Get repository file structure.

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        File tree dict
    """
    cmd = [
        "mcp-cli", "call", "gitmvp/get_file_tree",
        json.dumps({"owner": owner, "repo": repo, "format": "tree"})
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout) if result.stdout else {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def read_file(owner: str, repo: str, path: str, branch: str = "main") -> dict:
    """
    Read file from repository.

    Args:
        owner: Repository owner
        repo: Repository name
        path: File path
        branch: Branch name

    Returns:
        File content dict
    """
    cmd = [
        "mcp-cli", "call", "gitmvp/read_repository",
        json.dumps({"owner": owner, "repo": repo, "path": path, "branch": branch})
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout) if result.stdout else {"error": result.stderr}
    except Exception as e:
        return {"error": str(e)}


def query_docs(library_name: str, topic: str) -> dict:
    """
    Query library documentation via context7.

    Args:
        library_name: Library name to search
        topic: Documentation topic

    Returns:
        Documentation dict
    """
    # First resolve library ID
    resolve_cmd = [
        "mcp-cli", "call", "plugin_context7_context7/resolve-library-id",
        json.dumps({"libraryName": library_name})
    ]

    try:
        result = subprocess.run(resolve_cmd, capture_output=True, text=True, timeout=15)
        resolved = json.loads(result.stdout) if result.stdout else {}
        library_id = resolved.get("libraryId", f"/{library_name}/{library_name}")

        # Query docs
        docs_cmd = [
            "mcp-cli", "call", "plugin_context7_context7/query-docs",
            json.dumps({"libraryId": library_id, "query": topic, "tokens": 5000})
        ]

        docs_result = subprocess.run(docs_cmd, capture_output=True, text=True, timeout=30)
        return json.loads(docs_result.stdout) if docs_result.stdout else {"error": docs_result.stderr}
    except Exception as e:
        return {"error": str(e)}


def format_permalink(owner: str, repo: str, sha: str, path: str,
                     start_line: int, end_line: Optional[int] = None) -> str:
    """
    Format a GitHub permalink.

    Args:
        owner: Repository owner
        repo: Repository name
        sha: Commit SHA
        path: File path
        start_line: Start line number
        end_line: End line number (optional)

    Returns:
        Formatted permalink URL
    """
    base = f"https://github.com/{owner}/{repo}/blob/{sha}/{path}"
    if end_line:
        return f"{base}#L{start_line}-L{end_line}"
    return f"{base}#L{start_line}"


def main():
    """Main orchestrator entry point."""
    if len(sys.argv) < 2:
        print("Usage: orchestrator.py <query>")
        print("Example: orchestrator.py 'How does FastAPI handle dependency injection?'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # Classify request
    classification = classify_request(query)

    print(f"""
## Request Classification

**Query**: {query}
**Type**: {classification.request_type.name} ({classification.request_type.value})
**Reason**: {classification.reason}
**Minimum Tools**: {classification.min_tools}
**Agents Needed**: {', '.join(classification.agents_needed)}

---

Proceed with parallel agent dispatch using the Task tool.
""")


if __name__ == "__main__":
    main()
