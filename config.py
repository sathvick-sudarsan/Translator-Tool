"""
Configuration settings for the translation tool.
"""

import os
import torch

# Application settings
APP_NAME = "Multilingual Report Translator"
APP_VERSION = "1.0.0"
DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

# Model settings
MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_LENGTH = 1024
BATCH_SIZE = 8
CHUNK_SIZE = 500
OVERLAP = 50

# Supported languages
SUPPORTED_LANGUAGES = {
    "english": "en_XX",
    "hindi": "hi_IN",
    "tamil": "ta_IN",
    "malayalam": "ml_IN",
    "telugu": "te_IN"
}

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure directories exist
for directory in [TEMPLATES_DIR, STATIC_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(LOGS_DIR, "translator.log")

# API settings
API_TIMEOUT = 300  # seconds 