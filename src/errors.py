"""
Error Handling Module

This module defines custom exception classes for the todo application.
"""


class TodoAppError(Exception):
    """Base exception class for the todo application."""
    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task with a specific ID is not found."""
    pass


class InvalidTaskError(TodoAppError):
    """Raised when a task is invalid (e.g., empty title)."""
    pass


class InvalidTaskIdError(TodoAppError):
    """Raised when a task ID is invalid (e.g., negative number)."""
    pass