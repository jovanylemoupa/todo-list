from typing import List
from sqlalchemy.orm import Session

from app.repositories.category_repository import category_repository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.core.exceptions import NotFoundException, ConflictException, BusinessLogicException

class CategoryService:
    def __init__(self):
        self.repository = category_repository

    def get_all_categories(self, db: Session) -> List[CategoryResponse]:
        categories_with_counts = self.repository.get_with_task_counts(db)
        
        result = []
        for category, tasks_count in categories_with_counts:
            category_data = {
                **category.__dict__,
                'tasks_count': tasks_count or 0
            }
            # Enlever les clés SQLAlchemy internes
            category_data.pop('_sa_instance_state', None)
            result.append(CategoryResponse(**category_data))
        
        return result

    def get_category_by_id(self, db: Session, category_id: int) -> CategoryResponse:
        """Récupérer une catégorie par son ID"""
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise NotFoundException(f"Catégorie avec l'ID {category_id} introuvable")
        
        return CategoryResponse.from_orm(category)

    def create_category(self, db: Session, category_data: CategoryCreate) -> CategoryResponse:
        """Créer une nouvelle catégorie avec validation métier"""
        # Vérifier l'unicité du nom
        if self.repository.name_exists(db, category_data.name):
            raise ConflictException(
                f"Une catégorie avec le nom '{category_data.name}' existe déjà"
            )
        
        # Créer la catégorie
        category_dict = category_data.dict()
        new_category = self.repository.create(db, category_dict)
        
        return CategoryResponse.from_orm(new_category)

    def update_category(self, db: Session, category_id: int, category_data: CategoryUpdate) -> CategoryResponse:
        """Mettre à jour une catégorie existante"""
        # Vérifier l'existence
        category = self.repository.get_by_id(db, category_id)
        if not category:
            raise NotFoundException(f"Catégorie avec l'ID {category_id} introuvable")
        
        # Vérifier l'unicité du nom si modifié
        if (category_data.name and 
            category_data.name != category.name and
            self.repository.name_exists(db, category_data.name, exclude_id=category_id)):
            raise ConflictException(
                f"Une catégorie avec le nom '{category_data.name}' existe déjà"
            )
        
        # Mettre à jour
        update_dict = category_data.dict(exclude_unset=True)
        updated_category = self.repository.update(db, category, update_dict)
        
        return CategoryResponse.from_orm(updated_category)

    def delete_category(self, db: Session, category_id: int) -> bool:
        """Supprimer une catégorie (si elle n'a pas de tâches)"""
        # Vérifier l'existence
        if not self.repository.exists(db, category_id):
            raise NotFoundException(f"Catégorie avec l'ID {category_id} introuvable")
        
        # Vérifier qu'elle n'a pas de tâches associées
        if self.repository.has_tasks(db, category_id):
            raise BusinessLogicException(
                "Impossible de supprimer une catégorie qui contient des tâches. "
                "Veuillez d'abord supprimer ou déplacer les tâches associées.",
                code="CATEGORY_HAS_TASKS"
            )
        
        return self.repository.delete(db, category_id)

# Instance globale du service
category_service = CategoryService()