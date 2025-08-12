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

class GoogleShonaTranslator(BaseShonaTranslator):
    """English to Shona translator using Google Translate API with shared glossary"""
    
    def __init__(self, glossary_dir: str = "glossary"):
        super().__init__(glossary_dir)
        
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
        
        logger.info("Google Shona Translator initialized")
    
    def _translate_with_api(self, text: str) -> Optional[str]:
        """Translate text using Google Translate API"""
        if self.use_googletrans:
            return self._translate_with_googletrans(text)
        else:
            return self._translate_with_requests(text)
    
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
    
    def _translate_with_requests(self, text: str) -> Optional[str]:
        """Translate using direct requests to Google Translate"""
        try:
            # Preprocess the text using shared glossary manager
            processed_text = self.glossary_manager.preprocess_text(text)
            
            # Use direct requests to Google Translate service
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',
                'tl': 'sn',
                'dt': 't',
                'q': processed_text
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0 and len(result[0]) > 0:
                    translated_text = result[0][0][0]
                    if translated_text != text:
                        logger.info(f"Google (requests): '{text[:50]}...' -> '{translated_text[:50]}...'")
                        return translated_text
            
            logger.warning(f"Google requests API returned no translation for: {text[:50]}...")
            return None
            
        except Exception as e:
            logger.error(f"Google Translate requests error: {e}")
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
        print(f"   Using googletrans: {translator.use_googletrans}")
        
        print("\n🔍 Google Translate Features:")
        print("- Fast and reliable translation service")
        print("- Shared glossary for deterministic terms")
        print("- Abbreviation preprocessing")
        print("- Post-processing error correction")
        print("- Maintained document formatting")
    
    except Exception as e:
        print(f"❌ Failed to initialize Google Translate translator: {e}")
        print("Make sure you have installed googletrans library:")
        print("pip install googletrans==4.0.0-rc1")

if __name__ == "__main__":
    main()