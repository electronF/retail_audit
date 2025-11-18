# 📐 Diagrammes d'Architecture - Dashboard Analytique

## 🏗️ Architecture Globale

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INTERFACE UTILISATEUR                        │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐                │
│  │   Header   │  │   Sidebar    │  │Main Content  │                │
│  │  + Logo    │  │  + Filtres   │  │+ Graphiques  │                │
│  │  + Menu    │  │  + Options   │  │+ Tableaux    │                │
│  └────────────┘  └──────────────┘  └──────────────┘                │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          CALLBACKS DASH                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │Filter        │  │Chart         │  │Table         │             │
│  │Callbacks     │  │Callbacks     │  │Callbacks     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     COUCHE DE TRAITEMENT                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Aggregator   │  │ Calculator   │  │ Hierarchy    │             │
│  │              │  │              │  │ Builder      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    COUCHE VISUALISATION                             │
│  ┌──────────────────────────┐  ┌──────────────────────────┐        │
│  │      Charts              │  │      Tables              │        │
│  │  • Stacked Bar           │  │  • Hierarchical          │        │
│  │  • Line Chart            │  │  • Pivot                 │        │
│  │  • Combo Chart           │  │  • Comparison            │        │
│  └──────────────────────────┘  └──────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      COUCHE BASE DE DONNÉES                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Connection   │  │Query Builder │  │   Queries    │             │
│  │ Manager      │  │              │  │   Templates  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            SGBD                                     │
│                  (PostgreSQL / MySQL / SQL Server)                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flux de Données Détaillé

### Scénario : Utilisateur sélectionne un filtre

```
1. USER ACTION
   │
   ├─ Clique sur dropdown "Région"
   └─ Sélectionne "Nord"
        │
        ▼
2. DASH CALLBACK TRIGGER
   │
   ├─ Input: region-dropdown.value = "Nord"
   └─ Callback: update_data_store()
        │
        ▼
3. QUERY BUILDING
   │
   ├─ QueryBuilder.build_query()
   │   ├─ indicator: "ca_total"
   │   ├─ filters: {region: "Nord", date: "2024-01-01 to 2024-12-31"}
   │   └─ granularity: "categorie"
   │
   └─ Génère SQL:
       SELECT 
         DATE_TRUNC('month', date_vente) as periode,
         categorie_principale,
         SUM(montant_vente) as valeur
       FROM sales.ventes
       WHERE region_id = 1
         AND date_vente BETWEEN '2024-01-01' AND '2024-12-31'
       GROUP BY periode, categorie_principale
       ORDER BY periode, categorie_principale
        │
        ▼
4. DATABASE QUERY
   │
   ├─ DatabaseConnection.execute_query(sql, params)
   │   └─ SQLAlchemy → PostgreSQL
   │
   └─ Retourne DataFrame:
       ┌───────────┬──────────────┬────────┐
       │  periode  │  categorie   │ valeur │
       ├───────────┼──────────────┼────────┤
       │ 2024-01   │ Électronique │ 45000  │
       │ 2024-01   │ Vêtements    │ 32000  │
       │ 2024-02   │ Électronique │ 48000  │
       │ ...       │ ...          │ ...    │
       └───────────┴──────────────┴────────┘
        │
        ▼
5. DATA PROCESSING
   │
   ├─ Si indicateur computed:
   │   └─ Calculator.apply_formula()
   │
   ├─ Si tableau hiérarchique:
   │   └─ HierarchyBuilder.build_hierarchy()
   │
   └─ Stocke dans dcc.Store
        │
        ▼
6. VISUALIZATION CALLBACK
   │
   ├─ Input: data-store.data
   │
   ├─ Pour graphique:
   │   └─ StackedBarChart.create_monthly_stacked_bar()
   │       └─ Retourne: go.Figure
   │
   └─ Pour tableau:
       └─ HierarchicalTable.create_hierarchical_table()
           └─ Retourne: dash_table.DataTable
        │
        ▼
7. UI UPDATE
   │
   └─ Dash met à jour l'interface
       ├─ Graphique affiché
       └─ Tableau affiché
```

---

## 📊 Structure des Données

### Transformation des données brutes en visualisation

