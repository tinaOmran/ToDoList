class InMemoryStorage:
    """
    A simple in-memory storage for project objects.

    This class provides a container to store all projects during the
    runtime of the application. It does not persist data to disk or
    any external database.

    Attributes:
        projects (list): A list that holds all project objects.
    """

    def __init__(self):
        """
        Initialize the in-memory storage with an empty list of projects.
        """
        # Initialize an empty list to store project instances
        self.projects = []


# Create a single shared storage instance for the application
storage = InMemoryStorage()
