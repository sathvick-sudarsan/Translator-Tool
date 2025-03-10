import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import time
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Translator:
    """
    A class to handle translation between English and Indian languages.
    Uses the MBart-50 model which supports multiple Indian languages.
    """
    
    def __init__(self, model_name="facebook/mbart-large-50-many-to-many-mmt", device=None):
        """
        Initialize the translator with the specified model.
        
        Args:
            model_name (str): The name of the model to use for translation
            device (str, optional): Device to run the model on ('cuda' or 'cpu')
        """
        self.model_name = model_name
        
        # Determine device (use GPU if available)
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Using device: {self.device}")
        
        # Load model and tokenizer
        logger.info(f"Loading model: {model_name}")
        self.model = None
        self.tokenizer = None
        self.load_model()
        
        # Language code mapping
        self.language_codes = {
            "english": "en_XX",
            "hindi": "hi_IN",
            "tamil": "ta_IN",
            "malayalam": "ml_IN",
            "telugu": "te_IN"
        }
        
    def load_model(self):
        """Load the translation model and tokenizer"""
        try:
            start_time = time.time()
            self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.tokenizer = MBart50TokenizerFast.from_pretrained(self.model_name)
            logger.info(f"Model loaded in {time.time() - start_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def translate(self, text, target_language, source_language="english", batch_size=8, max_length=1024):
        """
        Translate text from source language to target language.
        
        Args:
            text (str or list): Text or list of texts to translate
            target_language (str): Target language name (e.g., "hindi", "tamil")
            source_language (str): Source language name (default: "english")
            batch_size (int): Batch size for processing long texts
            max_length (int): Maximum length of input sequence
            
        Returns:
            str or list: Translated text(s)
        """
        if not self.model or not self.tokenizer:
            logger.error("Model or tokenizer not loaded")
            return None
            
        # Validate languages
        if source_language not in self.language_codes:
            raise ValueError(f"Source language '{source_language}' not supported")
        if target_language not in self.language_codes:
            raise ValueError(f"Target language '{target_language}' not supported")
            
        source_code = self.language_codes[source_language]
        target_code = self.language_codes[target_language]
        
        # Set the source language
        self.tokenizer.src_lang = source_code
        
        # Handle single text or list of texts
        if isinstance(text, str):
            return self._translate_text(text, target_code, max_length)
        elif isinstance(text, list):
            return self._translate_batch(text, target_code, batch_size, max_length)
        else:
            raise TypeError("Text must be a string or a list of strings")
    
    def _translate_text(self, text, target_code, max_length):
        """Translate a single text"""
        try:
            # Tokenize the text
            encoded = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
            encoded = {k: v.to(self.device) for k, v in encoded.items()}
            
            # Generate translation
            with torch.no_grad():
                generated_tokens = self.model.generate(
                    **encoded,
                    forced_bos_token_id=self.tokenizer.lang_code_to_id[target_code],
                    max_length=max_length
                )
                
            # Decode the generated tokens
            translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            return translation
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return None
    
    def _translate_batch(self, texts, target_code, batch_size, max_length):
        """Translate a batch of texts"""
        translations = []
        
        # Process in batches
        for i in tqdm(range(0, len(texts), batch_size), desc="Translating batches"):
            batch_texts = texts[i:i+batch_size]
            
            try:
                # Tokenize the batch
                encoded = self.tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
                encoded = {k: v.to(self.device) for k, v in encoded.items()}
                
                # Generate translations
                with torch.no_grad():
                    generated_tokens = self.model.generate(
                        **encoded,
                        forced_bos_token_id=self.tokenizer.lang_code_to_id[target_code],
                        max_length=max_length
                    )
                    
                # Decode the generated tokens
                batch_translations = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
                translations.extend(batch_translations)
                
            except Exception as e:
                logger.error(f"Batch translation error: {str(e)}")
                # Add None for each failed translation in this batch
                translations.extend([None] * len(batch_texts))
                
        return translations
    
    def translate_large_text(self, text, target_language, source_language="english", 
                            chunk_size=500, overlap=50, max_length=1024):
        """
        Translate large text by breaking it into chunks with overlap.
        
        Args:
            text (str): Large text to translate
            target_language (str): Target language name
            source_language (str): Source language name (default: "english")
            chunk_size (int): Number of characters per chunk
            overlap (int): Number of overlapping characters between chunks
            max_length (int): Maximum length for the model
            
        Returns:
            str: Translated text
        """
        if len(text) <= chunk_size:
            return self.translate(text, target_language, source_language, max_length=max_length)
        
        # Split text into chunks with overlap
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk:  # Ensure we don't add empty chunks
                chunks.append(chunk)
        
        logger.info(f"Split large text into {len(chunks)} chunks")
        
        # Translate each chunk
        translated_chunks = self.translate(chunks, target_language, source_language, max_length=max_length)
        
        # Combine translated chunks (simple concatenation for now)
        # Note: A more sophisticated approach might be needed for better results
        combined_translation = " ".join(translated_chunks)
        
        return combined_translation

# Example usage
if __name__ == "__main__":
    # Initialize translator
    translator = Translator()
    
    # Example text
    english_text = "Hello, how are you? This is a test of the translation system."
    
    # Translate to Hindi
    hindi_translation = translator.translate(english_text, "hindi")
    print(f"Hindi: {hindi_translation}")
    
    # Translate to Tamil
    tamil_translation = translator.translate(english_text, "tamil")
    print(f"Tamil: {tamil_translation}")
    
    # Translate to Malayalam
    malayalam_translation = translator.translate(english_text, "malayalam")
    print(f"Malayalam: {malayalam_translation}")
    
    # Translate to Telugu
    telugu_translation = translator.translate(english_text, "telugu")
    print(f"Telugu: {telugu_translation}")
