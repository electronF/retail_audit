"""
Module de création de diagrammes à bandes superposées
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Optional, Dict


class StackedBarChart:
    """Créateur de diagrammes à bandes superposées (stacked bar charts)"""
    
    def __init__(self, color_scheme: str = "Viridis"):
        self.color_scheme = color_scheme
        self.default_colors = px.colors.qualitative.Set3
    
    def create_monthly_stacked_bar(
        self,
        data: pd.DataFrame,
        x_column: str = "periode",
        y_column: str = "valeur",
        stack_column: str = "categorie",
        title: str = "Évolution Mensuelle",
        y_axis_title: str = "Montant (€)",
        show_total: bool = True
    ) -> go.Figure:
        """
        Crée un diagramme à bandes empilées par mois
        
        Args:
            data: DataFrame avec colonnes [periode, valeur, categorie]
            x_column: Colonne pour l'axe X (généralement période)
            y_column: Colonne pour les valeurs
            stack_column: Colonne pour segmenter les bandes
            title: Titre du graphique
            y_axis_title: Titre de l'axe Y
            show_total: Afficher le total au sommet de chaque bande
            
        Returns:
            Figure Plotly
        """
        fig = go.Figure()
        
        # Obtenir toutes les catégories uniques
        categories = data[stack_column].unique()
        
        # Créer une trace pour chaque catégorie
        for idx, category in enumerate(categories):
            category_data = data[data[stack_column] == category]
            
            fig.add_trace(go.Bar(
                name=str(category),
                x=category_data[x_column],
                y=category_data[y_column],
                text=category_data[y_column].apply(lambda x: f"{x:,.0f}"),
                textposition='inside',
                textangle=0,
                marker_color=self.default_colors[idx % len(self.default_colors)],
                hovertemplate=(
                    f"<b>{category}</b><br>" +
                    f"{x_column}: %{{x}}<br>" +
                    f"{y_axis_title}: %{{y:,.0f}}<br>" +
                    "<extra></extra>"
                )
            ))
        
        # Configuration du layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#2c3e50'}
            },
            barmode='stack',
            xaxis={
                'title': 'Période',
                'tickangle': -45,
                'tickfont': {'size': 11}
            },
            yaxis={
                'title': y_axis_title,
                'tickformat': ',.0f',
                'gridcolor': '#e0e0e0'
            },
            legend={
                'orientation': 'v',
                'yanchor': 'top',
                'y': 1,
                'xanchor': 'left',
                'x': 1.02,
                'bgcolor': 'rgba(255, 255, 255, 0.8)',
                'bordercolor': '#d0d0d0',
                'borderwidth': 1
            },
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            height=500,
            margin=dict(l=80, r=150, t=80, b=80)
        )
        
        # Ajouter les totaux au sommet si demandé
        if show_total:
            totals = data.groupby(x_column)[y_column].sum().reset_index()
            
            fig.add_trace(go.Scatter(
                x=totals[x_column],
                y=totals[y_column],
                mode='text',
                text=totals[y_column].apply(lambda x: f"Total: {x:,.0f}"),
                textposition='top center',
                textfont=dict(size=10, color='#2c3e50', family='Arial Black'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        return fig
    
    def create_hierarchical_stacked_bar(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        hierarchy_columns: List[str],
        title: str = "Analyse Hiérarchique"
    ) -> go.Figure:
        """
        Crée un diagramme avec plusieurs niveaux de hiérarchie
        
        Args:
            data: DataFrame avec colonnes hiérarchiques
            x_column: Colonne pour l'axe X
            y_column: Colonne pour les valeurs
            hierarchy_columns: Liste des colonnes de hiérarchie 
                              ['categorie', 'sous_categorie', 'produit']
        """
        fig = go.Figure()
        
        # Créer une colonne combinée pour la légende
        data['hierarchy_label'] = data[hierarchy_columns].apply(
            lambda row: ' > '.join([str(val) for val in row if pd.notna(val)]),
            axis=1
        )
        
        # Grouper par la hiérarchie complète
        grouped = data.groupby([x_column, 'hierarchy_label'])[y_column].sum().reset_index()
        
        # Créer les traces
        for label in grouped['hierarchy_label'].unique():
            label_data = grouped[grouped['hierarchy_label'] == label]
            
            fig.add_trace(go.Bar(
                name=label,
                x=label_data[x_column],
                y=label_data[y_column],
                hovertemplate=(
                    f"<b>{label}</b><br>" +
                    f"%{{x}}: %{{y:,.0f}}<br>" +
                    "<extra></extra>"
                )
            ))
        
        fig.update_layout(
            title=title,
            barmode='stack',
            xaxis_title='Période',
            yaxis_title='Valeur',
            hovermode='x unified',
            height=600
        )
        
        return fig
    
    def create_grouped_and_stacked_bar(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        group_column: str,
        stack_column: str,
        title: str = "Comparaison Groupée et Empilée"
    ) -> go.Figure:
        """
        Crée un graphique avec à la fois groupement et empilement
        Exemple: Grouper par année, empiler par catégorie
        """
        fig = go.Figure()
        
        # Obtenir les valeurs uniques pour les groupes et les stacks
        groups = data[group_column].unique()
        stacks = data[stack_column].unique()
        
        # Pour chaque niveau de stack
        for stack_val in stacks:
            x_positions = []
            y_values = []
            text_values = []
            
            for group_val in groups:
                filtered = data[
                    (data[group_column] == group_val) & 
                    (data[stack_column] == stack_val)
                ]
                
                if not filtered.empty:
                    x_positions.append(f"{group_val}")
                    y_values.append(filtered[y_column].sum())
                    text_values.append(f"{filtered[y_column].sum():,.0f}")
            
            fig.add_trace(go.Bar(
                name=str(stack_val),
                x=x_positions,
                y=y_values,
                text=text_values,
                textposition='inside'
            ))
        
        fig.update_layout(
            title=title,
            barmode='stack',
            xaxis_title=group_column.capitalize(),
            yaxis_title='Valeur',
            height=500
        )
        
        return fig
    
    def add_comparison_line(
        self,
        fig: go.Figure,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        line_name: str = "Objectif",
        line_color: str = "red"
    ) -> go.Figure:
        """
        Ajoute une ligne de comparaison (ex: objectif) sur le graphique
        """
        fig.add_trace(go.Scatter(
            name=line_name,
            x=data[x_column],
            y=data[y_column],
            mode='lines+markers',
            line=dict(color=line_color, width=3, dash='dash'),
            marker=dict(size=8),
            yaxis='y2'
        ))
        
        # Ajouter un second axe Y si nécessaire
        fig.update_layout(
            yaxis2=dict(
                title=line_name,
                overlaying='y',
                side='right'
            )
        )
        
        return fig


# Fonction utilitaire pour créer rapidement un graphique
def quick_stacked_bar(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: str,
    title: str = "Graphique"
) -> go.Figure:
    """
    Fonction rapide pour créer un graphique empilé simple
    """
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        barmode='stack',
        text_auto='.0f'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        hovermode='x unified'
    )
    
    return fig
