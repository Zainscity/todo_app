# Data Model

## Entity Definitions

### User Entity
- **Managed by**: Better Auth
- **Fields**:
  - `id` (UUID): Unique identifier for the user
  - `email` (VARCHAR(255)): User's email address (unique)
  - `email_verified` (BOOLEAN): Whether the email has been verified
  - `phone` (VARCHAR(20)): Optional phone number
  - `phone_verified` (BOOLEAN): Whether the phone has been verified
  - `name` (VARCHAR(255)): User's display name
  - `image_url` (TEXT): URL to user's profile image
  - `created_at` (TIMESTAMP WITH TIME ZONE): Account creation timestamp
  - `updated_at` (TIMESTAMP WITH TIME ZONE): Last update timestamp

### Task Entity
- **Managed by**: Application backend
- **Fields**:
  - `id` (UUID): Auto-generated unique identifier for the task
  - `user_id` (UUID): Foreign key linking to the user who owns the task
  - `title` (VARCHAR(100)): Task title (required, 1-100 characters)
  - `description` (TEXT): Optional task description (max 500 characters)
  - `completed` (BOOLEAN): Completion status (default: false)
  - `created_at` (TIMESTAMP WITH TIME ZONE): Task creation timestamp (required)
  - `updated_at` (TIMESTAMP WITH TIME ZONE): Last update timestamp (required)

## Relationships

### User → Task (One-to-Many)
- A user can own multiple tasks
- Foreign key constraint: `tasks.user_id` → `users.id`
- Cascade delete: When a user is deleted, all their tasks are automatically removed
- Each task belongs to exactly one user

## Validation Rules

### User Validation
- Email format must be valid
- Email must be unique across all users
- Name, if provided, should be 1-255 characters

### Task Validation
- Title is required and must be 1-100 characters
- Description, if provided, must be 0-500 characters
- User ID must reference an existing user
- Completed status must be a boolean value
- Timestamps are automatically managed by the system

## State Transitions

### Task State Transitions
- **Pending** (completed: false) ↔ **Completed** (completed: true)
  - Transition triggered by PATCH /api/{user_id}/tasks/{id}/complete
  - Both directions supported (can mark complete/incomplete)

## Indexing Strategy

### Primary Indexes
- `users.id`: Primary key index for user identification
- `tasks.id`: Primary key index for task identification

### Secondary Indexes
- `users.email`: B-tree index for efficient email lookups during authentication
- `tasks.user_id`: B-tree index for efficient user-based task queries
- `tasks.created_at`: B-tree index for chronological sorting and filtering
- `tasks.completed`: B-tree index for filtering by completion status

### Composite Indexes
- `(user_id, completed)`: Combined index for efficient queries filtering tasks by user and status
- `(user_id, created_at)`: Combined index for chronological task retrieval per user