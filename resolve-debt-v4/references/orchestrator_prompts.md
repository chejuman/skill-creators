# Orchestrator Agent Prompts

Structured prompts for all phases of the resolve-debt-v4 workflow.

## Phase 2: Context Gathering Agents

### Planning Agent Prompt

```
Analyze project structure for comprehensive technical debt assessment.

Target: {target}

**Analysis Tasks:**

1. **Project Structure**
   - Identify source directories and file patterns
   - Detect languages and frameworks used
   - Find entry points and main modules

2. **Dependencies**
   - Locate package manifests (package.json, requirements.txt, go.mod)
   - Identify dependency manager (npm, yarn, pip, poetry)
   - Find lock files for version pinning

3. **Testing Setup**
   - Locate test directories and patterns
   - Find test configuration files
   - Identify coverage configuration

4. **Code Quality Tools**
   - Find linting configs (.eslintrc, .prettierrc, ruff.toml)
   - Locate type checking configs (tsconfig.json, mypy.ini)
   - Identify pre-commit hooks

5. **Critical Modules**
   - Identify authentication/authorization code
   - Find payment/financial logic
   - Locate core business logic

**Output Format (JSON):**
{
  "structure": {
    "source_dirs": ["src/", "lib/"],
    "file_patterns": ["**/*.ts", "**/*.py"],
    "languages": ["TypeScript", "Python"],
    "frameworks": ["React", "FastAPI"]
  },
  "dependencies": {
    "manifest": "package.json",
    "manager": "npm",
    "lock_file": "package-lock.json"
  },
  "testing": {
    "test_dirs": ["tests/", "__tests__/"],
    "test_patterns": ["*.test.ts", "test_*.py"],
    "coverage_config": "jest.config.js"
  },
  "quality_tools": {
    "linter": ".eslintrc.js",
    "formatter": ".prettierrc",
    "type_checker": "tsconfig.json"
  },
  "critical_modules": [
    {"name": "auth", "path": "src/auth/", "risk": "high"},
    {"name": "payments", "path": "src/payments/", "risk": "critical"}
  ]
}
```

### Git History Agent Prompt

```
Analyze git history for technical debt context and team dynamics.

Repository: {repo_path}
Time Range: Last 90 days

**Analysis Tasks:**

1. **File Churn Analysis**
   - Count changes per file in time range
   - Identify hotspots (files with > 10 changes)
   - Correlate churn with complexity
   - Flag files with increasing complexity trend

2. **Author Distribution**
   - Map files to contributors
   - Calculate author concentration per module
   - Identify single-author files (bus factor = 1)
   - Find modules with departed contributors

3. **Commit Pattern Analysis**
   - Rushed commits (< 5 min between commits)
   - After-hours commits (outside 9am-6pm)
   - Weekend/holiday commits
   - Large change sets (> 500 lines added)

4. **Quality Signals from History**
   - Revert frequency per module
   - Hotfix patterns ("fix", "hotfix", "urgent" in message)
   - TODO/FIXME additions vs removals
   - Test additions accompanying changes

5. **Complexity Trend Detection**
   - Module complexity trajectory (growing/stable/improving)
   - Growing vs shrinking files over time
   - Files frequently changed together (coupling)

**Output Format (JSON):**
{
  "churn_analysis": {
    "hotspots": [
      {"file": "src/api/handler.ts", "changes": 45, "complexity_delta": "+15"}
    ],
    "total_files_changed": 234,
    "avg_changes_per_file": 3.2
  },
  "author_distribution": {
    "single_author_files": [
      {"file": "src/legacy/parser.ts", "author": "john@example.com", "last_touched": "2024-03-15"}
    ],
    "bus_factor_risks": [
      {"module": "src/payments/", "bus_factor": 1, "sole_author": "jane@example.com"}
    ]
  },
  "commit_patterns": {
    "rushed_commits": 23,
    "after_hours_commits": 45,
    "weekend_commits": 12,
    "large_changesets": 8
  },
  "quality_signals": {
    "reverts": 5,
    "hotfixes": 12,
    "todo_added": 34,
    "todo_removed": 18
  },
  "complexity_trend": {
    "growing": ["src/api/", "src/handlers/"],
    "stable": ["src/utils/", "src/config/"],
    "improving": ["src/auth/"]
  }
}
```

## Phase 3: Analysis Worker Prompts

