from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

# Configuration du moteur de base de données
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    echo=settings.DEBUG  # Log des requêtes SQL en mode debug
)

# Factory pour les sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

def get_db():
    """
    Générateur de session de base de données pour les dépendances FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()