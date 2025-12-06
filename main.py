# main.py
import sys
import os

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.session import get_session, SessionLocal
from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository
from services.project_manager import ProjectManager
from services.task_manager import TaskManager
from exceptions.service_exceptions import (
    ProjectNotFoundError,
    TaskNotFoundError,
    ProjectNameExistsError,
    ProjectLimitExceededError,
    TaskLimitExceededError
)
from exceptions.base import ValidationError


def print_menu():
    print("\n=== منوی اصلی ToDoList ===")
    print("1. ایجاد پروژه جدید")
    print("2. ویرایش پروژه")
    print("3. حذف پروژه")
    print("4. افزودن تسک به پروژه")
    print("5. تغییر وضعیت تسک")
    print("6. ویرایش تسک")
    print("7. حذف تسک")
    print("8. نمایش لیست پروژه‌ها")
    print("9. نمایش تسک‌های یک پروژه")
    print("0. خروج")
    print("==============================")


def get_int_input(prompt: str):
    """ورودی عددی با کنترل خطا"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ لطفاً فقط عدد وارد کنید.")


def run_cli():
    # ایجاد session دیتابیس
    db = get_session()  # یا SessionLocal() بسته به تعریف شما

    try:
        # ایجاد repository ها
        project_repo = ProjectRepository(db)
        task_repo = TaskRepository(db)

        # ایجاد سرویس‌ها با dependency injection
        project_service = ProjectManager(project_repo)
        task_service = TaskManager(task_repo, project_repo)

        print("✨ برنامه مدیریت پروژه و تسک (PostgreSQL)")
        print("برای انتخاب عملیات از شماره‌های منو استفاده کنید.")

        while True:
            print_menu()
            choice = input("👉 گزینه مورد نظر را وارد کنید: ").strip()

            if choice == "0":
                print("👋 خروج از برنامه.")
                db.close()
                sys.exit()

            elif choice == "1":
                print("\n📁 ایجاد پروژه جدید:")
                name = input("نام پروژه (حداکثر 30 واژه): ").strip()
                description = input("توضیح پروژه (حداکثر 150 واژه): ").strip()
                try:
                    project = project_service.create_project(name, description)
                    print(f"✅ پروژه '{project.name}' با شناسه [{project.id}] ایجاد شد.")
                except (ProjectNameExistsError, ProjectLimitExceededError, ValidationError) as e:
                    print(f"❌ خطا: {e}")

            elif choice == "2":
                print("\n✏️ ویرایش پروژه:")
                project_id = get_int_input("شناسه پروژه برای ویرایش: ")
                new_name = input("نام جدید (خالی بگذار برای عدم تغییر): ").strip()
                new_description = input("توضیح جدید (خالی بگذار برای عدم تغییر): ").strip()
                try:
                    project = project_service.update_project(
                        project_id,
                        new_name or None,
                        new_description or None
                    )
                    print(f"✅ پروژه [{project.id}] به‌روزرسانی شد.")
                except (ProjectNotFoundError, ProjectNameExistsError, ValidationError) as e:
                    print(f"❌ خطا: {e.message}")

            elif choice == "3":
                print("\n🗑 حذف پروژه:")
                project_id = get_int_input("شناسه پروژه برای حذف: ")
                confirm = input("آیا مطمئن هستید؟ (y/n): ").strip().lower()
                if confirm == "y":
                    try:
                        project_service.delete_project(project_id)
                        print("✅ پروژه حذف شد.")
                    except ProjectNotFoundError as e:
                        print(f"❌ خطا: {e}")

            elif choice == "4":
                print("\n➕ افزودن تسک به پروژه:")
                project_id = get_int_input("شناسه پروژه: ")
                title = input("عنوان تسک (≤ 30 واژه): ").strip()
                description = input("توضیح تسک (≤ 150 واژه): ").strip()
                deadline = input("ددلاین (مثلاً 2025-11-01 یا خالی بگذار): ").strip() or None
                try:
                    task = task_service.create_task(project_id, title, description, deadline)
                    print(f"✅ تسک [{task.id}] با عنوان '{task.title}' افزوده شد.")
                except (ProjectNotFoundError, TaskLimitExceededError, ValidationError) as e:
                    print(f"❌ خطا: {e}")

            elif choice == "5":
                print("\n🔄 تغییر وضعیت تسک:")
                project_id = get_int_input("شناسه پروژه: ")
                task_id = get_int_input("شناسه تسک: ")
                print("مقادیر مجاز وضعیت: todo | doing | done")
                new_status = input("وضعیت جدید: ").strip()
                try:
                    task_service.change_status(project_id, task_id, new_status)
                    print("✅ وضعیت تسک تغییر کرد.")
                except (ProjectNotFoundError, TaskNotFoundError, ValidationError) as e:
                    print(f"❌ خطا: {e}")

            elif choice == "6":
                print("\n📝 ویرایش تسک:")
                project_id = get_int_input("شناسه پروژه: ")
                task_id = get_int_input("شناسه تسک: ")
                new_title = input("عنوان جدید (خالی بگذار برای عدم تغییر): ").strip()
                new_description = input("توضیح جدید (خالی بگذار برای عدم تغییر): ").strip()
                new_deadline = input("ددلاین جدید (YYYY-MM-DD یا خالی بگذار): ").strip() or None
                try:
                    task_service.update_task(
                        project_id,
                        task_id,
                        new_title or None,
                        new_description or None,
                        new_deadline
                    )
                    print("✅ تسک ویرایش شد.")
                except (ProjectNotFoundError, TaskNotFoundError, ValidationError) as e:
                    print(f"❌ خطا: {e}")

            elif choice == "7":
                print("\n❌ حذف تسک:")
                project_id = get_int_input("شناسه پروژه: ")
                task_id = get_int_input("شناسه تسک: ")
                confirm = input("آیا مطمئن هستید؟ (y/n): ").strip().lower()
                if confirm == "y":
                    try:
                        task_service.delete_task(project_id, task_id)
                        print("✅ تسک حذف شد.")
                    except (ProjectNotFoundError, TaskNotFoundError) as e:
                        print(f"❌ خطا: {e.message}")

            elif choice == "8":
                print("\n📋 لیست پروژه‌ها:")
                projects = project_service.get_all_projects()
                if not projects:
                    print("❌ هیچ پروژه‌ای وجود ندارد.")
                else:
                    for p in projects:
                        # تعداد تسک‌ها را محاسبه کنید
                        #task_count = task_service.count_tasks_by_project(p.id)

                        # در main.py خط ۱۷۱ را اصلاح کنید:
                        # ❌ قدیمی:
                        # task_count = task_service.count_tasks_by_project(p.id)

                        # ✅ جدید (اگر می‌خواهید تعداد تسک‌ها را نمایش دهید):
                        task_count = len(p.tasks) if hasattr(p, 'tasks') else 0

                        # یا ساده‌تر:
                        #print(f"[{p.id}] {p.name} - {p.description}")
                        # تعداد تسک‌ها را نشان ندهید اگر متد وجود ندارد
                        print(f"[{p.id}] {p.name} - {p.description} ({task_count} تسک)")

            elif choice == "9":
                print("\n📦 لیست تسک‌های پروژه:")
                project_id = get_int_input("شناسه پروژه: ")
                try:
                    tasks = task_service.get_tasks_by_project(project_id)
                    if not tasks:
                        print("❌ تسکی برای این پروژه وجود ندارد.")
                    else:
                        for t in tasks:
                            print(f"[{t.id}] {t.title} | وضعیت: {t.status} | deadline={t.deadline}")
                except ProjectNotFoundError as e:
                    print(f"❌ خطا: {e.message}")

            else:
                print("❌ گزینه نامعتبر است. عدد 0 تا 9 را وارد کنید.")

    except Exception as e:
        print(f"❌ خطای سیستمی: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # بستن session دیتابیس
        db.close()


if __name__ == "__main__":
    run_cli()