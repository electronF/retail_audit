import dash_bootstrap_components as dbc
from dash import html
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

def create_sidebar(indicators:list):
    """Crée la barre latérale avec les filtres"""
    return html.Div([
        # Section Indicateurs
        html.Div([
            html.H6("Indicateurs", className="mb-2 fw-bold"),
            dcc.Dropdown(
                id='indicator-dropdown',
                options=indicators,
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