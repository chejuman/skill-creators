# Architecture Patterns Reference

Database architecture and infrastructure optimization patterns.

## Connection Pooling

### PgBouncer Configuration

```ini
# /etc/pgbouncer/pgbouncer.ini

[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Pool settings
pool_mode = transaction          # session|transaction|statement
max_client_conn = 1000          # Max connections from clients
default_pool_size = 20          # Connections per database/user
min_pool_size = 5               # Minimum idle connections
reserve_pool_size = 5           # Extra for peak
reserve_pool_timeout = 3        # Wait time for reserve

# Timeouts
server_idle_timeout = 600       # Close idle server connections
client_idle_timeout = 0         # 0 = disabled
query_timeout = 0               # 0 = disabled
client_login_timeout = 60

# Logging
log_connections = 0
log_disconnections = 0
log_pooler_errors = 1
stats_period = 60
```

### Pool Modes

| Mode        | Best For                       | Caveats                 |
| ----------- | ------------------------------ | ----------------------- |
| session     | Long transactions, TEMP tables | Most connections needed |
| transaction | Web apps, short queries        | No session state        |
| statement   | Simple queries only            | No transactions         |

### SQLAlchemy Pool Settings

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool

# Production configuration
engine = create_engine(
    "postgresql://user:pass@localhost/db",

    # Pool type
    poolclass=QueuePool,

    # Connection limits
    pool_size=10,           # Base pool size
    max_overflow=20,        # Extra connections when busy
    pool_timeout=30,        # Wait time for connection
    pool_recycle=1800,      # Refresh connections every 30min
    pool_pre_ping=True,     # Health check before use

    # Connection settings
    connect_args={
        "connect_timeout": 10,
        "application_name": "myapp",
        "options": "-c statement_timeout=30000"
    }
)

# For serverless (Lambda, Cloud Functions)
# Use NullPool to avoid connection leaks
engine = create_engine(
    "postgresql://...",
    poolclass=NullPool  # New connection per request
)
```

## Read Replicas

### Read-Write Splitting

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Create engines
primary = create_engine("postgresql://user:pass@primary:5432/db")
replica = create_engine("postgresql://user:pass@replica:5432/db")

class RoutingSession(Session):
    """Route reads to replica, writes to primary."""

    def get_bind(self, mapper=None, clause=None):
        if self._flushing or self._is_clean():
            return replica
        return primary

# Usage
session = RoutingSession(bind=primary)
# Reads go to replica, writes go to primary
```

### Async with Read Replicas

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import random

primary = create_async_engine("postgresql+asyncpg://...@primary/db")
replicas = [
    create_async_engine("postgresql+asyncpg://...@replica1/db"),
    create_async_engine("postgresql+asyncpg://...@replica2/db"),
]

async def get_read_session() -> AsyncSession:
    """Get session for read operations."""
    engine = random.choice(replicas)  # Simple round-robin
    async with AsyncSession(engine) as session:
        yield session

async def get_write_session() -> AsyncSession:
    """Get session for write operations."""
    async with AsyncSession(primary) as session:
        yield session
```

### Replication Lag Handling

```python
import asyncio
from datetime import datetime, timedelta

async def wait_for_replication(session, max_wait=5.0):
    """Wait for replica to catch up after write."""
    # Get primary LSN
    primary_lsn = await primary_session.execute(
        text("SELECT pg_current_wal_lsn()")
    )

    start = datetime.now()
    while datetime.now() - start < timedelta(seconds=max_wait):
        replica_lsn = await session.execute(
            text("SELECT pg_last_wal_replay_lsn()")
        )
        if replica_lsn >= primary_lsn:
            return True
        await asyncio.sleep(0.1)

    return False  # Timeout
```

## Denormalization

### Materialized Views

```sql
-- Create materialized view for dashboard
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
    date_trunc('day', created_at) as day,
    COUNT(*) as order_count,
    SUM(total) as revenue,
    AVG(total) as avg_order_value
FROM orders
WHERE status = 'completed'
GROUP BY 1
WITH DATA;

-- Create index on materialized view
CREATE UNIQUE INDEX ON daily_sales_summary (day);

