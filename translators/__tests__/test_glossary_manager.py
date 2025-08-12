#!/usr/bin/env python3
"""
Test suite for GlossaryManager using standard Python unittest framework
"""

import unittest
import os
import sys
import tempfile
import shutil

# Import the module to test
from glossary_manager import GlossaryManager


class TestGlossaryManager(unittest.TestCase):
    """Test cases for GlossaryManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test glossary directory
        os.makedirs('glossary', exist_ok=True)
        
        # Initialize glossary manager
        self.glossary = GlossaryManager()
    
    def tearDown(self):
        """Clean up after each test method"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def test_glossary_manager_initialization(self):
        """Test that GlossaryManager initializes correctly"""
        self.assertIsNotNone(self.glossary)
        self.assertTrue(hasattr(self.glossary, 'preprocess_text'))
        self.assertTrue(hasattr(self.glossary, 'translate_with_glossary'))
        self.assertTrue(hasattr(self.glossary, 'post_process_translation'))
    
    def test_preprocess_text(self):
        """Test text preprocessing functionality"""
        test_cases = [
            ("HCW CDS AI NICU", "healthcare worker clinical decision support artificial intelligence neonatal intensive care unit"),
            ("version 1.0", "version 1.0"),
            ("normal text", "normal text")
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.glossary.preprocess_text(input_text)
                self.assertEqual(result.lower(), expected.lower())
    
    def test_translate_with_glossary(self):
        """Test glossary-based translation"""
        test_cases = [
            ("version", "shanduko"),
            ("healthcare workers", "vashandi vehutano"),
            ("clinical decision support", "rutsigiro rwesarudzo yekiriniki"),
            ("what is your name", "zita rako ndiani")
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.glossary.translate_with_glossary(input_text)
                self.assertEqual(result, expected)
    
    def test_post_process_translation(self):
        """Test post-processing corrections"""
        test_cases = [
            ("mhando", "mhando"),
            ("manzwiro", "manzwiro"),
            ("kuongorora", "kuongorora")
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = self.glossary.post_process_translation(input_text)
                self.assertEqual(result, expected)
    
    def test_get_glossary_stats(self):
        """Test that glossary stats are returned correctly"""
        stats = self.glossary.get_glossary_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('medical_technical_terms', stats)
        self.assertIn('phrase_translations', stats)
        self.assertIn('abbreviations', stats)
        self.assertIn('post_processing_corrections', stats)
        
        # All stats should be integers
        for key, value in stats.items():
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)
    
    def test_csv_files_creation(self):
        """Test that CSV files are created correctly"""
        csv_files = [
            "glossary/medical_technical_terms.csv",
            "glossary/phrase_translations.csv", 
            "glossary/abbreviations.csv",
            "glossary/post_processing_corrections.csv"
        ]
        
        for csv_file in csv_files:
            with self.subTest(csv_file=csv_file):
                self.assertTrue(os.path.exists(csv_file))
                self.assertGreater(os.path.getsize(csv_file), 0)


if __name__ == '__main__':
    unittest.main()
