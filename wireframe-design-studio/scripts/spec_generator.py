#!/usr/bin/env python3
"""
Spec Generator for Wireframe Design Studio
Generates component specifications, accessibility checklists, and responsive configs.

Usage:
    python3 spec_generator.py component --name StatCard --screen dashboard
    python3 spec_generator.py a11y --screen dashboard
    python3 spec_generator.py responsive --screen dashboard
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


WIREFRAME_DOCS_DIR = ".wireframe-docs"

COMPONENT_TEMPLATE = """# Component Spec: {name}

## Overview

| Property    | Value                 |
| ----------- | --------------------- |
| Name        | {name}                |
| Screen      | {screen}              |
| Category    | {category}            |
| shadcn Base | {shadcn_base}         |
| Created     | {created}             |

## shadcn/ui Components Used

{shadcn_components}

## Props Interface

```typescript
interface {name}Props {{
{props_interface}
}}
```

## Props Table

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
{props_table}

## State Management

| State | Type | Initial | Trigger |
|-------|------|---------|---------|
{state_table}

## Events

| Event | Payload | Description |
|-------|---------|-------------|
{events_table}

## Variants

| Variant | Description | Classes |
|---------|-------------|---------|
{variants_table}

## Usage Example

```tsx
{usage_example}
```

## Accessibility Notes

{a11y_notes}

## Responsive Behavior

{responsive_behavior}
"""

A11Y_TEMPLATE = """# Accessibility Checklist: {screen}

**Screen:** {screen}
**Generated:** {created}
**Standard:** WCAG 2.1 AA

## Keyboard Navigation

- [ ] All interactive elements are focusable via Tab
- [ ] Logical tab order follows visual layout
- [ ] Focus indicator is clearly visible (ring-2 ring-offset-2)
- [ ] Escape key closes modals/dropdowns/popovers
- [ ] Arrow keys navigate within menus and lists
- [ ] Enter/Space activates buttons and links
- [ ] No keyboard traps

## Screen Reader Support

- [ ] Page has descriptive `<title>`
- [ ] Semantic HTML structure (header, nav, main, section, footer)
- [ ] Headings follow logical hierarchy (h1 → h2 → h3)
- [ ] Images have meaningful alt text
- [ ] Icon-only buttons have aria-label
- [ ] Form inputs have associated labels
- [ ] Dynamic content uses aria-live regions
- [ ] Tables have proper headers with scope

## Visual Design

- [ ] Text color contrast ratio ≥ 4.5:1
- [ ] UI component contrast ratio ≥ 3:1
- [ ] Information not conveyed by color alone
- [ ] Focus states distinct from hover states
- [ ] Content readable at 200% zoom
- [ ] No horizontal scrolling at 320px width

## Forms & Inputs

- [ ] All inputs have visible labels
- [ ] Required fields clearly marked
- [ ] Error messages linked via aria-describedby
- [ ] Error states use more than just color
- [ ] Form validation feedback is accessible
- [ ] Autocomplete attributes where appropriate

## Interactive Components

### Buttons
- [ ] Type attribute specified
- [ ] Disabled state communicated
- [ ] Loading state with aria-busy

### Links
- [ ] Descriptive link text (not "click here")
- [ ] External links indicated
- [ ] Skip links for main content

### Modals/Dialogs
- [ ] Focus trapped within modal
- [ ] Focus returns on close
- [ ] aria-modal="true" applied
- [ ] Backdrop click closes modal

### Dropdowns/Menus
- [ ] aria-expanded state managed
- [ ] aria-haspopup attribute set
- [ ] Menu items with role="menuitem"

### Tables
- [ ] Caption or aria-label for table purpose
- [ ] Header cells use <th> with scope
- [ ] Complex tables use headers attribute

## Testing Checklist

- [ ] Tested with keyboard only
- [ ] Tested with screen reader (VoiceOver/NVDA)
- [ ] Tested color contrast with tool
- [ ] Tested at 200% zoom
- [ ] Tested with reduced motion preference
"""

RESPONSIVE_TEMPLATE = """# Responsive Design: {screen}

**Screen:** {screen}
**Generated:** {created}

## Breakpoint Definitions

| Breakpoint | Tailwind | Min Width | Max Width |
|------------|----------|-----------|-----------|
| mobile     | (default)| 0px       | 639px     |
| sm         | sm:      | 640px     | 767px     |
| md         | md:      | 768px     | 1023px    |
| lg         | lg:      | 1024px    | 1279px    |
| xl         | xl:      | 1280px    | 1535px    |
| 2xl        | 2xl:     | 1536px    | ∞         |

## Layout Adaptations

### Container

| Breakpoint | Width      | Padding |
|------------|------------|---------|
| mobile     | 100%       | px-4    |
| sm         | 100%       | px-6    |
| md         | 100%       | px-8    |
| lg         | max-w-7xl  | px-8    |
| xl         | max-w-7xl  | px-8    |

### Grid System

| Breakpoint | Columns | Gap    |
|------------|---------|--------|
| mobile     | 1       | gap-4  |
| sm         | 2       | gap-4  |
| md         | 2       | gap-6  |
| lg         | 3       | gap-6  |
| xl         | 4       | gap-8  |

## Component Adaptations

### Header
| Breakpoint | Logo | Search | Nav | User Menu |
|------------|------|--------|-----|-----------|
| mobile     | Icon | Hidden | Hamburger | Avatar |
| md         | Full | Compact | Icons | Avatar + Name |
| lg         | Full | Full | Full text | Full dropdown |

### Sidebar
| Breakpoint | Display | Width | Behavior |
|------------|---------|-------|----------|
| mobile     | Sheet (Drawer) | w-64 | Toggle via hamburger |
| md         | Collapsed | w-16 | Icons only, expand on hover |
| lg         | Expanded | w-64 | Always visible |

