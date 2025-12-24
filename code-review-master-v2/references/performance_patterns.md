# Performance Patterns

Anti-patterns and optimization guides for performance review.

## Algorithmic Complexity

### Common Anti-patterns

```typescript
// BAD: O(n²) nested loops
function findDuplicates(arr: string[]): string[] {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// GOOD: O(n) with Set
function findDuplicates(arr: string[]): string[] {
  const seen = new Set<string>();
  const duplicates = new Set<string>();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return [...duplicates];
}
```

### Data Structure Selection

| Use Case         | Wrong               | Right             | Improvement       |
| ---------------- | ------------------- | ----------------- | ----------------- |
| Lookup by key    | Array.find()        | Map/Object        | O(n) → O(1)       |
| Unique values    | Array + includes()  | Set               | O(n) → O(1)       |
| Queue operations | Array shift/unshift | Linked list/Deque | O(n) → O(1)       |
| Sorted iteration | Sort on each access | Sorted structure  | O(n log n) → O(1) |

## Database Performance

### N+1 Query Pattern

```python
# BAD: N+1 queries
users = User.objects.all()
for user in users:
    orders = Order.objects.filter(user_id=user.id)  # N queries!
    process(user, orders)

# GOOD: Prefetch
users = User.objects.prefetch_related('orders').all()
for user in users:
    orders = user.orders.all()  # No additional queries
    process(user, orders)
```

### Missing Pagination

```javascript
// BAD: Fetch all records
const users = await db.query("SELECT * FROM users");

// GOOD: Paginated
const users = await db.query("SELECT * FROM users LIMIT $1 OFFSET $2", [
  pageSize,
  page * pageSize,
]);
```

### Index Suggestions

```sql
-- If query pattern is:
SELECT * FROM orders WHERE user_id = ? AND status = ?

-- Suggest composite index:
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

## Memory Efficiency

### Memory Leaks

```typescript
// BAD: Event listener leak
class Component {
  init() {
    window.addEventListener("resize", this.handleResize);
  }
  // Missing cleanup!
}

// GOOD: Proper cleanup
class Component {
  init() {
    window.addEventListener("resize", this.handleResize);
  }
  destroy() {
    window.removeEventListener("resize", this.handleResize);
  }
}
```

### Unnecessary Object Creation

```java
// BAD: Object creation in loop
for (int i = 0; i < 1000000; i++) {
    String result = new StringBuilder()
        .append("Item: ")
        .append(i)
        .toString();
}

// GOOD: Reuse builder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000000; i++) {
    sb.setLength(0);
    sb.append("Item: ").append(i);
    String result = sb.toString();
}
```

## I/O and Async

### Sequential vs Parallel

```typescript
// BAD: Sequential async calls
const user = await fetchUser(id);
const orders = await fetchOrders(id);
const payments = await fetchPayments(id);

// GOOD: Parallel when independent
const [user, orders, payments] = await Promise.all([
  fetchUser(id),
  fetchOrders(id),
  fetchPayments(id),
]);
```

### Missing Caching

```python
# BAD: Repeated expensive computation
def get_report(user_id):
    data = expensive_database_query(user_id)  # Called every time
    return process(data)

# GOOD: With caching
@lru_cache(maxsize=100)
def get_report(user_id):
    data = expensive_database_query(user_id)
    return process(data)
```

## Language-Specific

### JavaScript/TypeScript

| Pattern                | Issue          | Fix                          |
| ---------------------- | -------------- | ---------------------------- |
| Unnecessary re-renders | Missing memo   | React.memo, useMemo          |
| Large bundle           | Unused imports | Tree shaking, dynamic import |
| String concat in loop  | O(n²)          | Array.join()                 |
| forEach with await     | Sequential     | Promise.all with map         |

### Python

| Pattern                | Issue         | Fix                     |
| ---------------------- | ------------- | ----------------------- |
| List append in loop    | Memory growth | Generator               |
| String concat          | O(n²)         | ''.join()               |
| Global variable access | Slow lookup   | Local variable          |
| Multiple isinstance    | Slow          | Match statement (3.10+) |

### Go

| Pattern          | Issue                 | Fix                 |
| ---------------- | --------------------- | ------------------- |
| Goroutine leak   | Unbounded creation    | Worker pool         |
| Channel deadlock | Blocking send/receive | Select with timeout |
| String concat    | O(n²)                 | strings.Builder     |
| Defer in loop    | Resource accumulation | Extract to function |

## Performance Severity Guide

| Finding                                 | Severity |
| --------------------------------------- | -------- |
| O(n²) or worse in hot path              | High     |
| N+1 database queries                    | High     |
| Memory leak                             | High     |
| Unbounded data fetch                    | Medium   |
| Missing pagination                      | Medium   |
| Suboptimal data structure               | Medium   |
| Sequential async when parallel possible | Low      |
| Minor optimization opportunity          | Low      |
