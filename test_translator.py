"""
Test script for the translator functionality.
"""

import argparse
import logging
import time
from translator import Translator
from utils import setup_logging, check_gpu_availability

# Set up logging
setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)

def test_basic_translation():
    """Test basic translation functionality for all supported languages"""
    logger.info("Testing basic translation functionality")
    
    # Check GPU availability
    gpu_info = check_gpu_availability()
    logger.info(f"Using device: {gpu_info['device']}")
    
    # Initialize translator
    translator = Translator()
    
    # Test text
    test_text = "Hello, how are you? This is a test of the translation system."
    
    # Test translation for each supported language
    for language in ["hindi", "tamil", "malayalam", "telugu"]:
        logger.info(f"Testing translation to {language}")
        
        start_time = time.time()
        translation = translator.translate(test_text, language)
        elapsed_time = time.time() - start_time
        
        logger.info(f"Translation to {language} completed in {elapsed_time:.2f} seconds")
        logger.info(f"Original: {test_text}")
        logger.info(f"Translated ({language}): {translation}")
        logger.info("-" * 50)

def test_large_text_translation(target_language="hindi"):
    """Test translation of a larger text"""
    logger.info(f"Testing large text translation to {target_language}")
    
    # Initialize translator
    translator = Translator()
    
    # Generate a larger test text (repeated sentences)
    base_text = "This is a test of the translation system for large documents. "
    large_text = base_text * 20
    
    logger.info(f"Large text length: {len(large_text)} characters")
    
    # Translate using the large text method
    start_time = time.time()
    translation = translator.translate_large_text(
        large_text, 
        target_language,
        chunk_size=200,  # Smaller chunk size for testing
        overlap=20
    )
    elapsed_time = time.time() - start_time
    
    logger.info(f"Large text translation completed in {elapsed_time:.2f} seconds")
    logger.info(f"Translation length: {len(translation)} characters")
    logger.info(f"First 100 characters: {translation[:100]}...")

def test_batch_translation(target_language="tamil"):
    """Test batch translation functionality"""
    logger.info(f"Testing batch translation to {target_language}")
    
    # Initialize translator
    translator = Translator()
    
    # Create a batch of test texts
    test_texts = [
        "Hello, how are you?",
        "This is the second sentence for testing.",
        "The weather is nice today.",
        "I hope the translation works well."
    ]
    
    logger.info(f"Translating batch of {len(test_texts)} texts")
    
    # Translate batch
    start_time = time.time()
    translations = translator.translate(test_texts, target_language)
    elapsed_time = time.time() - start_time
    
    logger.info(f"Batch translation completed in {elapsed_time:.2f} seconds")
    
    # Print results
    for i, (original, translated) in enumerate(zip(test_texts, translations)):
        logger.info(f"Text {i+1}:")
        logger.info(f"Original: {original}")
        logger.info(f"Translated: {translated}")
        logger.info("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the translator functionality")
    parser.add_argument("--test", choices=["basic", "large", "batch", "all"], default="basic",
                        help="Test type to run (basic, large, batch, or all)")
    parser.add_argument("--language", choices=["hindi", "tamil", "malayalam", "telugu"], default="hindi",
                        help="Target language for testing")
    
    args = parser.parse_args()
    
    if args.test == "basic" or args.test == "all":
        test_basic_translation()
        
    if args.test == "large" or args.test == "all":
        test_large_text_translation(args.language)
        
    if args.test == "batch" or args.test == "all":
        test_batch_translation(args.language) 