### Code Quality Agent

```
Analyze codebase for code quality issues and technical debt.

Target: {target}
File Patterns: {file_patterns}
High-Churn Files: {churn_files}

**Analysis Categories:**

1. **Complexity** (severity weighting: high)
   - Cyclomatic complexity > 10
   - Cognitive complexity > 15
   - Nesting depth > 4 levels
   - Methods > 50 lines, Files > 500 lines

2. **Duplication** (severity weighting: medium)
   - Code blocks > 6 lines duplicated
   - Structural clones (similar logic patterns)
   - Copy-paste with minor variations

3. **Code Smells** (severity weighting: medium)
   - Long parameter lists (> 4 params)
   - God classes (> 300 lines, multiple responsibilities)
   - Feature envy, dead code, magic numbers

4. **Naming/Conventions** (severity weighting: low)
   - Inconsistent naming patterns
   - Cryptic abbreviations
   - Single-letter variables (non-loop)

**Output Format (JSON Array):**
[{
  "id": "CQ-001",
  "type": "code_quality",
  "subtype": "complexity|duplication|smell|naming",
  "location": {"file": "src/handler.ts", "line": 45, "function": "processData"},
  "description": "Cyclomatic complexity of 25 exceeds threshold of 10",
  "severity": 4,
  "effort_hours": 2,
  "suggestion": "Extract into smaller functions: validateInput(), transformData(), saveResult()"
}]
```

### Dependency Agent

```
Analyze project dependencies for security and health issues.

Manifest: {dependency_file}
Lock File: {lock_file}
Package Manager: {pkg_manager}

**Analysis Categories:**

1. **Security Vulnerabilities** (severity weighting: critical)
   - CVEs in direct dependencies
   - CVEs in transitive dependencies
   - CVSS severity scoring

2. **Outdated Packages** (severity weighting: medium)
   - Major version updates available
   - Packages > 1 year without updates
   - Deprecated packages

3. **License Compliance** (severity weighting: high)
   - Incompatible licenses (GPL in MIT project)
   - Missing license declarations
   - Commercial license requirements

4. **Bundle/Size Impact** (severity weighting: low)
   - Large dependencies (> 100KB)
   - Duplicate packages in tree
   - Lighter alternatives available

**Output Format (JSON Array):**
[{
  "id": "DEP-001",
  "type": "dependency",
  "subtype": "vulnerability|outdated|license|bundle",
  "package": "lodash",
  "current_version": "4.17.15",
  "recommended_version": "4.17.21",
  "severity": 5,
  "cve": "CVE-2021-23337",
  "cvss": 7.2,
  "effort_hours": 0.5,
  "suggestion": "Run: npm update lodash"
}]
```

### Architecture Agent

```
Analyze architectural patterns and SOLID principle violations.

Target: {target}
File Patterns: {file_patterns}
Module Map: {module_map}

**Analysis Categories:**

1. **Coupling** (severity weighting: high)
   - High afferent/efferent coupling metrics
   - Circular dependencies
   - God modules (importing/exporting everything)

2. **Layering Violations** (severity weighting: high)
   - UI directly accessing database
   - Business logic in presentation layer
   - Cross-layer imports

3. **SOLID Violations** (severity weighting: medium)
   - SRP: Classes with multiple responsibilities
   - OCP: Modifications instead of extensions
   - DIP: Concrete dependencies instead of abstractions

4. **Pattern Inconsistency** (severity weighting: low)
   - Mixed state management approaches
   - Varied error handling patterns
   - Inconsistent API response structures

**Output Format (JSON Array):**
[{
  "id": "ARCH-001",
  "type": "architecture",
  "subtype": "coupling|layering|solid|pattern",
  "location": {"module": "src/handlers/", "file": "userHandler.ts"},
  "description": "Circular dependency between handlers/ and services/",
  "severity": 4,
  "impact": "Makes testing difficult, increases build times",
  "effort_hours": 4,
  "suggestion": "Extract shared types to common/ module"
}]
```

### Test Coverage Agent

