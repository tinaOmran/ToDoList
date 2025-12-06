from sqlalchemy.orm import Session
from models.project import Project
from typing import Optional, List


class ProjectRepository:
    """Repository for handling Project database operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        """Create a new project."""
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get a project by its ID."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def get_by_name(self, name: str) -> Optional[Project]:
        """Get a project by its name."""
        return self.db.query(Project).filter(Project.name == name).first()

    def get_all(self) -> List[Project]:
        """Get all projects."""
        return self.db.query(Project).all()

    def update(self, project: Project) -> Project:
        """Update an existing project."""
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project_id: int) -> bool:
        """Delete a project by ID."""
        project = self.get_by_id(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """Count total number of projects."""
        return self.db.query(Project).count()