### Cards/Grid Items
| Breakpoint | Columns | Card Style |
|------------|---------|------------|
| mobile     | 1 | Full width, stacked |
| sm         | 2 | Compact |
| lg         | 3-4 | Standard |

### Data Table
| Breakpoint | Display Mode | Features |
|------------|--------------|----------|
| mobile     | Card stack | Priority columns only |
| md         | Horizontal scroll | All columns |
| lg         | Full table | All features |

## Tailwind Class Patterns

### Responsive Layout
```tsx
// Container
<div className="w-full px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">

// Grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">

// Sidebar + Content
<div className="flex">
  <aside className="hidden md:block md:w-16 lg:w-64">
  <main className="flex-1">
</div>
```

### Responsive Typography
```tsx
// Heading
<h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold">

// Body
<p className="text-sm sm:text-base">
```

### Responsive Spacing
```tsx
// Padding
<div className="p-4 sm:p-6 lg:p-8">

// Margin
<div className="mt-4 sm:mt-6 lg:mt-8">

// Gap
<div className="gap-2 sm:gap-4 lg:gap-6">
```

## Media Query Hooks

```tsx
// useMediaQuery hook usage
const isMobile = useMediaQuery('(max-width: 639px)')
const isTablet = useMediaQuery('(min-width: 640px) and (max-width: 1023px)')
const isDesktop = useMediaQuery('(min-width: 1024px)')
```

## Testing Checklist

- [ ] Tested at 320px (minimum mobile)
- [ ] Tested at 640px (sm breakpoint)
- [ ] Tested at 768px (md breakpoint)
- [ ] Tested at 1024px (lg breakpoint)
- [ ] Tested at 1280px (xl breakpoint)
- [ ] Touch targets ≥ 44x44px on mobile
- [ ] No horizontal overflow
- [ ] Images scale appropriately
"""


def get_docs_path(base_path: str = ".") -> Path:
    return Path(base_path) / WIREFRAME_DOCS_DIR


def generate_component_spec(name: str, screen: str, category: str = "display",
                            shadcn_base: str = "Card", base_path: str = ".") -> str:
    """Generate component specification."""
    spec = COMPONENT_TEMPLATE.format(
        name=name,
        screen=screen,
        category=category,
        shadcn_base=shadcn_base,
        created=datetime.now().strftime('%Y-%m-%d'),
        shadcn_components=f"- {shadcn_base}\n- (Add more components)",
        props_interface="  // Add props here",
        props_table="| - | - | - | - | - |",
        state_table="| - | - | - | - |",
        events_table="| - | - | - |",
        variants_table="| default | Default style | - |",
        usage_example=f"<{name} />",
        a11y_notes="- Add accessibility notes",
        responsive_behavior="- Add responsive behavior"
    )

    spec_dir = get_docs_path(base_path) / "specs" / screen
    spec_dir.mkdir(parents=True, exist_ok=True)

    spec_path = spec_dir / f"{name.lower()}_spec.md"
    with open(spec_path, "w") as f:
        f.write(spec)

    return str(spec_path)


def generate_a11y_checklist(screen: str, base_path: str = ".") -> str:
    """Generate accessibility checklist."""
    checklist = A11Y_TEMPLATE.format(
        screen=screen,
        created=datetime.now().strftime('%Y-%m-%d')
    )

    spec_dir = get_docs_path(base_path) / "specs" / screen
    spec_dir.mkdir(parents=True, exist_ok=True)

    checklist_path = spec_dir / "a11y_checklist.md"
    with open(checklist_path, "w") as f:
        f.write(checklist)

    return str(checklist_path)


def generate_responsive_config(screen: str, base_path: str = ".") -> str:
    """Generate responsive configuration."""
    config = RESPONSIVE_TEMPLATE.format(
        screen=screen,
        created=datetime.now().strftime('%Y-%m-%d')
    )

    spec_dir = get_docs_path(base_path) / "specs" / screen
    spec_dir.mkdir(parents=True, exist_ok=True)

    config_path = spec_dir / "responsive.md"
    with open(config_path, "w") as f:
        f.write(config)

    return str(config_path)


def main():
    parser = argparse.ArgumentParser(description="Generate wireframe specs")
    subparsers = parser.add_subparsers(dest="command", required=True)

    comp_parser = subparsers.add_parser("component", help="Generate component spec")
    comp_parser.add_argument("--name", required=True, help="Component name")
    comp_parser.add_argument("--screen", required=True, help="Screen name")
    comp_parser.add_argument("--category", default="display", help="Component category")
    comp_parser.add_argument("--shadcn", default="Card", help="shadcn/ui base component")
    comp_parser.add_argument("--path", default=".", help="Base path")

    a11y_parser = subparsers.add_parser("a11y", help="Generate a11y checklist")
    a11y_parser.add_argument("--screen", required=True, help="Screen name")
    a11y_parser.add_argument("--path", default=".", help="Base path")

    resp_parser = subparsers.add_parser("responsive", help="Generate responsive config")
    resp_parser.add_argument("--screen", required=True, help="Screen name")
    resp_parser.add_argument("--path", default=".", help="Base path")

    args = parser.parse_args()

    if args.command == "component":
        path = generate_component_spec(args.name, args.screen, args.category, args.shadcn, args.path)
        print(json.dumps({"status": "created", "path": path}, indent=2))
    elif args.command == "a11y":
        path = generate_a11y_checklist(args.screen, args.path)
        print(json.dumps({"status": "created", "path": path}, indent=2))
    elif args.command == "responsive":
        path = generate_responsive_config(args.screen, args.path)
        print(json.dumps({"status": "created", "path": path}, indent=2))


if __name__ == "__main__":
    main()
