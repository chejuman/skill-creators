# Agent Prompts Reference - v4

Comprehensive prompts for 10 analysis workers plus coordination and remediation agents.

## Phase 1: Context Gathering

### Git History Agent [NEW]

```
Analyze git history for technical debt context.

Repository: {repo_path}
Time Range: Last 90 days

**Analysis Tasks:**

1. **File Churn Analysis**
   - Count changes per file in time range
   - Identify hotspots (> 10 changes)
   - Map churn to complexity changes
   - Flag files with increasing complexity

2. **Author Distribution**
   - Map files to authors (who knows what)
   - Calculate author concentration per module
   - Identify single-author files (bus factor = 1)
   - Find modules with departed contributors

3. **Commit Pattern Analysis**
   - Rushed commits (< 5 min between commits)
   - EOD commits (after 6pm local time)
   - Weekend/holiday commits
   - Large change sets (> 500 lines)

4. **Quality Signals**
   - Revert frequency
   - Hotfix patterns ("fix", "hotfix", "urgent")
   - TODO/FIXME additions vs removals
   - Test additions accompanying changes

5. **Trend Detection**
   - Complexity trajectory per module
   - Growing vs shrinking files
   - Coupling trend (files changed together)

**Output:**
{
  churn_files: [{file, changes, complexity_delta}],
  author_map: {file: [authors]},
  bus_factor_risks: [{file, sole_author, last_touched}],
  hotfixes: [{commit, date, files}],
  complexity_trend: {module: "growing"|"stable"|"improving"},
  rushed_commits: N,
  weekend_commits: N
}
```

## Phase 2: Analysis Workers (10 Parallel)

### Workers 1-8: Same as v3

See v3 agent_prompts.md for:

- Code Quality Agent
- Dependency Agent
- Architecture Agent
- Test Coverage Agent
- Performance Agent
- Security Agent
- Documentation Agent
- Type Safety Agent

### AI Code Quality Agent [NEW - Worker 9]

```
Analyze codebase for AI-generated code issues.

Target: {target}
File Patterns: {file_patterns}

**Detection Signals for AI-Generated Code:**
- Unusual comment density (excessive docstrings)
- Generic variable names (data, result, temp)
- Over-commented obvious code
- Inconsistent style within file
- Placeholder implementations
- Boilerplate-heavy structures

**Analysis Tasks:**

1. **Convention Violations**
   - Style inconsistent with project
   - Naming patterns differ from codebase
   - Import organization mismatch
   - Formatting deviations

2. **Implementation Issues**
   - Hallucinated imports (non-existent packages)
   - Deprecated API usage
   - Incomplete error handling
   - Missing edge cases
   - Overly complex solutions

3. **Quality Concerns**
   - Excessive abstraction
   - Unnecessary code
   - Copy-paste patterns
   - Missing tests for generated code
   - Unclear variable names

4. **License/Legal Risks**
   - Code matching known open source
   - Potential copyright issues
   - Missing attribution

5. **Maintenance Burden**
   - Poorly understood by team
   - Lacks domain knowledge
   - Over-engineered for requirements

**Output:**
[{
  id: "AI-001",
  type: "ai_code",
  subtype: "convention|implementation|quality|license",
  location: "file:line",
  description: "issue description",
  severity: 1-5,
  ai_confidence: 0.0-1.0,  # confidence it's AI-generated
  suggestion: "how to fix"
}]
```

### Knowledge Silo Agent [NEW - Worker 10]

