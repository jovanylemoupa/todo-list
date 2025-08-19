from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.api.dependencies import get_task_filters, get_task_sort, get_pagination_params
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskBulkUpdate, 
    TaskStatistics, TaskFilter, TaskSort
)
from app.schemas.common import PaginatedResponse, MessageResponse
from app.services.task_service import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", 
    response_model=PaginatedResponse[TaskResponse],
    summary="Liste toutes les tâches"
)
def get_tasks(
    db: Session = Depends(get_db),
    filters: TaskFilter = Depends(get_task_filters),
    sort: TaskSort = Depends(get_task_sort),
    pagination = Depends(get_pagination_params)
):
    return task_service.get_tasks_paginated(
        db, filters, sort, pagination["page"], pagination["size"]
    )

@router.post("/", 
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Crée une nouvelle tâche"
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task)

@router.get("/{task_id}", 
    response_model=TaskResponse,
    summary="Affiche une tâche par son ID"
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task_by_id(db, task_id)

@router.put("/{task_id}", 
    response_model=TaskResponse,
    summary="Modifie une tâche"
)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, task)

@router.delete("/{task_id}", 
    response_model=MessageResponse,
    summary="Supprime une tâche"
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = task_service.delete_task(db, task_id)
    return MessageResponse(
        message=f"Tâche {task_id} supprimée avec succès",
        success=success
    )

@router.patch("/{task_id}/complete", 
    response_model=TaskResponse,
    summary="Marquer une tâche comme terminée"
)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.complete_task(db, task_id)

@router.get("/urgent/list", 
    response_model=List[TaskResponse],
    summary="Tâches urgentes"
)
def get_urgent_tasks(db: Session = Depends(get_db)):
    return task_service.get_urgent_tasks(db)

@router.get("/overdue/list", 
    response_model=List[TaskResponse],
    summary="Tâches en retard"
)
def get_overdue_tasks(db: Session = Depends(get_db)):
    return task_service.get_overdue_tasks(db)

@router.get("/search/", 
    response_model=List[TaskResponse],
    summary="Recherche textuelle"
)
def search_tasks(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    db: Session = Depends(get_db)
):
    return task_service.search_tasks(db, q)

@router.get("/statistics/", 
    response_model=TaskStatistics,
    summary="Statistiques des tâches"
)
def get_task_statistics(db: Session = Depends(get_db)):
    return task_service.get_task_statistics(db)

@router.put("/reorder/", 
    response_model=MessageResponse,
    summary="Réorganiser les tâches"
)
def reorder_tasks(bulk_update: TaskBulkUpdate, db: Session = Depends(get_db)):
    success = task_service.reorder_tasks(db, bulk_update)
    return MessageResponse(
        message="Tâches réorganisées avec succès",
        success=success
    )