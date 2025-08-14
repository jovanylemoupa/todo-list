from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    """Schéma de base pour les catégories"""
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Nom de la catégorie"
    )
    description: Optional[str] = Field(
        None, 
        max_length=200, 
        description="Description optionnelle de la catégorie"
    )
    color: str = Field(
        default="#007bff", 
        pattern=r"^#[0-9A-Fa-f]{6}$",  # CHANGÉ: regex → pattern
        description="Couleur en format hexadécimal"
    )

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Le nom de la catégorie ne peut pas être vide')
        return v.strip().title()

class CategoryCreate(CategoryBase):
    """Schéma pour la création d'une catégorie"""
    pass

class CategoryUpdate(BaseModel):
    """Schéma pour la mise à jour d'une catégorie"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")  # CHANGÉ: regex → pattern

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Le nom de la catégorie ne peut pas être vide')
        return v.strip().title() if v else v

class CategoryResponse(CategoryBase):
    """Schéma pour les réponses contenant une catégorie"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tasks_count: int = 0

    class Config:
        from_attributes = True