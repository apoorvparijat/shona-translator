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
        self.assertEqual(self.translator.translator_type, "OpenAI")
        self.assertEqual(self.translator.rate_limit_delay, 2.0)
        self.assertTrue(hasattr(self.translator, 'translate_text'))
    
    def test_get_translator_info(self):
        """Test that translator info is returned correctly"""
        info = self.translator.get_translator_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('translator_type', info)
        self.assertIn('rate_limit_delay', info)
        self.assertIn('glossary_stats', info)
        
        self.assertEqual(info['translator_type'], "OpenAI")
        self.assertEqual(info['rate_limit_delay'], 2.0)
        self.assertIsInstance(info['glossary_stats'], dict)
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_success(self, mock_create):
        """Test successful translation via OpenAI API"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Mhoro"
        mock_create.return_value = mock_response
        
        result = self.translator.translate_text("Hello")
        
        self.assertEqual(result, "Mhoro")
        mock_create.assert_called_once()
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_api_error(self, mock_create):
        """Test handling of API errors"""
        # Mock API error
        mock_create.side_effect = Exception("API error")
        
        result = self.translator.translate_text("Hello")
        
        # Should return original text when API fails
        self.assertEqual(result, "Hello")
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_empty_response(self, mock_create):
        """Test handling of empty API response"""
        # Mock empty response
        mock_response = Mock()
        mock_response.choices = []
        mock_create.return_value = mock_response
        
        result = self.translator.translate_text("Hello")
        
        # Should return original text when response is empty
        self.assertEqual(result, "Hello")
    
    @patch('openai_translator.openai.ChatCompletion.create')
    def test_translate_text_missing_content(self, mock_create):
        """Test handling of response with missing content"""
        # Mock response with missing content
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None
        mock_create.return_value = mock_response
        
        result = self.translator.translate_text("Hello")
        
        # Should return original text when content is missing
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
    
    def test_prompt_generation(self):
        """Test that the prompt is generated correctly"""
        test_text = "Hello world"
        prompt = self.translator._generate_prompt(test_text)
        
        self.assertIsInstance(prompt, str)
        self.assertIn("Shona", prompt)
        self.assertIn(test_text, prompt)
        self.assertIn("Translate", prompt)


if __name__ == '__main__':
    unittest.main()
