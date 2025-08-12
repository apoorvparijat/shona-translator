#!/usr/bin/env python3
"""
Shona Translator CLI - Command-line interface for translating English documents to Shona
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional

# Add translators directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'translators'))

# Import translators
try:
    from mymemory_translator import MyMemoryShonaTranslator
    from google_translator import GoogleShonaTranslator
    from openai_translator import OpenAIShonaTranslator
    TRANSLATORS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing translators: {e}")
    print("Make sure you're running this from the project root directory")
    TRANSLATORS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShonaTranslateCLI:
    """Command-line interface for Shona translation"""
    
    def __init__(self):
        self.translators = {
            'mymemory': MyMemoryShonaTranslator,
            'google': GoogleShonaTranslator,
            'openai': OpenAIShonaTranslator
        }
    
    def validate_input_file(self, file_path: str) -> bool:
        """Validate that input file exists and is a DOCX file"""
        if not os.path.exists(file_path):
            print(f"❌ Error: Input file '{file_path}' does not exist")
            return False
        
        if not file_path.lower().endswith('.docx'):
            print(f"❌ Error: Input file '{file_path}' is not a DOCX file")
            return False
        
        return True
    
    def get_output_filename(self, input_path: str, method: str) -> str:
        """Generate output filename based on input and method"""
        input_file = Path(input_path)
        base_name = input_file.stem
        return f"{base_name}_shona_{method}.docx"
    
    def translate_with_method(self, input_file: str, method: str, output_file: Optional[str] = None) -> bool:
        """Translate using a specific method"""
        if method not in self.translators:
            print(f"❌ Error: Unknown translation method '{method}'")
            print(f"Available methods: {', '.join(self.translators.keys())}")
            return False
        
        try:
            # Generate output filename if not provided
            if not output_file:
                output_file = self.get_output_filename(input_file, method)
            
            print(f"🤖 Starting {method.upper()} translation...")
            print(f"📄 Input: {input_file}")
            print(f"📄 Output: {output_file}")
            
            # Initialize translator
            translator_class = self.translators[method]
            translator = translator_class()
            
            # Get translator info
            info = translator.get_translator_info()
            print(f"📊 Translator: {info['translator_type']}")
            print(f"📊 Rate limit: {info['rate_limit_delay']}s")
            print(f"📊 Glossary terms: {info['glossary_stats']['medical_technical_terms']}")
            
            # Perform translation
            success = translator.translate_docx(input_file, output_file)
            
            if success:
                print(f"✅ {method.upper()} translation completed successfully!")
                print(f"📄 Saved as: {output_file}")
                return True
            else:
                print(f"❌ {method.upper()} translation failed")
                return False
                
        except Exception as e:
            print(f"❌ Error during {method.upper()} translation: {e}")
            return False
    
    def translate_with_multiple_methods(self, input_file: str, methods: List[str]) -> dict:
        """Translate using multiple methods and return results"""
        results = {}
        
        print(f"🚀 Starting multi-method translation of: {input_file}")
        print(f"🎯 Methods: {', '.join(methods)}")
        print("=" * 60)
        
        for method in methods:
            output_file = self.get_output_filename(input_file, method)
            success = self.translate_with_method(input_file, method, output_file)
            results[method] = {
                'success': success,
                'output_file': output_file if success else None
            }
            print("-" * 40)
        
        return results
    
    def print_summary(self, results: dict):
        """Print summary of translation results"""
        print("\n" + "=" * 60)
        print("📋 TRANSLATION SUMMARY")
        print("=" * 60)
        
        success_count = sum(1 for result in results.values() if result['success'])
        total_count = len(results)
        
        for method, result in results.items():
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            output_info = f" -> {result['output_file']}" if result['success'] else ""
            print(f"{method.upper():10}: {status}{output_info}")
        
        print(f"\nOverall: {success_count}/{total_count} translations completed successfully")
        
        if success_count > 0:
            print("\n🎉 Translation files created:")
            for method, result in results.items():
                if result['success']:
                    print(f"   📄 {method.upper()}: {result['output_file']}")
        
        print("=" * 60)

def main():
    """Main CLI function"""
    if not TRANSLATORS_AVAILABLE:
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description="Translate English DOCX documents to Shona using multiple translation services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate using default method (MyMemory)
  python shona_translate.py document.docx
  
  # Translate using specific method
  python shona_translate.py document.docx --method google
  
  # Translate using multiple methods
  python shona_translate.py document.docx --method google,openai,mymemory
  
  # Specify custom output file
  python shona_translate.py document.docx --method openai --output custom_output.docx
  
  # Show available methods
  python shona_translate.py --list-methods
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='Input DOCX file to translate'
    )
    
    parser.add_argument(
        '--method', '-m',
        default='mymemory',
        help='Translation method(s). Use comma-separated list for multiple methods. '
             'Default: mymemory. Available: mymemory, google, openai'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (only used with single method)'
    )
    
    parser.add_argument(
        '--list-methods',
        action='store_true',
        help='List available translation methods and exit'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize CLI
    cli = ShonaTranslateCLI()
    
    # Handle list-methods
    if args.list_methods:
        print("Available translation methods:")
        for method, translator_class in cli.translators.items():
            print(f"  {method}: {translator_class.__name__}")
        return
    
    # Validate input file
    if not args.input_file:
        parser.error("Input file is required")
    
    if not cli.validate_input_file(args.input_file):
        sys.exit(1)
    
    # Parse methods
    methods = [m.strip().lower() for m in args.method.split(',')]
    
    # Validate methods
    invalid_methods = [m for m in methods if m not in cli.translators]
    if invalid_methods:
        print(f"❌ Error: Invalid translation method(s): {', '.join(invalid_methods)}")
        print(f"Available methods: {', '.join(cli.translators.keys())}")
        sys.exit(1)
    
    # Perform translation
    if len(methods) == 1:
        # Single method translation
        method = methods[0]
        success = cli.translate_with_method(args.input_file, method, args.output)
        sys.exit(0 if success else 1)
    else:
        # Multiple method translation
        results = cli.translate_with_multiple_methods(args.input_file, methods)
        cli.print_summary(results)
        
        # Exit with appropriate code
        success_count = sum(1 for result in results.values() if result['success'])
        if success_count == len(methods):
            print("\n🎉 All translations completed successfully!")
            sys.exit(0)
        elif success_count > 0:
            print("\n⚠️  Partial success - some translations completed")
            sys.exit(1)
        else:
            print("\n❌ All translations failed")
            sys.exit(2)

if __name__ == "__main__":
    main()
