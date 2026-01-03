# Role-Based Passes

Use these as structured passes in a single Codex session.

## Debt Scanner Pass

Return:
- hotspots: [file:line]
- debt_items: [{category, location, summary}]
- signals: [short bullets]

## Risk & Priority Pass

Return:
- ranked_items: [{category, location, impact, effort, confidence, reason}]
- quick_wins: [items]
- requires_approval: [items]

## Fix Plan Pass

Return:
- item: {category, location}
- target_behavior: "..."
- files: [paths]
- steps: [ordered steps]
- tests: [commands or checks]

## Review Pass

Return:
- issues: [{file, severity, description, suggestion}]
- test_status: "ran|skipped|failed"
- regression_risks: [bullets]
