# Slidev Layouts Reference

Detailed examples for all built-in Slidev layouts.

## Cover Layout
Title slide for presentations.

```markdown
---
layout: cover
background: /images/background.jpg
---

# Presentation Title

Subtitle or tagline

<div class="abs-bl m-6 text-sm opacity-50">
  Author Name | Date
</div>
```

## Center Layout
Content centered on screen.

```markdown
---
layout: center
class: text-center
---

# Centered Title

This content is horizontally and vertically centered.
```

## Default Layout
Standard slide with title and content.

```markdown
---
layout: default
---

# Slide Title

- Point one
- Point two
- Point three
```

## Two-Cols Layout
Side-by-side columns.

```markdown
---
layout: two-cols
---

# Left Column

- Left item 1
- Left item 2
- Left item 3

::right::

# Right Column

- Right item 1
- Right item 2
- Right item 3
```

## Two-Cols-Header Layout
Full-width header with columns below.

```markdown
---
layout: two-cols-header
---

::header::

# Full Width Header

This spans both columns

::left::

## Left Section
Content for left column

::right::

## Right Section
Content for right column
```

## Image Layout
Full-screen image.

```markdown
---
layout: image
image: /images/photo.jpg
---
```

## Image-Left Layout
Image on left, content on right.

```markdown
---
layout: image-left
image: /images/photo.jpg
---

# Title

Content appears on the right side of the image.

- Feature 1
- Feature 2
- Feature 3
```

## Image-Right Layout
Content on left, image on right.

```markdown
---
layout: image-right
image: /images/photo.jpg
---

# Title

Content appears on the left side of the image.

- Feature 1
- Feature 2
- Feature 3
```

## Quote Layout
Display quotations prominently.

```markdown
---
layout: quote
---

"The only way to do great work is to love what you do."

– Steve Jobs
```

## Fact Layout
Highlight key data or statistics.

```markdown
---
layout: fact
---

# 42%

Percentage of developers who prefer Markdown for presentations
```

## Statement Layout
Bold declarative statements.

```markdown
---
layout: statement
---

# Code is Poetry
```

## Section Layout
Mark new sections in presentation.

```markdown
---
layout: section
---

# Part 2

Advanced Features
```

## Full Layout
Use entire screen without padding.

```markdown
---
layout: full
---

<div class="w-full h-full flex items-center justify-center bg-gradient-to-r from-blue-500 to-purple-500">
  <h1 class="text-6xl text-white">Full Screen</h1>
</div>
```

## Iframe Layout
Embed web pages.

```markdown
---
layout: iframe
url: https://sli.dev
---
```

## Iframe-Left Layout
Iframe on left, content on right.

```markdown
---
layout: iframe-left
url: https://sli.dev
---

# Live Demo

The embedded website shows our product in action.
```

## Iframe-Right Layout
Content on left, iframe on right.

```markdown
---
layout: iframe-right
url: https://sli.dev
---

# Documentation

See the live documentation on the right.
```

## Intro Layout
Introduction slide with author info.

```markdown
---
layout: intro
---

# Welcome

A presentation about modern web development

<div class="absolute bottom-10">
  <span class="font-medium">
    John Doe | Tech Conference 2024
  </span>
</div>
```

## End Layout
Closing slide.

```markdown
---
layout: end
---

# Thank You!

Questions?

<div class="abs-br m-6">
  @yourhandle
</div>
```

## None Layout
No styling applied - blank canvas.

```markdown
---
layout: none
---

<div class="absolute inset-0 flex items-center justify-center">
  Completely custom layout
</div>
```

## Layout Options

### Common Frontmatter for Layouts
```yaml
---
layout: layout-name
class: 'custom-class'           # Additional CSS classes
background: '/image.jpg'        # Background image
backgroundSize: 'cover'         # Background size
backgroundPosition: 'center'    # Background position
---
```

### Custom Layouts
Create `layouts/my-layout.vue` in project:

```vue
<template>
  <div class="slidev-layout my-layout">
    <slot />
  </div>
</template>
```

Use with:
```yaml
---
layout: my-layout
---
```
