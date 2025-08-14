"""
Constantes de l'application
"""

# Priorités des tâches
TASK_PRIORITIES = {
    "BASSE": "Basse",
    "MOYENNE": "Moyenne", 
    "HAUTE": "Haute"
}

# Statuts des tâches
TASK_STATUSES = {
    "EN_COURS": "En cours",
    "TERMINEE": "Terminée",
    "REPORTEE": "Reportée"
}

# Couleurs par défaut des catégories
DEFAULT_CATEGORY_COLORS = {
    "Personnel": "#28a745",
    "Professionnel": "#007bff",
    "Urgent": "#dc3545",
    "Loisirs": "#ffc107",
    "Santé": "#17a2b8",
    "Formation": "#6f42c1"
}

# Limites de pagination
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20

# Seuil d'urgence (en jours)
URGENCY_THRESHOLD_DAYS = 2