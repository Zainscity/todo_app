"""
MCP Tool for deleting tasks from the todo list
"""
from typing import Dict, Any
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def delete_task(user_id: str, task_id: int = None, task_title: str = None) -> Dict[str, Any]:
    """
    Delete a task from the user's todo list

    Args:
        user_id: The ID of the user owning the task
        task_id: The ID of the task to delete (optional)
        task_title: The title of the task to delete (optional)

    Returns:
        Dict containing the result of the operation
    """
    try:
        # This is a placeholder implementation
        # In a real system, this would connect to the database
        # through an API or direct database connection

        # Placeholder for tasks (copied from list_tasks.py for consistency)
        sample_tasks = [
            {
                "id": 1,
                "user_id": user_id,
                "title": "Sample task",
                "description": "This is a sample task for demonstration",
                "completed": False,
                "created_at": "2026-02-06T10:00:00Z",
                "updated_at": "2026-02-06T10:00:00Z"
            },
            {
                "id": 2,
                "user_id": user_id,
                "title": "Another sample task",
                "description": "This is another sample task",
                "completed": True,
                "created_at": "2026-02-06T11:00:00Z",
                "updated_at": "2026-02-06T11:30:00Z"
            }
        ]

        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "user_id is required"
            }

        if task_id is None and task_title is None:
            return {
                "success": False,
                "error": "Either task_id or task_title is required"
            }

        resolved_task_id = task_id
        if task_title is not None and resolved_task_id is None:
            # Try to find task_id by title
            found_tasks = [task for task in sample_tasks if task["user_id"] == user_id and task["title"].lower() == task_title.lower()]
            if not found_tasks:
                return {
                    "success": False,
                    "error": f"No task found with title '{task_title}' for user '{user_id}'"
                }
            if len(found_tasks) > 1:
                return {
                    "success": False,
                    "error": f"Multiple tasks found with title '{task_title}'. Please provide task_id."
                }
            resolved_task_id = found_tasks[0]["id"]

        if resolved_task_id is None or resolved_task_id < 1:
            return {
                "success": False,
                "error": "A valid task_id is required"
            }

        # In a real implementation, we would:
        # 1. Connect to the backend API or database
        # 2. Delete the task record
        # 3. Confirm deletion

        # Placeholder response
        result = {
            "success": True,
            "deleted_task_id": resolved_task_id,
            "message": f"Task {resolved_task_id} has been deleted successfully"
        }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete task: {str(e)}"
        }


# If this script is run directly, it can be used for testing
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Delete a task from the user's todo list.")
    parser.add_argument("user_id", help="The ID of the user owning the task")
    parser.add_argument("--task_id", type=int, help="The ID of the task to delete")
    parser.add_argument("--task_title", type=str, help="The title of the task to delete")

    args = parser.parse_args()

    if args.user_id:
        result = delete_task(user_id=args.user_id, task_id=args.task_id, task_title=args.task_title)
        print(json.dumps(result))
    else:
        parser.print_help()