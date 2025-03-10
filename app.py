from flask import Flask, render_template, request, jsonify
import os
import logging
from translator import Translator
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize translator (lazy loading - will be initialized on first use)
translator = None

def get_translator():
    """Get or initialize the translator"""
    global translator
    if translator is None:
        logger.info("Initializing translator...")
        translator = Translator()
    return translator

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """API endpoint for translation"""
    try:
        # Get request data
        data = request.json
        text = data.get('text', '')
        target_language = data.get('target_language', '').lower()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        if not target_language:
            return jsonify({'error': 'No target language provided'}), 400
            
        # Validate target language
        valid_languages = ['hindi', 'tamil', 'malayalam', 'telugu']
        if target_language not in valid_languages:
            return jsonify({'error': f'Invalid target language. Choose from: {", ".join(valid_languages)}'}), 400
        
        # Get translator
        trans = get_translator()
        
        # Measure translation time
        start_time = time.time()
        
        # Translate text
        if len(text) > 1000:  # Use large text method for longer texts
            translation = trans.translate_large_text(text, target_language)
        else:
            translation = trans.translate(text, target_language)
            
        elapsed_time = time.time() - start_time
        
        # Return translation
        return jsonify({
            'translation': translation,
            'source_language': 'english',
            'target_language': target_language,
            'processing_time': f"{elapsed_time:.2f} seconds"
        })
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/batch_translate', methods=['POST'])
def batch_translate():
    """API endpoint for batch translation"""
    try:
        # Get request data
        data = request.json
        texts = data.get('texts', [])
        target_language = data.get('target_language', '').lower()
        
        if not texts:
            return jsonify({'error': 'No texts provided'}), 400
            
        if not target_language:
            return jsonify({'error': 'No target language provided'}), 400
            
        # Validate target language
        valid_languages = ['hindi', 'tamil', 'malayalam', 'telugu']
        if target_language not in valid_languages:
            return jsonify({'error': f'Invalid target language. Choose from: {", ".join(valid_languages)}'}), 400
        
        # Get translator
        trans = get_translator()
        
        # Measure translation time
        start_time = time.time()
        
        # Translate texts
        translations = trans.translate(texts, target_language)
        
        elapsed_time = time.time() - start_time
        
        # Return translations
        return jsonify({
            'translations': translations,
            'source_language': 'english',
            'target_language': target_language,
            'count': len(translations),
            'processing_time': f"{elapsed_time:.2f} seconds"
        })
        
    except Exception as e:
        logger.error(f"Batch translation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True) 