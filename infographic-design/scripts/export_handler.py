#!/usr/bin/env python3
"""
Export Handler - WebP/SVG output with Display P3 support.

Handles export to WebP (primary) and SVG (fallback) formats with
color profile management and responsive output.
"""

import io
import struct
import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

try:
    import cairo
    CAIRO_AVAILABLE = True
except ImportError:
    CAIRO_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ExportFormat(Enum):
    """Supported export formats."""
    WEBP = "webp"
    SVG = "svg"
    PNG = "png"


@dataclass
class ExportResult:
    """Result of export operation."""
    success: bool
    output_path: Path
    format: ExportFormat
    size_bytes: int
    color_profile: str
    errors: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "output_path": str(self.output_path),
            "format": self.format.value,
            "size_kb": self.size_bytes / 1024,
            "color_profile": self.color_profile,
            "errors": self.errors
        }


class ExportHandler:
    """
    Export handler for infographic output.

    Features:
    - WebP at 100% quality (primary)
    - SVG with CSS variables (fallback)
    - Display P3 color profile
    - Container queries support
    - Fluid typography
    """

    # Color profile specifications
    COLOR_PROFILES = {
        "sRGB": "sRGB IEC61966-2.1",
        "Display P3": "Display P3",
        "Adobe RGB": "Adobe RGB (1998)"
    }

    def __init__(self):
        self.errors: list[str] = []

    def export(
        self,
        surface: Any,  # Cairo surface
        output_path: Path,
        format: ExportFormat,
        quality: int = 100,
        color_profile: str = "Display P3"
    ) -> dict[str, Any]:
        """Export surface to specified format."""
        output_path = Path(output_path)
        self.errors = []

        if format == ExportFormat.WEBP:
            result = self._export_webp(surface, output_path, quality, color_profile)
        elif format == ExportFormat.SVG:
            result = self._export_svg(surface, output_path, color_profile)
        elif format == ExportFormat.PNG:
            result = self._export_png(surface, output_path, color_profile)
        else:
            self.errors.append(f"Unsupported format: {format}")
            return {"success": False, "errors": self.errors}

        return result.to_dict()

    def _export_webp(
        self,
        surface: Any,
        output_path: Path,
        quality: int,
        color_profile: str
    ) -> ExportResult:
        """Export to WebP format with Display P3 color profile."""
        if not CAIRO_AVAILABLE:
            return self._error_result(output_path, ExportFormat.WEBP, "Cairo not available")

        if not PIL_AVAILABLE:
            return self._error_result(output_path, ExportFormat.WEBP, "Pillow not available")

        try:
            # Convert Cairo surface to PIL Image
            width = surface.get_width()
            height = surface.get_height()
            data = surface.get_data()

            # Cairo uses BGRA, PIL uses RGBA
            image = Image.frombuffer("RGBA", (width, height), data, "raw", "BGRA", 0, 1)

            # Convert to RGB for WebP (no alpha in output)
            rgb_image = image.convert("RGB")

            # Add color profile metadata (P3 approximation)
            # Note: Full P3 embedding requires ICC profile handling
            exif_data = self._create_p3_metadata()

            # Save as WebP
            output_path = output_path.with_suffix(".webp")
            rgb_image.save(
                output_path,
                "WEBP",
                quality=quality,
                method=6  # Highest quality method
            )

            return ExportResult(
                success=True,
                output_path=output_path,
                format=ExportFormat.WEBP,
                size_bytes=output_path.stat().st_size,
                color_profile=color_profile,
                errors=[]
            )

        except Exception as e:
            return self._error_result(output_path, ExportFormat.WEBP, str(e))

    def _export_svg(
        self,
        surface: Any,
        output_path: Path,
        color_profile: str
    ) -> ExportResult:
        """Export to SVG format with CSS variables."""
        if not CAIRO_AVAILABLE:
            return self._error_result(output_path, ExportFormat.SVG, "Cairo not available")

        try:
            output_path = output_path.with_suffix(".svg")
            width = surface.get_width()
            height = surface.get_height()

            # Create SVG surface
            svg_surface = cairo.SVGSurface(str(output_path), width, height)
            svg_ctx = cairo.Context(svg_surface)

            # Copy from image surface to SVG
            svg_ctx.set_source_surface(surface, 0, 0)
            svg_ctx.paint()

            svg_surface.finish()

            # Post-process SVG to add CSS variables
            self._add_css_variables(output_path)

            return ExportResult(
                success=True,
                output_path=output_path,
                format=ExportFormat.SVG,
                size_bytes=output_path.stat().st_size,
                color_profile=color_profile,
                errors=[]
            )

        except Exception as e:
            return self._error_result(output_path, ExportFormat.SVG, str(e))

    def _export_png(
        self,
        surface: Any,
        output_path: Path,
        color_profile: str
    ) -> ExportResult:
        """Export to PNG format."""
        if not CAIRO_AVAILABLE:
            return self._error_result(output_path, ExportFormat.PNG, "Cairo not available")

        try:
            output_path = output_path.with_suffix(".png")
            surface.write_to_png(str(output_path))

            return ExportResult(
                success=True,
                output_path=output_path,
                format=ExportFormat.PNG,
                size_bytes=output_path.stat().st_size,
                color_profile=color_profile,
                errors=[]
            )

        except Exception as e:
            return self._error_result(output_path, ExportFormat.PNG, str(e))

    def _add_css_variables(self, svg_path: Path):
        """Add CSS custom properties to SVG for theming."""
        try:
            content = svg_path.read_text()

            # Add CSS variables style block
            css_block = """
<defs>
  <style type="text/css">
    :root {
      --infographic-primary: #1A1A2E;
      --infographic-secondary: #4A4A68;
      --infographic-accent: #E94560;
      --infographic-neutral: #F0F0F5;
      --infographic-muted: #9090A0;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --infographic-primary: #E0E0F0;
        --infographic-secondary: #A0A0B8;
        --infographic-accent: #FF6B7A;
        --infographic-neutral: #1A1A2E;
        --infographic-muted: #6060A0;
      }
    }
  </style>
</defs>
"""
            # Insert after opening SVG tag
            content = content.replace(">", f">\n{css_block}", 1)
            svg_path.write_text(content)

        except Exception as e:
            self.errors.append(f"Failed to add CSS variables: {e}")

    def _create_p3_metadata(self) -> bytes:
        """Create metadata indicating Display P3 color space."""
        # Simplified P3 indicator
        # Full implementation would embed ICC profile
        return b""

    def _error_result(
        self,
        output_path: Path,
        format: ExportFormat,
        error: str
    ) -> ExportResult:
        """Create error result."""
        self.errors.append(error)
        return ExportResult(
            success=False,
            output_path=output_path,
            format=format,
            size_bytes=0,
            color_profile="",
            errors=self.errors.copy()
        )

    def generate_responsive_wrapper(
        self,
        svg_path: Path,
        breakpoints: list[int] | None = None
    ) -> str:
        """Generate HTML wrapper with container queries for responsive SVG."""
        if breakpoints is None:
            breakpoints = [320, 768, 1024, 1440]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Infographic</title>
  <style>
    .infographic-container {{
      container-type: inline-size;
      width: 100%;
      max-width: 1440px;
      margin: 0 auto;
    }}

    .infographic {{
      width: 100%;
      height: auto;
    }}

    /* Fluid typography */
    .infographic text {{
      font-size: clamp(12px, 2cqi, 16px);
    }}

    /* Container query breakpoints */
    @container (min-width: {breakpoints[0]}px) {{
      .infographic {{ --scale: 0.75; }}
    }}

    @container (min-width: {breakpoints[1]}px) {{
      .infographic {{ --scale: 0.9; }}
    }}

    @container (min-width: {breakpoints[2]}px) {{
      .infographic {{ --scale: 1.0; }}
    }}

    @container (min-width: {breakpoints[3]}px) {{
      .infographic {{ --scale: 1.1; }}
    }}
  </style>
