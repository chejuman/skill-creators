#!/usr/bin/env python3
"""Template: Validate tool inputs before execution."""

import json
import sys
import re

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

# File protection
if tool_name in ["Write", "Edit"]:
    file_path = tool_input.get("file_path", "")
    protected = [".env", "package-lock.json", ".git/", "node_modules/"]

    for pattern in protected:
        if pattern in file_path:
            print(f"Protected file: {file_path}", file=sys.stderr)
            sys.exit(2)  # Block

# Command validation
if tool_name == "Bash":
    command = tool_input.get("command", "")
    dangerous = [
        (r"rm\s+-rf\s+/", "Dangerous: rm -rf /"),
        (r">\s*/dev/sd", "Dangerous: writing to device"),
    ]

    for pattern, message in dangerous:
        if re.search(pattern, command):
            print(message, file=sys.stderr)
            sys.exit(2)  # Block

sys.exit(0)
