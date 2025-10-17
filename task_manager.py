from validators import validate_task
from in_memory_storage import storage
from models import Task

class TaskManager:
    def __init__(self):
        self.storage = storage

    def add_task(self, project_id, title, description, deadline=None):
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")
        validate_task(title, description, project.tasks)
        task_id = len(project.tasks) + 1
        task = Task(task_id, title, description, deadline=deadline)
        project.tasks.append(task)
        return task
