import dash_bootstrap_components as dbc

from src.components.layout.sidebar import create_sidebar
from src.components.layout.page_content import create_page_content

def create_main_content(indicators:list, categories:list, granularities:list):
    return dbc.Row([
        # Side bar content
        dbc.Col([
                create_sidebar(indicators),
            ], width=3, className="pe-0"),
            
            # Main content
            dbc.Col([
                create_page_content(indicators, categories, granularities)
            ], width=9)
    ], className="pe-0")
    
     