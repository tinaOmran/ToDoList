from services.validators import validate_task
from in_memory_storage import storage
from models.models import Task
from services.project_manager import ProjectManager


class TaskManager:
    """
    A manager class to handle all operations related to tasks within projects.

    Attributes:
        pm (ProjectManager): An instance of ProjectManager for project access.
        storage (InMemoryStorage): Shared in-memory storage for projects and tasks.
    """

    def __init__(self, project_manager=None):
        """
        Initialize TaskManager with an optional ProjectManager instance.
        If none is provided, a new ProjectManager is created.

        Args:
            project_manager (ProjectManager, optional): An existing ProjectManager instance.
        """
        self.pm = project_manager or ProjectManager()
        self.storage = self.pm.storage

    def add_task(self, project_id, title, description, deadline=None):
        """
        Add a new task to a project.

        Args:
            project_id (int): ID of the project to add the task to.
            title (str): Title of the task.
            description (str): Description of the task.
            deadline (str, optional): Optional deadline for the task.

        Returns:
            Task: The newly created Task object.

        Raises:
            ValueError: If the project is not found or validation fails.
        """
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        validate_task(title, description, project.tasks)
        task_id = len(project.tasks) + 1
        task = Task(task_id, title, description, deadline=deadline)
        project.tasks.append(task)

        return task

    def change_status(self, project_id, task_id, new_status):
        """
        Change the status of a task within a project.

        Args:
            project_id (int): ID of the project containing the task.
            task_id (int): ID of the task to update.
            new_status (str): New status; must be 'todo', 'doing', or 'done'.

        Returns:
            Task: The updated Task object.

        Raises:
            ValueError: If the project or task is not found, or status is invalid.
        """
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
        """
        Edit the details of a task within a project.

        Args:
            project_id (int): ID of the project containing the task.
            task_id (int): ID of the task to edit.
            new_title (str, optional): New title for the task.
            new_description (str, optional): New description.
            new_deadline (str, optional): New deadline.

        Returns:
            Task: The updated Task object.

        Raises:
            ValueError: If project/task not found or validation fails.
        """
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
        """
        Delete a task from a project.

        Args:
            project_id (int): ID of the project.
            task_id (int): ID of the task to delete.

        Returns:
            bool: True if task was successfully deleted.

        Raises:
            ValueError: If project or task is not found.
        """
        project = next((p for p in self.storage.projects if p.id == project_id), None)
        if not project:
            raise ValueError("پروژه یافت نشد.")

        task = next((t for t in project.tasks if t.id == task_id), None)
        if not task:
            raise ValueError("تسک یافت نشد.")

        project.tasks.remove(task)
        return True

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
        project = next(
            (p for p in self.storage.projects if p.id == project_id),
            None
        )

        if not project:
            print("پروژه یافت نشد.")
            return []

        if not project.tasks:
            print("تسکی برای این پروژه وجود ندارد.")
            return []

        for task in project.tasks:
            print(
                f"[{task.id}] {task.title} | "
                f"{task.status} | deadline={task.deadline}"
            )

        return project.tasks
