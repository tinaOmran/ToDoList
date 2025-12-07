"""Controller for task-related endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from todo.db.session import get_session
from todo.services.task_service import TaskService
from todo.exceptions.service_exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    TaskLimitExceededError,
    InvalidDeadlineError
)
from todo.exceptions.base import ValidationError

from ..controller_schemas.requests import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskStatusUpdateRequest
)
from ..controller_schemas.responses import (
    TaskResponse,
    TaskListResponse,
    TaskCreatedResponse,
    TaskStatusUpdateResponse
)

# Create router
router = APIRouter()


# Dependency to get database session (همون پروژه‌ها)
def get_db():
    """Dependency to get database session."""
    session = get_session()
    try:
        yield session
    finally:
        session.close()


# Path parameter validation for project_id
def validate_project_id(project_id: int = Path(..., gt=0, description="Project ID must be positive")):
    return project_id


# Path parameter validation for task_id
def validate_task_id(task_id: int = Path(..., gt=0, description="Task ID must be positive")):
    return task_id


@router.get(
    "/projects/{project_id}/tasks",
    response_model=TaskListResponse,
    summary="List tasks in a project",
    description="Retrieve all tasks belonging to a specific project.",
    responses={
        404: {"description": "Project not found"}
    }
)
def list_tasks(
        project_id: int = Depends(validate_project_id),
        session: Session = Depends(get_db)
):
    """Get all tasks in a project."""
    try:
        service = TaskService(session)
        tasks = service.list_tasks(project_id)
        return TaskListResponse.from_tasks(tasks)
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/projects/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve details of a specific task within a project.",
    responses={
        404: {"description": "Task or project not found"}
    }
)
def get_task(
    project_id: int = Depends(validate_project_id),
    task_id: int = Depends(validate_task_id),
    session: Session = Depends(get_db)
):
    """Get a specific task by ID within a project."""
    try:
        service = TaskService(session)
        task = service.get_task(project_id, task_id)
        return task
    except (TaskNotFoundError, ProjectNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskCreatedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task within a specific project.",
    responses={
        404: {"description": "Project not found"},
        400: {"description": "Validation error or task limit exceeded"},
        422: {"description": "Invalid input data"}
    }
)
def create_task(
        project_id: int = Depends(validate_project_id),
        task_data: TaskCreateRequest = ...,
        session: Session = Depends(get_db)
):
    """Create a new task in a project."""
    try:
        service = TaskService(session)
        task = service.create_task(
            project_id=project_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            deadline=task_data.deadline
        )
        return TaskCreatedResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            created_at=task.created_at,
            closed_at=task.closed_at,
            project_id=task.project_id,
            message="Task created successfully"
        )
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (TaskLimitExceededError, InvalidDeadlineError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put(
    "/projects/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task's details.",
    responses={
        404: {"description": "Task or project not found"},
        400: {"description": "Validation error"}
    }
)
def update_task(
        project_id: int = Depends(validate_project_id),
        task_id: int = Depends(validate_task_id),
        task_data: TaskUpdateRequest = ...,
        session: Session = Depends(get_db)
):
    """Update a task."""
    try:
        service = TaskService(session)
        task = service.update_task(
            project_id=project_id,
            task_id=task_id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            deadline=task_data.deadline
        )
        return task
    except (TaskNotFoundError, ProjectNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (InvalidDeadlineError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch(
    "/projects/{project_id}/tasks/{task_id}/status",
    response_model=TaskStatusUpdateResponse,
    summary="Update task status",
    description="Update only the status of a task.",
    responses={
        404: {"description": "Task or project not found"},
        400: {"description": "Invalid status"}
    }
)
def update_task_status(
        project_id: int = Depends(validate_project_id),
        task_id: int = Depends(validate_task_id),
        status_data: TaskStatusUpdateRequest = ...,
        session: Session = Depends(get_db)
):
    """Update task status."""
    try:
        service = TaskService(session)
        task = service.change_task_status(
            project_id=project_id,
            task_id=task_id,
            new_status=status_data.status
        )

        return TaskStatusUpdateResponse(
            id=task.id,
            previous_status="",
            new_status=task.status,
            updated_at=task.created_at,
            message=f"Task status updated to {task.status}"
        )
    except (TaskNotFoundError, ProjectNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/projects/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task from a project.",
    responses={
        404: {"description": "Task or project not found"}
    }
)
def delete_task(
        project_id: int = Depends(validate_project_id),
        task_id: int = Depends(validate_task_id),
        session: Session = Depends(get_db)
):
    """Delete a task."""
    try:
        service = TaskService(session)
        service.delete_task(project_id, task_id)

    except (TaskNotFoundError, ProjectNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )