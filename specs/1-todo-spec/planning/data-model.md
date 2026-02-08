# Data Model: Todo In-Memory Python Console App

## Task Entity

### Attributes
- **id**: Integer (required, unique, auto-generated)
  - Auto-incrementing identifier starting from 1
  - Primary key for the task
  - Cannot be modified after creation

- **title**: String (required, non-empty)
  - Task title/description in short form
  - Must be at least 1 character long
  - Validation: Non-empty string

- **description**: String (optional, nullable)
  - Extended task description
  - Can be empty or null
  - No specific length restrictions (within reasonable limits)

- **completed**: Boolean (required, default: False)
  - Task completion status
  - True = completed, False = pending
  - Default value is False when task is created

### Validation Rules
1. **Title Validation**:
   - Cannot be null or empty
   - Must contain at least one non-whitespace character

2. **ID Validation**:
   - Must be a positive integer
   - Must be unique within the application session
   - Cannot be modified after task creation

3. **Completion Status**:
   - Must be a boolean value (True/False)
   - Default is False when creating new tasks

### State Transitions
- **Initial State**: When created, task has `completed=False`
- **Complete Transition**: Task moves from `completed=False` to `completed=True`
- **Incomplete Transition**: Task moves from `completed=True` to `completed=False`

## Task Collection (In-Memory Storage)

### Structure
- **Type**: List/Array of Task objects
- **Access**: Via TaskManager service
- **Persistence**: Exists only during application runtime

### Operations
1. **Create**: Add new Task object to collection
2. **Read**: Retrieve Task by ID or all Tasks
3. **Update**: Modify Task attributes (title, description)
4. **Delete**: Remove Task from collection
5. **Toggle**: Change completion status

### Constraints
- All IDs must be unique within the collection
- No persistent storage outside of application memory
- Collection resets when application terminates