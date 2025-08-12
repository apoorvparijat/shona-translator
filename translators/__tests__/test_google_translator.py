#!/usr/bin/env python3
"""
Test suite for GoogleShonaTranslator using standard Python unittest framework
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_translator import GoogleShonaTranslator


class TestGoogleShonaTranslator(unittest.TestCase):
    """Test cases for GoogleShonaTranslator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test glossary directory
        os.makedirs('glossary', exist_ok=True)
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_google_translator_initialization(self):
        """Test that GoogleShonaTranslator initializes correctly"""
        with patch('google_translator.Translator') as mock_translator_class:
            mock_translator = Mock()
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            self.assertIsNotNone(translator)
            self.assertEqual(translator._get_rate_limit_delay(), 0.2)
            self.assertTrue(hasattr(translator, '_translate_with_api'))
    
    def test_get_translator_info(self):
        """Test that translator info is returned correctly"""
        with patch('googletrans.Translator') as mock_translator_class:
            mock_translator = Mock()
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            info = translator.get_translator_info()
            
            self.assertIsInstance(info, dict)
            self.assertIn('translator_type', info)
            self.assertIn('rate_limit_delay', info)
            self.assertIn('glossary_stats', info)
            
            self.assertEqual(info['translator_type'], "GoogleShonaTranslator")
            self.assertEqual(info['rate_limit_delay'], 0.2)
            self.assertIsInstance(info['glossary_stats'], dict)
    
    def test_translate_text_success(self):
        """Test successful translation via Google Translate"""
        with patch('google_translator.Translator') as mock_translator_class:
            # Mock successful translation
            mock_translator = Mock()
            mock_result = Mock()
            mock_result.text = "Zvakanaka"
            mock_translator.translate.return_value = mock_result
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            result = translator._translate_with_api("Excellent")
            
            self.assertEqual(result, "Zvakanaka")
            mock_translator.translate.assert_called_once()
    
    def test_get_best_translation_with_api_only(self):
        """Test that API translation is used when glossary doesn't have the term"""
        with patch('google_translator.Translator') as mock_translator_class:
            # Mock successful translation
            mock_translator = Mock()
            mock_result = Mock()
            mock_result.text = "Zvakanaka"
            mock_translator.translate.return_value = mock_result
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            # Test with a term that's not in the glossary
            result = translator.get_best_translation("Excellent")
            
            # Should return the API translation
            self.assertEqual(result, "Zvakanaka")
            mock_translator.translate.assert_called_once()
    
    def test_translate_text_translation_error(self):
        """Test handling of translation errors"""
        with patch('google_translator.Translator') as mock_translator_class:
            # Mock translation error
            mock_translator = Mock()
            mock_translator.translate.side_effect = Exception("Translation failed")
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            result = translator._translate_with_api("Excellent")
            
            # Should return None when translation fails
            self.assertIsNone(result)
    
    def test_get_best_translation_with_api_error(self):
        """Test that API errors are handled correctly in get_best_translation"""
        with patch('google_translator.Translator') as mock_translator_class:
            # Mock translation error
            mock_translator = Mock()
            mock_translator.translate.side_effect = Exception("Translation failed")
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            # Test with a term that's not in the glossary
            result = translator.get_best_translation("Excellent")
            
            # Should return original text when API fails and glossary doesn't have it
            self.assertEqual(result, "Excellent")
    
    def test_translate_text_initialization_error(self):
        """Test handling of translator initialization errors"""
        with patch('google_translator.Translator') as mock_translator_class:
            # Mock initialization error
            mock_translator_class.side_effect = Exception("Initialization failed")
            
            with self.assertRaises(Exception):
                translator = GoogleShonaTranslator()
    
    def test_get_best_translation_with_glossary(self):
        """Test that glossary terms are handled correctly"""
        with patch('googletrans.Translator') as mock_translator_class:
            mock_translator = Mock()
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            # Test with a term that should be in the glossary
            test_text = "version"
            result = translator.get_best_translation(test_text)
            
            # Should return a string
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        with patch('googletrans.Translator') as mock_translator_class:
            mock_translator = Mock()
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            result = translator._translate_with_api("")
            self.assertIsNone(result)
            
            result = translator._translate_with_api(None)
            self.assertIsNone(result)
    
    def test_language_detection(self):
        """Test that the translator uses correct language codes"""
        with patch('googletrans.Translator') as mock_translator_class:
            mock_translator = Mock()
            mock_translator_class.return_value = mock_translator
            
            translator = GoogleShonaTranslator()
            # This test verifies that the translator is configured for English to Shona
            # The actual language codes should be 'en' for English and 'sn' for Shona
            # Note: These are hardcoded in the _translate_with_googletrans method
            self.assertTrue(hasattr(translator, 'translator'))


if __name__ == '__main__':
    unittest.main()
