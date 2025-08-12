#!/usr/bin/env python3
"""
MyMemory Shona Translator - Uses MyMemory API for English to Shona DOCX translation
"""

import os
import json
import requests
import logging
from typing import Optional
from dotenv import load_dotenv
from base_translator import BaseShonaTranslator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MyMemoryShonaTranslator(BaseShonaTranslator):
    """English to Shona translator using MyMemory API with shared glossary"""
    
    def __init__(self, glossary_dir: str = "glossary"):
        super().__init__(glossary_dir)
        
        # MyMemory API
        self.mymemory_base_url = "https://api.mymemory.translated.net/get"
        
        logger.info("MyMemory Shona Translator initialized")
    
    def _translate_with_api(self, text: str) -> Optional[str]:
        """Translate text using MyMemory API with preprocessing"""
        try:
            # Preprocess the text using shared glossary manager
            processed_text = self.glossary_manager.preprocess_text(text)
            
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
            
            return None
            
        except Exception as e:
            logger.error(f"MyMemory API error: {e}")
            return None
    
    def _get_rate_limit_delay(self) -> float:
        """Get the rate limit delay for MyMemory API"""
        return 0.1  # MyMemory is relatively fast

def main():
    """Main function to run the MyMemory translator"""
    translator = MyMemoryShonaTranslator()
    
    # Example usage - this is just for demonstration
    # In practice, use the CLI tool: python shona_translate.py input.docx --method mymemory
    print("🌐 MyMemory Shona Translator")
    print("Use the CLI tool for file translation:")
    print("  python shona_translate.py input.docx --method mymemory")
    
    # Print translator info
    info = translator.get_translator_info()
    print(f"\n📊 Translator Info:")
    print(f"   Type: {info['translator_type']}")
    print(f"   Rate limit delay: {info['rate_limit_delay']}s")
    print(f"   Glossary stats: {info['glossary_stats']}")
    
    print("\n🔍 MyMemory Translation Features:")
    print("- Free MyMemory API service")
    print("- Shared glossary for deterministic terms")
    print("- Abbreviation preprocessing")
    print("- Post-processing error correction")
    print("- Preserved document formatting and structure")

if __name__ == "__main__":
    main()