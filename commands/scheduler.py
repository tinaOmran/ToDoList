
"""Scheduler for periodic tasks using the schedule library."""

import time
import threading
from datetime import datetime

import schedule

from .autoclose_overdue import autoclose_overdue_tasks


class TaskScheduler:
    """Manages scheduled tasks for the Todo application."""

    def __init__(self):
        self.is_running = False
        self.thread = None
        self.stop_event = threading.Event()

    def setup_schedules(self):
        """Setup all scheduled tasks."""
        schedule.every(15).minutes.do(autoclose_overdue_tasks)

        print(" Schedules setup completed:")
        print("   - Auto-close overdue tasks: every 15 minutes")

    def run_scheduler(self):
        """Run the scheduler in a loop."""
        self.is_running = True
        self.setup_schedules()

        print(f" Task scheduler started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("   Press Ctrl+C in the terminal to stop the scheduler.")

        try:
            while self.is_running and not self.stop_event.is_set():
                try:
                    schedule.run_pending()
                    self.stop_event.wait(timeout=60)
                except Exception as e:
                    print(f"❌ Scheduler error: {e}")
                    time.sleep(60)
        except KeyboardInterrupt:
            print("\n Scheduler interrupted by user.")
        finally:
            self.is_running = False
            print("✅ Scheduler loop ended.")

    def start(self):
        """Start the scheduler in a background thread."""
        if self.is_running:
            print(" Scheduler is already running.")
            return

        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run_scheduler, daemon=False)
        self.thread.start()
        print("✅ Background scheduler started.")

    def stop(self):
        """Stop the scheduler gracefully."""
        if not self.is_running:
            print("ℹ Scheduler is not running.")
            return

        print(" Stopping scheduler gracefully...")
        self.is_running = False
        self.stop_event.set()

        if self.thread:
            self.thread.join(timeout=5)
            if self.thread.is_alive():
                print("⚠️ Scheduler thread did not stop in time.")
            else:
                print("✅ Scheduler stopped successfully.")

        schedule.clear()
        print(" All scheduled jobs cleared.")


# Global scheduler instance
scheduler = TaskScheduler()


def start_scheduler():
    """Start the global scheduler."""
    scheduler.start()


def stop_scheduler():
    """Stop the global scheduler."""
    scheduler.stop()


def run_once():
    """Run all scheduled tasks once (for testing)."""
    print(" Running scheduled tasks once...")
    schedule.run_all()
    print(" All scheduled tasks completed.")


if __name__ == "__main__":
    print("Starting Todo List Scheduler...")
    start_scheduler()

    try:
        while scheduler.is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Main thread interrupted.")
    finally:
        stop_scheduler()
    print("👋 Scheduler program ended.")
