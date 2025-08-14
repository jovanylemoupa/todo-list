from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import uvicorn
from contextlib import asynccontextmanager

from app.config.settings import settings
from app.config.database import Base, engine
from app.api.v1.router import api_router
from app.core.exceptions import TodoException
from app.schemas.common import ErrorResponse

# Gestionnaire de contexte pour le cycle de vie de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire du cycle de vie de l'application"""
    # Démarrage : créer les tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)
    
    print(f"🚀 {settings.APP_NAME} v{settings.VERSION} démarré!")
    print(f"📚 Documentation disponible sur : http://{settings.HOST}:{settings.PORT}/docs")
    
    yield  # L'application tourne ici
    
    # Arrêt : nettoyage si nécessaire
    print("🛑 Arrêt de l'application...")

# Création de l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    ## API de gestion de tâches (Todo List)
    
    Cette API REST permet de gérer des tâches avec les fonctionnalités suivantes :
    
    ### 📋 Fonctionnalités principales
    - **Gestion complète des tâches** (CRUD)
    - **Catégorisation** des tâches
    - **Validation robuste** avec Pydantic
    - **Filtrage et tri** avancés
    - **Pagination** automatique
    
    ### 🎯 Contraintes respectées
    - Titre obligatoire (min. 3 caractères)
    - Date d'échéance obligatoire (future)
    - Catégorie obligatoire
    - Validation stricte des données
    
    ### 🚀 Fonctionnalités bonus
    - Recherche textuelle
    - Tâches urgentes (< 2 jours)
    - Drag & drop (réorganisation)
    - Statistiques complètes
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(api_router)

# Gestionnaires d'exceptions globaux
@app.exception_handler(TodoException)
async def todo_exception_handler(request: Request, exc: TodoException):
    """Gestionnaire pour les exceptions métier de l'application"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            detail=exc.detail,
            code=getattr(exc, 'code', None)
        ).dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Gestionnaire pour les erreurs de validation Pydantic"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="ValidationError",
            detail="Erreur de validation des données",
            code="VALIDATION_FAILED"
        ).dict()
    )

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Gestionnaire pour les erreurs de base de données"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="DatabaseError",
            detail="Erreur de base de données",
            code="DATABASE_ERROR"
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Gestionnaire pour toutes les autres exceptions"""
    if settings.DEBUG:
        detail = str(exc)
    else:
        detail = "Une erreur interne s'est produite"
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            detail=detail,
            code="INTERNAL_ERROR"
        ).dict()
    )

# Endpoints de santé
@app.get("/health", 
    tags=["Health"],
    summary="Vérification de santé de l'API"
)
def health_check():
    """
    Endpoint de vérification de santé de l'API.
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }

@app.get("/", 
    tags=["Root"],
    summary="Point d'entrée de l'API"
)
def root():
    """
    Point d'entrée racine de l'API.
    """
    return {
        "message": f"Bienvenue sur {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1"
    }

# Point d'entrée pour l'exécution directe
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )