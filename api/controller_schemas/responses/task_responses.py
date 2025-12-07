"""Pydantic models for task-related responses."""

from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field

from ..requests.task_requests import TaskStatus


class TaskResponse(BaseModel):
    """Response schema for task data."""

    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    deadline: Optional[date] = Field(None, description="Deadline date")
    created_at: datetime = Field(..., description="Creation timestamp")
    closed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    project_id: int = Field(..., description="Parent project ID")

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Response schema for task list data."""

    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    count: int = Field(..., description="Number of tasks")

    @classmethod
    def from_tasks(cls, tasks:list) -> "TaskListResponse":
        """Helper method to create response from task list."""
        return cls(
            tasks=tasks,
            count=len(tasks)
        )


class TaskCreatedResponse(TaskResponse):
    """Response schema for task creation."""

    message: str = Field(
        default="Task created successfully.",
        description="Success message.",
    )


class TaskStatusUpdateResponse(BaseModel):
    """Response schema for status update operation."""

    id: int = Field(..., description="Task ID")
    previous_status: str = Field(..., description="Previous status")
    new_status: str = Field(..., description="New status")
    updated_at: datetime = Field(default_factory=datetime.now, description="Update timestamp")
    message: str = Field(..., description="Operation message")