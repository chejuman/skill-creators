#!/usr/bin/env python3
"""Validate Claude Code hook configurations."""

import argparse
import json
import os
import sys
from typing import List, Tuple

VALID_EVENTS = [
    "PreToolUse", "PostToolUse", "PermissionRequest",
    "UserPromptSubmit", "Stop", "SubagentStop",
    "SessionStart", "SessionEnd", "PreCompact", "Notification"
]

EVENTS_WITH_MATCHERS = [
    "PreToolUse", "PostToolUse", "PermissionRequest",
    "SessionStart", "PreCompact", "Notification"
]


def validate_hook_config(config: dict) -> Tuple[bool, List[str]]:
    """Validate a hook configuration. Returns (is_valid, errors)."""
    errors = []

    if "hooks" not in config:
        errors.append("Missing 'hooks' key at root level")
        return False, errors

    hooks = config["hooks"]
    if not isinstance(hooks, dict):
        errors.append("'hooks' must be an object")
        return False, errors

    for event_name, event_hooks in hooks.items():
        if event_name not in VALID_EVENTS:
            errors.append(f"Invalid event: '{event_name}'. Valid: {VALID_EVENTS}")
            continue

        if not isinstance(event_hooks, list):
            errors.append(f"'{event_name}' must be an array")
            continue

        for i, hook_entry in enumerate(event_hooks):
            prefix = f"{event_name}[{i}]"

            if "matcher" in hook_entry:
                if event_name not in EVENTS_WITH_MATCHERS:
                    errors.append(f"{prefix}: '{event_name}' does not support matchers")

            if "hooks" not in hook_entry:
                errors.append(f"{prefix}: Missing 'hooks' array")
                continue

            for j, hook in enumerate(hook_entry["hooks"]):
                hook_prefix = f"{prefix}.hooks[{j}]"

                if "type" not in hook:
                    errors.append(f"{hook_prefix}: Missing 'type' (command or prompt)")
                elif hook["type"] not in ["command", "prompt"]:
                    errors.append(f"{hook_prefix}: Invalid type '{hook['type']}'")

                if hook.get("type") == "command" and "command" not in hook:
                    errors.append(f"{hook_prefix}: type 'command' requires 'command' field")

                if hook.get("type") == "prompt" and "prompt" not in hook:
                    errors.append(f"{hook_prefix}: type 'prompt' requires 'prompt' field")

                if "timeout" in hook:
                    if not isinstance(hook["timeout"], int) or hook["timeout"] <= 0:
                        errors.append(f"{hook_prefix}: 'timeout' must be positive integer")

    return len(errors) == 0, errors


def validate_file(filepath: str) -> Tuple[bool, List[str]]:
    """Validate a hook configuration file."""
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]

    try:
        with open(filepath, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    return validate_hook_config(config)


def main():
    parser = argparse.ArgumentParser(description="Validate Claude Code hook configuration")
    parser.add_argument("file", help="JSON file to validate")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only show errors")

    args = parser.parse_args()

    is_valid, errors = validate_file(args.file)

    if is_valid:
        if not args.quiet:
            print(f"✅ {args.file} is valid")
        sys.exit(0)
    else:
        print(f"❌ {args.file} has {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
