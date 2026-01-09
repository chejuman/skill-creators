# Resumable Agents Guide

Guide to using resumable agents in Workflow Creator V3 for iterative workflow development.

## Overview

All research and generation agents in Workflow Creator V3 return an `agentId` that can be used to resume their work. This enables:

- **Iterative development**: Continue workflow generation with new requirements
- **Incremental refinement**: Add features without starting from scratch
- **Context preservation**: Agent remembers all previous context
- **Cost efficiency**: Don't re-execute completed work

## How Resumable Agents Work

### Initial Execution

```python
# Launch agent
result = Task(
  subagent_type='general-purpose',
  prompt='Create a CI/CD workflow for AWS ECS deployment...',
  description='Generate DevOps workflow',
  model='sonnet'
)

# Agent ID is returned
agent_id = 'b7e9a12'  # Unique identifier
```

### Resumption

```python
# Continue previous agent's work
result = Task(
  resume='b7e9a12',  # Resume with full context
  prompt='Add container scanning with Trivy and secrets management'
)
```

### Context Preservation

When resumed, the agent has:

- Full conversation history
- All previous tool calls and results
- Generated files and state
- Research findings
- Requirements gathered

## Use Cases in Workflow Creator V3

### 1. Iterative Research (Phase 4)

**Scenario**: Initial research insufficient, need deeper domain knowledge

```python
# Initial research
research_agent = Task(
  subagent_type='Explore',
  prompt='Research DevOps CI/CD best practices 2025...',
  description='Research best practices',
  model='haiku',
  run_in_background=True
)

research_agent_id = research_agent.id  # Store ID

# ... User reviews findings, wants more specific info ...

# Resume research
Task(
  resume=research_agent_id,
  prompt='Dive deeper into blue-green deployment patterns for ECS. Find code examples and GitHub repos with >1K stars.'
)
```

**Benefit**: Reuses previous research context, doesn't re-search basics.

### 2. Incremental Generation (Phase 7)

**Scenario**: Add features to generated workflow without regenerating everything

```python
# Initial generation
generation_agent = Task(
  subagent_type='general-purpose',
  prompt='Generate CI/CD workflow with basic deployment...',
  description='Generate DevOps workflow',
  model='sonnet'
)

generation_agent_id = generation_agent.id

# Generated: SKILL.md, scripts/deploy.sh

# ... User wants to add monitoring ...

# Resume generation
Task(
  resume=generation_agent_id,
  prompt='Add monitoring integration: CloudWatch metrics, alarms for failed deployments, and Slack notifications'
)

# Agent updates existing workflow, adds new scripts/monitor.sh
```

**Benefit**: Preserves existing files, only adds/modifies necessary parts.

### 3. Error Recovery

**Scenario**: Generation failed midway, resume to complete

```python
# Generation encountered error (network timeout, etc.)
generation_agent_id = 'c3d8f21'

# Resume from checkpoint
Task(
  resume=generation_agent_id,
  prompt='Continue generation. Complete the remaining scripts and references.'
)
```

**Benefit**: No need to regenerate completed components.

### 4. User Feedback Integration

**Scenario**: User reviews generated workflow, requests changes

```python
# Generated workflow
generation_agent_id = 'd9a4b32'

# User feedback
Task(
  resume=generation_agent_id,
  prompt='''Based on user feedback:
  1. Change deployment from ECS to Lambda
  2. Add SAM template for infrastructure
  3. Update tests to use pytest instead of unittest
  '''
)
```

**Benefit**: Agent understands existing structure, makes targeted changes.

## Best Practices

### 1. Store Agent IDs

Always store agent IDs for potential resumption:

```python
class WorkflowOrchestrator:
    def __init__(self):
        self.agent_ids = {
            'research': [],
            'generation': None,
            'validation': None
        }

    def launch_research_agents(self):
        for i in range(4):
            agent = Task(...)
            self.agent_ids['research'].append(agent.id)

    def resume_research(self, agent_index: int, new_prompt: str):
        Task(resume=self.agent_ids['research'][agent_index], prompt=new_prompt)
```

### 2. Provide Clear Resume Prompts

When resuming, be explicit about what to continue:

**Bad**:

```python
Task(resume='b7e9a12', prompt='Continue')  # Too vague
```

**Good**:

```python
Task(
  resume='b7e9a12',
  prompt='Continue generation. Add these specific components: [list]. Maintain existing file structure.'
)
```

### 3. Resume vs. New Agent

**Resume when**:

- Building on previous work
- Adding incremental features
- Fixing errors in generated output
- User provides feedback on specific aspect

**New agent when**:

- Completely different task
- Starting fresh workflow
- Context from previous agent irrelevant

