# Architecture du Projet - Dashboard Analytique de Ventes

## Vue d'ensemble

Application de visualisation et d'analyse de données de ventes avec Plotly Dash, permettant une exploration interactive des indicateurs via des graphiques dynamiques et des tableaux hiérarchiques.

## Structure des Répertoires

```
sales-analytics-dashboard/
│
├── config/
│   ├── __init__.py
│   ├── database.py              # Configuration connexion SGBD
│   ├── settings.py              # Paramètres globaux (host, port, etc.)
│   └── indicators.yaml          # Définition des indicateurs disponibles
│
├── src/
│   ├── __init__.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py        # Gestionnaire de connexion BD
│   │   ├── queries.py           # Templates de requêtes SQL
│   │   └── query_builder.py     # Construction dynamique de requêtes
│   │
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── aggregator.py        # Agrégations post-BD
│   │   ├── calculator.py        # Calculs d'indicateurs complexes
│   │   ├── transformer.py       # Transformations de données
│   │   └── hierarchy_builder.py # Construction des hiérarchies (catégories/sous-catégories)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── indicator.py         # Classe Indicator
│   │   ├── filter.py            # Classe Filter (région, période, etc.)
│   │   └── granularity.py       # Classe Granularity (entreprise, produit, etc.)
│   │
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py           # Barre latérale avec filtres
│   │   ├── header.py            # En-tête avec logo et infos
│   │   ├── dropdowns.py         # Composants dropdown réutilisables
│   │   └── navigation.py        # Navigation tableau/graphique
│   │
│   ├── visualizations/
│   │   ├── __init__.py
│   │   ├── charts/
│   │   │   ├── __init__.py
│   │   │   ├── stacked_bar.py   # Diagrammes à bandes superposées
│   │   │   ├── line_chart.py    # Courbes de progression
│   │   │   ├── combo_chart.py   # Graphiques combinés
│   │   │   └── chart_factory.py # Factory pour créer les graphiques
│   │   │
│   │   └── tables/
│   │       ├── __init__.py
│   │       ├── hierarchical_table.py  # Tableaux avec profondeur
│   │       ├── table_formatter.py     # Formatage des cellules
│   │       └── table_builder.py       # Construction dynamique
│   │
│   ├── callbacks/
│   │   ├── __init__.py
│   │   ├── filter_callbacks.py  # Callbacks pour les filtres
│   │   ├── chart_callbacks.py   # Callbacks pour graphiques
│   │   └── table_callbacks.py   # Callbacks pour tableaux
│   │
│   └── utils/
│       ├── __init__.py
│       ├── date_utils.py        # Utilitaires pour dates/périodes
│       ├── format_utils.py      # Formatage (nombres, devises)
│       ├── color_schemes.py     # Palettes de couleurs
│       └── validators.py        # Validation des entrées
│
├── assets/
│   ├── styles.css               # Styles CSS personnalisés
│   ├── logo.png                 # Logo de l'entreprise
│   └── favicon.ico
│
├── data/
│   ├── cache/                   # Cache des requêtes
│   └── exports/                 # Exports de données
│
├── tests/
│   ├── __init__.py
│   ├── test_database/
│   ├── test_processing/
│   ├── test_visualizations/
│   └── test_integration/
│
├── app.py                       # Point d'entrée de l'application
├── requirements.txt
├── README.md
└── .env                         # Variables d'environnement
```

## Détail des Composants Clés

### 1. **config/indicators.yaml**
Définit tous les indicateurs disponibles avec leurs propriétés :
```yaml
indicators:
  - id: "ca_total"
    name: "Chiffre d'Affaires Total"
    unit: "€"
    query_type: "direct"  # direct = requête BD directe
    calculation: null
    
  - id: "marge_commerciale"
    name: "Marge Commerciale"
    unit: "%"
    query_type: "computed"  # computed = calcul post-BD
    calculation: "(ca - cout_achat) / ca * 100"
    
  - id: "quantite_vendue"
    name: "Quantité Vendue"
    unit: "unités"
    query_type: "direct"
```

### 2. **src/models/indicator.py**
```python
class Indicator:
    """Représente un indicateur métier"""
    def __init__(self, id, name, unit, query_type, calculation=None):
        self.id = id
        self.name = name
        self.unit = unit
        self.query_type = query_type
        self.calculation = calculation
```

### 3. **src/models/filter.py**
```python
class Filter:
    """Représente un filtre applicable aux données"""
    def __init__(self, filter_type, values):
        self.filter_type = filter_type  # 'region', 'periode', 'categorie'
        self.values = values
        
class Granularity:
    """Niveau de détail de l'analyse"""
    ENTREPRISE = "entreprise"
    CATEGORIE = "categorie"
    SOUS_CATEGORIE = "sous_categorie"
    PRODUIT = "produit"
```

