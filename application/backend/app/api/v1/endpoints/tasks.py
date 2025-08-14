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
    """
    **Contrainte de l'exercice :** GET /tasks - Liste toutes les tâches
    
    Récupérer toutes les tâches avec filtrage, tri et pagination.
    
    **Filtres disponibles :**
    - `category_id` : Filtrer par catégorie
    - `priority` : Filtrer par priorité (Basse, Moyenne, Haute)
    - `status` : Filtrer par statut (En cours, Terminée, Reportée)
    - `search` : Recherche textuelle dans titre et description
    - `is_urgent` : Filtrer les tâches urgentes
    - `is_overdue` : Filtrer les tâches en retard
    
    **Tri disponible :**
    - `sort_by` : Champ de tri (title, priority, due_date, created_at, status, position)
    - `sort_order` : Ordre (asc, desc)
    
    **Pagination :**
    - `page` : Numéro de page (défaut: 1)
    - `size` : Taille de page (défaut: 20, max: 100)
    """
    return task_service.get_tasks_paginated(
        db, filters, sort, pagination["page"], pagination["size"]
    )

@router.post("/", 
    response_model=TaskResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Crée une nouvelle tâche"
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    **Contrainte de l'exercice :** POST /tasks - Crée une nouvelle tâche
    
    Créer une nouvelle tâche avec validation stricte des contraintes.
    
    **Validation Pydantic robuste :**
    - `title` : Obligatoire, minimum 3 caractères, maximum 200
    - `description` : Optionnelle, maximum 1000 caractères
    - `priority` : Obligatoire (Basse, Moyenne, Haute) - défaut: Moyenne
    - `due_date` : Obligatoire, doit être dans le futur
    - `category_id` : Obligatoire, doit correspondre à une catégorie existante
    """
    return task_service.create_task(db, task)

@router.get("/{task_id}", 
    response_model=TaskResponse,
    summary="Affiche une tâche par son ID"
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    **Contrainte de l'exercice :** GET /tasks/{id} - Affiche une tâche par son ID
    
    Récupérer une tâche spécifique avec toutes ses informations et sa catégorie.
    """
    return task_service.get_task_by_id(db, task_id)

@router.put("/{task_id}", 
    response_model=TaskResponse,
    summary="Modifie une tâche"
)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    **Contrainte de l'exercice :** PUT /tasks/{id} - Modifie une tâche
    
    Mettre à jour une tâche existante. Tous les champs sont optionnels.
    
    **Validation automatique :**
    - Si le statut passe à "Terminée", `completed_at` est automatiquement défini
    - Si le statut change de "Terminée" à autre chose, `completed_at` est remis à null
    - Le flag `is_urgent` est recalculé automatiquement
    """
    return task_service.update_task(db, task_id, task)

@router.delete("/{task_id}", 
    response_model=MessageResponse,
    summary="Supprime une tâche"
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    **Contrainte de l'exercice :** DELETE /tasks/{id} - Supprime une tâche
    
    Supprimer définitivement une tâche.
    """
    success = task_service.delete_task(db, task_id)
    return MessageResponse(
        message=f"Tâche {task_id} supprimée avec succès",
        success=success
    )

# Endpoints bonus pour fonctionnalités avancées

@router.patch("/{task_id}/complete", 
    response_model=TaskResponse,
    summary="Marquer une tâche comme terminée"
)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """
    **Bonus :** Marquer rapidement une tâche comme terminée.
    """
    return task_service.complete_task(db, task_id)

@router.get("/urgent/list", 
    response_model=List[TaskResponse],
    summary="Tâches urgentes"
)
def get_urgent_tasks(db: Session = Depends(get_db)):
    """
    **Bonus :** Récupérer toutes les tâches urgentes (échéance < 2 jours).
    """
    return task_service.get_urgent_tasks(db)

@router.get("/overdue/list", 
    response_model=List[TaskResponse],
    summary="Tâches en retard"
)
def get_overdue_tasks(db: Session = Depends(get_db)):
    """
    **Bonus :** Récupérer toutes les tâches en retard.
    """
    return task_service.get_overdue_tasks(db)

@router.get("/search/", 
    response_model=List[TaskResponse],
    summary="Recherche textuelle"
)
def search_tasks(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    db: Session = Depends(get_db)
):
    """
    **Bonus :** Recherche textuelle dans les tâches.
    
    Recherche dans les titres et descriptions des tâches.
    """
    return task_service.search_tasks(db, q)

@router.get("/statistics/", 
    response_model=TaskStatistics,
    summary="Statistiques des tâches"
)
def get_task_statistics(db: Session = Depends(get_db)):
    """
    **Bonus :** Obtenir des statistiques complètes sur les tâches.
    """
    return task_service.get_task_statistics(db)

@router.put("/reorder/", 
    response_model=MessageResponse,
    summary="Réorganiser les tâches"
)
def reorder_tasks(bulk_update: TaskBulkUpdate, db: Session = Depends(get_db)):
    """
    **Bonus :** Drag & drop - Réorganiser les positions des tâches.
    """
    success = task_service.reorder_tasks(db, bulk_update)
    return MessageResponse(
        message="Tâches réorganisées avec succès",
        success=success
    )