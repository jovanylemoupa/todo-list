"""
Configuration pytest pour les tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.config.database import get_db, Base
from app.models.category import Category
from app.models.task import Task, TaskPriority

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fixture pour la session de base de données de test"""
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    # Créer une session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Nettoyer après chaque test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Fixture pour le client de test FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_category(db_session):
    """Fixture pour créer une catégorie de test"""
    category = Category(
        name="Test Category",
        description="Catégorie pour les tests",
        color="#007bff"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category

@pytest.fixture
def sample_task(db_session, sample_category):
    """Fixture pour créer une tâche de test"""
    from datetime import datetime, timedelta
    
    task = Task(
        title="Tâche de test",
        description="Description de test",
        priority=TaskPriority.MOYENNE,
        due_date=datetime.now() + timedelta(days=7),
        category_id=sample_category.id,
        position=1
    )
    task.update_urgency()
    
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task