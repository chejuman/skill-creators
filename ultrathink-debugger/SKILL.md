---
name: ultrathink-debugger
description: Multi-agent debugging orchestrator with intelligent triage. Spawns parallel debugging agents (Systematic, RootCause, DefenseInDepth, Verification) based on error classification. Use when encountering bugs, test failures, or unexpected behavior. Triggers on "debug", "find bug", "root cause", "why is this failing", or complex error investigation.
---

# Ultrathink Debugger

Multi-agent debugging system that analyzes errors from multiple angles simultaneously.

## Architecture

```
Error Input
    │
    ▼
┌─────────────────────────────────┐
│       TRIAGE AGENT              │
│  (Classify problem type)        │
└─────────────────────────────────┘
    │
    ├── Runtime Error ────► Systematic + RootCause
    ├── Test Failure ─────► Systematic + Verification
    ├── Data Corruption ──► RootCause + DefenseInDepth
    ├── Integration Bug ──► All 4 agents (parallel)
    └── Unknown ──────────► Systematic + Web Research
    │
    ▼
┌─────────────────────────────────┐
│     PARALLEL DEBUG AGENTS       │
│  (Run selected agents)          │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│     SYNTHESIS AGENT             │
│  (Combine findings → Report)    │
└─────────────────────────────────┘
```

## Usage

```
/ultrathink-debugger [error description or stack trace]
```

Or naturally: "Debug this error", "Why is this test failing?", "Find the root cause"

## Triage Agent

**Purpose:** Classify error type and select appropriate debugging agents.

**Classification Categories:**

| Category | Indicators | Selected Agents |
|----------|-----------|-----------------|
| Runtime Error | Exception, crash, undefined | Systematic + RootCause |
| Test Failure | Assertion fail, expect mismatch | Systematic + Verification |
| Data Corruption | Wrong values, state pollution | RootCause + DefenseInDepth |
| Integration Bug | Multi-component, cascading | All 4 (parallel) |
| Performance | Slow, timeout, memory | Systematic + WebResearch |
| Unknown | Unclear symptoms | Systematic + WebResearch |

**Triage Execution:**

```
Task(
  subagent_type='general-purpose',
  model='haiku',
  prompt='''Analyze this error and classify:

ERROR: {error_description}

Classify into ONE category:
- RUNTIME_ERROR: Exception, crash, null/undefined
- TEST_FAILURE: Assertion failed, expected vs actual mismatch
- DATA_CORRUPTION: Wrong values propagated, state pollution
- INTEGRATION_BUG: Multiple components involved, cascading failures
- PERFORMANCE: Timeout, slow execution, memory issues
- UNKNOWN: Cannot determine category

Output format:
CATEGORY: <category>
CONFIDENCE: <high/medium/low>
REASONING: <1-2 sentences>
RECOMMENDED_AGENTS: <comma-separated list>''',
  description='Triage error classification'
)
```

## Debug Agents

### 1. Systematic Debugging Agent

**Focus:** Four-phase framework - Root cause before fixes.

```
Task(
  subagent_type='general-purpose',
  prompt='''Apply Systematic Debugging to this error:

ERROR: {error}
CONTEXT: {context}

Follow these phases:

PHASE 1 - ROOT CAUSE INVESTIGATION:
- Read error messages completely
- Can you reproduce consistently?
- What changed recently? (git diff)
- Add diagnostic instrumentation if multi-component

PHASE 2 - PATTERN ANALYSIS:
- Find working similar code
- Compare against references
- List all differences

PHASE 3 - HYPOTHESIS:
- State: "Root cause is X because Y"
- Propose minimal test

PHASE 4 - FIX RECOMMENDATION:
- Address root cause, not symptom
- Suggest failing test case
- Single focused change

Output in markdown with clear sections.''',
  description='Systematic debugging analysis',
  run_in_background=True
)
```

### 2. Root Cause Tracing Agent

**Focus:** Trace backwards through call stack to find origin.

```
Task(
  subagent_type='general-purpose',
  prompt='''Apply Root Cause Tracing to this error:

ERROR: {error}
STACK TRACE: {stack_trace}

TRACING PROCESS:
1. SYMPTOM: Where does error appear?
2. IMMEDIATE CAUSE: What code directly causes it?
3. TRACE UP: What called this? What value was passed?
4. KEEP TRACING: Continue until you find the source
5. ORIGIN: Where did bad value originate?

For each level, document:
- Function/method name
- File:line number
- Value at this point
- Who passed this value?

ADD INSTRUMENTATION if needed:
```javascript
const stack = new Error().stack;
console.error('DEBUG:', { variable, cwd: process.cwd(), stack });
```

Output: Call chain visualization + root origin identified''',
  description='Root cause tracing analysis',
  run_in_background=True
)
```

### 3. Defense-in-Depth Agent

**Focus:** Validate at every layer - Make bug impossible.

```
Task(
  subagent_type='general-purpose',
  prompt='''Apply Defense-in-Depth Validation:

ERROR: {error}
DATA FLOW: {data_flow}

MAP THE FOUR LAYERS:

LAYER 1 - ENTRY POINT:
- Where does data enter the system?
- What validation exists? What's missing?

LAYER 2 - BUSINESS LOGIC:
- Does the operation validate its inputs?
- What assumptions are made?

LAYER 3 - ENVIRONMENT GUARDS:
- Are there context-specific protections?
- Test vs Production differences?

LAYER 4 - DEBUG INSTRUMENTATION:
- Is there logging before dangerous operations?
- Can you trace the issue forensically?

For each layer, recommend:
- Current state (exists/missing)
- Suggested validation code
- What it would catch

Goal: Make this bug structurally impossible.''',
  description='Defense-in-depth analysis',
  run_in_background=True
)
```