-- Refresh (blocking)
REFRESH MATERIALIZED VIEW daily_sales_summary;

-- Refresh (non-blocking, requires unique index)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary;

-- Auto-refresh with pg_cron
SELECT cron.schedule(
    'refresh-sales-summary',
    '0 * * * *',  -- Every hour
    'REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales_summary'
);
```

### Computed Columns (Generated)

```sql
-- PostgreSQL 12+ generated columns
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    subtotal NUMERIC,
    tax_rate NUMERIC DEFAULT 0.1,
    -- Stored generated column
    total NUMERIC GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) STORED
);

-- Virtual computed in SQLAlchemy
from sqlalchemy import Column, Numeric, Computed

class Order(Base):
    subtotal = Column(Numeric)
    tax_rate = Column(Numeric, default=0.1)
    total = Column(Numeric, Computed('subtotal * (1 + tax_rate)'))
```

### JSON Denormalization

```sql
-- Store aggregated data in JSONB
ALTER TABLE users ADD COLUMN stats JSONB DEFAULT '{}';

-- Update with aggregated data
UPDATE users SET stats = (
    SELECT jsonb_build_object(
        'order_count', COUNT(*),
        'total_spent', COALESCE(SUM(total), 0),
        'last_order', MAX(created_at)
    )
    FROM orders WHERE user_id = users.id
);

-- Query denormalized data
SELECT * FROM users
WHERE (stats->>'total_spent')::numeric > 1000;

-- Create GIN index for fast JSONB queries
CREATE INDEX idx_users_stats ON users USING GIN (stats);
```

## Cloud-Native Scaling (2025)

### Serverless PostgreSQL

```python
# Neon PostgreSQL - scales to zero
DATABASE_URL = "postgresql://user:pass@project.neon.tech/db?sslmode=require"

# Aurora Serverless v2
DATABASE_URL = "postgresql://user:pass@cluster.cluster-xxx.region.rds.amazonaws.com/db"

# AlloyDB (Google Cloud)
DATABASE_URL = "postgresql://user:pass@10.0.0.1:5432/db"
```

### Auto-scaling Configuration

```python
# SQLAlchemy with auto-reconnect for serverless
engine = create_engine(
    SERVERLESS_DATABASE_URL,
    pool_pre_ping=True,        # Reconnect stale connections
    pool_recycle=300,          # Recycle every 5 min
    pool_size=1,               # Minimal pool for serverless
    max_overflow=4,            # Allow burst
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)
```

### AI-Powered Optimization (2025)

```python
# Example: Using AI for index recommendations
# Many cloud providers now offer this

# AWS RDS Performance Insights
# - Automatic index recommendations
# - Query optimization suggestions

# Google AlloyDB
# - AI-driven query optimization
# - Automatic index management

# Azure Database for PostgreSQL
# - Intelligent Performance recommendations
# - Automatic tuning
```

## Caching Strategies

### Application-Level Cache

```python
from functools import lru_cache
import redis

redis_client = redis.Redis()

def get_user_cached(user_id: int) -> dict:
    """Cache user data in Redis."""
    cache_key = f"user:{user_id}"

    # Try cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Query database
    with Session() as session:
        user = session.get(User, user_id)
        data = user.to_dict()

    # Store in cache
    redis_client.setex(cache_key, 300, json.dumps(data))  # 5 min TTL
    return data

# Cache invalidation on update
def update_user(user_id: int, data: dict):
    with Session() as session:
        user = session.get(User, user_id)
        for key, value in data.items():
            setattr(user, key, value)
        session.commit()

    # Invalidate cache
    redis_client.delete(f"user:{user_id}")
```

### Query Result Cache

```python
from dogpile.cache import make_region

# Configure cache region
cache = make_region().configure(
    'dogpile.cache.redis',
    arguments={
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'redis_expiration_time': 300,
    }
)

@cache.cache_on_arguments()
def get_active_users_count():
    """Cached query result."""
    with Session() as session:
        return session.query(User).filter(User.active == True).count()

# Invalidate when users change
def create_user(...):
    ...
    cache.invalidate(get_active_users_count)
```
