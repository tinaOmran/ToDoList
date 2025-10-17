class Project:
    def __init__(self, project_id, name, description=""):
        self.id = project_id
        self.name = name
        self.description = description
        self.tasks = []
