from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

from app.repositories.task_repository import task_repository
from app.repositories.category_repository import category_repository
from app.models.task import Task
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskFilter, 
    TaskSort, TaskBulkUpdate, TaskStatistics
)
from app.schemas.common import PaginatedResponse
from app.core.exceptions import NotFoundException, ValidationException, BusinessLogicException

class TaskService:
    def __init__(self):
        self.task_repo = task_repository
        self.category_repo = category_repository

    def get_tasks_paginated(
        self, 
        db: Session, 
        filters: TaskFilter,
        sort: TaskSort,
        page: int = 1,
        size: int = 20
    ) -> PaginatedResponse[TaskResponse]:
        skip = (page - 1) * size
        tasks, total = self.task_repo.get_filtered(db, filters, sort, skip, size)
        
        # Mettre à jour l'urgence des tâches récupérées
        for task in tasks:
            task.update_urgency()
        
        # Calculer les métadonnées de pagination
        pages = (total + size - 1) // size
        has_next = page < pages
        has_prev = page > 1
        
        # Convertir en schémas de réponse
        task_responses = [TaskResponse.from_orm(task) for task in tasks]
        
        return PaginatedResponse(
            items=task_responses,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )

    def get_task_by_id(self, db: Session, task_id: int) -> TaskResponse:
        """Récupérer une tâche par son ID avec sa catégorie"""
        task = self.task_repo.get_with_category(db, task_id)
        if not task:
            raise NotFoundException(f"Tâche avec l'ID {task_id} introuvable")
        
        # Mettre à jour l'urgence
        task.update_urgency()
        
        return TaskResponse.from_orm(task)

    def create_task(self, db: Session, task_data: TaskCreate) -> TaskResponse:
        """Créer une nouvelle tâche avec toutes les validations"""
        # Vérifier que la catégorie existe
        if not self.category_repo.exists(db, task_data.category_id):
            raise ValidationException(
                f"La catégorie avec l'ID {task_data.category_id} n'existe pas",
                code="INVALID_CATEGORY"
            )
        
        # Calculer la position pour le drag & drop
        max_position_result = db.query(func.max(Task.position)).scalar()
        next_position = (max_position_result or 0) + 1
        
        # Préparer les données avec la position
        task_dict = task_data.dict()
        task_dict['position'] = next_position
        
        # Créer la tâche
        new_task = self.task_repo.create(db, task_dict)
        
        # Mettre à jour l'urgence
        new_task.update_urgency()
        
        # Recharger avec la catégorie pour la réponse
        task_with_category = self.task_repo.get_with_category(db, new_task.id)
        
        return TaskResponse.from_orm(task_with_category)

    def update_task(self, db: Session, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        """Mettre à jour une tâche existante"""
        # Vérifier l'existence de la tâche
        task = self.task_repo.get_by_id(db, task_id)
        if not task:
            raise NotFoundException(f"Tâche avec l'ID {task_id} introuvable")
        
        # Vérifier la catégorie si elle est modifiée
        if task_data.category_id and not self.category_repo.exists(db, task_data.category_id):
            raise ValidationException(
                f"La catégorie avec l'ID {task_data.category_id} n'existe pas",
                code="INVALID_CATEGORY"
            )
        
        # Préparer les données de mise à jour
        update_dict = task_data.dict(exclude_unset=True)
        
        # Logique spéciale pour le changement de statut
        if task_data.status:
            if task_data.status.value == "Terminée" and task.status.value != "Terminée":
                # Marquer comme terminée
                update_dict['completed_at'] = datetime.now(timezone.utc)
            elif task_data.status.value != "Terminée" and task.status.value == "Terminée":
                # Remettre en cours
                update_dict['completed_at'] = None
        
        # Mettre à jour la tâche
        updated_task = self.task_repo.update(db, task, update_dict)
        
        # Mettre à jour l'urgence
        updated_task.update_urgency()
        
        # Recharger avec la catégorie
        task_with_category = self.task_repo.get_with_category(db, updated_task.id)
        
        return TaskResponse.from_orm(task_with_category)

    def delete_task(self, db: Session, task_id: int) -> bool:
        if not self.task_repo.exists(db, task_id):
            raise NotFoundException(f"Tâche avec l'ID {task_id} introuvable")
        
        return self.task_repo.delete(db, task_id)

    def complete_task(self, db: Session, task_id: int) -> TaskResponse:
        """Marquer une tâche comme terminée"""
        completed_task = self.task_repo.mark_as_completed(db, task_id)
        if not completed_task:
            raise NotFoundException(f"Tâche avec l'ID {task_id} introuvable")
        
        # Recharger avec la catégorie
        task_with_category = self.task_repo.get_with_category(db, completed_task.id)
        
        return TaskResponse.from_orm(task_with_category)

    def get_urgent_tasks(self, db: Session) -> List[TaskResponse]:
        urgent_tasks = self.task_repo.get_urgent_tasks(db)
        return [TaskResponse.from_orm(task) for task in urgent_tasks]

    def get_overdue_tasks(self, db: Session) -> List[TaskResponse]:
        overdue_tasks = self.task_repo.get_overdue_tasks(db)
        return [TaskResponse.from_orm(task) for task in overdue_tasks]

    def search_tasks(self, db: Session, search_term: str) -> List[TaskResponse]:
        if len(search_term.strip()) < 2:
            raise ValidationException(
                "Le terme de recherche doit contenir au moins 2 caractères",
                code="SEARCH_TOO_SHORT"
            )
        
        found_tasks = self.task_repo.search_tasks(db, search_term.strip())
        return [TaskResponse.from_orm(task) for task in found_tasks]

    def get_task_statistics(self, db: Session) -> TaskStatistics:
        """Obtenir des statistiques complètes sur les tâches"""
        stats_data = self.task_repo.get_statistics(db)
        return TaskStatistics(**stats_data)

    def reorder_tasks(self, db: Session, bulk_update: TaskBulkUpdate) -> bool:
        # Vérifier que toutes les tâches existent
        for task_id in bulk_update.task_ids:
            if not self.task_repo.exists(db, task_id):
                raise NotFoundException(
                    f"Tâche avec l'ID {task_id} introuvable",
                    code="TASK_NOT_FOUND_IN_BULK"
                )
        
        # Créer le mapping des nouvelles positions
        position_updates = dict(zip(bulk_update.task_ids, bulk_update.positions))
        
        # Appliquer les mises à jour
        success = self.task_repo.update_positions(db, position_updates)
        
        if not success:
            raise BusinessLogicException(
                "Erreur lors de la réorganisation des tâches",
                code="REORDER_FAILED"
            )
        
        return success

    def update_all_urgency_flags(self, db: Session) -> int:
        """Mettre à jour tous les flags d'urgence (utilitaire pour tâche cron)"""
        self.task_repo.update_all_urgency_flags(db)
        return self.task_repo.count(db)

# Instance globale du service
task_service = TaskService()