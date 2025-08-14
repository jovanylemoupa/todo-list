from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.common import MessageResponse
from app.services.category_service import category_service
from app.core.exceptions import TodoException

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryResponse], summary="Liste des catégories")
def get_categories(db: Session = Depends(get_db)):
    """
    Récupérer toutes les catégories disponibles avec le nombre de tâches associées.
    
    **Contrainte de l'exercice :** GET /categories - Liste les catégories possibles (Perso, Pro...)
    """
    return category_service.get_all_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse, summary="Détails d'une catégorie")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une catégorie spécifique par son ID.
    """
    return category_service.get_category_by_id(db, category_id)

@router.post("/", 
    response_model=CategoryResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Créer une catégorie"
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle catégorie.
    
    **Validation Pydantic :**
    - Nom obligatoire (1-50 caractères)
    - Description optionnelle (max 200 caractères)  
    - Couleur au format hexadécimal (défaut: #007bff)
    """
    return category_service.create_category(db, category)

@router.put("/{category_id}", response_model=CategoryResponse, summary="Modifier une catégorie")
def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: Session = Depends(get_db)
):
    """
    Mettre à jour une catégorie existante.
    
    Tous les champs sont optionnels en mise à jour.
    """
    return category_service.update_category(db, category_id, category)

@router.delete("/{category_id}", 
    response_model=MessageResponse,
    summary="Supprimer une catégorie"
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une catégorie.
    
    **Contrainte métier :** Une catégorie ne peut être supprimée que si elle ne contient aucune tâche.
    """
    success = category_service.delete_category(db, category_id)
    return MessageResponse(
        message=f"Catégorie {category_id} supprimée avec succès",
        success=success
    )