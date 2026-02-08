"""
CLI Interface Module

This module provides the command-line interface for interacting with the todo application.
"""
import sys
from typing import List
from pathlib import Path

# Import using relative path structure when running as a module
try:
    from ..services.task_manager import TaskManager
    from ..models.task import Task
    from .formatter import format_task_list, format_single_task, format_task_confirmation
except ImportError:
    # Fallback for direct execution
    src_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(src_dir))
    from services.task_manager import TaskManager
    from models.task import Task
    from cli.formatter import format_task_list, format_single_task, format_task_confirmation


class CLIInterface:
    """Handles command-line interface for the todo application."""

    def __init__(self):
        """Initialize the CLI interface with a task manager."""
        self.task_manager = TaskManager()

    def run_interactive(self):
        """Run the interactive mode of the application."""
        print("Welcome to the Todo App!")
        print("Commands: add, view, update, delete, complete, incomplete, help, quit")

        while True:
            try:
                command_input = input("\nEnter command: ").strip()
                if not command_input:
                    continue

                parts = command_input.split()
                command = parts[0].lower()

                if command == "quit" or command == "exit":
                    print("Goodbye!")
                    break
                elif command == "help":
                    self.show_help()
                else:
                    # Parse the rest of the input as arguments for the command
                    args = parts[1:] if len(parts) > 1 else []
                    self.execute_command(command, args)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def handle_command_line_args(self, args: List[str]):
        """Handle command-line arguments when running in non-interactive mode."""
        if len(args) == 0:
            print("Usage: python todo_app.py [command] [arguments]")
            print("Use 'python todo_app.py help' for more information")
            return

        command = args[0].lower()
        command_args = args[1:]

        if command == "help":
            self.show_help()
        else:
            self.execute_command(command, command_args)

    def execute_command(self, command: str, args: List[str]):
        """Execute a specific command with its arguments."""
        try:
            if command == "add":
                self.cmd_add(args)
            elif command == "view" or command == "list":
                self.cmd_view()
            elif command == "update":
                self.cmd_update(args)
            elif command == "delete":
                self.cmd_delete(args)
            elif command == "complete":
                self.cmd_complete(args)
            elif command == "incomplete":
                self.cmd_incomplete(args)
            elif command == "help":
                self.show_help()
            else:
                print(f"Unknown command: {command}")
                print("Use 'help' for available commands")
        except Exception as e:
            print(f"Error executing command '{command}': {e}")

    def cmd_add(self, args: List[str]):
        """Command to add a new task."""
        if len(args) < 1:
            print("Usage: add \"task title\" [\"optional description\"]")
            return

        title = args[0].strip('"')
        description = args[1].strip('"') if len(args) > 1 else None

        try:
            task = self.task_manager.add_task(title, description)
            print(format_task_confirmation(task, "added"))
        except ValueError as e:
            print(f"Error: {e}")

    def cmd_view(self):
        """Command to view all tasks."""
        tasks = self.task_manager.get_all_tasks()
        formatted_output = format_task_list(tasks)
        print(formatted_output)

    def cmd_update(self, args: List[str]):
        """Command to update a task."""
        if len(args) < 2:
            print("Usage: update <id> \"new title\" [\"new description\"]")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        title = args[1].strip('"') if len(args) > 1 else None
        description = args[2].strip('"') if len(args) > 2 else None

        if self.task_manager.update_task(task_id, title, description):
            task = self.task_manager.get_task_by_id(task_id)
            if task:
                print(format_task_confirmation(task, "updated"))
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def cmd_delete(self, args: List[str]):
        """Command to delete a task."""
        if len(args) < 1:
            print("Usage: delete <id>")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} does not exist")
            return

        if self.task_manager.delete_task(task_id):
            print(f"Task deleted successfully!")
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
        else:
            print(f"Error: Could not delete task with ID {task_id}")

    def cmd_complete(self, args: List[str]):
        """Command to mark a task as complete."""
        if len(args) < 1:
            print("Usage: complete <id>")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        if self.task_manager.toggle_completion(task_id):
            task = self.task_manager.get_task_by_id(task_id)
            if task:
                print(f"Task marked as completed!")
                print(f"ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Status: {'Completed' if task.completed else 'Pending'} {'✓' if task.completed else '○'}")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def cmd_incomplete(self, args: List[str]):
        """Command to mark a task as incomplete."""
        if len(args) < 1:
            print("Usage: incomplete <id>")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: Task ID must be a number")
            return

        if self.task_manager.set_task_completed(task_id, False):
            task = self.task_manager.get_task_by_id(task_id)
            if task:
                print(f"Task marked as incomplete!")
                print(f"ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Status: {'Completed' if task.completed else 'Pending'} {'✓' if task.completed else '○'}")
        else:
            print(f"Error: Task with ID {task_id} does not exist")

    def show_help(self):
        """Display help information."""
        print("\nTodo App Help")
        print("=" * 40)
        print("Available commands:")
        print("  add \"title\" [\"description\"]   - Add a new task")
        print("  view / list                   - View all tasks")
        print("  update <id> \"title\" [\"desc\"]  - Update a task")
        print("  delete <id>                   - Delete a task")
        print("  complete <id>                 - Mark task as complete")
        print("  incomplete <id>               - Mark task as incomplete")
        print("  help                          - Show this help")
        print("  quit / exit                   - Exit the application")
        print("\nExamples:")
        print("  add \"Buy groceries\"")
        print("  add \"Buy groceries\" \"Milk, bread, eggs\"")
        print("  view")
        print("  complete 1")
        print("  update 1 \"Buy groceries and cook\"")