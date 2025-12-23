# Agent Prompts

Conductor 멀티에이전트 시스템에서 사용하는 에이전트 프롬프트 템플릿.

## Explore Agent - Codebase Analyzer

```
Analyze the codebase structure for implementing: {description}

Focus on:
1. Existing patterns and conventions
2. Related files and modules
3. Potential integration points
4. Technical constraints

Output:
- File list with relevance
- Architecture summary
- Recommended approach
```

## Plan Agent - Strategy Designer

```
Design implementation strategy for: {description}

Given context:
- Tech stack: {tech_stack}
- Workflow: {workflow_preferences}
- Existing patterns: {patterns_found}

Create:
1. Phased implementation plan
2. Task breakdown with dependencies
3. Risk assessment
4. Effort estimation
```

## Implementation Agent - Frontend

```
Implement frontend components for: {task_description}

Constraints:
- Follow existing UI patterns
- Use established component library
- Maintain accessibility standards
- Write corresponding tests

Context:
{relevant_code_snippets}
```

## Implementation Agent - Backend

```
Implement backend logic for: {task_description}

Constraints:
- Follow existing API patterns
- Maintain database conventions
- Include error handling
- Write unit tests

Context:
{relevant_code_snippets}
```

## Implementation Agent - Test Writer

```
Write tests for: {implementation_description}

Test types:
- Unit tests for business logic
- Integration tests for APIs
- E2E tests for user flows

Coverage targets:
- Critical paths: 100%
- Edge cases: Comprehensive
- Error scenarios: All handled
```

## Review Agent - Code Reviewer

```
Review the implementation of: {track_description}

Check for:
1. Code quality and patterns
2. Test coverage
3. Security considerations
4. Performance implications
5. Documentation completeness

Provide:
- Approval/rejection decision
- Specific feedback items
- Suggested improvements
```

## Synthesis Agent - Documentation

```
Generate documentation for: {feature_description}

Include:
1. Feature overview
2. API documentation (if applicable)
3. Usage examples
4. Configuration options
5. Troubleshooting guide

Format: Markdown
Audience: Developers
```

## Parallel Execution Template

병렬 에이전트 실행 시 사용:

```python
# 3개의 병렬 Explore 에이전트
Task(
    subagent_type='Explore',
    prompt='Analyze frontend patterns for {description}',
    model='haiku',
    description='Frontend analysis',
    run_in_background=True
)
Task(
    subagent_type='Explore',
    prompt='Analyze backend patterns for {description}',
    model='haiku',
    description='Backend analysis',
    run_in_background=True
)
Task(
    subagent_type='Explore',
    prompt='Analyze test patterns for {description}',
    model='haiku',
    description='Test analysis',
    run_in_background=True
)
```

## Context Loading Pattern

에이전트에 컨텍스트 제공:

```markdown
## Project Context
Read from: .claude/conductor/product.md
Tech stack: .claude/conductor/tech-stack.md
Workflow: .claude/conductor/workflow.md

## Track Context
Spec: .claude/conductor/tracks/{track_id}/spec.md
Plan: .claude/conductor/tracks/{track_id}/plan.md

## Codebase Context
{relevant_files_from_explore}
```
