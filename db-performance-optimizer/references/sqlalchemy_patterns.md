# SQLAlchemy Performance Patterns

Quick reference for common SQLAlchemy optimization patterns.

## Loading Strategies

### Lazy Loading (Default)

```python
# Relationship definition
class User(Base):
    orders = relationship("Order", lazy="select")  # Default

# Problem: Each access triggers a query
for user in session.query(User).all():
    print(user.orders)  # N+1 problem!
```

### Joined Loading

```python
from sqlalchemy.orm import joinedload

# Best for: One-to-one, small one-to-many
users = session.query(User)\
    .options(joinedload(User.profile))\
    .all()

# Or set in relationship
class User(Base):
    profile = relationship("Profile", lazy="joined")
```

### Subquery Loading

```python
from sqlalchemy.orm import subqueryload

# Best for: Large collections where you need all items
users = session.query(User)\
    .options(subqueryload(User.orders))\
    .all()
```

### Selectin Loading (Recommended for SQLAlchemy 1.4+)

```python
from sqlalchemy.orm import selectinload

# Best for: Most one-to-many relationships
users = session.query(User)\
    .options(selectinload(User.orders))\
    .all()

# Nested loading
users = session.query(User)\
    .options(
        selectinload(User.orders)
        .selectinload(Order.items)
    ).all()
```

## Column Loading

### Load Only Specific Columns

```python
from sqlalchemy.orm import load_only

# Exclude large columns
users = session.query(User)\
    .options(load_only(User.id, User.name))\
    .all()
```

### Defer Large Columns

```python
from sqlalchemy.orm import defer

# Defer loading of large columns
users = session.query(User)\
    .options(defer(User.bio), defer(User.avatar))\
    .all()
```

### Undefer on Demand

```python
from sqlalchemy.orm import undefer

# Explicitly load deferred column
user = session.query(User)\
    .options(undefer(User.bio))\
    .filter_by(id=1)\
    .first()
```

## Bulk Operations

### Bulk Insert (Core)

```python
from sqlalchemy import insert

# Much faster than ORM for large inserts
stmt = insert(User).values([
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
])
session.execute(stmt)
session.commit()
```

### Bulk Update (Core)

```python
from sqlalchemy import update

stmt = update(User)\
    .where(User.status == "pending")\
    .values(status="active")
session.execute(stmt)
session.commit()
```

### Bulk Delete (Core)

```python
from sqlalchemy import delete

stmt = delete(User).where(User.status == "deleted")
session.execute(stmt)
session.commit()
```

## Query Optimization

### Use exists() Instead of count()

```python
# BAD: Counts all matching rows
if session.query(User).filter_by(email=email).count() > 0:
    pass

# GOOD: Stops at first match
from sqlalchemy import exists
if session.query(exists().where(User.email == email)).scalar():
    pass
```

### Use first() Instead of all()[0]

```python
# BAD: Loads all rows then takes first
user = session.query(User).all()[0]

# GOOD: Limits to 1 row
user = session.query(User).first()
```

### Limit Results

```python
# Always paginate large result sets
users = session.query(User)\
    .order_by(User.created_at.desc())\
    .limit(20)\
    .offset(page * 20)\
    .all()
```

## Caching Patterns

### Query Result Caching

```python
from dogpile.cache import make_region

cache = make_region().configure('dogpile.cache.redis')

@cache.cache_on_arguments(expiration_time=300)
def get_user_by_id(user_id):
    return session.query(User).get(user_id)
```

### SQL Compilation Caching (Built-in)

```python
# SQLAlchemy 1.4+ automatically caches query compilation
# Enable baked queries for even better performance
from sqlalchemy.ext.baked import bakery

baked_query = bakery(lambda session: session.query(User))
result = baked_query(session).filter(User.id == 1).first()
```

## Async SQLAlchemy

### Async Engine Setup

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host/db",
    pool_size=20,
    max_overflow=10
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### Async Query Execution

```python
async with async_session() as session:
    result = await session.execute(
        select(User).options(selectinload(User.orders))
    )
    users = result.scalars().all()
```

## Connection Management

### Engine Configuration

```python
engine = create_engine(
    "postgresql://user:pass@host/db",
    pool_size=10,           # Max connections in pool
    max_overflow=20,        # Additional connections allowed
    pool_timeout=30,        # Wait time for connection
    pool_recycle=1800,      # Recycle connections after 30 min
    pool_pre_ping=True,     # Check connection validity
    echo=False,             # Set True for debugging
)
```

### Context Manager Pattern

```python
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

## Monitoring Queries

### Echo All Queries

```python
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

### Query Event Listener

```python
from sqlalchemy import event
import time

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if total > 0.1:  # Log slow queries (>100ms)
        print(f"Slow query ({total:.3f}s): {statement[:100]}")
```
