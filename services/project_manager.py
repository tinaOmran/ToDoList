from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectNameExistsError,
    ProjectLimitExceededError
)
from exceptions.base import ValidationError
from repositories.project_repository import ProjectRepository
from models.project import Project
from typing import Optional


class ProjectManager:
    """
    Service layer for handling project business logic.
    Uses ProjectRepository for data access.
    """

    def __init__(self, project_repository: ProjectRepository):
        """
        Initialize ProjectService with a ProjectRepository instance.

        Args:
            project_repository (ProjectRepository): Repository for project data access.
        """
        self.project_repo = project_repository

    def create_project(self, name: str, description: str, max_projects: int = 5) -> Project:
        """
        Create a new project.

        Args:
            name (str): Name of the project.
            description (str): Description of the project.
            max_projects (int): Maximum allowed projects (default: 5).

        Returns:
            Project: The newly created Project object.

        Raises:
            ValidationError: If the name or description is too long.
            ProjectNameExistsError: If a project with the same name exists.
            ProjectLimitExceededError: If the number of projects exceeds maximum allowed.
        """
        # Check length of name and description
        if len(name.split()) > 30:
            raise ValidationError("نام پروژه بیش از حد طولانی است.")

        if len(description.split()) > 150:
            raise ValidationError("توضیح پروژه بیش از حد طولانی است.")

        # Check for duplicate project name
        existing_project = self.project_repo.get_by_name(name)
        if existing_project:
            raise ProjectNameExistsError("پروژه‌ای با این نام از قبل وجود دارد.")

        # Check if number of projects exceeds maximum allowed
        current_count = self.project_repo.count()
        if current_count >= max_projects:
            raise ProjectLimitExceededError("تعداد پروژه‌ها از سقف مجاز بیشتر است.")

        # Create and save the project
        project = Project(name=name, description=description)
        #project = Project()
        #project.name = name
        #project.description = description
        return self.project_repo.create(project)

    def get_project(self, project_id: int) -> Optional[Project]:
        """
        Get a project by its ID.

        Args:
            project_id (int): ID of the project.

        Returns:
            Optional[Project]: The project if found, None otherwise.
        """
        return self.project_repo.get_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
        """
        Get all projects.

        Returns:
            list[Project]: List of all projects.
        """
        return self.project_repo.get_all()

    def update_project(self, project_id: int, new_name: Optional[str] = None,
                       new_description: Optional[str] = None) -> Project:
        """
        Update an existing project.

        Args:
            project_id (int): ID of the project to update.
            new_name (str, optional): New name for the project.
            new_description (str, optional): New description for the project.

        Returns:
            Project: The updated project.

        Raises:
            ProjectNotFoundError: If project not found.
            ProjectNameExistsError: If trying to change to an existing project name.
            ValidationError: If validation fails.
        """
        # Get the project
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        # Update name if provided
        if new_name:
            # Validate name length
            if len(new_name.split()) > 30:
                raise ValidationError("نام پروژه بیش از حد طولانی است.")

            # Check if the new name already exists (excluding current project)
            existing_project = self.project_repo.get_by_name(new_name)
            if existing_project and existing_project.id != project_id:
                raise ProjectNameExistsError(f"پروژه‌ای با نام '{new_name}' از قبل وجود دارد.")

            project.name = new_name

        # Update description if provided
        if new_description:
            # Validate description length
            if len(new_description.split()) > 150:
                raise ValidationError("توضیح پروژه بیش از حد طولانی است.")

            project.description = new_description

        # Save changes
        return self.project_repo.update(project)

    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project.

        Args:
            project_id (int): ID of the project to delete.

        Returns:
            bool: True if project was successfully deleted.

        Raises:
            ProjectNotFoundError: If project not found.
        """
        # Check if project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        # Delete the project
        return self.project_repo.delete(project_id)

    def count_projects(self) -> int:
        """
        Count total number of projects.

        Returns:
            int: Number of projects.
        """
        return self.project_repo.count()