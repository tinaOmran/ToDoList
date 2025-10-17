from project_manager import ProjectManager

pm = ProjectManager()
project = pm.create_project("Test App", "Initial Test")
print(project.name, project.description)
