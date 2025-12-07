"""Pydantic models for task-related requests."""

from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator

TaskStatus = Literal["todo", "doing", "done"]


class TaskCreateRequest(BaseModel):
    """Request schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Task title"
    )

    description: Optional[str] = Field(
        default="",
        max_length=150,
        description="Optional task description"
    )

    status: Optional[TaskStatus] = Field(
        default="todo",
        description="Task status"
    )

    deadline: Optional[date] = Field(
        default=None,
        description="Deadline date (YYYY-MM-DD)"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError("Task title cannot be empty")
        return v.strip()

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, v):
        if v and v < date.today():
            raise ValueError("Deadline cannot be in the past")
        return v


class TaskUpdateRequest(BaseModel):
    """Request schema for updating a task."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=30,
        description="New task title"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=150,
        description="New description"
    )

    status: Optional[TaskStatus] = Field(
        default=None,
        description="New status"
    )

    deadline: Optional[date] = Field(
        default=None,
        description="New deadline date (YYYY-MM-DD)"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Task title cannot be empty")
        return v.strip() if v else v

    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, v):
        if v and v < date.today():
            raise ValueError("Deadline cannot be in the past")
        return v


class TaskStatusUpdateRequest(BaseModel):
    """Request schema for updating only task status."""

    status: TaskStatus = Field(
        ...,
        description="New task status"
    )