# Mermaid Diagram Templates

Ready-to-use Mermaid diagrams for documentation.

## System Architecture

### Microservices Architecture

```mermaid
graph TB
    subgraph Clients
        Web[Web App]
        Mobile[Mobile App]
        CLI[CLI Tool]
    end

    subgraph Gateway
        LB[Load Balancer]
        API[API Gateway]
    end

    subgraph Services
        Auth[Auth Service]
        User[User Service]
        Order[Order Service]
        Notify[Notification Service]
    end

    subgraph Data
        UserDB[(User DB)]
        OrderDB[(Order DB)]
        Cache[(Redis)]
        Queue[Message Queue]
    end

    Web --> LB
    Mobile --> LB
    CLI --> LB
    LB --> API
    API --> Auth
    API --> User
    API --> Order
    User --> UserDB
    Order --> OrderDB
    Order --> Queue
    Queue --> Notify
    Auth --> Cache
```

### Monolith Architecture

```mermaid
graph TB
    subgraph Client
        Browser[Browser]
        API_Client[API Client]
    end

    subgraph Application
        Web[Web Server]
        Controllers[Controllers]
        Services[Services]
        Models[Models]
    end

    subgraph Infrastructure
        DB[(Database)]
        Cache[(Cache)]
        Storage[File Storage]
    end

    Browser --> Web
    API_Client --> Web
    Web --> Controllers
    Controllers --> Services
    Services --> Models
    Models --> DB
    Services --> Cache
    Services --> Storage
```

### Three-Tier Architecture

```mermaid
graph TB
    subgraph Presentation
        UI[User Interface]
    end

    subgraph Logic
        BL[Business Logic]
        API[API Layer]
    end

    subgraph Data
        DAL[Data Access Layer]
        DB[(Database)]
    end

    UI --> API
    API --> BL
    BL --> DAL
    DAL --> DB
```

## Sequence Diagrams

### Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as Client
    participant A as API
    participant Auth as Auth Service
    participant DB as Database

    U->>C: Enter credentials
    C->>A: POST /auth/login
    A->>Auth: Validate credentials
    Auth->>DB: Query user
    DB-->>Auth: User data
    Auth->>Auth: Generate JWT
    Auth-->>A: Token
    A-->>C: 200 OK + Token
    C->>C: Store token
    C-->>U: Login success
```

### API Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant G as API Gateway
    participant A as Auth
    participant S as Service
    participant D as Database
    participant Ca as Cache

    C->>G: Request + JWT
    G->>A: Validate token
    A-->>G: Valid
    G->>S: Forward request
    S->>Ca: Check cache
    alt Cache hit
        Ca-->>S: Cached data
    else Cache miss
        S->>D: Query database
        D-->>S: Data
        S->>Ca: Update cache
    end
    S-->>G: Response
    G-->>C: Response
```

### Error Handling Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant S as Service
    participant L as Logger
    participant M as Monitoring

    C->>A: Request
    A->>S: Process
    S->>S: Error occurs
    S->>L: Log error
    S->>M: Send metric
    S-->>A: Error response
    A-->>C: 500 Internal Error
