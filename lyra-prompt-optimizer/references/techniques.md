# Optimization Techniques Reference

Detailed techniques for prompt optimization.

## Foundation Techniques

### 1. Role Assignment

Assign a specific expert role to prime the AI:

```markdown
You are a [expertise level] [role] with deep experience in [domain].
Your approach emphasizes [key qualities].
```

**Examples:**

- "You are a senior software architect with 15 years of experience in distributed systems."
- "You are a professional copywriter specializing in conversion-focused marketing."

### 2. Context Layering

Structure context from broad to specific:

```markdown
# Background

[Industry/domain context]

# Specific Situation

[Current task context]

# Requirements

[Specific needs and constraints]
```

### 3. Output Specification

Define expected output format clearly:

```markdown
Provide your response in the following format:

- Format: [markdown/JSON/plain text]
- Length: [word count or section count]
- Structure: [headers/bullets/numbered list]
- Tone: [formal/casual/technical]
```

### 4. Task Decomposition

Break complex tasks into steps:

```markdown
Complete this task in stages:

1. [Analysis stage]
2. [Planning stage]
3. [Execution stage]
4. [Review stage]
```

## Advanced Techniques

### 5. Chain-of-Thought (CoT)

Guide reasoning through explicit steps:

```markdown
Think through this step-by-step:

1. First, analyze [aspect 1]
2. Then, consider [aspect 2]
3. Evaluate the relationship between [1] and [2]
4. Based on this analysis, conclude...

Show your reasoning before providing the final answer.
```

**When to use:**

- Mathematical or logical problems
- Complex analysis requiring multiple considerations
- Decision-making with trade-offs

### 6. Few-Shot Learning

Provide examples to guide output:

```markdown
Here are examples of the format I need:

Example 1:
Input: [sample input]
Output: [sample output]

Example 2:
Input: [sample input]
Output: [sample output]

Now apply this pattern to:
Input: [actual input]
```

**Best practices:**

- Use 2-3 representative examples
- Show edge cases if relevant
- Keep examples consistent in format

### 7. Multi-Perspective Analysis

Request multiple viewpoints:

```markdown
Analyze this from multiple perspectives:

- Technical feasibility
- Business impact
- User experience
- Risk assessment

For each perspective, provide:

- Key considerations
- Potential issues
- Recommendations
```

### 8. Constraint Optimization

Define boundaries explicitly:

```markdown
Constraints:

- MUST: [required elements]
- MUST NOT: [prohibited elements]
- SHOULD: [preferred but optional]
- AVOID: [discouraged approaches]
```

## Request-Type Optimization

### Creative Requests

```markdown
# Role

You are a creative [role] known for [distinctive quality].

# Style Guidelines

- Tone: [specific tone]
- Voice: [active/passive, first/third person]
- Emotion: [emotional quality to evoke]

# Creative Direction

[Specific creative constraints or freedoms]

# Output

[Format and length expectations]
```

### Technical Requests

```markdown
# Technical Context

- Technology stack: [relevant technologies]
- Constraints: [performance, compatibility requirements]
- Standards: [coding standards, best practices to follow]

# Task

[Precise technical requirement]

# Expected Output

- Format: [code, documentation, diagram]
- Include: [tests, error handling, comments]
- Exclude: [deprecated approaches, specific patterns]
```

### Educational Requests

```markdown
# Learner Context

- Current level: [beginner/intermediate/advanced]
- Background: [relevant prior knowledge]
- Goal: [what they want to learn]

# Teaching Approach

- Start with: [foundational concept]
- Build to: [target understanding]
- Use: [examples, analogies, exercises]

# Format

- Structure: [progressive complexity]
- Include: [practice exercises, knowledge checks]
```

### Analytical Requests

```markdown
# Analysis Framework

- Scope: [what to analyze]
- Depth: [surface/moderate/deep]
- Focus areas: [specific aspects]

# Data/Evidence Requirements

- Sources: [what data to consider]
- Validation: [how to verify claims]

# Output Structure

- Summary: [key findings]
- Details: [supporting analysis]
- Recommendations: [actionable insights]
```

## Validation Techniques

### Self-Consistency Check

After generating output, verify:

```markdown
Review your response and confirm:

1. Does it fully address the original request?
2. Are there any logical inconsistencies?
3. Is the format as specified?
4. Are all constraints satisfied?
```

### Iterative Refinement

```markdown
After your initial response:

1. Identify the weakest part
2. Explain why it's weak
3. Provide an improved version
```
