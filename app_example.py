"""
Application Dash principale pour le dashboard analytique
"""
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Imports des modules personnalisés (à adapter selon votre structure)
# from src.database.connection import get_db_connection
# from src.database.query_builder import QueryBuilder
# from src.visualizations.charts.stacked_bar import StackedBarChart
# from src.visualizations.tables.hierarchical_table import HierarchicalTable

# Initialisation de l'application
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Configuration
INDICATORS = [
    {'label': 'Chiffre d\'Affaires', 'value': 'ca_total'},
    {'label': 'Quantité Vendue', 'value': 'quantite_vendue'},
    {'label': 'Nombre de Transactions', 'value': 'nombre_transactions'},
    {'label': 'Panier Moyen', 'value': 'panier_moyen'}
]

GRANULARITIES = [
    {'label': 'Entreprise', 'value': 'entreprise'},
    {'label': 'Catégorie', 'value': 'categorie'},
    {'label': 'Sous-catégorie', 'value': 'sous_categorie'},
    {'label': 'Produit', 'value': 'produit'}
]

CATEGORIES = [
    {'label': 'Toutes', 'value': 'all'},
    {'label': 'Électronique', 'value': 'electronique'},
    {'label': 'Vêtements', 'value': 'vetements'},
    {'label': 'Alimentation', 'value': 'alimentation'}
]

# ============================================
# LAYOUT DE L'APPLICATION
# ============================================

def create_header():
    """Crée l'en-tête de l'application"""
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("DataBank", className="mb-0", style={'color': 'white'}),
                        html.Small("Nom de la base de données", style={'color': '#95a5a6'})
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("tableau", active=True, href="#")),
                        dbc.NavItem(dbc.NavLink("graphique", href="#")),
                        dbc.NavItem(dbc.NavLink("Telechargement", href="#"))
                    ], pills=True)
                ], width=6, className="d-flex justify-content-center"),
            ], className="w-100 align-items-center")
        ], fluid=True),
        color="#16697a",
        dark=True,
        className="mb-3"
    )

def create_sidebar():
    """Crée la barre latérale avec les filtres"""
    return html.Div([
        # Section Indicateurs
        html.Div([
            html.H6("Indicateurs", className="mb-2 fw-bold"),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=INDICATORS,
                value='ca_total',
                clearable=False,
                className="mb-3"
            ),
            html.Div(id='indicator-list', className="mb-3")
        ], className="mb-4"),
        
        # Section Région
        html.Div([
            html.H6("Région", className="mb-2 fw-bold"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': 'Toutes les régions', 'value': 'all'},
                    {'label': 'Nord', 'value': 'nord'},
                    {'label': 'Sud', 'value': 'sud'},
                    {'label': 'Est', 'value': 'est'},
                    {'label': 'Ouest', 'value': 'ouest'}
                ],
                value='all',
                clearable=False
            )
        ], className="mb-4"),
        
        # Section Période
        html.Div([
            html.H6("Période", className="mb-2 fw-bold"),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=datetime.now() - timedelta(days=365),
                end_date=datetime.now(),
                display_format='DD/MM/YYYY',
                className="w-100"
            )
        ], className="mb-4"),
        
    ], className="sidebar p-3")

def create_filter_section():
    """Crée la section des filtres au-dessus du contenu principal"""
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.Label("Indicateurs", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='main-indicator-dropdown',
                    options=INDICATORS,
                    value='ca_total',
                    clearable=False
                )
            ])
        ], width=3),
        
        dbc.Col([
            html.Div([
                html.Label("Catégorie", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=CATEGORIES,
                    value='all',
                    clearable=False
                )
            ])
        ], width=3),
        
        dbc.Col([
            html.Div([
                html.Label("Granularité", className="fw-bold mb-1"),
                dcc.Dropdown(
                    id='granularity-dropdown',
                    options=GRANULARITIES,
                    value='entreprise',
                    clearable=False
                )
            ])
        ], width=3),
        
    ], className="mb-4 p-3 bg-light rounded")

def create_main_content():
    """Crée la zone de contenu principal"""
    return html.Div([
        # Filtres en haut
        create_filter_section(),
        
        # Onglets pour basculer entre tableau et graphique
        dbc.Tabs([
            dbc.Tab(
                html.Div(id='chart-container', className="p-4"),
                label="Graphique",
                tab_id="tab-chart"
            ),
            dbc.Tab(
                html.Div(id='table-container', className="p-4"),
                label="Tableau",
                tab_id="tab-table"
            )
        ], id='tabs', active_tab='tab-chart'),
        
        # Loading overlay
        dcc.Loading(
            id="loading",
            type="circle",
            children=html.Div(id="loading-output")
        )
    ])

