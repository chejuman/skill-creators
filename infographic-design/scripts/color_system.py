#!/usr/bin/env python3
"""
Color System - Five-hue palette with desaturation control.

Implements Tufte-compliant color palettes with WCAG accessibility verification.
"""

import colorsys
import math
from dataclasses import dataclass
from typing import Any


@dataclass
class Color:
    """Color with multiple representations."""
    hex: str
    rgb: tuple[int, int, int]
    hsl: tuple[float, float, float]
    name: str = ""

    @classmethod
    def from_hex(cls, hex_color: str, name: str = "") -> "Color":
        hex_clean = hex_color.lstrip("#")
        r = int(hex_clean[0:2], 16)
        g = int(hex_clean[2:4], 16)
        b = int(hex_clean[4:6], 16)

        # Convert to HSL
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

        return cls(
            hex=f"#{hex_clean.upper()}",
            rgb=(r, g, b),
            hsl=(h * 360, s * 100, l * 100),
            name=name
        )

    def with_saturation(self, saturation: float) -> "Color":
        """Return new color with adjusted saturation."""
        h, s, l = self.hsl
        new_s = min(saturation, s)

        # Convert back to RGB
        r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, new_s / 100)
        r, g, b = int(r * 255), int(g * 255), int(b * 255)

        return Color(
            hex=f"#{r:02X}{g:02X}{b:02X}",
            rgb=(r, g, b),
            hsl=(h, new_s, l),
            name=self.name
        )


@dataclass
class Palette:
    """Complete five-hue color palette."""
    primary: Color
    secondary: Color
    accent: Color
    neutral: Color
    muted: Color

    def to_dict(self) -> dict[str, str]:
        return {
            "primary": self.primary.hex,
            "secondary": self.secondary.hex,
            "accent": self.accent.hex,
            "neutral": self.neutral.hex,
            "muted": self.muted.hex
        }


