# models/project.py
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

class Project(Base):
    __tablename__ = "project"  # با FK در Task هماهنگ

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project")
