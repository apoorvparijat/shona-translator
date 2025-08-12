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
        
        # Initialize translator
        self.translator = GoogleShonaTranslator()
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_google_translator_initialization(self):
        """Test that GoogleShonaTranslator initializes correctly"""
        self.assertIsNotNone(self.translator)
        self.assertEqual(self.translator.translator_type, "Google")
        self.assertEqual(self.translator.rate_limit_delay, 0.5)
        self.assertTrue(hasattr(self.translator, 'translate_text'))
    
    def test_get_translator_info(self):
        """Test that translator info is returned correctly"""
        info = self.translator.get_translator_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('translator_type', info)
        self.assertIn('rate_limit_delay', info)
        self.assertIn('glossary_stats', info)
        
        self.assertEqual(info['translator_type'], "Google")
        self.assertEqual(info['rate_limit_delay'], 0.5)
        self.assertIsInstance(info['glossary_stats'], dict)
    
    @patch('google_translator.googletrans.Translator')
    def test_translate_text_success(self, mock_translator_class):
        """Test successful translation via Google Translate"""
        # Mock successful translation
        mock_translator = Mock()
        mock_translator.translate.return_value.text = "Mhoro"
        mock_translator_class.return_value = mock_translator
        
        result = self.translator.translate_text("Hello")
        
        self.assertEqual(result, "Mhoro")
        mock_translator.translate.assert_called_once()
    
    @patch('google_translator.googletrans.Translator')
    def test_translate_text_translation_error(self, mock_translator_class):
        """Test handling of translation errors"""
        # Mock translation error
        mock_translator = Mock()
        mock_translator.translate.side_effect = Exception("Translation failed")
        mock_translator_class.return_value = mock_translator
        
        result = self.translator.translate_text("Hello")
        
        # Should return original text when translation fails
        self.assertEqual(result, "Hello")
    
    @patch('google_translator.googletrans.Translator')
    def test_translate_text_initialization_error(self, mock_translator_class):
        """Test handling of translator initialization errors"""
        # Mock initialization error
        mock_translator_class.side_effect = Exception("Initialization failed")
        
        result = self.translator.translate_text("Hello")
        
        # Should return original text when initialization fails
        self.assertEqual(result, "Hello")
    
    def test_get_best_translation_with_glossary(self):
        """Test that glossary terms are handled correctly"""
        # Test with a term that should be in the glossary
        test_text = "version"
        result = self.translator.get_best_translation(test_text)
        
        # Should return a string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        result = self.translator.translate_text("")
        self.assertEqual(result, "")
        
        result = self.translator.translate_text(None)
        self.assertEqual(result, "")
    
    def test_language_detection(self):
        """Test that the translator uses correct language codes"""
        # This test verifies that the translator is configured for English to Shona
        # The actual language codes should be 'en' for English and 'sn' for Shona
        self.assertEqual(self.translator.source_lang, 'en')
        self.assertEqual(self.translator.target_lang, 'sn')


if __name__ == '__main__':
    unittest.main()
