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
    
    def __init__(self, glossary_dir: str = "../glossary"):
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
            
            logger.debug(f"Google Translate request - Original: '{text[:100]}...' -> Processed: '{processed_text[:100]}...'")
            
            # Google Translate API call - handle both sync and async versions
            result = self.translator.translate(processed_text, src='en', dest='sn')
            
            # Check if result is a coroutine (async version)
            if hasattr(result, '__await__'):
                logger.debug(f"Google Translate returned coroutine, attempting to await...")
                try:
                    import asyncio
                    # Create new event loop if none exists
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    # Await the coroutine
                    result = loop.run_until_complete(result)
                    logger.debug(f"Successfully awaited coroutine, result: {result}")
                except Exception as await_error:
                    logger.error(f"Failed to await coroutine: {await_error}")
                    return None
            
            # Detailed result inspection
            logger.debug(f"Google Translate result type: {type(result)}")
            logger.debug(f"Google Translate result: {result}")
            
            if result:
                logger.debug(f"Google Translate result attributes: {dir(result)}")
                logger.debug(f"Google Translate result.text: {getattr(result, 'text', 'NO_TEXT_ATTR')}")
                logger.debug(f"Google Translate result.src: {getattr(result, 'src', 'NO_SRC_ATTR')}")
                logger.debug(f"Google Translate result.dest: {getattr(result, 'dest', 'NO_DEST_ATTR')}")
                logger.debug(f"Google Translate result.origin: {getattr(result, 'origin', 'NO_ORIGIN_ATTR')}")
                
                if hasattr(result, 'text') and result.text:
                    translated_text = result.text.strip()
                    logger.debug(f"Google Translate translated_text: '{translated_text}'")
                    
                    # Validate the translation
                    if translated_text and translated_text != processed_text:
                        # Additional validation: check if translation is not just empty or whitespace
                        if len(translated_text) > 0 and not translated_text.isspace():
                            logger.info(f"Google: '{text[:50]}...' -> '{translated_text[:50]}...'")
                            return translated_text
                        else:
                            logger.warning(f"Google returned empty/whitespace translation for: '{text[:100]}...' -> '{translated_text}'")
                            return None
                    else:
                        logger.warning(f"Google returned same text or empty for: '{text[:100]}...' -> '{translated_text}' (processed: '{processed_text[:100]}...')")
                        return None
                else:
                    logger.warning(f"Google returned result without text attribute or empty text for: '{text[:100]}...'")
                    logger.warning(f"Result object: {result}")
                    return None
            else:
                logger.warning(f"Google returned None result for: '{text[:100]}...'")
                return None
                
        except Exception as e:
            # Handle None text safely
            text_preview = text[:100] if text else "None"
            logger.error(f"Google Translate API error for text '{text_preview}...': {e}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error details: {str(e)}")
            
            # Check for specific error types
            if "429" in str(e):
                logger.error("Rate limit exceeded (HTTP 429) - Google Translate is throttling requests")
            elif "403" in str(e):
                logger.error("Access forbidden (HTTP 403) - Check if Google Translate is blocking requests")
            elif "timeout" in str(e).lower():
                logger.error("Request timeout - Network or service issue")
            elif "connection" in str(e).lower():
                logger.error("Connection error - Network issue")
            
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