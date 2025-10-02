"""Configuration settings for Strategic Conquest game server."""

import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = True

    # Game settings
    DEFAULT_MAP_WIDTH = 30
    DEFAULT_MAP_HEIGHT = 20
    MAX_MAP_SIZE = 50

    # Save directory
    SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saves')

    # Ensure save directory exists
    os.makedirs(SAVE_DIR, exist_ok=True)
