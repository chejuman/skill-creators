---
name: brand-system-architect
description: Premium hierarchical multi-agent brand system generator deploying 10 parallel domain experts for comprehensive brand specification. Generates W3C Design Tokens, CSS variables, AI image generation prompts, voice/tone guidelines, and motion specifications. Use when creating brand systems, design tokens, brand guidelines, style guides, or when user mentions "brand system", "design tokens", "brand specification", "brand guidelines", "brand identity", "design system".
---

# Brand System Architect

Premium multi-agent brand system generator using hierarchical orchestration with 10 parallel domain experts.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COORDINATOR (Sonnet)                             │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 1: DISCOVER ──► WebSearch + AskUserQuestion                   │
│ Phase 2: RESEARCH ──► 3 parallel Haiku research agents             │
│ Phase 3: GENERATE ──► 10 parallel domain experts (Hybrid)          │
│ Phase 4: SYNTHESIZE ──► Merge into unified specification           │
│ Phase 5: OUTPUT ──► W3C Tokens + CSS + AI prompts                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase 1: Discovery

Gather brand context via AskUserQuestion:

```
AskUserQuestion(questions=[
  {"question": "What is the brand name and industry?", "header": "Brand", ...},
  {"question": "Describe the brand personality (3-5 adjectives)?", "header": "Personality", ...},
  {"question": "Who is the target audience?", "header": "Audience", ...},
  {"question": "Any existing brand assets (logos, colors)?", "header": "Assets", ...}
])
```

Then conduct trend research:

```
WebSearch("brand design trends 2025 {industry}")
WebSearch("color psychology {industry} brand")
WebSearch("typography trends {brand_personality}")
```

## Phase 2: Research (3 Parallel Haiku Agents)

Launch parallel research agents:

```
# Agent 1: Competitive Analysis
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Research competitor brand systems in {industry}. Find: color palettes, typography, voice patterns.')

# Agent 2: Industry Standards
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Research {industry} design standards and accessibility requirements.')

# Agent 3: AI Integration Patterns
Task(subagent_type='Explore', model='haiku', run_in_background=true,
  prompt='Research AI image generation brand guidelines and voice/tone frameworks.')
```

## Phase 3: Generation (10 Parallel Domain Experts)

Deploy 10 domain experts in parallel. See [references/agent_prompts.md](references/agent_prompts.md) for full prompts.

| Agent | Domain               | Model  | Output            |
| ----- | -------------------- | ------ | ----------------- |
| 1     | Brand Strategy       | Sonnet | `strategy.json`   |
| 2     | Color Systems        | Haiku  | `colors.json`     |
| 3     | Typography           | Haiku  | `typography.json` |
| 4     | Motion & Animation   | Haiku  | `motion.json`     |
| 5     | Voice & Tone         | Sonnet | `voice.json`      |
| 6     | Visual Imagery       | Sonnet | `imagery.json`    |
| 7     | Component Patterns   | Haiku  | `components.json` |
| 8     | Layout & Composition | Haiku  | `layout.json`     |
| 9     | Video & Multimedia   | Haiku  | `multimedia.json` |
| 10    | Marketing & Campaign | Haiku  | `marketing.json`  |

**Execution pattern:**

```python
# Launch all 10 agents in parallel
for domain in DOMAINS:
    Task(
        subagent_type='general-purpose',
        model=domain.model,  # Sonnet for strategy, Haiku for execution
        run_in_background=True,
        prompt=f'''Generate {domain.name} specification for brand: {brand_context}
        Output JSON schema: {domain.schema}
        Research findings: {research_results}'''
    )

# Collect results
results = [TaskOutput(task_id=id, block=True) for id in task_ids]
```

## Phase 4: Synthesis

Merge all domain outputs into unified brand specification:

1. Validate cross-domain consistency (colors referenced in components match)
2. Resolve conflicts (e.g., motion timing vs accessibility requirements)
3. Generate design token hierarchy with semantic naming
4. Create CSS custom properties from tokens

## Phase 5: Output Generation

Generate multi-format output using [scripts/generate_tokens.py](scripts/generate_tokens.py):

### W3C Design Tokens (Primary)

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "color": {
    "brand": {
      "primary": { "$value": "#0066CC", "$type": "color" }
    }
  }
}
```

### CSS Variables

```css
:root {
  --color-brand-primary: #0066cc;
  --font-family-heading: "Inter", sans-serif;
  --motion-duration-fast: 150ms;
}
```

### AI Image Generation Prompts

```json
{
  "midjourney": {
    "style_reference": "--sref {url} --sw 100",
    "parameters": "--ar 16:9 --stylize 250 --v 6.1"
  },
  "stable_diffusion": {
    "positive": "brand aesthetic, {style_keywords}, professional",
    "negative": "off-brand, unprofessional, cluttered"
  }
}
```

## Output Files

The skill generates `.brand-system/` directory:

```
.brand-system/
├── brand-spec.json          # Complete unified specification
├── tokens/
│   ├── w3c-tokens.json      # W3C Design Tokens format
│   ├── variables.css        # CSS custom properties
│   └── tailwind.config.js   # Tailwind theme config
├── guidelines/
│   ├── voice-tone.md        # Voice & tone guide
│   ├── imagery.md           # Visual imagery guide
│   └── motion.md            # Animation specifications
└── ai-prompts/
    ├── image-generation.json # Midjourney/SD/DALL-E prompts
    └── voice-parameters.json # AI voice/chatbot guidelines
```

## Domain Specifications

Detailed schemas in [references/output_schemas.md](references/output_schemas.md).

### Quick Reference

**Color System:** Palette science, WCAG contrast ratios, semantic color tokens
**Typography:** Type scale (1.25 ratio), font pairing, responsive sizing
**Motion:** Easing curves (cubic-bezier), duration scale, micro-interactions
**Voice:** Personality traits, tone matrix, context adaptation rules
**Imagery:** Photography style, illustration guidelines, AI generation params

## AI/LLM Integration

See [references/ai_integration.md](references/ai_integration.md) for:

- Image generation prompt templates (Midjourney, Stable Diffusion, DALL-E)
- Chatbot personality configuration
- Voice synthesis parameters
- Semantic token naming for AI consumption

## Trigger Phrases

- "brand system", "design system", "brand specification"
- "design tokens", "create brand guidelines", "brand identity"
- "generate style guide", "brand architecture"
- "W3C tokens", "CSS variables from brand"
