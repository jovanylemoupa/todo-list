"""
Script pour peupler la base de données avec des données de test plus complètes
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

# Ajouter le chemin racine au Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.category import Category
from app.models.task import Task, TaskPriority, TaskStatus

def seed_comprehensive_data():
    """Peupler avec des données de test complètes"""
    db = SessionLocal()
    
    try:
        # Données de tâches variées
        task_templates = [
            # Tâches professionnelles
            {
                "title": "Préparer la présentation client",
                "description": "Créer une présentation PowerPoint pour le client ABC avec les résultats du Q4",
                "priority": TaskPriority.HAUTE,
                "category_name": "Professionnel"
            },
            {
                "title": "Code review du module authentification",
                "description": "Réviser le code du système d'authentification avant la mise en production",
                "priority": TaskPriority.MOYENNE,
                "category_name": "Professionnel"
            },
            {
                "title": "Réunion équipe développement",
                "description": "Stand-up hebdomadaire avec l'équipe de développement",
                "priority": TaskPriority.BASSE,
                "category_name": "Professionnel"
            },
            
            # Tâches personnelles
            {
                "title": "Organiser l'anniversaire de maman",
                "description": "Réserver le restaurant et inviter la famille",
                "priority": TaskPriority.HAUTE,
                "category_name": "Personnel"
            },
            {
                "title": "Nettoyer le garage",
                "description": "Faire le tri et organiser les outils",
                "priority": TaskPriority.BASSE,
                "category_name": "Personnel"
            },
            {
                "title": "Renouveler l'assurance voiture",
                "description": "Comparer les offres et renouveler le contrat",
                "priority": TaskPriority.MOYENNE,
                "category_name": "Personnel"
            },
            
            # Tâches de formation
            {
                "title": "Suivre le cours Python avancé",
                "description": "Terminer les modules 5 à 8 du cours en ligne",
                "priority": TaskPriority.MOYENNE,
                "category_name": "Formation"
            },
            {
                "title": "Lire 'Clean Code'",
                "description": "Finir la lecture du livre de Robert Martin",
                "priority": TaskPriority.BASSE,
                "category_name": "Formation"
            },
            
            # Tâches de santé
            {
                "title": "Prendre RDV ophtalmo",
                "description": "Contrôle annuel de la vue - Dr. Dubois",
                "priority": TaskPriority.MOYENNE,
                "category_name": "Santé"
            },
            {
                "title": "Séance kiné",
                "description": "Rééducation du genou - Cabinet central",
                "priority": TaskPriority.HAUTE,
                "category_name": "Santé"
            },
            
            # Loisirs
            {
                "title": "Planifier les vacances d'été",
                "description": "Rechercher des destinations et faire les réservations",
                "priority": TaskPriority.MOYENNE,
                "category_name": "Loisirs"
            },
            {
                "title": "Inscription club de tennis",
                "description": "S'inscrire au club de tennis local pour la saison",
                "priority": TaskPriority.BASSE,
                "category_name": "Loisirs"
            },
        ]
        
        # Récupérer les catégories existantes
        categories = {cat.name: cat for cat in db.query(Category).all()}
        
        # Créer les tâches
        created_tasks = []
        for i, task_template in enumerate(task_templates, 1):
            category_name = task_template["category_name"]
            if category_name in categories:
                # Générer des dates variées
                days_offset = random.randint(-5, 15)  # Quelques tâches passées, beaucoup futures
                due_date = datetime.now() + timedelta(days=days_offset)
                
                # Quelques tâches terminées
                status = TaskStatus.EN_COURS
                completed_at = None
                if random.random() < 0.3:  # 30% de tâches terminées
                    status = TaskStatus.TERMINEE
                    completed_at = datetime.now() - timedelta(days=random.randint(1, 7))
                elif random.random() < 0.1:  # 10% reportées
                    status = TaskStatus.REPORTEE
                
                task = Task(
                    title=task_template["title"],
                    description=task_template["description"],
                    priority=task_template["priority"],
                    status=status,
                    due_date=due_date,
                    completed_at=completed_at,
                    category_id=categories[category_name].id,
                    position=i
                )
                
                # Calculer l'urgence
                task.update_urgency()
                
                db.add(task)
                created_tasks.append(task)
        
        db.commit()
        
        print(f"✅ {len(created_tasks)} tâches de test créées avec succès")
        
        # Afficher un résumé
        print("\n📊 Résumé des données créées :")
        print(f"   - Tâches en cours : {len([t for t in created_tasks if t.status == TaskStatus.EN_COURS])}")
        print(f"   - Tâches terminées : {len([t for t in created_tasks if t.status == TaskStatus.TERMINEE])}")
        print(f"   - Tâches reportées : {len([t for t in created_tasks if t.status == TaskStatus.REPORTEE])}")
        print(f"   - Tâches urgentes : {len([t for t in created_tasks if t.is_urgent])}")
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement : {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Peuplement de la base de données avec des données de test...")
    seed_comprehensive_data()
    print("✅ Peuplement terminé !")