```
BASE DE DONNÉES (Tables brutes)
┌────────────────────────────────────────────────────────────┐
│ ventes                                                      │
├───────────┬────────────┬──────────┬─────────────┬─────────┤
│transaction│ date_vente │ montant  │ categorie   │ region  │
├───────────┼────────────┼──────────┼─────────────┼─────────┤
│ 1001      │ 2024-01-15 │ 450.00   │Électronique │ Nord    │
│ 1002      │ 2024-01-16 │ 120.00   │Vêtements    │ Sud     │
│ 1003      │ 2024-01-17 │ 890.00   │Électronique │ Nord    │
│ ...       │ ...        │ ...      │ ...         │ ...     │
└───────────┴────────────┴──────────┴─────────────┴─────────┘
                    │
                    ▼ SQL Aggregation
DONNÉES AGRÉGÉES (Après requête)
┌────────────┬─────────────┬─────────┐
│  periode   │  categorie  │ valeur  │
├────────────┼─────────────┼─────────┤
│ 2024-01    │Électronique │ 125000  │
│ 2024-01    │ Vêtements   │  85000  │
│ 2024-02    │Électronique │ 135000  │
│ 2024-02    │ Vêtements   │  92000  │
└────────────┴─────────────┴─────────┘
                    │
                    ▼ Pour Graphique Empilé
VISUALISATION GRAPHIQUE
┌─────────────────────────────────────┐
│  Ventes par Mois et Catégorie       │
│                                     │
│  250K│ ┌────────┐                   │
│      │ │Vêtement│                   │
│  200K│ │        │ ┌────────┐        │
│      │ │        │ │Vêtement│        │
│  150K│ ├────────┤ │        │        │
│      │ │Électro │ ├────────┤        │
│  100K│ │        │ │Électro │        │
│      │ │        │ │        │        │
│   50K│ │        │ │        │        │
│      │ └────────┘ └────────┘        │
│    0 ├─────────────────────────────│
│      Jan-24    Feb-24               │
└─────────────────────────────────────┘
                    │
                    ▼ Pour Tableau Hiérarchique
VISUALISATION TABLEAU
┌──────────────────┬────────┬────────┐
│ Catégorie        │ Jan-24 │ Feb-24 │
├──────────────────┼────────┼────────┤
│ Électronique     │125,000 │135,000 │
│   ├─ Téléphones  │ 80,000 │ 90,000 │
│   └─ Ordinateurs │ 45,000 │ 45,000 │
│ Vêtements        │ 85,000 │ 92,000 │
│   ├─ Homme       │ 45,000 │ 48,000 │
│   └─ Femme       │ 40,000 │ 44,000 │
│ TOTAL            │210,000 │227,000 │
└──────────────────┴────────┴────────┘
```

---

## 🗂️ Organisation des Fichiers par Fonction

### 📦 Modules de Base de Données

```
src/database/
│
├── connection.py
│   └── Fonctions:
│       • __init__()           : Initialise la connexion
│       • _connect()           : Crée l'engine SQLAlchemy
│       • execute_query()      : Exécute une requête
│       • execute_query_chunked() : Pour grandes données
│       • test_connection()    : Teste la connexion
│       • close()              : Ferme proprement
│
├── query_builder.py
│   └── Fonctions:
│       • build_query()        : Construit requête standard
│       • build_hierarchy_query() : Pour tableaux hiérarchiques
│       • build_comparison_query() : Pour comparaisons périodes
│
└── queries.py (à créer)
    └── Templates de requêtes réutilisables
```

### 📊 Modules de Visualisation

```
src/visualizations/
│
├── charts/
│   ├── stacked_bar.py
│   │   └── Fonctions:
│   │       • create_monthly_stacked_bar()      : Barres mensuelles
│   │       • create_hierarchical_stacked_bar() : Multi-niveaux
│   │       • create_grouped_and_stacked_bar()  : Groupé + empilé
│   │       • add_comparison_line()             : Ajoute ligne objectif
│   │
│   ├── line_chart.py (à créer)
│   └── chart_factory.py (à créer)
│
└── tables/
    ├── hierarchical_table.py
    │   └── Fonctions:
    │       • create_hierarchical_table()   : Tableau avec profondeur
    │       • create_pivot_table()          : Tableau croisé
    │       • create_comparison_table()     : Comparaison périodes
    │       • _prepare_hierarchical_data()  : Prépare hiérarchie
    │       • _create_indent_styles()       : Styles indentation
    │
    └── table_builder.py (à créer)
```

### 🎛️ Modules de Composants UI

```
src/components/
│
├── sidebar.py (à créer)
│   └── create_sidebar()
│       • Filtres région
│       • Filtres période
│       • Sélection indicateurs
│
├── header.py (à créer)
│   └── create_header()
│       • Logo
│       • Navigation
│       • Actions utilisateur
│
└── dropdowns.py (à créer)
    └── Composants dropdown réutilisables
```

---

## 🔄 Cycles de Vie des Callbacks

### Callback de Mise à Jour des Données

```python
@app.callback(
    Output('data-store', 'data'),        # ← Où stocker
    [
        Input('indicator-dropdown', 'value'),    # ← Déclencheurs
        Input('region-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ]
)
def update_data_store(indicator, region, start, end):
    """
    ÉTAPES:
    1. Récupérer les valeurs des inputs
    2. Construire les filtres
    3. Appeler QueryBuilder
    4. Exécuter la requête
    5. Traiter les données si nécessaire
    6. Retourner JSON pour le store
    """
    pass
```

### Callback de Mise à Jour du Graphique