class ColorSystem:
    """
    Color system for infographic design.

    Features:
    - Five-hue palette generation
    - Desaturation control (≤22% for non-accent)
    - WCAG contrast verification
    - Data-driven palette suggestions
    """

    # Preset palettes
    PRESETS = {
        "default": {
            "primary": "#1A1A2E",
            "secondary": "#4A4A68",
            "accent": "#E94560",
            "neutral": "#F0F0F5",
            "muted": "#9090A0"
        },
        "monochrome": {
            "primary": "#1A1A1A",
            "secondary": "#4A4A4A",
            "accent": "#2A6BD4",
            "neutral": "#F5F5F5",
            "muted": "#909090"
        },
        "warm": {
            "primary": "#2E1A1A",
            "secondary": "#684A4A",
            "accent": "#E96045",
            "neutral": "#F5F0F0",
            "muted": "#A09090"
        },
        "cool": {
            "primary": "#1A1A2E",
            "secondary": "#4A4A68",
            "accent": "#45B5E9",
            "neutral": "#F0F0F5",
            "muted": "#9090A0"
        }
    }

    def __init__(self, max_saturation: float = 22.0):
        self.max_saturation = max_saturation

    def generate_palette(
        self,
        data: dict[str, Any] | None = None,
        preset: str = "default",
        max_saturation: float | None = None
    ) -> Palette:
        """Generate a color palette based on data characteristics."""
        max_sat = max_saturation if max_saturation is not None else self.max_saturation

        # Get base colors from preset
        base_colors = self.PRESETS.get(preset, self.PRESETS["default"])

        # Create Color objects
        primary = Color.from_hex(base_colors["primary"], "primary")
        secondary = Color.from_hex(base_colors["secondary"], "secondary")
        accent = Color.from_hex(base_colors["accent"], "accent")
        neutral = Color.from_hex(base_colors["neutral"], "neutral")
        muted = Color.from_hex(base_colors["muted"], "muted")

        # Apply saturation limits to non-accent colors
        primary = primary.with_saturation(max_sat)
        secondary = secondary.with_saturation(max_sat)
        muted = muted.with_saturation(max_sat)

        return Palette(
            primary=primary,
            secondary=secondary,
            accent=accent,
            neutral=neutral,
            muted=muted
        )

    def verify_contrast(self, palette: Palette) -> dict[str, Any]:
        """Verify WCAG contrast ratios for palette combinations."""
        results = {
            "combinations": [],
            "min_ratio": float("inf"),
            "aa_compliant": True,
            "aaa_compliant": True
        }

        # Key combinations to check
        combinations = [
            ("primary", palette.primary, "neutral", palette.neutral),
            ("secondary", palette.secondary, "neutral", palette.neutral),
            ("accent", palette.accent, "neutral", palette.neutral),
            ("primary", palette.primary, "muted", palette.muted),
        ]

        for fg_name, fg_color, bg_name, bg_color in combinations:
            ratio = self._calculate_contrast_ratio(fg_color.rgb, bg_color.rgb)

            results["combinations"].append({
                "foreground": fg_name,
                "background": bg_name,
                "ratio": round(ratio, 2),
                "aa_pass": ratio >= 4.5,
                "aaa_pass": ratio >= 7.0
            })

            results["min_ratio"] = min(results["min_ratio"], ratio)
            if ratio < 4.5:
                results["aa_compliant"] = False
            if ratio < 7.0:
                results["aaa_compliant"] = False

        return results

    def _calculate_contrast_ratio(
        self,
        rgb1: tuple[int, int, int],
        rgb2: tuple[int, int, int]
    ) -> float:
        """Calculate WCAG contrast ratio between two colors."""
        l1 = self._relative_luminance(rgb1)
        l2 = self._relative_luminance(rgb2)

        lighter = max(l1, l2)
        darker = min(l1, l2)

        return (lighter + 0.05) / (darker + 0.05)

    def _relative_luminance(self, rgb: tuple[int, int, int]) -> float:
        """Calculate relative luminance of a color."""
        r, g, b = rgb

        def adjust(value: int) -> float:
            v = value / 255
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    def suggest_palette(self, data: dict[str, Any]) -> str:
        """Suggest a palette preset based on data characteristics."""
        # Analyze data for emotional tone
        data_str = str(data).lower()

        if any(word in data_str for word in ["loss", "decline", "negative", "decrease"]):
            return "warm"  # Warm colors for negative trends
        elif any(word in data_str for word in ["growth", "increase", "positive", "success"]):
            return "cool"  # Cool colors for positive trends
        elif any(word in data_str for word in ["neutral", "stable", "constant"]):
            return "monochrome"

        return "default"

    def generate_categorical_colors(
        self,
        num_categories: int,
        base_hue: float = 220
    ) -> list[Color]:
        """Generate distinct colors for categorical data."""
        colors = []

        # Use golden angle for optimal distribution
        golden_angle = 137.508

        for i in range(num_categories):
            hue = (base_hue + i * golden_angle) % 360

            # Use consistent saturation and lightness
            saturation = 50
            lightness = 45

            # Convert to RGB
            r, g, b = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

            colors.append(Color(
                hex=f"#{r:02X}{g:02X}{b:02X}",
                rgb=(r, g, b),
                hsl=(hue, saturation, lightness),
                name=f"category_{i + 1}"
            ))

        return colors

    def apply_display_p3(self, color: Color) -> dict[str, Any]:
        """Convert color to Display P3 color space representation."""
        # Approximate P3 conversion (actual conversion requires ICC profiles)
        r, g, b = color.rgb

        # P3 has a wider gamut, so we scale values slightly
        p3_r = min(255, int(r * 1.02))
        p3_g = min(255, int(g * 1.02))
        p3_b = min(255, int(b * 1.02))

        return {
            "srgb": color.hex,
            "display_p3": f"color(display-p3 {p3_r / 255:.4f} {p3_g / 255:.4f} {p3_b / 255:.4f})",
            "css_fallback": f"rgb({r}, {g}, {b})"
        }
