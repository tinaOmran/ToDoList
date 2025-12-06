"""Service layer providing high-level operations for projects."""

from __future__ import annotations

from typing import List, Optional
from sqlalchemy.orm import Session

from repositories.project_repository import ProjectRepository
from exceptions.service_exceptions import ProjectNotFoundError

class ProjectService:
    """Provides business logic for managing projects."""

    def __init__(self, session: Session):
        """Initialize the service with a repository."""
        self.project_repo = ProjectRepository(session)

    def create_project(self, name: str, description: str = ""):
        """Create a new project.

        Args:
            name (str): The project name (must be unique).
            description (str): Optional project description.
        """
        return self.project_repo.create(name, description)

    def list_projects(self) -> List:
        """Return all projects sorted by creation time."""
        return self.project_repo.get_all()

    def get_project(self, project_id: int):
        """Retrieve a specific project by ID."""
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        return project

    def update_project(self, project_id: int, name: Optional[str] = None, description: Optional[str] = None) :
        """Update an existing project's name or description.

        Args:
            project_id (int): The project ID.
            name (Optional[str]): New project name (must be unique).
            description (Optional[str]): New description.

        """
        return self.project_repo.update(project_id, name, description)

    def delete_project(self, project_id: int) -> str:
        """Delete a project and its associated tasks."""
        self.project_repo.delete(project_id)
        return f"Project {project_id} deleted successfully"