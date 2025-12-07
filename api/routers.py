"""API router definitions for the TodoList application."""

from fastapi import APIRouter

from .controllers import projects_controller, tasks_controller

# Create main API router with version prefix
api_router = APIRouter(prefix="/api/v1")

# Register project routes
api_router.include_router(
    projects_controller.router,
    prefix="/projects",
    tags=["Projects"],
)

# Register task routes
api_router.include_router(
    tasks_controller.router,
    tags=["Tasks"],
)