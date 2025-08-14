"""
Script d'initialisation de la base de données
"""
import sys
import os
from pathlib import Path

# Ajouter le chemin racine au Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal, engine, Base
from app.models.category import Category
from app.models.task import Task, TaskPriority, TaskStatus
from datetime import datetime, timedelta

def create_tables():
    """Créer toutes les tables"""
    print("🔧 Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès")

def init_categories(db: Session):
    """Initialiser les catégories par défaut"""
    print("📁 Initialisation des catégories...")
    
    # Vérifier si des catégories existent déjà
    existing_count = db.query(Category).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} catégories déjà présentes, passage de l'initialisation")
        return
    
    # Créer les catégories par défaut
    default_categories = [
        Category(
            name="Personnel", 
            description="Tâches personnelles et vie privée", 
            color="#28a745"
        ),
        Category(
            name="Professionnel", 
            description="Tâches de travail et projets", 
            color="#007bff"
        ),
        Category(
            name="Urgent", 
            description="Tâches urgentes et prioritaires", 
            color="#dc3545"
        ),
        Category(
            name="Loisirs", 
            description="Activités de loisir et détente", 
            color="#ffc107"
        ),
        Category(
            name="Santé", 
            description="Rendez-vous médicaux et bien-être", 
            color="#17a2b8"
        ),
        Category(
            name="Formation", 
            description="Apprentissage et développement personnel", 
            color="#6f42c1"
        ),
    ]
    
    for category in default_categories:
        db.add(category)
    
    db.commit()
    print(f"✅ {len(default_categories)} catégories par défaut créées")

def create_sample_tasks(db: Session):
    """Créer quelques tâches d'exemple (optionnel)"""
    print("📝 Création de tâches d'exemple...")
    
    # Vérifier si des tâches existent déjà
    existing_count = db.query(Task).count()
    if existing_count > 0:
        print(f"ℹ️  {existing_count} tâches déjà présentes, passage de la création d'exemples")
        return
    
    # Récupérer les catégories
    categories = db.query(Category).all()
    if not categories:
        print("❌ Aucune catégorie trouvée, impossible de créer des tâches d'exemple")
        return
    
    # Créer quelques tâches d'exemple
    sample_tasks = [
        Task(
            title="Finaliser le projet Todo List",
            description="Terminer l'implémentation du backend FastAPI avec toutes les fonctionnalités requises",
            priority=TaskPriority.HAUTE,
            due_date=datetime.now() + timedelta(days=1),  # Urgente
            category_id=categories[1].id,  # Professionnel
            position=1
        ),
        Task(
            title="Rendez-vous dentiste",
            description="Contrôle annuel chez le dentiste - Dr. Martin",
            priority=TaskPriority.MOYENNE,
            due_date=datetime.now() + timedelta(days=7),
            category_id=categories[4].id if len(categories) > 4 else categories[0].id,  # Santé
            position=2
        ),
        Task(
            title="Faire les courses",
            description="Acheter des légumes, fruits et produits pour la semaine",
            priority=TaskPriority.BASSE,
            due_date=datetime.now() + timedelta(days=3),
            category_id=categories[0].id,  # Personnel
            position=3
        ),
        Task(
            title="Réviser Vue.js",
            description="Approfondir la Composition API pour le frontend du projet",
            priority=TaskPriority.MOYENNE,
            due_date=datetime.now() + timedelta(days=5),
            category_id=categories[5].id if len(categories) > 5 else categories[1].id,  # Formation
            position=4
        ),
    ]
    
    for task in sample_tasks:
        # Calculer l'urgence
        task.update_urgency()
        db.add(task)
    
    db.commit()
    print(f"✅ {len(sample_tasks)} tâches d'exemple créées")

def main():
    """Fonction principale d'initialisation"""
    print("🚀 Initialisation de la base de données Todo List...")
    print("=" * 50)
    
    try:
        # Créer les tables
        create_tables()
        
        # Initialiser les données
        db = SessionLocal()
        try:
            init_categories(db)
            
            # Demander si on veut créer des tâches d'exemple
            create_samples = input("Voulez-vous créer des tâches d'exemple ? (y/N): ").lower() == 'y'
            if create_samples:
                create_sample_tasks(db)
            
        finally:
            db.close()
        
        print("=" * 50)
        print("✅ Initialisation terminée avec succès!")
        print(f"🌐 Vous pouvez maintenant lancer l'API avec : python run.py")
        print(f"📚 Documentation disponible sur : http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        raise

if __name__ == "__main__":
    main()