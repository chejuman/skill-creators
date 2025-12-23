# Agent Prompts Reference

Detailed prompts for each worker agent in the resolve-debt-v2 system.

## Code Smell Agent Prompt

```
Analyze codebase for code smells and quality issues.

Target: {target}
File Patterns: {file_patterns}
High-Churn Files: {churn_files}

**Analysis Tasks:**

1. **Complexity Analysis**
   - Find functions with cyclomatic complexity > 10
   - Identify deeply nested code (> 4 levels)
   - Locate methods exceeding 50 lines

2. **Duplication Detection**
   - Search for repeated code blocks (> 10 lines)
   - Identify copy-paste patterns
   - Find similar logic in different files

3. **Code Smell Patterns**
   - Long parameter lists (> 5 params)
   - God classes (> 500 lines, many responsibilities)
   - Feature envy (methods using other class data)
   - Dead code (unused functions, variables)
   - Magic numbers/strings without constants

4. **Naming & Conventions**
   - Inconsistent naming patterns
   - Single-letter variables (except loop counters)
   - Misleading or unclear names

5. **TODO/FIXME Markers**
   - Grep for TODO, FIXME, HACK, XXX comments
   - Categorize by age and severity

**Output Format:**
Return JSON array:
[{
  "id": "CS-001",
  "type": "code_smell",
  "subtype": "complexity|duplication|naming|dead_code",
  "location": "file:line",
  "description": "issue description",
  "severity": 1-5,
  "suggestion": "how to fix"
}]
```

## Dependency Agent Prompt

```
Analyze project dependencies for vulnerabilities and updates.

Dependency File: {dep_file}
Package Manager: {pkg_manager}

**Analysis Tasks:**

1. **Security Vulnerabilities**
   - Check npm audit / pip-audit results
   - Identify CVEs in dependencies
   - Flag critical and high severity issues

2. **Outdated Packages**
   - List packages with major version updates available
   - Identify packages > 1 year without updates
   - Check for deprecated packages

3. **Dependency Health**
   - Packages with known maintenance issues
   - Abandoned or archived repositories
   - License compatibility concerns

4. **Bundle Analysis** (for JS projects)
   - Large dependencies impacting bundle size
   - Duplicate packages in dependency tree
   - Packages that could be replaced with lighter alternatives

5. **Version Constraints**
   - Loose version constraints (^, *, latest)
   - Conflicting peer dependencies
   - Lock file inconsistencies

**Output Format:**
Return JSON array:
[{
  "id": "DEP-001",
  "type": "dependency",
  "subtype": "vulnerability|outdated|health|bundle|version",
  "package": "package-name",
  "current_version": "x.y.z",
  "recommended_version": "a.b.c",
  "severity": 1-5,
  "description": "issue description",
  "cve": "CVE-xxxx-xxxxx" (if applicable)
}]
```

## Architecture Agent Prompt

```
Analyze codebase for architectural issues and pattern violations.

Target: {target}
File Patterns: {file_patterns}

**Analysis Tasks:**

1. **Coupling Analysis**
   - High coupling between modules
   - Circular dependencies
   - God modules importing everything

2. **Layering Violations**
   - Direct database access from UI layer
   - Business logic in presentation layer
   - Cross-layer dependencies

3. **Pattern Consistency**
   - Mixed architectural patterns
   - Inconsistent error handling approaches
   - Varied state management patterns

4. **API Design Issues**
   - Inconsistent endpoint naming
   - Missing versioning
   - Overly complex response structures

5. **Configuration Issues**
   - Hardcoded values that should be configurable
   - Environment-specific code in source
   - Missing environment variable validation

6. **SOLID Violations**
   - Large classes with multiple responsibilities (SRP)
   - Concrete dependencies instead of abstractions (DIP)
   - Interface segregation issues (ISP)

**Output Format:**
Return JSON array:
[{
  "id": "ARCH-001",
  "type": "architecture",
  "subtype": "coupling|layering|pattern|api|config|solid",
  "location": "file or module",
  "description": "issue description",
  "severity": 1-5,
  "impact": "what problems this causes",
  "suggestion": "recommended approach"
}]
```

