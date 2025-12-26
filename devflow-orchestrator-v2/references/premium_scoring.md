# Premium Scoring Guide (RICE++)

## RICE++ Formula

```
RICE++ = (Reach × Impact × Confidence × Urgency) / (Effort × Risk)
```

## Parameters

### Reach (1-1000)

Users affected in the target period.

| Range    | Description    | Typical Projects   |
| -------- | -------------- | ------------------ |
| 1-10     | Internal/Admin | Tools, dashboards  |
| 10-100   | Power Users    | Advanced features  |
| 100-500  | Active Users   | Core functionality |
| 500-1000 | All Users      | Universal features |

### Impact (0.25-3.0)

Effect magnitude on each user.

| Score | Level   | User Reaction             |
| ----- | ------- | ------------------------- |
| 3.0   | Massive | "Life-changing"           |
| 2.0   | High    | "Significant improvement" |
| 1.0   | Medium  | "Nice to have"            |
| 0.5   | Low     | "Minor improvement"       |
| 0.25  | Minimal | "Barely noticed"          |

### Confidence (0-100%)

Certainty in estimates.

| Level    | Percentage | Basis                    |
| -------- | ---------- | ------------------------ |
| High     | 100%       | Hard data, A/B tests     |
| Medium   | 80%        | User research, some data |
| Low      | 50%        | Gut feeling, hypothesis  |
| Very Low | 25%        | Wild guess               |

### Urgency (0.5-2.0)

Time sensitivity factor.

| Score | Level    | Situation                 |
| ----- | -------- | ------------------------- |
| 2.0   | Critical | Market window, regulatory |
| 1.5   | High     | Competitive pressure      |
| 1.0   | Normal   | Standard roadmap          |
| 0.5   | Low      | Nice to have, can wait    |

### Effort (1-12)

Person-months required.

| Months | T-Shirt | Description |
| ------ | ------- | ----------- |
| 0.5    | XS      | Days        |
| 1      | S       | 1-2 weeks   |
| 2      | M       | 2-4 weeks   |
| 4      | L       | 1-2 months  |
| 8      | XL      | 2-4 months  |
| 12+    | XXL     | Quarter+    |

### Risk (0.5-2.0)

Implementation risk multiplier.

| Score | Level    | Factors                         |
| ----- | -------- | ------------------------------- |
| 0.5   | Low      | Well-understood, team expertise |
| 1.0   | Normal   | Standard complexity             |
| 1.5   | High     | New technology, dependencies    |
| 2.0   | Critical | Unknown territory, blockers     |

## Scoring Example

**Feature: Real-time Collaboration**

| Parameter  | Value | Justification                  |
| ---------- | ----- | ------------------------------ |
| Reach      | 500   | Core feature for all users     |
| Impact     | 2.0   | Significant productivity boost |
| Confidence | 80%   | User research supports         |
| Urgency    | 1.5   | Competitor launching soon      |
| Effort     | 4     | 1-2 months development         |
| Risk       | 1.5   | WebSocket complexity           |

```
RICE++ = (500 × 2.0 × 0.8 × 1.5) / (4 × 1.5)
       = 1200 / 6
       = 200
```

## Score Interpretation

| Range   | Priority    | Action                     |
| ------- | ----------- | -------------------------- |
| 200+    | Must-Have   | Include in current version |
| 100-200 | Should-Have | High priority              |
| 50-100  | Could-Have  | Consider if capacity       |
| <50     | Won't-Have  | Defer to later             |

## Confidence Intervals

For high-stakes decisions, calculate range:

```
Optimistic = RICE++ × 1.2
Pessimistic = RICE++ × 0.8
```

Report as: "RICE++: 200 (160-240)"
