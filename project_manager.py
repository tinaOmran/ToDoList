from utils.validators import validate_project
from data.in_memory_storage import storage

class ProjectManager:
    def __init__(self):
        self.storage = storage

    def create_project(self, name, description):
        validate_project(name, description, self.storage.projects)
        project_id = len(self.storage.projects) + 1
        project = Project(project_id, name, description)
        self.storage.projects.append(project)
        return project
