#!/usr/bin/env python3
"""
Test to reproduce the glossary bug where partial matches prevent API translation
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_translator import BaseShonaTranslator
from glossary_manager import GlossaryManager


class TestGlossaryBug(unittest.TestCase):
    """Test cases to reproduce the glossary bug"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test glossary directory
        os.makedirs('glossary', exist_ok=True)
        
        # Create a test glossary with some terms
        self._create_test_glossary()
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def _create_test_glossary(self):
        """Create a test glossary with specific terms"""
        import csv
        
        # Create medical_technical_terms.csv
        medical_terms = [
            {'english': 'clinical decision support system', 'shona': 'rutsigiro rwesarudzo yekiriniki hurongwa', 'category': 'medical'},
            {'english': 'cds', 'shona': 'rutsigiro rwesarudzo', 'category': 'medical'},
        ]
        
        with open('glossary/medical_technical_terms.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['english', 'shona', 'category'])
            writer.writeheader()
            writer.writerows(medical_terms)
        
        # Create phrase_translations.csv
        phrases = [
            {'english': 'what have been key benefits', 'shona': 'zvakave zvibatsiro zvakakosha', 'category': 'general'},
        ]
        
        with open('glossary/phrase_translations.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['english', 'shona', 'category'])
            writer.writeheader()
            writer.writerows(phrases)
        
        # Create other required CSV files
        for filename in ['abbreviations.csv', 'post_processing_corrections.csv', 'exclusion_list.csv']:
            with open(f'glossary/{filename}', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['term', 'reason'])
                writer.writeheader()
    
    def test_glossary_partial_match_bug(self):
        """Test that partial glossary matches don't prevent API translation"""
        # Create a mock translator that implements _translate_with_api
        class MockTranslator(BaseShonaTranslator):
            def _translate_with_api(self, text):
                # Mock API translation that would translate the full text
                if "clinical decision support system" in text.lower():
                    return "Zvakave zvibatsiro zvakakosha kana kuvandudzwa kubva pakushandisa Neotree's rutsigiro rwesarudzo yekiriniki hurongwa zvichienzaniswa neapo pakutanga pakanga pasina rutsigiro rwesarudzo yekiriniki hurongwa?"
                return None
            
            def _get_rate_limit_delay(self):
                return 0.0
        
        translator = MockTranslator()
        
        # Test text that should be partially translated by glossary but fully by API
        test_text = "What have been key benefits or improvements from using Neotree's clinical decision support system compared to before where there was no clinical decision support system?"
        
        # This should now work correctly - API translation should be chosen over partial glossary translation
        result = translator.get_best_translation(test_text)
        
        print(f"Original: {test_text}")
        print(f"Result: {result}")
        
        # Check if the result contains the full API translation
        self.assertIn("Zvakave zvibatsiro zvakakosha", result)
        self.assertNotIn("What have been key benefits", result)
        
        # Check that the result is mostly in Shona (not English)
        english_words = ["What", "have", "been", "key", "benefits", "or", "improvements", "from", "using", "compared", "to", "before", "where", "there", "was", "no"]
        untranslated_count = sum(1 for word in english_words if word in result)
        
        # Should have very few English words remaining
        self.assertLess(untranslated_count, 3, 
                       f"Too many English words remain untranslated: {untranslated_count}/{len(english_words)}")
    
    def test_glossary_vs_api_priority(self):
        """Test that API translation is used when glossary only provides partial translation"""
        class MockTranslator(BaseShonaTranslator):
            def _translate_with_api(self, text):
                # Mock API that would provide full translation
                if "clinical decision support" in text.lower():
                    return "Zvakave zvibatsiro zvakakosha kana kuvandudzwa kubva pakushandisa Neotree's rutsigiro rwesarudzo yekiriniki hurongwa zvichienzaniswa neapo pakutanga pakanga pasina rutsigiro rwesarudzo yekiriniki hurongwa?"
                return None
            
            def _get_rate_limit_delay(self):
                return 0.0
        
        translator = MockTranslator()
        
        test_text = "What have been key benefits or improvements from using Neotree's clinical decision support system compared to before where there was no clinical decision support system?"
        
        # Add debug logging
        print(f"\n=== Debug Info ===")
        glossary_result = translator.glossary_manager.translate_with_glossary(test_text)
        api_result = translator._translate_with_api(test_text)
        print(f"Glossary result: {glossary_result}")
        print(f"API result: {api_result}")
        
        if glossary_result and glossary_result != test_text:
            glossary_english = translator._count_english_words(glossary_result)
            print(f"Glossary English words: {glossary_english}")
        
        if api_result and api_result != test_text:
            api_english = translator._count_english_words(api_result)
            print(f"API English words: {api_english}")
        
        result = translator.get_best_translation(test_text)
        print(f"Final result: {result}")
        print(f"=== End Debug ===\n")
        
        # Should get full translation, not just glossary replacement
        self.assertIn("Zvakave zvibatsiro", result)
        self.assertNotIn("What have been key benefits", result)


if __name__ == '__main__':
    unittest.main()
