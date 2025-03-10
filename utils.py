"""
Utility functions for the translation tool.
"""

import os
import re
import logging
import time
from functools import wraps
import torch

logger = logging.getLogger(__name__)

def setup_logging(log_level="INFO", log_format=None, log_file=None):
    """
    Set up logging configuration.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format (str): Log message format
        log_file (str): Path to log file
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
    # Convert string log level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    
    # Configure logging
    logging_config = {
        'level': numeric_level,
        'format': log_format
    }
    
    # Add file handler if log file is specified
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        logging_config['filename'] = log_file
        
    logging.basicConfig(**logging_config)
    logger.info(f"Logging configured with level {log_level}")

def timer(func):
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to be timed
        
    Returns:
        Wrapped function with timing
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"Function {func.__name__} executed in {elapsed_time:.2f} seconds")
        return result
    return wrapper

def check_gpu_availability():
    """
    Check if GPU is available and return device information.
    
    Returns:
        dict: GPU information
    """
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        current_device = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(current_device)
        
        info = {
            'available': True,
            'count': gpu_count,
            'current_device': current_device,
            'device_name': device_name,
            'device': 'cuda'
        }
        
        logger.info(f"GPU available: {device_name}")
    else:
        info = {
            'available': False,
            'device': 'cpu'
        }
        logger.info("GPU not available, using CPU")
        
    return info

def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """
    Split a large text into chunks with overlap.
    
    Args:
        text (str): Text to split
        chunk_size (int): Maximum size of each chunk
        overlap (int): Number of characters to overlap between chunks
        
    Returns:
        list: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
        
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk:  # Ensure we don't add empty chunks
            chunks.append(chunk)
            
    logger.debug(f"Split text into {len(chunks)} chunks")
    return chunks

def clean_text(text):
    """
    Clean text by removing extra whitespace and normalizing line breaks.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return text
        
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize line breaks
    text = re.sub(r'\n+', '\n', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def format_translation_result(translation, source_language, target_language, processing_time):
    """
    Format translation result for API response.
    
    Args:
        translation (str): Translated text
        source_language (str): Source language
        target_language (str): Target language
        processing_time (float): Processing time in seconds
        
    Returns:
        dict: Formatted result
    """
    return {
        'translation': translation,
        'source_language': source_language,
        'target_language': target_language,
        'processing_time': f"{processing_time:.2f} seconds"
    }

def get_memory_usage():
    """
    Get current memory usage information.
    
    Returns:
        dict: Memory usage information
    """
    if torch.cuda.is_available():
        # Get GPU memory usage
        allocated = torch.cuda.memory_allocated() / (1024 ** 3)  # GB
        reserved = torch.cuda.memory_reserved() / (1024 ** 3)    # GB
        
        memory_info = {
            'gpu_allocated_gb': allocated,
            'gpu_reserved_gb': reserved
        }
    else:
        memory_info = {
            'gpu_allocated_gb': 0,
            'gpu_reserved_gb': 0
        }
        
    return memory_info 