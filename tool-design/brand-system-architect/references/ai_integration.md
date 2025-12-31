# AI/LLM Integration Guide

Specifications for integrating brand system with AI tools.

## Image Generation Prompts

### Midjourney Configuration

```json
{
  "midjourney": {
    "version": "6.1",
    "base_structure": "{subject}, {style_keywords}, {lighting}, {color_mood} --ar {ratio} --stylize {value} --v 6.1",
    "parameters": {
      "--ar": "Aspect ratio (16:9, 9:16, 1:1, 4:3)",
      "--stylize": "0-1000, higher = more Midjourney aesthetic",
      "--chaos": "0-100, variation between outputs",
      "--no": "Negative prompts (text, blur, watermark)",
      "--sref": "Style reference URL for consistency",
      "--sw": "Style weight 0-1000 (default 100)",
      "--cref": "Character reference for consistency"
    },
    "brand_template": {
      "product_shot": "{product}, {brand_style}, professional studio lighting, minimalist --ar 4:3 --stylize 150",
      "lifestyle": "{scene}, {brand_aesthetic}, natural lighting, authentic --ar 16:9 --stylize 200",
      "abstract": "{concept}, {brand_colors}, geometric, modern --ar 1:1 --stylize 300"
    }
  }
}
```

### Stable Diffusion Configuration

```json
{
  "stable_diffusion": {
    "model": "SDXL 1.0 / SD 3.5",
    "prompt_structure": "{quality}, {subject}, {style}, {lighting}, {details}",
    "parameters": {
      "cfg_scale": "7-12 (higher = stricter prompt adherence)",
      "steps": "20-50 (higher = more refined)",
      "sampler": "DPM++ 2M Karras (recommended)",
      "scheduler": "Karras"
    },
    "brand_template": {
      "positive": "masterpiece, best quality, {brand_style}, {subject}, professional, {brand_colors}, sharp focus",
      "negative": "low quality, blurry, text, watermark, signature, off-brand, amateur, oversaturated"
    },
    "lora_recommendations": {
      "product": "Product photography LoRA",
      "portrait": "Professional portrait LoRA"
    }
  }
}
```

### DALL-E 3 Configuration

```json
{
  "dall_e": {
    "style_presets": ["vivid", "natural"],
    "quality": ["standard", "hd"],
    "size_options": ["1024x1024", "1792x1024", "1024x1792"],
    "brand_template": {
      "structure": "{detailed_description} in a {brand_style} aesthetic with {brand_colors}",
      "tips": [
        "Be extremely specific about style",
        "Describe colors explicitly with hex or names",
        "Include composition instructions",
        "Specify lighting and mood"
      ]
    }
  }
}
```

## AI Chatbot Voice Configuration

### System Prompt Template

```markdown
You are {brand_name}'s AI assistant. Embody these characteristics:

**Voice Attributes:**
{voice_attributes_list}

**Tone Guidelines:**

- Formality: {formality_scale}/10 (0=casual, 10=formal)
- Enthusiasm: {enthusiasm_scale}/10
- Humor: {humor_scale}/10

**Vocabulary:**

- USE: {preferred_words}
- AVOID: {avoided_words}

**Response Style:**

- Keep responses {concise/detailed}
- Use {sentence_structure}
- {additional_guidelines}

Remember: You represent {brand_name}. Stay consistent with these guidelines.
```

### Temperature & Parameter Mapping

| Brand Personality      | Temperature | Top-P | Frequency Penalty |
| ---------------------- | ----------- | ----- | ----------------- |
| Professional/Corporate | 0.3-0.5     | 0.8   | 0.3               |
| Friendly/Approachable  | 0.6-0.7     | 0.9   | 0.2               |
| Creative/Playful       | 0.7-0.9     | 0.95  | 0.1               |
| Technical/Precise      | 0.2-0.4     | 0.7   | 0.4               |

### Context Adaptation Rules

