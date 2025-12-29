# /wire-spec

View or generate component specification.

## Usage

```
/wire-spec {component_name}
/wire-spec {component_name} --screen {screen}
/wire-spec --generate {component_name} --screen {screen}
```

## Examples

```
/wire-spec StatCard
/wire-spec DataTable --screen dashboard
/wire-spec --generate UserMenu --screen header
```

## Workflow

### View Existing Spec

1. **Search for Spec**

   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/search_docs.py --query "{component}" --type specs
   ```

2. **Display Spec**
   - Props interface
   - State management
   - Events
   - Usage example

### Generate New Spec

1. **Generate Spec**
   ```bash
   python3 ~/.claude/skills/wireframe-design-studio/scripts/spec_generator.py component --name {name} --screen {screen}
   ```

## Output

````markdown
## Component Spec: StatCard

### Overview

| Property    | Value     |
| ----------- | --------- |
| Name        | StatCard  |
| Screen      | dashboard |
| shadcn Base | Card      |

### Props Interface

```typescript
interface StatCardProps {
  title: string;
  value: string | number;
  icon?: LucideIcon;
  trend?: { value: number; direction: "up" | "down" };
  variant?: "default" | "success" | "warning" | "danger";
}
```
````

### Props Table

| Prop  | Type             | Required | Default | Description  |
| ----- | ---------------- | -------- | ------- | ------------ |
| title | string           | Yes      | -       | Card title   |
| value | string \| number | Yes      | -       | Main metric  |
| icon  | LucideIcon       | No       | null    | Leading icon |

### Events

| Event   | Payload | Description        |
| ------- | ------- | ------------------ |
| onClick | void    | Card click handler |

### Usage Example

```tsx
<StatCard
  title="Revenue"
  value="$12,500"
  icon={DollarSign}
  trend={{ value: 12.5, direction: "up" }}
/>
```

```

## Options

| Option | Description |
|--------|-------------|
| --screen | Target screen name |
| --generate | Generate new spec instead of viewing |
| --category | Component category (display, input, navigation) |
| --shadcn | shadcn/ui base component |

## Related Commands

- `/wire-view {screen}` - View wireframe
- `/wire-search {query}` - Search docs
```
