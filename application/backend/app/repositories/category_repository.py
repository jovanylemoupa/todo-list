from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from .base import BaseRepository
from app.models.category import Category
from app.models.task import Task

class CategoryRepository(BaseRepository[Category]):
    """Repository pour les opérations spécifiques aux catégories"""
    
    def __init__(self):
        super().__init__(Category)

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        """Récupérer une catégorie par son nom (insensible à la casse)"""
        return db.query(Category).filter(
            func.lower(Category.name) == func.lower(name)
        ).first()

    def get_with_task_counts(self, db: Session) -> List[tuple]:
        """Récupérer toutes les catégories avec le nombre de tâches associées"""
        return db.query(
            Category,
            func.count(Task.id).label('tasks_count')
        ).outerjoin(Task).group_by(Category.id).all()

    def name_exists(self, db: Session, name: str, exclude_id: Optional[int] = None) -> bool:
        """Vérifier si un nom de catégorie existe déjà"""
        query = db.query(Category).filter(
            func.lower(Category.name) == func.lower(name)
        )
        
        if exclude_id:
            query = query.filter(Category.id != exclude_id)
        
        return query.first() is not None

    def has_tasks(self, db: Session, category_id: int) -> bool:
        """Vérifier si une catégorie contient des tâches"""
        return db.query(Task).filter(Task.category_id == category_id).first() is not None

# Instance globale du repository
category_repository = CategoryRepository()