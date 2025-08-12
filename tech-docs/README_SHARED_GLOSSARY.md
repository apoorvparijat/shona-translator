# Shared Glossary System for Shona Translators

This document describes the new shared glossary system that provides deterministic terms and abbreviations across all three translators.

## Overview

The shared glossary system consists of:

1. **GlossaryManager** (`glossary_manager.py`) - Core component that loads and manages glossary data from CSV files
2. **BaseShonaTranslator** (`base_translator.py`) - Base class that all translators inherit from
3. **CSV Files** - Configuration files stored in the `glossary/` directory

## Architecture

```
translators/
├── glossary_manager.py          # Shared glossary management
├── base_translator.py           # Base translator class
├── mymemory_translator.py       # MyMemory API translator
├── google_translator.py         # Google Translate translator
├── openai_translator.py         # OpenAI GPT translator
├── test_shared_glossary.py      # Test suite
├── glossary/                    # CSV configuration files
│   ├── medical_technical_terms.csv
│   ├── phrase_translations.csv
│   ├── abbreviations.csv
│   └── post_processing_corrections.csv
└── README_SHARED_GLOSSARY.md    # This file
```

## CSV File Structure

### 1. Medical/Technical Terms (`medical_technical_terms.csv`)

```csv
english,shona,category
version,shanduko,document
healthcare,hutano,medical
patient,murwere,medical
artificial intelligence,huchenjeri hwekugadzira,technology
```

### 2. Phrase Translations (`phrase_translations.csv`)

```csv
english,shona,category
what is your name,zita rako ndiani,conversation
clinical decision support system,hurongwa hwekutsigira sarudzo dzekiriniki,medical
```

### 3. Abbreviations (`abbreviations.csv`)

```csv
abbreviation,expansion,category
HCW,healthcare worker,medical
CDS,clinical decision support,medical
AI,artificial intelligence,technology
NICU,neonatal intensive care unit,medical
```

### 4. Post-Processing Corrections (`post_processing_corrections.csv`)

```csv
pattern,replacement,description
\bmhando\b,shanduko,Fix version translation
\bmanzwiro\b,pfungwa,Better word for feelings/thoughts
\bkuongorora\b,kuongororwa,Standardize examination
```

## Translation Flow

All translators now follow this consistent flow:

1. **Glossary First** - Check for exact matches in phrase translations and medical/technical terms
2. **Abbreviation Expansion** - Expand abbreviations (HCW → healthcare worker)
3. **API Translation** - Use the specific API (MyMemory, Google, or OpenAI)
4. **Post-Processing** - Apply corrections to fix common errors
5. **Formatting Preservation** - Maintain document formatting

## Usage

### Basic Usage

```python
from mymemory_translator import MyMemoryShonaTranslator
from google_translator import GoogleShonaTranslator
from openai_translator import OpenAIShonaTranslator

# All translators use the same shared glossary
mymemory = MyMemoryShonaTranslator()
google = GoogleShonaTranslator()
openai = OpenAIShonaTranslator()

# Translate documents
mymemory.translate_docx("input.docx", "output_mymemory.docx")
google.translate_docx("input.docx", "output_google.docx")
openai.translate_docx("input.docx", "output_openai.docx")
```

### Custom Glossary Directory

```python
# Use a custom glossary directory
translator = MyMemoryShonaTranslator(glossary_dir="my_custom_glossary")
```

### Getting Translator Information

```python
info = translator.get_translator_info()
print(f"Type: {info['translator_type']}")
print(f"Rate limit delay: {info['rate_limit_delay']}s")
print(f"Glossary stats: {info['glossary_stats']}")
```

## Adding New Terms

### Method 1: Edit CSV Files Directly

1. Navigate to the `glossary/` directory
2. Edit the appropriate CSV file
3. Add new rows following the existing format
4. Restart your translator

### Method 2: Programmatic Addition

```python
from glossary_manager import GlossaryManager

glossary = GlossaryManager()

# Add a new medical term
glossary.medical_technical_glossary["new_term"] = "new_shona_translation"

# Add a new abbreviation
glossary.abbreviations["NEW"] = "new expansion"
```

## Testing

Run the test suite to verify everything works:

```bash
cd translators
python test_shared_glossary.py
```

This will test:

- CSV file creation and loading
- Glossary manager functionality
- All three translators with shared glossary
- Translation consistency across translators

## Benefits

1. **Consistency** - All translators use the same deterministic terms
2. **Maintainability** - Single source of truth for glossary data
3. **Extensibility** - Easy to add new terms via CSV files
4. **Quality** - Glossary-first approach ensures domain accuracy
5. **Flexibility** - Each translator can still use its own API while sharing common logic

## Migration from Old System

The old translators had hardcoded glossaries. The new system:

- ✅ Extracts all glossary data to CSV files
- ✅ Provides shared preprocessing and post-processing
- ✅ Maintains the same API for existing code
- ✅ Adds new features like translator info and statistics

## Troubleshooting

### CSV Files Not Created

- Ensure the `glossary/` directory is writable
- Check that the GlossaryManager can create files

### Import Errors

- Make sure all required dependencies are installed
- Check that `glossary_manager.py` and `base_translator.py` are in the same directory

### Translation Issues

- Verify CSV files are properly formatted
- Check that terms are in lowercase in the CSV files
- Ensure abbreviations are in uppercase

### Rate Limiting

- Each translator has its own rate limit delay
- MyMemory: 0.1s, Google: 0.2s, OpenAI: 0.5s
- Adjust delays in the `_get_rate_limit_delay()` method if needed
