# Shona Translator

A high-accuracy English to Shona DOCX translation tool that preserves document formatting and structure.

## Features

- 🌍 **Multiple translation services**: MyMemory (free), Google Translate (free), OpenAI GPT (paid)
- 📄 **Preserves DOCX formatting** (bold, italic, tables, etc.)
- 🔧 **Shared glossary system** with consistent terminology
- 🚫 **Exclusion list** for brand names, proper nouns, and specific terms
- 📊 **Table support** - translates content within tables
- 🎯 **Context-aware** translation with OpenAI integration
- ⚡ **Command-line interface** for easy usage

## Installation

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Set up OpenAI API for enhanced translation:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Command Line Interface

```bash
# Translate using default method (MyMemory)
python shona_translate.py document.docx

# Translate using specific method
python shona_translate.py document.docx --method google

# Translate using multiple methods
python shona_translate.py document.docx --method google,openai,mymemory

# List available methods
python shona_translate.py --list-methods
```

For detailed CLI usage, see [README_CLI.md](README_CLI.md).

### Programmatic Usage

```python
from translators.mymemory_translator import MyMemoryShonaTranslator

translator = MyMemoryShonaTranslator()
success = translator.translate_docx("input.docx", "output.docx")
```

## Translation Quality

The tool uses a multi-engine approach with shared glossary for maximum accuracy:

1. **MyMemory**: Free translation service (default)
2. **Google Translate**: Fast and reliable (free)
3. **OpenAI GPT**: Highest quality, context-aware (paid)

All translators use the same shared glossary system for consistent terminology and include an exclusion list for terms that should not be translated.

## Supported Features

- ✅ Paragraphs with formatting (bold, italic, underline)
- ✅ Tables with cell content
- ✅ Font preservation
- ✅ Document structure
- ⚠️ Images (preserved but captions not translated)
- ⚠️ Headers/footers (basic support)

## Language Support

- **Source**: English
- **Target**: Shona (Bantu language spoken in Zimbabwe)

## Performance

- Small documents (< 10 pages): ~2-5 minutes
- Medium documents (10-50 pages): ~10-30 minutes
- Large documents (> 50 pages): ~30+ minutes

Translation speed depends on document complexity and API response times.

## Troubleshooting

### Common Issues

1. **Rate limiting**: The tool includes automatic delays to prevent rate limiting
2. **API errors**: Check your internet connection and API keys
3. **Formatting issues**: Some complex formatting might be simplified

### Logs

The tool provides detailed logging. Check console output for translation progress and any errors.

## Contributing

Feel free to improve the translation quality by:

- Adding more translation services
- Improving formatting preservation
- Adding support for more document elements
