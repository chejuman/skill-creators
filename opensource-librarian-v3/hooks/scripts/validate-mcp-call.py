#!/usr/bin/env python3
"""
MCP Call Validation Hook

Validates mcp-cli call syntax before execution.
Ensures proper JSON formatting and required parameters.
"""

import json
import os
import re
import sys


def validate_mcp_call(command: str) -> tuple[bool, str]:
    """
    Validate mcp-cli call command syntax.

    Returns:
        (is_valid, message)
    """
    if "mcp-cli call" not in command:
        return True, ""  # Not an MCP call, skip

    # Extract the JSON argument
    match = re.search(r"mcp-cli call [^\s]+ '(\{[^']+\})'", command)
    if not match:
        match = re.search(r'mcp-cli call [^\s]+ "(\{[^"]+\})"', command)

    if not match:
        return False, "MCP call missing JSON arguments"

    json_str = match.group(1)

    try:
        params = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in MCP call: {e}"

    # Check for common gitmvp required params
    if "gitmvp" in command:
        if "search_code_in_repo" in command:
            required = ["owner", "repo", "query"]
            missing = [p for p in required if p not in params]
            if missing:
                return False, f"Missing required params for search_code_in_repo: {missing}"

        elif "read_repository" in command:
            required = ["owner", "repo", "path"]
            missing = [p for p in required if p not in params]
            if missing:
                return False, f"Missing required params for read_repository: {missing}"

    return True, ""


def main():
    """Main hook entry point."""
    # Get command from environment
    command = os.environ.get("TOOL_INPUT", "")
    if not command:
        try:
            input_data = json.loads(sys.stdin.read())
            command = input_data.get("command", "")
        except Exception:
            command = ""

    is_valid, message = validate_mcp_call(command)

    if not is_valid:
        result = {
            "continue": False,
            "stopReason": f"MCP call validation failed: {message}"
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
