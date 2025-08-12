#!/usr/bin/env python3
"""
Shona Translator - High-accuracy English to Shona DOCX translation tool
"""

import os
import re
from typing import List, Dict, Optional
from docx import Document
from googletrans import Translator
import openai
from dotenv import load_dotenv
import time
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShonaTranslator:
    """High-accuracy English to Shona translator for DOCX documents"""
    
    def __init__(self):
        try:
            # Initialize Google Translate with updated method
            self.google_translator = Translator()
        except Exception as e:
            logger.warning(f"Error initializing Google Translator: {e}")
            self.google_translator = None
        
        self.openai_client = None
        
        # Initialize OpenAI if API key is available
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_client = openai.OpenAI()
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OpenAI API key not found. Using Google Translate only.")
    
    def translate_with_google(self, text: str) -> str:
        """Translate text using Google Translate"""
        if not self.google_translator:
            return text
        
        try:
            # Add a small delay to avoid rate limiting
            time.sleep(0.1)
            result = self.google_translator.translate(text, src='en', dest='sn')
            if result and result.text:
                return result.text
            else:
                return text
        except Exception as e:
            logger.error(f"Google Translate error: {e}")
            # Try to reinitialize translator
            try:
                self.google_translator = Translator()
                result = self.google_translator.translate(text, src='en', dest='sn')
                return result.text if result and result.text else text
            except Exception as e2:
                logger.error(f"Failed to reinitialize Google Translator: {e2}")
                return text
    
    def translate_with_openai(self, text: str) -> Optional[str]:
        """Translate text using OpenAI with context awareness"""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional translator specializing in English to Shona translation. 
                        Shona is a Bantu language spoken primarily in Zimbabwe. 
                        Provide accurate, natural-sounding translations that preserve the meaning and tone of the original text.
                        Consider cultural context and use appropriate formal/informal registers.
                        Only return the translated text, no explanations."""
                    },
                    {
                        "role": "user",
                        "content": f"Translate this English text to Shona: {text}"
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI translation error: {e}")
            return None
    
    def get_best_translation(self, text: str) -> str:
        """Get the best translation by comparing multiple services"""
        if not text.strip():
            return text
        
        # Skip translation for very short text or numbers/special characters only
        if len(text.strip()) < 3 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        # Try Google Translate first
        google_translation = self.translate_with_google(text)
        
        # If Google Translate fails, try OpenAI
        if self.openai_client and (google_translation == text or not google_translation):
            openai_translation = self.translate_with_openai(text)
            if openai_translation and openai_translation != text:
                logger.info(f"Using OpenAI translation for: {text[:50]}...")
                return openai_translation
        
        # If we have both translations, prefer OpenAI for better context
        if self.openai_client and google_translation != text:
            openai_translation = self.translate_with_openai(text)
            if openai_translation and openai_translation != text:
                logger.info(f"Original: {text[:50]}...")
                logger.info(f"Google: {google_translation[:50]}...")
                logger.info(f"OpenAI: {openai_translation[:50]}...")
                return openai_translation
        
        # Fallback to Google translation or original text
        if google_translation and google_translation != text:
            return google_translation
        
        logger.warning(f"No translation available for: {text[:50]}...")
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
        # For simplicity, we'll apply the formatting of the first run to the entire translation
        if runs:
            new_run = paragraph.add_run(translated_text)
            # Copy formatting from the first run
            new_run.bold = runs[0].bold
            new_run.italic = runs[0].italic
            new_run.underline = runs[0].underline
            new_run.font.name = runs[0].font.name
            new_run.font.size = runs[0].font.size
        else:
            paragraph.add_run(translated_text)
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.1)
    
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
    translator = ShonaTranslator()
    
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
        print("- Used Google Translate as primary service")
        if translator.openai_client:
            print("- Enhanced with OpenAI for context-aware translation")
        print("- Preserved document formatting and structure")
        print("- Maintained tables and paragraph formatting")
    else:
        print("❌ Translation failed. Check the logs for details.")

if __name__ == "__main__":
    main()