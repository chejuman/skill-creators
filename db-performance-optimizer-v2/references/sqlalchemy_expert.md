# SQLAlchemy Expert Reference

Advanced SQLAlchemy 2.0 optimization patterns for high-performance applications.

## Eager Loading Strategies

### Joined Loading

Single query with LEFT OUTER JOIN. Best for one-to-one or small one-to-many.

```python
from sqlalchemy.orm import joinedload

# Load user with profile in single query
users = session.execute(
    select(User)
    .options(joinedload(User.profile))
    .where(User.active == True)
).scalars().all()

# Nested joined loading
users = session.execute(
    select(User)
    .options(
        joinedload(User.profile),
        joinedload(User.address)
    )
).scalars().all()
```

**Caution:** Avoid for large collections (cartesian product explosion)

### Selectin Loading

Separate IN query for related objects. Best for one-to-many.

```python
from sqlalchemy.orm import selectinload

# Load users with their orders (N+1 → 2 queries)
users = session.execute(
    select(User)
    .options(selectinload(User.orders))
).scalars().all()

# Nested loading
users = session.execute(
    select(User)
    .options(
        selectinload(User.orders)
        .selectinload(Order.items)
    )
).scalars().all()
```

### Subquery Loading

Separate subquery for collections. Good when filter conditions needed.

```python
from sqlalchemy.orm import subqueryload

# Subquery loading with filter
users = session.execute(
    select(User)
    .options(subqueryload(User.orders))
    .where(User.created_at > datetime.now() - timedelta(days=30))
).scalars().all()
```

### Load Strategy Comparison

| Strategy | Queries | Best For                  | Avoid When             |
| -------- | ------- | ------------------------- | ---------------------- |
| joined   | 1       | 1:1, small 1:N            | Large collections      |
| selectin | 2       | 1:N, M:N                  | Very large parent sets |
| subquery | 2       | 1:N with WHERE on parent  | Simple cases           |
| lazy     | N+1     | Rarely accessed relations | Loops                  |

## Bulk Operations

### Bulk Insert (Core)

```python
from sqlalchemy import insert

# 10-100x faster than ORM for bulk inserts
stmt = insert(User).values([
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    # ... thousands more
])
session.execute(stmt)
session.commit()

# With RETURNING (PostgreSQL)
stmt = insert(User).values([...]).returning(User.id)
result = session.execute(stmt)
new_ids = result.scalars().all()
```

### Bulk Insert Mappings

```python
# ORM-aware bulk insert
session.bulk_insert_mappings(User, [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
])
session.commit()
```

### Bulk Update

```python
from sqlalchemy import update

# Single UPDATE statement
stmt = (
    update(User)
    .where(User.status == "pending")
    .values(status="active", updated_at=func.now())
)
session.execute(stmt)
session.commit()

# Bulk update mappings
session.bulk_update_mappings(User, [
    {"id": 1, "status": "active"},
    {"id": 2, "status": "inactive"},
])
```

### Bulk Delete

```python
from sqlalchemy import delete

# Single DELETE statement
stmt = delete(User).where(User.last_login < datetime.now() - timedelta(days=365))
result = session.execute(stmt)
print(f"Deleted {result.rowcount} rows")
session.commit()
```

## Session Management

### Context Manager Pattern

```python
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

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

# Usage
with get_session() as session:
    user = session.get(User, 1)
    user.name = "Updated"
```

### Scoped Session (Web Apps)

```python
from sqlalchemy.orm import scoped_session, sessionmaker

# Thread-local session
Session = scoped_session(sessionmaker(bind=engine))

# In request handler
@app.route("/users")
def get_users():
    users = Session.query(User).all()
    Session.remove()  # Important: cleanup after request
    return users

# Or use Flask-SQLAlchemy which handles this
```

### Expire on Commit

```python
# Prevent stale data in long-running sessions
Session = sessionmaker(
    bind=engine,
    expire_on_commit=True  # Default, objects refreshed on next access
)

# For async: expire_on_commit=False often needed
async_session = sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
)
```

## Hybrid Attributes

Combine Python and SQL expressions for optimal filtering.

```python
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

class Order(Base):
    __tablename__ = "orders"

    subtotal = Column(Numeric)
    tax_rate = Column(Numeric, default=0.1)

    @hybrid_property
    def total(self):
        """Python-side calculation"""
        return self.subtotal * (1 + self.tax_rate)

    @total.expression
    def total(cls):
        """SQL-side expression for filtering"""
        return cls.subtotal * (1 + cls.tax_rate)

# Now works in both Python and SQL
order.total  # Python calculation
session.query(Order).filter(Order.total > 100)  # SQL filter

# Hybrid method with parameter
class User(Base):
    @hybrid_method
    def has_role(self, role_name):
        return role_name in [r.name for r in self.roles]

    @has_role.expression
    def has_role(cls, role_name):
        return cls.roles.any(Role.name == role_name)
```

## Connection Pooling

### Pool Configuration

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@localhost/db",

    # Pool settings
    poolclass=QueuePool,
    pool_size=10,           # Persistent connections
    max_overflow=20,        # Temporary overflow connections
    pool_timeout=30,        # Wait time for connection
    pool_recycle=1800,      # Recycle connections after 30 min
    pool_pre_ping=True,     # Verify connection before use

    # Performance settings
    echo=False,             # Disable SQL logging in production
    echo_pool=False,        # Disable pool logging
)
```

### Pool Events

```python
from sqlalchemy import event

@event.listens_for(engine, "connect")
def set_search_path(dbapi_conn, connection_record):
    """Set search path on new connections"""
    cursor = dbapi_conn.cursor()
    cursor.execute("SET search_path TO myschema, public")
    cursor.close()

@event.listens_for(engine, "checkout")
def ping_connection(dbapi_conn, connection_record, connection_proxy):
    """Verify connection is alive"""
    cursor = dbapi_conn.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        raise exc.DisconnectionError()
    finally:
        cursor.close()
```

## Async SQLAlchemy

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
)

# Async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
)

# Usage
async with async_session() as session:
    result = await session.execute(
        select(User)
        .options(selectinload(User.orders))
        .where(User.active == True)
    )
    users = result.scalars().all()
```

## Query Optimization Tips

```python
# 1. Use load_only for large tables
from sqlalchemy.orm import load_only

users = session.execute(
    select(User).options(load_only(User.id, User.name))
).scalars().all()

# 2. Use contains_eager for filtered relationships
from sqlalchemy.orm import contains_eager

orders = session.execute(
    select(User)
    .join(User.orders)
    .options(contains_eager(User.orders))
    .where(Order.status == "pending")
).scalars().all()

# 3. Use yield_per for streaming large results
for user in session.execute(select(User)).scalars().yield_per(1000):
    process(user)
```
