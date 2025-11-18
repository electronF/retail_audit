"""
Module de construction dynamique de requêtes SQL
"""
from typing import List, Dict, Any, Optional
from datetime import datetime


class QueryBuilder:
    """Constructeur de requêtes SQL dynamiques"""
    
    def __init__(self, schema: str = "sales"):
        self.schema = schema
        self.base_table = f"{schema}.ventes"
        
    def build_query(
        self,
        indicator_id: str,
        filters: Dict[str, Any],
        granularity: str,
        time_dimension: str = "mois"
    ) -> tuple[str, Dict[str, Any]]:
        """
        Construit une requête SQL dynamique
        
        Args:
            indicator_id: ID de l'indicateur à calculer
            filters: Dictionnaire des filtres {type: valeurs}
            granularity: Niveau de granularité (entreprise, categorie, produit)
            time_dimension: Dimension temporelle (jour, semaine, mois, annee)
            
        Returns:
            Tuple (query_string, params_dict)
        """
        # Mapping des indicateurs vers les colonnes
        indicator_mapping = {
            'ca_total': 'SUM(montant_vente) as valeur',
            'quantite_vendue': 'SUM(quantite) as valeur',
            'nombre_transactions': 'COUNT(DISTINCT transaction_id) as valeur',
            'panier_moyen': 'AVG(montant_vente) as valeur',
        }
        
        # Mapping de la granularité
        granularity_mapping = {
            'entreprise': [],
            'categorie': ['categorie_principale'],
            'sous_categorie': ['categorie_principale', 'sous_categorie'],
            'produit': ['categorie_principale', 'sous_categorie', 'produit_id', 'nom_produit']
        }
        
        # Mapping de la dimension temporelle
        time_mapping = {
            'jour': "DATE(date_vente)",
            'semaine': "DATE_TRUNC('week', date_vente)",
            'mois': "DATE_TRUNC('month', date_vente)",
            'annee': "DATE_TRUNC('year', date_vente)"
        }
        
        # Construction de la clause SELECT
        select_parts = [indicator_mapping.get(indicator_id, 'SUM(montant_vente) as valeur')]
        group_by_parts = []
        
        # Ajout de la dimension temporelle
        time_expr = time_mapping.get(time_dimension, "DATE_TRUNC('month', date_vente)")
        select_parts.append(f"{time_expr} as periode")
        group_by_parts.append(time_expr)
        
        # Ajout des dimensions de granularité
        granularity_columns = granularity_mapping.get(granularity, [])
        for col in granularity_columns:
            select_parts.append(col)
            group_by_parts.append(col)
        
        # Construction de la clause WHERE
        where_clauses = []
        params = {}
        
        if 'region' in filters and filters['region']:
            where_clauses.append("region_id = ANY(:regions)")
            params['regions'] = filters['region']
        
        if 'categorie' in filters and filters['categorie']:
            where_clauses.append("categorie_principale = ANY(:categories)")
            params['categories'] = filters['categorie']
        
        if 'date_debut' in filters and filters['date_debut']:
            where_clauses.append("date_vente >= :date_debut")
            params['date_debut'] = filters['date_debut']
        
        if 'date_fin' in filters and filters['date_fin']:
            where_clauses.append("date_vente <= :date_fin")
            params['date_fin'] = filters['date_fin']
        
        # Assemblage de la requête
        query = f"""
        SELECT 
            {', '.join(select_parts)}
        FROM {self.base_table}
        """
        
        if where_clauses:
            query += f"\nWHERE {' AND '.join(where_clauses)}"
        
        if group_by_parts:
            query += f"\nGROUP BY {', '.join(group_by_parts)}"
        
        query += "\nORDER BY periode"
        
        if granularity_columns:
            query += ", " + ", ".join(granularity_columns)
        
        return query, params
    
    def build_hierarchy_query(
        self,
        indicator_id: str,
        filters: Dict[str, Any],
        hierarchy_levels: List[str],
        time_periods: List[str]
    ) -> tuple[str, Dict[str, Any]]:
        """
        Construit une requête pour un tableau hiérarchique
        
        Args:
            indicator_id: ID de l'indicateur
            filters: Dictionnaire des filtres
            hierarchy_levels: Liste des niveaux ['categorie', 'sous_categorie', 'produit']
            time_periods: Liste des périodes à afficher
            
        Returns:
            Tuple (query_string, params_dict)
        """
        indicator_mapping = {
            'ca_total': 'SUM(montant_vente)',
            'quantite_vendue': 'SUM(quantite)',
            'nombre_transactions': 'COUNT(DISTINCT transaction_id)',
        }
        
        indicator_expr = indicator_mapping.get(indicator_id, 'SUM(montant_vente)')
        
        # Construction des colonnes de hiérarchie
        hierarchy_cols = ', '.join(hierarchy_levels)
        
        # Construction des périodes
        # Utilise FILTER pour PostgreSQL ou CASE pour MySQL
        period_columns = []
        for period in time_periods:
            col = f"""
            {indicator_expr} FILTER (
                WHERE DATE_TRUNC('month', date_vente) = '{period}'::timestamp
            ) as "{period}"
            """
            period_columns.append(col)
        
        # Construction WHERE
        where_clauses = []
        params = {}
        
        if 'region' in filters and filters['region']:
            where_clauses.append("region_id = ANY(:regions)")
            params['regions'] = filters['region']
        
        if 'date_debut' in filters:
            where_clauses.append("date_vente >= :date_debut")
            params['date_debut'] = filters['date_debut']
        
        if 'date_fin' in filters:
            where_clauses.append("date_vente <= :date_fin")
            params['date_fin'] = filters['date_fin']
        
        # Assemblage
        query = f"""
        SELECT 
            {hierarchy_cols},
            {', '.join(period_columns)}
        FROM {self.base_table}
        """
        
        if where_clauses:
            query += f"\nWHERE {' AND '.join(where_clauses)}"
        
        query += f"\nGROUP BY {hierarchy_cols}"
        query += f"\nORDER BY {hierarchy_cols}"
        
        return query, params
    
    def build_comparison_query(
        self,
        indicator_id: str,
        filters: Dict[str, Any],
        compare_dimension: str = "annee"
    ) -> tuple[str, Dict[str, Any]]:
        """
        Construit une requête pour comparer des périodes
        Exemple: Comparer 2023 vs 2024
        """
        indicator_mapping = {
            'ca_total': 'SUM(montant_vente) as valeur',
            'quantite_vendue': 'SUM(quantite) as valeur',
        }
        
        indicator_expr = indicator_mapping.get(indicator_id, 'SUM(montant_vente) as valeur')
        
        compare_mapping = {
            'annee': "EXTRACT(YEAR FROM date_vente)",
            'mois': "TO_CHAR(date_vente, 'YYYY-MM')",
            'trimestre': "TO_CHAR(date_vente, 'YYYY-Q')"
        }
        
        compare_expr = compare_mapping.get(compare_dimension, "EXTRACT(YEAR FROM date_vente)")
        
        query = f"""
        SELECT 
            {compare_expr} as periode,
            {indicator_expr}
        FROM {self.base_table}
        WHERE date_vente BETWEEN :date_debut AND :date_fin
        GROUP BY {compare_expr}
        ORDER BY periode
        """
        
        params = {
            'date_debut': filters.get('date_debut'),
            'date_fin': filters.get('date_fin')
        }
        
        return query, params
