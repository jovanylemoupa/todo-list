from typing import List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc, func
from datetime import datetime, timedelta

from .base import BaseRepository
from app.models.task import Task, TaskPriority, TaskStatus
from app.schemas.task import TaskFilter, TaskSort

class TaskRepository(BaseRepository[Task]):
    """Repository pour les opérations spécifiques aux tâches"""
    
    def __init__(self):
        super().__init__(Task)

    def get_with_category(self, db: Session, task_id: int) -> Optional[Task]:
        """Récupérer une tâche avec sa catégorie chargée"""
        return db.query(Task).options(
            joinedload(Task.category)
        ).filter(Task.id == task_id).first()

    def get_filtered(
        self, 
        db: Session, 
        filters: TaskFilter,
        sort: TaskSort,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Task], int]:
        """Récupérer les tâches avec filtres, tri et pagination"""
        query = db.query(Task).options(joinedload(Task.category))
        
        # Application des filtres
        if filters.category_id:
            query = query.filter(Task.category_id == filters.category_id)
        
        if filters.priority:
            query = query.filter(Task.priority == filters.priority)
            
        if filters.status:
            query = query.filter(Task.status == filters.status)
            
        if filters.is_urgent is not None:
            query = query.filter(Task.is_urgent == filters.is_urgent)
            
        if filters.search:
            search_pattern = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern)
                )
            )
        
        # Compter le total avant pagination
        total = query.count()
        
        # Application du tri
        if hasattr(Task, sort.sort_by):
            order_func = asc if sort.sort_order == "asc" else desc
            query = query.order_by(order_func(getattr(Task, sort.sort_by)))
        
        # Pagination
        tasks = query.offset(skip).limit(limit).all()
        
        return tasks, total

    def get_urgent_tasks(self, db: Session) -> List[Task]:
        """Récupérer les tâches urgentes (échéance < 2 jours et non terminées)"""
        return db.query(Task).options(joinedload(Task.category)).filter(
            and_(
                Task.is_urgent == True,
                Task.status != TaskStatus.TERMINEE
            )
        ).order_by(Task.due_date).all()

    def get_overdue_tasks(self, db: Session) -> List[Task]:
        """Récupérer les tâches en retard"""
        now = datetime.now()
        return db.query(Task).options(joinedload(Task.category)).filter(
            and_(
                Task.due_date < now,
                Task.status != TaskStatus.TERMINEE
            )
        ).order_by(Task.due_date).all()

    def search_tasks(self, db: Session, search_term: str, limit: int = 10) -> List[Task]:
        """Recherche textuelle dans les tâches (bonus)"""
        search_pattern = f"%{search_term}%"
        return db.query(Task).options(joinedload(Task.category)).filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        ).limit(limit).all()

    def mark_as_completed(self, db: Session, task_id: int) -> Optional[Task]:
        """Marquer une tâche comme terminée"""
        task = self.get_by_id(db, task_id)
        if task and task.status != TaskStatus.TERMINEE:
            task.status = TaskStatus.TERMINEE
            task.completed_at = datetime.now()
            task.is_urgent = False
            db.commit()
            db.refresh(task)
        return task

    def update_positions(self, db: Session, position_updates: Dict[int, int]) -> bool:
        """Mettre à jour les positions de plusieurs tâches (drag & drop)"""
        try:
            for task_id, position in position_updates.items():
                task = self.get_by_id(db, task_id)
                if task:
                    task.position = position
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False

    def get_statistics(self, db: Session) -> dict:
        """Obtenir des statistiques complètes sur les tâches"""
        total_tasks = db.query(Task).count()
        
        # Statistiques par statut
        status_stats = db.query(
            Task.status,
            func.count(Task.id).label('count')
        ).group_by(Task.status).all()
        
        # Statistiques par priorité
        priority_stats = db.query(
            Task.priority,
            func.count(Task.id).label('count')
        ).group_by(Task.priority).all()
        
        # Tâches urgentes
        urgent_count = db.query(Task).filter(Task.is_urgent == True).count()
        
        # Tâches en retard
        overdue_count = len(self.get_overdue_tasks(db))
        
        # Tâches terminées aujourd'hui
        today = datetime.now().date()
        completed_today = db.query(Task).filter(
            and_(
                Task.status == TaskStatus.TERMINEE,
                func.date(Task.completed_at) == today
            )
        ).count()
        
        # Taux de completion
        completed_count = db.query(Task).filter(Task.status == TaskStatus.TERMINEE).count()
        completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total': total_tasks,
            'by_status': {stat.status.value: stat.count for stat in status_stats},
            'by_priority': {stat.priority.value: stat.count for stat in priority_stats},
            'urgent_count': urgent_count,
            'overdue_count': overdue_count,
            'completed_today': completed_today,
            'completion_rate': round(completion_rate, 2)
        }

    def update_all_urgency_flags(self, db: Session):
        """Mettre à jour tous les flags d'urgence (tâche périodique)"""
        urgent_threshold = datetime.now() + timedelta(days=2)
        
        # Marquer comme urgent
        db.query(Task).filter(
            and_(
                Task.due_date <= urgent_threshold,
                Task.status != TaskStatus.TERMINEE,
                Task.is_urgent == False
            )
        ).update({Task.is_urgent: True})
        
        # Retirer le flag urgent si plus valide
        db.query(Task).filter(
            and_(
                or_(
                    Task.due_date > urgent_threshold,
                    Task.status == TaskStatus.TERMINEE
                ),
                Task.is_urgent == True
            )
        ).update({Task.is_urgent: False})
        
        db.commit()

# Instance globale du repository
task_repository = TaskRepository()