# Feature Scoring Guide

## RICE Framework

### Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### Reach

How many users/customers will this impact in a given time period?

| Range    | Description   | Example            |
| -------- | ------------- | ------------------ |
| 1-10     | Internal only | Admin tools        |
| 10-100   | Power users   | Advanced features  |
| 100-500  | Active users  | Core improvements  |
| 500-1000 | All users     | Universal features |

### Impact

Expected effect on each user who encounters this feature.

| Score | Level   | Description                       |
| ----- | ------- | --------------------------------- |
| 3     | Massive | Life-changing, can't live without |
| 2     | High    | Significant improvement           |
| 1     | Medium  | Noticeable improvement            |
| 0.5   | Low     | Minor improvement                 |
| 0.25  | Minimal | Barely noticeable                 |

### Confidence

How certain are you about your estimates?

| Percentage | Level  | Basis                       |
| ---------- | ------ | --------------------------- |
| 100%       | High   | Hard data, prior experience |
| 80%        | Medium | Some data, educated guess   |
| 50%        | Low    | Gut feeling, hypothesis     |

### Effort

Person-months of work required.

| Months | Size | Typical Scope      |
| ------ | ---- | ------------------ |
| 0.5    | XS   | Few hours to 1 day |
| 1      | S    | 1-2 weeks          |
| 2      | M    | 2-4 weeks          |
| 4      | L    | 1-2 months         |
| 8      | XL   | 2-4 months         |
| 12+    | XXL  | Quarter+           |

## MoSCoW Prioritization

### Must Have

- Critical for this version
- Product fails without it
- Contractual/legal requirement
- No workaround exists

### Should Have

- Important but not vital
- Painful without it
- Workaround exists but is difficult
- High business value

### Could Have

- Nice to have
- Enhances experience
- Easy workaround exists
- Lower business value

### Won't Have (This Time)

- Out of scope for this version
- Deprioritized consciously
- May revisit in future versions
- Documented for later

## Combined Scoring Process

1. **Initial Scoring**: Apply RICE to all features
2. **MoSCoW Classification**: Assign priority category
3. **Sort Order**: MoSCoW first, then RICE within category
4. **Effort Budget**: Select features fitting available capacity
5. **Dependency Check**: Ensure prerequisites are included

## Version Capacity Planning

### MVP (v1.0)

- 3-5 Must-have features only
- Focus on core value proposition
- Minimal viable scope

### Growth (v2.0-3.0)

- 2-3 Must + 2-3 Should
- Address user feedback
- Expand core functionality

### Maturity (v4.0-6.0)

- 1-2 Must + 2-3 Should + 1-2 Could
- Polish and refinement
- Competitive features

### Enterprise (v7.0+)

- Mixed priorities based on market
- Enterprise requirements
- Scale and performance
