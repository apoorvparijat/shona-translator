#!/usr/bin/env python3
"""
Test script to demonstrate improved AgentTranslator functionality
"""

import sys
import os
import time

# Add translators directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'translators'))

from agent_translator import AgentShonaTranslator

def test_agent_improvements():
    """Test the improved AgentTranslator features"""
    
    print("🧪 Testing Improved AgentTranslator")
    print("=" * 50)
    
    try:
        # Initialize the translator
        translator = AgentShonaTranslator()
        
        # Test 1: Basic translation (should use system prompt for glossary)
        print("📝 Test 1: Basic translation with glossary terms")
        test_text1 = "The patient was admitted to NICU for treatment"
        print(f"Input: '{test_text1}'")
        
        start_time = time.time()
        translation1 = translator.get_best_translation(test_text1)
        translation_time = time.time() - start_time
        
        print(f"Output: '{translation1}'")
        print(f"Time: {translation_time:.2f}s")
        print()
        
        # Test 2: Large text chunking
        print("📝 Test 2: Large text chunking")
        test_text2 = """
        The healthcare workers at the hospital conducted a comprehensive study on clinical decision support systems. 
        The research methodology involved interviews with medical professionals and analysis of patient data. 
        The findings showed that artificial intelligence can significantly improve healthcare outcomes. 
        The study concluded that CDS systems should be implemented across all medical facilities.
        """
        print(f"Input length: {len(test_text2)} characters")
        
        start_time = time.time()
        translation2 = translator.translate_large_text(test_text2)
        chunk_time = time.time() - start_time
        
        print(f"Output: '{translation2[:100]}...'")
        print(f"Time: {chunk_time:.2f}s")
        print()
        
        # Test 3: Exclusion list respect
        print("📝 Test 3: Exclusion list respect")
        test_text3 = "The neotree system and dhis2 platform are used in healthcare"
        print(f"Input: '{test_text3}'")
        
        translation3 = translator.get_best_translation(test_text3)
        print(f"Output: '{translation3}'")
        print()
        
        # Test 4: Abbreviation expansion
        print("📝 Test 4: Abbreviation expansion")
        test_text4 = "The AI system provides CDS support for healthcare workers"
        print(f"Input: '{test_text4}'")
        
        translation4 = translator.get_best_translation(test_text4)
        print(f"Output: '{translation4}'")
        print()
        
        # Test 5: Cache performance
        print("📝 Test 5: Cache performance")
        print("First translation (should hit API)...")
        start_time = time.time()
        cache_test1 = translator.get_best_translation("Hello, how are you?")
        api_time = time.time() - start_time
        print(f"API time: {api_time:.2f}s")
        
        print("Second translation (should hit cache)...")
        start_time = time.time()
        cache_test2 = translator.get_best_translation("Hello, how are you?")
        cache_time = time.time() - start_time
        print(f"Cache time: {cache_time:.2f}s")
        
        if cache_test1 == cache_test2:
            print("✅ Cache working correctly")
        else:
            print("❌ Cache issue detected")
        
        if api_time > 0 and cache_time > 0:
            speedup = api_time / cache_time
            print(f"🚀 Cache is {speedup:.1f}x faster than API")
        
        print()
        
        # Show system prompt info
        print("📋 System Prompt Information:")
        print(f"- Exclusion terms loaded: {len(translator.exclusion_terms)}")
        print(f"- Abbreviations loaded: {len(translator.abbreviations)}")
        print(f"- Medical terms loaded: {len(translator.medical_terms)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agent_improvements()
    sys.exit(0 if success else 1)
