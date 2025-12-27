# Agent Prompts Reference - v3

Comprehensive prompts for all 8 analysis workers plus coordination agents.

## Code Quality Agent

```
Analyze codebase for code quality issues.

Target: {target}
File Patterns: {file_patterns}
High-Churn Files: {churn_files}

**Analysis Tasks:**

1. **Complexity Analysis**
   - Cyclomatic complexity > 10
   - Cognitive complexity > 15
   - Nesting depth > 4 levels
   - Methods > 50 lines
   - Files > 500 lines

2. **Duplication Detection**
   - Repeated code blocks > 6 lines
   - Similar logic patterns (structural clones)
   - Copy-paste with minor variations

3. **Code Smells**
   - Long parameter lists (> 4 params)
   - God classes (> 300 lines, multiple responsibilities)
   - Feature envy (excessive use of other class data)
   - Dead code (unreachable/unused)
   - Magic numbers/strings

4. **Naming & Conventions**
   - Inconsistent naming patterns
   - Cryptic abbreviations
   - Single-letter variables (non-loop)

**Output:** JSON array [{id, type:"code_quality", subtype, location, severity:1-5, description, fix}]
```

## Dependency Agent

```
Analyze dependencies for vulnerabilities and health.

Dependency File: {dep_file}
Package Manager: {pkg_manager}

**Analysis Tasks:**

1. **Security Vulnerabilities**
   - CVEs in direct dependencies
   - CVEs in transitive dependencies
   - CVSS severity scoring

2. **Outdated Packages**
   - Major version updates available
   - Packages > 1 year without updates
   - Deprecated packages

3. **License Compliance**
   - Incompatible licenses (GPL in MIT project)
   - Missing license declarations
   - Commercial license requirements

4. **Bundle Impact** (JS/TS)
   - Large dependencies (> 100KB)
   - Duplicate packages in tree
   - Lighter alternatives available

5. **Maintenance Health**
   - Abandoned repositories (> 2 years)
   - Known maintenance issues
   - Bus factor concerns

**Output:** JSON array [{id, type:"dependency", subtype, package, current, recommended, severity:1-5, cve}]
```

## Architecture Agent

```
Analyze architectural quality and patterns.

Target: {target}
File Patterns: {file_patterns}
Module Map: {module_map}

**Analysis Tasks:**

1. **Coupling Analysis**
   - High afferent/efferent coupling
   - Circular dependencies
   - God modules (importing/exporting everything)

2. **Layering Violations**
   - UI accessing database directly
   - Business logic in presentation
   - Cross-layer imports

3. **SOLID Violations**
   - SRP: Classes with multiple responsibilities
   - OCP: Modifications instead of extensions
   - LSP: Substitution violations
   - ISP: Fat interfaces
   - DIP: Concrete dependencies

4. **Pattern Consistency**
   - Mixed state management approaches
   - Inconsistent error handling
   - Varied API response structures

5. **Configuration Debt**
   - Hardcoded values
   - Environment-specific code in source
   - Missing env validation

**Output:** JSON array [{id, type:"architecture", subtype, location, severity:1-5, impact, suggestion}]
```

## Test Coverage Agent

```
Analyze test coverage and quality.

Target: {target}
Test Patterns: {test_patterns}
High-Churn Files: {churn_files}
Critical Modules: {critical_modules}

**Analysis Tasks:**

1. **Coverage Gaps**
   - Source files without tests
   - Public functions without coverage
   - Critical paths untested

2. **Test Quality**
   - Tests without meaningful assertions
   - Snapshot tests without review
   - Testing implementation vs behavior
   - Missing edge cases

3. **High-Risk Untested**
   - Authentication/authorization untested
   - Payment/financial logic untested
   - Error handling paths untested

4. **Test Health**
   - Flaky tests (non-deterministic)
   - Slow tests (> 5s)
   - Tests with external dependencies
   - Poor test isolation

**Priority:** Cross-reference churn files - untested high-churn code is critical.

**Output:** JSON array [{id, type:"test_coverage", subtype, location, severity:1-5, churn:0-5, suggestion}]
```

## Performance Agent (NEW)

```
Analyze performance issues and optimization opportunities.

Target: {target}
File Patterns: {file_patterns}
Tech Stack: {tech_stack}

**Analysis Tasks:**

1. **Database Performance**
   - N+1 query patterns
   - Missing indexes (from query patterns)
   - Unbounded queries (no LIMIT)
   - Inefficient JOINs

2. **Memory Issues**
   - Large object allocations in loops
   - Missing cleanup/disposal
   - Memory leak patterns (event listeners, closures)
   - Unbounded caches

3. **Async/Concurrency**
   - Blocking I/O in async contexts
   - Missing Promise.all for parallel ops
   - Sync file operations
   - Thread pool exhaustion patterns

4. **Frontend Performance** (JS/TS)
   - Large bundle imports
   - Missing code splitting
   - Render-blocking operations
   - Excessive re-renders (React)
   - Missing memoization

5. **Caching Opportunities**
   - Repeated expensive computations
   - Cacheable API responses
   - Static data recomputed

**Output:** JSON array [{id, type:"performance", subtype, location, severity:1-5, impact_ms, suggestion}]
```

## Security Agent (NEW)

