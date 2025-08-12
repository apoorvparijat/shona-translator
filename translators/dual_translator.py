#!/usr/bin/env python3
"""
Dual Document Translator - Creates two versions of documents using OpenAI and Google Translate
"""

import os
import sys
import time
import logging
import concurrent.futures
from typing import Optional, Tuple
from dotenv import load_dotenv

# Import our custom translators
try:
    from openai_translator import OpenAIShonaTranslator
    OPENAI_AVAILABLE = True
except ImportError as e:
    OPENAI_AVAILABLE = False
    openai_error = str(e)

try:
    from google_translator import GoogleShonaTranslator
    GOOGLE_AVAILABLE = True
except ImportError as e:
    GOOGLE_AVAILABLE = False
    google_error = str(e)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DualDocumentTranslator:
    """Creates two versions of documents using OpenAI and Google Translate"""
    
    def __init__(self):
        self.openai_translator = None
        self.google_translator = None
        
        # Initialize translators with fallback capability
        self.init_translators()
        
        logger.info("Dual Document Translator initialized")
    
    def init_translators(self):
        """Initialize both translators with error handling"""
        # Try to initialize OpenAI translator
        if OPENAI_AVAILABLE:
            try:
                self.openai_translator = OpenAIShonaTranslator()
                logger.info("✅ OpenAI translator initialized successfully")
            except Exception as e:
                logger.warning(f"❌ Failed to initialize OpenAI translator: {e}")
                self.openai_translator = None
        else:
            logger.warning(f"❌ OpenAI translator not available: {openai_error}")
        
        # Try to initialize Google translator
        if GOOGLE_AVAILABLE:
            try:
                self.google_translator = GoogleShonaTranslator()
                logger.info("✅ Google translator initialized successfully")
            except Exception as e:
                logger.warning(f"❌ Failed to initialize Google translator: {e}")
                self.google_translator = None
        else:
            logger.warning(f"❌ Google translator not available: {google_error}")
        
        # Check if at least one translator is available
        if not self.openai_translator and not self.google_translator:
            raise Exception("No translators available. Please check your setup.")
    
    def translate_with_openai(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Translate document using OpenAI"""
        if not self.openai_translator:
            return False, "OpenAI translator not available"
        
        try:
            logger.info(f"🤖 Starting OpenAI translation: {input_file} -> {output_file}")
            success = self.openai_translator.translate_docx(input_file, output_file)
            if success:
                return True, f"OpenAI translation completed: {output_file}"
            else:
                return False, "OpenAI translation failed"
        except Exception as e:
            error_msg = f"OpenAI translation error: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def translate_with_google(self, input_file: str, output_file: str) -> Tuple[bool, str]:
        """Translate document using Google Translate"""
        if not self.google_translator:
            return False, "Google translator not available"
        
        try:
            logger.info(f"🌍 Starting Google translation: {input_file} -> {output_file}")
            success = self.google_translator.translate_docx(input_file, output_file)
            if success:
                return True, f"Google translation completed: {output_file}"
            else:
                return False, "Google translation failed"
        except Exception as e:
            error_msg = f"Google translation error: {e}"
            logger.error(error_msg)
            return False, error_msg
    
    def translate_document_dual(self, input_file: str, 
                               openai_output: str = None, 
                               google_output: str = None,
                               parallel: bool = True) -> dict:
        """
        Translate document using both services
        
        Args:
            input_file: Path to input DOCX file
            openai_output: Output file for OpenAI translation (optional)
            google_output: Output file for Google translation (optional)
            parallel: Whether to run translations in parallel
        
        Returns:
            Dictionary with translation results
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Generate default output file names if not provided
        base_name = os.path.splitext(input_file)[0]
        if not openai_output:
            openai_output = f"{base_name}_shona_openai.docx"
        if not google_output:
            google_output = f"{base_name}_shona_google.docx"
        
        results = {
            'input_file': input_file,
            'openai': {'file': openai_output, 'success': False, 'message': ''},
            'google': {'file': google_output, 'success': False, 'message': ''},
            'start_time': time.time()
        }
        
        logger.info(f"🚀 Starting dual translation of: {input_file}")
        logger.info(f"📄 OpenAI output: {openai_output}")
        logger.info(f"📄 Google output: {google_output}")
        
        if parallel and self.openai_translator and self.google_translator:
            # Run both translations in parallel
            logger.info("⚡ Running translations in parallel...")
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both translation tasks
                openai_future = executor.submit(self.translate_with_openai, input_file, openai_output)
                google_future = executor.submit(self.translate_with_google, input_file, google_output)
                
                # Wait for OpenAI result
                try:
                    openai_success, openai_msg = openai_future.result(timeout=1800)  # 30 min timeout
                    results['openai']['success'] = openai_success
                    results['openai']['message'] = openai_msg
                except Exception as e:
                    results['openai']['message'] = f"OpenAI timeout/error: {e}"
                
                # Wait for Google result
                try:
                    google_success, google_msg = google_future.result(timeout=1800)  # 30 min timeout
                    results['google']['success'] = google_success
                    results['google']['message'] = google_msg
                except Exception as e:
                    results['google']['message'] = f"Google timeout/error: {e}"
        
        else:
            # Run translations sequentially or use fallback
            logger.info("⏳ Running translations sequentially...")
            
            # Try OpenAI first
            if self.openai_translator:
                openai_success, openai_msg = self.translate_with_openai(input_file, openai_output)
                results['openai']['success'] = openai_success
                results['openai']['message'] = openai_msg
            else:
                results['openai']['message'] = "OpenAI translator not available"
            
            # Then try Google
            if self.google_translator:
                google_success, google_msg = self.translate_with_google(input_file, google_output)
                results['google']['success'] = google_success
                results['google']['message'] = google_msg
            else:
                results['google']['message'] = "Google translator not available"
        
        results['end_time'] = time.time()
        results['duration'] = results['end_time'] - results['start_time']
        
        return results
    
    def print_results(self, results: dict):
        """Print translation results in a nice format"""
        print("\n" + "="*60)
        print("📊 DUAL TRANSLATION RESULTS")
        print("="*60)
        print(f"📁 Input file: {results['input_file']}")
        print(f"⏱️  Total duration: {results['duration']:.1f} seconds")
        print()
        
        # OpenAI results
        openai_status = "✅ SUCCESS" if results['openai']['success'] else "❌ FAILED"
        print(f"🤖 OPENAI TRANSLATION: {openai_status}")
        print(f"   📄 Output: {results['openai']['file']}")
        print(f"   💬 Message: {results['openai']['message']}")
        print()
        
        # Google results
        google_status = "✅ SUCCESS" if results['google']['success'] else "❌ FAILED"
        print(f"🌍 GOOGLE TRANSLATION: {google_status}")
        print(f"   📄 Output: {results['google']['file']}")
        print(f"   💬 Message: {results['google']['message']}")
        print()
        
        # Summary
        success_count = sum([results['openai']['success'], results['google']['success']])
        print(f"📋 SUMMARY: {success_count}/2 translations completed successfully")
        
        if success_count > 0:
            print("\n🎉 Translation files created:")
            if results['openai']['success']:
                print(f"   🤖 OpenAI version: {results['openai']['file']}")
            if results['google']['success']:
                print(f"   🌍 Google version: {results['google']['file']}")
        
        print("="*60)

def main():
    """Main function to run dual translation"""
    try:
        # Initialize dual translator
        dual_translator = DualDocumentTranslator()
        
        # Input file
        input_file = "collection-tools.docx"
        
        if not os.path.exists(input_file):
            print(f"❌ Error: Input file '{input_file}' not found.")
            print("Available files:")
            for file in os.listdir('.'):
                if file.endswith('.docx'):
                    print(f"   📄 {file}")
            return
        
        print("🚀 DUAL DOCUMENT TRANSLATOR")
        print("=" * 50)
        print(f"📄 Translating: {input_file}")
        print("🎯 Creating two versions:")
        print("   🤖 OpenAI (GPT-3.5-turbo)")
        print("   🌍 Google Translate")
        print("=" * 50)
        
        # Run dual translation
        results = dual_translator.translate_document_dual(
            input_file=input_file,
            parallel=True  # Run in parallel for speed
        )
        
        # Print results
        dual_translator.print_results(results)
        
        # Exit with appropriate code
        success_count = sum([results['openai']['success'], results['google']['success']])
        if success_count == 2:
            print("\n🎉 All translations completed successfully!")
            sys.exit(0)
        elif success_count == 1:
            print("\n⚠️  Partial success - one translation completed")
            sys.exit(1)
        else:
            print("\n❌ All translations failed")
            sys.exit(2)
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY environment variable (for OpenAI)")
        print("2. Installed required libraries:")
        print("   pip install openai googletrans==4.0.0-rc1 python-docx python-dotenv")
        sys.exit(3)

if __name__ == "__main__":
    main()