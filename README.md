# Shona Translator

A high-accuracy English to Shona DOCX translation tool that preserves document formatting and structure.

## Features

- 🌍 **High-accuracy translation** using multiple translation services
- 📄 **Preserves DOCX formatting** (bold, italic, tables, etc.)
- 🔄 **Dual translation engine**: Google Translate + OpenAI (optional)
- 📊 **Table support** - translates content within tables
- 🎯 **Context-aware** translation with OpenAI integration
- ⚡ **Batch processing** ready

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

### Basic Translation

```bash
python shona_translator.py
```

This will translate `collection-tools.docx` to `collection-tools_shona.docx`.

### Custom Files

Edit the `input_file` and `output_file` variables in `main()` function or modify the script for command-line arguments.

## Translation Quality

The tool uses a dual-engine approach for maximum accuracy:

1. **Google Translate**: Primary translation service (no API key required)
2. **OpenAI GPT-4**: Context-aware translation (requires API key, optional)

When both services are available, the tool compares translations and selects the most contextually appropriate one.

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
