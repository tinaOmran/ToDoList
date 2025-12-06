"""Module defining the Task class for managing to-do items."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from exceptions.base import ValidationError
from exceptions.service_exceptions import TaskLimitExceededError, InvalidDeadlineError
import config

if TYPE_CHECKING:
    from .project import Project


VALID_STATUSES = ("todo", "doing", "done")


class Task(Base):
    """SQLAlchemy model for Task entity."""

    __tablename__ = "tasks"

    # Columns
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Foreign Key
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    description: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(10), default="todo")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"

    def __init__(self, **kwargs):
        """Initialize Task with validation."""
        super().__init__(**kwargs)
        self._validate_title()
        self._validate_description()
        self._validate_status()
        self._validate_deadline()

    def _validate_title(self) -> None:
        """Ensure that the title is non-empty and within character limits."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValidationError("Task title must be a non-empty string.")
        if len(self.title) > 30:
            raise ValidationError("Task title must be at most 30 characters.")

    def _validate_description(self) -> None:
        """Ensure that the description length does not exceed 150 characters."""
        if self.description is None:
            self.description = ""
        if len(self.description) > 150:
            raise ValidationError("Task description must be at most 150 characters.")

    def _validate_deadline(self) -> None:
        """Ensure that the deadline, if provided, is a valid date and not in the past."""
        if self.deadline is None:
            return

        #if the deadline is of type string, convert it to a date.
        if isinstance(self.deadline, str):
            try:
                self.deadline = datetime.strptime(self.deadline, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Deadline format must be YYYY-MM-DD.")

        # error if the deadline is in the past.
        if self.deadline < date.today():
            raise InvalidDeadlineError("Deadline cannot be in the past.")

    def _validate_status(self) -> None:
        """Ensure that the status value is valid."""
        if self.status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {self.status}. Valid: {VALID_STATUSES}")

    def change_status(self, new_status: str) -> None:
        """Change the task's status to a new valid one.

        Args:
            new_status (str): New status, one of VALID_STATUSES.

        Raises:
            ValueError: If new_status is not valid.
        """
        if new_status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status: {new_status}. Valid: {VALID_STATUSES}")

        original_status = self.status
        try:
            self.status = new_status
            self._validate_status()

            # Auto-set closed_at when task is marked as done
            if new_status == "done" and self.closed_at is None:
                self.closed_at = datetime.now()
            elif new_status != "done":
                self.closed_at = None

        except ValueError as e:
            self.status = original_status
            raise e

    def edit(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[str] = None,
    ) -> None:
        """Edit task details with proper validation.

        Args:
            title: New title
            description: New description
            status: New status ("todo", "doing", "done")
            deadline: New deadline (YYYY-MM-DD or date object)

        Raises:
            ValueError: If any of the fields are invalid
        """
        # Store original values for rollback
        original_title = self.title
        original_description = self.description
        original_status = self.status
        original_deadline = self.deadline

        try:
            if title is not None:
                self.title = title
                self._validate_title()

            if description is not None:
                self.description = description
                self._validate_description()

            if status is not None:
                self.status = status
                self._validate_status()

                # Handle closed_at for done status
                if status == "done" and self.closed_at is None:
                    self.closed_at = datetime.now()
                elif status != "done":
                    self.closed_at = None


            if deadline is not None:
                # Convert string to date if needed
                if isinstance(deadline, str):
                    try:
                        self.deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError("Deadline format must be YYYY-MM-DD.")
                else:
                    self.deadline = deadline
                self._validate_deadline()

        except ValueError as e:
            # Rollback all changes if any validation fails
            self.title = original_title
            self.description = original_description
            self.status = original_status
            self.deadline = original_deadline
            raise e