"""
MCP Tool for completing tasks in the todo list
"""
from typing import Dict, Any
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Complete a task in the user's todo list

    Args:
        user_id: The ID of the user owning the task
        task_id: The ID of the task to complete

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

        # In a real implementation, we would:
        # 1. Connect to the backend API or database
        # 2. Update the task record to set completed = True
        # 3. Return the updated task

        # Placeholder response
        result = {
            "success": True,
            "task": {
                "id": task_id,
                "user_id": user_id,
                "title": "Sample task to complete",  # In reality, this would come from the database
                "description": "Sample task description",
                "completed": True,
                "updated_at": "2026-02-06T12:00:00Z"
            },
            "message": f"Task {task_id} has been marked as completed"
        }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to complete task: {str(e)}"
        }


# If this script is run directly, it can be used for testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        result = complete_task(sys.argv[1], int(sys.argv[2]))
        print(json.dumps(result))
    else:
        print("Usage: python complete_task.py <user_id> <task_id>")