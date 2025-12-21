# Design Tokens Reference

Complete specification of design tokens for the infographic system.

## Grid Tokens

```json
{
  "grid": {
    "8x8": {
      "cols": 8,
      "rows": 8,
      "gutter": {"min": 9, "max": 13},
      "use_case": "compact layouts, ≤16 items"
    },
    "12x12": {
      "cols": 12,
      "rows": 12,
      "gutter": {"min": 9, "max": 11},
      "use_case": "detailed layouts, >16 items"
    }
  },
  "margin": {
    "default": 24,
    "compact": 16,
    "spacious": 32
  }
}
```

## Typography Tokens

```json
{
  "typography": {
    "fontFamily": {
      "primary": "Inter",
      "fallback": ["Helvetica Neue", "Arial", "system-ui", "sans-serif"]
    },
    "fontSize": {
      "title": 32,
      "subtitle": 24,
      "body": 16,
      "caption": 12,
      "data": 11
    },
    "fontWeight": {
      "bold": 700,
      "semibold": 600,
      "medium": 500,
      "regular": 400
    },
    "lineHeight": {
      "tight": 1.0,
      "snug": 1.2,
      "normal": 1.5,
      "relaxed": 1.6
    },
    "letterSpacing": {
      "tight": "-0.02em",
      "normal": "0",
      "wide": "0.02em"
    }
  }
}
```

## Color Tokens

```json
{
  "color": {
    "palette": {
      "default": {
        "primary": "#1A1A2E",
        "secondary": "#4A4A68",
        "accent": "#E94560",
        "neutral": "#F0F0F5",
        "muted": "#9090A0"
      },
      "monochrome": {
        "primary": "#1A1A1A",
        "secondary": "#4A4A4A",
        "accent": "#2A6BD4",
        "neutral": "#F5F5F5",
        "muted": "#909090"
      },
      "warm": {
        "primary": "#2E1A1A",
        "secondary": "#684A4A",
        "accent": "#E96045",
        "neutral": "#F5F0F0",
        "muted": "#A09090"
      },
      "cool": {
        "primary": "#1A1A2E",
        "secondary": "#4A4A68",
        "accent": "#45B5E9",
        "neutral": "#F0F0F5",
        "muted": "#9090A0"
      }
    },
    "semantic": {
      "dataInk": "var(--color-primary)",
      "background": "var(--color-neutral)",
      "highlight": "var(--color-accent)",
      "deemphasis": "var(--color-muted)"
    },
    "constraints": {
      "maxSaturation": "22%",
      "accentUsage": "≤22%"
    }
  }
}
```

## Spacing Tokens

```json
{
  "spacing": {
    "unit": 8,
    "scale": {
      "xs": 4,
      "sm": 8,
      "md": 16,
      "lg": 24,
      "xl": 32,
      "2xl": 48,
      "3xl": 64
    }
  }
}
```

## Icon Tokens

```json
{
  "icon": {
    "artboard": 64,
    "stroke": 4,
    "cornerRadius": "8%",
    "style": "monoline",
    "padding": 8
  }
}
```

## Visualization Tokens

```json
{
  "visualization": {
    "axis": {
      "hairlineWidth": 0.5,
      "labelRotation": 45,
      "tickLength": 4,
      "defaultScale": "logarithmic"
    },
    "horizon": {
      "numBands": 3,
      "mirrorNegative": true
    },
    "euler": {
      "fillOpacity": 0.3,
      "strokeWidth": 2
    },
    "sparkline": {
      "height": 24,
      "lineWidth": 1.5
    },
    "metrics": {
      "minDataInkRatio": 0.8,
      "maxEntropy": 0.18
    }
  }
}
```

## Export Tokens

```json
{
  "export": {
    "webp": {
      "quality": 100,
      "colorProfile": "Display P3"
    },
    "svg": {
      "cssVariables": true,
      "accessible": true
    },
    "responsive": {
      "breakpoints": [320, 768, 1024, 1440],
      "fluidTypography": "clamp(12px, 2vw, 16px)"
    }
  }
}
```

## CSS Custom Properties

```css
:root {
  /* Grid */
  --grid-cols: 12;
  --grid-rows: 12;
  --grid-gutter: 11px;
  --grid-margin: 24px;

  /* Typography */
  --font-family: "Inter", "Helvetica Neue", Arial, system-ui, sans-serif;
  --font-size-title: 32px;
  --font-size-subtitle: 24px;
  --font-size-body: 16px;
  --font-size-caption: 12px;
  --font-size-data: 11px;

  /* Colors */
  --color-primary: #1A1A2E;
  --color-secondary: #4A4A68;
  --color-accent: #E94560;
  --color-neutral: #F0F0F5;
  --color-muted: #9090A0;

  /* Spacing */
  --spacing-unit: 8px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Visualization */
  --axis-hairline: 0.5pt;
  --data-ink-min: 0.8;
  --entropy-max: 0.18;
}
```