```
Analyze test coverage gaps and test quality issues.

Target: {target}
Test Patterns: {test_patterns}
Coverage Config: {coverage_config}
Critical Modules: {critical_modules}
High-Churn Files: {churn_files}

**Analysis Categories:**

1. **Coverage Gaps** (severity weighting: high for critical modules)
   - Source files without corresponding tests
   - Public functions without coverage
   - Critical paths untested

2. **Test Quality** (severity weighting: medium)
   - Tests without meaningful assertions
   - Testing implementation vs behavior
   - Missing edge case coverage

3. **High-Risk Untested** (severity weighting: critical)
   - Auth/authz untested
   - Payment logic untested
   - Error handling paths untested

4. **Test Health** (severity weighting: low)
   - Flaky tests (non-deterministic)
   - Slow tests (> 5s each)
   - Tests with external dependencies

**Priority Boost:** Items in high-churn files get +1 severity

**Output Format (JSON Array):**
[{
  "id": "TEST-001",
  "type": "test_coverage",
  "subtype": "gap|quality|risk|health",
  "location": {"file": "src/payments/processor.ts", "function": "chargeCard"},
  "description": "Critical payment function has no test coverage",
  "severity": 5,
  "churn_score": 4,
  "effort_hours": 3,
  "suggestion": "Add unit tests for success, failure, and edge cases"
}]
```

### Performance Agent

```
Analyze performance issues and optimization opportunities.

Target: {target}
File Patterns: {file_patterns}
Tech Stack: {tech_stack}

**Analysis Categories:**

1. **Database Performance** (severity weighting: high)
   - N+1 query patterns
   - Missing indexes (from query patterns)
   - Unbounded queries (no LIMIT)
   - Inefficient JOINs

2. **Memory Issues** (severity weighting: high)
   - Large allocations in loops
   - Missing cleanup/disposal
   - Memory leak patterns (event listeners, closures)

3. **Async/Concurrency** (severity weighting: medium)
   - Blocking I/O in async contexts
   - Missing Promise.all for parallel ops
   - Sync file operations

4. **Frontend Performance** (JS/TS) (severity weighting: medium)
   - Large bundle imports
   - Missing code splitting/lazy loading
   - Excessive re-renders (React)
   - Missing memoization

**Output Format (JSON Array):**
[{
  "id": "PERF-001",
  "type": "performance",
  "subtype": "database|memory|async|frontend",
  "location": {"file": "src/api/users.ts", "line": 34},
  "description": "N+1 query: fetching user.posts individually in loop",
  "severity": 4,
  "impact_ms": 500,
  "effort_hours": 2,
  "suggestion": "Use eager loading: User.findAll({include: ['posts']})"
}]
```

### Security Agent

```
Analyze security vulnerabilities and risks.

Target: {target}
File Patterns: {file_patterns}
Critical Modules: {critical_modules}

**Analysis Categories:**

1. **Injection Risks** (severity weighting: critical)
   - SQL injection (string concatenation)
   - NoSQL injection
   - Command injection
   - Template injection

2. **XSS/CSRF** (severity weighting: high)
   - Unescaped user input in output
   - Missing CSRF tokens
   - innerHTML/dangerouslySetInnerHTML usage

3. **Auth/Authz** (severity weighting: critical)
   - Weak password requirements
   - Missing rate limiting
   - Broken access control
   - Insecure session handling

4. **Secrets Exposure** (severity weighting: critical)
   - Hardcoded credentials
   - API keys in source
   - Secrets in logs/error messages

**OWASP Mapping Required for Each Finding**

**Output Format (JSON Array):**
[{
  "id": "SEC-001",
  "type": "security",
  "subtype": "injection|xss|auth|secrets",
  "location": {"file": "src/api/query.ts", "line": 23},
  "description": "SQL query built with string concatenation from user input",
  "severity": 5,
  "owasp": "A03:2021-Injection",
  "cwe": "CWE-89",
  "effort_hours": 1,
  "suggestion": "Use parameterized queries: db.query('SELECT * FROM users WHERE id = ?', [userId])"
}]
```

### Documentation Agent

```
Analyze documentation quality and gaps.

Target: {target}
File Patterns: {file_patterns}
Public APIs: {public_apis}

**Analysis Categories:**

1. **API Documentation** (severity weighting: medium)
   - Public functions without JSDoc/docstrings
   - Missing parameter descriptions
   - Outdated documentation

2. **README Quality** (severity weighting: low)
   - Missing setup instructions
   - Outdated dependencies list
   - Broken links

3. **Changelog Gaps** (severity weighting: low)
   - Missing CHANGELOG entries
   - Undocumented breaking changes

4. **Inline Comments** (severity weighting: low)
   - Stale comments (code changed)
   - TODO/FIXME > 6 months old
   - Missing "why" comments for complex logic

**Output Format (JSON Array):**
[{
  "id": "DOC-001",
  "type": "documentation",
  "subtype": "api|readme|changelog|inline",
  "location": {"file": "src/utils/crypto.ts", "function": "hashPassword"},
  "description": "Complex password hashing function lacks documentation",
  "severity": 3,
  "effort_hours": 0.5,
  "suggestion": "Add JSDoc explaining algorithm choice and security considerations"
}]
```

