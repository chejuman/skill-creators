#!/usr/bin/env python3
"""
Specification Validator for Fullstack Orchestrator

Validates that a specification document contains all required sections
and follows the expected format for spec-driven development.
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of spec validation."""
    valid: bool
    errors: list[str]
    warnings: list[str]
    score: float


REQUIRED_SECTIONS = [
    "Overview",
    "Functional Requirements",
    "Non-Functional Requirements",
    "Technical Specification",
]

RECOMMENDED_SECTIONS = [
    "User Stories",
    "API Endpoints",
    "Database Schema",
    "Constraints",
    "Out of Scope",
    "Milestones",
]


def validate_spec(spec_path: Path) -> ValidationResult:
    """Validate a specification document."""
    errors = []
    warnings = []

    if not spec_path.exists():
        return ValidationResult(
            valid=False,
            errors=[f"Spec file not found: {spec_path}"],
            warnings=[],
            score=0.0
        )

    content = spec_path.read_text()

    # Check required sections
    for section in REQUIRED_SECTIONS:
        pattern = rf"^##?\s+{re.escape(section)}"
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required section: {section}")

    # Check recommended sections
    for section in RECOMMENDED_SECTIONS:
        pattern = rf"^##?\s+{re.escape(section)}"
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            warnings.append(f"Missing recommended section: {section}")

    # Check for user stories format
    if "As a" not in content or "I want" not in content:
        warnings.append("No user stories found in standard format")

    # Check for acceptance criteria
    if "Acceptance Criteria" not in content:
        warnings.append("No acceptance criteria found")

    # Check for requirement IDs
    fr_pattern = r"FR-\d+"
    nfr_pattern = r"NFR-\d+"

    if not re.search(fr_pattern, content):
        warnings.append("No functional requirement IDs (FR-XXX) found")

    if not re.search(nfr_pattern, content):
        warnings.append("No non-functional requirement IDs (NFR-XXX) found")

    # Check for API endpoints
    if "| Method |" not in content and "| Endpoint |" not in content:
        warnings.append("No API endpoint table found")

    # Calculate score
    total_checks = len(REQUIRED_SECTIONS) + len(RECOMMENDED_SECTIONS)
    passed = total_checks - len(errors) - (len(warnings) * 0.5)
    score = max(0, min(100, (passed / total_checks) * 100))

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        score=score
    )


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: validate_spec.py <spec_file.md>")
        sys.exit(1)

    spec_path = Path(sys.argv[1])
    result = validate_spec(spec_path)

    print("=" * 60)
    print("SPECIFICATION VALIDATION REPORT")
    print("=" * 60)
    print(f"File: {spec_path}")
    print(f"Valid: {'YES' if result.valid else 'NO'}")
    print(f"Score: {result.score:.1f}/100")
    print()

    if result.errors:
        print("ERRORS:")
        for error in result.errors:
            print(f"  [ERROR] {error}")
        print()

    if result.warnings:
        print("WARNINGS:")
        for warning in result.warnings:
            print(f"  [WARN] {warning}")
        print()

    if result.valid:
        print("Specification is valid and ready for development.")
    else:
        print("Please fix the errors before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    main()
