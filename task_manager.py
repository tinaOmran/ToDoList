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

    def change_status(self, project_id, task_id, new_status):
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("تسک یافت نشد.")

        allowed_status = ["todo", "doing", "done"]
        if new_status not in allowed_status:
            raise ValueError(f"وضعیت نامعتبر است. وضعیت مجاز: {allowed_status}")

        task.status = new_status
        return task

    def edit_task(self, project_id, task_id, new_title=None, new_description=None, new_deadline=None):
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("تسک یافت نشد.")

        if new_title:
            if len(new_title.split()) > 30:
                raise ValueError("عنوان تسک بیش از حد طولانی است.")
            task.title = new_title

        if new_description:
            if len(new_description.split()) > 150:
                raise ValueError("توضیح تسک بیش از حد طولانی است.")
            task.description = new_description

        if new_deadline:
            task.deadline = new_deadline

        return task

    def delete_task(self, project_id, task_id):
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("تسک یافت نشد.")

        project.tasks.remove(task)
        return True

