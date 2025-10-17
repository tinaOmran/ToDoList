import os

MAX_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))

def validate_project(name, description, existing_projects):
    if len(name.split()) > 30 or len(description.split()) > 150:
        raise ValueError("نام یا توضیح بیش از حد طولانی است.")
    if any(p.name == name for p in existing_projects):
        raise ValueError("پروژه‌ای با این نام از قبل وجود دارد.")
    if len(existing_projects) >= MAX_PROJECTS:
        raise ValueError("تعداد پروژه‌ها از سقف مجاز بیشتر است.")


MAX_TASKS = int(os.getenv("MAX_NUMBER_OF_TASK", 10))

def validate_task(title, description, existing_tasks):
    if len(title.split()) > 30 or len(description.split()) > 150:
        raise ValueError("عنوان یا توضیح تسک بیش از حد طولانی است.")
    if len(existing_tasks) >= MAX_TASKS:
        raise ValueError("تعداد تسک‌ها از سقف مجاز بیشتر است.")