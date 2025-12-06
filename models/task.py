# models/task.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from db.base import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "task"  # نام جدول با FK هماهنگ

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    deadline: Mapped[datetime] = mapped_column(nullable=True)
    #project_id: Mapped[int] = mapped_column(sa.ForeignKey("project.id") , ondelete="CASCADE")  # باید کوچک و همخوان با Project.__tablename__
    # در migration یا مدل task.py

    #project_id = mapped_column(sa.ForeignKey("project.id", ondelete="CASCADE"))
    project_id: Mapped[int] = mapped_column(
        sa.ForeignKey("project.id", ondelete="CASCADE"),  # ondelete اینجاست
        nullable=False
    )
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    status: Mapped[str] = mapped_column(default="todo")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
