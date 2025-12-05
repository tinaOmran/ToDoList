# main.py
from services.project_manager import ProjectManager
from services.task_manager import TaskManager
from services.validators import validate_project, validate_task
import sys

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
    pm = ProjectManager()
    tm = TaskManager(pm)

    print("✨ برنامه مدیریت پروژه و تسک (In-Memory)")
    print("برای انتخاب عملیات از شماره‌های منو استفاده کنید.")

    while True:
        print_menu()
        choice = input("👉 گزینه مورد نظر را وارد کنید: ").strip()

        if choice == "0":
            print("👋 خروج از برنامه. داده‌ها در حافظه پاک می‌شوند.")
            sys.exit()

        elif choice == "1":
            print("\n📁 ایجاد پروژه جدید:")
            name = input("نام پروژه (حداکثر 30 واژه): ").strip()
            description = input("توضیح پروژه (حداکثر 150 واژه): ").strip()
            try:
                project = pm.create_project(name, description)
                print(f"✅ پروژه '{project.name}' با شناسه [{project.id}] ایجاد شد.")
            except ValueError as e:
                print("❌ خطا:", e)

        elif choice == "2":
            print("\n✏️ ویرایش پروژه:")
            project_id = get_int_input("شناسه پروژه برای ویرایش: ")
            new_name = input("نام جدید (خالی بگذار برای عدم تغییر): ").strip()
            new_description = input("توضیح جدید (خالی بگذار برای عدم تغییر): ").strip()
            try:
                project = pm.edit_project(project_id,
                                          new_name or None,
                                          new_description or None)
                print(f"✅ پروژه [{project.id}] به‌روزرسانی شد.")
            except ValueError as e:
                print("❌ خطا:", e)

        elif choice == "3":
            print("\n🗑 حذف پروژه:")
            project_id = get_int_input("شناسه پروژه برای حذف: ")
            confirm = input("آیا مطمئن هستید؟ (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    pm.delete_project(project_id)
                    print("✅ پروژه حذف شد (تسک‌هایش نیز حذف شدند).")
                except ValueError as e:
                    print("❌ خطا:", e)

        elif choice == "4":
            print("\n➕ افزودن تسک به پروژه:")
            project_id = get_int_input("شناسه پروژه: ")
            title = input("عنوان تسک (≤ 30 واژه): ").strip()
            description = input("توضیح تسک (≤ 150 واژه): ").strip()
            deadline = input("ددلاین (مثلاً 2025-11-01 یا خالی بگذار): ").strip() or None
            try:
                task = tm.add_task(project_id, title, description, deadline)
                print(f"✅ تسک [{task.id}] با عنوان '{task.title}' افزوده شد.")
            except ValueError as e:
                print("❌ خطا:", e)

        elif choice == "5":
            print("\n🔄 تغییر وضعیت تسک:")
            project_id = get_int_input("شناسه پروژه: ")
            task_id = get_int_input("شناسه تسک: ")
            print("مقادیر مجاز وضعیت: todo | doing | done")
            new_status = input("وضعیت جدید: ").strip()
            try:
                tm.change_status(project_id, task_id, new_status)
                print("✅ وضعیت تسک تغییر کرد.")
            except ValueError as e:
                print("❌ خطا:", e)

        elif choice == "6":
            print("\n📝 ویرایش تسک:")
            project_id = get_int_input("شناسه پروژه: ")
            task_id = get_int_input("شناسه تسک: ")
            new_title = input("عنوان جدید (خالی بگذار برای عدم تغییر): ").strip()
            new_description = input("توضیح جدید (خالی بگذار برای عدم تغییر): ").strip()
            new_deadline = input("ددلاین جدید (YYYY-MM-DD یا خالی بگذار): ").strip() or None
            try:
                tm.edit_task(project_id, task_id,
                             new_title or None,
                             new_description or None,
                             new_deadline)
                print("✅ تسک ویرایش شد.")
            except ValueError as e:
                print("❌ خطا:", e)

        elif choice == "7":
            print("\n❌ حذف تسک:")
            project_id = get_int_input("شناسه پروژه: ")
            task_id = get_int_input("شناسه تسک: ")
            confirm = input("آیا مطمئن هستید؟ (y/n): ").strip().lower()
            if confirm == "y":
                try:
                    tm.delete_task(project_id, task_id)
                    print("✅ تسک حذف شد.")
                except ValueError as e:
                    print("❌ خطا:", e)

        elif choice == "8":
            print("\n📋 لیست پروژه‌ها:")
            projects = pm.list_projects()
            if not projects:
                print("❌ هیچ پروژه‌ای وجود ندارد.")
            else:
                for p in projects:
                    print(f"[{p.id}] {p.name} - {p.description} ({len(p.tasks)} تسک)")

        elif choice == "9":
            print("\n📦 لیست تسک‌های پروژه:")
            project_id = get_int_input("شناسه پروژه: ")
            tasks = tm.list_tasks_by_project(project_id)
            if not tasks:
                print("❌ تسکی برای این پروژه وجود ندارد.")
            else:
                for t in tasks:
                    print(f"[{t.id}] {t.title} | وضعیت: {t.status} | deadline={t.deadline}")
        else:
            print("❌ گزینه نامعتبر است. عدد 0 تا 9 را وارد کنید.")

if __name__ == "__main__":
    run_cli()

