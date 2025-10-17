class Project:
    """
    Represents a project containing tasks.

    Attributes:
        id (int): Unique identifier for the project.
        name (str): Name of the project.
        description (str): Optional description of the project.
        tasks (list): List of Task objects associated with this project.
    """

    def __init__(self, project_id, name, description=""):
        """
        Initialize a Project instance.

        Args:
            project_id (int): Unique ID of the project.
            name (str): Name of the project.
            description (str, optional): Description of the project. Defaults to empty string.
        """
        self.id = project_id
        self.name = name
        self.description = description
        self.tasks = []  # List to hold tasks associated with this project


class Task:
    """
    Represents a task within a project.

    Attributes:
        id (int): Unique identifier for the task.
        title (str): Title of the task.
        description (str): Description of the task.
        status (str): Status of the task ('todo', 'doing', 'done'). Defaults to 'todo'.
        deadline (str, optional): Optional deadline for the task.
    """

    def __init__(self, id, title, description, status="todo", deadline=None):
        """
        Initialize a Task instance.

        Args:
            id (int): Unique ID of the task.
            title (str): Title of the task.
            description (str): Description of the task.
            status (str, optional): Status of the task. Defaults to 'todo'.
            deadline (str, optional): Deadline of the task. Defaults to None.
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline

