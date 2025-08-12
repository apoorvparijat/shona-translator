#!/usr/bin/env python3
"""
Test suite for BaseShonaTranslator using standard Python unittest framework
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_translator import BaseShonaTranslator


class TestBaseShonaTranslator(unittest.TestCase):
    """Test cases for BaseShonaTranslator class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test glossary directory
        os.makedirs('glossary', exist_ok=True)
        
        # Create a mock translator that inherits from BaseShonaTranslator
        class MockTranslator(BaseShonaTranslator):
            def __init__(self):
                super().__init__()
                self.rate_limit_delay = 0.1
            
            def _translate_with_api(self, text):
                return f"Mock translation: {text}"
        
        self.translator = MockTranslator()
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_base_translator_initialization(self):
        """Test that BaseShonaTranslator initializes correctly"""
        self.assertIsNotNone(self.translator)
        self.assertTrue(hasattr(self.translator, 'glossary_manager'))
        self.assertTrue(hasattr(self.translator, 'translate_text'))
        self.assertTrue(hasattr(self.translator, 'get_best_translation'))
    
    def test_get_best_translation(self):
        """Test the get_best_translation method"""
        test_text = "Hello world"
        result = self.translator.get_best_translation(test_text)
        
        # Should return a string
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_get_translator_info(self):
        """Test that translator info is returned correctly"""
        info = self.translator.get_translator_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn('translator_type', info)
        self.assertIn('rate_limit_delay', info)
        self.assertIn('glossary_stats', info)
        
        self.assertEqual(info['translator_type'], "MockTranslator")
        self.assertEqual(info['rate_limit_delay'], 0.1)
        self.assertIsInstance(info['glossary_stats'], dict)
    
    def test_rate_limiting(self):
        """Test that rate limiting works correctly"""
        import time
        
        start_time = time.time()
        
        # Call translate multiple times to test rate limiting
        for i in range(3):
            self.translator.get_best_translation(f"test {i}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Should take at least the rate limit delay * number of calls
        expected_min_time = self.translator._get_rate_limit_delay() * 2  # 2 delays between 3 calls
        self.assertGreaterEqual(elapsed_time, expected_min_time)
    
    def test_glossary_integration(self):
        """Test that glossary integration works"""
        # Test with a term that should be in the glossary
        test_text = "version"
        result = self.translator.get_best_translation(test_text)
        
        # Should return a string (either glossary translation or mock translation)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