```json
{
  "context_adaptation": {
    "support_inquiry": {
      "tone_shift": "more_empathetic",
      "temperature_delta": -0.1,
      "priority": "clarity_and_helpfulness"
    },
    "sales_inquiry": {
      "tone_shift": "more_enthusiastic",
      "temperature_delta": 0,
      "priority": "value_communication"
    },
    "complaint": {
      "tone_shift": "apologetic_and_solution_focused",
      "temperature_delta": -0.2,
      "priority": "resolution"
    },
    "casual_chat": {
      "tone_shift": "relaxed",
      "temperature_delta": +0.1,
      "priority": "engagement"
    }
  }
}
```

## Voice Synthesis Parameters

### Text-to-Speech Configuration

```json
{
  "tts_config": {
    "voice_characteristics": {
      "gender": "string",
      "age_range": "string",
      "accent": "string",
      "pitch": "low/medium/high",
      "speed": "0.8-1.2 (1.0 = normal)",
      "warmth": "0-1 scale"
    },
    "prosody": {
      "emphasis_words": ["brand_name", "key_features"],
      "pause_after": ["period", "comma"],
      "pause_duration_ms": { "short": 200, "medium": 400, "long": 600 }
    },
    "platform_presets": {
      "eleven_labs": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.3
      },
      "azure_tts": {
        "style": "friendly|professional|empathetic",
        "style_degree": "0.5-2.0"
      }
    }
  }
}
```

## Semantic Token Naming

Design tokens optimized for AI consumption:

### Naming Convention

```
{category}-{property}-{variant}-{state}

Examples:
color-brand-primary-default
color-text-body-muted
font-size-heading-lg
motion-duration-fast
spacing-component-padding-md
```

### AI-Readable Token Structure

```json
{
  "$metadata": {
    "ai_consumable": true,
    "semantic_level": "application",
    "usage_hints": true
  },
  "tokens": {
    "color-brand-primary": {
      "$value": "#0066CC",
      "$type": "color",
      "$description": "Primary brand color for CTAs, links, and brand emphasis",
      "$usage": ["buttons", "links", "icons", "brand-elements"],
      "$contrast_with": ["color-background-default"],
      "$accessibility": { "wcag_aa": true, "wcag_aaa": false }
    }
  }
}
```

### Token Relationships for AI

```json
{
  "$relationships": {
    "color-brand-primary": {
      "pairs_with": ["color-text-on-primary", "color-background-default"],
      "derived_from": null,
      "derives": ["color-brand-primary-hover", "color-brand-primary-active"]
    },
    "font-size-base": {
      "scale_factor": 1.25,
      "derives": ["font-size-lg", "font-size-xl", "font-size-2xl"]
    }
  }
}
```

## Multi-Modal Brand Consistency

### Cross-Platform Token Mapping

```json
{
  "platform_mapping": {
    "web": {
      "format": "CSS custom properties",
      "file": "variables.css",
      "prefix": "--"
    },
    "ios": {
      "format": "Swift constants",
      "file": "BrandTokens.swift",
      "prefix": "Brand."
    },
    "android": {
      "format": "XML resources",
      "file": "brand_tokens.xml",
      "prefix": "@color/, @dimen/"
    },
    "figma": {
      "format": "Figma variables",
      "collection": "Brand System"
    },
    "ai_tools": {
      "format": "JSON with descriptions",
      "file": "ai_tokens.json",
      "include_usage_hints": true
    }
  }
}
```

### Prompt Engineering Token Usage

When generating AI prompts, use semantic tokens:

```
Generate an image with:
- Primary color: {color-brand-primary.$value}
- Secondary color: {color-brand-secondary.$value}
- Style mood: {brand.personality.traits.join(", ")}
- Composition: {imagery.photography.composition.rules.join(", ")}
```

## Validation & Consistency Checks

### AI-Assisted Brand Audit

```json
{
  "audit_prompts": {
    "color_consistency": "Analyze these colors for brand consistency: {colors}. Check for: contrast ratios, harmony, accessibility.",
    "voice_consistency": "Review this content for brand voice alignment: {content}. Brand voice: {voice_attributes}. Score adherence 1-10.",
    "imagery_alignment": "Evaluate if this image matches brand guidelines: {image_description}. Guidelines: {imagery_specs}."
  }
}
```