```python
@app.callback(
    Output('chart-container', 'children'),  # ← Où afficher
    [
        Input('data-store', 'data'),         # ← Source de données
        Input('indicator-dropdown', 'value')  # ← Configuration
    ]
)
def update_chart(json_data, indicator):
    """
    ÉTAPES:
    1. Charger les données du store
    2. Créer le graphique approprié
    3. Appliquer le styling
    4. Retourner le composant dcc.Graph
    """
    pass
```

---

## 🎨 Cascade de Styles CSS

```
NIVEAU 1: Variables Globales (assets/styles.css)
:root {
    --primary-color: #16697a;
    --secondary-color: #489fb5;
}

            ▼

NIVEAU 2: Classes de Composants
.sidebar { background-color: var(--primary-color); }
.chart-container { padding: 20px; }

            ▼

NIVEAU 3: Styles Dash Inline
style_header={'backgroundColor': '#2c3e50'}

            ▼

NIVEAU 4: Styles Plotly
fig.update_layout(plot_bgcolor='white')
```

---

## 💾 Gestion du Cache (Optionnel)

```
REQUÊTE UTILISATEUR
        │
        ▼
    ┌───────┐
    │ Cache?│
    └───┬───┘
        │
    OUI │ NON
        │  │
        │  ▼
        │ ┌────────────┐
        │ │   SGBD     │
        │ └─────┬──────┘
        │       │
        │       ▼
        │ ┌────────────┐
        │ │Sauver Cache│
        │ └─────┬──────┘
        │       │
        └───────┴───────▶ RÉSULTAT
```

### Configuration Redis

```python
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes
}

@cache.memoize(timeout=300)
def get_sales_data(indicator, filters):
    # Données mises en cache pendant 5 minutes
    pass
```

---

## 🔐 Flux de Sécurité

```
REQUÊTE UTILISATEUR
        │
        ▼
┌───────────────┐
│ Validation    │
│ des Inputs    │◄── Empêche injections
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Construction  │
│ Requête Sûre  │◄── Paramètres préparés
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Exécution BD  │◄── Pool de connexions limité
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Limitation    │
│ Résultats     │◄── MAX_ROWS_PER_QUERY
└───────┬───────┘
        │
        ▼
    RÉSULTAT
```

---

## 📈 Optimisations de Performance

### 1. Requêtes Optimisées
```sql
-- MAUVAIS: Charge tout puis filtre
SELECT * FROM ventes;  -- En Python: df[df.region == 'Nord']

-- BON: Filtre dans la BD
SELECT * FROM ventes WHERE region_id = 1;
```

### 2. Index de Base de Données
```sql
CREATE INDEX idx_ventes_date ON ventes(date_vente);
CREATE INDEX idx_ventes_region ON ventes(region_id);
CREATE INDEX idx_ventes_categorie ON ventes(categorie_principale);
```

### 3. Agrégations côté BD
```sql
-- MAUVAIS: Récupère toutes les lignes, agrège en Python
SELECT date_vente, montant_vente FROM ventes;

-- BON: Agrège dans la BD
SELECT 
  DATE_TRUNC('month', date_vente) as mois,
  SUM(montant_vente) as total
FROM ventes
GROUP BY mois;
```

### 4. Pagination pour Gros Volumes
```python
# Pour tableaux avec beaucoup de lignes
dash_table.DataTable(
    data=data,
    page_size=50,      # Affiche 50 lignes à la fois
    page_action='native'  # Pagination native
)
```

---

## 🎯 Résumé Visuel des Responsabilités

```
┌─────────────────────────────────────────────────┐
│ app.py                                          │
│ • Point d'entrée                                │
│ • Définit le layout                             │
│ • Enregistre les callbacks                      │
│ • Lance le serveur                              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ config/                                         │
│ • database.py    : Config connexion BD          │
│ • settings.py    : Paramètres app               │
│ • indicators.yaml: Définition KPIs              │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ src/database/                                   │
│ • connection.py  : Gère connexions BD           │
│ • query_builder.py: Construit requêtes SQL      │
│ • queries.py     : Templates réutilisables      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ src/data_processing/                            │
│ • aggregator.py  : Agrège données post-BD       │
│ • calculator.py  : Calcule indicateurs complexes│
│ • hierarchy_builder.py: Construit hiérarchies   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ src/visualizations/                             │
│ • charts/        : Graphiques Plotly            │
│   - stacked_bar.py, line_chart.py, etc.         │
│ • tables/        : Tableaux Dash                │
│   - hierarchical_table.py, pivot.py, etc.       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ src/components/                                 │
│ • sidebar.py     : Barre latérale filtres       │
│ • header.py      : En-tête navigation           │
│ • dropdowns.py   : Composants réutilisables     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ src/callbacks/                                  │
│ • filter_callbacks.py: Gère filtres             │
│ • chart_callbacks.py : Met à jour graphiques    │
│ • table_callbacks.py : Met à jour tableaux      │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ assets/                                         │
│ • styles.css     : Styles personnalisés         │
│ • logo.png       : Logo entreprise              │
└─────────────────────────────────────────────────┘
```

---

**Fin des diagrammes d'architecture** 🎉
