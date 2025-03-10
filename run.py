"""
Script to run the translation application.
"""

import os
import argparse
import logging
from app import app
from utils import setup_logging, check_gpu_availability
import config

# Set up logging
setup_logging(
    log_level=config.LOG_LEVEL,
    log_format=config.LOG_FORMAT,
    log_file=config.LOG_FILE
)
logger = logging.getLogger(__name__)

def main():
    """Run the translation application"""
    parser = argparse.ArgumentParser(description="Run the translation application")
    parser.add_argument("--host", default=config.HOST, help="Host to run the server on")
    parser.add_argument("--port", type=int, default=config.PORT, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", default=config.DEBUG, help="Run in debug mode")
    
    args = parser.parse_args()
    
    # Check GPU availability
    gpu_info = check_gpu_availability()
    if gpu_info['available']:
        logger.info(f"GPU available: {gpu_info['device_name']}")
    else:
        logger.info("GPU not available, using CPU. Translation will be slower.")
    
    # Ensure directories exist
    for directory in [config.TEMPLATES_DIR, config.STATIC_DIR, config.LOGS_DIR]:
        os.makedirs(directory, exist_ok=True)
    
    # Print application info
    logger.info(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    logger.info(f"Server running at http://{args.host}:{args.port}")
    
    # Run the Flask app
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )

if __name__ == "__main__":
    main() 