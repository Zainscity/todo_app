"""
MCP Tool for listing tasks from the todo list
"""
from typing import Dict, Any, List
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def list_tasks(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    List tasks for a user

    Args:
        user_id: The ID of the user whose tasks to list
        status: The status of tasks to return ('all', 'pending', 'completed')

    Returns:
        Dict containing the list of tasks
    """
    try:
        # This is a placeholder implementation
        # In a real system, this would connect to the database
        # through an API or direct database connection

        # Validate inputs
        if not user_id:
            return {
                "success": False,
                "error": "user_id is required"
            }

        # Validate status parameter
        valid_statuses = ["all", "pending", "completed"]
        if status not in valid_statuses:
            status = "all"

        # In a real implementation, we would:
        # 1. Connect to the backend API or database
        # 2. Query the task records for the specified user and status
        # 3. Return the matching tasks

        # Placeholder response
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

        # Filter by status if needed
        if status != "all":
            if status == "pending":
                filtered_tasks = [task for task in sample_tasks if not task["completed"]]
            elif status == "completed":
                filtered_tasks = [task for task in sample_tasks if task["completed"]]
            else:
                filtered_tasks = []
        else:
            filtered_tasks = sample_tasks

        result = {
            "success": True,
            "tasks": filtered_tasks,
            "count": len(filtered_tasks),
            "status_filter": status
        }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list tasks: {str(e)}"
        }


# If this script is run directly, it can be used for testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        result = list_tasks(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "all")
        print(json.dumps(result))
    else:
        print("Usage: python list_tasks.py <user_id> [status]")