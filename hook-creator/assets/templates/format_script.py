#!/usr/bin/env python3
"""Template: Auto-format files after Write/Edit operations."""

import json
import subprocess
import sys

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

file_path = data.get("tool_input", {}).get("file_path", "")

# TypeScript/JavaScript
if file_path.endswith((".ts", ".tsx", ".js", ".jsx")):
    subprocess.run(["npx", "prettier", "--write", file_path], capture_output=True)
    print(f"Formatted: {file_path}")

# Python
elif file_path.endswith(".py"):
    subprocess.run(["black", file_path], capture_output=True)
    print(f"Formatted: {file_path}")

sys.exit(0)
