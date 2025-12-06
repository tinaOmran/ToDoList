from .base import ToDoError , ValidationError

class ProjectNotFoundError(ToDoError):
    """Raised when a project with a given ID does not exist."""
    pass

class TaskNotFoundError(ToDoError):
    """Raised when a task with a given ID does not exist."""
    pass

class ProjectNameExistsError(ToDoError):
    """Raised when trying to create a project with a name that already exists."""
    pass

class ProjectLimitExceededError(ToDoError):
    """Raised when the maximum number of projects has been reached."""
    pass

class TaskLimitExceededError(ToDoError):
    """Raised when the maximum number of tasks for a project has been reached."""
    pass

class InvalidDeadlineError(ValidationError):
    """Raised when the provided deadline is in the past."""
    pass