# Database Schema

## SQLModel-Based Schema Definition

### Users Table (Managed by Better Auth)
The users table is managed by Better Auth and contains user account information:

```sql
-- Managed by Better Auth
users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20),
    phone_verified BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
)
```

### Tasks Table
The tasks table stores todo items with relations to users:

```sql
tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
)
```

## Relations and Constraints

### Foreign Key Relationships
- `tasks.user_id` → `users.id` (CASCADE DELETE)
  - When a user is deleted, all their tasks are automatically removed
  - Prevents orphaned tasks in the database

### Primary Keys
- `users.id`: UUID primary key for user identification
- `tasks.id`: Auto-generated UUID primary key for task identification

### Unique Constraints
- `users.email`: Ensures email uniqueness across the system
- `tasks.id`: Unique identifier for each task

### Check Constraints
- `tasks.title`: Length constraint (1-100 characters)
- `tasks.description`: Length constraint (max 500 characters)
- `tasks.completed`: Boolean value (true/false only)

## Indexing Strategy

### Primary Indexes
- `users.id`: Primary key index (automatically created)
- `tasks.id`: Primary key index (automatically created)

### Secondary Indexes
- `users.email`: B-tree index for efficient email lookups during authentication
- `tasks.user_id`: B-tree index for efficient user-based task queries
- `tasks.created_at`: B-tree index for chronological sorting and filtering
- `tasks.completed`: B-tree index for filtering by completion status

### Composite Indexes
- `(user_id, completed)`: Combined index for efficient queries filtering tasks by user and status
- `(user_id, created_at)`: Combined index for chronological task retrieval per user

## Data Integrity Rules

### Referential Integrity
- Foreign key constraints ensure tasks always reference valid users
- CASCADE DELETE maintains data consistency when users are removed
- Prevents insertion of tasks with non-existent user IDs

### Field Constraints
- `tasks.title`: NOT NULL to ensure every task has a title
- `tasks.completed`: NOT NULL with default FALSE to ensure consistent state
- `tasks.user_id`: NOT NULL to ensure every task belongs to a user
- Timestamps: NOT NULL with default values to track creation/modification

### Data Validation
- Email format validation enforced at application level
- Title length validation (1-100 characters) to prevent oversized entries
- Description length validation (max 500 characters) to prevent oversized entries
- UUID format validation for ID fields to ensure proper identification

## Additional Database Considerations

### Connection Management
- Database connection string configured via environment variable
- Connection pooling managed by the application framework
- SSL encryption enabled for production environments

### Backup and Recovery
- Neon Serverless PostgreSQL provides automated backups
- Point-in-time recovery available for data restoration
- Regular backup schedules maintained according to business requirements

### Performance Optimization
- Query optimization through proper indexing strategy
- Connection pooling to minimize database connection overhead
- Prepared statements to prevent SQL injection and improve performance