```

## Entity Relationship Diagrams

### User Management Schema

```mermaid
erDiagram
    User ||--o{ Post : creates
    User ||--o{ Comment : writes
    User ||--o{ Like : gives
    User }|--|| Role : has
    Post ||--o{ Comment : has
    Post ||--o{ Like : receives
    Post ||--o{ Tag : tagged_with
    Tag }|--|{ Post : tags

    User {
        uuid id PK
        string email UK
        string password_hash
        string name
        enum status
        timestamp created_at
        timestamp updated_at
    }

    Role {
        uuid id PK
        string name UK
        json permissions
    }

    Post {
        uuid id PK
        uuid user_id FK
        string title
        text content
        enum status
        timestamp published_at
    }

    Comment {
        uuid id PK
        uuid user_id FK
        uuid post_id FK
        text content
        timestamp created_at
    }

    Like {
        uuid id PK
        uuid user_id FK
        uuid post_id FK
        timestamp created_at
    }

    Tag {
        uuid id PK
        string name UK
        string slug UK
    }
```

### E-commerce Schema

```mermaid
erDiagram
    Customer ||--o{ Order : places
    Order ||--|{ OrderItem : contains
    Product ||--o{ OrderItem : included_in
    Product }|--|| Category : belongs_to
    Customer ||--o{ Address : has

    Customer {
        uuid id PK
        string email UK
        string name
        string phone
    }

    Order {
        uuid id PK
        uuid customer_id FK
        decimal total
        enum status
        timestamp created_at
    }

    OrderItem {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        decimal price
    }

    Product {
        uuid id PK
        uuid category_id FK
        string name
        decimal price
        int stock
    }

    Category {
        uuid id PK
        string name
        uuid parent_id FK
    }

    Address {
        uuid id PK
        uuid customer_id FK
        string street
        string city
        string country
        string postal_code
    }
```

## Flowcharts

### CI/CD Pipeline

```mermaid
flowchart TD
    A[Push to GitHub] --> B{Branch?}
    B -->|main| C[Build Production]
    B -->|develop| D[Build Staging]
    B -->|feature/*| E[Build Preview]

    C --> F[Run Tests]
    D --> F
    E --> F

    F --> G{Tests Pass?}
    G -->|Yes| H[Build Docker Image]
    G -->|No| I[Notify Team]

    H --> J[Push to Registry]
    J --> K{Environment}
    K -->|Production| L[Deploy to Prod]
    K -->|Staging| M[Deploy to Staging]
    K -->|Preview| N[Deploy Preview]

    L --> O[Run Smoke Tests]
    M --> O
    N --> P[Generate Preview URL]

    O --> Q{Healthy?}
    Q -->|Yes| R[Complete]
    Q -->|No| S[Rollback]
```

### User Registration Flow

```mermaid
flowchart TD
    A[Start] --> B[Enter Email]
    B --> C{Valid Email?}
    C -->|No| B
    C -->|Yes| D{Email Exists?}
    D -->|Yes| E[Show Error]
    E --> B
    D -->|No| F[Enter Password]
    F --> G{Strong Password?}
    G -->|No| F
    G -->|Yes| H[Create Account]
    H --> I[Send Verification Email]
    I --> J[Show Success]
    J --> K[End]
```

### Error Handling Decision Tree

```mermaid
flowchart TD
    A[Error Occurred] --> B{Error Type?}
    B -->|Validation| C[Return 400]
    B -->|Auth| D[Return 401/403]
    B -->|NotFound| E[Return 404]
    B -->|Server| F[Log Error]

    C --> G[Include Details]
    D --> H[Clear Token]
    E --> I[Suggest Alternatives]
    F --> J[Return 500]

    J --> K[Alert Team]
```

## State Diagrams

### Order Status

```mermaid
stateDiagram-v2
    [*] --> Pending: Order Created
    Pending --> Processing: Payment Confirmed
    Pending --> Cancelled: Customer Cancels
    Processing --> Shipped: Items Shipped
    Processing --> Cancelled: Refund Requested
    Shipped --> Delivered: Delivery Confirmed
    Shipped --> Returned: Return Requested
    Delivered --> Returned: Return Initiated
    Returned --> Refunded: Refund Processed
    Cancelled --> Refunded: Refund Processed
    Refunded --> [*]
    Delivered --> [*]
```

### User Account Status

```mermaid
stateDiagram-v2
    [*] --> Pending: Sign Up
    Pending --> Active: Email Verified
    Pending --> Expired: Verification Timeout
    Active --> Suspended: Violation Detected
    Active --> Inactive: No Activity 90 days
    Suspended --> Active: Appeal Approved
    Inactive --> Active: User Login
    Suspended --> Banned: Multiple Violations
    Banned --> [*]
```

## Class Diagrams

### Service Layer Pattern

```mermaid
classDiagram
    class Controller {
        -service: Service
        +handleRequest(req)
        +handleResponse(res)
    }

    class Service {
        -repository: Repository
        +create(data)
        +findById(id)
        +update(id, data)
        +delete(id)
    }

    class Repository {
        -db: Database
        +save(entity)
        +findOne(query)
        +findMany(query)
        +remove(entity)
    }

    class Entity {
        +id: string
        +createdAt: Date
        +updatedAt: Date
    }

    Controller --> Service
    Service --> Repository
    Repository --> Entity
```

## Gantt Charts

### Project Timeline

```mermaid
gantt
    title Project Development Timeline
    dateFormat  YYYY-MM-DD

    section Planning
    Requirements    :done, req, 2024-01-01, 7d
    Design          :done, des, after req, 7d

    section Development
    Backend API     :active, api, 2024-01-15, 14d
    Frontend UI     :ui, after api, 14d
    Integration     :int, after ui, 7d

    section Testing
    Unit Tests      :test1, 2024-01-22, 21d
    E2E Tests       :test2, after int, 7d

    section Deployment
    Staging         :stg, after test2, 3d
    Production      :prd, after stg, 2d
```

## Usage Tips

1. **Keep diagrams simple** - Max 15-20 nodes per diagram
2. **Use meaningful labels** - Short but descriptive
3. **Group related items** - Use subgraphs/containers
4. **Consistent direction** - TB (top-bottom) or LR (left-right)
5. **Color sparingly** - Only for emphasis
