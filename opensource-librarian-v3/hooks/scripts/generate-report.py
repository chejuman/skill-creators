#!/usr/bin/env python3
"""
Report Generation Hook

Generates a summary report when research session completes.
Includes worker statistics and citation summary.
"""

import json
import os
import sys
from datetime import datetime


def main():
    """Main hook entry point."""
    # Get session info
    session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")

    # Try to read worker log
    log_file = os.path.expanduser("~/.claude/librarian-workers.log")
    workers_dispatched = 0

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            workers_dispatched = sum(1 for l in lines if '"event": "worker_dispatch"' in l)
    except Exception:
        pass

    # Generate summary
    report = {
        "session_id": session_id,
        "completed_at": datetime.utcnow().isoformat() + "Z",
        "workers_dispatched": workers_dispatched,
        "plugin": "opensource-librarian-v3"
    }

    result = {
        "continue": True,
        "systemMessage": f"""
Research session completed.
- Workers dispatched: {workers_dispatched}
- Session ID: {session_id[:8]}...
- Plugin: Open Source Librarian V3
""",
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "report": report
        }
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