```
Analyze knowledge distribution and bus factor risks.

Target: {target}
Author Map: {author_map}
Churn Data: {churn_data}

**Analysis Tasks:**

1. **Bus Factor Analysis**
   - Files with single author ever
   - Files with no changes in 6+ months
   - Critical files with limited knowledge
   - Calculate bus factor per module

2. **Ownership Gaps**
   - Orphaned code (original author left)
   - No clear maintainer
   - Disputed ownership (many authors, none active)
   - Stale CODEOWNERS entries

3. **Knowledge Islands**
   - Isolated expertise areas
   - No cross-training evidence
   - Single-expert subsystems
   - Documentation gaps for complex modules

4. **Handoff Risks**
   - Complex code by departed devs
   - Undocumented tribal knowledge
   - Custom frameworks/tools
   - Non-standard implementations

5. **Onboarding Friction**
   - High complexity + low documentation
   - Unusual patterns
   - Missing architecture docs
   - No tests explaining behavior

**Severity Scoring:**
- Critical: Bus factor=1 on core business logic
- High: Bus factor=1 on important modules
- Medium: Bus factor<=2 on any module
- Low: Documentation gaps

**Output:**
[{
  id: "SILO-001",
  type: "knowledge_silo",
  subtype: "bus_factor|ownership|island|handoff|onboarding",
  location: "file or module",
  description: "issue description",
  severity: 1-5,
  bus_factor: N,
  last_author: "name",
  last_touched: "date",
  suggestion: "mitigation action"
}]
```

## Phase 3: Business Impact

### Business Impact Agent [NEW]

```
Calculate business cost and DevEx impact of technical debt.

Inputs:
- All issues: {all_issues}
- Hourly rate: ${hourly_rate}
- Team size: {team_size}
- Codebase LOC: {loc}
- Annual dev budget (estimated): {budget}

**Calculations:**

1. **Per-Issue Cost**
   For each issue:
   - Remediation Cost = fix_hours × hourly_rate
   - Monthly Interest = (severity/5) × base_interest
   - Annual Interest = Monthly Interest × 12
   - Total Annual Cost = Remediation + Annual Interest

   Base Interest by type:
   - Security: $500/month (risk exposure)
   - Performance: $200/month (infrastructure)
   - Code Quality: $100/month (velocity)
   - Architecture: $300/month (scalability)
   - Test Coverage: $150/month (bugs)
   - AI Code: $100/month (maintenance)
   - Knowledge Silo: $250/month (risk)

2. **Technical Debt Ratio (TDR)**
   TDR = (Total Remediation Cost / Annual Dev Budget) × 100%

   Interpretation:
   - < 10%: Excellent, sustainable
   - 10-25%: Good, manageable
   - 25-42%: Average (Stripe benchmark: 42%)
   - 42-60%: Concerning, impacts delivery
   - > 60%: Critical, blocking innovation

3. **DevEx Impact**
   Hours_Lost_Weekly = Σ(issue_friction × touch_frequency)

   Friction factors:
   - Complexity: 0.5h per touch
   - Poor docs: 0.3h per touch
   - Flaky tests: 0.2h per touch
   - Security blocks: 1h per occurrence
   - Knowledge gaps: 0.5h per question

   Productivity Tax = (Hours Lost / 40h) × 100%

4. **ROI Calculation**
   For each item:
   Annual_Savings = Interest_Cost × Years_Remaining
   ROI = (Annual_Savings - Remediation) / Remediation × 100%

   Sort by: ROI × Confidence

5. **Trend Analysis** (when --compare provided)
   Compare with previous report:
   - New issues (not in previous)
   - Resolved issues (in previous, not now)
   - Changed severity
   - Cost trajectory

**Output:**
{
  total_cost: {
    remediation_usd: N,
    annual_interest_usd: N,
    total_annual_usd: N
  },
  tdr: {
    percent: N,
    rating: "excellent"|"good"|"average"|"concerning"|"critical",
    industry_benchmark: 42
  },
  devex: {
    hours_lost_weekly: N,
    productivity_tax_percent: N,
    top_friction_sources: [{type, hours}]
  },
  roi_ranking: [{id, roi_percent, payback_months}],
  trend: {
    new_issues: N,
    resolved_issues: N,
    cost_change_percent: N,
    trajectory: "growing"|"stable"|"shrinking"
  }
}
```

## Phase 5: Remediation

### Auto-Fix Agent [NEW]

