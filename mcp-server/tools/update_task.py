"""
MCP Tool for updating tasks in the todo list
"""
from typing import Dict, Any, Optional
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a task in the user's todo list

    Args:
        user_id: The ID of the user owning the task
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        Dict containing the result of the operation
    """
    try:
        # This is a placeholder implementation
        # In a real system, this would connect to the database
        # through an API or direct database connection

        # Validate inputs
        if not user_id or task_id is None or task_id < 1:
            return {
                "success": False,
                "error": "user_id and valid task_id are required"
            }

        # At least one field must be provided for update
        if title is None and description is None:
            return {
                "success": False,
                "error": "At least one field (title or description) must be provided for update"
            }

        # In a real implementation, we would:
        # 1. Connect to the backend API or database
        # 2. Update the task record with the provided fields
        # 3. Return the updated task

        # Placeholder response
        result = {
            "success": True,
            "task": {
                "id": task_id,
                "user_id": user_id,
                "title": title or "Existing title",  # In reality, this would preserve the existing value if not updated
                "description": description or "Existing description",  # Same here
                "completed": False,  # This would be preserved from existing task
                "updated_at": "2026-02-06T12:00:00Z"
            },
            "message": f"Task {task_id} has been updated successfully"
        }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update task: {str(e)}"
        }


# If this script is run directly, it can be used for testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        user_id = sys.argv[1]
        task_id = int(sys.argv[2])

        # Handle optional parameters properly
        title = None
        description = None

        if len(sys.argv) > 3:
            title = sys.argv[3] if sys.argv[3] != "" else None
        if len(sys.argv) > 4:
            description = sys.argv[4] if sys.argv[4] != "" else None

        result = update_task(user_id, task_id, title, description)
        print(json.dumps(result))
    else:
        print("Usage: python update_task.py <user_id> <task_id> [title] [description]")