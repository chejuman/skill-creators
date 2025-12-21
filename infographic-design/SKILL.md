---
name: infographic-design
description: Generate publication-quality infographics and data visualizations using Tufte principles, multi-agent orchestration, and Pycairo rendering. Use when creating statistical graphics, diagrams, reports, or any visual data representation. Triggers on "infographic", "data visualization", "chart", "diagram", "visual design", or design-related requests.
---

# Infographic Design System

Expert-level infographic generation with ruthless reductionism and tyrannical aesthetic restraint.

## Core Philosophy

- **Zero Chartjunk**: Every pixel must convey data (Tufte)
- **Visual Entropy Threshold**: Maximum 0.18 Shannon density
- **Data-Ink Ratio**: Maximize information per visual element
- **Proportional Integrity**: No lie factor distortions

## Multi-Agent Architecture

```
Orchestrator
    ├─► Layout Agent ──► Grid, spacing, composition
    ├─► Typography Agent ──► Font hierarchy, readability
    ├─► Color Agent ──► Palette, contrast, accessibility
    ├─► Visualization Agent ──► Charts, diagrams, data mapping
    └─► Export Agent ──► WebP/SVG output, validation
```

## Quick Start

### Generate Infographic
```bash
python3 scripts/orchestrator.py \
  --data data.json \
  --type horizon \
  --output infographic.webp
```

### Available Visualization Types
| Type | Description | Use Case |
|------|-------------|----------|
| `horizon` | Horizon graphs | Time series, dense data |
| `euler` | Euler diagrams | Set relationships |
| `isometric` | Isometric small-multiples | Comparative data |
| `sparkline` | Word-sized graphics | Inline metrics |

## Foundation Layer

### Grid System
- **Primary**: 12×12 modular grid
- **Alternative**: 8×8 for compact layouts
- **Gutters**: 9-13px (responsive)
- **Margins**: 24px minimum

### Typography Hierarchy
```
Level 1 (Title):     32px, 700 weight, 1.2 line-height
Level 2 (Subtitle):  24px, 600 weight, 1.3 line-height
Level 3 (Body):      16px, 400 weight, 1.5 line-height
Level 4 (Caption):   12px, 400 weight, 1.4 line-height
Level 5 (Data):      11px, 500 weight, 1.0 line-height
```
Font: Neo-grotesque superfamily (Inter, Helvetica Neue, or system)

### Color System
```python
# Five-hue palette with desaturation limits
PALETTE = {
    "primary": "#1A1A2E",      # Data ink
    "secondary": "#4A4A68",    # Supporting
    "accent": "#E94560",       # Highlight (≤22% usage)
    "neutral": "#F0F0F5",      # Background
    "muted": "#9090A0"         # De-emphasized
}
# Non-accent elements: saturation ≤22%
```

### Icon Specifications
- **Artboard**: 64×64 px
- **Stroke**: 4px
- **Corner Radius**: 8%
- **Style**: Monoline, geometric

## Visualization Rules

### BANNED (Chartjunk Sources)
- Bar charts (use horizon graphs)
- Pie charts (use Euler diagrams)
- 3D effects
- Gradient fills
- Decorative elements

### ALLOWED
- Horizon graphs (time series)
- Euler diagrams (set relationships)
- Isometric small-multiples (comparisons)
- Sparklines (inline data)
- Dot plots (distributions)

### Axis Standards
- Labels: 45° rotation
- Hairlines: 0.5pt
- Scale: Logarithmic default
- Ticks: Minimal, data-driven

## Agent Workflows

### Layout Agent
```
Task(subagent_type='general-purpose', model='haiku', prompt='''
Analyze content requirements and generate grid layout:
1. Calculate content density
2. Select grid (8×8 or 12×12)
3. Allocate regions for each element
4. Ensure visual entropy < 0.18
Output: JSON layout specification
''')
```

### Typography Agent
```
Task(subagent_type='general-purpose', model='haiku', prompt='''
Design typography hierarchy:
1. Analyze text content lengths
2. Assign hierarchy levels
3. Calculate optimal sizes
4. Verify readability metrics
Output: Typography specification
''')
```

### Color Agent
```
Task(subagent_type='general-purpose', model='haiku', prompt='''
Generate color palette:
1. Extract data characteristics
2. Create 5-hue palette
3. Ensure WCAG AA contrast
4. Apply desaturation rules
Output: Color specification with hex values
''')
```

### Visualization Agent
```
Task(subagent_type='general-purpose', model='sonnet', prompt='''
Generate data visualization:
1. Analyze data structure
2. Select appropriate chart type (horizon/euler/isometric)
3. Calculate data-ink ratio
4. Generate visualization code
Output: Pycairo rendering instructions
''')
```

## Export Protocol

### Primary: WebP
- Quality: 100%
- Color Profile: Display P3
- Metadata: Preserved

### Fallback: SVG
- CSS Variables for theming
- Accessible `<title>` and `<desc>`
- Optimized paths

### Responsive
- Container queries
- Fluid typography: `clamp(12px, 2vw, 16px)`
- Breakpoints: 320, 768, 1024, 1440px

## Usage Examples

### Example 1: Time Series Visualization
```bash
python3 scripts/orchestrator.py \
  --data sales_2024.json \
  --type horizon \
  --title "Q4 Sales Performance" \
  --output sales_horizon.webp
```

### Example 2: Set Relationship Diagram
```bash
python3 scripts/orchestrator.py \
  --data categories.json \
  --type euler \
  --title "Product Categories" \
  --output categories_euler.svg
```

### Example 3: Comparative Analysis
```bash
python3 scripts/orchestrator.py \
  --data metrics.json \
  --type isometric \
  --title "Regional Comparison" \
  --output comparison.webp
```

## Validation Checklist

Before export, verify:
- [ ] Visual entropy ≤ 0.18
- [ ] Data-ink ratio ≥ 0.8
- [ ] No chartjunk elements
- [ ] WCAG AA color contrast
- [ ] Typography hierarchy clear
- [ ] Grid alignment verified
- [ ] 72-hour wall test ready

## Resources

- [Agent Prompts](references/agent_prompts.md) - Detailed agent instructions
- [Design Tokens](references/design_tokens.md) - Complete token reference
- [Validation Rules](references/validation_rules.md) - Quality criteria

## Dependencies

```
pycairo>=1.25.0
Pillow>=10.0.0
numpy>=1.24.0
```

## Trigger Phrases

- "create infographic" / "인포그래픽 만들어"
- "data visualization" / "데이터 시각화"
- "generate chart" / "차트 생성"
- "design diagram" / "다이어그램 디자인"
- "Tufte style" / "투프테 스타일"
