import dash_bootstrap_components as dbc
from dash import html
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

from src.components.elements.input_radio import create_radio_group

 
def create_sidebar(indicators:list):
    """Crée la barre latérale avec les filtres"""
    return html.Div([
        dbc.Accordion(
            [
                # 1. ITEM INDICATEURS
                dbc.AccordionItem(
                    # Contenu du menu Indicateurs : placez ici votre liste déroulante ou vos radios
                    # Pour l'exemple, nous mettons un simple Div, vous le remplacerez par votre composant
                    html.Div([
                        html.Form([
                            create_radio_group(
                                id_name='select-database',
                                options_list=['Entreprise', 'Région', 'Ventes'],
                                default_value='Entreprise' # 'Entreprise' sera sélectionné au démarrage
                            )
                        ])
                    ]),
                    title="Base de données",
                    # Idée : vous pouvez laisser celui-ci ouvert par défaut si vous voulez
                    item_id="item-database" 
                ),
                
                # 1. ITEM INDICATEURS
                dbc.AccordionItem(
                    # Contenu du menu Indicateurs : placez ici votre liste déroulante ou vos radios
                    # Pour l'exemple, nous mettons un simple Div, vous le remplacerez par votre composant
                    html.Div("Liste des indicateurs à sélectionner (Dropdown, Checkbox, etc.)"),
                    title="Indicateurs",
                    # Idée : vous pouvez laisser celui-ci ouvert par défaut si vous voulez
                    item_id="item-indicateurs" 
                ),

                # 2. ITEM RÉGION
                dbc.AccordionItem(
                    html.Div("Liste des régions"),
                    title="Région",
                    item_id="item-region"
                ),

                # 3. ITEM PÉRIODE
                dbc.AccordionItem(
                    html.Div("Sélection de la période (RangeSlider, DatePicker)"),
                    title="Période",
                    item_id="item-periode"
                ),
            ],
            # L'ID est important pour les Callbacks si vous voulez manipuler l'accordéon
            id="sidebar-accordion", 
            active_item=["item-indicateurs"] # Garde l'item Indicateurs ouvert par défaut
        ),
        
        # Section Indicateurs
        # html.Div([
        #     html.H6("Indicateurs", className="mb-2 fw-bold"),
        #     dcc.Dropdown(
        #         id='indicator-dropdown',
        #         options=indicators,
        #         value='ca_total',
        #         clearable=False,
        #         className="mb-3"
        #     ),
        #     html.Div(id='indicator-list', className="mb-3")
        # ], className="mb-4"),
        
        # # Section Région
        # html.Div([
        #     html.H6("Région", className="mb-2 fw-bold"),
        #     dcc.Dropdown(
        #         id='region-dropdown',
        #         options=[
        #             {'label': 'Toutes les régions', 'value': 'all'},
        #             {'label': 'Nord', 'value': 'nord'},
        #             {'label': 'Sud', 'value': 'sud'},
        #             {'label': 'Est', 'value': 'est'},
        #             {'label': 'Ouest', 'value': 'ouest'}
        #         ],
        #         value='all',
        #         clearable=False
        #     )
        # ], className="mb-4"),
        
        # # Section Période
        # html.Div([
        #     html.H6("Période", className="mb-2 fw-bold"),
        #     dcc.DatePickerRange(
        #         id='date-picker',
        #         start_date=datetime.now() - timedelta(days=365),
        #         end_date=datetime.now(),
        #         display_format='DD/MM/YYYY',
        #         className="w-100"
        #     )
        # ], className="mb-4"),
        
    ], className="sidebar p-0")