## Test Coverage Agent Prompt

```
Analyze test coverage and testing gaps.

Target: {target}
Test Patterns: {test_patterns}
High-Churn Files: {churn_files}

**Analysis Tasks:**

1. **Coverage Gaps**
   - Source files without corresponding tests
   - Functions/methods with no test coverage
   - Critical paths without integration tests

2. **Test Quality**
   - Tests without assertions
   - Brittle tests with hardcoded values
   - Tests that test implementation, not behavior
   - Missing edge case coverage

3. **Test Organization**
   - Inconsistent test file naming
   - Tests in wrong directories
   - Missing test utilities/helpers

4. **High-Risk Untested Code**
   - Business-critical functions without tests
   - Error handling paths without coverage
   - Authentication/authorization without tests
   - Financial/transaction code without tests

5. **Test Performance**
   - Slow running tests (> 5 seconds)
   - Tests with external dependencies
   - Tests without proper isolation

**Priority Focus:**
Cross-reference with high-churn files - untested high-churn code is highest priority.

**Output Format:**
Return JSON array:
[{
  "id": "TEST-001",
  "type": "test_coverage",
  "subtype": "missing|quality|organization|risk|performance",
  "location": "file or function",
  "description": "issue description",
  "severity": 1-5,
  "churn_score": 0-5 (how often this code changes),
  "suggestion": "what tests to add"
}]
```

## Analysis Agent Prompt

```
Synthesize worker results into prioritized debt inventory.

Input Data:
- Code Smell Results: {code_smell_results}
- Dependency Results: {dependency_results}
- Architecture Results: {architecture_results}
- Test Coverage Results: {test_coverage_results}

**Prioritization Algorithm:**

For each item, calculate Priority Score:
  Priority = (Severity x Change_Frequency) / Fix_Effort

Where:
- Severity: 1-5 (from worker analysis)
- Change_Frequency: 1-5 (derived from git churn data)
- Fix_Effort: 1-5 (estimated based on item type)

**Fix Effort Estimates:**
- Naming fix: 1
- Add missing test: 2
- Extract method: 2
- Update dependency: 2-3
- Remove duplication: 3
- Reduce complexity: 3-4
- Architecture refactor: 4-5

**Categorization:**
- Critical (Score >= 4): Sprint priority
- High (Score 2-4): Quarter priority
- Medium (Score < 2): Backlog

**Quick Wins Criteria:**
- Fix effort <= 2
- Severity >= 3
- No dependencies on other fixes
- < 30 minutes estimated time

**Output:**
Return structured data:
{
  "total_items": N,
  "critical_count": N,
  "high_count": N,
  "medium_count": N,
  "estimated_hours": N,
  "prioritized_items": [...sorted by priority score...],
  "quick_wins": [...items matching quick win criteria...],
  "dependency_map": {"item_id": ["depends_on_ids"]}
}
```

## Synthesis Agent Prompt

```
Generate final technical debt report.

Input:
- Target: {target}
- Level: {level}
- Analysis Results: {analysis_results}

**Report Sections:**

1. **Executive Summary**
   - Total items found
   - Critical items count
   - Estimated total effort
   - Key risk areas

2. **Debt Inventory Table**
   - ID, Type, Location, Severity, Description

3. **Prioritized Resolution Plan**
   - Critical: Detailed with solutions
   - High: Detailed with solutions
   - Medium: Summary list

4. **Quick Wins**
   - Checkbox list of < 30 min fixes

5. **Implementation Order**
   - Dependency-aware sequence
   - What each step unblocks

6. **Metrics to Track**
   - Current state
   - Target state
   - How to measure

Use template from assets/report_template.md
Output clean markdown format.
```
