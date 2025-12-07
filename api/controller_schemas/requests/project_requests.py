"""Pydantic models for project-related requests."""

from typing import Optional

from pydantic import BaseModel, Field, field_validator

class ProjectCreateRequest(BaseModel):
    """Request schema for creating a new project."""

    name: str = Field(..., min_length=1,max_length=30,description="Project name (must be unique)")
    description: Optional[str] = Field(default="", max_length=150,description="Optional project description")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Project name cannot be empty")
        return v.strip()


class ProjectUpdateRequest(BaseModel):
    """Request schema for updating a project."""

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=30,
        description="New project name (must be unique if provided)",
        examples=["Updated Project Name"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=150,
        description="New description",
        examples=["Updated description"]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Project name cannot be empty")
        return v.strip() if v else v