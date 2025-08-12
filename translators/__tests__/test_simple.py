#!/usr/bin/env python3
"""
Simple test example showing the clean approach
"""

import unittest
import tempfile
import os
import shutil

# Import what we want to test
from glossary_manager import GlossaryManager


class TestSimple(unittest.TestCase):
    """Simple test to verify the setup works"""
    
    def setUp(self):
        """Set up a clean test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        os.makedirs('glossary', exist_ok=True)
        self.glossary = GlossaryManager()
    
    def tearDown(self):
        """Clean up after tests"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_basic_functionality(self):
        """Test basic glossary functionality"""
        # Test that glossary manager works
        self.assertIsNotNone(self.glossary)
        
        # Test a simple translation
        result = self.glossary.translate_with_glossary("hello")
        self.assertEqual(result, "mhoro")
        
        # Test preprocessing
        result = self.glossary.preprocess_text("HCW")
        self.assertIn("healthcare worker", result.lower())


if __name__ == '__main__':
    unittest.main()
