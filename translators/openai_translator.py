#!/usr/bin/env python3
"""
OpenAI Shona Translator - Uses OpenAI GPT models for English to Shona DOCX translation
"""

import os
import re
import time
import logging
from typing import List, Dict, Optional
from docx import Document
from dotenv import load_dotenv

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI library not installed. Please install with: pip install openai")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAIShonaTranslator:
    """English to Shona translator using OpenAI GPT models"""
    
    def __init__(self):
        self.client = None
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5-turbo for cost efficiency
        
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Please install with: pip install openai")
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        try:
            # Initialize OpenAI client with just the API key
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {e}")
        
        # System prompt for Shona translation
        self.system_prompt = """You are an expert English to Shona translator specializing in medical, technical, and academic documents. 

Key guidelines for translation:
1. Maintain formal and professional tone appropriate for academic/medical contexts
2. Use standard Shona orthography and grammar
3. For technical terms without direct Shona equivalents, provide the English term in parentheses after the Shona translation
4. Preserve the meaning and context while making it natural in Shona
5. For medical terms, use established Shona medical terminology where available
6. Keep document formatting markers intact (if any)

Common domain-specific translations:
- Healthcare: hutano
- Patient: murwere
- Doctor: chiremba
- Nurse: mukoti
- Hospital: chipatara
- Clinical: kiriniki
- Research: kutsvagisa
- Study: kudzidza
- Interview: bvunzurudzo
- Questionnaire: mubvunzo
- Methodology: maitiro
- Analysis: kuongororwa
- Results: mhedzisiro

Translate the following text from English to Shona:"""

        logger.info("OpenAI Shona Translator initialized")
    
    def translate_with_openai(self, text: str) -> str:
        """Translate text using OpenAI API"""
        if not text.strip():
            return text
        
        # Skip very short or numeric-only text
        if len(text.strip()) < 2 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=1000,
                temperature=0.3,  # Lower temperature for more consistent translations
                timeout=30
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            if translated_text and translated_text != text:
                logger.info(f"OpenAI: '{text[:50]}...' -> '{translated_text[:50]}...'")
                return translated_text
            else:
                logger.warning(f"OpenAI returned same text for: {text[:50]}...")
                return text
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return text
    
    def translate_paragraph(self, paragraph) -> None:
        """Translate a paragraph while preserving formatting"""
        if not paragraph.text.strip():
            return
        
        # Store original formatting
        runs = list(paragraph.runs)
        original_text = paragraph.text
        
        # Translate the text
        translated_text = self.translate_with_openai(original_text)
        
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
        time.sleep(0.5)
    
    def translate_table(self, table) -> None:
        """Translate table content while preserving structure"""
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    self.translate_paragraph(paragraph)
    
    def translate_docx(self, input_file: str, output_file: str) -> bool:
        """Translate a DOCX file from English to Shona using OpenAI"""
        try:
            logger.info(f"Starting OpenAI translation of {input_file}")
            
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
            logger.info(f"OpenAI translation completed. Saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error translating document: {e}")
            return False

def main():
    """Main function to run the OpenAI translator"""
    try:
        translator = OpenAIShonaTranslator()
        
        # Input and output files
        input_file = "collection-tools.docx"
        output_file = "collection-tools_shona_openai.docx"
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return
        
        print(f"🤖 Starting OpenAI translation of '{input_file}' from English to Shona...")
        print("⚡ Using GPT-3.5-turbo for high-quality translation")
        print("This may take a while due to API rate limits...")
        
        success = translator.translate_docx(input_file, output_file)
        
        if success:
            print(f"✅ OpenAI translation completed successfully!")
            print(f"📄 Translated document saved as: {output_file}")
            print("\n🔍 OpenAI Translation Features:")
            print("- Context-aware AI translation")
            print("- Medical/technical terminology expertise")
            print("- Professional tone preservation")
            print("- Maintained document formatting")
        else:
            print("❌ OpenAI translation failed. Check the logs for details.")
    
    except Exception as e:
        print(f"❌ Failed to initialize OpenAI translator: {e}")
        print("Make sure you have:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Installed openai library: pip install openai")

if __name__ == "__main__":
    main()