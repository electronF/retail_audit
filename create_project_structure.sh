#!/bin/bash

# Script de création de la structure du projet
# Usage: bash create_project_structure.sh

PROJECT_NAME="sales-analytics-dashboard"

echo "🚀 Création de la structure du projet: $PROJECT_NAME"
echo "================================================"

# Création du répertoire racine
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Création de la structure des répertoires
echo "📁 Création des répertoires..."

# Config
mkdir -p config

# Source code
mkdir -p src/database
mkdir -p src/data_processing
mkdir -p src/models
mkdir -p src/components
mkdir -p src/visualizations/charts
mkdir -p src/visualizations/tables
mkdir -p src/callbacks
mkdir -p src/utils

# Assets
mkdir -p assets

# Data
mkdir -p data/cache
mkdir -p data/exports

# Tests
mkdir -p tests/test_database
mkdir -p tests/test_processing
mkdir -p tests/test_visualizations
mkdir -p tests/test_integration

# Logs
mkdir -p logs

echo "✅ Répertoires créés"

# Création des fichiers __init__.py
echo "📝 Création des fichiers __init__.py..."

touch config/__init__.py
touch src/__init__.py
touch src/database/__init__.py
touch src/data_processing/__init__.py
touch src/models/__init__.py
touch src/components/__init__.py
touch src/visualizations/__init__.py
touch src/visualizations/charts/__init__.py
touch src/visualizations/tables/__init__.py
touch src/callbacks/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
touch tests/test_database/__init__.py
touch tests/test_processing/__init__.py
touch tests/test_visualizations/__init__.py
touch tests/test_integration/__init__.py

echo "✅ Fichiers __init__.py créés"

# Création des fichiers de configuration
echo "📝 Création des fichiers de configuration..."

# config/database.py
cat > config/database.py << 'EOF'
"""Configuration de la connexion à la base de données"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_CONFIG = {
    'type': os.getenv('DB_TYPE', 'postgresql'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}
EOF

# config/settings.py
cat > config/settings.py << 'EOF'
"""Paramètres globaux de l'application"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application
APP_CONFIG = {
    'host': os.getenv('APP_HOST', '0.0.0.0'),
    'port': int(os.getenv('APP_PORT', 8050)),
    'debug': os.getenv('DEBUG_MODE', 'True').lower() == 'true'
}

# Cache
CACHE_CONFIG = {
    'type': os.getenv('CACHE_TYPE', 'redis'),
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'timeout': int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
}

# Performance
PERFORMANCE_CONFIG = {
    'max_rows_per_query': int(os.getenv('MAX_ROWS_PER_QUERY', 100000)),
    'query_timeout': int(os.getenv('QUERY_TIMEOUT', 30))
}

# Export
EXPORT_CONFIG = {
    'folder': os.getenv('EXPORT_FOLDER', 'data/exports'),
    'max_rows': int(os.getenv('MAX_EXPORT_ROWS', 50000))
}
EOF

# config/indicators.yaml
cat > config/indicators.yaml << 'EOF'
indicators:
  - id: ca_total
    name: "Chiffre d'Affaires Total"
    unit: "€"
    query_type: direct
    sql_column: montant_vente
    aggregation: sum
    
  - id: quantite_vendue
    name: "Quantité Vendue"
    unit: "unités"
    query_type: direct
    sql_column: quantite
    aggregation: sum
    
  - id: nombre_transactions
    name: "Nombre de Transactions"
    unit: "transactions"
    query_type: direct
    sql_column: transaction_id
    aggregation: count_distinct
    
  - id: panier_moyen
    name: "Panier Moyen"
    unit: "€"
    query_type: computed
    calculation: "SUM(montant_vente) / COUNT(DISTINCT transaction_id)"
    
  - id: marge_commerciale
    name: "Marge Commerciale"
    unit: "%"
    query_type: computed
    calculation: "(SUM(montant_vente) - SUM(cout_achat)) / SUM(montant_vente) * 100"

