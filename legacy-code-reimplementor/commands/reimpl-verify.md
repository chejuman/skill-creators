# /reimpl-verify

Verify current feature implementation against the original codebase.

## Usage

```
/reimpl-verify [options]
```

## Options

- `--feature N` or `-f N`: Verify specific feature ID
- `--unit M` or `-u M`: Verify specific unit within feature
- `--context PATH` or `-c PATH`: Path to context file (default: `.reimpl-context.json`)
- `--all`: Verify all completed features

## Workflow

### 1. Run Verification

```bash
python3 ~/.claude/skills/legacy-code-reimplementor/scripts/verify_feature.py \
  --feature {N} [--unit {M}] --context .reimpl-context.json
```

### 2. Compare Implementation

The verification compares:

- Function signatures and count
- Class definitions
- Method implementations
- Edge case handling

### 3. Generate Report

Output verification results with coverage metrics.

## Output Format

```
# Feature Verification Report

**Feature 4:** Auth Module
**Unit 2:** JWT Token Handler
**Status:** ✅ PASSED

## Coverage Summary

| Metric | Coverage |
|--------|----------|
| Functions | 95% |
| Classes | 100% |
| **Average** | **97.5%** |

## Function Comparison

| Metric | Count |
|--------|-------|
| Original functions | 12 |
| Implemented functions | 12 |
| Matched | 11 |

### Missing Functions

- `legacy_compat_check` (may be intentionally removed)

### New Functions (improvements)

- `validate_token_async`
- `refresh_token_handler`

## Recommendation

✅ Feature implementation is complete. Minor differences are intentional improvements.
Proceed to next unit/feature.
```

## Verification Levels

### Unit Level

Verify a single unit within a feature:

```
/reimpl-verify --feature 4 --unit 2
```

### Feature Level

Verify entire feature (all units):

```
/reimpl-verify --feature 4
```

### Full Verification

Verify all completed features:

```
/reimpl-verify --all
```

## Coverage Thresholds

| Coverage | Status     | Action             |
| -------- | ---------- | ------------------ |
| ≥90%     | ✅ Passed  | Proceed to next    |
| 70-89%   | ⚠️ Partial | Review gaps        |
| <70%     | ❌ Failed  | Fix implementation |

## Integration with Context

After verification:

1. Results are logged to context history
2. Feature status is updated if passed
3. Next prompt is generated for continuation

## Example

```
User: /reimpl-verify --feature 4
```

Or verify current work:

```
User: /reimpl-verify
```