### 4. Verification Agent

**Focus:** Evidence before claims - Run and confirm.

```
Task(
  subagent_type='general-purpose',
  prompt='''Apply Verification Before Completion:

CLAIMED FIX: {proposed_fix}
CONTEXT: {context}

VERIFICATION CHECKLIST:

1. IDENTIFY: What command proves the fix works?
2. RUN: Execute the verification command
3. READ: Full output, check exit code
4. VERIFY: Does output confirm the claim?

For regression testing:
- Write test → Run (should pass)
- Revert fix → Run (MUST FAIL)
- Restore fix → Run (should pass)

RED FLAGS to check:
- "Should work now" without running
- Partial verification only
- Trusting agent reports without checking

Output: Verification commands + expected results''',
  description='Verification analysis',
  run_in_background=True
)
```

### 5. Web Research Agent (Optional)

**Focus:** Real-time research for unknown errors.

```
WebSearch(query='{error_message} solution 2025')
WebSearch(query='{framework} {error_type} fix')

Task(
  subagent_type='Explore',
  model='haiku',
  prompt='Research solutions for: {error}',
  description='Web research for error',
  run_in_background=True
)
```

## Execution Flow

### Step 1: Receive Error
```python
error_input = {
    'description': user_error_description,
    'stack_trace': extracted_stack_trace,
    'context': relevant_code_context,
    'recent_changes': git_diff_if_available
}
```

### Step 2: Triage Classification
```
# Run triage agent (fast, synchronous)
triage_result = Task(
  subagent_type='general-purpose',
  model='haiku',
  prompt=triage_prompt.format(**error_input),
  description='Triage classification'
)
```

### Step 3: Spawn Debug Agents (Parallel)
```python
# Based on triage, spawn selected agents in parallel
agents = []

if 'SYSTEMATIC' in recommended_agents:
    agents.append(Task(...systematic_agent...))

if 'ROOTCAUSE' in recommended_agents:
    agents.append(Task(...rootcause_agent...))

if 'DEFENSE' in recommended_agents:
    agents.append(Task(...defense_agent...))

if 'VERIFICATION' in recommended_agents:
    agents.append(Task(...verification_agent...))

if 'WEBRESEARCH' in recommended_agents:
    agents.append(WebSearch(...))

# All agents run in parallel with run_in_background=True
```

### Step 4: Collect Results
```python
# Wait for all agents to complete
for agent in agents:
    result = TaskOutput(task_id=agent.id, block=True)
    findings.append(result)
```

### Step 5: Synthesize Report
```
Task(
  subagent_type='general-purpose',
  prompt='''Synthesize debugging findings into final report:

TRIAGE: {triage_result}

FINDINGS:
{all_agent_findings}

Create a unified report with:
1. EXECUTIVE SUMMARY (2-3 sentences)
2. ROOT CAUSE IDENTIFIED
3. EVIDENCE (from each agent)
4. RECOMMENDED FIX (specific, actionable)
5. PREVENTION (defense-in-depth recommendations)
6. VERIFICATION STEPS

Format as clean markdown.''',
  description='Synthesize debug report'
)
```

## Output Format

```markdown
# Debug Report: {error_title}

## Executive Summary
{2-3 sentence summary of root cause and fix}

## Triage Classification
- **Category:** {category}
- **Confidence:** {high/medium/low}
- **Agents Used:** {list of agents}

## Root Cause Analysis

### Call Chain
{visualization of call stack to root}

### Origin Point
- **File:** {file:line}
- **Issue:** {what's wrong}
- **Why:** {why it's wrong}

## Evidence

### From Systematic Analysis
{key findings}

### From Root Cause Tracing
{call chain + origin}

### From Defense-in-Depth
{layer gaps identified}

### From Verification
{commands to verify}

## Recommended Fix

```{language}
{specific code change}
```

## Prevention Layers

| Layer | Current | Recommended |
|-------|---------|-------------|
| Entry | {status} | {add validation} |
| Logic | {status} | {add check} |
| Environment | {status} | {add guard} |
| Debug | {status} | {add logging} |

## Verification Steps

1. Run: `{command}`
2. Expected: `{output}`
3. Regression: {test to add}
```

## Depth Levels

| Level | Agents | Use Case |
|-------|--------|----------|
| 1 | Triage only | Quick classification |
| 2 | Triage + 1 agent | Simple bugs |
| 3 (default) | Triage + 2 agents | Standard debugging |
| 4 | Triage + 3 agents | Complex issues |
| 5 | All 4 + WebResearch | Critical/unknown bugs |

## Trigger Phrases

- "debug this" / "디버그해줘"
- "find the root cause" / "원인 찾아줘"
- "why is this failing" / "왜 실패하는지"
- "investigate this error" / "이 에러 분석해줘"
- "ultrathink debug" / "심층 디버깅"

## Integration

Works with existing skills:
- @skill root-cause-tracing for detailed call chain analysis
- @skill defense-in-depth for validation layer recommendations
- @skill systematic-debugging for structured investigation
- @skill verification-before-completion for fix confirmation
