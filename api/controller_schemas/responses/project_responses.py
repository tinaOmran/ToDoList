"""Pydantic models for project-related responses."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ProjectResponse(BaseModel):
    """Response schema for Project model."""

    id: int = Field(..., description="Unique project id.")
    name: str = Field(..., description="Project name.")
    description: str = Field(..., description="Project description.")
    created_at: datetime = Field(..., description="creation timestamp")

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models


class ProjectListResponse(BaseModel):
    """Response schema for listing projects."""

    projects: List[ProjectResponse] = Field(..., description="List of projects")
    count: int = Field(..., description="Total number of projects")

    @classmethod
    def from_projects(cls, projects: list) -> "ProjectListResponse":
        """Helper method to create response from project list."""
        return cls(
            projects=projects,
            count=len(projects)
        )


class ProjectCreateResponse(ProjectResponse):
    """Response schema for project creation."""

    message: str = Field(
        default="Project created successfully.",
        description="Success message.",
    )