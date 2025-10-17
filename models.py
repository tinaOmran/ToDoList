class Project:
    def __init__(self, project_id, name, description=""):
        self.id = project_id
        self.name = name
        self.description = description
        self.tasks = []

class Task:
    def __init__(self, id, title, description, status="todo", deadline=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.deadline = deadline
