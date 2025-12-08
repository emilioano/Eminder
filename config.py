"""
Configuration module for EmilFlow.

This module centralizes all configuration, paths, and constants.
Demonstrates proper path handling using __file__ and pathlib.
"""

from pathlib import Path

# === PATH CONFIGURATION ===
# Using __file__ makes paths work regardless of where the script is run from
PACKAGE_DIR = Path(__file__).parent  # Directory where this file lives
PROJECT_ROOT = PACKAGE_DIR.parent.parent  # DataLab root
DATA_DIR = PROJECT_ROOT / 'data'  # Data directory in project root

# === APPLICATION SETTINGS ===
LOG_PREFIX = '[EmilFlow]'
DECIMAL_PLACES = 2
