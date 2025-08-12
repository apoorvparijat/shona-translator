#!/usr/bin/env python3
"""
Test suite for OpenAIShonaTranslator using standard Python unittest framework
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai_translator import OpenAIShonaTranslator


class TestOpenAIShonaTranslator(unittest.TestCase):
    """Test cases for OpenAIShonaTranslator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test glossary directory
        os.makedirs('glossary', exist_ok=True)
        
        # Initialize translator
        self.translator = OpenAIShonaTranslator()
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_openai_translator_initialization(self):
        """Test that OpenAIShonaTranslator initializes correctly"""
        self.assertIsNotNone(self.translator)
        self.assertEqual(self.translator._get_rate_limit_delay(), 0.5)
        self.assertTrue(hasattr(self.translator, '_translate_with_api'))
    
    def test_get_translator_info(self):
        """Test that translator info is returned correctly"""
        info = self.translator.get_translator_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('translator_type', info)
        self.assertIn('rate_limit_delay', info)
        self.assertIn('glossary_stats', info)
        
        self.assertEqual(info['translator_type'], "OpenAIShonaTranslator")
        self.assertEqual(info['rate_limit_delay'], 0.5)
        self.assertIsInstance(info['glossary_stats'], dict)
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_success(self, mock_create):
        """Test successful translation via OpenAI API"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Mhoro"
        mock_create.return_value = mock_response
        
        result = self.translator._translate_with_api("Hello")
        
        self.assertEqual(result, "Mhoro")
        mock_create.assert_called_once()
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_api_error(self, mock_create):
        """Test handling of API errors"""
        # Mock API error
        mock_create.side_effect = Exception("API error")
        
        result = self.translator._translate_with_api("Hello")
        
        # Should return None when API fails
        self.assertIsNone(result)
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_empty_response(self, mock_create):
        """Test handling of empty API response"""
        # Mock empty response
        mock_response = Mock()
        mock_response.choices = []
        mock_create.return_value = mock_response
        
        result = self.translator._translate_with_api("Hello")
        
        # Should return None when response is empty
        self.assertIsNone(result)
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_missing_content(self, mock_create):
        """Test handling of response with missing content"""
        # Mock response with missing content
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None
        mock_create.return_value = mock_response
        
        result = self.translator._translate_with_api("Hello")
        
        # Should return None when content is missing
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
    
    def test_prompt_generation(self):
        """Test that the system prompt is correctly configured"""
        self.assertIsInstance(self.translator.system_prompt, str)
        self.assertIn("Shona", self.translator.system_prompt)
        self.assertIn("Translate", self.translator.system_prompt)


if __name__ == '__main__':
    unittest.main()
