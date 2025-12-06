"""
Configuration module for the ToDoList.
Loads environment variables from .env in project root if it exists,
otherwise from the system environment.
"""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


# Load .env from project root if it exists
_env_path = Path(__file__).resolve().parents[2] / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()


@dataclass(frozen=True)
class Config:
    """Immutable configuration values for the ToDoList."""
    MAX_NUMBER_OF_PROJECT: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", "50"))
    MAX_NUMBER_OF_TASK: int = int(os.getenv("MAX_NUMBER_OF_TASK", "500"))
    DEFAULT_TASK_STATUS: str = os.getenv("DEFAULT_TASK_STATUS", "todo")


# Global configuration instance
config = Config()