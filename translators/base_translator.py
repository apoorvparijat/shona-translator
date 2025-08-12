#!/usr/bin/env python3
"""
Base Translator - Common functionality for all Shona translators
"""

import os
import re
import time
import logging
from typing import Optional
from docx import Document
from glossary_manager import GlossaryManager

logger = logging.getLogger(__name__)

class BaseShonaTranslator:
    """Base class for all Shona translators with common functionality"""
    
    def __init__(self, glossary_dir: str = "../glossary"):
        self.glossary_manager = GlossaryManager(glossary_dir)
        logger.info("Base translator initialized with glossary manager")
    
    def get_best_translation(self, text: str) -> str:
        """Get the best translation using glossary-first approach with fallback to API"""
        if not text.strip():
            return text
        
        # Skip very short or numeric-only text
        if len(text.strip()) < 2 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        # 1. Try glossary first
        glossary_translation = self.glossary_manager.translate_with_glossary(text)
        
        # 2. Try API-specific translation
        api_translation = self._translate_with_api(text)
        
        # 3. Choose the best translation
        if glossary_translation and glossary_translation != text:
            if api_translation and api_translation != text and api_translation.strip():
                # Both glossary and API provided translations
                # Choose the one that translates more of the text
                glossary_english_words = self._count_english_words(glossary_translation)
                api_english_words = self._count_english_words(api_translation)
                
                if api_english_words < glossary_english_words:
                    # API translation is more complete
                    logger.info(f"API (chosen): '{text}' -> '{api_translation}'")
                    return self.glossary_manager.post_process_translation(api_translation)
                else:
                    # Glossary translation is more complete or equal
                    logger.info(f"Glossary (chosen): '{text}' -> '{glossary_translation}'")
                    return self.glossary_manager.post_process_translation(glossary_translation)
            else:
                # Only glossary provided translation
                logger.info(f"Glossary: '{text}' -> '{glossary_translation}'")
                return self.glossary_manager.post_process_translation(glossary_translation)
        elif api_translation and api_translation != text and api_translation.strip():
            # Only API provided translation
            logger.info(f"API: '{text}' -> '{api_translation}'")
            return self.glossary_manager.post_process_translation(api_translation)
        
        # 4. If no translation found, return original
        logger.warning(f"No translation found for: {text}")
        return text
    
    def _count_english_words(self, text: str) -> int:
        """Count English words in text to determine translation completeness"""
        import re
        # Simple heuristic: count words that look like English
        english_pattern = r'\b[a-zA-Z]{2,}\b'
        english_words = re.findall(english_pattern, text)
        return len(english_words)
    
    def _translate_with_api(self, text: str) -> Optional[str]:
        """Translate text using the specific API (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement _translate_with_api")
    
    def translate_paragraph(self, paragraph) -> None:
        """Translate a paragraph while preserving formatting"""
        if not paragraph.text.strip():
            return
        
        # Store original formatting
        runs = list(paragraph.runs)
        original_text = paragraph.text
        
        # Translate the text
        translated_text = self.get_best_translation(original_text)
        
        # Clear the paragraph
        paragraph.clear()
        
        # Add translated text with preserved formatting
        if runs:
            new_run = paragraph.add_run(translated_text)
            # Copy formatting from the first run
            if runs[0].bold is not None:
                new_run.bold = runs[0].bold
            if runs[0].italic is not None:
                new_run.italic = runs[0].italic
            if runs[0].underline is not None:
                new_run.underline = runs[0].underline
            if runs[0].font.name:
                new_run.font.name = runs[0].font.name
            if runs[0].font.size:
                new_run.font.size = runs[0].font.size
        else:
            paragraph.add_run(translated_text)
        
        # Add delay to respect rate limits (can be overridden by subclasses)
        time.sleep(self._get_rate_limit_delay())
    
    def translate_table(self, table) -> None:
        """Translate table content while preserving structure"""
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.translate_paragraph(paragraph)
    
    def translate_docx(self, input_file: str, output_file: str) -> bool:
        """Translate a DOCX file from English to Shona"""
        try:
            logger.info(f"Starting translation of {input_file}")
            
            # Load the document
            doc = Document(input_file)
            
            # Translate main document paragraphs
            logger.info("Translating paragraphs...")
            total_paragraphs = len([p for p in doc.paragraphs if p.text.strip()])
            
            for i, paragraph in enumerate(doc.paragraphs):
                if paragraph.text.strip():
                    logger.info(f"Translating paragraph {i+1}/{total_paragraphs}")
                    self.translate_paragraph(paragraph)
            
            # Translate tables
            logger.info("Translating tables...")
            for i, table in enumerate(doc.tables):
                logger.info(f"Translating table {i+1}/{len(doc.tables)}")
                self.translate_table(table)
            
            # Save the translated document
            doc.save(output_file)
            logger.info(f"Translation completed. Saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error translating document: {e}")
            return False
    
    def _get_rate_limit_delay(self) -> float:
        """Get the rate limit delay in seconds (can be overridden by subclasses)"""
        return 0.1  # Default delay
    
    def get_translator_info(self) -> dict:
        """Get information about the translator"""
        return {
            'translator_type': self.__class__.__name__,
            'glossary_stats': self.glossary_manager.get_glossary_stats(),
            'rate_limit_delay': self._get_rate_limit_delay()
        }
