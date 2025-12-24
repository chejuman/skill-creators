---
name: coding-tutor-v2
description: Multi-agent personalized coding tutor with codebase analysis, real-time web research, and adaptive curriculum. Use when learning programming concepts, understanding codebases, or requesting personalized tutorials. Triggers on "teach me", "explain this code", "create curriculum", "coding tutor", or learning-related requests.
---

# Coding Tutor V2

Multi-agent architecture for personalized coding education focused on understanding YOUR codebase.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                             │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: User Profiling ──► AskUserQuestion               │
│  Phase 2: Codebase Analysis ──► Parallel Agents            │
│  Phase 3: Web Research ──► Tech Stack Documentation        │
│  Phase 4: Curriculum Design ──► Personalized Plan          │
│  Phase 5: Tutorial Generation ──► Interactive Learning     │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: User Profiling

**First-time users**: Conduct onboarding interview using AskUserQuestion:

```
AskUserQuestion(questions=[
  {
    "question": "What is your current programming experience level?",
    "header": "Level",
    "options": [
      {"label": "Beginner", "description": "New to programming, need foundational concepts"},
      {"label": "Intermediate", "description": "Know basics, want to deepen understanding"},
      {"label": "Advanced", "description": "Experienced, want specific patterns/architecture"}
    ],
    "multiSelect": false
  },
  {
    "question": "What tech stacks are you interested in learning?",
    "header": "Tech Stack",
    "options": [
      {"label": "Web (React, Next.js, Node)", "description": "Frontend/Backend web development"},
      {"label": "Backend (Python, Go, DB)", "description": "Server, API, database, infrastructure"},
      {"label": "Mobile (Flutter, React Native)", "description": "Cross-platform mobile apps"},
      {"label": "AI/ML (Python, PyTorch, LLM)", "description": "Machine learning, AI agents"}
    ],
    "multiSelect": true
  },
  {
    "question": "What is your preferred learning style?",
    "header": "Style",
    "options": [
      {"label": "Socratic (Recommended)", "description": "Guided questions to discover answers yourself"},
      {"label": "Step-by-step", "description": "Detailed explanations of each concept"},
      {"label": "Hands-on", "description": "Learn by writing code immediately"}
    ],
    "multiSelect": false
  },
  {
    "question": "What is your primary learning goal?",
    "header": "Goal",
    "options": [
      {"label": "Understand this codebase", "description": "Deep dive into current project"},
      {"label": "Learn new technology", "description": "Master a new framework/language"},
      {"label": "Improve coding skills", "description": "Better patterns, architecture, practices"}
    ],
    "multiSelect": false
  }
])
```

Save profile to `~/coding-tutor-tutorials/learner_profile.md`:

```yaml
---
created: DD-MM-YYYY
last_updated: DD-MM-YYYY
level: beginner|intermediate|advanced
tech_stacks: [web, backend, mobile, ai-ml]
learning_style: socratic|step-by-step|hands-on
primary_goal: understand-codebase|learn-tech|improve-skills
---
## Interview Summary
[User responses and your analysis]
```

**Returning users**: Read existing profile and adapt accordingly.

## Phase 2: Codebase Analysis (Parallel Agents)

Spawn multiple Explore agents to analyze the current codebase:

```
# Launch 4-5 parallel agents for comprehensive analysis
Task(
  subagent_type='Explore',
  prompt='Analyze languages and frameworks used in this codebase. List: primary language, framework versions, package.json/requirements.txt dependencies.',
  description='Analyze languages and frameworks',
  model='haiku',
  run_in_background=true
)

Task(
  subagent_type='Explore',
  prompt='Identify architectural patterns: MVC, Clean Architecture, microservices, monolith. Find: folder structure, layer separation, dependency injection.',
  description='Identify architecture patterns',
  model='haiku',
  run_in_background=true
)

Task(
  subagent_type='Explore',
  prompt='Find key libraries and their usage: state management, routing, API calls, testing, styling. Include version and usage patterns.',
  description='Catalog key libraries',
  model='haiku',
  run_in_background=true
)

Task(
  subagent_type='Explore',
  prompt='Discover coding patterns: error handling, async patterns, type usage, naming conventions. Find examples in code.',
  description='Discover coding patterns',
  model='haiku',
  run_in_background=true
)

Task(
  subagent_type='Explore',
  prompt='Map data flow: API endpoints, database models, state management, component hierarchy. Create overview.',
  description='Map data flow',
  model='haiku',
  run_in_background=true
)
```

Collect results and create `codebase_analysis.md`:

```yaml
---
repo_name: project-name
analyzed_at: DD-MM-YYYY
---

## Tech Stack
- **Primary Language**: TypeScript 5.x
- **Framework**: Next.js 14 (App Router)
- **Key Dependencies**: React Query, Zustand, Tailwind CSS

## Architecture
- Pattern: Feature-based folder structure
- State: Zustand for global, React Query for server

## Key Patterns
- Error handling: try/catch with toast notifications
- API: REST with axios, type-safe responses
- Styling: Tailwind + shadcn/ui components

## Learning Opportunities
1. [High Priority] Understanding App Router patterns
2. [Medium] Zustand state management
3. [Medium] React Query caching strategies
```

