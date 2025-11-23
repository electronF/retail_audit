from dash import html
import dash_bootstrap_components as dbc

from src.utils.style  import Colors as colors

 
def create_menu_bar():
    """Crée l'en-tête de l'application"""
    return dbc.Navbar(
        dbc.Container([ 
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3("DataBank", className="mb-0", style={'color': colors.secondary_text_color}),
                        html.Small("Nom de la base de données", style={'color': colors.secondary_text_color})
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
        color=colors.secondary_color,
        dark=True,
        className="mb-3"
    )