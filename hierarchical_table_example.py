"""
Module de création de tableaux hiérarchiques avec profondeur
"""
import pandas as pd
from dash import dash_table, html
import dash_bootstrap_components as dbc
from typing import List, Dict, Any, Optional


class HierarchicalTable:
    """Créateur de tableaux hiérarchiques interactifs"""
    
    def __init__(self):
        self.indent_width = 20  # pixels d'indentation par niveau
    
    def create_hierarchical_table(
        self,
        data: pd.DataFrame,
        hierarchy_columns: List[str],
        metric_columns: List[str],
        expandable: bool = True
    ) -> dash_table.DataTable:
        """
        Crée un tableau hiérarchique avec indentations visuelles
        
        Args:
            data: DataFrame avec les données
            hierarchy_columns: Colonnes de hiérarchie ['categorie', 'sous_categorie', 'produit']
            metric_columns: Colonnes de métriques ['mois_1', 'mois_2', etc.]
            expandable: Permettre l'expansion/collapse des lignes
            
        Returns:
            Composant dash_table.DataTable
        """
        # Préparer les données avec niveaux et indentations
        prepared_data = self._prepare_hierarchical_data(
            data, 
            hierarchy_columns, 
            metric_columns
        )
        
        # Définir les colonnes du tableau
        columns = self._define_columns(hierarchy_columns, metric_columns)
        
        # Créer le style conditionnel pour les indentations
        style_data_conditional = self._create_indent_styles(hierarchy_columns)
        
        # Ajouter le style pour les totaux/sous-totaux
        style_data_conditional.extend([
            {
                'if': {'filter_query': '{is_total} = true'},
                'fontWeight': 'bold',
                'backgroundColor': '#f0f0f0'
            },
            {
                'if': {'filter_query': '{is_subtotal} = true'},
                'fontWeight': 'bold',
                'backgroundColor': '#f8f8f8'
            }
        ])
        
        # Créer le DataTable
        table = dash_table.DataTable(
            data=prepared_data.to_dict('records'),
            columns=columns,
            style_table={
                'overflowX': 'auto',
                'minWidth': '100%'
            },
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'fontSize': '14px',
                'padding': '10px'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '8px',
                'fontSize': '13px',
                'fontFamily': 'Arial, sans-serif',
                'border': '1px solid #ddd'
            },
            style_data_conditional=style_data_conditional,
            style_cell_conditional=[
                {
                    'if': {'column_id': hierarchy_columns[0]},
                    'minWidth': '250px',
                    'maxWidth': '250px',
                    'whiteSpace': 'normal'
                }
            ] + [
                {
                    'if': {'column_id': col},
                    'textAlign': 'right',
                    'fontFamily': 'monospace'
                }
                for col in metric_columns
            ],
            page_size=50,
            page_action='native',
            sort_action='native',
            filter_action='native',
            export_format='xlsx',
            export_headers='display'
        )
        
        return table
    
    def _prepare_hierarchical_data(
        self,
        data: pd.DataFrame,
        hierarchy_columns: List[str],
        metric_columns: List[str]
    ) -> pd.DataFrame:
        """
        Prépare les données avec calcul des sous-totaux et totaux
        """
        result_rows = []
        
        # Grouper par le premier niveau de hiérarchie
        for level1_value in data[hierarchy_columns[0]].unique():
            level1_data = data[data[hierarchy_columns[0]] == level1_value]
            
            # Ajouter la ligne de niveau 1
            level1_row = self._create_row(
                level1_value,
                level1_data[metric_columns].sum(),
                level=0,
                is_total=False,
                is_subtotal=True if len(hierarchy_columns) > 1 else False
            )
            result_rows.append(level1_row)
            
            # Si il y a un deuxième niveau
            if len(hierarchy_columns) > 1:
                for level2_value in level1_data[hierarchy_columns[1]].unique():
                    level2_data = level1_data[
                        level1_data[hierarchy_columns[1]] == level2_value
                    ]
                    
                    # Ajouter la ligne de niveau 2
                    level2_row = self._create_row(
                        level2_value,
                        level2_data[metric_columns].sum(),
                        level=1,
                        is_total=False,
                        is_subtotal=True if len(hierarchy_columns) > 2 else False
                    )
                    result_rows.append(level2_row)
                    
                    # Si il y a un troisième niveau
                    if len(hierarchy_columns) > 2:
                        for level3_value in level2_data[hierarchy_columns[2]].unique():
                            level3_data = level2_data[
                                level2_data[hierarchy_columns[2]] == level3_value
                            ]
                            
                            # Ajouter la ligne de niveau 3
                            level3_row = self._create_row(
                                level3_value,
                                level3_data[metric_columns].sum(),
                                level=2,
                                is_total=False,
                                is_subtotal=False
                            )
                            result_rows.append(level3_row)
        
        # Ajouter la ligne de total général
        total_row = self._create_row(
            "TOTAL GÉNÉRAL",
            data[metric_columns].sum(),
            level=0,
            is_total=True,
            is_subtotal=False
        )
        result_rows.append(total_row)
        
        result_df = pd.DataFrame(result_rows)
        return result_df
    
    def _create_row(
        self,
        label: str,
        metrics: pd.Series,
        level: int,
        is_total: bool,
        is_subtotal: bool
    ) -> Dict[str, Any]:
        """
        Crée une ligne de données avec indentation
        """
        indent = "  " * level  # Indentation textuelle
        
        row = {
            'label': f"{indent}{label}",
            'level': level,
            'is_total': is_total,
            'is_subtotal': is_subtotal
        }
        
        # Ajouter les métriques formatées
        for col_name, value in metrics.items():
            row[col_name] = self._format_number(value)
        
        return row
    
    def _define_columns(
        self,
        hierarchy_columns: List[str],
        metric_columns: List[str]
    ) -> List[Dict[str, str]]:
        """
        Définit les colonnes du tableau
        """
        columns = [
            {
                'id': 'label',
                'name': hierarchy_columns[0].replace('_', ' ').title(),
                'type': 'text'
            }
        ]
        
        # Ajouter les colonnes de métriques
        for col in metric_columns:
            columns.append({
                'id': col,
                'name': col.replace('_', ' ').title(),
                'type': 'numeric',
                'format': {'specifier': ',.0f'}
            })
        
        return columns
    
    def _create_indent_styles(
        self,
        hierarchy_columns: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Crée les styles pour l'indentation visuelle
        """
        styles = []
        
        for level in range(len(hierarchy_columns)):
            styles.append({
                'if': {
                    'filter_query': f'{{level}} = {level}',
                    'column_id': 'label'
                },
                'paddingLeft': f'{self.indent_width * level}px'
            })
        
        return styles
    
    def _format_number(self, value: float) -> str:
        """
        Formate un nombre pour l'affichage
        """
        if pd.isna(value):
            return "-"
        return f"{value:,.0f}".replace(',', ' ')
    
    def create_pivot_table(
        self,
        data: pd.DataFrame,
        index_cols: List[str],
        column_col: str,
        value_col: str,
        aggfunc: str = 'sum'
    ) -> dash_table.DataTable:
        """
        Crée un tableau croisé dynamique (pivot table)
        
        Args:
            data: DataFrame source
            index_cols: Colonnes pour les lignes
            column_col: Colonne pour les en-têtes de colonnes
            value_col: Colonne des valeurs à agréger
            aggfunc: Fonction d'agrégation ('sum', 'mean', 'count', etc.)
        """
        # Créer le pivot
        pivot = pd.pivot_table(
            data,
            values=value_col,
            index=index_cols,
            columns=column_col,
            aggfunc=aggfunc,
            fill_value=0
        )
        
        # Réinitialiser l'index pour avoir des colonnes normales
        pivot_reset = pivot.reset_index()
        
        # Formater les nombres
        for col in pivot_reset.columns:
            if col not in index_cols:
                pivot_reset[col] = pivot_reset[col].apply(
                    lambda x: f"{x:,.0f}".replace(',', ' ')
                )
        
        # Créer le DataTable
        table = dash_table.DataTable(
            data=pivot_reset.to_dict('records'),
            columns=[{'name': str(col), 'id': str(col)} for col in pivot_reset.columns],
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': '#34495e',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'textAlign': 'right',
                'padding': '8px',
                'fontFamily': 'monospace'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': index_cols[0]},
                    'textAlign': 'left',
                    'fontWeight': 'bold',
                    'fontFamily': 'Arial'
                }
            ],
            export_format='xlsx'
        )
        
        return table


def create_comparison_table(
    data1: pd.DataFrame,
    data2: pd.DataFrame,
    label1: str = "Période 1",
    label2: str = "Période 2",
    show_variance: bool = True
) -> dash_table.DataTable:
    """
    Crée un tableau de comparaison entre deux périodes
    """
    # Fusionner les deux DataFrames
    comparison = pd.merge(
        data1,
        data2,
        on='label',
        suffixes=(f'_{label1}', f'_{label2}')
    )
    
    # Calculer les écarts si demandé
    if show_variance:
        metric_cols = [col for col in data1.columns if col != 'label']
        for col in metric_cols:
            col1 = f"{col}_{label1}"
            col2 = f"{col}_{label2}"
            comparison[f'{col}_variance'] = comparison[col2] - comparison[col1]
            comparison[f'{col}_variance_pct'] = (
                (comparison[col2] - comparison[col1]) / comparison[col1] * 100
            )
    
    # Créer le tableau
    table = dash_table.DataTable(
        data=comparison.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in comparison.columns],
        style_header={'backgroundColor': '#27ae60', 'color': 'white'},
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{variance_pct} > 0',
                    'column_id': [col for col in comparison.columns if 'variance' in col]
                },
                'backgroundColor': '#d4edda',
                'color': '#155724'
            },
            {
                'if': {
                    'filter_query': '{variance_pct} < 0',
                    'column_id': [col for col in comparison.columns if 'variance' in col]
                },
                'backgroundColor': '#f8d7da',
                'color': '#721c24'
            }
        ]
    )
    
    return table