granularities:
  - id: entreprise
    name: "Entreprise"
    columns: []
    
  - id: categorie
    name: "Catégorie"
    columns: [categorie_principale]
    
  - id: sous_categorie
    name: "Sous-catégorie"
    columns: [categorie_principale, sous_categorie]
    
  - id: produit
    name: "Produit"
    columns: [categorie_principale, sous_categorie, produit_id, nom_produit]
EOF

echo "✅ Fichiers de configuration créés"

# Création des fichiers CSS
echo "📝 Création des assets CSS..."

cat > assets/styles.css << 'EOF'
/* Styles personnalisés pour le dashboard */

:root {
    --primary-color: #16697a;
    --secondary-color: #489fb5;
    --accent-color: #82c0cc;
    --background-color: #ffa62b;
    --text-color: #2c3e50;
    --border-color: #bdc3c7;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.sidebar {
    background-color: #ecf0f1;
    min-height: calc(100vh - 80px);
    border-right: 1px solid var(--border-color);
    padding: 20px;
}

.main-content {
    padding: 20px;
}

.filter-section {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-container {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Dropdowns */
.Select-control {
    border-radius: 4px;
    border-color: var(--border-color);
}

.Select-control:hover {
    border-color: var(--secondary-color);
}

/* Buttons */
.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}

/* Cards */
.card {
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

/* Tables */
.dash-table-container {
    font-family: monospace;
}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th {
    background-color: var(--primary-color);
    color: white;
}

/* Loading */
._dash-loading {
    color: var(--primary-color);
}
EOF

echo "✅ Assets CSS créés"

# Création du README
cat > README.md << 'EOF'
# Dashboard Analytique de Ventes

Application de visualisation et d'analyse de données de ventes avec Plotly Dash.

## 🚀 Installation

1. Cloner le repository
2. Créer un environnement virtuel:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement:
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. Lancer l'application:
```bash
python app.py
```

## 📁 Structure du Projet

- `config/` : Configuration de l'application et de la BD
- `src/` : Code source
  - `database/` : Connexion et requêtes BD
  - `data_processing/` : Traitement et agrégation de données
  - `models/` : Modèles de données
  - `components/` : Composants UI réutilisables
  - `visualizations/` : Graphiques et tableaux
  - `callbacks/` : Callbacks Dash
  - `utils/` : Fonctions utilitaires
- `assets/` : CSS, images, et autres ressources
- `data/` : Cache et exports
- `tests/` : Tests unitaires et d'intégration

## 🔧 Configuration

Éditer le fichier `.env` avec vos paramètres:
- Connexion base de données
- Port de l'application
- Configuration du cache
- Etc.

## 📊 Fonctionnalités

- Visualisation interactive avec graphiques à bandes empilées
- Tableaux hiérarchiques avec profondeur
- Filtres dynamiques (région, période, catégorie)
- Granularité ajustable (entreprise, catégorie, produit)
- Export de données (Excel)
- Cache pour améliorer les performances

## 🧪 Tests

```bash
pytest tests/
```

## 📝 License

[Votre License]
EOF

# Création du .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data
data/cache/*
data/exports/*
!data/cache/.gitkeep
!data/exports/.gitkeep

# Logs
logs/*.log
!logs/.gitkeep

# OS
.DS_Store
Thumbs.db

# Tests
.pytest_cache/
htmlcov/
.coverage
EOF

# Création des fichiers .gitkeep
touch data/cache/.gitkeep
touch data/exports/.gitkeep
touch logs/.gitkeep

echo "✅ Fichiers de configuration créés"

# Résumé
echo ""
echo "================================================"
echo "✨ Projet créé avec succès!"
echo "================================================"
echo ""
echo "📂 Structure créée dans: $PROJECT_NAME/"
echo ""
echo "🎯 Prochaines étapes:"
echo "  1. cd $PROJECT_NAME"
echo "  2. python -m venv venv"
echo "  3. source venv/bin/activate"
echo "  4. pip install -r requirements.txt"
echo "  5. cp .env.example .env"
echo "  6. Éditer .env avec vos configurations"
echo "  7. python app.py"
echo ""
echo "================================================"
