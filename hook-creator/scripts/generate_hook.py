#!/usr/bin/env python3
"""Generate Claude Code hook configurations."""

import argparse
import json
import sys

VALID_EVENTS = [
    "PreToolUse", "PostToolUse", "PermissionRequest",
    "UserPromptSubmit", "Stop", "SubagentStop",
    "SessionStart", "SessionEnd", "PreCompact", "Notification"
]

EVENTS_WITH_MATCHERS = [
    "PreToolUse", "PostToolUse", "PermissionRequest",
    "SessionStart", "PreCompact", "Notification"
]


def generate_hook(event: str, matcher: str = None, command: str = None,
                  prompt: str = None, timeout: int = 60, description: str = None) -> dict:
    """Generate a hook configuration dictionary."""
    if event not in VALID_EVENTS:
        raise ValueError(f"Invalid event: {event}. Valid: {VALID_EVENTS}")

    hook_entry = {}
    if matcher and event in EVENTS_WITH_MATCHERS:
        hook_entry["matcher"] = matcher

    hook_config = {"type": "prompt" if prompt else "command"}
    if prompt:
        hook_config["prompt"] = prompt
    elif command:
        hook_config["command"] = command
    else:
        raise ValueError("Either --command or --prompt is required")

    if timeout != 60:
        hook_config["timeout"] = timeout

    hook_entry["hooks"] = [hook_config]

    return {"hooks": {event: [hook_entry]}}


def interactive_mode() -> dict:
    """Interactive hook creation wizard."""
    print("\n=== Claude Code Hook Generator ===\n")

    print("Available events:")
    for i, event in enumerate(VALID_EVENTS, 1):
        has_matcher = "✓" if event in EVENTS_WITH_MATCHERS else "✗"
        print(f"  {i}. {event} (matcher: {has_matcher})")

    choice = input("\nSelect event (1-10): ").strip()
    try:
        event = VALID_EVENTS[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice", file=sys.stderr)
        sys.exit(1)

    matcher = None
    if event in EVENTS_WITH_MATCHERS:
        matcher = input("Matcher pattern (e.g., Write|Edit, or press Enter to skip): ").strip()
        matcher = matcher if matcher else None

    hook_type = input("Hook type (command/prompt) [command]: ").strip() or "command"

    if hook_type == "prompt":
        prompt_text = input("LLM prompt: ").strip()
        command = None
    else:
        command = input("Shell command: ").strip()
        prompt_text = None

    timeout_str = input("Timeout in seconds [60]: ").strip()
    timeout = int(timeout_str) if timeout_str else 60

    return generate_hook(event, matcher, command, prompt_text, timeout)


def main():
    parser = argparse.ArgumentParser(description="Generate Claude Code hook configuration")
    parser.add_argument("--event", "-e", choices=VALID_EVENTS, help="Hook event type")
    parser.add_argument("--matcher", "-m", help="Matcher pattern (for supported events)")
    parser.add_argument("--command", "-c", help="Shell command to execute")
    parser.add_argument("--prompt", "-p", help="LLM prompt (for prompt-type hooks)")
    parser.add_argument("--timeout", "-t", type=int, default=60, help="Timeout seconds")
    parser.add_argument("--description", "-d", help="Hook description (for documentation)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    args = parser.parse_args()

    if args.interactive:
        hook_config = interactive_mode()
    elif args.event:
        hook_config = generate_hook(
            args.event, args.matcher, args.command,
            args.prompt, args.timeout, args.description
        )
    else:
        parser.print_help()
        sys.exit(1)

    output = json.dumps(hook_config, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
