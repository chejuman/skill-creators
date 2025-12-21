# Infographic Generation Report

## Summary

| Metric | Value | Status |
|--------|-------|--------|
| Visual Entropy | {{entropy}} | {{entropy_status}} |
| Data-Ink Ratio | {{data_ink_ratio}} | {{data_ink_status}} |
| WCAG Compliance | {{wcag_status}} | {{wcag_pass}} |
| Readability Score | {{readability}} | {{readability_status}} |

## Agent Results

### Layout Agent
- Grid: {{grid_type}}
- Utilization: {{utilization}}%
- Entropy: {{entropy}}

### Typography Agent
- Font: {{font_family}}
- Levels: {{type_levels}}
- Readability: {{readability}}

### Color Agent
- Palette: {{palette_name}}
- Contrast: {{min_contrast}}:1
- WCAG AA: {{wcag_aa}}

### Visualization Agent
- Type: {{viz_type}}
- Data Points: {{data_points}}
- Data-Ink Ratio: {{data_ink_ratio}}

### Export Agent
- Format: {{output_format}}
- Size: {{file_size_kb}} KB
- Color Profile: {{color_profile}}

## Output

**File**: {{output_path}}

## Validation Checklist

- [{{entropy_check}}] Visual entropy ≤ 0.18
- [{{data_ink_check}}] Data-ink ratio ≥ 0.8
- [{{wcag_check}}] WCAG AA compliant
- [{{type_check}}] Typography hierarchy valid
- [{{grid_check}}] Grid alignment verified

## Recommendations

{{recommendations}}
