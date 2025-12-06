"""Command to auto-close overdue tasks."""

from datetime import datetime
from db.session import get_session
from repositories.task_repository import TaskRepository


def autoclose_overdue_tasks():
    """
    Close tasks that are overdue (deadline passed) and not done.
    Uses the model's business logic for consistency.
    """
    session = get_session()
    task_repo = TaskRepository(session)

    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"🕐 [{timestamp}] Checking for overdue tasks...")


        overdue_before = task_repo.get_overdue_tasks()

        if not overdue_before:
            print("   ✅ No overdue tasks found.")
            return 0

        print(f" Found {len(overdue_before)} overdue task(s)")

        closed_count = task_repo.close_overdue_tasks()

        if closed_count > 0:
            print(f" Successfully auto-closed {closed_count} overdue task(s)")
        else:
            print("    No tasks were closed (possible errors)")

        return closed_count

    except Exception as e:
        print(f"❌ Error in autoclose_overdue_tasks: {e}")
        session.rollback()
        return 0
    finally:
        session.close()


def main():
    """Entry point for command line execution."""

    print(" Starting auto-close overdue tasks job...")
    result = autoclose_overdue_tasks()

    if result > 0:
        print(f"✅ Auto-close job completed. Closed {result} task(s).")
    else:
        print("✅ Auto-close job completed. No tasks were closed.")

    return result


if __name__ == "__main__":
    main()