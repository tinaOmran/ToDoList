"""Controller for project-related endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todo.db.session import get_session
from todo.services.project_service import ProjectService
from todo.exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectNameExistsError,
    ProjectLimitExceededError
)

from ..controller_schemas.requests import ProjectCreateRequest, ProjectUpdateRequest
from ..controller_schemas.responses import (
    ProjectResponse,
    ProjectListResponse,
    ProjectCreateResponse
)

# Create router
router = APIRouter()

# Dependency to get database session
def get_db():
    """Dependency to get database session."""
    session = get_session()
    try:
        yield session
    finally:
        session.close()

@router.get(
    "/",
    response_model=ProjectListResponse,
    summary="List all projects",
    description="Retrieve a list of all projects sorted by creation time."
)
def list_projects(session: Session = Depends(get_db)):
    """Get all projects."""
    service = ProjectService(session)
    projects = service.list_projects()
    return ProjectListResponse.from_projects(projects)

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Retrieve details of a specific project by its ID.",
    responses={
        404: {"description": "Project not found"}
    }
)
def get_project(project_id: int, session: Session = Depends(get_db)):
    """Get a specific project by ID."""
    try:
        service = ProjectService(session)
        project = service.get_project(project_id)
        return project
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    "/",
    response_model=ProjectCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with a unique name.",
    responses={
        409: {"description": "Project name already exists"},
        400: {"description": "Validation error or limit exceeded"}
    }
)
def create_project(
    project_data: ProjectCreateRequest,
    session: Session = Depends(get_db)
):
    """Create a new project."""
    try:
        service = ProjectService(session)
        project = service.create_project(
            name=project_data.name,
            description=project_data.description
        )

        return ProjectCreateResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            message="Project created successfully"
        )
    except ProjectNameExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Project with name '{project_data.name}' already exists"
        )
    except ProjectLimitExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
    description="Update an existing project's name and/or description.",
    responses={
        404: {"description": "Project not found"},
        409: {"description": "Project name already exists"},
        400: {"description": "Validation error"}
    }
)
def update_project(
    project_id: int,
    project_data: ProjectUpdateRequest,
    session: Session = Depends(get_db)
):
    """Update a project."""
    try:
        service = ProjectService(session)
        project = service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        return project
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ProjectNameExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete a project and all its associated tasks.",
    responses={
        404: {"description": "Project not found"}
    }
)
def delete_project(project_id: int, session: Session = Depends(get_db)):
    """Delete a project."""
    try:
        service = ProjectService(session)
        service.delete_project(project_id)
        # No content to return for 204
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )