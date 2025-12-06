class ToDoError(Exception):
    """Base exception for all ToDoList errors."""
    pass

class ValidationError(ToDoError):
    """Raised when input data violates validation rules."""
    pass

class StorageError(ToDoError):
    """Raised when something goes wrong with the storage layer."""
    pass