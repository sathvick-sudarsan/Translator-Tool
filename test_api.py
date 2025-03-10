"""
Script to test the Flask API endpoints.
"""

import requests
import json
import time
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_translate_endpoint(base_url, text, target_language):
    """
    Test the /translate endpoint.
    
    Args:
        base_url (str): Base URL of the API
        text (str): Text to translate
        target_language (str): Target language
        
    Returns:
        dict: API response
    """
    url = f"{base_url}/translate"
    
    payload = {
        "text": text,
        "target_language": target_language
    }
    
    logger.info(f"Testing /translate endpoint with target language: {target_language}")
    logger.info(f"Text: {text[:50]}..." if len(text) > 50 else f"Text: {text}")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload)
        elapsed_time = time.time() - start_time
        
        logger.info(f"Request completed in {elapsed_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Translation: {result['translation'][:100]}..." if len(result['translation']) > 100 else f"Translation: {result['translation']}")
            logger.info(f"Processing time: {result['processing_time']}")
            return result
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return None

def test_batch_translate_endpoint(base_url, texts, target_language):
    """
    Test the /batch_translate endpoint.
    
    Args:
        base_url (str): Base URL of the API
        texts (list): List of texts to translate
        target_language (str): Target language
        
    Returns:
        dict: API response
    """
    url = f"{base_url}/batch_translate"
    
    payload = {
        "texts": texts,
        "target_language": target_language
    }
    
    logger.info(f"Testing /batch_translate endpoint with target language: {target_language}")
    logger.info(f"Number of texts: {len(texts)}")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload)
        elapsed_time = time.time() - start_time
        
        logger.info(f"Request completed in {elapsed_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Number of translations: {result['count']}")
            logger.info(f"Processing time: {result['processing_time']}")
            
            # Print first translation
            if result['translations']:
                logger.info(f"First translation: {result['translations'][0]}")
                
            return result
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return None

def test_health_endpoint(base_url):
    """
    Test the /health endpoint.
    
    Args:
        base_url (str): Base URL of the API
        
    Returns:
        dict: API response
    """
    url = f"{base_url}/health"
    
    logger.info("Testing /health endpoint")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Health status: {result['status']}")
            return result
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Test the Flask API endpoints")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of the API")
    parser.add_argument("--endpoint", choices=["translate", "batch", "health", "all"], default="all",
                        help="Endpoint to test")
    parser.add_argument("--language", choices=["hindi", "tamil", "malayalam", "telugu"], default="hindi",
                        help="Target language for translation")
    
    args = parser.parse_args()
    
    # Test health endpoint
    if args.endpoint in ["health", "all"]:
        test_health_endpoint(args.url)
        print()
        
    # Test translate endpoint
    if args.endpoint in ["translate", "all"]:
        test_text = "Hello, how are you? This is a test of the translation API."
        test_translate_endpoint(args.url, test_text, args.language)
        print()
        
    # Test batch translate endpoint
    if args.endpoint in ["batch", "all"]:
        test_texts = [
            "Hello, how are you?",
            "This is the second sentence for testing.",
            "The weather is nice today.",
            "I hope the translation works well."
        ]
        test_batch_translate_endpoint(args.url, test_texts, args.language)

if __name__ == "__main__":
    main() 