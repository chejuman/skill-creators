#!/usr/bin/env python3
"""
MCP Server Availability Check Hook

Checks that required MCP servers (gitmvp, context7) are available
at session start. Warns if servers are missing.
"""

import json
import subprocess
import sys


def check_mcp_server(server_name: str) -> bool:
    """
    Check if an MCP server is available.

    Returns:
        True if available, False otherwise
    """
    try:
        result = subprocess.run(
            ["mcp-cli", "tools", server_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0 and len(result.stdout.strip()) > 0
    except Exception:
        return False


def main():
    """Main hook entry point."""
    required_servers = {
        "gitmvp": "GitHub repository analysis",
        "plugin_context7_context7": "Library documentation"
    }

    missing = []
    available = []

    for server, purpose in required_servers.items():
        if check_mcp_server(server):
            available.append(f"{server} ({purpose})")
        else:
            missing.append(f"{server} ({purpose})")

    if missing:
        result = {
            "continue": True,
            "systemMessage": f"""Open Source Librarian V3 - MCP Server Status

Available:
{chr(10).join(f'  [OK] {s}' for s in available) if available else '  (none)'}

Missing:
{chr(10).join(f'  [X] {s}' for s in missing)}

Some features may be limited without all MCP servers.
"""
        }
        print(json.dumps(result))
    else:
        result = {
            "continue": True,
            "systemMessage": "Open Source Librarian V3 ready. All MCP servers available."
        }
        print(json.dumps(result))


if __name__ == "__main__":
    main()
