#!/usr/bin/env python3
"""
Infographic Design Orchestrator - Multi-Agent Coordination Engine

Orchestrates Layout, Typography, Color, and Visualization agents to generate
publication-quality infographics following Tufte principles.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# Import local modules
from layout_engine import LayoutEngine, GridSpec
from color_system import ColorSystem, Palette
from typography import TypographySystem, TypeHierarchy
from visualizations import VisualizationEngine, ChartType
from render_engine import RenderEngine
from export_handler import ExportHandler, ExportFormat


class VisualizationType(Enum):
    """Allowed visualization types (Tufte-compliant)."""
    HORIZON = "horizon"
    EULER = "euler"
    ISOMETRIC = "isometric"
    SPARKLINE = "sparkline"
    DOT_PLOT = "dot_plot"


@dataclass
class InfographicSpec:
    """Complete specification for infographic generation."""
    data: dict[str, Any]
    viz_type: VisualizationType
    title: str = ""
    subtitle: str = ""
    width: int = 1200
    height: int = 800
    grid_type: str = "12x12"
    color_palette: str = "default"
    output_format: ExportFormat = ExportFormat.WEBP

    # Tufte constraints
    max_entropy: float = 0.18
    min_data_ink_ratio: float = 0.8


@dataclass
class AgentResult:
    """Result from an agent execution."""
    agent_name: str
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)


class InfographicOrchestrator:
    """
    Multi-agent orchestrator for infographic generation.

    Coordinates:
    - Layout Agent: Grid system, spacing, composition
    - Typography Agent: Font hierarchy, readability
    - Color Agent: Palette generation, contrast
    - Visualization Agent: Chart/diagram generation
    - Export Agent: WebP/SVG output
    """

    def __init__(self, spec: InfographicSpec):
        self.spec = spec
        self.layout_engine = LayoutEngine()
        self.color_system = ColorSystem()
        self.typography = TypographySystem()
        self.viz_engine = VisualizationEngine()
        self.render_engine = RenderEngine(spec.width, spec.height)
        self.export_handler = ExportHandler()

        self.results: dict[str, AgentResult] = {}

    def run_layout_agent(self) -> AgentResult:
        """Execute Layout Agent to determine grid and composition."""
        print("[Layout Agent] Analyzing content density...")

        try:
            # Calculate content requirements
            content_items = self._count_content_items()

            # Select appropriate grid
            grid_spec = self.layout_engine.calculate_grid(
                content_items=content_items,
                width=self.spec.width,
                height=self.spec.height,
                grid_type=self.spec.grid_type
            )

            # Calculate visual entropy
            entropy = self.layout_engine.calculate_entropy(grid_spec)

            if entropy > self.spec.max_entropy:
                print(f"[Layout Agent] Warning: Entropy {entropy:.3f} exceeds threshold {self.spec.max_entropy}")

            return AgentResult(
                agent_name="layout",
                success=True,
                data={"grid": grid_spec.to_dict()},
                metrics={"entropy": entropy, "utilization": grid_spec.utilization}
            )
        except Exception as e:
            return AgentResult(
                agent_name="layout",
                success=False,
                errors=[str(e)]
            )

    def run_typography_agent(self, layout_result: AgentResult) -> AgentResult:
        """Execute Typography Agent to design text hierarchy."""
        print("[Typography Agent] Designing type hierarchy...")

        try:
            # Analyze text content
            text_elements = self._extract_text_elements()

            # Generate hierarchy
            hierarchy = self.typography.create_hierarchy(
                elements=text_elements,
                max_levels=5,
                base_size=16
            )

            # Verify readability
            readability_score = self.typography.calculate_readability(hierarchy)

            return AgentResult(
                agent_name="typography",
                success=True,
                data={"hierarchy": hierarchy.to_dict()},
                metrics={"readability": readability_score}
            )
        except Exception as e:
            return AgentResult(
                agent_name="typography",
                success=False,
                errors=[str(e)]
            )

    def run_color_agent(self) -> AgentResult:
        """Execute Color Agent to generate compliant palette."""
        print("[Color Agent] Generating 5-hue palette...")

        try:
            # Generate palette based on data characteristics
            palette = self.color_system.generate_palette(
                data=self.spec.data,
                preset=self.spec.color_palette,
                max_saturation=0.22  # Tufte constraint
            )

            # Verify WCAG contrast
            contrast_results = self.color_system.verify_contrast(palette)

            return AgentResult(
                agent_name="color",
                success=True,
                data={"palette": palette.to_dict()},
                metrics={
                    "min_contrast": contrast_results["min_ratio"],
                    "wcag_aa_pass": 1.0 if contrast_results["aa_compliant"] else 0.0
                }
            )
        except Exception as e:
            return AgentResult(
                agent_name="color",
                success=False,
                errors=[str(e)]
            )

    def run_visualization_agent(
        self,
        layout_result: AgentResult,
        color_result: AgentResult
    ) -> AgentResult:
        """Execute Visualization Agent to generate chart/diagram."""
        print(f"[Visualization Agent] Creating {self.spec.viz_type.value} visualization...")

        try:
            # Validate visualization type is allowed
            if self.spec.viz_type not in VisualizationType:
                raise ValueError(f"Banned chart type: {self.spec.viz_type}")

            # Generate visualization
            viz_data = self.viz_engine.generate(
                data=self.spec.data,
                chart_type=ChartType(self.spec.viz_type.value),
                grid=layout_result.data.get("grid", {}),
                palette=color_result.data.get("palette", {})
            )

            # Calculate data-ink ratio
            data_ink_ratio = self.viz_engine.calculate_data_ink_ratio(viz_data)

            if data_ink_ratio < self.spec.min_data_ink_ratio:
                print(f"[Visualization Agent] Warning: Data-ink ratio {data_ink_ratio:.2f} below threshold")

            return AgentResult(
                agent_name="visualization",
                success=True,
                data={"visualization": viz_data},
                metrics={"data_ink_ratio": data_ink_ratio}
            )
        except Exception as e:
            return AgentResult(
                agent_name="visualization",
                success=False,
                errors=[str(e)]
            )

    def run_export_agent(
        self,
        all_results: dict[str, AgentResult],
        output_path: Path
    ) -> AgentResult:
        """Execute Export Agent to render and save output."""
        print(f"[Export Agent] Rendering to {self.spec.output_format.value}...")

        try:
            # Compose all elements
            self.render_engine.compose(
                layout=all_results["layout"].data.get("grid", {}),
                typography=all_results["typography"].data.get("hierarchy", {}),
                colors=all_results["color"].data.get("palette", {}),
                visualization=all_results["visualization"].data.get("visualization", {}),
                title=self.spec.title,
                subtitle=self.spec.subtitle
            )

            # Export to specified format
            export_result = self.export_handler.export(
                surface=self.render_engine.surface,
                output_path=output_path,
                format=self.spec.output_format,
                quality=100,
                color_profile="Display P3"
            )

            return AgentResult(
                agent_name="export",
                success=True,
                data={"output_path": str(output_path)},
                metrics={"file_size_kb": export_result.get("size_kb", 0)}
            )
        except Exception as e:
            return AgentResult(
                agent_name="export",
                success=False,
                errors=[str(e)]
            )

    def orchestrate(self, output_path: Path) -> dict[str, Any]:
        """Run complete multi-agent workflow."""
        print("=" * 60)
        print("INFOGRAPHIC DESIGN ORCHESTRATOR")
        print("=" * 60)
        print(f"Type: {self.spec.viz_type.value}")
        print(f"Dimensions: {self.spec.width}x{self.spec.height}")
        print(f"Output: {output_path}")
        print("=" * 60)

        # Phase 1: Layout Agent
        self.results["layout"] = self.run_layout_agent()
        if not self.results["layout"].success:
            return self._build_error_report("layout")

        # Phase 2: Typography Agent (depends on layout)
        self.results["typography"] = self.run_typography_agent(self.results["layout"])
        if not self.results["typography"].success:
            return self._build_error_report("typography")

        # Phase 3: Color Agent (independent)
        self.results["color"] = self.run_color_agent()
        if not self.results["color"].success:
            return self._build_error_report("color")

        # Phase 4: Visualization Agent (depends on layout + color)
        self.results["visualization"] = self.run_visualization_agent(
            self.results["layout"],
            self.results["color"]
        )
        if not self.results["visualization"].success:
            return self._build_error_report("visualization")

        # Phase 5: Export Agent
        self.results["export"] = self.run_export_agent(self.results, output_path)
        if not self.results["export"].success:
            return self._build_error_report("export")

        return self._build_success_report()

    def _count_content_items(self) -> int:
        """Count data items for layout calculation."""
        if isinstance(self.spec.data, dict):
            return sum(
                len(v) if isinstance(v, (list, dict)) else 1
                for v in self.spec.data.values()
            )
        elif isinstance(self.spec.data, list):
            return len(self.spec.data)
        return 1

    def _extract_text_elements(self) -> list[dict]:
        """Extract text elements from specification."""
        elements = []
        if self.spec.title:
            elements.append({"text": self.spec.title, "level": 1})
        if self.spec.subtitle:
            elements.append({"text": self.spec.subtitle, "level": 2})
        # Extract labels from data
        if isinstance(self.spec.data, dict):
            for key in self.spec.data.keys():
                elements.append({"text": str(key), "level": 4})
        return elements

    def _build_error_report(self, failed_agent: str) -> dict[str, Any]:
        """Build error report for failed orchestration."""
        return {
            "success": False,
            "failed_agent": failed_agent,
            "errors": self.results[failed_agent].errors,
            "completed_agents": [
                name for name, result in self.results.items()
                if result.success
            ]
        }

    def _build_success_report(self) -> dict[str, Any]:
        """Build success report with all metrics."""
        metrics = {}
        for name, result in self.results.items():
            metrics[name] = result.metrics

        return {
            "success": True,
            "output_path": self.results["export"].data.get("output_path"),
            "metrics": metrics,
            "validation": {
                "entropy": metrics.get("layout", {}).get("entropy", 0),
                "data_ink_ratio": metrics.get("visualization", {}).get("data_ink_ratio", 0),
                "wcag_compliant": metrics.get("color", {}).get("wcag_aa_pass", 0) == 1.0,
                "readability": metrics.get("typography", {}).get("readability", 0)
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate Tufte-compliant infographics"
    )
    parser.add_argument(
        "--data", "-d",
        required=True,
        help="Path to JSON data file"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["horizon", "euler", "isometric", "sparkline", "dot_plot"],
        default="horizon",
        help="Visualization type"
    )
    parser.add_argument(
        "--title",
        default="",
        help="Infographic title"
    )
    parser.add_argument(
        "--subtitle",
        default="",
        help="Infographic subtitle"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1200,
        help="Width in pixels"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=800,
        help="Height in pixels"
    )
    parser.add_argument(
        "--grid",
        choices=["8x8", "12x12"],
        default="12x12",
        help="Grid system"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["webp", "svg", "png"],
        default="webp",
        help="Output format"
    )

    args = parser.parse_args()

    # Load data
    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: Data file not found: {data_path}")
        sys.exit(1)

    with open(data_path) as f:
        data = json.load(f)

    # Create specification
    spec = InfographicSpec(
        data=data,
        viz_type=VisualizationType(args.type),
        title=args.title,
        subtitle=args.subtitle,
        width=args.width,
        height=args.height,
        grid_type=args.grid,
        output_format=ExportFormat(args.format)
    )

    # Run orchestrator
    orchestrator = InfographicOrchestrator(spec)
    result = orchestrator.orchestrate(Path(args.output))

    # Output result
    print("\n" + "=" * 60)
    if result["success"]:
        print("SUCCESS: Infographic generated")
        print(f"Output: {result['output_path']}")
        print("\nValidation Metrics:")
        for key, value in result["validation"].items():
            status = "PASS" if (
                (key == "entropy" and value <= 0.18) or
                (key == "data_ink_ratio" and value >= 0.8) or
                (key in ["wcag_compliant", "readability"] and value)
            ) else "WARN"
            print(f"  [{status}] {key}: {value}")
    else:
        print(f"FAILED: {result['failed_agent']} agent")
        for error in result["errors"]:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
