from services.validators import validate_project
from in_memory_storage import storage
from models.project import Project


class ProjectManager:
    """
    A manager class to handle all operations related to projects.

    Attributes:
        storage (InMemoryStorage): Shared in-memory storage for projects.
    """

    def __init__(self):
        """
        Initialize ProjectManager with a shared in-memory storage instance.
        """
        self.storage = storage

    def create_project(self, name, description):
        """
        Create a new project and add it to storage.

        Args:
            name (str): Name of the project.
            description (str): Description of the project.

        Returns:
            Project: The newly created Project object.

        Raises:
            ValueError: If project validation fails.
        """
        # Validate project data
        validate_project(name, description, self.storage.projects)

        # Generate project ID
        project_id = len(self.storage.projects) + 1

        # Create and store the project
        project = Project(project_id, name, description)
        self.storage.projects.append(project)

        return project

    def edit_project(self, project_id, new_name=None, new_description=None):
        """
        Edit an existing project's name and/or description.

        Args:
            project_id (int): ID of the project to edit.
            new_name (str, optional): New name for the project.
            new_description (str, optional): New description for the project.

        Returns:
            Project: The updated Project object.

        Raises:
            ValueError: If project not found or validation fails.
        """
        # Find project by ID
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        # Update name if provided
        if new_name:
            validate_project(new_name, new_description or project.description, self.storage.projects)
            project.name = new_name

        # Update description if provided
        if new_description:
            project.description = new_description

        return project

    def delete_project(self, project_id):
        """
        Delete a project from storage.

        Args:
            project_id (int): ID of the project to delete.

        Returns:
            bool: True if project was successfully deleted.

        Raises:
            ValueError: If project not found.
        """
        # Find project by ID
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        # Remove project from storage
        self.storage.projects.remove(project)
        return True

    def list_projects(self):
        """
        Display all existing projects and return them as a list.

        This method checks whether any projects are stored.
        If no projects exist, it prints a message and returns an empty list.
        Otherwise, it prints each project's ID, name, and description,
        and returns the list of all projects.

        Returns:
            list: A list of all stored project objects. Returns an empty list if none exist.
        """
        # Check if there are any projects stored in memory
        if not self.storage.projects:
            print("هیچ پروژه‌ای وجود ندارد.")
            return []

        # Iterate through all stored projects and print their details
        for p in self.storage.projects:
            print(f"[{p.id}] {p.name} - {p.description}")

        # Return the list of all project objects
        return self.storage.projects
