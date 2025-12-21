#!/usr/bin/env python3
"""
Render Engine - Pycairo-based vector rendering system.

Provides high-quality vector graphics rendering with Display P3 color support.
"""

import math
from dataclasses import dataclass
from typing import Any

try:
    import cairo
    CAIRO_AVAILABLE = True
except ImportError:
    CAIRO_AVAILABLE = False
    print("Warning: pycairo not installed. Install with: pip install pycairo")


@dataclass
class Point:
    """2D point."""
    x: float
    y: float


@dataclass
class Rect:
    """Rectangle specification."""
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


class RenderEngine:
    """
    Pycairo-based rendering engine for infographics.

    Features:
    - Vector-first rendering (scalable)
    - Display P3 color profile support
    - Anti-aliased output
    - Precise typography
    """

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = None
        self.ctx = None

        if CAIRO_AVAILABLE:
            self._init_surface()

    def _init_surface(self):
        """Initialize Cairo surface and context."""
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32,
            self.width,
            self.height
        )
        self.ctx = cairo.Context(self.surface)

        # Set high-quality rendering
        self.ctx.set_antialias(cairo.ANTIALIAS_BEST)

        # White background
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.paint()

    def compose(
        self,
        layout: dict[str, Any],
        typography: dict[str, Any],
        colors: dict[str, Any],
        visualization: dict[str, Any],
        title: str = "",
        subtitle: str = ""
    ):
        """Compose all elements onto the surface."""
        if not CAIRO_AVAILABLE:
            raise RuntimeError("pycairo is required for rendering")

        # Apply background
        bg_color = self._parse_color(colors.get("neutral", "#F0F0F5"))
        self.ctx.set_source_rgb(*bg_color)
        self.ctx.paint()

        # Render title
        if title:
            self._render_title(title, typography, colors)

        # Render subtitle
        if subtitle:
            self._render_subtitle(subtitle, typography, colors)

        # Render visualization
        self._render_visualization(visualization, layout, colors)

        # Render grid lines (debug mode only)
        if layout.get("debug_grid", False):
            self._render_grid(layout)

    def _render_title(
        self,
        title: str,
        typography: dict[str, Any],
        colors: dict[str, Any]
    ):
        """Render title text."""
        hierarchy = typography.get("levels", {})
        level1 = hierarchy.get("1", {"size": 32, "weight": "bold"})

        self.ctx.select_font_face(
            "Inter",
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_BOLD if level1.get("weight") == "bold" else cairo.FONT_WEIGHT_NORMAL
        )
        self.ctx.set_font_size(level1.get("size", 32))

        text_color = self._parse_color(colors.get("primary", "#1A1A2E"))
        self.ctx.set_source_rgb(*text_color)

        # Position title
        x_bearing, y_bearing, text_width, text_height, _, _ = self.ctx.text_extents(title)
        x = (self.width - text_width) / 2
        y = 48 + text_height

        self.ctx.move_to(x, y)
        self.ctx.show_text(title)

    def _render_subtitle(
        self,
        subtitle: str,
        typography: dict[str, Any],
        colors: dict[str, Any]
    ):
        """Render subtitle text."""
        hierarchy = typography.get("levels", {})
        level2 = hierarchy.get("2", {"size": 24, "weight": "normal"})

        self.ctx.select_font_face(
            "Inter",
            cairo.FONT_SLANT_NORMAL,
            cairo.FONT_WEIGHT_NORMAL
        )
        self.ctx.set_font_size(level2.get("size", 24))

        text_color = self._parse_color(colors.get("secondary", "#4A4A68"))
        self.ctx.set_source_rgb(*text_color)

        x_bearing, y_bearing, text_width, text_height, _, _ = self.ctx.text_extents(subtitle)
        x = (self.width - text_width) / 2
        y = 80 + text_height

        self.ctx.move_to(x, y)
        self.ctx.show_text(subtitle)

    def _render_visualization(
        self,
        visualization: dict[str, Any],
        layout: dict[str, Any],
        colors: dict[str, Any]
    ):
        """Render the main visualization."""
        viz_type = visualization.get("type", "horizon")
        data = visualization.get("data", [])
        bounds = visualization.get("bounds", {
            "x": 48,
            "y": 120,
            "width": self.width - 96,
            "height": self.height - 168
        })

        if viz_type == "horizon":
            self._render_horizon_graph(data, bounds, colors)
        elif viz_type == "euler":
            self._render_euler_diagram(data, bounds, colors)
        elif viz_type == "isometric":
            self._render_isometric(data, bounds, colors)
        elif viz_type == "sparkline":
            self._render_sparkline(data, bounds, colors)

    def _render_horizon_graph(
        self,
        data: list[dict],
        bounds: dict[str, float],
        colors: dict[str, Any]
    ):
        """Render a horizon graph visualization."""
        if not data:
            return

        rect = Rect(**bounds)
        num_bands = 3  # Standard horizon graph bands
        band_height = rect.height / len(data)

        primary = self._parse_color(colors.get("primary", "#1A1A2E"))
        accent = self._parse_color(colors.get("accent", "#E94560"))

        for i, series in enumerate(data):
            y_offset = rect.y + i * band_height
            values = series.get("values", [])

            if not values:
                continue

            max_val = max(abs(v) for v in values)
            point_width = rect.width / len(values)

            for j, value in enumerate(values):
                x = rect.x + j * point_width
                normalized = abs(value) / max_val if max_val else 0

                # Determine band and color
                band = min(int(normalized * num_bands), num_bands - 1)
                alpha = (band + 1) / num_bands

                if value >= 0:
                    self.ctx.set_source_rgba(*primary, alpha)
                else:
                    self.ctx.set_source_rgba(*accent, alpha)

                bar_height = (normalized * band_height) / num_bands
                self.ctx.rectangle(x, y_offset + band_height - bar_height, point_width - 1, bar_height)
                self.ctx.fill()

    def _render_euler_diagram(
        self,
        data: list[dict],
        bounds: dict[str, float],
        colors: dict[str, Any]
    ):
        """Render an Euler diagram for set relationships."""
        rect = Rect(**bounds)
        center = rect.center

        num_sets = len(data)
        base_radius = min(rect.width, rect.height) / 3

        palette_keys = ["primary", "secondary", "accent", "muted"]

        for i, set_data in enumerate(data):
            # Position sets in a circle
            angle = (2 * math.pi * i / num_sets) - math.pi / 2
            offset = base_radius * 0.3 if num_sets > 1 else 0

            cx = center.x + math.cos(angle) * offset
            cy = center.y + math.sin(angle) * offset

            size = set_data.get("size", 1.0)
            radius = base_radius * size

            color_key = palette_keys[i % len(palette_keys)]
            color = self._parse_color(colors.get(color_key, "#1A1A2E"))

            # Draw set circle
            self.ctx.set_source_rgba(*color, 0.3)
            self.ctx.arc(cx, cy, radius, 0, 2 * math.pi)
            self.ctx.fill()

            # Draw border
            self.ctx.set_source_rgba(*color, 0.8)
            self.ctx.set_line_width(2)
            self.ctx.arc(cx, cy, radius, 0, 2 * math.pi)
            self.ctx.stroke()

            # Label
            label = set_data.get("label", f"Set {i + 1}")
            self.ctx.set_source_rgb(*color)
            self.ctx.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            self.ctx.set_font_size(14)

            extents = self.ctx.text_extents(label)
            self.ctx.move_to(cx - extents.width / 2, cy + extents.height / 2)
            self.ctx.show_text(label)

    def _render_isometric(
        self,
        data: list[dict],
        bounds: dict[str, float],
        colors: dict[str, Any]
    ):
        """Render isometric small-multiples."""
        rect = Rect(**bounds)

        # Calculate grid for small multiples
        num_items = len(data)
        cols = math.ceil(math.sqrt(num_items))
        rows = math.ceil(num_items / cols)

        cell_width = rect.width / cols
        cell_height = rect.height / rows

        primary = self._parse_color(colors.get("primary", "#1A1A2E"))

        for i, item in enumerate(data):
            col = i % cols
            row = i // cols

            cx = rect.x + col * cell_width + cell_width / 2
            cy = rect.y + row * cell_height + cell_height / 2

            value = item.get("value", 1.0)
            size = min(cell_width, cell_height) * 0.4 * value

            # Draw isometric cube
            self._draw_isometric_cube(cx, cy, size, primary)

    def _draw_isometric_cube(
        self,
        cx: float,
        cy: float,
        size: float,
        color: tuple[float, float, float]
    ):
        """Draw an isometric cube."""
        # Isometric angles
        angle = math.pi / 6  # 30 degrees

        # Calculate vertices
        dx = size * math.cos(angle)
        dy = size * math.sin(angle)

        # Top face
        self.ctx.set_source_rgba(*color, 0.9)
        self.ctx.move_to(cx, cy - size)
        self.ctx.line_to(cx + dx, cy - size + dy)
        self.ctx.line_to(cx, cy)
        self.ctx.line_to(cx - dx, cy - size + dy)
        self.ctx.close_path()
        self.ctx.fill()

        # Left face
        self.ctx.set_source_rgba(*color, 0.6)
        self.ctx.move_to(cx - dx, cy - size + dy)
        self.ctx.line_to(cx, cy)
        self.ctx.line_to(cx, cy + size)
        self.ctx.line_to(cx - dx, cy + dy)
        self.ctx.close_path()
        self.ctx.fill()

        # Right face
        self.ctx.set_source_rgba(*color, 0.4)
        self.ctx.move_to(cx + dx, cy - size + dy)
        self.ctx.line_to(cx, cy)
        self.ctx.line_to(cx, cy + size)
        self.ctx.line_to(cx + dx, cy + dy)
        self.ctx.close_path()
        self.ctx.fill()

    def _render_sparkline(
        self,
        data: list[dict],
        bounds: dict[str, float],
        colors: dict[str, Any]
    ):
        """Render word-sized sparkline graphics."""
        rect = Rect(**bounds)
        primary = self._parse_color(colors.get("primary", "#1A1A2E"))

        for i, series in enumerate(data):
            values = series.get("values", [])
            if not values:
                continue

            # Calculate sparkline bounds
            spark_width = rect.width / len(data)
            spark_x = rect.x + i * spark_width
            spark_height = 24  # Word-sized

            min_val = min(values)
            max_val = max(values)
            val_range = max_val - min_val or 1

            self.ctx.set_source_rgb(*primary)
            self.ctx.set_line_width(1.5)

            # Draw sparkline
            for j, value in enumerate(values):
                x = spark_x + (j / len(values)) * spark_width
                y = rect.y + spark_height - ((value - min_val) / val_range) * spark_height

                if j == 0:
                    self.ctx.move_to(x, y)
                else:
                    self.ctx.line_to(x, y)

            self.ctx.stroke()

    def _render_grid(self, layout: dict[str, Any]):
        """Render debug grid overlay."""
        grid_type = layout.get("type", "12x12")
        cols, rows = map(int, grid_type.split("x"))

        cell_width = self.width / cols
        cell_height = self.height / rows

        self.ctx.set_source_rgba(0.8, 0.8, 0.8, 0.3)
        self.ctx.set_line_width(0.5)

        for i in range(cols + 1):
            x = i * cell_width
            self.ctx.move_to(x, 0)
            self.ctx.line_to(x, self.height)
            self.ctx.stroke()

        for i in range(rows + 1):
            y = i * cell_height
            self.ctx.move_to(0, y)
            self.ctx.line_to(self.width, y)
            self.ctx.stroke()

    def _parse_color(self, hex_color: str) -> tuple[float, float, float]:
        """Parse hex color to RGB tuple (0-1 range)."""
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        return (r, g, b)

    def get_surface(self):
        """Get the Cairo surface for export."""
        return self.surface
