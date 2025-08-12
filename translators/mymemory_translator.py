#!/usr/bin/env python3
"""
Improved Shona Translator - Enhanced accuracy English to Shona DOCX translation
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

class ImprovedShonaTranslator:
    """Enhanced English to Shona translator with better accuracy"""
    
    def __init__(self):
        # MyMemory API
        self.mymemory_base_url = "https://api.mymemory.translated.net/get"
        
        # Enhanced medical/technical glossary
        self.medical_technical_glossary = {
            # Document terms
            "version": "shanduko",
            "objective": "chinangwa", 
            "methodology": "maitiro",
            "duration": "nguva",
            "participants": "vatori vechikamu",
            "sites": "nzvimbo",
            "introduction": "nhanganyaya",
            "discussion": "nhaurirano",
            "interview": "bvunzurudzo",
            "guide": "gwara",
            "questionnaire": "mubvunzo",
            "focus group": "boka rekutarisa",
            
            # Medical terms
            "healthcare": "hutano",
            "healthcare workers": "vashandi vehutano",
            "hospital": "chipatara",
            "patient": "murwere",
            "clinical": "kiriniki",
            "diagnosis": "kuongororwa",
            "treatment": "kurapwa",
            "medicine": "mushonga",
            "doctor": "chiremba",
            "nurse": "mukoti",
            "midwife": "nyamukuta",
            "newborn": "mwana achangoberekwa",
            "baby": "mwana",
            "neonatal": "vana vachangoberekwa",
            "ward": "wadhi",
            "facility": "nzvimbo yehutano",
            
            # Technology terms
            "system": "hurongwa",
            "technology": "hunyanzvi",
            "application": "application",
            "software": "software",
            "data": "data",
            "digital": "dhijitari",
            "artificial intelligence": "huchenjeri hwekugadzira",
            "decision support": "rutsigiro rwesarudzo",
            "clinical decision support": "rutsigiro rwesarudzo yekiriniki",
            
            # Research terms
            "study": "kudzidza",
            "research": "kutsvagisa",
            "observation": "kucherechedza",
            "analysis": "kuongororwa",
            "findings": "zvakawanwa",
            "results": "mhedzisiro",
            "conclusion": "mhedziso",
            "recommendations": "zviratidziro",
            
            # Common words with specific meanings
            "experience": "ruzivo",
            "workflow": "mukufamba webasa",
            "efficiency": "kushanda zvakanaka",
            "quality": "kunaka",
            "safety": "kuchengeteka",
            "training": "kudzidziswa",
            "support": "rutsigiro",
            "implementation": "kushandiswa",
            "evaluation": "kuongororwa",
            "feedback": "mhinduro",
            
            # Basic common translations (corrected)
            "hello": "mhoro",
            "good morning": "mangwanani",
            "good afternoon": "masikati", 
            "good evening": "manheru",
            "thank you": "ndatenda",
            "please": "ndapota",
            "yes": "hongu",
            "no": "kwete",
            "welcome": "mutauya",
            "goodbye": "chisarai zvakanaka"
        }
        
        # Context-specific phrase translations
        self.phrase_translations = {
            "what is your name": "zita rako ndiani",
            "how are you": "makadii",
            "i am fine": "ndiri right",
            "thank you very much": "ndatenda zvikuru",
            "please help me": "ndibatsireiwo",
            "good morning": "mangwanani akanaka",
            "clinical decision support system": "hurongwa hwekutsigira sarudzo dzekiriniki",
            "healthcare workers": "vashandi vehutano",
            "focus group discussion": "nhaurirano yeboka rekutarisa"
        }
        
        logger.info("Improved Shona Translator initialized with enhanced glossary")
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text to handle common patterns"""
        # Handle abbreviations
        text = re.sub(r'\bHCW\b', 'healthcare worker', text, flags=re.IGNORECASE)
        text = re.sub(r'\bCDS\b', 'clinical decision support', text, flags=re.IGNORECASE)
        text = re.sub(r'\bAI\b', 'artificial intelligence', text, flags=re.IGNORECASE)
        text = re.sub(r'\bNICU\b', 'neonatal intensive care unit', text, flags=re.IGNORECASE)
        
        return text
    
    def translate_with_glossary(self, text: str) -> Optional[str]:
        """Try to translate using enhanced glossary first"""
        text_lower = text.lower().strip()
        
        # Check for exact phrase matches first
        if text_lower in self.phrase_translations:
            return self.phrase_translations[text_lower]
        
        # Check for exact word matches
        if text_lower in self.medical_technical_glossary:
            return self.medical_technical_glossary[text_lower]
        
        # Check for partial matches and replace terms
        result = text
        replacements_made = False
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_terms = sorted(self.medical_technical_glossary.items(), 
                            key=lambda x: len(x[0]), reverse=True)
        
        for english, shona in sorted_terms:
            pattern = r'\b' + re.escape(english) + r'\b'
            if re.search(pattern, result, re.IGNORECASE):
                result = re.sub(pattern, shona, result, flags=re.IGNORECASE)
                replacements_made = True
        
        return result if replacements_made else None
    
    def translate_with_mymemory(self, text: str) -> str:
        """Translate text using MyMemory API with preprocessing"""
        try:
            # Preprocess the text
            processed_text = self.preprocess_text(text)
            
            params = {
                'q': processed_text,
                'langpair': 'en|sn',
                'de': 'shona.translator@example.com'
            }
            
            response = requests.get(self.mymemory_base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    translated_text = data.get('responseData', {}).get('translatedText', text)
                    if translated_text and translated_text.lower() != text.lower():
                        return translated_text
            
            return text
            
        except Exception as e:
            logger.error(f"MyMemory API error: {e}")
            return text
    
    def post_process_translation(self, text: str) -> str:
        """Post-process translation to fix common errors"""
        # Common correction patterns
        corrections = {
            r'\bmhando\b': 'shanduko',  # Fix version translation
            r'\bmanzwiro\b': 'pfungwa',  # Better word for feelings/thoughts
            r'\bkuongorora\b': 'kuongororwa',  # Standardize examination
        }
        
        result = text
        for pattern, replacement in corrections.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def get_best_translation(self, text: str) -> str:
        """Get the best translation using multiple approaches"""
        if not text.strip():
            return text
        
        # Skip very short or numeric-only text
        if len(text.strip()) < 2 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        # 1. Try glossary first (highest priority)
        glossary_translation = self.translate_with_glossary(text)
        if glossary_translation and glossary_translation != text:
            logger.info(f"Glossary: '{text}' -> '{glossary_translation}'")
            return self.post_process_translation(glossary_translation)
        
        # 2. Try MyMemory API
        api_translation = self.translate_with_mymemory(text)
        if api_translation != text and api_translation.strip():
            logger.info(f"MyMemory: '{text}' -> '{api_translation}'")
            return self.post_process_translation(api_translation)
        
        # 3. If no translation found, return original
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
        
        # Reduced delay for better performance
        time.sleep(0.1)
    
    def translate_table(self, table) -> None:
        """Translate table content while preserving structure"""
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.translate_paragraph(paragraph)
    
    def translate_docx(self, input_file: str, output_file: str) -> bool:
        """Translate a DOCX file from English to Shona with enhanced accuracy"""
        try:
            logger.info(f"Starting enhanced translation of {input_file}")
            
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
            logger.info(f"Enhanced translation completed. Saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error translating document: {e}")
            return False

def main():
    """Main function to run the improved translator"""
    translator = ImprovedShonaTranslator()
    
    # Input and output files
    input_file = "collection-tools.docx"
    output_file = "collection-tools_shona_improved.docx"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    print(f"🚀 Starting enhanced translation of '{input_file}' from English to Shona...")
    print("⚡ Using improved accuracy with medical/technical glossary")
    print("This may take a while depending on document size...")
    
    success = translator.translate_docx(input_file, output_file)
    
    if success:
        print(f"✅ Enhanced translation completed successfully!")
        print(f"📄 Translated document saved as: {output_file}")
        print("\n🔍 Enhanced Translation Features:")
        print("- Domain-specific medical/technical glossary")
        print("- Context-aware phrase translation")
        print("- Post-processing error correction")
        print("- Improved accuracy for technical terms")
        print("- Preserved document formatting and structure")
    else:
        print("❌ Translation failed. Check the logs for details.")

if __name__ == "__main__":
    main()