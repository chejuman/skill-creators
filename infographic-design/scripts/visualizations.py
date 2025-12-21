#!/usr/bin/env python3
"""
Visualization Engine - Tufte-compliant chart generation.

Implements horizon graphs, Euler diagrams, isometric small-multiples,
and sparklines. Explicitly bans bar charts and pie charts.
"""

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ChartType(Enum):
    """Allowed visualization types (Tufte-compliant)."""
    HORIZON = "horizon"
    EULER = "euler"
    ISOMETRIC = "isometric"
    SPARKLINE = "sparkline"
    DOT_PLOT = "dot_plot"


# Explicitly banned chart types
BANNED_CHARTS = frozenset([
    "bar", "bar_chart", "column", "column_chart",
    "pie", "pie_chart", "donut", "doughnut",
    "3d", "3d_bar", "3d_pie"
])


@dataclass
class VisualizationSpec:
    """Specification for a visualization."""
    chart_type: ChartType
    data: list[dict[str, Any]]
    bounds: dict[str, float]
    options: dict[str, Any]


@dataclass
class RenderInstruction:
    """Rendering instruction for the render engine."""
    operation: str  # "path", "arc", "rect", "text"
    params: dict[str, Any]
    style: dict[str, Any]


class VisualizationEngine:
    """
    Visualization engine for Tufte-compliant charts.

    Allowed:
    - Horizon graphs (time series)
    - Euler diagrams (set relationships)
    - Isometric small-multiples (comparisons)
    - Sparklines (inline data)
    - Dot plots (distributions)

    Banned:
    - Bar charts
    - Pie charts
    - 3D effects
    - Gradient fills
    """

    # Axis styling
    AXIS_STYLE = {
        "hairline_width": 0.5,
        "label_rotation": 45,
        "tick_length": 4,
        "scale": "logarithmic"
    }

    def __init__(self):
        self.instructions: list[RenderInstruction] = []

    def generate(
        self,
        data: dict[str, Any],
        chart_type: ChartType,
        grid: dict[str, Any],
        palette: dict[str, str]
    ) -> dict[str, Any]:
        """Generate visualization data structure."""
        self._validate_chart_type(chart_type)
        self.instructions = []

        # Normalize data to list format
        if isinstance(data, dict):
            if "series" in data:
                data_list = data["series"]
            elif "sets" in data:
                data_list = data["sets"]
            elif "values" in data:
                data_list = [{"values": data["values"]}]
            else:
                data_list = [{"values": list(data.values())}]
        elif isinstance(data, list):
            data_list = data
        else:
            data_list = []

        # Calculate bounds
        bounds = self._calculate_bounds(grid)

        # Generate based on type
        if chart_type == ChartType.HORIZON:
            viz_data = self._generate_horizon(data_list, bounds, palette)
        elif chart_type == ChartType.EULER:
            viz_data = self._generate_euler(data_list, bounds, palette)
        elif chart_type == ChartType.ISOMETRIC:
            viz_data = self._generate_isometric(data_list, bounds, palette)
        elif chart_type == ChartType.SPARKLINE:
            viz_data = self._generate_sparkline(data_list, bounds, palette)
        elif chart_type == ChartType.DOT_PLOT:
            viz_data = self._generate_dot_plot(data_list, bounds, palette)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        return viz_data

    def _validate_chart_type(self, chart_type: ChartType | str):
        """Validate chart type is not banned."""
        type_str = chart_type.value if isinstance(chart_type, ChartType) else str(chart_type)

        if type_str.lower() in BANNED_CHARTS:
            raise ValueError(
                f"Chart type '{type_str}' is banned. "
                f"Use horizon, euler, isometric, or sparkline instead."
            )

    def _calculate_bounds(self, grid: dict[str, Any]) -> dict[str, float]:
        """Calculate visualization bounds from grid."""
        margin = grid.get("margin", 24)
        cell_width = grid.get("cell_width", 100)
        cell_height = grid.get("cell_height", 100)
        cols = grid.get("cols", 12)
        rows = grid.get("rows", 12)

        # Reserve top 2 rows for title/subtitle
        content_start_row = 2
        content_end_row = rows - 1

        return {
            "x": margin,
            "y": margin + content_start_row * cell_height,
            "width": cols * cell_width,
            "height": (content_end_row - content_start_row) * cell_height
        }

    def _generate_horizon(
        self,
        data: list[dict],
        bounds: dict[str, float],
        palette: dict[str, str]
    ) -> dict[str, Any]:
        """Generate horizon graph visualization."""
        num_bands = 3  # Standard horizon graph uses 3 bands
        band_colors = self._generate_band_colors(palette.get("primary", "#1A1A2E"), num_bands)

        return {
            "type": "horizon",
            "data": data,
            "bounds": bounds,
            "config": {
                "num_bands": num_bands,
                "band_colors": band_colors,
                "mirror_negative": True,
                "scale": self.AXIS_STYLE["scale"]
            }
        }

    def _generate_euler(
        self,
        data: list[dict],
        bounds: dict[str, float],
        palette: dict[str, str]
    ) -> dict[str, Any]:
        """Generate Euler diagram visualization."""
        return {
            "type": "euler",
            "data": data,
            "bounds": bounds,
            "config": {
                "fill_opacity": 0.3,
                "stroke_width": 2,
                "label_position": "center"
            }
        }

    def _generate_isometric(
        self,
        data: list[dict],
        bounds: dict[str, float],
        palette: dict[str, str]
    ) -> dict[str, Any]:
        """Generate isometric small-multiples visualization."""
        # Calculate grid for small multiples
        num_items = len(data)
        cols = math.ceil(math.sqrt(num_items))
        rows = math.ceil(num_items / cols)

        return {
            "type": "isometric",
            "data": data,
            "bounds": bounds,
            "config": {
                "grid_cols": cols,
                "grid_rows": rows,
                "iso_angle": 30,
                "cube_style": True
            }
        }

    def _generate_sparkline(
        self,
        data: list[dict],
        bounds: dict[str, float],
        palette: dict[str, str]
    ) -> dict[str, Any]:
        """Generate sparkline visualization (word-sized graphics)."""
        return {
            "type": "sparkline",
            "data": data,
            "bounds": bounds,
            "config": {
                "line_width": 1.5,
                "height": 24,  # Word-sized
                "show_endpoints": True,
                "show_min_max": False
            }
        }

    def _generate_dot_plot(
        self,
        data: list[dict],
        bounds: dict[str, float],
        palette: dict[str, str]
    ) -> dict[str, Any]:
        """Generate dot plot visualization."""
        return {
            "type": "dot_plot",
            "data": data,
            "bounds": bounds,
            "config": {
                "dot_radius": 4,
                "dot_spacing": 8,
                "stack_direction": "horizontal"
            }
        }

    def _generate_band_colors(
        self,
        base_color: str,
        num_bands: int
    ) -> list[str]:
        """Generate band colors for horizon graph."""
        colors = []
        for i in range(num_bands):
            alpha = (i + 1) / num_bands
            colors.append(f"{base_color}{int(alpha * 255):02X}")
        return colors

    def calculate_data_ink_ratio(self, viz_data: dict[str, Any]) -> float:
        """
        Calculate data-ink ratio (Tufte metric).

        Ratio = Data ink / Total ink
        Goal: ≥ 0.8 (80% of ink shows data)
        """
        data = viz_data.get("data", [])
        bounds = viz_data.get("bounds", {})
        config = viz_data.get("config", {})

        # Estimate total visual area
        total_area = bounds.get("width", 0) * bounds.get("height", 0)
        if total_area == 0:
            return 0.0

        # Estimate data ink based on chart type
        viz_type = viz_data.get("type", "")

        if viz_type == "horizon":
            # Horizon graphs are very data-dense
            data_points = sum(len(s.get("values", [])) for s in data)
            data_ink_estimate = data_points * 4  # Approximate pixels per point

        elif viz_type == "euler":
            # Euler diagrams use fill and stroke
            num_sets = len(data)
            avg_radius = min(bounds.get("width", 0), bounds.get("height", 0)) / 3
            data_ink_estimate = num_sets * math.pi * avg_radius * 2  # Circumference

        elif viz_type == "isometric":
            # Isometric cubes are data-dense
            num_items = len(data)
            cube_size = 40  # Approximate
            data_ink_estimate = num_items * (cube_size ** 2) * 0.5

        elif viz_type == "sparkline":
            # Sparklines are minimal
            data_points = sum(len(s.get("values", [])) for s in data)
            line_width = config.get("line_width", 1.5)
            data_ink_estimate = data_points * line_width

        else:
            data_ink_estimate = 0

        # Calculate ratio
        # Non-data ink includes: margins, axes, labels (minimal in Tufte style)
        non_data_ink = total_area * 0.1  # Estimate 10% for axes/labels

        data_ink_ratio = data_ink_estimate / (data_ink_estimate + non_data_ink)

        return min(1.0, max(0.0, data_ink_ratio))

    def generate_axis(
        self,
        orientation: str,  # "x" or "y"
        bounds: dict[str, float],
        scale: str = "logarithmic",
        ticks: list[float] | None = None
    ) -> list[RenderInstruction]:
        """Generate minimal axis with hairlines."""
        instructions = []

        style = {
            "stroke_width": self.AXIS_STYLE["hairline_width"],
            "stroke_color": "#9090A0"
        }

        if orientation == "x":
            # Horizontal axis line
            instructions.append(RenderInstruction(
                operation="path",
                params={
                    "start": (bounds["x"], bounds["y"] + bounds["height"]),
                    "end": (bounds["x"] + bounds["width"], bounds["y"] + bounds["height"])
                },
                style=style
            ))
        else:
            # Vertical axis line
            instructions.append(RenderInstruction(
                operation="path",
                params={
                    "start": (bounds["x"], bounds["y"]),
                    "end": (bounds["x"], bounds["y"] + bounds["height"])
                },
                style=style
            ))

        return instructions
