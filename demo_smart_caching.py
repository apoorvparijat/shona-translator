#!/usr/bin/env python3
"""
Demonstration of Smart Caching System for Shona Translator
"""

import sys
import os
import time

# Add translators directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'translators'))

from translation_cache import TranslationCache
from base_translator import BaseShonaTranslator

class DemoTranslator(BaseShonaTranslator):
    """Demo translator for showcasing smart caching"""
    
    def _translate_with_api(self, text: str):
        """Simulate API translation with delay"""
        # Simulate API delay
        time.sleep(0.1)
        
        # Simple mock translations
        translations = {
            "Hello world": "Mhoro nyika",
            "Good morning": "Mangwanani akanaka",
            "How are you": "Makadii",
            "Thank you": "Tinotenda",
            "Welcome": "Tigashirei"
        }
        
        return translations.get(text, None)
    
    def _get_rate_limit_delay(self):
        return 0.0

def demo_smart_caching():
    """Demonstrate the smart caching system"""
    print("🚀 Smart Caching System Demo")
    print("=" * 50)
    
    # Create cache and translator
    cache = TranslationCache("demo_cache.json")
    cache.clear_cache()  # Start fresh
    
    with patch('base_translator.get_translation_cache', return_value=cache):
        translator = DemoTranslator()
    
    test_texts = [
        "Hello world",
        "Good morning", 
        "How are you",
        "Thank you",
        "Welcome"
    ]
    
    print("\n📊 Initial Cache Stats:")
    stats = cache.get_cache_stats()
    print(f"   Total entries: {stats['total_entries']}")
    print(f"   Hit rate: {stats['hit_rate']}%")
    
    print("\n🔄 First Translation Pass (API calls):")
    print("-" * 40)
    
    for i, text in enumerate(test_texts, 1):
        start_time = time.time()
        result = translator.get_best_translation(text)
        end_time = time.time()
        
        print(f"{i}. '{text}' -> '{result}' ({(end_time - start_time)*1000:.1f}ms)")
    
    print("\n📊 Cache Stats After First Pass:")
    stats = cache.get_cache_stats()
    print(f"   Total entries: {stats['total_entries']}")
    print(f"   Hit rate: {stats['hit_rate']}%")
    print(f"   Hits: {stats['hits']}, Misses: {stats['misses']}")
    
    print("\n🔄 Second Translation Pass (Cache hits):")
    print("-" * 40)
    
    for i, text in enumerate(test_texts, 1):
        start_time = time.time()
        result = translator.get_best_translation(text)
        end_time = time.time()
        
        print(f"{i}. '{text}' -> '{result}' ({(end_time - start_time)*1000:.1f}ms)")
    
    print("\n📊 Final Cache Stats:")
    stats = cache.get_cache_stats()
    print(f"   Total entries: {stats['total_entries']}")
    print(f"   Hit rate: {stats['hit_rate']}%")
    print(f"   Hits: {stats['hits']}, Misses: {stats['misses']}")
    
    print("\n🔍 Cache Contents:")
    print("-" * 40)
    for text in test_texts:
        cached_result = cache.get(text)
        if cached_result:
            print(f"   '{text}' -> '{cached_result}'")
    
    print("\n✨ Benefits of Smart Caching:")
    print("-" * 40)
    print("✅ Faster subsequent translations")
    print("✅ Reduced API calls and costs")
    print("✅ Consistent translations across providers")
    print("✅ Persistent cache between sessions")
    print("✅ Automatic cache key normalization")
    
    # Clean up
    if os.path.exists("demo_cache.json"):
        os.unlink("demo_cache.json")

if __name__ == "__main__":
    from unittest.mock import patch
    demo_smart_caching()
