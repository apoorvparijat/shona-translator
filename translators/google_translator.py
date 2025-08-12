#!/usr/bin/env python3
"""
Google Translate Shona Translator - Uses Google Translate API for English to Shona DOCX translation
"""

import os
import re
import logging
from typing import Optional
from dotenv import load_dotenv
from base_translator import BaseShonaTranslator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Try to import Google Translate
try:
    from googletrans import Translator
    GOOGLE_AVAILABLE = True
    USE_GOOGLETRANS = True
except (ImportError, AttributeError) as e:
    logger.error(f"Failed to import googletrans: {e}")
    logger.error("Please install the correct version: pip install googletrans==4.0.0-rc1")
    GOOGLE_AVAILABLE = False
    USE_GOOGLETRANS = False

class GoogleShonaTranslator(BaseShonaTranslator):
    """English to Shona translator using Google Translate API with shared glossary"""
    
    def __init__(self, glossary_dir: str = "glossary"):
        super().__init__(glossary_dir)
        
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google Translate not available. Please install: pip install googletrans==4.0.0-rc1")
        
        try:
            self.translator = Translator()
            logger.info("Google Translate client initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize Google Translate: {e}")
        
        logger.info("Google Shona Translator initialized")
    
    def _translate_with_api(self, text: str) -> Optional[str]:
        """Translate text using Google Translate API"""
        return self._translate_with_googletrans(text)
    
    def _translate_with_googletrans(self, text: str) -> Optional[str]:
        """Translate using googletrans library"""
        try:
            # Preprocess the text using shared glossary manager
            processed_text = self.glossary_manager.preprocess_text(text)
            
            # Google Translate API call
            result = self.translator.translate(processed_text, src='en', dest='sn')
            
            if result and result.text and result.text.strip():
                translated_text = result.text.strip()
                if translated_text != text:
                    logger.info(f"Google: '{text[:50]}...' -> '{translated_text[:50]}...'")
                    return translated_text
                else:
                    logger.warning(f"Google returned same text for: {text[:50]}...")
                    return None
            else:
                logger.warning(f"Google returned empty translation for: {text[:50]}...")
                return None
                
        except Exception as e:
            logger.error(f"Google Translate API error: {e}")
            return None
    

    
    def _get_rate_limit_delay(self) -> float:
        """Get the rate limit delay for Google Translate API"""
        return 0.2  # Google Translate needs a bit more delay

def main():
    """Main function to run the Google Translate translator"""
    try:
        translator = GoogleShonaTranslator()
        
        # Example usage - this is just for demonstration
        # In practice, use the CLI tool: python shona_translate.py input.docx --method google
        print("🌍 Google Translate Shona Translator")
        print("Use the CLI tool for file translation:")
        print("  python shona_translate.py input.docx --method google")
        
        # Print translator info
        info = translator.get_translator_info()
        print(f"\n📊 Translator Info:")
        print(f"   Type: {info['translator_type']}")
        print(f"   Rate limit delay: {info['rate_limit_delay']}s")
        print(f"   Glossary stats: {info['glossary_stats']}")
        
        print("\n🔍 Google Translate Features:")
        print("- Fast and reliable translation service")
        print("- Shared glossary for deterministic terms")
        print("- Abbreviation preprocessing")
        print("- Post-processing error correction")
        print("- Maintained document formatting")
    
    except Exception as e:
        print(f"❌ Failed to initialize Google Translate translator: {e}")
        print("Make sure you have installed the correct googletrans version:")
        print("pip install googletrans==4.0.0-rc1")
        print("If you still get dependency conflicts, try:")
        print("pip uninstall googletrans")
        print("pip install googletrans==4.0.0-rc1")

if __name__ == "__main__":
    main()