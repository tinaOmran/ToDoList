from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from models.project import Project
from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectNameExistsError,
    ProjectLimitExceededError,
)
from config import config


class ProjectRepository:
    """Repository class for Project database operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieve project by its ID."""
        return self.session.get(Project, project_id)

    def get_all(self) -> List[Project]:
        """Return list of all projects ordered by creation time."""
        stmt = select(Project).order_by(Project.created_at)
        return list(self.session.scalars(stmt))

    def get_by_name(self, name: str) -> Optional[Project]:
        """Return a project by its unique name."""
        stmt = select(Project).where(Project.name == name)
        return self.session.scalar(stmt)

    def get_project_count(self) -> int:
        """Return total number of stored projects."""
        stmt = select(func.count(Project.id))
        return self.session.scalar(stmt)

    def create(self, name: str, description: str = "") -> Project:
        """Create a new project with validation."""
        # Check project limit
        if self.get_project_count() >= config.MAX_NUMBER_OF_PROJECT:
            raise ProjectLimitExceededError("Max number of projects reached.")

        # Check unique name
        if self.get_by_name(name):
            raise ProjectNameExistsError(
                f"Project with name '{name}' already exists"
            )

        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

        return project

    def update(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        """Update project's name and/or description."""
        project = self.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found"
            )

        # Check unique name if changing name
        if name and name != project.name:
            existing = self.get_by_name(name)
            if existing:
                raise ProjectNameExistsError(
                    f"Project with name '{name}' already exists"
                )
            project.name = name

        if description is not None:
            project.description = description

        self.session.commit()
        self.session.refresh(project)

        return project

    def delete(self, project_id: int) -> bool:
        """Delete a project by ID."""
        project = self.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found"
            )

        self.session.delete(project)
        self.session.commit()

        return True