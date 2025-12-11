"""
Configuration module for EmilFlow.

This module centralizes all configuration, paths, and constants.
Demonstrates proper path handling using __file__ and pathlib.
"""

from pathlib import Path
from dotenv import load_dotenv,find_dotenv
import os

from google.oauth2.credentials import Credentials


# === PATH CONFIGURATION ===
# Using __file__ makes paths work regardless of where the script is run from
PACKAGE_DIR = Path(__file__).resolve().parent  # Directory where this file lives
PROJECT_ROOT = PACKAGE_DIR  # Eminder root
DATA_DIR = PROJECT_ROOT / 'data'  # Data directory in project root

# === APPLICATION SETTINGS ===
LOG_PREFIX = '[EmilFlow]'
DECIMAL_PLACES = 2

# .env finder
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


# === GOOGLE AUTH ===
GOOGLECRED = Credentials(
None,
refresh_token = os.getenv('refresh_token'),
token_uri = os.getenv('token_uri'),
client_id = os.getenv('client_id'),
client_secret = os.getenv('client_secret'),
scopes = [os.getenv('scopes')]
)


# === TEXT COLORS ===
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'