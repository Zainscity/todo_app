# Quickstart Guide: Todo In-Memory Python Console App

## Prerequisites
- Python 3.13 or higher
- Command-line interface access

## Installation
1. Clone or download the application files
2. Navigate to the application directory
3. Ensure Python 3.13+ is installed and accessible

## Running the Application
```bash
python todo_app.py [command] [arguments]
```

## Basic Usage Examples

### Add a Task
```bash
python todo_app.py add "Buy groceries" "Milk, bread, eggs"
```

### View All Tasks
```bash
python todo_app.py view
```

### Update a Task
```bash
python todo_app.py update 1 "Buy groceries and cook dinner" "Milk, bread, eggs, chicken"
```

### Mark Task as Complete
```bash
python todo_app.py complete 1
```

### Delete a Task
```bash
python todo_app.py delete 1
```

## Available Commands
- `add` - Add a new task
- `view` or `list` - View all tasks
- `update` - Update a task
- `delete` - Delete a task
- `complete` - Mark task as complete
- `incomplete` - Mark task as incomplete
- `help` - Show help information

## Important Notes
- All data is stored in memory only and will be lost when the application closes
- Task IDs are auto-generated and unique within the current session
- Use quotes around titles and descriptions that contain spaces