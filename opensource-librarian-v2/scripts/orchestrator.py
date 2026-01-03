#!/usr/bin/env python3
"""
Open Source Librarian V2 - Principal Orchestrator

Level 7 hierarchical multi-agent coordination for evidence-based code research.
Classifies requests and dispatches 15+ parallel workers.
"""

import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
from datetime import datetime


class RequestType(Enum):
    """Request classification types with worker counts."""
    TYPE_A = ("conceptual", 5)      # How do I use X?
    TYPE_B = ("implementation", 8)   # Show me how X works
    TYPE_C = ("historical", 10)      # Why was X changed?
    TYPE_D = ("comprehensive", 15)   # Complex multi-part


@dataclass
class ClassificationResult:
    """Result of request classification."""
    request_type: str
    category: str
    reason: str
    workers: int
    parallel_minimum: int
    agents: list


def classify_request(query: str) -> ClassificationResult:
    """
    Classify user request into TYPE A/B/C/D.

    Args:
        query: User's question

    Returns:
        ClassificationResult with type, workers, and agent assignments
    """
    q = query.lower()

    # TYPE C: Historical context
    if any(p in q for p in ["why was", "why did", "history", "changed", "왜 변경", "히스토리"]):
        return ClassificationResult(
            request_type="TYPE_C",
            category="historical",
            reason="Query asks about historical context or reasons for changes",
            workers=10,
            parallel_minimum=6,
            agents=["code_hunter_1", "code_hunter_2", "git_history_1", "git_history_2",
                   "git_history_3", "documentation", "validator_1", "validator_2",
                   "synthesis", "json_api"]
        )

    # TYPE B: Implementation details
    if any(p in q for p in ["show me", "source", "implementation", "how does", "내부", "구현"]):
        return ClassificationResult(
            request_type="TYPE_B",
            category="implementation",
            reason="Query asks about source code or implementation details",
            workers=8,
            parallel_minimum=5,
            agents=["code_hunter_1", "code_hunter_2", "code_hunter_3",
                   "documentation", "git_history", "validator", "synthesis", "json_api"]
        )

    # TYPE A: Conceptual
    if any(p in q for p in ["how do i", "how to", "best way", "사용법", "어떻게 사용"]):
        return ClassificationResult(
            request_type="TYPE_A",
            category="conceptual",
            reason="Query asks about usage or conceptual understanding",
            workers=5,
            parallel_minimum=3,
            agents=["documentation", "code_hunter", "web_research", "synthesis", "json_api"]
        )

    # TYPE D: Comprehensive (default for complex queries)
    return ClassificationResult(
        request_type="TYPE_D",
        category="comprehensive",
        reason="Complex query requiring comprehensive multi-agent research",
        workers=15,
        parallel_minimum=10,
        agents=["code_hunter_1", "code_hunter_2", "code_hunter_3", "code_hunter_4",
               "git_history_1", "git_history_2", "git_history_3",
               "documentation_1", "documentation_2",
               "web_research_1", "web_research_2",
               "validator_1", "validator_2",
               "synthesis", "json_api"]
    )


def execute_mcp_tool(server: str, tool: str, params: dict) -> dict:
    """
    Execute MCP tool via mcp-cli.

    Args:
        server: MCP server name
        tool: Tool name
        params: Tool parameters

    Returns:
        Tool result as dict
    """
    cmd = ["mcp-cli", "call", f"{server}/{tool}", json.dumps(params)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout) if result.stdout else {"error": result.stderr}
    except subprocess.TimeoutExpired:
        return {"error": "Timeout after 30s"}
    except json.JSONDecodeError:
        return {"raw_output": result.stdout if result else "No output"}
    except Exception as e:
        return {"error": str(e)}


def search_repositories(query: str, sort: str = "stars", per_page: int = 5) -> dict:
    """Search GitHub repositories via gitmvp."""
    return execute_mcp_tool("gitmvp", "search_repositories", {
        "query": query,
        "sort": sort,
        "per_page": per_page
    })


def search_code_in_repo(owner: str, repo: str, query: str) -> dict:
    """Search code within specific repository via gitmvp."""
    return execute_mcp_tool("gitmvp", "search_code_in_repo", {
        "owner": owner,
        "repo": repo,
        "query": query
    })


def get_file_tree(owner: str, repo: str) -> dict:
    """Get repository file structure via gitmvp."""
    return execute_mcp_tool("gitmvp", "get_file_tree", {
        "owner": owner,
        "repo": repo,
        "format": "tree"
    })


def read_repository(owner: str, repo: str, path: str, branch: str = "main") -> dict:
    """Read file from repository via gitmvp."""
    return execute_mcp_tool("gitmvp", "read_repository", {
        "owner": owner,
        "repo": repo,
        "path": path,
        "branch": branch
    })


def query_docs(library_name: str, topic: str, tokens: int = 5000) -> dict:
    """Query library documentation via context7."""
    # First resolve library ID
    resolve_result = execute_mcp_tool(
        "plugin_context7_context7", "resolve-library-id",
        {"libraryName": library_name}
    )

    library_id = resolve_result.get("libraryId", f"/{library_name}/{library_name}")

    # Query docs
    return execute_mcp_tool(
        "plugin_context7_context7", "query-docs",
        {"libraryId": library_id, "query": topic, "tokens": tokens}
    )


def get_commit_sha(owner: str, repo: str) -> Optional[str]:
    """Get HEAD commit SHA for permalinks."""
    cmd = ["gh", "api", f"repos/{owner}/{repo}/commits/HEAD", "--jq", ".sha"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def format_permalink(owner: str, repo: str, sha: str, path: str,
                    start_line: int, end_line: Optional[int] = None) -> str:
    """Format GitHub permalink with SHA."""
    base = f"https://github.com/{owner}/{repo}/blob/{sha}/{path}"
    if end_line and end_line != start_line:
        return f"{base}#L{start_line}-L{end_line}"
    return f"{base}#L{start_line}"


def generate_execution_plan(classification: ClassificationResult) -> dict:
    """Generate execution plan based on classification."""
    return {
        "phases": [
            {
                "phase": 1,
                "name": "DISPATCH",
                "action": "Launch parallel workers",
                "workers": classification.agents[:classification.parallel_minimum],
                "parallel": True
            },
            {
                "phase": 2,
                "name": "SYNCHRONIZE",
                "action": "Collect all worker results",
                "wait_for": "all"
            },
            {
                "phase": 3,
                "name": "SYNTHESIZE",
                "action": "AI synthesis with findings",
                "agent": "synthesis"
            },
            {
                "phase": 4,
                "name": "DELIVER",
                "action": "Generate JSON API v2 response",
                "agent": "json_api"
            }
        ]
    }


def main():
    """Main orchestrator entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No query provided",
            "usage": "orchestrator.py <query>",
            "example": "orchestrator.py 'How does FastAPI handle dependency injection?'"
        }, indent=2))
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    # Classify request
    classification = classify_request(query)
    execution_plan = generate_execution_plan(classification)

    # Generate output
    output = {
        "apiVersion": "v2",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "classification": {
            "type": classification.request_type,
            "category": classification.category,
            "reason": classification.reason,
            "workers_total": classification.workers,
            "parallel_minimum": classification.parallel_minimum
        },
        "agents": classification.agents,
        "execution_plan": execution_plan,
        "instructions": {
            "parallel_dispatch": f"Launch {classification.parallel_minimum}+ agents with run_in_background=true",
            "sync_point": "Wait for all workers with TaskOutput(block=true)",
            "synthesis": "Invoke AI Synthesis Agent with collected findings",
            "output": "Generate JSON API v2 response"
        }
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