### Type Safety Agent

```
Analyze type safety issues (TypeScript/Python with type hints).

Target: {target}
File Patterns: {file_patterns}
Language: {language}

**TypeScript Analysis:**

1. **Explicit Any** (severity weighting: high)
   - Direct `any` annotations
   - `any` in function signatures
   - `any` in generics

2. **Implicit Any** (severity weighting: medium)
   - Failed type inference
   - Missing return types
   - Untyped imports

3. **Type Assertions** (severity weighting: medium)
   - Overuse of `as` casting
   - Non-null assertions (`!`)

4. **Null Safety** (severity weighting: high)
   - Missing null checks
   - Inconsistent optional chaining

**Python Analysis:**

1. **Missing Type Hints** - Functions without annotations
2. **Type Ignore** - `# type: ignore` usage

**Output Format (JSON Array):**
[{
  "id": "TYPE-001",
  "type": "type_safety",
  "subtype": "explicit_any|implicit_any|assertion|null_safety",
  "location": {"file": "src/api/handler.ts", "line": 15},
  "description": "Function parameter typed as 'any': processData(data: any)",
  "severity": 3,
  "effort_hours": 0.5,
  "suggestion": "Define interface: interface ProcessInput { ... }"
}]
```

### AI Code Quality Agent (Level 4+)

```
Analyze AI-generated code for quality issues.

Target: {target}
File Patterns: {file_patterns}

**Detection Signals:**
- Unusual comment density
- Generic variable names (data, result, temp)
- Inconsistent style within file
- Boilerplate-heavy structures

**Analysis Categories:**

1. **Convention Violations** (severity weighting: medium)
   - Style inconsistent with project
   - Naming patterns differ from codebase
   - Import organization mismatch

2. **Implementation Issues** (severity weighting: high)
   - Hallucinated imports
   - Deprecated API usage
   - Incomplete error handling
   - Over-engineered solutions

3. **Maintenance Burden** (severity weighting: medium)
   - Poorly understood by team
   - Lacks domain knowledge
   - Excessive abstraction

**Output Format (JSON Array):**
[{
  "id": "AI-001",
  "type": "ai_code",
  "subtype": "convention|implementation|maintenance",
  "location": {"file": "src/components/DataGrid.tsx", "line": 1},
  "description": "AI-generated component uses deprecated React patterns",
  "severity": 3,
  "ai_confidence": 0.85,
  "effort_hours": 2,
  "suggestion": "Refactor to use modern React patterns (hooks, functional components)"
}]
```

### Knowledge Silo Agent (Level 4+)

```
Analyze knowledge distribution and bus factor risks.

Target: {target}
Author Map: {author_map}
Churn Data: {churn_data}

**Analysis Categories:**

1. **Bus Factor Analysis** (severity weighting: critical for core modules)
   - Files with single author ever
   - Critical files with limited knowledge
   - Calculate bus factor per module

2. **Ownership Gaps** (severity weighting: high)
   - Orphaned code (author left)
   - No clear maintainer
   - Stale CODEOWNERS entries

3. **Knowledge Islands** (severity weighting: medium)
   - Isolated expertise areas
   - No cross-training evidence
   - Single-expert subsystems

4. **Onboarding Friction** (severity weighting: low)
   - High complexity + low documentation
   - Unusual patterns
   - Missing tests explaining behavior

**Output Format (JSON Array):**
[{
  "id": "SILO-001",
  "type": "knowledge_silo",
  "subtype": "bus_factor|ownership|island|onboarding",
  "location": {"module": "src/payments/", "file": "stripe-integration.ts"},
  "description": "Critical payment module has bus factor of 1",
  "severity": 5,
  "bus_factor": 1,
  "last_author": "jane@example.com",
  "last_touched": "2024-02-15",
  "effort_hours": 8,
  "suggestion": "Schedule knowledge transfer session, add comprehensive documentation"
}]
```

## Phase 4: Synthesis Agent Prompts

### Correlation Agent

```
Correlate findings across all analysis workers.

