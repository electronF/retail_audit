import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Initialisation avec un thème Bootstrap (pour avoir une base propre)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# --- DONNÉES MOCKUP (Pour l'exemple) ---
df = pd.DataFrame({
    "Mois": ["Jan", "Jan", "Feb", "Feb"],
    "Marque": ["XXL", "Monster", "XXL", "Monster"],
    "Valeur": [10, 20, 15, 25],
    "Indicateur": ["Ventes", "Ventes", "Ventes", "Ventes"]
})

# --- COMPOSANTS ---

# 1. Le Header (Zone bleu clair tout en haut)
header = html.Div(
    [html.H4("Logo + informations supplémentaires", className="p-3")],
    style={"backgroundColor": "#B2EBF2"} # Couleur bleu clair style image 1
)

# 2. La Navbar (Zone bleu foncé avec boutons)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Tableau", id="btn-tableau", n_clicks=0, href="#")),
        dbc.NavItem(dbc.NavLink("Graphique", id="btn-graphique", n_clicks=0, href="#")),
        dbc.Button("Téléchargement", color="light", outline=True, className="ms-2"),
    ],
    brand="DataBank | Nom de la base de donnée",
    color="#00798C", # Bleu pétrole
    dark=True,
    fluid=True,
)

# 3. La Sidebar (Accordéons dynamiques à gauche)
def create_sidebar():
    # Tu peux ajouter autant d'items que tu veux ici via une boucle
    items = ["Indicateurs", "Region", "Periode", "Categorie 3", "Marques"]
    accordion_items = []
    
    for item in items:
        accordion_items.append(
            dbc.AccordionItem(
                [html.P(f"Contenu pour {item}...")], # Ici tu mettras tes Checkbox ou RadioItems
                title=item
            )
        )
    
    return html.Div(
        dbc.Accordion(accordion_items, start_collapsed=True),
        style={"backgroundColor": "#E0E0E0", "height": "100vh", "padding": "10px"}
    )

# 4. Filtres du haut (dans la zone principale)
top_filters = dbc.Row([
    dbc.Col(dcc.Dropdown(["Indicateur 1", "Indicateur 2"], "Indicateur 1", id="dd-indicateur"), width=4),
    dbc.Col(dcc.Dropdown(["Bierre", "Jus"], "Bierre", id="dd-categorie"), width=4),
    dbc.Col(dcc.Dropdown(["Entreprise", "Marque"], "Entreprise", id="dd-granularite"), width=4),
], className="mb-4 mt-3")

# --- LAYOUT PRINCIPAL ---
app.layout = html.Div([
    header,
    navbar,
    dbc.Container([
        dbc.Row([
            # Colonne Gauche (Sidebar) - largeur 3/12
            dbc.Col(create_sidebar(), width=3, className="p-0"),
            
            # Colonne Droite (Contenu Principal) - largeur 9/12
            dbc.Col([
                top_filters,
                html.Div(id="main-content-area") # Le contenu changera ici (Graph ou Table)
            ], width=9)
        ])
    ], fluid=True) # fluid=True permet d'utiliser toute la largeur de l'écran
])

# --- LOGIQUE (CALLBACKS) ---
@callback(
    Output("main-content-area", "children"),
    [Input("btn-tableau", "n_clicks"),
     Input("btn-graphique", "n_clicks"),
     Input("dd-indicateur", "value")]
)
def update_view(btn_tab, btn_graph, indicator):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-graphique'

    if button_id == "btn-tableau":
        # Retourner le Tableau (Image 3)
        return html.Div([
            html.H5("Vue Tableau"),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            # Note: Pour le tableau complexe coloré (Image 3), on utilisera dash_table.DataTable plus tard
        ])
    else:
        # Retourner le Graphique (Image 2)
        fig = px.bar(df, x="Mois", y="Valeur", color="Marque", title=f"Données pour {indicator}", barmode="stack")
        # Personnalisation des couleurs pour ressembler à ton image
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        
        return dcc.Graph(figure=fig)

if __name__ == "__main__":
    app.run_server(debug=True)