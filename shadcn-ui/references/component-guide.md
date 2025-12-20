# shadcn/ui Component Selection Guide

Quick reference for selecting the right component for common use cases.

## Form Components

**User Input:**
- `input` - Single-line text input
- `textarea` - Multi-line text input
- `select` - Dropdown selection
- `combobox` - Searchable dropdown with autocomplete
- `checkbox` - Multi-select options
- `radio-group` - Single-select from options
- `switch` - Boolean toggle (on/off)
- `slider` - Range value selection

**Date/Time:**
- `calendar` - Date picker and calendar view
- `date-picker` - Simple date selection

**Form Structure:**
- `form` - Complete form with validation
- `label` - Input labels and descriptions

## Data Display

**Lists & Tables:**
- `table` - Structured data display
- `accordion` - Collapsible content sections
- `card` - Content container with header/footer

**User Info:**
- `avatar` - Profile images and fallbacks
- `badge` - Status indicators and tags

## Navigation

**Menus:**
- `dropdown-menu` - Action menus and context menus
- `command` - Command palette for quick actions
- `tabs` - Section navigation

**Other:**
- `breadcrumb` - Hierarchical navigation
- `pagination` - Page navigation

## Overlays & Modals

**Dialogs:**
- `dialog` - Modal dialogs for forms/content
- `alert-dialog` - Confirmation and warning dialogs
- `sheet` - Side drawer/panel

**Contextual:**
- `popover` - Contextual popups
- `tooltip` - Hover hints and help text
- `hover-card` - Rich hover content

## Feedback

**Messages:**
- `toast` - Temporary notifications
- `alert` - Persistent status messages

**Progress:**
- `progress` - Progress bars
- `skeleton` - Loading placeholders

## Layout

**Structure:**
- `card` - Content containers
- `separator` - Visual dividers
- `aspect-ratio` - Maintain aspect ratios
- `scroll-area` - Custom scrollable areas

## Interactive

**Actions:**
- `button` - Primary actions and CTAs
- `toggle` - State toggle buttons
- `toggle-group` - Multiple toggle options

## Common Patterns

**User Registration Form:**
- form + input + label + button

**Data Table with Actions:**
- table + dropdown-menu + dialog

**Settings Page:**
- card + switch + select + button

**Search with Filters:**
- input + combobox + popover + command

**User Profile:**
- avatar + card + badge + button

**Dashboard:**
- card + chart + badge + separator

## Accessibility

All shadcn/ui components are built with accessibility in mind:
- Keyboard navigation support
- Screen reader friendly
- ARIA attributes included
- Focus management

## Mobile Considerations

For mobile-first designs, consider:
- Use `sheet` instead of `dialog` for better mobile UX
- Use `combobox` for long select lists
- Ensure touch targets are large enough (buttons, switches)

## Performance

Components are designed for optimal performance:
- Tree-shakeable (only import what you need)
- No runtime CSS-in-JS overhead
- Built on Radix UI primitives
- Minimal bundle size

## Customization

All components support:
- Tailwind CSS classes for styling
- CSS variables for theming
- Component composition and extension
- Variant customization

## Further Reading

- [Official shadcn/ui docs](https://ui.shadcn.com/)
- [Radix UI primitives](https://www.radix-ui.com/)
- [Tailwind CSS docs](https://tailwindcss.com/)
