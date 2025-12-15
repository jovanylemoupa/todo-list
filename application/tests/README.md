# Tests

Ce dossier contient tous les tests pour l'application Todo List (frontend et backend).

## Structure

```
tests/
├── backend/           # Tests backend (Jest)
│   └── *.spec.js     # Fichiers de tests
├── frontend/          # Tests frontend (Cypress E2E)
│   ├── support/      # Commandes et configuration Cypress
│   ├── fixtures/     # Données de test
│   └── *.cy.js       # Fichiers de tests Cypress
├── node_modules/      # Dépendances partagées (Cypress + Jest)
├── package.json       # Configuration des tests
├── cypress.config.js  # Configuration Cypress
└── jest.config.js     # Configuration Jest
```

## Installation

Les dépendances sont déjà installées. Si besoin :

```bash
cd application/tests
npm install
```

## Lancer tous les tests

```bash
cd application/tests
npm test
```

Cela lancera les tests frontend (Cypress) ET backend (Jest).

## Tests Frontend (Cypress)

### Mode interactif (avec interface graphique)
```bash
cd application/tests
npm run cypress:open
```

### Mode headless (en ligne de commande)
```bash
cd application/tests
npm run test:frontend
```

### Prérequis
L'application frontend doit être en cours d'exécution :
```bash
cd application/frontend
npm run dev
```

### Configuration
- **Fichier de config :** [cypress.config.js](cypress.config.js)
- **URL de base :** `http://localhost:5173`
- **Tests :** [frontend/](frontend/)

## Tests Backend (Jest)

### Lancer les tests backend uniquement
```bash
cd application/tests
npm run test:backend
```

### Configuration
- **Fichier de config :** [jest.config.js](jest.config.js)
- **Tests :** [backend/](backend/)

### Prérequis
Votre API backend doit être en cours d'exécution si vous testez des endpoints HTTP.

## Avantages de cette structure

✅ **Un seul `node_modules`** partagé entre frontend et backend
✅ **Gestion centralisée** des dépendances de test
✅ **Commandes simplifiées** via npm scripts
✅ **Organisation claire** : frontend vs backend
