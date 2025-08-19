from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone  
import enum

from .base import BaseModel

class TaskPriority(str, enum.Enum):
    BASSE = "Basse"
    MOYENNE = "Moyenne"
    HAUTE = "Haute"

class TaskStatus(str, enum.Enum):
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    REPORTEE = "Reportée"

class Task(BaseModel):
    __tablename__ = "tasks"
    
    title = Column(String(200), nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=False)
    
    description = Column(Text, nullable=True)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MOYENNE)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.EN_COURS)
    
    completed_at = Column(DateTime(timezone=True), nullable=True)
    is_urgent = Column(Boolean, default=False) 
    position = Column(Integer, default=0) 

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    category = relationship("Category", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(title={self.title}, priority={self.priority})>"
    
    @property
    def is_overdue(self) -> bool:
        """Vérifie si la tâche est en retard"""
        if self.status == TaskStatus.TERMINEE:
            return False
        
        now = datetime.now(timezone.utc)
        
        if self.due_date.tzinfo is None:
            due_date_aware = self.due_date.replace(tzinfo=timezone.utc)
        else:
            due_date_aware = self.due_date
            
        return due_date_aware < now
    
    @property
    def days_until_due(self) -> int:
        now = datetime.now(timezone.utc)
        
        if self.due_date.tzinfo is None:
            due_date_aware = self.due_date.replace(tzinfo=timezone.utc)
        else:
            due_date_aware = self.due_date
            
        delta = due_date_aware.date() - now.date()
        return delta.days
    
    def update_urgency(self):
        if self.status != TaskStatus.TERMINEE:
            self.is_urgent = self.days_until_due <= 2
        else:
            self.is_urgent = False