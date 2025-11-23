import dash_bootstrap_components as dbc
from dash import dcc, html


def create_filter_section(indicators:list, categories:list, granularities:list):
    """Crée la section des filtres au-dessus du contenu principal"""
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.Label("Indicateurs", className="fw-bold mb-1"),
                dcc.Dropdown( 
                    id='main-indicator-dropdown',
                    options=indicators,
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
                    options=categories,
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
                    options=granularities,
                    value='entreprise',
                    clearable=False
                )
            ])
        ], width=3),
        
    ], className="mb-4 p-3 bg-light rounded")
    

def create_page_content(indicators:list, categories:list, granularities:list):
    """Crée la zone de contenu principal"""
    return html.Div([
        # Filtres en haut
        create_filter_section(indicators, categories, granularities),
        
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
