"""
Configuration module for EmilFlow.

This module centralizes all configuration, paths, and constants.
Demonstrates proper path handling using __file__ and pathlib.
"""

from pathlib import Path
from dotenv import load_dotenv,find_dotenv
import os








# === PATH CONFIGURATION ===
# Using __file__ makes paths work regardless of where the script is run from
PACKAGE_DIR = Path(__file__).resolve().parent  # Directory where this file lives
PROJECT_ROOT = PACKAGE_DIR  # Eminder root
DATA_DIR = PROJECT_ROOT / 'data'  # Data directory in project root

# === APPLICATION SETTINGS ===
LOG_PREFIX = '[EmilFlow]'
DECIMAL_PLACES = 2


env_path = find_dotenv(usecwd=True)
if not env_path:
    #Fallback:
    env_path = PROJECT_ROOT / ".env"
    
load_dotenv(dotenv_path=env_path, override=False)

# === DB-Config ===
DBCONFIG = {
'host': os.getenv('DB_HOST'),
'user': os.getenv('DB_USER'),
'password': os.getenv('DB_PASS'),
'database': os.getenv('DB_NAME')
}