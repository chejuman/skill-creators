#!/usr/bin/env python3
"""Parse resolve-debt-v4 command arguments."""

import argparse
import json
import sys
from pathlib import Path


def parse_arguments(args_str: str = None) -> dict:
    """Parse command line arguments for resolve-debt-v4."""
    parser = argparse.ArgumentParser(
        description="Enterprise Technical Debt Resolution"
    )

    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target directory or file pattern (default: current directory)"
    )

    parser.add_argument(
        "--level", "-l",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=3,
        help="Analysis depth level 1-5 (default: 3)"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["md", "html", "json", "exec", "all"],
        default="md",
        help="Output format (default: md)"
    )

    parser.add_argument(
        "--focus",
        type=str,
        default="all",
        help="Focus areas: perf,sec,arch,ai,silo or 'all' (default: all)"
    )

    parser.add_argument(
        "--cost",
        action="store_true",
        help="Enable business cost quantification"
    )

    parser.add_argument(
        "--autofix",
        action="store_true",
        help="Generate auto-fix patches for quick wins"
    )

    parser.add_argument(
        "--compare",
        type=str,
        help="Path to previous report for trend comparison"
    )

    parser.add_argument(
        "--hourly-rate",
        type=int,
        default=75,
        help="Developer hourly rate for cost calculation (default: 75)"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Force self-critique validation (auto-enabled at level 5)"
    )

    if args_str:
        args = parser.parse_args(args_str.split())
    else:
        args = parser.parse_args()

    # Parse focus areas
    focus_areas = []
    if args.focus == "all":
        focus_areas = ["cq", "dep", "arch", "test", "perf", "sec", "doc", "type", "ai", "silo"]
    else:
        focus_map = {
            "cq": "cq", "code": "cq", "quality": "cq",
            "dep": "dep", "dependency": "dep",
            "arch": "arch", "architecture": "arch",
            "test": "test", "coverage": "test",
            "perf": "perf", "performance": "perf",
            "sec": "sec", "security": "sec",
            "doc": "doc", "documentation": "doc",
            "type": "type", "types": "type",
            "ai": "ai",
            "silo": "silo", "knowledge": "silo"
        }
        for area in args.focus.split(","):
            mapped = focus_map.get(area.strip().lower())
            if mapped:
                focus_areas.append(mapped)

    # Determine worker configuration
    worker_config = {
        1: {"workers": 4, "model": "haiku", "agents": ["cq", "dep", "sec", "test"]},
        2: {"workers": 6, "model": "haiku", "agents": ["cq", "dep", "sec", "test", "arch", "perf"]},
        3: {"workers": 8, "model": "sonnet", "agents": ["cq", "dep", "sec", "test", "arch", "perf", "doc", "type"]},
        4: {"workers": 10, "model": "sonnet", "agents": ["cq", "dep", "sec", "test", "arch", "perf", "doc", "type", "ai", "silo"]},
        5: {"workers": 10, "model": "opus", "agents": ["cq", "dep", "sec", "test", "arch", "perf", "doc", "type", "ai", "silo"]}
    }

    config = worker_config[args.level]

    # Filter agents by focus if not "all"
    if args.focus != "all":
        config["agents"] = [a for a in config["agents"] if a in focus_areas]
        config["workers"] = len(config["agents"])

    result = {
        "target": str(Path(args.target).resolve()),
        "level": args.level,
        "format": args.format,
        "focus": focus_areas,
        "cost_enabled": args.cost,
        "autofix_enabled": args.autofix,
        "compare_file": args.compare,
        "hourly_rate": args.hourly_rate,
        "validate_enabled": args.validate or args.level >= 5,
        "config": config
    }

    return result


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        result = parse_arguments(" ".join(sys.argv[1:]))
    else:
        result = parse_arguments()

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