## Phase 3: Web Research (Tech Stack Documentation)

Based on identified tech stack, search for latest documentation:

```
WebSearch(query='{framework} best practices {current_year}')
WebSearch(query='{library} tutorial advanced patterns {current_year}')
WebSearch(query='{architecture_pattern} implementation guide')
```

**Important**:

- Use current year (2025) in queries
- Include Sources section with markdown links
- Focus on official docs and reputable tutorials

Save findings to `research_notes.md` for curriculum reference.

## Phase 4: Curriculum Design

Create personalized learning path based on:

1. User profile (level, style, goal)
2. Codebase analysis (what's actually used)
3. Web research (latest best practices)

**Curriculum structure**:

```yaml
---
learner: username
created: DD-MM-YYYY
focus: codebase-understanding
estimated_tutorials: 10
---

## Learning Path

### Foundation (Tutorials 1-3)
1. **Project Overview**: Architecture and folder structure
2. **Core Framework**: {framework} fundamentals in this codebase
3. **Data Flow**: How data moves through the application

### Intermediate (Tutorials 4-6)
4. **State Management**: {state_lib} patterns used here
5. **API Integration**: How backend calls are handled
6. **Component Patterns**: Reusable component architecture

### Advanced (Tutorials 7-10)
7. **Performance Optimization**: Caching and rendering
8. **Testing Strategy**: Test patterns in this codebase
9. **Error Handling**: Robust error management
10. **Deployment & DevOps**: Build and deploy pipeline
```

Present curriculum to user with AskUserQuestion for approval:

```
AskUserQuestion(questions=[{
  "question": "Does this curriculum match your learning goals?",
  "header": "Approval",
  "options": [
    {"label": "Approve", "description": "Start learning with this curriculum"},
    {"label": "Modify focus", "description": "Adjust priorities or topics"},
    {"label": "Regenerate", "description": "Create new curriculum with different focus"}
  ],
  "multiSelect": false
}])
```

## Phase 5: Tutorial Generation

Create tutorials using THIS codebase as the primary teaching material.

### Tutorial Structure

````markdown
---
concepts: [primary_concept, related_1, related_2]
source_repo: project-name
description: One paragraph summary
understanding_score: null
last_quizzed: null
prerequisites: [previous_tutorial.md]
created: DD-MM-YYYY
last_updated: DD-MM-YYYY
---

# Tutorial Title

## Why This Matters

[Connect to learner's goal and real problem in codebase]

## The Problem in Your Code

[Show actual code example from THIS repository]

## Key Concepts

[Build mental models with diagrams and analogies]

## Examples from Your Codebase

### Example 1: [location]

```code
// Actual code from repo
```
````

**What this demonstrates:** [Explanation]

## Socratic Exploration

[Guide questions for self-discovery - adjust based on learning style]

## Try It Yourself

[Exercise using this codebase]

---

## Q&A

[Learner questions appended here]

## Quiz History

[Quiz sessions recorded here]

````

### Teaching Style Adaptation

**Socratic Style**:
- Ask guiding questions before explaining
- "What do you think happens when...?"
- "Can you find where this pattern is used?"

**Step-by-step Style**:
- Detailed explanations with each concept
- Clear progression from simple to complex
- Check understanding at each step

**Hands-on Style**:
- Start with code exercise
- Explain concepts through doing
- Immediate practical application

## Quiz Mode (Spaced Repetition)

Run quiz priority script:
```bash
python3 ${SKILL_PATH}/scripts/quiz_priority.py
````

**Fibonacci-based intervals**:
| Score | Review Interval |
|-------|-----------------|
| 1-2 | 2-3 days |
| 3-4 | 5-8 days |
| 5-6 | 13-21 days |
| 7-8 | 34-55 days |
| 9-10 | 89-144 days |

**Quiz question types** (use codebase examples):

- Conceptual: "When would you use X over Y?"
- Code reading: "What does this function in your app do?"
- Debugging: "What's wrong with this pattern?"
- Application: "How would you add feature X?"

## Commands

- `/teach-me` - Start learning (runs full workflow)
- `/teach-me [topic]` - Learn specific topic
- `/quiz-me` - Spaced repetition quiz
- `/analyze-codebase` - Run codebase analysis only
- `/my-curriculum` - View/update learning path
- `/sync-tutorials` - Backup to GitHub

## Storage

All data stored in `~/coding-tutor-tutorials/`:

- `learner_profile.md` - User profile
- `codebase_analysis.md` - Analysis results
- `curriculum.md` - Learning path
- `YYYY-MM-DD-topic.md` - Individual tutorials

## Best Practices

1. **Always use codebase examples** - Abstract examples are forgettable
2. **Adapt to learning style** - Socratic/step-by-step/hands-on
3. **Build on previous tutorials** - Reference prerequisites
4. **Update Q&A section** - Every question becomes part of record
5. **Honest quiz scoring** - Reflects actual retention
6. **Web research for accuracy** - Verify before teaching