```
Analyze security vulnerabilities and risks.

Target: {target}
File Patterns: {file_patterns}
Critical Modules: {critical_modules}

**Analysis Tasks:**

1. **Injection Risks**
   - SQL injection (string concatenation)
   - NoSQL injection
   - Command injection
   - LDAP injection
   - Template injection

2. **XSS/CSRF**
   - Unescaped user input in output
   - Missing CSRF tokens
   - innerHTML/dangerouslySetInnerHTML usage
   - Missing Content-Security-Policy

3. **Authentication/Authorization**
   - Weak password requirements
   - Missing rate limiting
   - Insecure session handling
   - Broken access control
   - Missing auth checks

4. **Secrets Exposure**
   - Hardcoded credentials
   - API keys in source
   - Secrets in logs
   - Exposed in error messages

5. **Input Validation**
   - Missing input sanitization
   - Unsafe deserialization
   - Path traversal risks
   - File upload vulnerabilities

**OWASP Top 10 mapping included in each finding.**

**Output:** JSON array [{id, type:"security", subtype, location, severity:1-5, owasp, cwe, suggestion}]
```

## Documentation Agent (NEW)

```
Analyze documentation quality and gaps.

Target: {target}
File Patterns: {file_patterns}
Public APIs: {public_apis}

**Analysis Tasks:**

1. **API Documentation**
   - Public functions without JSDoc/docstrings
   - Missing parameter descriptions
   - Missing return type documentation
   - Outdated documentation (code changed)

2. **README Quality**
   - Missing setup instructions
   - Outdated dependencies list
   - Missing environment variables
   - Broken links

3. **Changelog Gaps**
   - Missing CHANGELOG entries
   - Undocumented breaking changes
   - Version gaps

4. **Inline Comments**
   - Stale comments (code changed)
   - TODO/FIXME > 6 months old
   - Comments contradicting code
   - Missing "why" comments for complex logic

5. **Architecture Docs**
   - Missing system diagrams
   - Undocumented design decisions
   - Missing onboarding docs

**Output:** JSON array [{id, type:"documentation", subtype, location, severity:1-5, suggestion}]
```

## Type Safety Agent (NEW)

```
Analyze type safety issues (TypeScript/Python with type hints).

Target: {target}
File Patterns: {file_patterns}
Language: {language}

**TypeScript Analysis:**

1. **Explicit Any**
   - Direct `any` type annotations
   - `any` in function signatures
   - `any` in generics

2. **Implicit Any**
   - Failed type inference
   - Missing function return types
   - Untyped imports

3. **Type Assertions**
   - Overuse of `as` casting
   - Non-null assertions (`!`)
   - Type assertions hiding bugs

4. **Null Safety**
   - Missing null checks
   - Inconsistent optional chaining
   - Unsafe property access

5. **Generic Issues**
   - Missing constraints
   - Overly permissive generics
   - Type parameter unused

**Python Analysis:**

1. **Missing Type Hints**
   - Functions without annotations
   - Missing return types
   - Untyped class attributes

2. **Type Ignore Comments**
   - `# type: ignore` usage
   - Suppressed mypy errors

**Output:** JSON array [{id, type:"type_safety", subtype, location, severity:1-5, suggestion}]
```

## Correlation Agent Prompt

```
Correlate findings across all 8 analysis workers.

Worker Results:
- Code Quality: {code_quality_results}
- Dependency: {dependency_results}
- Architecture: {architecture_results}
- Test Coverage: {test_coverage_results}
- Performance: {performance_results}
- Security: {security_results}
- Documentation: {documentation_results}
- Type Safety: {type_safety_results}

**Tasks:**

1. **Root Cause Identification**
   - Single issues causing multiple symptoms
   - Architectural decisions creating debt clusters
   - Knowledge gaps indicated by patterns

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

**Output:**
{
  root_causes: [{id, description, symptoms[], fix_unlocks[]}],
  dependencies: {item_id: [blocked_by_ids]},
  patterns: [{pattern, occurrences, fix_approach}],
  clusters: [{name, items[], suggested_approach}]
}
```

## Impact Analysis (RICE Scoring) Prompt

```
Apply RICE scoring for prioritization.

Items: {all_items}
Correlations: {correlations}
Critical Modules: {critical_modules}
Churn Data: {churn_data}

**RICE Calculation:**

Reach (1-10): What % of codebase/users affected
- 10: Entire application
- 7-9: Core functionality
- 4-6: Major feature
- 1-3: Isolated component

Impact (1-10): Severity if unaddressed
- 10: Security breach, data loss
- 7-9: Major bugs, outages
- 4-6: Performance issues, UX problems
- 1-3: Minor inconvenience

Confidence (0.5-1.0): Assessment certainty
- 1.0: Verified, reproducible
- 0.8: High confidence
- 0.5: Uncertain, needs investigation

Effort (person-hours): Fix complexity
- 1-2h: Simple fix
- 4-8h: Moderate refactor
- 16-40h: Major refactor
- 40+h: Rewrite/redesign

**RICE Score = (Reach × Impact × Confidence) / Effort**

**Categorization:**
- Critical (RICE >= 50): This sprint
- High (RICE 20-50): This quarter
- Medium (RICE < 20): Backlog

**Quick Wins:** Impact >= 7, Effort <= 2h

**Output:**
{
  prioritized_items: [...sorted by RICE],
  quick_wins: [...],
  critical_count, high_count, medium_count,
  total_effort_hours
}
```

## Self-Critique Agent Prompt

```
Critically validate analysis findings.

Findings: {prioritized_items}
Codebase Context: {context}

**Validation Tasks:**

1. **False Positive Check**
   - Is this actually an issue?
   - Is context missing that would explain the pattern?
   - Is this intentional design decision?

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

5. **Confidence Tagging**
   - High: Definitely an issue
   - Medium: Likely an issue
   - Low: Needs human review

**Output:**
{
  validated_items: [...],
  removed_items: [{id, reason}],
  adjusted_items: [{id, field, old, new, reason}],
  review_needed: [{id, reason}]
}
```
