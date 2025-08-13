from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import BaseModel

class Category(BaseModel):
    """
    Modèle pour les catégories de tâches
    """
    __tablename__ = "categories"
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(200), nullable=True)
    color = Column(String(7), default="#007bff")  # Code couleur hexadécimal
    
    # Relations
    tasks = relationship("Task", back_populates="category", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Category(name={self.name})>"