### 4. **src/database/query_builder.py**
Construit dynamiquement les requêtes SQL selon les filtres :
```python
class QueryBuilder:
    def build_query(self, indicator, filters, granularity):
        """Construit une requête SQL dynamique"""
        # SELECT clause basée sur l'indicateur
        # WHERE clause basée sur les filtres
        # GROUP BY clause basée sur la granularité
        pass
```

### 5. **src/data_processing/hierarchy_builder.py**
Gère la structure hiérarchique des tableaux :
```python
class HierarchyBuilder:
    def build_hierarchy(self, data, levels):
        """
        Construit une structure hiérarchique
        levels = ['categorie', 'sous_categorie', 'produit']
        """
        pass
```

### 6. **src/visualizations/charts/stacked_bar.py**
Crée les diagrammes à bandes superposées :
```python
def create_stacked_bar_chart(data, x_axis, y_axis, stack_by, title):
    """
    data: DataFrame avec les données
    x_axis: 'mois' par exemple
    y_axis: indicateur à afficher
    stack_by: dimension de segmentation ('produit', 'categorie')
    """
    fig = go.Figure()
    # Logique de création du graphique
    return fig
```

### 7. **src/visualizations/tables/hierarchical_table.py**
Crée les tableaux avec profondeur :
```python
def create_hierarchical_table(data, hierarchy_levels, metrics):
    """
    Crée un tableau Dash DataTable avec indentations
    hierarchy_levels: ['categorie', 'sous_categorie', 'produit']
    metrics: ['mois_1', 'mois_2', ..., 'mois_n']
    """
    pass
```

### 8. **app.py - Structure principale**
```python
import dash
from dash import html, dcc
from src.components import sidebar, header, navigation
from src.callbacks import filter_callbacks, chart_callbacks

app = dash.Dash(__name__)

app.layout = html.Div([
    header.create_header(),
    html.Div([
        html.Div([
            sidebar.create_sidebar()
        ], className='sidebar'),
        
        html.Div([
            navigation.create_navigation(),
            html.Div(id='main-content')
        ], className='main-content')
    ], className='container')
])

# Enregistrement des callbacks
filter_callbacks.register_callbacks(app)
chart_callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
```

## Flux de Données

```
1. Utilisateur sélectionne filtres (sidebar)
   ↓
2. Callback déclenché
   ↓
3. QueryBuilder construit la requête SQL
   ↓
4. Connection.execute_query() → SGBD
   ↓
5. DataProcessor traite les données
   ↓
6. Si query_type="computed" → Calculator applique formules
   ↓
7. HierarchyBuilder structure les données (si tableau)
   ↓
8. ChartFactory ou TableBuilder crée la visualisation
   ↓
9. Affichage dans l'interface
```

## Technologies et Librairies

### requirements.txt
```
dash==2.14.0
plotly==5.17.0
pandas==2.1.0
sqlalchemy==2.0.20
psycopg2-binary==2.9.7  # Pour PostgreSQL
# ou pymysql pour MySQL
# ou pyodbc pour SQL Server
python-dotenv==1.0.0
pyyaml==6.0.1
redis==5.0.0  # Pour le cache (optionnel)
dash-bootstrap-components==1.5.0  # Pour styling
```

## Considérations Importantes

### Performance
- **Cache** : Implémenter un système de cache (Redis ou disque) pour les requêtes fréquentes
- **Pagination** : Pour les tableaux avec beaucoup de lignes
- **Lazy Loading** : Charger les données à la demande
- **Agrégations BD** : Maximiser les calculs côté SGBD

### Sécurité
- Variables d'environnement pour credentials BD
- Validation des inputs utilisateurs
- Paramètres préparés pour les requêtes SQL

### Scalabilité
- Architecture modulaire pour faciliter l'ajout de nouveaux indicateurs
- Factory patterns pour les graphiques
- Configuration centralisée

### UX/UI
- Loading spinners pendant chargement des données
- Messages d'erreur clairs
- Responsive design (Bootstrap)
- Export de données (CSV, Excel)

## Prochaines Étapes

1. Créer la structure de répertoires
2. Implémenter la connexion BD et les requêtes de base
3. Développer les composants de l'interface
4. Créer les premiers graphiques et tableaux
5. Implémenter les callbacks
6. Tests et optimisations
7. Déploiement

---

Cette architecture est évolutive et permet d'ajouter facilement de nouveaux indicateurs, filtres ou types de visualisations.
