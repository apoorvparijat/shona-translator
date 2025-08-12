#!/usr/bin/env python3
"""
OpenAI Shona Translator - Uses OpenAI GPT models for English to Shona DOCX translation
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from base_translator import BaseShonaTranslator

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

class OpenAIShonaTranslator(BaseShonaTranslator):
    """English to Shona translator using OpenAI GPT models with shared glossary"""
    
    def __init__(self, glossary_dir: str = "glossary"):
        super().__init__(glossary_dir)
        
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
    
    def _translate_with_api(self, text: str) -> Optional[str]:
        """Translate text using OpenAI API"""
        try:
            # Preprocess the text using shared glossary manager
            processed_text = self.glossary_manager.preprocess_text(text)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": processed_text}
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
                return None
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None
    
    def _get_rate_limit_delay(self) -> float:
        """Get the rate limit delay for OpenAI API"""
        return 0.5  # OpenAI needs more delay due to rate limits

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
        print("⚡ Using GPT-3.5-turbo with shared glossary")
        print("This may take a while due to API rate limits...")
        
        # Print translator info
        info = translator.get_translator_info()
        print(f"\n📊 Translator Info:")
        print(f"   Type: {info['translator_type']}")
        print(f"   Rate limit delay: {info['rate_limit_delay']}s")
        print(f"   Glossary stats: {info['glossary_stats']}")
        print(f"   Model: {translator.model}")
        
        success = translator.translate_docx(input_file, output_file)
        
        if success:
            print(f"✅ OpenAI translation completed successfully!")
            print(f"📄 Translated document saved as: {output_file}")
            print("\n🔍 OpenAI Translation Features:")
            print("- Context-aware AI translation")
            print("- Shared glossary for deterministic terms")
            print("- Abbreviation preprocessing")
            print("- Post-processing error correction")
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