from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional
from datetime import datetime

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Schéma générique pour les réponses paginées"""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

class MessageResponse(BaseModel):
    """Schéma pour les messages de retour simples"""
    message: str
    success: bool = True
    # SUPPRIMÉ: timestamp pour éviter problème sérialisation

class ErrorResponse(BaseModel):
    """Schéma pour les réponses d'erreur"""
    error: str
    detail: str
    code: Optional[str] = None
    # SUPPRIMÉ: timestamp pour éviter problème sérialisation