Worker Results: {all_worker_results}

**Tasks:**

1. **Root Cause Identification**
   - Find single issues causing multiple symptoms
   - Identify architectural decisions creating debt clusters
   - Detect knowledge gaps indicated by patterns

2. **Dependency Mapping**
   - Which fixes enable other fixes
   - Which issues block each other
   - Optimal fix ordering

3. **Pattern Recognition**
   - Repeated mistakes across codebase
   - Team-wide anti-patterns
   - Module-specific issues

4. **Cluster Analysis**
   - Group related issues
   - Identify refactoring opportunities
   - Batch fix possibilities

**Output Format (JSON):**
{
  "root_causes": [
    {
      "id": "RC-001",
      "description": "Missing abstraction layer between API and database",
      "symptoms": ["ARCH-001", "TEST-003", "PERF-002"],
      "fix_unlocks": ["TEST-003", "PERF-002"]
    }
  ],
  "dependencies": {
    "ARCH-001": [],
    "TEST-003": ["ARCH-001"],
    "PERF-002": ["ARCH-001"]
  },
  "patterns": [
    {
      "pattern": "N+1 queries in all handlers",
      "occurrences": 8,
      "locations": ["src/handlers/"],
      "fix_approach": "Add repository pattern with eager loading"
    }
  ],
  "clusters": [
    {
      "name": "Handler refactoring",
      "items": ["CQ-001", "CQ-002", "ARCH-003"],
      "suggested_approach": "Extract to service layer"
    }
  ]
}
```

### Business Impact Agent

```
Calculate business cost and DevEx impact of technical debt.

Issues: {all_issues}
Hourly Rate: ${hourly_rate}
Team Size: {team_size}
Codebase LOC: {loc}
Correlations: {correlations}

**Calculations:**

1. **Per-Issue Cost**
   Remediation Cost = fix_hours × hourly_rate
   Interest Cost = (severity/5) × base_interest × 12
   Total Annual Cost = Remediation + Interest

   Base Interest by Type:
   - Security: $500/month
   - Performance: $200/month
   - Architecture: $300/month
   - Code Quality: $100/month
   - Knowledge Silo: $250/month

2. **Technical Debt Ratio (TDR)**
   TDR = (Total Remediation Cost / Annual Dev Budget) × 100%

   Ratings:
   - < 10%: Excellent
   - 10-25%: Good
   - 25-42%: Average (Stripe: 42%)
   - 42-60%: Concerning
   - > 60%: Critical

3. **DevEx Impact**
   Hours_Lost_Weekly = Σ(issue_friction × touch_frequency)
   Productivity_Tax = Hours_Lost / 40h × 100%

4. **ROI Ranking**
   ROI = (Annual_Savings - Remediation) / Remediation × 100%
   Priority = ROI × Confidence

**Output Format (JSON):**
{
  "total_cost": {
    "remediation_usd": 125000,
    "annual_interest_usd": 48000,
    "total_annual_usd": 173000
  },
  "tdr": {
    "percent": 28.5,
    "rating": "average",
    "industry_benchmark": 42
  },
  "devex": {
    "hours_lost_weekly": 12.5,
    "productivity_tax_percent": 31.25,
    "top_friction": [
      {"type": "complexity", "hours": 4.5},
      {"type": "missing_docs", "hours": 3.2}
    ]
  },
  "roi_ranking": [
    {"id": "SEC-001", "roi_percent": 450, "payback_weeks": 2},
    {"id": "PERF-001", "roi_percent": 320, "payback_weeks": 4}
  ],
  "quick_wins": [
    {"id": "DEP-001", "effort": 0.5, "savings": 2400}
  ]
}
```

## Phase 5: Validation Agent

### Self-Critique Agent

```
Critically validate all analysis findings.

Findings: {prioritized_items}
Codebase Context: {context_summary}
Correlations: {correlations}

**Validation Tasks:**

1. **False Positive Check**
   - Is this actually an issue?
   - Is context missing that explains the pattern?
   - Is this an intentional design decision?

2. **Severity Validation**
   - Is severity accurate given context?
   - Are edge cases considered?
   - Is business impact correctly assessed?

