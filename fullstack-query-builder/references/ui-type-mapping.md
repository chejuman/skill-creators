# UI Type Decision Tree

This document explains how the Query Analyzer determines the optimal UI type based on query results.

## Decision Process

### 1. Single Row → Detail View
**Condition:** `rowCount === 1`
**Confidence:** 0.95
**Rationale:** Single record is best shown as a detailed view with labels
**Components:** Card, Separator, Badge, Label

**Example:**
```sql
SELECT * FROM users WHERE id = 1
```

### 2. Aggregated Data → Dashboard
**Condition:** Query contains `GROUP BY`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
**Confidence:** 0.88
**Rationale:** Aggregated metrics suit dashboard visualization
**Components:** Card, Progress, Badge

**Example:**
```sql
SELECT department, COUNT(*) as total, AVG(salary) as avg_salary
FROM employees GROUP BY department
```

### 3. Small Dataset + Rich Columns → Card Grid
**Condition:** `rowCount <= 10 AND columnCount >= 4`
**Confidence:** 0.85
**Rationale:** Few items with detailed info suit card-based layout
**Components:** Card, CardHeader, CardContent, Badge, Button

**Example:**
```sql
SELECT id, name, email, role, department, created_at
FROM users LIMIT 10
```

### 4. Large Dataset → Table
**Condition:** `rowCount > 10 AND columnCount <= 10`
**Confidence:** 0.90
**Rationale:** Many rows of structured data best displayed in table
**Components:** Table, TableHeader, TableBody, Pagination, DropdownMenu

**Example:**
```sql
SELECT id, name, email, created_at FROM users
```

### 5. Default → Table
**Condition:** None of the above match
**Confidence:** 0.70
**Rationale:** Fallback to table for general data display
**Components:** Table, Pagination

## Column Type Detection

Query Analyzer maps PostgreSQL types to TypeScript/Python types:

| PostgreSQL Type | TypeScript | Python | UI Treatment |
|----------------|------------|--------|--------------|
| integer, bigint | number | int | Numeric display |
| varchar, text | string | str | Text display |
| boolean | boolean | bool | Checkbox/badge |
| timestamp, date | Date | datetime | Formatted date |
| uuid | string | str | Monospace text |

## UI Recommendations by Pattern

### List/Index Pages
- Many rows (>50): Table with pagination
- Few rows (<10): Card grid
- Include search/filter for >20 rows

### Detail Pages
- Single record: Detail view with sections
- Related data: Tabs or accordion sections

### Dashboards
- Aggregated metrics: Dashboard cards
- Time series: Add chart components
- Multiple metrics: Grid layout

## shadcn/ui Component Selection

Based on UI type, these components are automatically selected:

**Table View:**
- Table, TableHeader, TableBody, TableRow, TableHead, TableCell
- Button (for actions)
- DropdownMenu (for bulk actions)
- Input (for filters)

**Card Grid:**
- Card, CardHeader, CardTitle, CardContent
- Badge (for status)
- Button (for actions)

**Detail View:**
- Card, Separator
- Label (for field labels)
- Badge (for status)

**Dashboard:**
- Card (for metrics)
- Progress (for percentages)
- Badge (for highlights)

## Customization

After generation, you can modify the UI type by:
1. Editing the generated component files
2. Mixing components from different templates
3. Adding custom shadcn/ui components

## Best Practices

- Use Table for data > 20 rows
- Use Cards for visual emphasis on individual items
- Use Detail View for single-record focus
- Use Dashboard for metrics and KPIs
- Always enable pagination for >50 rows
- Add search/filter for >20 rows
