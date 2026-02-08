# Agent Context: Todo App Implementation

## Project Specific Information

### Application Type
- Console-based Python application
- In-memory data storage only
- No persistence beyond runtime

### Architecture
- Clean architecture with separation of concerns
- Three-layer structure:
  1. Models: Task entity with validation
  2. Services: TaskManager with CRUD operations
  3. CLI Interface: Command parsing and user interaction

### Data Model
- Task entity with id (int), title (str), description (str, optional), completed (bool)
- In-memory storage using Python list of Task objects
- Auto-generated unique IDs

### CLI Commands
- add: Create new tasks
- view/list: Display all tasks
- update: Modify task title/description
- delete: Remove tasks
- complete/incomplete: Toggle completion status

### Error Handling
- Validate input before processing
- Handle invalid task IDs gracefully
- Provide user-friendly error messages
- Follow constitution principle of graceful error handling