# services/task_manager.py
from exceptions.service_exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
    TaskLimitExceededError,
    InvalidDeadlineError
)
from exceptions.base import ValidationError
from repositories.task_repository import TaskRepository
from repositories.project_repository import ProjectRepository
from models.task import Task
from typing import Optional, List
from datetime import datetime


class TaskManager:
    """
    Service layer for handling task business logic.
    Uses TaskRepository for data access.
    """

    def __init__(self, task_repository: TaskRepository,
                 project_repository: ProjectRepository):
        """
        Initialize TaskService with TaskRepository and ProjectRepository instances.

        Args:
            task_repository (TaskRepository): Repository for task data access.
            project_repository (ProjectRepository): Repository for project data access.
        """
        self.task_repo = task_repository
        self.project_repo = project_repository

    def create_task(self, project_id: int, title: str, description: str,
                    deadline: Optional[str] = None, max_tasks: int = 10) -> Task:
        """
        Create a new task in a project.

        Args:
            project_id (int): ID of the project.
            title (str): Title of the task.
            description (str): Description of the task.
            deadline (str, optional): Deadline in format 'YYYY-MM-DD'.
            max_tasks (int): Maximum allowed tasks per project (default: 10).

        Returns:
            Task: The newly created task.

        Raises:
            ProjectNotFoundError: If project not found.
            ValidationError: If title or description is too long.
            TaskLimitExceededError: If number of tasks exceeds maximum allowed.
            InvalidDeadlineError: If deadline is in the past.
        """
        # Check if project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        # Validate title and description length
        if len(title.split()) > 30:
            raise ValidationError("عنوان تسک بیش از حد طولانی است.")

        if len(description.split()) > 150:
            raise ValidationError("توضیح تسک بیش از حد طولانی است.")

        # Check task limit for the project
        task_count = self.task_repo.count_by_project(project_id)
        if task_count >= max_tasks:
            raise TaskLimitExceededError("تعداد تسک‌ها از سقف مجاز بیشتر است.")

        # Validate deadline if provided
        deadline_date = None
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                if deadline_date < datetime.now():
                    raise InvalidDeadlineError("ددلاین نمی‌تواند در گذشته باشد.")
            except ValueError:
                raise ValidationError("فرمت ددلاین نامعتبر است. باید YYYY-MM-DD باشد.")

        # Create and save the task
        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            deadline=deadline_date
        )
        return self.task_repo.create(task)

    def change_status(self, project_id: int, task_id: int, new_status: str) -> Task:
        """
        Change the status of a task.

        Args:
            project_id (int): ID of the project.
            task_id (int): ID of the task.
            new_status (str): New status (todo/doing/done).

        Returns:
            Task: Updated task object.

        Raises:
            ProjectNotFoundError: If project not found.
            TaskNotFoundError: If task not found or doesn't belong to project.
            ValidationError: If status is invalid.
        """
        # Check if project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        # Check if task exists and belongs to project
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} یافت نشد.")

        if task.project_id != project_id:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} متعلق به پروژه {project_id} نیست.")

        # Validate status
        allowed_status = ["todo", "doing", "done"]
        if new_status not in allowed_status:
            raise ValidationError(f"وضعیت نامعتبر است. وضعیت‌های مجاز: {allowed_status}")

        # Update status
        task.status = new_status
        return self.task_repo.update(task)

    def update_task(self, project_id: int, task_id: int,
                    new_title: Optional[str] = None,
                    new_description: Optional[str] = None,
                    new_deadline: Optional[str] = None) -> Task:
        """
        Update task details.

        Args:
            project_id (int): ID of the project.
            task_id (int): ID of the task.
            new_title (str, optional): New title.
            new_description (str, optional): New description.
            new_deadline (str, optional): New deadline in 'YYYY-MM-DD' format.

        Returns:
            Task: Updated task object.

        Raises:
            ProjectNotFoundError: If project not found.
            TaskNotFoundError: If task not found or doesn't belong to project.
            ValidationError: If validation fails.
        """
        # Check if project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        # Check if task exists and belongs to project
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} یافت نشد.")

        if task.project_id != project_id:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} متعلق به پروژه {project_id} نیست.")

        # Update title if provided
        if new_title:
            if len(new_title.split()) > 30:
                raise ValidationError("عنوان تسک بیش از حد طولانی است.")
            task.title = new_title

        # Update description if provided
        if new_description:
            if len(new_description.split()) > 150:
                raise ValidationError("توضیح تسک بیش از حد طولانی است.")
            task.description = new_description

        # Update deadline if provided
        if new_deadline is not None:  # Can be empty string to clear deadline
            if new_deadline:
                try:
                    deadline_date = datetime.strptime(new_deadline, '%Y-%m-%d')
                    if deadline_date < datetime.now():
                        raise InvalidDeadlineError("ددلاین نمی‌تواند در گذشته باشد.")
                    task.deadline = deadline_date
                except ValueError:
                    raise ValidationError("فرمت ددلاین نامعتبر است. باید YYYY-MM-DD باشد.")
            else:
                task.deadline = None

        return self.task_repo.update(task)

    def delete_task(self, project_id: int, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            project_id (int): ID of the project.
            task_id (int): ID of the task.

        Returns:
            bool: True if task was successfully deleted.

        Raises:
            ProjectNotFoundError: If project not found.
            TaskNotFoundError: If task not found or doesn't belong to project.
        """
        # Check if project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        # Check if task exists and belongs to project
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} یافت نشد.")

        if task.project_id != project_id:
            raise TaskNotFoundError(f"تسک با شناسه {task_id} متعلق به پروژه {project_id} نیست.")

        # Delete task
        return self.task_repo.delete(task_id)

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """
        Get all tasks for a project.

        Args:
            project_id (int): ID of the project.

        Returns:
            List[Task]: List of tasks for the project.

        Raises:
            ProjectNotFoundError: If project not found.
        """
        # Check if project exists
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(f"پروژه با شناسه {project_id} یافت نشد.")

        return self.task_repo.get_by_project_id(project_id)

    def count_tasks_by_project(self, project_id: int) -> int:
        """
        Count number of tasks in a project.

        Args:
            project_id (int): ID of the project.

        Returns:
            int: Number of tasks in the project.
        """
        return self.task_repo.count_by_project(project_id)

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks (deadline < now and status != 'done').

        Returns:
            List[Task]: List of overdue tasks.
        """
        current_time = datetime.now()
        return self.task_repo.get_overdue_tasks(current_time)

    def close_overdue_tasks(self) -> int:
        """
        Close all overdue tasks (set status to 'done' and add closed_at).

        Returns:
            int: Number of tasks closed.
        """
        overdue_tasks = self.get_overdue_tasks()
        closed_count = 0

        for task in overdue_tasks:
            task.status = "done"
            # task.closed_at is automatically set in model if needed
            self.task_repo.update(task)
            closed_count += 1

        return closed_count