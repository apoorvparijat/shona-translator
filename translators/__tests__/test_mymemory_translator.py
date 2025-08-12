#!/usr/bin/env python3
"""
Test suite for MyMemoryShonaTranslator using standard Python unittest framework
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mymemory_translator import MyMemoryShonaTranslator


class TestMyMemoryShonaTranslator(unittest.TestCase):
    """Test cases for MyMemoryShonaTranslator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test glossary directory
        os.makedirs('glossary', exist_ok=True)
        
        # Initialize translator
        self.translator = MyMemoryShonaTranslator()
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_mymemory_translator_initialization(self):
        """Test that MyMemoryShonaTranslator initializes correctly"""
        self.assertIsNotNone(self.translator)
        self.assertEqual(self.translator._get_rate_limit_delay(), 0.1)
        self.assertTrue(hasattr(self.translator, '_translate_with_api'))
    
    def test_get_translator_info(self):
        """Test that translator info is returned correctly"""
        info = self.translator.get_translator_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('translator_type', info)
        self.assertIn('rate_limit_delay', info)
        self.assertIn('glossary_stats', info)
        
        self.assertEqual(info['translator_type'], "MyMemoryShonaTranslator")
        self.assertEqual(info['rate_limit_delay'], 0.1)
        self.assertIsInstance(info['glossary_stats'], dict)
    
    @patch('mymemory_translator.requests.get')
    def test_translate_text_success(self, mock_get):
        """Test successful translation via MyMemory API"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'responseData': {
                'translatedText': 'Mhoro'
            },
            'responseStatus': 200
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.translator._translate_with_api("Hello")
        
        self.assertEqual(result, "Mhoro")
        mock_get.assert_called_once()
    
    @patch('mymemory_translator.requests.get')
    def test_translate_text_api_error(self, mock_get):
        """Test handling of API errors"""
        # Mock API error response
        mock_response = Mock()
        mock_response.json.return_value = {
            'responseStatus': 403,
            'responseDetails': 'API key invalid'
        }
        mock_get.return_value = mock_response
        
        result = self.translator._translate_with_api("Hello")
        
        # Should return None when API fails
        self.assertIsNone(result)
    
    @patch('mymemory_translator.requests.get')
    def test_translate_text_network_error(self, mock_get):
        """Test handling of network errors"""
        # Mock network error
        mock_get.side_effect = Exception("Network error")
        
        result = self.translator._translate_with_api("Hello")
        
        # Should return None when network fails
        self.assertIsNone(result)
    
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
        result = self.translator._translate_with_api("")
        self.assertIsNone(result)
        
        result = self.translator._translate_with_api(None)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
