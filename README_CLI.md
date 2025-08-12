# Shona Translator CLI

A command-line interface for translating English DOCX documents to Shona using multiple translation services.

## Features

- **Multiple Translation Services**: MyMemory (free), Google Translate (free), OpenAI GPT (paid)
- **Shared Glossary System**: Consistent deterministic terms across all translators
- **Flexible Output**: Single or multiple translation methods
- **File Validation**: Ensures input files exist and are DOCX format
- **Progress Tracking**: Real-time translation progress and statistics

## Installation

1. Ensure you have the required dependencies:

   ```bash
   pip install python-docx python-dotenv requests
   ```

2. For Google Translate (required for Google method):

   ```bash
   pip install googletrans==4.0.0-rc1
   ```

   **Note**: If you encounter dependency conflicts, run:

   ```bash
   python fix_googletrans.py
   ```

3. For OpenAI (optional):
   ```bash
   pip install openai
   ```

## Usage

### Basic Usage

```bash
# Translate using default method (MyMemory)
python shona_translate.py document.docx

# Translate using specific method
python shona_translate.py document.docx --method google

# Translate using multiple methods
python shona_translate.py document.docx --method google,openai,mymemory
```

### Command Options

```bash
python shona_translate.py [input_file] [options]

Options:
  -h, --help            Show help message
  --method METHOD, -m METHOD
                        Translation method(s). Use comma-separated list for multiple methods.
                        Default: mymemory. Available: mymemory, google, openai
  --output OUTPUT, -o OUTPUT
                        Output file path (only used with single method)
  --list-methods        List available translation methods and exit
  --verbose, -v         Enable verbose logging
```

### Examples

```bash
# List available methods
python shona_translate.py --list-methods

# Translate with MyMemory (default)
python shona_translate.py my_document.docx

# Translate with Google Translate
python shona_translate.py my_document.docx --method google

# Translate with OpenAI
python shona_translate.py my_document.docx --method openai

# Translate with multiple methods
python shona_translate.py my_document.docx --method google,openai,mymemory

# Specify custom output file (single method only)
python shona_translate.py my_document.docx --method openai --output custom_output.docx

# Enable verbose logging
python shona_translate.py my_document.docx --method google --verbose
```

## Translation Methods

### 1. MyMemory (Default)

- **Cost**: Free
- **Speed**: Fast
- **Quality**: Good for general text
- **Rate Limit**: 0.1s delay between requests

### 2. Google Translate

- **Cost**: Free
- **Speed**: Fast
- **Quality**: Good for general text
- **Rate Limit**: 0.2s delay between requests
- **Fallback**: Uses requests-based API if googletrans library fails

### 3. OpenAI GPT

- **Cost**: Paid (requires OPENAI_API_KEY)
- **Speed**: Slower due to API rate limits
- **Quality**: Highest quality, context-aware
- **Rate Limit**: 0.5s delay between requests

## Output Files

When using multiple methods, output files are automatically named:

- `document_shona_mymemory.docx`
- `document_shona_google.docx`
- `document_shona_openai.docx`

## Environment Variables

For OpenAI translation, set your API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

## Shared Glossary System

All translators use the same shared glossary system for consistent terminology:

- **Medical/Technical Terms**: 65+ domain-specific terms
- **Phrase Translations**: 9+ common phrases
- **Abbreviations**: 10+ abbreviations (HCW, CDS, AI, NICU, etc.)
- **Post-Processing**: 6+ error corrections
- **Exclusion List**: 20+ terms that should not be translated (brand names, proper nouns, etc.)

Glossary files are stored in `translators/glossary/` and can be edited directly.

### Exclusion List

The exclusion list prevents certain terms from being translated by the glossary system, including:

- **Brand names**: Neotree, Neotree's
- **Hospital names**: Sally Mugabe Central Hospital, Chinhoyi Provincial Hospital, etc.
- **Technical abbreviations**: CDS, AI, NICU, NNU, DHIS2, EMRs, MoH
- **Specific terms**: "Healthcare Systems Usability Scale for Clinical Decision Support Systems", "gut feeling", "Aim 2", etc.

**Note**: The exclusion list only prevents glossary-based translation. API-based translation (Google Translate, OpenAI) may still translate these terms if the API service chooses to do so.

To add new exclusions, edit `translators/glossary/exclusion_list.csv`:

```csv
term,reason
new_term,Reason for exclusion
```

## Error Handling

The CLI provides clear error messages for common issues:

- **File not found**: `❌ Error: Input file 'file.docx' does not exist`
- **Invalid file type**: `❌ Error: Input file 'file.txt' is not a DOCX file`
- **Invalid method**: `❌ Error: Invalid translation method(s): invalid`
- **Missing API key**: `❌ Failed to initialize OpenAI translator: OPENAI_API_KEY environment variable not set`

## Exit Codes

- `0`: Success
- `1`: Error (file not found, invalid method, etc.)
- `2`: All translations failed (when using multiple methods)

## Architecture

```
shona-translator/
├── shona_translate.py          # CLI tool (this file)
├── translators/                # Translation modules
│   ├── glossary_manager.py     # Shared glossary system
│   ├── base_translator.py      # Base translator class
│   ├── mymemory_translator.py  # MyMemory API translator
│   ├── google_translator.py    # Google Translate translator
│   ├── openai_translator.py    # OpenAI GPT translator
│   └── glossary/               # CSV configuration files
└── README_CLI.md              # This file
```

## Troubleshooting

### Import Errors

- Ensure you're running from the project root directory
- Check that all required dependencies are installed
- For Google Translate conflicts, run `python fix_googletrans.py`

### Translation Failures

- For OpenAI: Verify OPENAI_API_KEY is set
- For Google: Check internet connection
- For MyMemory: Check internet connection

### Rate Limiting

- Each translator has built-in rate limiting
- Increase delays in translator code if needed

### File Permissions

- Ensure the current directory is writable for output files
- Check that input files are readable
