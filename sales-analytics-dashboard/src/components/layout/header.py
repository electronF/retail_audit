import dash_bootstrap_components as dbc
from src.components.layout.title_bar import create_title_bar
from src.components.layout.menu_bar import create_menu_bar

def create_header():
    return dbc.Container([
        create_title_bar(),
        create_menu_bar(),
    ], fluid=True, className="p-0")