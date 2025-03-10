"""
Example script demonstrating how to use the translator programmatically.
"""

import argparse
import logging
import time
import sys
from translator import Translator
from utils import setup_logging

# Set up logging
setup_logging(log_level="INFO")
logger = logging.getLogger(__name__)

def translate_text(text, target_language, source_language="english"):
    """
    Translate text from source language to target language.
    
    Args:
        text (str): Text to translate
        target_language (str): Target language name
        source_language (str): Source language name (default: "english")
        
    Returns:
        str: Translated text
    """
    logger.info(f"Translating from {source_language} to {target_language}")
    
    # Initialize translator
    translator = Translator()
    
    # Measure translation time
    start_time = time.time()
    
    # Translate text
    if len(text) > 1000:  # Use large text method for longer texts
        translation = translator.translate_large_text(text, target_language, source_language)
    else:
        translation = translator.translate(text, target_language, source_language)
        
    elapsed_time = time.time() - start_time
    
    logger.info(f"Translation completed in {elapsed_time:.2f} seconds")
    
    return translation

def translate_file(file_path, target_language, source_language="english", output_file=None):
    """
    Translate text from a file.
    
    Args:
        file_path (str): Path to the file to translate
        target_language (str): Target language name
        source_language (str): Source language name (default: "english")
        output_file (str): Path to save the translated text (default: None)
        
    Returns:
        str: Translated text
    """
    logger.info(f"Translating file: {file_path}")
    
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        logger.info(f"File loaded: {len(text)} characters")
        
        # Translate text
        translation = translate_text(text, target_language, source_language)
        
        # Save translation if output file is specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translation)
            logger.info(f"Translation saved to: {output_file}")
            
        return translation
        
    except Exception as e:
        logger.error(f"Error translating file: {str(e)}")
        return None

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Translate text or files")
    parser.add_argument("--text", help="Text to translate")
    parser.add_argument("--file", help="File to translate")
    parser.add_argument("--target", choices=["hindi", "tamil", "malayalam", "telugu"], required=True,
                        help="Target language")
    parser.add_argument("--source", default="english", help="Source language (default: english)")
    parser.add_argument("--output", help="Output file for translation")
    
    args = parser.parse_args()
    
    if not args.text and not args.file:
        parser.error("Either --text or --file must be specified")
        
    if args.text:
        # Translate text
        translation = translate_text(args.text, args.target, args.source)
        
        # Print translation
        print("\nTranslation:")
        print("-" * 50)
        print(translation)
        print("-" * 50)
        
        # Save translation if output file is specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(translation)
            logger.info(f"Translation saved to: {args.output}")
            
    elif args.file:
        # Translate file
        translation = translate_file(args.file, args.target, args.source, args.output)
        
        if translation:
            # Print first 500 characters of translation
            print("\nTranslation (first 500 characters):")
            print("-" * 50)
            print(translation[:500] + ("..." if len(translation) > 500 else ""))
            print("-" * 50)

if __name__ == "__main__":
    main() 