#!/usr/bin/env python3
"""
Test script to demonstrate AgentTranslator caching functionality
"""

import sys
import os
import time

# Add translators directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'translators'))

from agent_translator import AgentShonaTranslator

def test_agent_caching():
    """Test that AgentTranslator properly uses caching"""
    
    print("🧪 Testing AgentTranslator Caching")
    print("=" * 50)
    
    try:
        # Initialize the translator
        translator = AgentShonaTranslator()
        
        # Test text
        test_text = "Hello, how are you today?"
        
        print(f"📝 Test text: '{test_text}'")
        print()
        
        # First translation (should hit API)
        print("🔄 First translation (should hit API)...")
        start_time = time.time()
        translation1 = translator.get_best_translation(test_text)
        api_time = time.time() - start_time
        print(f"⏱️  API time: {api_time:.2f}s")
        print(f"📄 Translation: '{translation1}'")
        print()
        
        # Second translation (should hit cache)
        print("🔄 Second translation (should hit cache)...")
        start_time = time.time()
        translation2 = translator.get_best_translation(test_text)
        cache_time = time.time() - start_time
        print(f"⏱️  Cache time: {cache_time:.2f}s")
        print(f"📄 Translation: '{translation2}'")
        print()
        
        # Verify translations are the same
        if translation1 == translation2:
            print("✅ Caching working correctly - translations match!")
        else:
            print("❌ Caching issue - translations don't match!")
        
        # Show cache speed improvement
        if api_time > 0 and cache_time > 0:
            speedup = api_time / cache_time
            print(f"🚀 Cache is {speedup:.1f}x faster than API")
        
        # Show cache stats
        cache_stats = translator.cache.get_stats()
        print(f"📊 Cache stats: {cache_stats['hits']} hits, {cache_stats['misses']} misses")
        print(f"📊 Hit rate: {cache_stats['hit_rate']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_agent_caching()
    sys.exit(0 if success else 1)
