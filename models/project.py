from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from exceptions.base import ValidationError
import config

if TYPE_CHECKING:
    from .task import Task

class Project(Base):
    """SQLAlchemy model for Project entity."""

    __tablename__ = "projects"

    # Columns
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)

    # Relationships
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="select"
    )

    #Columns with default
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Project(id={self.id}, name='{self.name}')"

    def __init__(self, **kwargs):
        """Initialize project with validation."""
        super().__init__(**kwargs)
        self._validate_name()
        self._validate_description()

    def _validate_name(self):
        """Ensure that the project name is a valid non-empty string."""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValidationError("Project name cannot be empty.")
        if len(self.name) > 30:
            raise ValidationError("Project name must be at most 30 characters.")

    def _validate_description(self):
        """Ensure that the project description is within allowed length."""
        if self.description is None:
            self.description = ""
        if len(self.description) > 150:
            raise ValidationError("Project description must be at most 150 characters.")

    def edit(self, name: Optional[str] = None, description: Optional[str] = None):
        """Edit the project's name and/or description.

        Args:
            name (Optional[str]): New name for the project.
            description (Optional[str]): New description for the project.

        Raises:
            ValueError: If provided values are invalid.
        """
        original_name = self.name
        original_description = self.description

        try:
            if name is not None:
                self.name = name
                self._validate_name()

            if description is not None:
                self.description = description
                self._validate_description()

        except ValidationError as e:
            # Rollback in case of validation error
            self.name = original_name
            self.description = original_description
            raise e


