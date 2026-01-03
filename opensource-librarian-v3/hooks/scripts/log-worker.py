#!/usr/bin/env python3
"""
Worker Logging Hook

Logs worker dispatch and completion for parallel execution tracking.
Helps monitor the 15+ parallel worker system.
"""

import json
import os
import sys
from datetime import datetime


LOG_FILE = os.path.expanduser("~/.claude/librarian-workers.log")


def log_worker_event(event_type: str, details: dict):
    """
    Log a worker event to the log file.
    """
    try:
        with open(LOG_FILE, "a") as f:
            entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event": event_type,
                **details
            }
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Silent fail for logging


def main():
    """Main hook entry point."""
    # Get Task tool details from environment
    tool_input = os.environ.get("TOOL_INPUT", "")
    tool_output = os.environ.get("TOOL_OUTPUT", "")

    try:
        if tool_input:
            input_data = json.loads(tool_input)
        else:
            input_data = json.loads(sys.stdin.read())
    except Exception:
        input_data = {}

    # Extract worker info
    description = input_data.get("description", "unknown")
    model = input_data.get("model", "unknown")
    background = input_data.get("run_in_background", False)

    # Log the worker dispatch
    log_worker_event("worker_dispatch", {
        "description": description,
        "model": model,
        "background": background
    })

    # Count active workers
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-50:]  # Last 50 entries
            dispatched = sum(1 for l in lines if '"event": "worker_dispatch"' in l)
    except Exception:
        dispatched = 0

    result = {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "workerLogged": description,
            "recentDispatches": dispatched
        }
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