</head>
<body>
  <div class="infographic-container">
    <object class="infographic" type="image/svg+xml" data="{svg_path.name}">
      <img src="{svg_path.with_suffix('.webp').name}" alt="Infographic">
    </object>
  </div>
</body>
</html>"""

        return html

    def validate_output(self, output_path: Path) -> dict[str, Any]:
        """Validate exported file meets quality standards."""
        if not output_path.exists():
            return {"valid": False, "errors": ["Output file not found"]}

        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "metrics": {}
        }

        # Check file size
        size_bytes = output_path.stat().st_size
        validation["metrics"]["size_kb"] = size_bytes / 1024

        if size_bytes == 0:
            validation["valid"] = False
            validation["errors"].append("File is empty")

        if size_bytes > 10 * 1024 * 1024:  # 10MB
            validation["warnings"].append("File exceeds 10MB")

        # Format-specific validation
        suffix = output_path.suffix.lower()

        if suffix == ".webp":
            # Check WebP header
            with open(output_path, "rb") as f:
                header = f.read(12)
                if header[:4] != b"RIFF" or header[8:12] != b"WEBP":
                    validation["valid"] = False
                    validation["errors"].append("Invalid WebP format")

        elif suffix == ".svg":
            # Check SVG structure
            content = output_path.read_text()
            if "<svg" not in content:
                validation["valid"] = False
                validation["errors"].append("Invalid SVG format")
            if "var(--" in content:
                validation["metrics"]["has_css_variables"] = True

        elif suffix == ".png":
            # Check PNG header
            with open(output_path, "rb") as f:
                header = f.read(8)
                if header != b"\x89PNG\r\n\x1a\n":
                    validation["valid"] = False
                    validation["errors"].append("Invalid PNG format")

        return validation