### 4. Track Agent State

Maintain metadata about what each agent has done:

```python
agent_metadata = {
    'b7e9a12': {
        'type': 'generation',
        'domain': 'DevOps',
        'status': 'completed',
        'files_generated': ['SKILL.md', 'scripts/deploy.sh'],
        'can_resume': True
    }
}
```

## Integration with Workflow Creator V3 Phases

### Phase 4: Parallel Research Agents (All Resumable)

```python
# Launch 4 parallel research agents
agent_ids = {}

agent_ids['best_practices'] = Task(
  subagent_type='Explore',
  prompt='Research DevOps best practices...',
  model='haiku',
  run_in_background=True
).id

agent_ids['tools'] = Task(
  subagent_type='Explore',
  prompt='Discover DevOps automation tools...',
  model='haiku',
  run_in_background=True
).id

agent_ids['existing'] = Task(
  subagent_type='Explore',
  prompt='Research existing Claude Code DevOps skills...',
  model='haiku',
  run_in_background=True
).id

agent_ids['web_research'] = Task(
  subagent_type='general-purpose',
  prompt='Web research for DevOps workflows...',
  model='sonnet',
  run_in_background=True
).id

# Wait for completion...

# If user wants more specific research on any topic:
Task(resume=agent_ids['tools'], prompt='Find MCP servers for CI/CD integration')
```

### Phase 7: Generation Agent (Resumable)

```python
# Initial generation
generation_result = Task(
  subagent_type='general-purpose',
  prompt=refined_generation_prompt,
  description='Generate workflow',
  model='sonnet'
)

generation_agent_id = generation_result.id

# Store in report
report = f'''
## Agent IDs for Resumption

- Generation Agent: {generation_agent_id}
  Use: `Task(resume='{generation_agent_id}', prompt='your changes')`

### Example Resumption Commands:

# Add hooks
Task(resume='{generation_agent_id}', prompt='Add PreToolUse and PostToolUse hooks for validation')

# Add MCP integration
Task(resume='{generation_agent_id}', prompt='Add .mcp.json with github and postgres MCP servers')

# Expand scripts
Task(resume='{generation_agent_id}', prompt='Add error handling and retry logic to all scripts')
'''
```

## Example Workflows

### Example 1: Iterative DevOps Workflow Development

```
User: Create a CI/CD workflow for AWS ECS deployment

Phase 7: Generate initial workflow
  Agent ID: b7e9a12
  Generated: SKILL.md, scripts/deploy.sh, scripts/test.sh

User: Add container scanning

Resume b7e9a12: Add Trivy container scanning
  Updated: scripts/deploy.sh (added scan step)
  Generated: scripts/scan.sh

User: Add monitoring and alerts

Resume b7e9a12: Add CloudWatch monitoring
  Generated: scripts/monitor.sh, scripts/alert.sh
  Updated: SKILL.md (added monitoring section)

User: Change deployment to blue-green

Resume b7e9a12: Change to blue-green deployment strategy
  Updated: scripts/deploy.sh (blue-green logic)
  Updated: references/deployment_guide.md

Final Result: Complete workflow with all requested features
```

### Example 2: Research Deep Dive

```
Phase 4: Initial research

  Best Practices Agent (ID: a1b2c3d)
    Found: 10 general DevOps patterns

  Tools Agent (ID: e4f5g6h)
    Found: 15 tools (GitHub Actions, GitLab CI, etc.)

User: I want to focus on AWS-specific tools

Resume e4f5g6h: Deep dive into AWS CodePipeline, CodeBuild, CodeDeploy
  Found: 8 AWS-native tools with examples

Resume a1b2c3d: Find AWS Well-Architected best practices for CI/CD
  Found: 12 AWS-specific patterns

Phase 7: Generation uses refined research
  Result: AWS-optimized workflow
```

## Performance Considerations

### Resume Overhead

- Minimal: Agent loads previous context (~1-2s)
- No re-execution of previous tool calls
- Efficient for incremental work

### When Not to Resume

- Agent context exceeds token limit (rare, ~150K tokens)
- Too many iterations (>5-10 resumes, start fresh)
- Completely different direction (new agent faster)

## Troubleshooting

| Issue                           | Solution                                              |
| ------------------------------- | ----------------------------------------------------- |
| Agent ID not found              | Verify ID is correct, agent may have expired (24h)    |
| Resume doesn't remember context | Check if agent completed successfully before resuming |
| Resume creates duplicate work   | Be explicit in prompt about updating vs. creating new |
| Too many iterations             | Consider starting fresh if >10 resumes                |

## References

- Claude Code Guide: Resumable Subagents
- Task tool documentation
- Phase 4 and Phase 7 in SKILL.md
