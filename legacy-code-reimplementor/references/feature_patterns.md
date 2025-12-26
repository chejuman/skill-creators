# Feature-Based Implementation Patterns

Best practices for atomic, iterative feature implementation.

## What is a Feature?

A feature is the smallest independently-implementable and verifiable unit of functionality.

### Good Feature Characteristics

- **Atomic**: Can be implemented without partial states
- **Testable**: Has clear inputs/outputs for verification
- **Independent**: Minimal dependencies on unimplemented features
- **Valuable**: Provides measurable progress toward completion

### Feature Granularity

| Too Large         | Just Right             | Too Small               |
| ----------------- | ---------------------- | ----------------------- |
| "User Management" | "User Registration"    | "Validate email format" |
| "Product Catalog" | "Product Search API"   | "Trim whitespace"       |
| "Authentication"  | "JWT Token Generation" | "Check null"            |

## Feature Extraction Strategy

### 1. Dependency-First Ordering

```
Priority 1: No dependencies (foundations)
├── Configuration
├── Utilities
└── Constants

Priority 2: Data layer
├── Models/Entities
└── Repositories

Priority 3: Business logic
├── Services
└── Use cases

Priority 4: Interface layer
├── Controllers/Handlers
└── API endpoints

Priority 5: Integration
├── External services
└── Migration scripts
```

### 2. Unit Decomposition

Each feature contains 1-N units. A unit should be:

- Implementable in one session
- ~50-200 lines of code
- Testable in isolation

Example feature breakdown:

```
Feature: User Authentication
├── Unit 1: User model and schema
├── Unit 2: Password hashing utilities
├── Unit 3: JWT token generation
├── Unit 4: Login endpoint
└── Unit 5: Session management
```

## Implementation Cycle

For each unit:

```
┌─────────────────────────────────────────────┐
│ 1. IMPLEMENT                                │
│    - Read original source                   │
│    - Write new implementation               │
│    - Follow target stack conventions        │
├─────────────────────────────────────────────┤
│ 2. TEST                                     │
│    - Unit tests for new code               │
│    - Edge cases from original              │
│    - Integration with completed units       │
├─────────────────────────────────────────────┤
│ 3. VERIFY                                   │
│    - Compare function coverage              │
│    - Validate behavior matches              │
│    - Run verification script               │
├─────────────────────────────────────────────┤
│ 4. COMMIT                                   │
│    - Save context                          │
│    - Generate continuation command          │
│    - Document any deviations               │
└─────────────────────────────────────────────┘
```

## Context Continuity

### Session State

The `.reimpl-context.json` file tracks:

```json
{
  "current_feature_id": 3,
  "current_unit_id": 2,
  "features": [
    {
      "id": 1,
      "status": "completed",
      "completed_units": 2,
      "units": 2
    },
    {
      "id": 2,
      "status": "completed",
      "completed_units": 3,
      "units": 3
    },
    {
      "id": 3,
      "status": "in_progress",
      "completed_units": 1,
      "units": 4
    }
  ],
  "next_prompt": "Implement Feature 3, Unit 2: OrderRepository..."
}
```

### Continuation Prompt

After each unit, generate a complete next-step prompt:

```
## Continue: Feature 3 (Order Management), Unit 2

### Context
- Repo A: /path/to/legacy
- Repo B: /path/to/new
- Stack: Python + FastAPI + Clean Architecture

### Previous Work (Unit 1)
- Implemented: Order model, OrderStatus enum
- Files: src/domain/order.py

### Current Task (Unit 2)
Implement OrderRepository with:
- CRUD operations for orders
- Query by user, status, date range
- Transaction support

### Source Reference
Original files to analyze:
- legacy/dao/OrderDAO.java
- legacy/repository/OrderRepository.java

### Target Structure
Create in: src/infrastructure/repositories/order_repository.py
```

## Handling Dependencies

### Forward References

When a feature depends on unimplemented features:

1. Create interface/protocol first
2. Use dependency injection
3. Mock dependencies in tests
4. Document for later connection

### Circular Dependencies

If detected:

1. Extract shared interface to new feature
2. Implement interface first
3. Both features depend on interface

## Verification Metrics

### Coverage Thresholds

| Metric            | Pass | Warning | Fail |
| ----------------- | ---- | ------- | ---- |
| Function coverage | ≥90% | 70-89%  | <70% |
| Class coverage    | ≥90% | 70-89%  | <70% |
| Line coverage     | ≥80% | 60-79%  | <60% |

### Acceptable Differences

Some differences between Repo A and Repo B are expected:

- **Language idioms**: Different conventions are OK
- **Improved patterns**: Better approaches in new stack
- **Removed deprecated**: Old workarounds not needed
- **Added helpers**: Supporting functions for clarity

### Must Match

- Core business logic behavior
- API contracts (inputs/outputs)
- Error handling semantics
- Edge case handling

## Progress Tracking

### TodoWrite Pattern

```python
TodoWrite(todos=[
  {"content": f"F{fid}.U{uid}: Implement {name}", "status": "in_progress", "activeForm": f"Implementing {name}"},
  {"content": f"F{fid}.U{uid}: Write tests", "status": "pending", "activeForm": "Writing tests"},
  {"content": f"F{fid}.U{uid}: Verify", "status": "pending", "activeForm": "Verifying"}
])
```

### Completion Markers

After each unit:

1. Mark current todo as complete
2. Update context with completion
3. Advance to next unit/feature
4. Generate continuation command
