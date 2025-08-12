#!/usr/bin/env python3
"""
Test translation cache functionality
"""

import sys
import os
import tempfile
import json
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from translation_cache import TranslationCache

class TestTranslationCache(unittest.TestCase):
    """Test cases for TranslationCache"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary cache file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.cache = TranslationCache(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_cache_set_and_get(self):
        """Test basic cache set and get functionality"""
        text = "Hello world"
        translation = "Mhoro nyika"
        provider = "test_provider"
        
        # Set translation in cache
        self.cache.set(text, translation, provider)
        
        # Get translation from cache
        cached_translation = self.cache.get(text, provider)
        
        self.assertEqual(cached_translation, translation)
    
    def test_cache_get_best_translation(self):
        """Test getting best translation when multiple providers exist"""
        text = "Hello world"
        translation1 = "Mhoro nyika"
        translation2 = "Mhoro pasi"
        provider1 = "provider1"
        provider2 = "provider2"
        
        # Set translations with different confidence levels
        self.cache.set(text, translation1, provider1, confidence=0.8)
        self.cache.set(text, translation2, provider2, confidence=0.9)
        
        # Get best translation (should be the one with higher confidence)
        best_translation = self.cache.get(text)
        
        self.assertEqual(best_translation, translation2)
    
    def test_cache_normalization(self):
        """Test that cache keys are normalized"""
        text1 = "Hello world"
        text2 = "  hello WORLD  "
        translation = "Mhoro nyika"
        provider = "test_provider"
        
        # Set translation with normalized text
        self.cache.set(text1, translation, provider)
        
        # Get translation with different case/whitespace
        cached_translation = self.cache.get(text2, provider)
        
        self.assertEqual(cached_translation, translation)
    
    def test_cache_empty_text(self):
        """Test handling of empty text"""
        empty_text = ""
        translation = "some translation"
        provider = "test_provider"
        
        # Empty text should not be cached
        self.cache.set(empty_text, translation, provider)
        
        # Getting empty text should return the text itself
        result = self.cache.get(empty_text)
        self.assertEqual(result, empty_text)
    
    def test_cache_stats(self):
        """Test cache statistics"""
        text = "Hello world"
        translation = "Mhoro nyika"
        provider = "test_provider"
        
        # Make some requests
        self.cache.get(text)  # Miss
        self.cache.set(text, translation, provider)
        self.cache.get(text)  # Hit
        self.cache.get(text)  # Hit
        
        stats = self.cache.get_cache_stats()
        
        self.assertEqual(stats['total_requests'], 3)
        self.assertEqual(stats['hits'], 2)
        self.assertEqual(stats['misses'], 1)
        self.assertEqual(stats['hit_rate'], 66.67)
    
    def test_cache_persistence(self):
        """Test that cache persists between instances"""
        text = "Hello world"
        translation = "Mhoro nyika"
        provider = "test_provider"
        
        # Set translation in first cache instance
        self.cache.set(text, translation, provider)
        
        # Create new cache instance with same file
        new_cache = TranslationCache(self.temp_file.name)
        
        # Should be able to retrieve the translation
        cached_translation = new_cache.get(text, provider)
        self.assertEqual(cached_translation, translation)

if __name__ == '__main__':
    unittest.main()
