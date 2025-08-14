from fastapi import HTTPException, status
from typing import Optional

class TodoException(HTTPException):
    """Exception de base pour l'application Todo"""
    def __init__(self, status_code: int, detail: str, code: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.code = code

class NotFoundException(TodoException):
    """Exception pour les ressources non trouvées"""
    def __init__(self, detail: str = "Ressource non trouvée", code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail, 
            code=code
        )

class ValidationException(TodoException):
    """Exception pour les erreurs de validation"""
    def __init__(self, detail: str = "Données invalides", code: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=detail, 
            code=code
        )

class ConflictException(TodoException):
    """Exception pour les conflits (ex: nom déjà existant)"""
    def __init__(self, detail: str = "Conflit détecté", code: str = "CONFLICT"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail, 
            code=code
        )

class BusinessLogicException(TodoException):
    """Exception pour les erreurs de logique métier"""
    def __init__(self, detail: str = "Erreur de logique métier", code: str = "BUSINESS_ERROR"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=detail, 
            code=code
        )