"""
Module de gestion de connexion à la base de données
"""
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
import pandas as pd
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    """Gestionnaire de connexion à la base de données"""
    
    def __init__(self):
        self.engine = None
        self._connect()
    
    def _connect(self):
        """Établit la connexion à la BD"""
        db_type = os.getenv('DB_TYPE', 'postgresql')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME')
        
        connection_string = (
            f"{db_type}://{db_user}:{db_password}@"
            f"{db_host}:{db_port}/{db_name}"
        )
        
        self.engine = create_engine(
            connection_string,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True  # Vérifie la connexion avant utilisation
        )
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Exécute une requête SQL et retourne un DataFrame
        
        Args:
            query: Requête SQL à exécuter
            params: Paramètres pour la requête préparée
            
        Returns:
            DataFrame pandas avec les résultats
        """
        try:
            with self.engine.connect() as connection:
                result = pd.read_sql_query(
                    text(query), 
                    connection, 
                    params=params
                )
                return result
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            raise
    
    def execute_query_chunked(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None,
        chunksize: int = 10000
    ):
        """
        Exécute une requête et retourne les résultats par chunks
        Utile pour les grandes quantités de données
        """
        try:
            with self.engine.connect() as connection:
                for chunk in pd.read_sql_query(
                    text(query), 
                    connection, 
                    params=params,
                    chunksize=chunksize
                ):
                    yield chunk
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Teste la connexion à la BD"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Échec du test de connexion: {e}")
            return False
    
    def close(self):
        """Ferme la connexion"""
        if self.engine:
            self.engine.dispose()


# Singleton pour une seule instance de connexion
_db_connection = None

def get_db_connection() -> DatabaseConnection:
    """Retourne l'instance unique de connexion BD"""
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection
