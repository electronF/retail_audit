"""Paramètres globaux de l'application"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application
APP_CONFIG = {
    'host': os.getenv('APP_HOST', '0.0.0.0'),
    'port': int(os.getenv('APP_PORT', 8050)),
    'debug': os.getenv('DEBUG_MODE', 'True').lower() == 'true'
}

# Cache
CACHE_CONFIG = {
    'type': os.getenv('CACHE_TYPE', 'redis'),
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': int(os.getenv('REDIS_PORT', 6379)),
    'db': int(os.getenv('REDIS_DB', 0)),
    'timeout': int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
}

# Performance
PERFORMANCE_CONFIG = {
    'max_rows_per_query': int(os.getenv('MAX_ROWS_PER_QUERY', 100000)),
    'query_timeout': int(os.getenv('QUERY_TIMEOUT', 30))
}

# Export
EXPORT_CONFIG = {
    'folder': os.getenv('EXPORT_FOLDER', 'data/exports'),
    'max_rows': int(os.getenv('MAX_EXPORT_ROWS', 50000))
}
