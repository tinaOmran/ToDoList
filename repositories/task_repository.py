from typing import List, Optional

from datetime import date
from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from config import config
from exceptions.service_exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    TaskLimitExceededError,
)
from models.project import Project
from models.task import Task


class TaskRepository:
    """
    Repository class responsible for handling database operations
    related to Task objects, including creation, update, deletion,
    and retrieval of tasks.
    """
    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.
        """
        self.session = session

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id (int): ID of the task.

        Returns:
        Optional[Task]: The task if found, else None.
        """
        return self.session.get(Task, task_id)

    def get_all(self) -> List[Task]:
        """
         Retrieve all tasks stored in the database.

         Returns:
             List[Task]: A list of all tasks.
         """
        stmt = select(Task)
        return list(self.session.scalars(stmt))

    def get_by_project_id(self, project_id: int) -> List[Task]:
        """
         Retrieve all tasks associated with a specific project.

         Args:
             project_id (int): ID of the project.

         Returns:
             List[Task]: List of tasks under the project.
         """
        stmt = select(Task).where(Task.project_id == project_id)
        return list(self.session.scalars(stmt))

    def get_task_count_by_project(self, project_id: int) -> int:
        """
        Count the number of tasks assigned to a specific project.

        Args:
            project_id (int): ID of the project.

        Returns:
            int: Number of associated tasks.
        """
        stmt = select(func.count(Task.id)).where(Task.project_id == project_id)
        return self.session.scalar(stmt)

    def create(
        self,
        project_id: int,
        title: str,
        description: str = "",
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Task:
        """
        Create a new task under a specified project.

        Args:
            project_id (int): ID of the project to attach task to.
            title (str): Task title.
            description (str, optional): Task description. Defaults to "".
            status (str, optional): Task status. Defaults to "todo".
            deadline (str, optional): Deadline date as string.

        Raises:
            ProjectNotFoundError: If the project does not exist.
            TaskLimitExceededError: If project task limit is reached.

        Returns:
            Task: Newly created task.
        """


        project = self.session.get(Project, project_id)
        if not project:
            raise ProjectNotFoundError(
                f"Project with ID {project_id} not found"
            )

        if (
            self.get_task_count_by_project(project_id)
            >= config.MAX_NUMBER_OF_TASK
        ):
            raise TaskLimitExceededError(
                "Max number of tasks for this project reached."
            )

        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status or "todo",
            deadline=deadline,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> Task:
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update.
            title (str, optional): New title.
            description (str, optional): New description.
            status (str, optional): New status.
            deadline (str, optional): New deadline.

        Raises:
            TaskNotFoundError: If task does not exist.

        Returns:
            Task: Updated task.
        """

        task = self.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(
                f"Task with ID {task_id} not found"
            )

        task.edit(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
        )

        self.session.commit()
        self.session.refresh(task)
        return task

    def change_status(self, task_id: int, new_status: str) -> Task:
        """
         Change the status of an existing task.

         Args:
             task_id (int): ID of the task.
             new_status (str): The new status value.

         Raises:
             TaskNotFoundError: If task does not exist.

         Returns:
             Task: Task with updated status.
         """

        task = self.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(
                f"Task with ID {task_id} not found"
            )

        task.change_status(new_status)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        """
         Delete a task by its ID.

         Args:
             task_id (int): ID of the task.

         Raises:
             TaskNotFoundError: If task does not exist.

         Returns:
             bool: True if deletion succeeded.
         """

        task = self.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(
                f"Task with ID {task_id} not found"
            )

        self.session.delete(task)
        self.session.commit()
        return True

    def get_overdue_tasks(self) -> List[Task]:
        """Get all tasks that are overdue and not done."""

        stmt = select(Task).where(
            and_(
                Task.deadline < date.today(),
                Task.status != "done",
                Task.closed_at.is_(None)
            )
        )

        return list(self.session.scalars(stmt))

    def close_overdue_tasks(self) -> int:
        """
        Close all overdue tasks using model's business logic.
        Returns the number of tasks closed.
        """
        overdue_tasks = self.get_overdue_tasks()
        closed_count = 0

        for task in overdue_tasks:
            try:

                task.change_status("done")
                closed_count += 1
                print(f"   ✅ Closed: {task.title} (Project: {task.project.name})")
            except Exception as e:
                print(f"   ❌ Failed to close task {task.id}: {e}")
                continue

        if closed_count > 0:
            self.session.commit()

        return closed_count