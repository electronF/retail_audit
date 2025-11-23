import dash_bootstrap_components as dbc
from dash import dcc

def create_radio_group(id_name, options_list, default_value):
    return dbc.Card( # dbc.Card est utilisé ici pour encadrer et styliser le filtre
        dbc.CardBody([
            dcc.RadioItems(
                id=id_name,
                options=[
                    # Chaque dictionnaire représente un bouton radio :
                    {'label': option, 'value': option}
                    for option in options_list
                ],
                value=default_value, # La valeur sélectionnée par défaut
                inline=False,         # Affiche les boutons côte à côte (horizontalement)
                className="c-flex justify-content-around" # Style Bootstrap pour espacer
            )
        ])
    )