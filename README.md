# Shona Translator

A high-accuracy English to Shona DOCX translation tool that preserves document formatting and structure.

## Quick Start

### Setup (one-time)

```bash
# Install Python packages
pip install -r requirements.txt

# Or use the setup script
python setup.py
```

### Run Translator

```bash
# Translate a document (uses MyMemory by default)
python shona_translate.py your_document.docx

# Translate with Agent (requires API key in .env file)
python shona_translate.py your_document.docx --method agent

# Translate with Google Translate
python shona_translate.py your_document.docx --method google

# Translate with MyMemory (free https://translated.com service)
python shona_translate.py your_document.docx --method mymemory

# See all available methods
python shona_translate.py --list-methods
```

### Optional: Add OpenAI API Key

```bash
# Create .env file and add your OpenAI API key for better translations
echo "OPENAI_API_KEY=your_key_here" > .env
```

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

## File Format Support

- **DOCX**: Microsoft Word documents
- **PDF**: Portable Document Format
- **TXT**: Plain text files
- **HTML**: Hypertext Markup Language
- **RTF**: Rich Text Format
- **ODT**: OpenDocument Text
- **ODS**: OpenDocument Spreadsheet
- **ODP**: OpenDocument Presentation
- **ODG**: OpenDocument Graphics
- **ODF**: OpenDocument Formula

## Language Support

- **Source**: English
- **Target**: Shona (Bantu language spoken in Zimbabwe)

# FAQ

## How to avoid cache issues?

Delete the translation_cache.json file.
