#!/usr/bin/env python3
"""
Typography System - Neo-grotesque type hierarchy.

Implements precise typography with single superfamily and strict hierarchy ratios.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TypeLevel:
    """Single level in the type hierarchy."""
    level: int
    size: float
    weight: int
    line_height: float
    letter_spacing: float
    role: str


@dataclass
class TypeHierarchy:
    """Complete typography hierarchy."""
    font_family: str
    base_size: float
    scale_ratio: float
    levels: list[TypeLevel]

    def to_dict(self) -> dict[str, Any]:
        return {
            "font_family": self.font_family,
            "base_size": self.base_size,
            "scale_ratio": self.scale_ratio,
            "levels": {
                str(level.level): {
                    "size": level.size,
                    "weight": level.weight,
                    "line_height": level.line_height,
                    "letter_spacing": level.letter_spacing,
                    "role": level.role
                }
                for level in self.levels
            }
        }


class TypographySystem:
    """
    Typography system for infographics.

    Features:
    - Single neo-grotesque superfamily
    - 5-level hierarchy
    - Precise ratios (1.25 scale)
    - Readability metrics
    """

    # Neo-grotesque font stack (priority order)
    FONT_STACK = [
        "Inter",
        "Helvetica Neue",
        "Arial",
        "system-ui",
        "sans-serif"
    ]

    # Hierarchy specifications
    LEVELS = {
        1: {"role": "title", "weight": 700, "line_height": 1.2, "letter_spacing": -0.02},
        2: {"role": "subtitle", "weight": 600, "line_height": 1.3, "letter_spacing": -0.01},
        3: {"role": "body", "weight": 400, "line_height": 1.5, "letter_spacing": 0},
        4: {"role": "caption", "weight": 400, "line_height": 1.4, "letter_spacing": 0.01},
        5: {"role": "data", "weight": 500, "line_height": 1.0, "letter_spacing": 0.02}
    }

    # Size specifications from design system
    SIZES = {
        1: 32,  # Title
        2: 24,  # Subtitle
        3: 16,  # Body
        4: 12,  # Caption
        5: 11   # Data labels
    }

    def __init__(self, font_family: str | None = None, base_size: float = 16):
        self.font_family = font_family or self.FONT_STACK[0]
        self.base_size = base_size
        self.scale_ratio = 1.25  # Major third scale

    def create_hierarchy(
        self,
        elements: list[dict[str, Any]],
        max_levels: int = 5,
        base_size: float | None = None
    ) -> TypeHierarchy:
        """Create typography hierarchy based on content elements."""
        base = base_size or self.base_size
        levels = []

        for level_num in range(1, max_levels + 1):
            spec = self.LEVELS.get(level_num, self.LEVELS[3])
            size = self.SIZES.get(level_num, base)

            levels.append(TypeLevel(
                level=level_num,
                size=size,
                weight=spec["weight"],
                line_height=spec["line_height"],
                letter_spacing=spec["letter_spacing"],
                role=spec["role"]
            ))

        return TypeHierarchy(
            font_family=self.font_family,
            base_size=base,
            scale_ratio=self.scale_ratio,
            levels=levels
        )

    def calculate_readability(self, hierarchy: TypeHierarchy) -> float:
        """
        Calculate readability score (0-1).

        Based on:
        - Sufficient size differentiation between levels
        - Appropriate line heights
        - Consistent scale ratio
        """
        score = 1.0
        levels = sorted(hierarchy.levels, key=lambda l: l.level)

        # Check size differentiation
        for i in range(len(levels) - 1):
            current = levels[i]
            next_level = levels[i + 1]

            ratio = current.size / next_level.size
            if ratio < 1.1:  # Less than 10% difference
                score -= 0.1
            elif ratio > 2.0:  # More than 100% difference
                score -= 0.05

        # Check line heights
        for level in levels:
            if level.line_height < 1.0:
                score -= 0.1
            elif level.line_height > 2.0:
                score -= 0.05

        # Check body text size
        body_level = next((l for l in levels if l.role == "body"), None)
        if body_level:
            if body_level.size < 14:
                score -= 0.2  # Too small for readability
            elif body_level.size > 20:
                score -= 0.1  # Potentially too large

        return max(0.0, min(1.0, score))

    def get_fluid_size(
        self,
        level: int,
        min_viewport: int = 320,
        max_viewport: int = 1440
    ) -> str:
        """Generate CSS clamp() for fluid typography."""
        sizes = self.SIZES

        base_size = sizes.get(level, 16)

        # Calculate min/max based on viewport scaling
        min_size = base_size * 0.75
        max_size = base_size * 1.25

        # Calculate preferred value
        vw = (max_size - min_size) / (max_viewport - min_viewport) * 100
        offset = min_size - (vw * min_viewport / 100)

        return f"clamp({min_size}px, {offset:.2f}px + {vw:.4f}vw, {max_size}px)"

    def get_font_stack(self) -> str:
        """Get CSS font-family declaration."""
        quoted = [f'"{font}"' if " " in font else font for font in self.FONT_STACK]
        return ", ".join(quoted)

    def calculate_optimal_line_length(
        self,
        font_size: float,
        characters_per_line: int = 66
    ) -> float:
        """Calculate optimal line length in pixels."""
        # Average character width is approximately 0.5 * font size for sans-serif
        avg_char_width = font_size * 0.5
        return avg_char_width * characters_per_line

    def generate_css_variables(self, hierarchy: TypeHierarchy) -> str:
        """Generate CSS custom properties for typography."""
        lines = [":root {"]

        lines.append(f'  --font-family: {self.get_font_stack()};')
        lines.append(f'  --base-size: {hierarchy.base_size}px;')
        lines.append(f'  --scale-ratio: {hierarchy.scale_ratio};')
        lines.append("")

        for level in hierarchy.levels:
            prefix = f"--type-{level.role}"
            lines.append(f'  {prefix}-size: {level.size}px;')
            lines.append(f'  {prefix}-weight: {level.weight};')
            lines.append(f'  {prefix}-line-height: {level.line_height};')
            lines.append(f'  {prefix}-letter-spacing: {level.letter_spacing}em;')
            lines.append("")

        lines.append("}")
        return "\n".join(lines)

    def validate_contrast_ratio(
        self,
        font_size: float,
        font_weight: int,
        contrast_ratio: float
    ) -> dict[str, bool]:
        """Validate text meets WCAG requirements for given size/weight."""
        # Large text threshold: 18pt (24px) or 14pt (18.67px) bold
        is_large = font_size >= 24 or (font_size >= 18.67 and font_weight >= 700)

        return {
            "aa_pass": contrast_ratio >= (3.0 if is_large else 4.5),
            "aaa_pass": contrast_ratio >= (4.5 if is_large else 7.0),
            "is_large_text": is_large
        }