```
Generate fix patches for quick wins.

Quick Wins: {quick_wins}
Codebase Context: {context}

**Fix Generation Rules:**

1. **Eligibility Criteria**
   - Confidence >= 0.8
   - Effort <= 2 hours
   - No breaking changes
   - Clear solution path

2. **Fix Types Supported**
   - Naming improvements
   - Type annotations
   - Unused imports/variables
   - Simple refactorings
   - Missing null checks
   - Documentation additions
   - Test additions

3. **Fix Generation Process**
   For each eligible item:
   a. Read current file content
   b. Identify exact change location
   c. Generate minimal fix
   d. Preserve surrounding code
   e. Follow project style
   f. Create unified diff

4. **Validation**
   - Syntax check (if possible)
   - Style consistency
   - No new issues introduced

5. **Test Generation**
   If item is about missing tests:
   - Generate test file/additions
   - Include setup/teardown
   - Cover happy path + edge cases

**Output:**
{
  patches: [
    {
      id: "item_id",
      file: "path/to/file",
      description: "what this fixes",
      diff: "unified diff content",
      test_file: "path/to/test" (optional),
      test_diff: "test additions" (optional),
      verification: "how to verify fix"
    }
  ],
  skipped: [
    {
      id: "item_id",
      reason: "why not auto-fixable"
    }
  ],
  stats: {
    total_eligible: N,
    fixes_generated: N,
    tests_generated: N
  }
}
```

### PR Generator Agent [NEW]

```
Generate PR descriptions for fix patches.

Patches: {patches}
Project: {project_name}

**Grouping Strategy:**
Group patches by:
- Type (naming, types, tests, docs)
- Module/directory
- Related functionality

**PR Generation:**

For each group:

1. **Title**
   Format: "[type] Brief description"
   Examples:
   - "[refactor] Improve type safety in auth module"
   - "[test] Add missing tests for payment service"
   - "[fix] Resolve code smells in user controller"

2. **Description**
   Structure:
   ## Summary
   Brief overview of changes

   ## Changes
   - File-by-file breakdown
   - Before/after for key changes

   ## Impact
   - Lines changed: N
   - Files affected: N
   - Risk level: Low/Medium

   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual verification steps

   ## Metrics Improvement
   - Technical Debt: -$X,XXX
   - Code Quality: +N points
   - Test Coverage: +N%

3. **Labels**
   Suggest appropriate labels:
   - tech-debt
   - auto-generated
   - low-risk
   - needs-review

**Output:**
{
  prs: [
    {
      title: "PR title",
      body: "PR description markdown",
      files: ["list", "of", "files"],
      labels: ["label1", "label2"],
      estimated_review_time: "15 min"
    }
  ]
}
```

## Analysis Agent (Updated)

```
Correlate findings with business context.

Worker Results:
- Code Quality: {code_quality}
- Dependencies: {dependencies}
- Architecture: {architecture}
- Test Coverage: {test_coverage}
- Performance: {performance}
- Security: {security}
- Documentation: {documentation}
- Type Safety: {type_safety}
- AI Code Quality: {ai_code}
- Knowledge Silos: {knowledge_silos}

**Enhanced Correlation:**

1. **Root Cause Identification**
   - Single issues causing multiple symptoms
   - Architectural decisions creating debt clusters
   - Knowledge gaps leading to poor code
   - AI code creating maintenance burden

2. **Cross-Domain Connections**
   - Security issues from poor architecture
   - Performance issues from AI-generated code
   - Test gaps in knowledge silo areas
   - Documentation missing where bus factor = 1

3. **Business Risk Aggregation**
   - Knowledge + Security = Critical risk
   - Bus Factor + Complexity = Handoff risk
   - AI Code + No Tests = Reliability risk

4. **Pattern Recognition**
   - Team-wide anti-patterns
   - Module-specific issues
   - Technology-specific debt

**Output:**
{
  root_causes: [...],
  cross_domain_risks: [{types, combined_severity, description}],
  patterns: [...],
  clusters: [...]
}
```
