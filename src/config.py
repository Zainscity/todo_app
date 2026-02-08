"""
Configuration Constants

This module contains configuration constants for the todo application.
"""

# Application settings
APP_NAME = "Todo In-Memory Python Console App"
APP_VERSION = "1.0.0"

# Task settings
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Display settings
DEFAULT_TASK_STATUS_SYMBOLS = {
    True: "✓",   # Completed
    False: "○"   # Pending
}

# Error messages
ERROR_MESSAGES = {
    "invalid_task_id": "Error: Task ID must be a positive number",
    "task_not_found": "Error: Task with ID {} does not exist",
    "empty_title": "Error: Task title cannot be empty",
    "invalid_command": "Error: Unknown command '{}'. Use 'help' for available commands"
}