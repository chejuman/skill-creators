#!/usr/bin/env python3
"""
Validate brand specification for completeness and consistency.

Usage:
    python validate_brand.py <brand-spec.json>

Example:
    python validate_brand.py .brand-system/brand-spec.json
"""

import json
import sys
import re
from pathlib import Path
from typing import Any


class BrandValidator:
    def __init__(self, spec: dict):
        self.spec = spec
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate(self) -> bool:
        """Run all validations."""
        self._validate_required_sections()
        self._validate_colors()
        self._validate_typography()
        self._validate_motion()
        self._validate_accessibility()
        self._validate_ai_integration()
        return len(self.errors) == 0

    def _validate_required_sections(self):
        """Check for required top-level sections."""
        required = ['color', 'font', 'motion', 'spacing']
        for section in required:
            if section not in self.spec:
                self.errors.append(f"Missing required section: {section}")

    def _validate_colors(self):
        """Validate color tokens."""
        colors = self.spec.get('color', {})

        # Check for brand colors
        if 'brand' not in colors:
            self.errors.append("Missing color.brand section")
        elif 'primary' not in colors.get('brand', {}):
            self.errors.append("Missing color.brand.primary")

        # Validate hex format
        def check_hex(obj: dict, path: str = ""):
            for key, value in obj.items():
                if key.startswith('$'):
                    continue
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, dict):
                    if '$value' in value:
                        hex_val = value['$value']
                        if not re.match(r'^#[0-9A-Fa-f]{6}$', str(hex_val)):
                            if value.get('$type') == 'color':
                                self.warnings.append(f"Invalid hex at {current_path}: {hex_val}")
                    else:
                        check_hex(value, current_path)

        check_hex(colors, "color")

    def _validate_typography(self):
        """Validate typography tokens."""
        font = self.spec.get('font', {})

        if 'family' not in font:
            self.errors.append("Missing font.family section")

        if 'size' not in font:
            self.errors.append("Missing font.size section")
        elif 'base' not in font.get('size', {}):
            self.warnings.append("Missing font.size.base - recommended for type scale")

    def _validate_motion(self):
        """Validate motion tokens."""
        motion = self.spec.get('motion', {})

        if 'duration' not in motion:
            self.warnings.append("Missing motion.duration section")

        if 'easing' not in motion:
            self.warnings.append("Missing motion.easing section")

        # Validate cubic-bezier format
        easing = motion.get('easing', {})
        for key, value in easing.items():
            if isinstance(value, dict) and '$value' in value:
                bezier = value['$value']
                if 'cubic-bezier' in str(bezier):
                    # Basic format check
                    if not re.match(r'cubic-bezier\([0-9.]+,\s*[0-9.]+,\s*[0-9.]+,\s*[0-9.]+\)', bezier):
                        self.warnings.append(f"Invalid cubic-bezier at motion.easing.{key}")

    def _validate_accessibility(self):
        """Validate accessibility requirements."""
        colors = self.spec.get('color', {})

        # Check for semantic colors
        if 'semantic' not in colors:
            self.warnings.append("Missing color.semantic (success, warning, error, info)")

        # Check for contrast ratios
        accessibility = self.spec.get('accessibility', colors.get('accessibility', {}))
        if not accessibility:
            self.warnings.append("No accessibility/contrast data found - WCAG compliance unverified")

    def _validate_ai_integration(self):
        """Validate AI integration sections."""
        voice = self.spec.get('voice', {})
        imagery = self.spec.get('imagery', {})

        if voice:
            if 'ai_config' not in voice:
                self.warnings.append("Missing voice.ai_config for chatbot integration")

        if imagery:
            if 'ai_generation' not in imagery:
                self.warnings.append("Missing imagery.ai_generation for image generation prompts")

    def report(self) -> str:
        """Generate validation report."""
        lines = ["=" * 50, "Brand Specification Validation Report", "=" * 50, ""]

        if self.errors:
            lines.append(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"   • {error}")
            lines.append("")

        if self.warnings:
            lines.append(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"   • {warning}")
            lines.append("")

        if not self.errors and not self.warnings:
            lines.append("✅ All validations passed!")
        elif not self.errors:
            lines.append("✅ Validation passed with warnings")
        else:
            lines.append("❌ Validation failed - fix errors before proceeding")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_brand.py <brand-spec.json>")
        sys.exit(1)

    spec_path = sys.argv[1]

    if not Path(spec_path).exists():
        print(f"Error: File not found: {spec_path}")
        sys.exit(1)

    with open(spec_path, 'r') as f:
        spec = json.load(f)

    validator = BrandValidator(spec)
    is_valid = validator.validate()

    print(validator.report())

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
