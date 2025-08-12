#!/usr/bin/env python3
"""
Test smart caching system with actual translators
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from base_translator import BaseShonaTranslator
from translation_cache import TranslationCache

class MockTranslator(BaseShonaTranslator):
    """Mock translator for testing"""
    
    def _translate_with_api(self, text: str):
        """Mock API translation"""
        if text == "Hello world":
            return "Mhoro nyika"
        elif text == "Good morning":
            return "Mangwanani"
        elif text == "Unique test text":
            return "Yakasarudzika bvunzo zvinyorwa"
        else:
            return None
    
    def _get_rate_limit_delay(self):
        return 0.0

class TestSmartCaching(unittest.TestCase):
    """Test cases for smart caching system"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary cache
        self.cache = TranslationCache("test_cache.json")
        self.cache.clear_cache()  # Start with clean cache
        
        # Create mock translator
        with patch('base_translator.get_translation_cache', return_value=self.cache):
            self.translator = MockTranslator()
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove test cache file
        if os.path.exists("test_cache.json"):
            os.unlink("test_cache.json")
    
    def test_cache_first_translation(self):
        """Test that first translation is cached"""
        text = "Unique test text"
        
        # First translation should hit the API
        result1 = self.translator.get_best_translation(text)
        self.assertEqual(result1, "Yakasarudzika bvunzo zvinyorwa")
        
        # Check cache stats
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['misses'], 1)  # First request was a miss
        self.assertEqual(stats['hits'], 0)
        
        # Verify translation was cached
        cached_translation = self.cache.get(text)
        self.assertEqual(cached_translation, "Yakasarudzika bvunzo zvinyorwa")
    
    def test_cache_reuse_translation(self):
        """Test that cached translations are reused"""
        text = "Unique test text"
        
        # First translation
        result1 = self.translator.get_best_translation(text)
        self.assertEqual(result1, "Yakasarudzika bvunzo zvinyorwa")
        
        # Second translation should use cache
        result2 = self.translator.get_best_translation(text)
        self.assertEqual(result2, "Yakasarudzika bvunzo zvinyorwa")
        
        # Check cache stats
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['misses'], 1)  # First request was a miss
        self.assertEqual(stats['hits'], 1)    # Second request was a hit
    
    def test_cache_multiple_providers(self):
        """Test caching with multiple providers"""
        text = "Hello world"
        
        # Cache translation from different providers
        self.cache.set(text, "Mhoro nyika", "google", confidence=0.8)
        self.cache.set(text, "Mhoro pasi", "mymemory", confidence=0.9)
        
        # Should get the best translation (highest confidence)
        best_translation = self.cache.get(text)
        self.assertEqual(best_translation, "Mhoro pasi")  # Higher confidence
        
        # Should get specific provider translation
        google_translation = self.cache.get(text, "google")
        self.assertEqual(google_translation, "Mhoro nyika")
    
    def test_cache_normalization(self):
        """Test that cache keys are normalized"""
        text1 = "Hello world"
        text2 = "  hello WORLD  "
        
        # Cache with normalized text
        self.cache.set(text1, "Mhoro nyika", "test")
        
        # Should retrieve with different case/whitespace
        cached_translation = self.cache.get(text2, "test")
        self.assertEqual(cached_translation, "Mhoro nyika")
    
    def test_cache_empty_text_handling(self):
        """Test handling of empty text"""
        empty_text = ""
        
        # Empty text should not be cached
        result = self.translator.get_best_translation(empty_text)
        self.assertEqual(result, empty_text)
        
        # Should not affect cache stats
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['total_requests'], 0)
    
    def test_cache_persistence(self):
        """Test that cache persists between translator instances"""
        text = "Unique test text"
        
        # First translator instance
        with patch('base_translator.get_translation_cache', return_value=self.cache):
            translator1 = MockTranslator()
            result1 = translator1.get_best_translation(text)
        
        # Second translator instance should use cached result
        with patch('base_translator.get_translation_cache', return_value=self.cache):
            translator2 = MockTranslator()
            result2 = translator2.get_best_translation(text)
        
        self.assertEqual(result1, result2)
        
        # Check that cache was used
        stats = self.cache.get_cache_stats()
        self.assertEqual(stats['misses'], 1)  # First request
        self.assertEqual(stats['hits'], 1)    # Second request used cache

if __name__ == '__main__':
    unittest.main()
