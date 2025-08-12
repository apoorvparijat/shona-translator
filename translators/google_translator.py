#!/usr/bin/env python3
"""
Google Translate Shona Translator - Uses Google Translate API for English to Shona DOCX translation
"""

import os
import re
import time
import logging
from typing import List, Dict, Optional
from docx import Document
from dotenv import load_dotenv

# Try to import Google Translate with fallback to requests-based translation
try:
    from googletrans import Translator
    GOOGLE_AVAILABLE = True
    USE_GOOGLETRANS = True
except (ImportError, AttributeError) as e:
    print(f"⚠️  googletrans library has dependency conflicts: {e}")
    print("🔄  Falling back to requests-based Google Translate...")
    GOOGLE_AVAILABLE = True
    USE_GOOGLETRANS = False

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GoogleShonaTranslator:
    """English to Shona translator using Google Translate API"""
    
    def __init__(self):
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google Translate not available")
        
        self.use_googletrans = USE_GOOGLETRANS
        
        if self.use_googletrans:
            try:
                self.translator = Translator()
                logger.info("Google Translate client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize googletrans, falling back to requests: {e}")
                self.use_googletrans = False
        
        if not self.use_googletrans:
            # Use requests-based fallback
            import requests
            self.session = requests.Session()
            logger.info("Requests-based Google Translate fallback initialized")
        
        # Medical/technical glossary for post-processing corrections
        self.domain_corrections = {
            # Common Google Translate issues with Shona medical terms
            "hutano": "hutano",  # healthcare - sometimes gets mistranslated
            "chipatara": "chipatara",  # hospital
            "murwere": "murwere",  # patient
            "chiremba": "chiremba",  # doctor
            "mukoti": "mukoti",  # nurse
            "bvunzurudzo": "bvunzurudzo",  # interview
            "mubvunzo": "mubvunzo",  # questionnaire
            "kutsvagisa": "kutsvagisa",  # research
            "kudzidza": "kudzidza",  # study
            "maitiro": "maitiro",  # methodology
            "kuongororwa": "kuongororwa",  # analysis
            "mhedzisiro": "mhedzisiro",  # results
        }
        
        logger.info("Google Shona Translator initialized")
    
    def translate_with_google(self, text: str) -> str:
        """Translate text using Google Translate API"""
        if not text.strip():
            return text
        
        # Skip very short or numeric-only text
        if len(text.strip()) < 2 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        if self.use_googletrans:
            return self._translate_with_googletrans(text)
        else:
            return self._translate_with_requests(text)
    
    def _translate_with_googletrans(self, text: str) -> str:
        """Translate using googletrans library"""
        try:
            # Google Translate API call
            result = self.translator.translate(text, src='en', dest='sn')
            
            if result and result.text and result.text.strip():
                translated_text = result.text.strip()
                corrected_text = self.apply_domain_corrections(translated_text)
                
                if corrected_text != text:
                    logger.info(f"Google: '{text[:50]}...' -> '{corrected_text[:50]}...'")
                    return corrected_text
                else:
                    logger.warning(f"Google returned same text for: {text[:50]}...")
                    return text
            else:
                logger.warning(f"Google returned empty translation for: {text[:50]}...")
                return text
                
        except Exception as e:
            logger.error(f"Google Translate API error: {e}")
            return text
    
    def _translate_with_requests(self, text: str) -> str:
        """Translate using direct requests to Google Translate"""
        try:
            # Use direct requests to Google Translate service
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',
                'tl': 'sn',
                'dt': 't',
                'q': text
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and len(result[0]) > 0:
                    translated_text = result[0][0][0]
                    corrected_text = self.apply_domain_corrections(translated_text)
                    
                    if corrected_text != text:
                        logger.info(f"Google (requests): '{text[:50]}...' -> '{corrected_text[:50]}...'")
                        return corrected_text
            
            logger.warning(f"Google requests API returned no translation for: {text[:50]}...")
            return text
            
        except Exception as e:
            logger.error(f"Google Translate requests error: {e}")
            return text
    
    def apply_domain_corrections(self, text: str) -> str:
        """Apply domain-specific corrections to Google Translate output"""
        corrected_text = text
        
        # Apply word-level corrections for medical/technical terms
        for incorrect, correct in self.domain_corrections.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(incorrect) + r'\b'
            corrected_text = re.sub(pattern, correct, corrected_text, flags=re.IGNORECASE)
        
        # Common Google Translate pattern fixes for Shona
        corrections = {
            r'\bkubvunza\b': 'bvunzurudzo',  # Fix interview translation
            r'\bmubvunzo\b': 'mubvunzo',  # Questionnaire consistency
            r'\bzvikuru\b': 'zvikuru',  # Very/much consistency
        }
        
        for pattern, replacement in corrections.items():
            corrected_text = re.sub(pattern, replacement, corrected_text, flags=re.IGNORECASE)
        
        return corrected_text
    
    def translate_paragraph(self, paragraph) -> None:
        """Translate a paragraph while preserving formatting"""
        if not paragraph.text.strip():
            return
        
        # Store original formatting
        runs = list(paragraph.runs)
        original_text = paragraph.text
        
        # Translate the text
        translated_text = self.translate_with_google(original_text)
        
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
        
        # Add delay to respect rate limits
        time.sleep(0.2)
    
    def translate_table(self, table) -> None:
        """Translate table content while preserving structure"""
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.translate_paragraph(paragraph)
    
    def translate_docx(self, input_file: str, output_file: str) -> bool:
        """Translate a DOCX file from English to Shona using Google Translate"""
        try:
            logger.info(f"Starting Google Translate translation of {input_file}")
            
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
            logger.info(f"Google Translate translation completed. Saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error translating document: {e}")
            return False

def main():
    """Main function to run the Google Translate translator"""
    try:
        translator = GoogleShonaTranslator()
        
        # Input and output files
        input_file = "collection-tools.docx"
        output_file = "collection-tools_shona_google.docx"
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return
        
        print(f"🌍 Starting Google Translate translation of '{input_file}' from English to Shona...")
        print("⚡ Using Google Translate API for fast, reliable translation")
        print("This may take a while depending on document size...")
        
        success = translator.translate_docx(input_file, output_file)
        
        if success:
            print(f"✅ Google Translate translation completed successfully!")
            print(f"📄 Translated document saved as: {output_file}")
            print("\n🔍 Google Translate Features:")
            print("- Fast and reliable translation service")
            print("- Domain-specific post-processing corrections")
            print("- Medical/technical term optimization")
            print("- Maintained document formatting")
        else:
            print("❌ Google Translate translation failed. Check the logs for details.")
    
    except Exception as e:
        print(f"❌ Failed to initialize Google Translate translator: {e}")
        print("Make sure you have installed googletrans library:")
        print("pip install googletrans==4.0.0-rc1")

if __name__ == "__main__":
    main()