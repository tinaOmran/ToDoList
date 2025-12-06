"""Service layer providing high-level operations for tasks."""

from typing import List, Optional
from sqlalchemy.orm import Session

from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository
from exceptions.service_exceptions import TaskNotFoundError, ProjectNotFoundError


class TaskService:
    """Provides business logic for managing tasks."""

    def __init__(self, session: Session):
        """Initialize the service with a repository."""
        self.task_repo = TaskRepository(session)
        self.project_repo = ProjectRepository(session)

    def create_task(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ):
        """Add a new task to a project."""
        return self.task_repo.create(project_id, title, description, status, deadline)

    def list_tasks(self, project_id: int) -> List:
        """List all tasks for a given project.

        Args:
            project_id (int): The ID of the parent project.
        """
        # Verify project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        return self.task_repo.get_by_project_id(project_id)

    def change_task_status(self, project_id: int, task_id: int, new_status: str):
        """Change the status of a specific task."""
        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}")

        return self.task_repo.change_status(task_id, new_status)

    def delete_task(self, project_id: int, task_id: int) -> str:
        """Remove a task from a project."""
        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}")

        self.task_repo.delete(task_id)
        return f"Task {task_id} deleted successfully"

    def update_task(
        self,
        project_id: int,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ):
        """Update an existing task."""
        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}")

        return self.task_repo.update(task_id, title, description, status, deadline)


    def get_task(self, project_id: int, task_id: int):
        """Get a specific task by ID within a project."""

        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")

        task = self.task_repo.get_by_id(task_id)
        if not task or task.project_id != project_id:
            raise TaskNotFoundError(f"Task with ID {task_id} not found in project {project_id}")
        return task