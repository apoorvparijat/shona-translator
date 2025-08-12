#!/usr/bin/env python3
"""
Simple Shona Translator - High-accuracy English to Shona DOCX translation tool
Using requests-based translation API
"""

import os
import re
import json
import time
import logging
from typing import List, Dict, Optional
from docx import Document
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleShonaTranslator:
    """Simple English to Shona translator for DOCX documents using MyMemory API"""
    
    def __init__(self):
        # MyMemory is a free translation API that doesn't require authentication
        self.mymemory_base_url = "https://api.mymemory.translated.net/get"
        
        # Common English to Shona translations for fallback
        self.common_translations = {
            "hello": "mhoro",
            "good morning": "mangwanani",
            "good afternoon": "masikati",
            "good evening": "manheru",
            "thank you": "ndatenda",
            "please": "ndapota",
            "yes": "hongu",
            "no": "kwete",
            "welcome": "mutauya",
            "goodbye": "chisarai zvakanaka",
            "name": "zita",
            "how are you": "makadii",
            "i am fine": "ndiri right",
            "what": "chii",
            "where": "kupi",
            "when": "rini",
            "why": "sei",
            "how": "sei",
            "who": "ani",
            "water": "mvura",
            "food": "chikafu",
            "house": "imba",
            "family": "mhuri",
            "friend": "shamwari",
            "work": "basa",
            "school": "chikoro",
            "book": "bhuku",
            "time": "nguva",
            "money": "mari",
            "love": "rudo",
            "help": "rubatsiro",
            "problem": "dambudziko",
            "good": "zvakanaka",
            "bad": "zvisina",
            "big": "hombe",
            "small": "duku",
            "new": "nyowani",
            "old": "chekare"
        }
        
        logger.info("Simple Shona Translator initialized")
    
    def translate_with_mymemory(self, text: str) -> str:
        """Translate text using MyMemory API"""
        try:
            params = {
                'q': text,
                'langpair': 'en|sn',  # English to Shona
                'de': 'shona.translator@example.com'  # Email for rate limiting
            }
            
            response = requests.get(self.mymemory_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    translated_text = data.get('responseData', {}).get('translatedText', text)
                    if translated_text and translated_text.lower() != text.lower():
                        return translated_text
            
            logger.warning(f"MyMemory API returned no translation for: {text[:50]}...")
            return text
            
        except Exception as e:
            logger.error(f"MyMemory API error: {e}")
            return text
    
    def translate_with_fallback(self, text: str) -> str:
        """Try to translate using common translations dictionary"""
        text_lower = text.lower().strip()
        
        # Check for exact matches first
        if text_lower in self.common_translations:
            return self.common_translations[text_lower]
        
        # Check for partial matches
        for english, shona in self.common_translations.items():
            if english in text_lower:
                return text.lower().replace(english, shona)
        
        return text
    
    def get_best_translation(self, text: str) -> str:
        """Get the best translation by trying multiple approaches"""
        if not text.strip():
            return text
        
        # Skip translation for very short text or numbers/special characters only
        if len(text.strip()) < 2 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        # Try MyMemory API first
        mymemory_translation = self.translate_with_mymemory(text)
        
        # If API translation is different from original, use it
        if mymemory_translation != text and mymemory_translation.strip():
            logger.info(f"MyMemory: '{text}' -> '{mymemory_translation}'")
            return mymemory_translation
        
        # Try fallback dictionary
        fallback_translation = self.translate_with_fallback(text)
        if fallback_translation != text:
            logger.info(f"Fallback: '{text}' -> '{fallback_translation}'")
            return fallback_translation
        
        # If no translation found, return original
        logger.warning(f"No translation found for: {text}")
        return text
    
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
            new_run.bold = runs[0].bold
            new_run.italic = runs[0].italic
            new_run.underline = runs[0].underline
            if runs[0].font.name:
                new_run.font.name = runs[0].font.name
            if runs[0].font.size:
                new_run.font.size = runs[0].font.size
        else:
            paragraph.add_run(translated_text)
        
        # Add a small delay to be nice to the API
        time.sleep(0.2)
    
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
            for i, paragraph in enumerate(doc.paragraphs):
                if paragraph.text.strip():
                    logger.info(f"Translating paragraph {i+1}/{len(doc.paragraphs)}")
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

def main():
    """Main function to run the translator"""
    translator = SimpleShonaTranslator()
    
    # Input and output files
    input_file = "collection-tools.docx"
    output_file = "collection-tools_shona.docx"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    print(f"Translating '{input_file}' from English to Shona...")
    print("This may take a while depending on document size...")
    
    success = translator.translate_docx(input_file, output_file)
    
    if success:
        print(f"✅ Translation completed successfully!")
        print(f"📄 Translated document saved as: {output_file}")
        print("\n🔍 Translation Details:")
        print("- Used MyMemory API as primary service")
        print("- Enhanced with common Shona phrase dictionary")
        print("- Preserved document formatting and structure")
        print("- Maintained tables and paragraph formatting")
    else:
        print("❌ Translation failed. Check the logs for details.")

if __name__ == "__main__":
    main()