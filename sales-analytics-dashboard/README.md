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
