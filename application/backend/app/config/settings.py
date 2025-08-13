from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

# Chemin racine du projet
ROOT_DIR = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    """Configuration centralisée de l'application"""
    
    # Database
    DATABASE_URL: str
    
    # Application
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_NAME: str = "Todo List API"
    VERSION: str = "1.0.0"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Paths
    ROOT_DIR: Path = ROOT_DIR
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance globale des paramètres
settings = Settings()