from sqlalchemy.orm import Session
from models.task import Task
from typing import Optional, List
from datetime import datetime


class TaskRepository:
    """Repository for handling Task database operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        """Create a new task."""
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID."""
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_by_project_id(self, project_id: int) -> List[Task]:
        """Get all tasks for a specific project."""
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def get_overdue_tasks(self, current_time: datetime = None) -> List[Task]:
        """Get all overdue tasks (deadline < current_time and status != 'done')."""
        if current_time is None:
            current_time = datetime.now()

        return self.db.query(Task).filter(
            Task.deadline < current_time,
            Task.status != 'done'
        ).all()

    def update(self, task: Task) -> Task:
        """Update an existing task."""
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by ID."""
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
            return True
        return False

    def count_by_project(self, project_id: int) -> int:
        """Count number of tasks in a project."""
        return self.db.query(Task).filter(Task.project_id == project_id).count()