from dash import html
import dash_bootstrap_components as dbc
from src.utils.style  import Colors as colors


# 1. Le Header (Zone bleu clair tout en haut)
def create_title_bar(): 
    return html.Div(
    [html.H4("Logo + informations supplémentaires", className="p-3 mb-0")],
    className="mb-0", 
    style={"backgroundColor": colors.light_primary_color, "color": colors.primary_text_color} # Couleur bleu clair style image 1
)