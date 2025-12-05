import os

# Maximum number of projects allowed (from environment or default 5)
MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))

# Maximum number of tasks allowed per project (from environment or default 10)
MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 10))


def validate_project(name, description, existing_projects):
    """
    Validate project details before creation.

    Args:
        name (str): The name of the project.
        description (str): The description of the project.
        existing_projects (list): List of existing project objects.

    Raises:
        ValueError: If the name or description is too long,
                    if a project with the same name exists,
                    or if the number of projects exceeds MAX_PROJECTS.
    """
    # Check length of name and description
    if len(name.split()) > 30 or len(description.split()) > 150:
        raise ValueError("نام یا توضیح بیش از حد طولانی است.")

    # Check for duplicate project name
    if any(p.name == name for p in existing_projects):
        raise ValueError("پروژه‌ای با این نام از قبل وجود دارد.")

    # Check if number of projects exceeds maximum allowed
    if len(existing_projects) >= MAX_PROJECTS:
        raise ValueError("تعداد پروژه‌ها از سقف مجاز بیشتر است.")


def validate_task(title, description, existing_tasks):
    """
    Validate task details before creation.

    Args:
        title (str): The title of the task.
        description (str): The description of the task.
        existing_tasks (list): List of existing task objects.

    Raises:
        ValueError: If title or description is too long,
                    or if the number of tasks exceeds MAX_TASKS.
    """
    # Check length of title and description
    if len(title.split()) > 30 or len(description.split()) > 150:
        raise ValueError("عنوان یا توضیح تسک بیش از حد طولانی است.")

    # Check if number of tasks exceeds maximum allowed
    if len(existing_tasks) >= MAX_TASKS:
        raise ValueError("تعداد تسک‌ها از سقف مجاز بیشتر است.")
