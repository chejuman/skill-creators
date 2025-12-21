#!/usr/bin/env python3
"""
Layout Engine - Grid system and composition calculator.

Implements modular grid systems with visual entropy calculation
following Tufte's principles of graphical excellence.
"""

import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GridCell:
    """Single cell in the grid."""
    row: int
    col: int
    x: float
    y: float
    width: float
    height: float
    content_type: str = ""
    occupied: bool = False


@dataclass
class GridSpec:
    """Complete grid specification."""
    grid_type: str
    cols: int
    rows: int
    cell_width: float
    cell_height: float
    gutter: float
    margin: float
    cells: list[GridCell] = field(default_factory=list)
    utilization: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.grid_type,
            "cols": self.cols,
            "rows": self.rows,
            "cell_width": self.cell_width,
            "cell_height": self.cell_height,
            "gutter": self.gutter,
            "margin": self.margin,
            "utilization": self.utilization
        }


@dataclass
class Region:
    """Layout region for content placement."""
    name: str
    start_row: int
    start_col: int
    span_rows: int
    span_cols: int
    content_type: str


class LayoutEngine:
    """
    Grid-based layout engine for infographics.

    Features:
    - 8×8 and 12×12 modular grids
    - 9-13px responsive gutters
    - Visual entropy calculation
    - Content region allocation
    """

    # Grid configurations
    GRID_CONFIGS = {
        "8x8": {"cols": 8, "rows": 8, "gutter_range": (9, 13)},
        "12x12": {"cols": 12, "rows": 12, "gutter_range": (9, 11)}
    }

    # Standard regions
    REGIONS = {
        "header": {"start_row": 0, "span_rows": 1},
        "title": {"start_row": 0, "span_rows": 2},
        "content": {"start_row": 2, "span_rows": -2},  # -2 means "rest minus 2"
        "footer": {"start_row": -1, "span_rows": 1}
    }

    def __init__(self, margin: float = 24):
        self.margin = margin

    def calculate_grid(
        self,
        content_items: int,
        width: int,
        height: int,
        grid_type: str = "12x12"
    ) -> GridSpec:
        """Calculate optimal grid based on content requirements."""
        config = self.GRID_CONFIGS.get(grid_type, self.GRID_CONFIGS["12x12"])

        cols = config["cols"]
        rows = config["rows"]
        gutter_min, gutter_max = config["gutter_range"]

        # Calculate gutter based on available space
        available_width = width - (2 * self.margin)
        available_height = height - (2 * self.margin)

        # Optimal gutter is middle of range
        gutter = (gutter_min + gutter_max) / 2

        # Calculate cell dimensions
        total_gutter_width = (cols - 1) * gutter
        total_gutter_height = (rows - 1) * gutter

        cell_width = (available_width - total_gutter_width) / cols
        cell_height = (available_height - total_gutter_height) / rows

        # Generate cells
        cells = []
        for row in range(rows):
            for col in range(cols):
                x = self.margin + col * (cell_width + gutter)
                y = self.margin + row * (cell_height + gutter)

                cells.append(GridCell(
                    row=row,
                    col=col,
                    x=x,
                    y=y,
                    width=cell_width,
                    height=cell_height
                ))

        # Calculate utilization
        utilization = min(1.0, content_items / (cols * rows))

        return GridSpec(
            grid_type=grid_type,
            cols=cols,
            rows=rows,
            cell_width=cell_width,
            cell_height=cell_height,
            gutter=gutter,
            margin=self.margin,
            cells=cells,
            utilization=utilization
        )

    def calculate_entropy(self, grid: GridSpec) -> float:
        """
        Calculate visual entropy (Shannon density).

        Entropy should be ≤ 0.18 for optimal readability.

        Formula: H = -Σ p(x) * log2(p(x))
        where p(x) is the probability of each unique visual element.
        """
        # Count occupied vs empty cells
        total_cells = len(grid.cells)
        occupied = sum(1 for cell in grid.cells if cell.occupied)

        if total_cells == 0 or occupied == 0:
            return 0.0

        # Calculate probabilities
        p_occupied = occupied / total_cells
        p_empty = 1 - p_occupied

        # Calculate entropy
        entropy = 0.0
        if p_occupied > 0:
            entropy -= p_occupied * math.log2(p_occupied)
        if p_empty > 0:
            entropy -= p_empty * math.log2(p_empty)

        # Normalize to 0-1 range (max entropy for binary is 1.0)
        return entropy

    def allocate_regions(
        self,
        grid: GridSpec,
        regions: list[Region]
    ) -> dict[str, list[GridCell]]:
        """Allocate grid cells to named regions."""
        allocated = {}

        for region in regions:
            region_cells = []

            # Calculate actual row range
            start_row = region.start_row if region.start_row >= 0 else grid.rows + region.start_row
            span_rows = region.span_rows

            if span_rows < 0:
                span_rows = grid.rows - start_row + span_rows

            end_row = start_row + span_rows

            # Calculate actual col range
            start_col = region.start_col if region.start_col >= 0 else grid.cols + region.start_col
            end_col = start_col + region.span_cols

            # Collect cells in region
            for cell in grid.cells:
                if start_row <= cell.row < end_row and start_col <= cell.col < end_col:
                    cell.content_type = region.content_type
                    cell.occupied = True
                    region_cells.append(cell)

            allocated[region.name] = region_cells

        return allocated

    def get_region_bounds(
        self,
        cells: list[GridCell],
        gutter: float
    ) -> dict[str, float]:
        """Calculate bounding box for a set of cells."""
        if not cells:
            return {"x": 0, "y": 0, "width": 0, "height": 0}

        min_x = min(cell.x for cell in cells)
        min_y = min(cell.y for cell in cells)
        max_x = max(cell.x + cell.width for cell in cells)
        max_y = max(cell.y + cell.height for cell in cells)

        return {
            "x": min_x,
            "y": min_y,
            "width": max_x - min_x,
            "height": max_y - min_y
        }

    def suggest_grid_type(self, content_items: int) -> str:
        """Suggest optimal grid type based on content count."""
        if content_items <= 16:
            return "8x8"
        return "12x12"

    def calculate_aspect_ratio_fit(
        self,
        content_width: float,
        content_height: float,
        cell_width: float,
        cell_height: float
    ) -> tuple[float, float]:
        """Calculate dimensions that fit content while preserving aspect ratio."""
        content_ratio = content_width / content_height
        cell_ratio = cell_width / cell_height

        if content_ratio > cell_ratio:
            # Content is wider, fit to width
            fit_width = cell_width
            fit_height = cell_width / content_ratio
        else:
            # Content is taller, fit to height
            fit_height = cell_height
            fit_width = cell_height * content_ratio

        return (fit_width, fit_height)
