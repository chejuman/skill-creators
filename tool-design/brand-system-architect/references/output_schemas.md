# Output Schemas

JSON schemas for domain expert outputs. All follow W3C Design Tokens format where applicable.

## W3C Design Tokens Base

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$description": "Brand System Tokens",
  "$version": "1.0.0"
}
```

## Strategy Schema {#strategy}

```json
{
  "brand": {
    "name": { "$value": "string", "$type": "string" },
    "purpose": { "$value": "string", "$type": "string" },
    "mission": { "$value": "string", "$type": "string" },
    "vision": { "$value": "string", "$type": "string" }
  },
  "values": [
    { "name": "string", "description": "string", "priority": "number" }
  ],
  "personality": {
    "traits": ["string"],
    "archetype": { "primary": "string", "secondary": "string" }
  },
  "positioning": {
    "statement": "string",
    "taglines": ["string"],
    "differentiators": ["string"]
  }
}
```

## Color Schema {#colors}

```json
{
  "color": {
    "brand": {
      "primary": {
        "$value": "#hex",
        "$type": "color",
        "hsl": { "h": 0, "s": 0, "l": 0 },
        "semantic": "string"
      },
      "secondary": { "$value": "#hex", "$type": "color" }
    },
    "accent": {
      "default": { "$value": "#hex", "$type": "color" }
    },
    "neutral": {
      "50": { "$value": "#hex", "$type": "color" },
      "900": { "$value": "#hex", "$type": "color" }
    },
    "semantic": {
      "success": { "$value": "#hex", "$type": "color" },
      "warning": { "$value": "#hex", "$type": "color" },
      "error": { "$value": "#hex", "$type": "color" },
      "info": { "$value": "#hex", "$type": "color" }
    }
  },
  "dark_mode": {
    "color": { "...": "inverted values" }
  },
  "accessibility": {
    "contrast_ratios": {
      "primary_on_white": {
        "ratio": "number",
        "aa": "boolean",
        "aaa": "boolean"
      }
    }
  }
}
```

## Typography Schema {#typography}

```json
{
  "font": {
    "family": {
      "heading": { "$value": "Inter, sans-serif", "$type": "fontFamily" },
      "body": { "$value": "Inter, sans-serif", "$type": "fontFamily" },
      "mono": { "$value": "JetBrains Mono, monospace", "$type": "fontFamily" }
    },
    "size": {
      "xs": { "$value": "0.75rem", "$type": "dimension" },
      "sm": { "$value": "0.875rem", "$type": "dimension" },
      "base": { "$value": "1rem", "$type": "dimension" },
      "lg": { "$value": "1.125rem", "$type": "dimension" },
      "xl": { "$value": "1.25rem", "$type": "dimension" },
      "2xl": { "$value": "1.5rem", "$type": "dimension" },
      "3xl": { "$value": "1.875rem", "$type": "dimension" },
      "4xl": { "$value": "2.25rem", "$type": "dimension" }
    },
    "weight": {
      "normal": { "$value": 400, "$type": "fontWeight" },
      "medium": { "$value": 500, "$type": "fontWeight" },
      "semibold": { "$value": 600, "$type": "fontWeight" },
      "bold": { "$value": 700, "$type": "fontWeight" }
    },
    "lineHeight": {
      "tight": { "$value": 1.25, "$type": "number" },
      "normal": { "$value": 1.5, "$type": "number" },
      "relaxed": { "$value": 1.75, "$type": "number" }
    }
  },
  "responsive": {
    "fluid_base": "clamp(1rem, 0.5vw + 0.875rem, 1.125rem)"
  }
}
```

## Motion Schema {#motion}

```json
{
  "motion": {
    "duration": {
      "instant": { "$value": "0ms", "$type": "duration" },
      "fast": { "$value": "150ms", "$type": "duration" },
      "normal": { "$value": "250ms", "$type": "duration" },
      "slow": { "$value": "350ms", "$type": "duration" },
      "slower": { "$value": "500ms", "$type": "duration" }
    },
    "easing": {
      "standard": {
        "$value": "cubic-bezier(0.4, 0, 0.2, 1)",
        "$type": "cubicBezier"
      },
      "entrance": {
        "$value": "cubic-bezier(0, 0, 0.2, 1)",
        "$type": "cubicBezier"
      },
      "exit": {
        "$value": "cubic-bezier(0.4, 0, 1, 1)",
        "$type": "cubicBezier"
      },
      "emphasis": {
        "$value": "cubic-bezier(0.4, 0, 0.6, 1)",
        "$type": "cubicBezier"
      }
    }
  },
  "keyframes": {
    "fade_in": "@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }",
    "slide_up": "@keyframes slideUp { from { transform: translateY(10px); } }"
  },
  "reduced_motion": {
    "duration": { "all": { "$value": "0ms" } }
  }
}
```

## Voice Schema {#voice}

```json
{
  "voice": {
    "attributes": [
      { "trait": "string", "description": "string", "example": "string" }
    ],
    "tone_matrix": {
      "formal_casual": { "scale": 0.0, "description": "string" },
      "serious_playful": { "scale": 0.0, "description": "string" },
      "respectful_irreverent": { "scale": 0.0, "description": "string" }
    }
  },
  "vocabulary": {
    "preferred": ["string"],
    "avoided": ["string"]
  },
  "ai_config": {
    "system_prompt": "string",
    "temperature": 0.7,
    "max_tokens": 500,
    "style_parameters": {
      "formality": 0.5,
      "enthusiasm": 0.7,
      "humor": 0.3
    }
  }
}
```

## Imagery Schema {#imagery}

```json
{
  "photography": {
    "lighting": { "style": "string", "temperature": "string" },
    "color": { "saturation": "string", "treatment": "string" },
    "composition": { "rules": ["string"] },
    "subjects": { "people": "string", "products": "string" }
  },
  "illustration": {
    "style": "string",
    "line_weight": "string",
    "color_approach": "string"
  },
  "ai_generation": {
    "midjourney": {
      "base_prompt": "string",
      "style_ref": "--sref {url}",
      "parameters": "--ar 16:9 --stylize 250 --v 6.1",
      "negative": "--no text, watermark, blur"
    },
    "stable_diffusion": {
      "positive": "string",
      "negative": "string",
      "cfg_scale": 7,
      "sampler": "DPM++ 2M Karras"
    },
    "dall_e": {
      "style": "vivid|natural",
      "quality": "hd"
    }
  }
}
```

## Components Schema {#components}

```json
{
  "spacing": {
    "0": { "$value": "0", "$type": "dimension" },
    "1": { "$value": "0.25rem", "$type": "dimension" },
    "2": { "$value": "0.5rem", "$type": "dimension" },
    "4": { "$value": "1rem", "$type": "dimension" },
    "8": { "$value": "2rem", "$type": "dimension" }
  },
  "radius": {
    "none": { "$value": "0", "$type": "dimension" },
    "sm": { "$value": "0.25rem", "$type": "dimension" },
    "md": { "$value": "0.5rem", "$type": "dimension" },
    "lg": { "$value": "1rem", "$type": "dimension" },
    "full": { "$value": "9999px", "$type": "dimension" }
  },
  "shadow": {
    "sm": { "$value": "0 1px 2px rgba(0,0,0,0.05)", "$type": "shadow" },
    "md": { "$value": "0 4px 6px rgba(0,0,0,0.1)", "$type": "shadow" },
    "lg": { "$value": "0 10px 15px rgba(0,0,0,0.1)", "$type": "shadow" }
  },
  "focus": {
    "ring_width": { "$value": "2px", "$type": "dimension" },
    "ring_color": { "$value": "{color.brand.primary}", "$type": "color" },
    "ring_offset": { "$value": "2px", "$type": "dimension" }
  }
}
```

## Layout Schema {#layout}

```json
{
  "breakpoint": {
    "xs": { "$value": "320px", "$type": "dimension" },
    "sm": { "$value": "640px", "$type": "dimension" },
    "md": { "$value": "768px", "$type": "dimension" },
    "lg": { "$value": "1024px", "$type": "dimension" },
    "xl": { "$value": "1280px", "$type": "dimension" },
    "2xl": { "$value": "1536px", "$type": "dimension" }
  },
  "container": {
    "sm": { "$value": "640px", "$type": "dimension" },
    "md": { "$value": "768px", "$type": "dimension" },
    "lg": { "$value": "1024px", "$type": "dimension" },
    "xl": { "$value": "1280px", "$type": "dimension" }
  },
  "grid": {
    "columns": 12,
    "gutter": { "$value": "1.5rem", "$type": "dimension" },
    "margin": { "$value": "1rem", "$type": "dimension" }
  },
  "z_index": {
    "base": 0,
    "dropdown": 100,
    "sticky": 200,
    "modal": 300,
    "toast": 400
  }
}
```

## Multimedia Schema {#multimedia}

```json
{
  "video": {
    "pacing": { "cuts_per_minute": "number", "rhythm": "string" },
    "transitions": ["string"],
    "color_grading": { "lut": "string", "look": "string" },
    "aspect_ratios": {
      "landscape": "16:9",
      "portrait": "9:16",
      "square": "1:1"
    }
  },
  "audio": {
    "sonic_logo": { "description": "string", "duration": "string" },
    "music": { "genre": "string", "tempo_bpm": "number", "mood": ["string"] },
    "ui_sounds": { "click": "string", "success": "string", "error": "string" }
  },
  "captions": {
    "font": { "$value": "{font.family.body}" },
    "size": { "$value": "1rem" },
    "position": "bottom",
    "background": "rgba(0,0,0,0.7)"
  }
}
```

## Marketing Schema {#marketing}

```json
{
  "social": {
    "instagram": {
      "post": { "width": 1080, "height": 1080 },
      "story": { "width": 1080, "height": 1920 },
      "safe_zone": { "margin": 100 }
    },
    "linkedin": {
      "post": { "width": 1200, "height": 627 }
    }
  },
  "display_ads": {
    "leaderboard": { "width": 728, "height": 90 },
    "medium_rectangle": { "width": 300, "height": 250 },
    "safe_zone_percent": 10
  },
  "email": {
    "width": 600,
    "padding": 20,
    "cta_button": { "height": 44, "min_width": 120 }
  },
  "print": {
    "business_card": { "width": "3.5in", "height": "2in", "bleed": "0.125in" }
  }
}
```
