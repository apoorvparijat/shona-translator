# Agent Translator

The Agent Translator is a new translation method that uses OpenAI with a custom system prompt to provide intelligent English-to-Shona translation with built-in exclusions and glossary usage.

## Features

- **OpenAI Integration**: Uses GPT-3.5-turbo for high-quality translations
- **Smart Caching**: Automatically caches translations for faster subsequent requests
- **Exclusion List**: Respects terms from `exclusion_list.csv` that should not be translated
- **Glossary Integration**: Uses `abbreviations.csv` and `medical_technical_terms.csv` for consistent terminology
- **Professional Tone**: Maintains formal academic/medical context appropriate for documents

## How to Use

### Via CLI

```bash
# Basic usage with agent translator
python shona_translate.py document.docx --method agent

# Specify custom output file
python shona_translate.py document.docx --method agent --output my_translation.docx

# Use with other methods for comparison
python shona_translate.py document.docx --method agent,openai,google

# Enable verbose logging
python shona_translate.py document.docx --method agent --verbose
```

### Via Python

```python
from translators.agent_translator import AgentShonaTranslator

# Initialize translator
translator = AgentShonaTranslator()

# Translate text
translation = translator.get_best_translation("Hello, how are you?")
print(translation)

# Translate DOCX file
success = translator.translate_docx("input.docx", "output.docx")
```

## Configuration

### Environment Variables

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-openai-api-key-here
```

### Glossary Files

The Agent Translator automatically loads and uses these glossary files:

- `glossary/exclusion_list.csv` - Terms that should NOT be translated
- `glossary/abbreviations.csv` - Abbreviations and their expansions
- `glossary/medical_technical_terms.csv` - Medical and technical terms

## Caching

The Agent Translator automatically uses the smart caching system:

- **Cache Hits**: Subsequent translations of the same text are served from cache (much faster)
- **Provider-Specific**: Cache entries are tagged with "agent" provider name
- **Persistence**: Cache is saved to `translation_cache.json` and persists between runs
- **Confidence**: API translations are cached with 0.8 confidence, glossary with 1.0

### Cache Performance

You can test caching performance:

```bash
python test_agent_caching.py
```

This will show:

- First translation time (API call)
- Second translation time (cache hit)
- Speed improvement ratio
- Cache statistics

## System Prompt

The Agent Translator generates a custom system prompt that includes:

1. **Exclusion List**: All terms from `exclusion_list.csv` with instructions not to translate them
2. **Abbreviations**: All abbreviations from `abbreviations.csv` with their expansions
3. **Medical Terms**: All medical/technical terms from `medical_technical_terms.csv` with Shona translations
4. **Translation Guidelines**: Professional tone, Shona orthography, context preservation

## Example Output

For the text: "The patient was admitted to NICU for treatment"

The Agent Translator will:

- Keep "NICU" in English (from exclusion list)
- Use "murwere" for "patient" (from medical terms)
- Use "kurapwa" for "treatment" (from medical terms)
- Translate the rest naturally in Shona

Result: "Murwere akapinzwa muNICU kuti arapwe"

## Error Handling

- **Missing API Key**: Clear error message if `OPENAI_API_KEY` is not set
- **Network Issues**: Graceful handling of API timeouts and connection errors
- **Missing Glossary Files**: Warning messages but continues operation
- **Invalid Responses**: Validation of OpenAI responses before caching

## Comparison with Other Translators

| Feature                | Agent  | OpenAI | Google | MyMemory |
| ---------------------- | ------ | ------ | ------ | -------- |
| Custom System Prompt   | ✅     | ❌     | ❌     | ❌       |
| Exclusion List Support | ✅     | ❌     | ❌     | ❌       |
| Glossary Integration   | ✅     | ✅     | ✅     | ✅       |
| Caching                | ✅     | ✅     | ✅     | ✅       |
| Cost                   | Medium | Medium | Low    | Low      |
| Quality                | High   | High   | Medium | Low      |
