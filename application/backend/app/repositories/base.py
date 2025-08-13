from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    """Repository de base avec les opérations CRUD communes"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_data: Dict[str, Any]) -> ModelType:
        """Créer un nouvel objet en base"""
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_id(self, db: Session, obj_id: int) -> Optional[ModelType]:
        """Récupérer un objet par son ID"""
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Récupérer tous les objets avec pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: ModelType, update_data: Dict[str, Any]) -> ModelType:
        """Mettre à jour un objet existant"""
        for field, value in update_data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj_id: int) -> bool:
        """Supprimer un objet par son ID"""
        obj = self.get_by_id(db, obj_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

    def count(self, db: Session) -> int:
        """Compter le nombre total d'objets"""
        return db.query(self.model).count()

    def exists(self, db: Session, obj_id: int) -> bool:
        """Vérifier si un objet existe"""
        return self.get_by_id(db, obj_id) is not None