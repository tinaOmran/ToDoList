"""
FastAPI application entry point for ToDo List API.

Run with:
    uvicorn todo.api.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import api_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="ToDo List API",
        description=(
            "A RESTful API for managing projects and tasks. "
            "This is Phase 3 of the ToDo List project, replacing the CLI interface."
        ),
        version="1.0.0",
        docs_url="/docs"
    )

    # Add CORS middleware
    # In production, you should restrict origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Include API routes
    app.include_router(api_router)

    return app


# Create the FastAPI application instance
app = create_application()


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.

    Returns:
        dict: API metadata and available endpoints
    """
    return {
        "application": "ToDo List API",
        "version": "1.0.0",
        "description": "RESTful API for managing projects and tasks",
        "endpoints": {
            "projects": "/api/v1/projects",
            "tasks": "/api/v1/tasks",
        },
        "documentation": {
            "swagger_ui": "/docs"
        },
        "note": "CLI interface is deprecated. Please use this HTTP API."
    }


@app.get("/api", tags=["API Info"])
async def api_info():
    """
    API version and configuration information.

    Returns:
        dict: API configuration details
    """
    return {
        "api_version": "v1",
        "base_path": "/api/v1",
        "available_resources": ["projects", "tasks"],
        "authentication": "None (public API for now)",
        "rate_limiting": "None"
    }


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Run the FastAPI development server.

    Args:
        host: Server host address
        port: Server port
        reload: Enable auto-reload on code changes
    """
    import uvicorn

    print("🚀 Starting ToDo List API Server...")
    print(f"   URL: http://{host}:{port}")
    print(f"   Docs: http://{host}:{port}/docs")
    print("\n📋 Available Endpoints:")
    print("   • GET  /                    - API information")
    print("   • GET  /api                 - API configuration")
    print("   • GET  /api/v1/projects     - List projects")
    print("   • POST /api/v1/projects     - Create project")
    print("   • GET  /api/v1/projects/{id} - Get project")
    print("   • PUT  /api/v1/projects/{id} - Update project")
    print("   • DEL  /api/v1/projects/{id} - Delete project")
    print("   • GET  /api/v1/tasks        - List tasks (with project_id query)")
    print("   • POST /api/v1/tasks        - Create task")
    print("\n⚡ Press Ctrl+C to stop the server")

    uvicorn.run(
        "todo.api.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":

    run_server()