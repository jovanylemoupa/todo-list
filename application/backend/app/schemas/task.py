from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from app.models.task import TaskPriority, TaskStatus
from .category import CategoryResponse

class TaskBase(BaseModel):
    """Schéma de base pour les tâches avec toutes les validations requises"""
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=200, 
        description="Titre de la tâche (minimum 3 caractères - OBLIGATOIRE)"
    )
    description: Optional[str] = Field(
        None, 
        max_length=1000, 
        description="Description détaillée de la tâche (optionnelle)"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MOYENNE, 
        description="Niveau de priorité (Basse, Moyenne, Haute)"
    )
    due_date: datetime = Field(
        ..., 
        description="Date et heure d'échéance (OBLIGATOIRE - doit être dans le futur)"
    )
    category_id: int = Field(
        ..., 
        gt=0, 
        description="ID de la catégorie (OBLIGATOIRE)"
    )

    @validator('title')
    def validate_title(cls, v):
        """Validation stricte du titre selon les contraintes"""
        if not v or not v.strip():
            raise ValueError('Le titre est obligatoire et ne peut pas être vide')
        
        title_clean = v.strip()
        if len(title_clean) < 3:
            raise ValueError('Le titre doit contenir au moins 3 caractères')
        
        return title_clean

    @validator('due_date')
    def validate_due_date(cls, v):
        """Validation de la date d'échéance (doit être future)"""
        if not v:
            raise ValueError('La date d\'échéance est obligatoire')
        
        # Vérifier que la date est dans le futur
        if v.date() <= date.today():
            raise ValueError('La date d\'échéance doit être dans le futur')
        
        return v

    @validator('description')
    def validate_description(cls, v):
        """Nettoie la description si fournie"""
        if v is not None:
            cleaned = v.strip()
            return cleaned if cleaned else None
        return v

class TaskCreate(TaskBase):
    """Schéma pour créer une nouvelle tâche"""
    pass

class TaskUpdate(BaseModel):
    """Schéma pour mettre à jour une tâche (tous les champs optionnels)"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = Field(None, gt=0)
    position: Optional[int] = Field(None, ge=0, description="Position pour le drag & drop")

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Le titre ne peut pas être vide')
            if len(v.strip()) < 3:
                raise ValueError('Le titre doit contenir au moins 3 caractères')
            return v.strip()
        return v

    @validator('due_date')
    def validate_due_date(cls, v):
        if v is not None and v.date() <= date.today():
            raise ValueError('La date d\'échéance doit être dans le futur')
        return v

class TaskResponse(TaskBase):
    """Schéma complet pour les réponses contenant une tâche"""
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    is_urgent: bool
    is_overdue: bool
    days_until_due: int
    position: int
    
    # Relation avec la catégorie incluse
    category: CategoryResponse

    class Config:
        from_attributes = True

class TaskFilter(BaseModel):
    """Schéma pour filtrer les tâches"""
    category_id: Optional[int] = Field(None, gt=0)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    search: Optional[str] = Field(None, min_length=2, max_length=100, description="Recherche textuelle")
    is_urgent: Optional[bool] = None
    is_overdue: Optional[bool] = None

class TaskSort(BaseModel):
    """Schéma pour le tri des tâches"""
    sort_by: str = Field(
        default="due_date",
        pattern=r"^(title|priority|due_date|created_at|status|position)$",  # CHANGÉ: regex → pattern
        description="Champ de tri"
    )
    sort_order: str = Field(
        default="asc", 
        pattern=r"^(asc|desc)$",  # CHANGÉ: regex → pattern
        description="Ordre de tri (asc/desc)"
    )

class TaskBulkUpdate(BaseModel):
    """Schéma pour la mise à jour en lot (drag & drop)"""
    task_ids: List[int] = Field(..., min_items=1)
    positions: List[int] = Field(..., min_items=1)

    @validator('positions')
    def validate_positions_length(cls, v, values):
        if 'task_ids' in values and len(v) != len(values['task_ids']):
            raise ValueError('Le nombre de positions doit correspondre au nombre de tâches')
        return v

class TaskStatistics(BaseModel):
    """Schéma pour les statistiques des tâches"""
    total: int
    by_status: dict
    by_priority: dict
    urgent_count: int
    overdue_count: int
    completed_today: int
    completion_rate: float