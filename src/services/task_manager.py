"""
Task Manager Service

This service manages the in-memory storage and operations for tasks.
"""
from typing import List, Optional

# Import using relative path structure when running as a module
try:
    from ..models.task import Task
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    src_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(src_dir))
    from models.task import Task


class TaskManager:
    """Manages the collection of tasks in memory."""

    def __init__(self):
        """Initialize the task manager with an empty list of tasks."""
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task to the collection.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty
        """
        task = Task(
            task_id=self._get_next_id(),
            title=title,
            description=description,
            completed=False
        )
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            List of all Task objects
        """
        return self._tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if the task was updated, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.update_details(title=title, description=description)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            return True
        return False

    def toggle_completion(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task status was toggled, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.toggle_completion()
            return True
        return False

    def set_task_completed(self, task_id: int, completed: bool) -> bool:
        """
        Set the completion status of a task.

        Args:
            task_id: The ID of the task to update
            completed: The new completion status

        Returns:
            True if the task status was updated, False if the task was not found
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = completed
            return True
        return False

    def _get_next_id(self) -> int:
        """Get the next available task ID."""
        current_id = self._next_id
        self._next_id += 1
        return current_id