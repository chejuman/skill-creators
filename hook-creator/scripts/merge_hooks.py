#!/usr/bin/env python3
"""Merge hook configurations into Claude Code settings."""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime


def load_json(filepath: str) -> dict:
    """Load JSON file, return empty dict if not exists."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


def merge_hooks(existing: dict, new_hooks: dict) -> dict:
    """Merge new hooks into existing configuration."""
    if "hooks" not in existing:
        existing["hooks"] = {}

    new_hook_events = new_hooks.get("hooks", {})

    for event_name, event_hooks in new_hook_events.items():
        if event_name not in existing["hooks"]:
            existing["hooks"][event_name] = []

        # Check for duplicate matchers
        existing_matchers = set()
        for hook_entry in existing["hooks"][event_name]:
            matcher = hook_entry.get("matcher", "*")
            existing_matchers.add(matcher)

        for new_hook_entry in event_hooks:
            new_matcher = new_hook_entry.get("matcher", "*")
            if new_matcher in existing_matchers:
                print(f"⚠️  Duplicate matcher '{new_matcher}' for {event_name}, appending")

            existing["hooks"][event_name].append(new_hook_entry)

    return existing


def backup_file(filepath: str) -> str:
    """Create a timestamped backup of the file."""
    if not os.path.exists(filepath):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.backup.{timestamp}"
    shutil.copy2(filepath, backup_path)
    return backup_path


def main():
    parser = argparse.ArgumentParser(description="Merge hooks into Claude Code settings")
    parser.add_argument("hooks_file", help="JSON file with new hooks to merge")
    parser.add_argument("settings_file", nargs="?", default=os.path.expanduser("~/.claude/settings.json"),
                        help="Target settings file (default: ~/.claude/settings.json)")
    parser.add_argument("--no-backup", action="store_true", help="Skip backup creation")
    parser.add_argument("--dry-run", action="store_true", help="Show result without writing")

    args = parser.parse_args()

    # Load files
    if not os.path.exists(args.hooks_file):
        print(f"❌ Hooks file not found: {args.hooks_file}", file=sys.stderr)
        sys.exit(1)

    new_hooks = load_json(args.hooks_file)
    existing = load_json(args.settings_file)

    # Merge
    merged = merge_hooks(existing, new_hooks)

    if args.dry_run:
        print("=== Dry Run Result ===")
        print(json.dumps(merged, indent=2))
        return

    # Backup
    if not args.no_backup and os.path.exists(args.settings_file):
        backup_path = backup_file(args.settings_file)
        print(f"📦 Backup created: {backup_path}")

    # Ensure directory exists
    os.makedirs(os.path.dirname(args.settings_file), exist_ok=True)

    # Write merged config
    with open(args.settings_file, "w") as f:
        json.dump(merged, indent=2, fp=f)

    print(f"✅ Hooks merged into {args.settings_file}")

    # Count hooks
    hook_count = sum(len(hooks) for hooks in merged.get("hooks", {}).values())
    print(f"   Total hooks: {hook_count}")


if __name__ == "__main__":
    main()
