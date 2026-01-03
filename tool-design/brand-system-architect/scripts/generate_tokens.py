#!/usr/bin/env python3
"""
Generate W3C Design Tokens and CSS Variables from brand specification.

Usage:
    python generate_tokens.py <brand-spec.json> [output-dir]

Example:
    python generate_tokens.py .brand-system/brand-spec.json .brand-system/tokens/
"""

import json
import sys
from pathlib import Path
from typing import Any


def load_brand_spec(path: str) -> dict:
    """Load brand specification JSON."""
    with open(path, 'r') as f:
        return json.load(f)


def generate_w3c_tokens(spec: dict) -> dict:
    """Generate W3C Design Tokens format from brand spec."""
    tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "$description": f"{spec.get('brand', {}).get('name', 'Brand')} Design Tokens",
        "$version": "1.0.0"
    }

    # Color tokens
    if 'color' in spec:
        tokens['color'] = spec['color']

    # Typography tokens
    if 'font' in spec:
        tokens['font'] = spec['font']

    # Motion tokens
    if 'motion' in spec:
        tokens['motion'] = spec['motion']

    # Spacing tokens
    if 'spacing' in spec:
        tokens['spacing'] = spec['spacing']

    # Radius tokens
    if 'radius' in spec:
        tokens['radius'] = spec['radius']

    # Shadow tokens
    if 'shadow' in spec:
        tokens['shadow'] = spec['shadow']

    return tokens


def extract_css_value(token: Any) -> str:
    """Extract CSS value from token."""
    if isinstance(token, dict):
        return token.get('$value', str(token))
    return str(token)


def generate_css_variables(spec: dict) -> str:
    """Generate CSS custom properties from brand spec."""
    lines = [":root {"]

    def process_tokens(obj: dict, prefix: str = ""):
        for key, value in obj.items():
            if key.startswith('$'):
                continue

            var_name = f"{prefix}-{key}" if prefix else key

            if isinstance(value, dict):
                if '$value' in value:
                    css_val = extract_css_value(value)
                    lines.append(f"  --{var_name}: {css_val};")
                else:
                    process_tokens(value, var_name)

    # Process color tokens
    if 'color' in spec:
        process_tokens(spec['color'], 'color')

    # Process font tokens
    if 'font' in spec:
        process_tokens(spec['font'], 'font')

    # Process motion tokens
    if 'motion' in spec:
        process_tokens(spec['motion'], 'motion')

    # Process spacing tokens
    if 'spacing' in spec:
        process_tokens(spec['spacing'], 'spacing')

    # Process radius tokens
    if 'radius' in spec:
        process_tokens(spec['radius'], 'radius')

    # Process shadow tokens
    if 'shadow' in spec:
        process_tokens(spec['shadow'], 'shadow')

    lines.append("}")
    return "\n".join(lines)


def generate_tailwind_config(spec: dict) -> str:
    """Generate Tailwind CSS theme configuration."""
    config = {
        "theme": {
            "extend": {}
        }
    }

    # Colors
    if 'color' in spec:
        colors = {}
        def extract_colors(obj: dict, prefix: str = ""):
            for key, value in obj.items():
                if key.startswith('$'):
                    continue
                name = f"{prefix}-{key}" if prefix else key
                if isinstance(value, dict):
                    if '$value' in value:
                        colors[name.replace('-', '.')] = value['$value']
                    else:
                        extract_colors(value, name)
        extract_colors(spec['color'])
        config['theme']['extend']['colors'] = colors

    # Font families
    if 'font' in spec and 'family' in spec['font']:
        families = {}
        for key, value in spec['font']['family'].items():
            if isinstance(value, dict) and '$value' in value:
                families[key] = value['$value'].split(',')
        config['theme']['extend']['fontFamily'] = families

    # Border radius
    if 'radius' in spec:
        radius = {}
        for key, value in spec['radius'].items():
            if isinstance(value, dict) and '$value' in value:
                radius[key] = value['$value']
        config['theme']['extend']['borderRadius'] = radius

    return f"/** @type {{import('tailwindcss').Config}} */\nmodule.exports = {json.dumps(config, indent=2)}"


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_tokens.py <brand-spec.json> [output-dir]")
        sys.exit(1)

    spec_path = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./tokens")

    # Load specification
    spec = load_brand_spec(spec_path)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate W3C tokens
    w3c_tokens = generate_w3c_tokens(spec)
    with open(output_dir / "w3c-tokens.json", 'w') as f:
        json.dump(w3c_tokens, f, indent=2)
    print(f"✓ Generated {output_dir}/w3c-tokens.json")

    # Generate CSS variables
    css_vars = generate_css_variables(spec)
    with open(output_dir / "variables.css", 'w') as f:
        f.write(css_vars)
    print(f"✓ Generated {output_dir}/variables.css")

    # Generate Tailwind config
    tailwind_config = generate_tailwind_config(spec)
    with open(output_dir / "tailwind.config.js", 'w') as f:
        f.write(tailwind_config)
    print(f"✓ Generated {output_dir}/tailwind.config.js")

    print(f"\n✅ All tokens generated in {output_dir}/")


if __name__ == "__main__":
    main()
