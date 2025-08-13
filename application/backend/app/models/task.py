from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import enum

from .base import BaseModel

class TaskPriority(str, enum.Enum):
    """Énumération pour les niveaux de priorité"""
    BASSE = "Basse"
    MOYENNE = "Moyenne"
    HAUTE = "Haute"

class TaskStatus(str, enum.Enum):
    """Énumération pour les statuts de tâche"""
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    REPORTEE = "Reportée"

class Task(BaseModel):
    """
    Modèle pour les tâches
    """
    __tablename__ = "tasks"
    
    # Champs obligatoires selon les contraintes de l'exercice
    title = Column(String(200), nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=False)
    
    # Champs optionnels avec valeurs par défaut
    description = Column(Text, nullable=True)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MOYENNE)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.EN_COURS)
    
    # Champs de gestion et métadonnées
    completed_at = Column(DateTime(timezone=True), nullable=True)
    is_urgent = Column(Boolean, default=False)  # Calculé automatiquement
    position = Column(Integer, default=0)  # Pour le drag & drop (bonus)
    
    # Clé étrangère obligatoire
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # Relations
    category = relationship("Category", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(title={self.title}, priority={self.priority})>"
    
    @property
    def is_overdue(self) -> bool:
        """Vérifie si la tâche est en retard"""
        if self.status == TaskStatus.TERMINEE:
            return False
        return self.due_date < datetime.now()
    
    @property
    def days_until_due(self) -> int:
        """Nombre de jours jusqu'à l'échéance"""
        delta = self.due_date.date() - datetime.now().date()
        return delta.days
    
    def update_urgency(self):
        """Met à jour le statut d'urgence (< 2 jours)"""
        if self.status != TaskStatus.TERMINEE:
            self.is_urgent = self.days_until_due <= 2
        else:
            self.is_urgent = False