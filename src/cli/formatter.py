"""
Task Display Formatter

This module provides functions for formatting task display in the CLI interface.
"""
from typing import List
from models.task import Task


def format_task_list(tasks: List[Task]) -> str:
    """
    Format a list of tasks for display.

    Args:
        tasks: List of Task objects to format

    Returns:
        Formatted string representation of the tasks
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = ["All Tasks:"]
    for task in tasks:
        status_symbol = "✓" if task.completed else "○"
        description = task.description if task.description else "N/A"
        formatted_task = (
            f"ID: {task.id} | "
            f"Title: {task.title} | "
            f"Description: {description} | "
            f"Status: {'Completed' if task.completed else 'Pending'} {status_symbol}"
        )
        formatted_tasks.append(formatted_task)

    return "\n".join(formatted_tasks)


def format_single_task(task: Task) -> str:
    """
    Format a single task for display.

    Args:
        task: Task object to format

    Returns:
        Formatted string representation of the task
    """
    status_symbol = "✓" if task.completed else "○"
    description = task.description if task.description else "N/A"

    return (
        f"ID: {task.id}\n"
        f"Title: {task.title}\n"
        f"Description: {description}\n"
        f"Status: {'Completed' if task.completed else 'Pending'} {status_symbol}"
    )


def format_task_confirmation(task: Task, action: str) -> str:
    """
    Format a task confirmation message.

    Args:
        task: Task object to format
        action: Action that was performed

    Returns:
        Formatted confirmation message
    """
    status_symbol = "✓" if task.completed else "○"

    return (
        f"Task {action} successfully!\n"
        f"ID: {task.id}\n"
        f"Title: {task.title}\n"
        f"Description: {task.description or 'N/A'}\n"
        f"Status: {'Completed' if task.completed else 'Pending'} {status_symbol}"
    )