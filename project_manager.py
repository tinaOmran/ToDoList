from validators import validate_project
from in_memory_storage import storage
from models import Project

class ProjectManager:
    def __init__(self):
        self.storage = storage

    def create_project(self, name, description):
        validate_project(name, description, self.storage.projects)
        project_id = len(self.storage.projects) + 1
        project = Project(project_id, name, description)
        self.storage.projects.append(project)
        return project

    def edit_project(self, project_id, new_name=None, new_description=None):
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")
        if new_name:
            validate_project(new_name, new_description or project.description, self.storage.projects)
            project.name = new_name
        if new_description:
            project.description = new_description
        return project

    def delete_project(self, project_id):
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")
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
            print("No projects available.")
            return []

        # Iterate through all stored projects and print their details
        for p in self.storage.projects:
            print(f"[{p.id}] {p.name} - {p.description}")

        # Return the list of all project objects
        return self.storage.projects