3. **Fix Appropriateness**
   - Is suggested fix correct?
   - Are there better alternatives?
   - Does fix introduce new issues?

4. **Deduplication**
   - Remove duplicate findings
   - Merge related issues
   - Consolidate overlapping items

5. **Confidence Assignment**
   - High (0.9-1.0): Definitely an issue
   - Medium (0.7-0.9): Likely an issue
   - Low (0.5-0.7): Needs human review

**Output Format (JSON):**
{
  "validated_items": [
    {"id": "SEC-001", "confidence": 0.95, "validated": true}
  ],
  "removed_items": [
    {"id": "CQ-005", "reason": "Intentional pattern per team convention"}
  ],
  "adjusted_items": [
    {"id": "PERF-002", "field": "severity", "old": 4, "new": 3, "reason": "Edge case only"}
  ],
  "review_needed": [
    {"id": "ARCH-003", "reason": "Requires domain knowledge to validate"}
  ],
  "confidence_distribution": {
    "high": 65,
    "medium": 25,
    "low": 10
  }
}
```

## Phase 6: Remediation Agent Prompts

### Auto-Fix Agent

```
Generate fix patches for validated quick wins.

Quick Wins: {quick_wins}
Codebase Context: {context}

**Eligibility Criteria:**
- Confidence >= 0.8
- Effort <= 2 hours
- No breaking changes
- Clear solution path

**Fix Generation Process:**

For each eligible item:
1. Read current file content
2. Identify exact change location
3. Generate minimal, safe fix
4. Preserve surrounding code
5. Follow project style
6. Create unified diff

**Supported Fix Types:**
- Naming improvements
- Type annotations
- Unused code removal
- Simple refactorings
- Null checks
- Documentation additions

**Output Format (JSON):**
{
  "patches": [
    {
      "id": "TYPE-001",
      "file": "src/api/handler.ts",
      "description": "Add type annotation to processData parameter",
      "diff": "--- a/src/api/handler.ts\n+++ b/src/api/handler.ts\n@@ -15,1 +15,1 @@\n-function processData(data: any) {\n+function processData(data: ProcessInput) {",
      "verification": "Run: npx tsc --noEmit"
    }
  ],
  "skipped": [
    {"id": "ARCH-001", "reason": "Requires architectural decision"}
  ],
  "stats": {
    "eligible": 12,
    "generated": 8,
    "skipped": 4
  }
}
```

### PR Generator Agent

```
Generate PR descriptions for fix patches.

Patches: {patches}
Project: {project_name}

**Grouping Strategy:**
Group patches by type or module for logical PRs.

**PR Format:**

Title: "[type] Brief description"

Body:
## Summary
[1-2 sentences describing the changes]

## Changes
[File-by-file breakdown]

## Impact
- Lines changed: N
- Files affected: N
- Risk level: Low/Medium

## Testing
- [ ] Type check passes
- [ ] Tests pass
- [ ] Manual verification complete

## Metrics Improvement
- Technical Debt: -$X,XXX
- [Other relevant metrics]

**Output Format (JSON):**
{
  "prs": [
    {
      "title": "[types] Add missing type annotations in api module",
      "body": "## Summary\n...",
      "files": ["src/api/handler.ts", "src/api/router.ts"],
      "labels": ["tech-debt", "auto-generated", "low-risk"],
      "estimated_review_time": "15 min"
    }
  ]
}
```

## Phase 7: Output Agent

### Synthesis Agent

```
Generate final technical debt report.

Data:
- Target: {target}
- Level: {level}
- Validated Items: {validated_items}
- Correlations: {correlations}
- Business Impact: {business_impact}
- Patches: {patches}
- Format: {format}

**Report Sections:**

1. **Executive Summary**
   - Total issues, cost, TDR
   - Key risk areas
   - Top 3 root causes

2. **Issue Breakdown by Category**
   - Table with counts per category
   - Cost per category

3. **Critical Issues (Detailed)**
   - Full details with solutions

4. **Quick Wins**
   - Checkbox list with effort/ROI

5. **Implementation Roadmap**
   - Dependency-aware phases
   - Effort estimates per phase

6. **Metrics to Track**
   - Current vs target values

7. **Appendix**
   - Worker statistics
   - Validation summary

**Template:** Use assets/report_template_{format}.md

**Output:** Complete report in requested format(s)
```
