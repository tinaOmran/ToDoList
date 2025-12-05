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

