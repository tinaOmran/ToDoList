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

<<<<<<< HEAD
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
=======
    def list_tasks_by_project(self, project_id):
        """
        List all tasks that belong to a specific project.

        Args:
            project_id (int): The ID of the project whose tasks should be listed.

        Returns:
            list: A list of Task objects for the given project.
                  Returns an empty list if the project is not found
                  or if there are no tasks.
        """
        # Try to find the project with the given ID
        project = next(
            (p for p in self.storage.projects if p.id == project_id),
            None
        )

        # Handle case when project does not exist
        if not project:
            print("Project not found.")
            return []

        # Handle case when project exists but has no tasks
        if not project.tasks:
            print("No tasks exist for this project.")
            return []

        # Print each task's details in a readable format
        for task in project.tasks:
            print(
                f"[{task.id}] {task.title} | "
                f"{task.status} | deadline={task.deadline}"
            )

        # Return the list of tasks for further use
        return project.tasks
>>>>>>> feature/list-project-tasks
