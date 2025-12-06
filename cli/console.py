"""Command-line interface for the To-Do List application.

WARNING: CLI interface is deprecated and will be removed in the next release.
Please use the FastAPI HTTP interface instead.
"""

from db.session import get_session
from exceptions.base import ValidationError
from exceptions.service_exceptions import  (
    ProjectNotFoundError,
    TaskNotFoundError,
)
from services.project_service import ProjectService
from services.task_service import TaskService


class TodoCLI:
    """CLI class for Todo List Application.

    DEPRECATED: This CLI will be removed in the next release.
    Use the FastAPI HTTP interface instead.
    """

    def __init__(self, project_service: ProjectService, task_service: TaskService):
        self.project_service = project_service
        self.task_service = task_service

        print("\n⚠️  WARNING: CLI interface is deprecated and will be removed in the next release.")
        print("   Please use the FastAPI HTTP interface instead.\n")

    def print_menu(self):
        """Display the main menu options."""
        print("\n📋 --- To-Do List Menu ---")
        print("1. List all projects")
        print("2. Create a new project")
        print("3. Edit a project")
        print("4. Delete a project")
        print("5. List tasks in a project")
        print("6. Add a new task")
        print("7. Edit a task")
        print("8. Change task status")
        print("9. Delete a task")
        print("0. Exit")

    def handle_list_projects(self):
        """Print all available projects."""

        projects = self.project_service.list_projects()
        if not projects:
            print("⚠️  No projects found.")
        else:
            for p in projects:
                print(f"[{p.id}] {p.name} - {p.description or '-'}")

    def handle_create_project(self):
        """Handle creation of a new project."""

        name = input("Project name: ")
        desc = input("Description (optional): ")
        project = self.project_service.create_project(name, desc)
        print(f"✅ Project '{project.name}' created successfully!")

    def handle_edit_project(self):
        """Handle editing an existing project."""

        pid = int(input("Enter project ID: "))
        name = input("New name (leave blank to keep current): ")
        desc = input("New description (leave blank to keep current): ")
        project = self.project_service.update_project(pid, name or None, desc or None)
        print(f"✅ Project {project.id} updated successfully!")

    def handle_delete_project(self):
        """Handle deleting a project."""

        pid = int(input("Enter project ID to delete: "))
        msg = self.project_service.delete_project(pid)
        print(msg)

    def handle_list_tasks(self):
        """List all tasks belonging to a project."""

        pid = int(input("Enter project ID: "))
        tasks = self.task_service.list_tasks(pid)

        if not tasks:
            print("⚠️  No tasks in this project.")

        else:
            for t in tasks:
                deadline = t.deadline.strftime("%Y-%m-%d") if t.deadline else "-"
                closed = f" (Closed: {t.closed_at.strftime('%Y-%m-%d %H:%M')})" if t.closed_at else ""
                print(f"[{t.id}] {t.title} - {t.status}{closed} (Deadline: {deadline})")

    def handle_create_task(self):
        """Handle creating a new task under a project."""

        pid = int(input("Enter project ID: "))
        title = input("Task title: ")
        desc = input("Description (optional): ")
        status = input("Status (todo/doing/done, optional): ")
        deadline = input("Deadline (YYYY-MM-DD, optional): ")
        task = self.task_service.create_task(pid, title, desc, status or None, deadline or None)
        print(f"✅ Task '{task.title}' added successfully!")

    def handle_edit_task(self):
        """Handle editing an existing task."""

        pid = int(input("Enter project ID: "))
        tid = int(input("Enter task ID: "))
        title = input("New title (leave blank to keep current): ")
        desc = input("New description (leave blank to keep current): ")
        status = input("New status (todo/doing/done, optional): ")
        deadline = input("New deadline (YYYY-MM-DD, optional): ")
        task = self.task_service.update_task(pid, tid, title or None, desc or None, status or None, deadline or None)
        print(f"✅ Task {task.id} updated successfully!")

    def handle_change_task_status(self):
        """Handle changing the status of an existing task."""

        pid = int(input("Enter project ID: "))
        tid = int(input("Enter task ID: "))
        status = input("Enter new status (todo/doing/done): ")
        task = self.task_service.change_task_status(pid, tid, status)
        print(f"🔄 Task {task.id} status changed to '{task.status}'.")

    def handle_delete_task(self):
        """Handle deleting a task."""

        pid = int(input("Enter project ID: "))
        tid = int(input("Enter task ID: "))
        msg = self.task_service.delete_task(pid, tid)
        print(msg)

    def run(self):
        """Main CLI loop."""
        try:
            while True:
                self.print_menu()
                choice = input("\nEnter your choice: ").strip()

                try:
                    if choice == "1":
                        self.handle_list_projects()
                    elif choice == "2":
                        self.handle_create_project()
                    elif choice == "3":
                        self.handle_edit_project()
                    elif choice == "4":
                        self.handle_delete_project()
                    elif choice == "5":
                        self.handle_list_tasks()
                    elif choice == "6":
                        self.handle_create_task()
                    elif choice == "7":
                        self.handle_edit_task()
                    elif choice == "8":
                        self.handle_change_task_status()
                    elif choice == "9":
                        self.handle_delete_task()
                    elif choice == "0":
                        print("👋 Goodbye!")
                        break
                    else:
                        print("❌ Invalid choice. Please try again.")

                except (ValidationError, ProjectNotFoundError, TaskNotFoundError) as e:
                    print(f"❌ Error: {e}")
                except Exception as e:
                    print(f"❌ Unexpected error: {e}")

        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")


def run_cli() -> None:
    """Run the CLI application."""

    session = get_session()

    try:
        project_service = ProjectService(session)
        task_service = TaskService(session)

        cli = TodoCLI(project_service, task_service)
        cli.run()
    finally:
        session.close()