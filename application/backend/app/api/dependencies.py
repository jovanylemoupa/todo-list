from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.task import TaskFilter, TaskSort
from app.config.settings import settings

def get_task_filters(
    category_id: int = None,
    priority: str = None,
    status: str = None,
    search: str = None,
    is_urgent: bool = None,
    is_overdue: bool = None
) -> TaskFilter:
    """Dépendance pour extraire les filtres des paramètres de requête"""
    return TaskFilter(
        category_id=category_id,
        priority=priority,
        status=status,
        search=search,
        is_urgent=is_urgent,
        is_overdue=is_overdue
    )

def get_task_sort(
    sort_by: str = "due_date",
    sort_order: str = "asc"
) -> TaskSort:
    """Dépendance pour extraire les paramètres de tri"""
    return TaskSort(sort_by=sort_by, sort_order=sort_order)

def get_pagination_params(
    page: int = 1,
    size: int = settings.DEFAULT_PAGE_SIZE
):
    """Dépendance pour les paramètres de pagination"""
    if page < 1:
        page = 1
    if size < 1 or size > settings.MAX_PAGE_SIZE:
        size = settings.DEFAULT_PAGE_SIZE
    
    return {"page": page, "size": size}