# CLI Contract: Todo In-Memory Python Console App

## Command Structure
```
python todo_app.py [command] [arguments]
```

## Commands

### 1. Add Task
**Command**: `add`
**Arguments**:
- `title` (required): Task title in quotes
- `description` (optional): Task description in quotes

**Usage Examples**:
```
python todo_app.py add "Buy groceries"
python todo_app.py add "Buy groceries" "Milk, bread, eggs"
```

**Expected Behavior**:
- Creates a new task with provided title and description
- Auto-generates unique ID
- Sets completion status to False (incomplete)
- Displays confirmation with new task details

**Success Response**:
```
Task added successfully!
ID: 1
Title: Buy groceries
Description: Milk, bread, eggs
Status: Pending
```

**Error Responses**:
- Missing title: "Error: Title is required to add a task"
- Invalid input: "Error: Unable to add task"

### 2. View Tasks
**Command**: `view` or `list`
**Arguments**: None

**Usage Examples**:
```
python todo_app.py view
python todo_app.py list
```

**Expected Behavior**:
- Displays all tasks with ID, title, description, and status
- Shows "No tasks found" if no tasks exist

**Success Response**:
```
All Tasks:
ID: 1 | Title: Buy groceries | Description: Milk, bread, eggs | Status: Pending
ID: 2 | Title: Walk the dog | Description:  | Status: Completed ✓
```

**Error Responses**:
- No tasks: "No tasks found."

### 3. Update Task
**Command**: `update`
**Arguments**:
- `id` (required): Task ID to update
- `title` (optional): New title in quotes
- `description` (optional): New description in quotes

**Usage Examples**:
```
python todo_app.py update 1 "Buy groceries and cook dinner"
python todo_app.py update 1 "Buy groceries and cook dinner" "Milk, bread, eggs, chicken"
```

**Expected Behavior**:
- Updates specified task with provided title and/or description
- Preserves existing values if not specified
- Validates that task exists before updating

**Success Response**:
```
Task updated successfully!
ID: 1
Title: Buy groceries and cook dinner
Description: Milk, bread, eggs, chicken
Status: Pending
```

**Error Responses**:
- Invalid ID: "Error: Task with ID X does not exist"
- Missing ID: "Error: Task ID is required to update a task"

### 4. Delete Task
**Command**: `delete`
**Arguments**:
- `id` (required): Task ID to delete

**Usage Examples**:
```
python todo_app.py delete 1
```

**Expected Behavior**:
- Removes task with specified ID from the system
- Confirms deletion to user

**Success Response**:
```
Task deleted successfully!
ID: 1
Title: Buy groceries and cook dinner
```

**Error Responses**:
- Invalid ID: "Error: Task with ID X does not exist"
- Missing ID: "Error: Task ID is required to delete a task"

### 5. Mark Task Complete/Incomplete
**Commands**: `complete` or `incomplete`
**Arguments**:
- `id` (required): Task ID to update

**Usage Examples**:
```
python todo_app.py complete 1
python todo_app.py incomplete 1
```

**Expected Behavior**:
- Changes completion status of specified task
- Validates that task exists before updating
- `complete` command sets status to True
- `incomplete` command sets status to False

**Success Response**:
```
Task marked as completed!
ID: 1
Title: Buy groceries
Status: Completed ✓
```

**Error Responses**:
- Invalid ID: "Error: Task with ID X does not exist"
- Missing ID: "Error: Task ID is required to update task status"

## Common Error Responses

### General Errors
- Invalid command: "Error: Unknown command. Use: add, view, update, delete, complete, incomplete"
- Missing arguments: "Error: Insufficient arguments for command"
- Invalid ID format: "Error: Invalid task ID format. Please provide a numeric ID."

### Help Command
**Command**: `help` or `-h` or `--help`
**Behavior**: Displays help information with available commands