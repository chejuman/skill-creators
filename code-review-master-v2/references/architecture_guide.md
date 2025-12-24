# Architecture Guide

SOLID principles, design patterns, and architectural review guidelines.

## SOLID Principles

### Single Responsibility Principle (SRP)

A class should have only one reason to change.

```typescript
// BAD: Multiple responsibilities
class UserService {
  createUser(data: UserData) {
    /* ... */
  }
  sendWelcomeEmail(user: User) {
    /* ... */
  }
  generateReport(users: User[]) {
    /* ... */
  }
  validateUserInput(data: UserData) {
    /* ... */
  }
}

// GOOD: Separated concerns
class UserService {
  createUser(data: UserData) {
    /* ... */
  }
}

class EmailService {
  sendWelcomeEmail(user: User) {
    /* ... */
  }
}

class UserReportService {
  generateReport(users: User[]) {
    /* ... */
  }
}

class UserValidator {
  validate(data: UserData) {
    /* ... */
  }
}
```

### Open/Closed Principle (OCP)

Open for extension, closed for modification.

```typescript
// BAD: Must modify to add new payment type
class PaymentProcessor {
  process(type: string, amount: number) {
    if (type === "credit") {
      /* ... */
    } else if (type === "debit") {
      /* ... */
    }
    // Must add else-if for each new type
  }
}

// GOOD: Extensible without modification
interface PaymentMethod {
  process(amount: number): Promise<Result>;
}

class CreditPayment implements PaymentMethod {
  process(amount: number) {
    /* ... */
  }
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}
  process(amount: number) {
    return this.method.process(amount);
  }
}
```

### Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types.

```typescript
// BAD: Violates LSP
class Rectangle {
  setWidth(w: number) {
    this.width = w;
  }
  setHeight(h: number) {
    this.height = h;
  }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w; // Changes both!
  }
}

// GOOD: Proper abstraction
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(
    private width: number,
    private height: number,
  ) {}
  area() {
    return this.width * this.height;
  }
}

class Square implements Shape {
  constructor(private side: number) {}
  area() {
    return this.side * this.side;
  }
}
```

### Interface Segregation Principle (ISP)

Clients should not depend on interfaces they don't use.

```typescript
// BAD: Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

// Robots can't eat or sleep!
class Robot implements Worker {
  work() {
    /* ... */
  }
  eat() {
    throw new Error("Not applicable");
  }
  sleep() {
    throw new Error("Not applicable");
  }
}

// GOOD: Segregated interfaces
interface Workable {
  work(): void;
}

interface Feedable {
  eat(): void;
}

class Robot implements Workable {
  work() {
    /* ... */
  }
}

class Human implements Workable, Feedable {
  work() {
    /* ... */
  }
  eat() {
    /* ... */
  }
}
```

### Dependency Inversion Principle (DIP)

Depend on abstractions, not concretions.

```typescript
// BAD: Concrete dependency
class UserService {
  private db = new MySQLDatabase(); // Tight coupling

  getUser(id: string) {
    return this.db.query(`SELECT * FROM users WHERE id = ?`, [id]);
  }
}

// GOOD: Abstraction dependency
interface Database {
  query(sql: string, params: any[]): Promise<any>;
}

class UserService {
  constructor(private db: Database) {} // Inject abstraction

  getUser(id: string) {
    return this.db.query(`SELECT * FROM users WHERE id = ?`, [id]);
  }
}
```

## Common Anti-patterns

### God Object

One class that knows/does too much.

**Detection:**

- Class with 500+ lines
- 20+ methods
- Dependencies on 10+ other classes
- "Manager" or "Handler" suffix

### Spaghetti Code

Unstructured, tangled control flow.

**Detection:**

- Deep nesting (5+ levels)
- Functions 100+ lines
- Many goto-like patterns
- Global state mutations

### Golden Hammer

Using one pattern/tool for everything.

**Detection:**

- Same pattern everywhere
- Force-fitting solutions
- Ignoring simpler alternatives

### Leaky Abstraction

Implementation details exposed through abstraction.

**Detection:**

- Interface requires knowledge of implementation
- Exceptions from underlying layers bubble up
- Configuration specific to one implementation

## Layer Architecture

### Violations to Detect

```
┌─────────────────────┐
│   Presentation      │  ← Should NOT access DB directly
├─────────────────────┤
│   Business Logic    │
├─────────────────────┤
│   Data Access       │
└─────────────────────┘
```

```typescript
// BAD: UI layer accessing database
function UserProfile({ userId }: Props) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Direct DB access in UI component!
    const result = await db.query("SELECT * FROM users WHERE id = ?", [userId]);
    setUser(result);
  }, [userId]);
}

// GOOD: Proper layering
function UserProfile({ userId }: Props) {
  const { data: user } = useQuery(
    ["user", userId],
    () => userService.getById(userId), // Through service layer
  );
}
```

## Testability Checklist

```
[ ] Dependencies are injectable
[ ] No static method dependencies
[ ] No hidden dependencies (service locators)
[ ] Side effects isolated
[ ] Pure functions where possible
[ ] Interfaces for external services
```

## Architecture Severity Guide

| Finding                 | Severity |
| ----------------------- | -------- |
| Circular dependencies   | High     |
| Layer violations        | High     |
| God object (>500 lines) | Medium   |
| SOLID violation (SRP)   | Medium   |
| Missing abstraction     | Medium   |
| Tight coupling          | Medium   |
| Missing interface       | Low      |
| Naming inconsistency    | Low      |
