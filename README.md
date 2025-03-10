# Multilingual Report Translator

A powerful translation tool that can translate large English reports into multiple Indian languages: Hindi, Tamil, Malayalam, and Telugu. This tool is designed for translating company reports, student assessments, and other large documents while maintaining privacy by running locally.

## Features

- **Multiple Language Support**: Translate English text to Hindi, Tamil, Malayalam, and Telugu
- **Large Document Handling**: Efficiently processes large reports by breaking them into manageable chunks
- **Privacy-Focused**: Uses locally running models to ensure data privacy
- **User-Friendly Interface**: Clean, modern web interface for easy translation
- **Batch Processing**: Translate multiple texts at once
- **File Upload**: Support for uploading text files for translation
- **Download & Copy**: Easy options to download or copy translated content

## Architecture

The application is built with the following components:

- **Translation Engine**: Uses Hugging Face's MBart-50 model for high-quality translations
- **Web Interface**: Flask-based web application with a responsive UI
- **API Endpoints**: RESTful API for programmatic access to translation services

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multilingual-report-translator.git
   cd multilingual-report-translator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Web Interface

1. Select the target language (Hindi, Tamil, Malayalam, or Telugu)
2. Enter or paste the English text you want to translate
3. Alternatively, upload a text file
4. Click the "Translate" button
5. View the translation result
6. Copy or download the translated text

### API Usage

The application provides RESTful API endpoints for programmatic access:

#### Translate a Single Text

```
POST /translate
Content-Type: application/json

{
  "text": "Your English text here",
  "target_language": "hindi"
}
```

Response:
```json
{
  "translation": "हिंदी में अनुवादित पाठ",
  "source_language": "english",
  "target_language": "hindi",
  "processing_time": "1.25 seconds"
}
```

#### Batch Translation

```
POST /batch_translate
Content-Type: application/json

{
  "texts": ["First text", "Second text"],
  "target_language": "tamil"
}
```

Response:
```json
{
  "translations": ["முதல் உரை", "இரண்டாவது உரை"],
  "source_language": "english",
  "target_language": "tamil",
  "count": 2,
  "processing_time": "2.34 seconds"
}
```

## Integration with Existing Systems

To integrate this translation tool with your company's website:

1. **API Integration**: Use the provided RESTful API endpoints to send text for translation and receive translated content
2. **Iframe Embedding**: Embed the web interface in an iframe on your website
3. **Direct Code Integration**: Import the `Translator` class from `translator.py` into your Python application

## Performance Considerations

- **GPU Acceleration**: The tool automatically uses GPU if available, significantly improving translation speed
- **Batch Processing**: For multiple texts, use the batch translation endpoint for better performance
- **Chunking**: Large texts are automatically split into chunks with overlap for better translation quality

## Privacy and Security

- All translations are performed locally, ensuring data privacy
- No data is sent to external services
- The application can be deployed within your organization's infrastructure

## Development

### Project Structure

```
multilingual-report-translator/
├── app.py                 # Flask web application
├── translator.py          # Core translation functionality
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── templates/             # HTML templates
│   └── index.html         # Main web interface
├── static/                # Static assets
├── logs/                  # Log files
└── README.md              # Documentation
```

### Extending the Tool

To add support for additional languages:

1. Check if the language is supported by the MBart-50 model
2. Add the language code to the `SUPPORTED_LANGUAGES` dictionary in `config.py`
3. Update the UI in `templates/index.html` to include the new language option

## Troubleshooting

### Common Issues

- **Model Loading Errors**: Ensure you have sufficient RAM/VRAM for the model
- **Slow Translation**: Consider using a GPU for faster processing
- **Out of Memory Errors**: Reduce batch size or chunk size in `config.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for the translation models
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components 