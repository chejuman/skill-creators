# shadcn/ui Component Reference for Wireframes

## Layout Components

### Container

```tsx
<div className="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
```

### Grid System

```tsx
// 1-4 column responsive grid
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
```

## Navigation Components

| Component      | Use Case                | Key Props                       |
| -------------- | ----------------------- | ------------------------------- |
| NavigationMenu | Main nav with dropdowns | `orientation`, triggers         |
| Breadcrumb     | Page location           | `separator`, items              |
| Tabs           | Content sections        | `defaultValue`, `onValueChange` |
| Sidebar        | App navigation          | collapsible, Sheet for mobile   |

## Data Display

| Component | Use Case          | Key Props                                        |
| --------- | ----------------- | ------------------------------------------------ |
| Card      | Content container | CardHeader, CardContent, CardFooter              |
| Table     | Tabular data      | DataTable for sorting/filtering                  |
| Badge     | Status indicators | `variant`: default/secondary/destructive/outline |
| Avatar    | User images       | fallback initials                                |

## Form Components

| Component  | Use Case             | Key Props                    |
| ---------- | -------------------- | ---------------------------- |
| Input      | Text input           | `type`, `placeholder`        |
| Select     | Dropdown selection   | `onValueChange`, items       |
| Checkbox   | Boolean/multi-select | `checked`, `onCheckedChange` |
| Switch     | Toggle on/off        | `checked`, `onCheckedChange` |
| DatePicker | Date selection       | Calendar + Popover           |

## Feedback Components

| Component | Use Case                | Key Props                      |
| --------- | ----------------------- | ------------------------------ |
| Alert     | Important messages      | `variant`: default/destructive |
| Toast     | Temporary notifications | Sonner integration             |
| Progress  | Loading/completion      | `value`                        |
| Skeleton  | Loading placeholder     | animate-pulse                  |

## Overlay Components

| Component    | Use Case        | Key Props                     |
| ------------ | --------------- | ----------------------------- |
| Dialog       | Modal dialogs   | `open`, `onOpenChange`        |
| Sheet        | Side panels     | `side`: top/right/bottom/left |
| Popover      | Contextual info | trigger + content             |
| DropdownMenu | Action menus    | items, separators             |
| Command      | Command palette | Cmdk-based search             |

## Common Patterns

### Stat Card

```tsx
<Card>
  <CardHeader className="flex flex-row items-center justify-between pb-2">
    <CardTitle className="text-sm font-medium">{title}</CardTitle>
    <Icon className="h-4 w-4 text-muted-foreground" />
  </CardHeader>
  <CardContent>
    <div className="text-2xl font-bold">{value}</div>
    <p className="text-xs text-muted-foreground">{description}</p>
  </CardContent>
</Card>
```

### Data Table with Toolbar

```tsx
<div className="space-y-4">
  <div className="flex items-center gap-2">
    <Input placeholder="Search..." className="max-w-sm" />
    <DropdownMenu>...</DropdownMenu>
    <Button>Export</Button>
  </div>
  <Table>...</Table>
  <Pagination>...</Pagination>
</div>
```

### Sidebar Navigation

```tsx
<aside className="hidden md:flex md:w-64 flex-col border-r">
  <div className="p-4">Logo</div>
  <nav className="flex-1 space-y-1 px-2">
    <Button variant="ghost" className="w-full justify-start">
      <Icon className="mr-2 h-4 w-4" /> Menu Item
    </Button>
  </nav>
</aside>
```

## Variant Reference

### Button Variants

- `default` - Primary action
- `secondary` - Secondary action
- `outline` - Tertiary action
- `ghost` - Minimal emphasis
- `destructive` - Dangerous action

### Badge Variants

- `default` - Neutral
- `secondary` - Muted
- `destructive` - Error/danger
- `outline` - Bordered

## Responsive Prefixes

| Prefix | Min Width | Use           |
| ------ | --------- | ------------- |
| (none) | 0px       | Mobile first  |
| sm:    | 640px     | Small tablets |
| md:    | 768px     | Tablets       |
| lg:    | 1024px    | Desktop       |
| xl:    | 1280px    | Large desktop |
| 2xl:   | 1536px    | Extra large   |