# Layout principal
app.layout = html.Div([
    create_header(),
    
    dbc.Container([
        dbc.Row([
            # Sidebar
            dbc.Col([
                create_sidebar()
            ], width=2, className="pe-0"),
            
            # Main content
            dbc.Col([
                create_main_content()
            ], width=10)
        ])
    ], fluid=True),
    
    # Store pour les données
    dcc.Store(id='data-store')
], className="dashboard-container")

# ============================================
# CALLBACKS
# ============================================

@app.callback(
    Output('data-store', 'data'),
    [
        Input('main-indicator-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('granularity-dropdown', 'value'),
        Input('region-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ]
)
def update_data_store(indicator, category, granularity, region, start_date, end_date):
    """
    Récupère les données de la base de données selon les filtres
    """
    # Ici, vous appelleriez votre QueryBuilder et DatabaseConnection
    # query_builder = QueryBuilder()
    # db = get_db_connection()
    
    # filters = {
    #     'region': [region] if region != 'all' else None,
    #     'categorie': [category] if category != 'all' else None,
    #     'date_debut': start_date,
    #     'date_fin': end_date
    # }
    
    # query, params = query_builder.build_query(indicator, filters, granularity)
    # data = db.execute_query(query, params)
    
    # Pour l'exemple, générer des données fictives
    dates = pd.date_range(start=start_date, end=end_date, freq='MS')
    categories_list = ['Catégorie A', 'Catégorie B', 'Catégorie C']
    
    data_list = []
    for date in dates:
        for cat in categories_list:
            data_list.append({
                'periode': date.strftime('%Y-%m'),
                'categorie': cat,
                'valeur': pd.np.random.randint(10000, 50000)
            })
    
    df = pd.DataFrame(data_list)
    
    return df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('chart-container', 'children'),
    [
        Input('data-store', 'data'),
        Input('main-indicator-dropdown', 'value')
    ]
)
def update_chart(json_data, indicator):
    """
    Met à jour le graphique selon les données
    """
    if json_data is None:
        return html.Div("Aucune donnée disponible")
    
    df = pd.read_json(json_data, orient='split')
    
    # Créer le graphique à bandes empilées
    fig = go.Figure()
    
    for category in df['categorie'].unique():
        cat_data = df[df['categorie'] == category]
        fig.add_trace(go.Bar(
            name=category,
            x=cat_data['periode'],
            y=cat_data['valeur'],
            text=cat_data['valeur'].apply(lambda x: f"{x:,.0f}"),
            textposition='inside'
        ))
    
    fig.update_layout(
        title="Évolution de l'indicateur par période",
        barmode='stack',
        xaxis_title="Période",
        yaxis_title="Valeur",
        hovermode='x unified',
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return dcc.Graph(figure=fig)

@app.callback(
    Output('table-container', 'children'),
    Input('data-store', 'data')
)
def update_table(json_data):
    """
    Met à jour le tableau selon les données
    """
    if json_data is None:
        return html.Div("Aucune donnée disponible")
    
    df = pd.read_json(json_data, orient='split')
    
    # Créer un tableau pivot
    pivot = df.pivot_table(
        values='valeur',
        index='categorie',
        columns='periode',
        aggfunc='sum',
        fill_value=0
    ).reset_index()
    
    # Créer le DataTable
    from dash import dash_table
    
    table = dash_table.DataTable(
        data=pivot.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in pivot.columns],
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'right',
            'padding': '10px',
            'fontFamily': 'monospace'
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'categorie'},
                'textAlign': 'left',
                'fontWeight': 'bold'
            }
        ],
        export_format='xlsx',
        export_headers='display'
    )
    
    return table

@app.callback(
    Output('indicator-list', 'children'),
    Input('indicator-dropdown', 'value')
)
def update_indicator_list(selected_indicator):
    """
    Affiche la liste des indicateurs sélectionnés
    """
    # Ceci pourrait être étendu pour gérer plusieurs indicateurs
    indicator_name = next(
        (ind['label'] for ind in INDICATORS if ind['value'] == selected_indicator),
        selected_indicator
    )
    
    return html.Div([
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.Span(indicator_name, className="me-2"),
                    html.I(className="fas fa-times", style={'cursor': 'pointer'})
                ], className="d-flex justify-content-between align-items-center")
            ])
        ], className="mb-2", color="light")
    ])

# ============================================
# CSS PERSONNALISÉ
# ============================================

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashboard Analytique</title>
        {%favicon%}
        {%css%}
        <style>
            .sidebar {
                background-color: #ecf0f1;
                min-height: calc(100vh - 80px);
                border-right: 1px solid #bdc3c7;
            }
            
            .dashboard-container {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .nav-pills .nav-link.active {
                background-color: #3498db !important;
            }
            
            .Select-control {
                border-radius: 4px;
            }
            
            .card {
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ============================================
# LANCEMENT DE L'APPLICATION
# ============================================

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
