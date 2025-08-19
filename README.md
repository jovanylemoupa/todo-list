# 📋 Todo List - Application Full-Stack

> Mini-application web de gestion de tâches développée avec FastAPI (Python) et Vue.js 3

## 📖 Description

Application web moderne de gestion de tâches avec catégories colorées, priorités, dates d'échéance et interface responsive.

## 🎯 Fonctionnalités

- **CRUD complet** des tâches et catégories
- **Recherche textuelle** et filtres multiples
- **Système de priorités** avec alertes visuelles
- **Interface responsive** (PC, tablette, mobile)
- **Validation temps réel** frontend + backend

## 🛠️ Technologies

**Backend :** Python 3.9+ • FastAPI • PostgreSQL • SQLAlchemy • Alembic • Pydantic
**Frontend :** Vue.js 3 • TypeScript • Pinia • Axios • CSS moderne

## 📋 Prérequis

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js 16+](https://nodejs.org/)
- [PostgreSQL 12+](https://www.postgresql.org/download/)

## 🚀 Installation Rapide

### 1. Cloner et configurer la base

```bash
git clone <url-du-repo>
cd todo-list

# Créer la base PostgreSQL
psql -U postgres -c "CREATE DATABASE todolist_db;"
```

### 2. Backend Setup

```bash
cd backend

# Environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Dépendances
pip install -r requirements.txt

# Configuration (.env)
cp .env.example .env
# Éditer DATABASE_URL dans .env si nécessaire

# Migrations base de données
alembic upgrade head

# Lancer le serveur
python run.py
```

✅ **Backend accessible :** http://localhost:8000  
📚 **API Docs :** http://localhost:8000/docs

### 3. Frontend Setup (nouveau terminal)

```bash
cd frontend

# Dépendances
npm install

# Configuration (optionnel)
cp .env.example .env.local

# Lancer
npm run dev
```

✅ **Frontend accessible :** http://localhost:3000

### 4. Données d'exemple (optionnel)

```bash
# Dans le terminal backend (avec venv activé)
python seed_data.py
```

## 🔧 Variables d'environnement

**Backend (.env) :**

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/todolist_db
ALLOWED_ORIGINS=["http://localhost:3000"]
DEBUG=True
```

**Frontend (.env.local) :**

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Troubleshooting

| Problème                     | Solution                                   |
| ---------------------------- | ------------------------------------------ |
| `psycopg2 not found`         | `pip install psycopg2-binary`              |
| `Database connection failed` | Vérifier PostgreSQL démarré + DATABASE_URL |
| `CORS Policy error`          | Vérifier ALLOWED_ORIGINS dans .env         |
| `Port already in use`        | Changer port ou tuer processus existant    |

## Commandes Utiles

```bash
# Backend
source venv/bin/activate && python run.py
uvicorn app.main:app --reload  # Mode dev avec rechargement
alembic upgrade head           # Appliquer migrations
alembic revision --autogenerate -m "description"  # Nouvelle migration
python seed_data.py           # Charger données d'exemple

# Frontend
npm run dev        # Développement
npm run build      # Production
npm run type-check # Vérifier TypeScript
```

## 🎯 Accès rapides

- 🌐 **Application :** http://localhost:3000
- 🔧 **API :** http://localhost:8000
- 📚 **Documentation API :** http://localhost:8000/docs

---

## 📞 Contact

**Développeur :** Jovany Lemoupa  
**Email :** jovanylemoupa@gmail.com  
**GitHub :** [jovanylemoupa](https://github.com/jovanylemoupa)

## 📚 Ressources

- [FastAPI Docs](https://fastapi.tiangolo.com/) • [Vue.js 3 Docs](https://vuejs.org/) • [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

🎉 **Application opérationnelle !** Créez vos premières tâches et explorez toutes les fonctionnalités.
