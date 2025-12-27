#!/usr/bin/env python3
"""Validate generated technical debt reports."""

import json
import sys
from pathlib import Path


def validate_markdown_report(content: str) -> dict:
    """Validate markdown report structure."""
    errors = []
    warnings = []

    # Required sections
    required_sections = [
        "## Executive Summary",
        "## Issues by Category",
        "## Quick Wins"
    ]

    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")

    # Check for placeholder tokens
    if "{" in content and "}" in content:
        import re
        placeholders = re.findall(r'\{[A-Z_]+\}', content)
        if placeholders:
            warnings.append(f"Unfilled placeholders found: {placeholders[:5]}")

    # Check tables are properly formatted
    lines = content.split("\n")
    in_table = False
    for i, line in enumerate(lines):
        if "|" in line:
            if not in_table:
                in_table = True
            # Check for proper table format
            if line.count("|") < 2:
                warnings.append(f"Malformed table row at line {i+1}")
        else:
            in_table = False

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_json_report(content: str) -> dict:
    """Validate JSON report structure."""
    errors = []
    warnings = []

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "errors": [f"Invalid JSON: {e}"],
            "warnings": []
        }

    # Required top-level keys
    required_keys = ["metadata", "summary", "items"]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required key: {key}")

    # Validate metadata
    if "metadata" in data:
        meta = data["metadata"]
        if "version" not in meta:
            warnings.append("Missing version in metadata")
        if "date" not in meta:
            warnings.append("Missing date in metadata")

    # Validate items structure
    if "items" in data:
        for i, item in enumerate(data["items"][:5]):  # Check first 5
            if "id" not in item:
                errors.append(f"Item {i} missing 'id' field")
            if "severity" not in item:
                warnings.append(f"Item {i} missing 'severity' field")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_report(file_path: str) -> dict:
    """Validate a report file based on its extension."""
    path = Path(file_path)

    if not path.exists():
        return {
            "valid": False,
            "errors": [f"File not found: {file_path}"],
            "warnings": []
        }

    content = path.read_text()

    if path.suffix == ".md":
        return validate_markdown_report(content)
    elif path.suffix == ".json":
        return validate_json_report(content)
    elif path.suffix == ".html":
        # Basic HTML validation
        errors = []
        if "<html" not in content.lower():
            errors.append("Missing <html> tag")
        if "</html>" not in content.lower():
            errors.append("Missing closing </html> tag")
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": []
        }
    else:
        return {
            "valid": False,
            "errors": [f"Unsupported file format: {path.suffix}"],
            "warnings": []
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_report.py <report_file>")
        sys.exit(1)

    result = validate_report(sys.argv[1])
    print(json.dumps(result, indent=2))

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
