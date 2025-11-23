from dash import html
import dash_bootstrap_components as dbc
from src.utils.style  import Colors as colors


# 1. Le Header (Zone bleu clair tout en haut)
def create_footer_bar(): 
    return html.Div(
    [html.Div("Droits réservés © Productivité Aggressive - 2025", className="p-1 mb-0")],
    # [
    #         html.P(f"Droits réservés - Mon Entreprise {html.Unescape(' &copy; ')} {2025}", 
    #                className="text-center p-3 m-0")
    # ],
    className="mb-0", 
    style={"backgroundColor": colors.divider_color, "color": colors.primary_text_color} # Couleur bleu clair style image 1
)