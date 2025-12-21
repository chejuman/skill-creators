# Validation Rules Reference

Quality criteria and validation rules for Tufte-compliant infographics.

## Core Metrics

### Visual Entropy

**Threshold**: ≤ 0.18 Shannon density

**Formula**: H = -Σ p(x) × log₂(p(x))

**Interpretation**:
- 0.00-0.10: Minimal (very sparse)
- 0.10-0.15: Optimal (balanced)
- 0.15-0.18: Acceptable (dense but readable)
- 0.18+: **REJECT** (too cluttered)

**Calculation**:
```python
def calculate_entropy(occupied_cells, total_cells):
    if total_cells == 0:
        return 0.0
    p_occupied = occupied_cells / total_cells
    p_empty = 1 - p_occupied
    entropy = 0.0
    if p_occupied > 0:
        entropy -= p_occupied * log2(p_occupied)
    if p_empty > 0:
        entropy -= p_empty * log2(p_empty)
    return entropy
```

### Data-Ink Ratio

**Threshold**: ≥ 0.8 (80% of ink shows data)

**Formula**: Data ink / Total ink

**What counts as data ink**:
- Data points
- Data lines
- Data labels (when necessary)

**What counts as non-data ink**:
- Gridlines
- Borders
- Decorative elements
- Legends (minimize)

**Interpretation**:
- 0.90+: Excellent (Tufte ideal)
- 0.80-0.90: Good (acceptable)
- 0.70-0.80: Fair (needs review)
- <0.70: **REJECT** (too much chartjunk)

## Chart Type Validation

### Banned Charts (REJECT immediately)

| Chart Type | Reason | Alternative |
|------------|--------|-------------|
| Bar chart | Poor data density | Horizon graph |
| Pie chart | Difficult angle comparison | Euler diagram |
| 3D charts | Distorts perception | 2D equivalent |
| Donut chart | Same as pie | Euler/dot plot |
| Stacked bar | Complex comparison | Small multiples |
| Area chart | Obscures data | Line + horizon |

### Allowed Charts

| Chart Type | Use Case | Constraints |
|------------|----------|-------------|
| Horizon graph | Time series | 3 bands, log scale |
| Euler diagram | Set relations | ≤5 sets |
| Isometric | Comparisons | Equal-sized units |
| Sparkline | Inline metrics | Word-sized (24px) |
| Dot plot | Distributions | Aligned dots |

## Typography Validation

### Size Hierarchy

**Rule**: Each level must be ≥10% larger than the next

**Check**:
```python
def validate_hierarchy(sizes):
    for i in range(len(sizes) - 1):
        ratio = sizes[i] / sizes[i + 1]
        if ratio < 1.10:
            return False, f"Level {i+1} too similar to {i+2}"
    return True, "Valid"
```

### Readability

| Element | Minimum Size | Maximum Size |
|---------|--------------|--------------|
| Title | 24px | 48px |
| Subtitle | 18px | 32px |
| Body | 14px | 20px |
| Caption | 11px | 14px |
| Data label | 10px | 14px |

### Line Height

| Element | Minimum | Maximum |
|---------|---------|---------|
| Titles | 1.1 | 1.3 |
| Body text | 1.4 | 1.6 |
| Data labels | 1.0 | 1.2 |

## Color Validation

### WCAG Contrast

| Text Size | AA Minimum | AAA Minimum |
|-----------|------------|-------------|
| Normal (<18px) | 4.5:1 | 7.0:1 |
| Large (≥18px) | 3.0:1 | 4.5:1 |
| Bold (≥14px) | 3.0:1 | 4.5:1 |

**Formula**:
```python
def contrast_ratio(l1, l2):
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
```

### Saturation Limits

| Element Type | Max Saturation |
|--------------|----------------|
| Primary text | 22% |
| Secondary text | 22% |
| Accent elements | 100% (but ≤22% usage) |
| Background | 10% |
| Muted elements | 22% |

## Grid Validation

### Utilization

**Optimal range**: 60-85%

| Utilization | Status |
|-------------|--------|
| 85-100% | Too dense |
| 60-85% | Optimal |
| 40-60% | Sparse but acceptable |
| <40% | Too sparse |

### Alignment

All elements must align to grid:
- Text baseline to row
- Element edges to columns
- Margins consistent

## Export Validation

### File Format

| Format | Header Check |
|--------|--------------|
| WebP | `RIFF....WEBP` |
| PNG | `\x89PNG\r\n\x1a\n` |
| SVG | Contains `<svg` |

### Size Limits

| Format | Warning | Error |
|--------|---------|-------|
| WebP | >5MB | >10MB |
| PNG | >10MB | >20MB |
| SVG | >2MB | >5MB |

### Color Profile

**Required**: Display P3 for WebP
**Fallback**: sRGB

## Pre-Export Checklist

```markdown
## Visual Quality
- [ ] Entropy ≤ 0.18
- [ ] Data-ink ratio ≥ 0.8
- [ ] No banned chart types
- [ ] No 3D effects
- [ ] No gradient fills
- [ ] No decorative elements

## Typography
- [ ] Single font family
- [ ] Size hierarchy validated
- [ ] Body text ≥ 14px
- [ ] Line heights appropriate

## Color
- [ ] WCAG AA contrast (4.5:1)
- [ ] Saturation ≤ 22% (non-accent)
- [ ] Five-hue maximum
- [ ] Works in grayscale

## Grid
- [ ] Consistent margins
- [ ] Aligned to grid
- [ ] Utilization 60-85%

## Export
- [ ] Format header valid
- [ ] Size within limits
- [ ] Color profile embedded
- [ ] SVG has CSS variables
```

## 72-Hour Wall Test

Physical validation protocol:

1. Print at 100% scale
2. Post on studio wall
3. View from 3 feet distance
4. Evaluate over 72 hours

**Criteria**:
- Is the main message clear immediately?
- Can you read all text comfortably?
- Are there any distracting elements?
- Does the hierarchy guide your eye?
- Is there unnecessary ink?

If any issues found after 72 hours, revise and repeat.
