#!/usr/bin/env python3
"""
Test script for shared glossary functionality across all translators
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_glossary_manager():
    """Test the glossary manager directly"""
    print("🧪 Testing GlossaryManager...")
    
    try:
        from glossary_manager import GlossaryManager
        
        # Initialize glossary manager
        glossary = GlossaryManager()
        
        # Test preprocessing
        test_text = "HCW CDS AI NICU"
        processed = glossary.preprocess_text(test_text)
        print(f"Preprocessing: '{test_text}' -> '{processed}'")
        
        # Test glossary translation
        test_terms = [
            "version",
            "healthcare workers", 
            "clinical decision support",
            "what is your name"
        ]
        
        print("\n📝 Testing glossary translations:")
        for term in test_terms:
            translation = glossary.translate_with_glossary(term)
            print(f"  '{term}' -> '{translation}'")
        
        # Test post-processing
        test_corrections = [
            "mhando",
            "manzwiro",
            "kuongorora"
        ]
        
        print("\n🔧 Testing post-processing corrections:")
        for text in test_corrections:
            corrected = glossary.post_process_translation(text)
            print(f"  '{text}' -> '{corrected}'")
        
        # Print stats
        stats = glossary.get_glossary_stats()
        print(f"\n📊 Glossary Stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ GlossaryManager test failed: {e}")
        return False

def test_translators():
    """Test all three translators"""
    print("\n🧪 Testing all translators...")
    
    test_phrases = [
        "Version 1.0",
        "Healthcare workers",
        "Clinical decision support system",
        "What is your name?",
        "Thank you very much"
    ]
    
    translators = []
    
    # Test MyMemory translator
    try:
        from mymemory_translator import MyMemoryShonaTranslator
        mymemory = MyMemoryShonaTranslator()
        translators.append(("MyMemory", mymemory))
        print("✅ MyMemory translator initialized")
    except Exception as e:
        print(f"❌ MyMemory translator failed: {e}")
    
    # Test Google translator
    try:
        from google_translator import GoogleShonaTranslator
        google = GoogleShonaTranslator()
        translators.append(("Google", google))
        print("✅ Google translator initialized")
    except Exception as e:
        print(f"❌ Google translator failed: {e}")
    
    # Test OpenAI translator
    try:
        from openai_translator import OpenAIShonaTranslator
        openai = OpenAIShonaTranslator()
        translators.append(("OpenAI", openai))
        print("✅ OpenAI translator initialized")
    except Exception as e:
        print(f"❌ OpenAI translator failed: {e}")
    
    if not translators:
        print("❌ No translators could be initialized")
        return False
    
    # Test translations
    print(f"\n📝 Testing translations with {len(translators)} translator(s):")
    print("=" * 80)
    
    for phrase in test_phrases:
        print(f"\n🔤 Original: '{phrase}'")
        for name, translator in translators:
            try:
                translation = translator.get_best_translation(phrase)
                print(f"  {name:8}: '{translation}'")
            except Exception as e:
                print(f"  {name:8}: ERROR - {e}")
    
    # Print translator info
    print(f"\n📊 Translator Information:")
    print("=" * 80)
    for name, translator in translators:
        try:
            info = translator.get_translator_info()
            print(f"\n{name}:")
            print(f"  Type: {info['translator_type']}")
            print(f"  Rate limit delay: {info['rate_limit_delay']}s")
            print(f"  Glossary stats: {info['glossary_stats']}")
        except Exception as e:
            print(f"  {name}: ERROR getting info - {e}")
    
    return True

def test_csv_files():
    """Test that CSV files are created and readable"""
    print("\n🧪 Testing CSV file creation...")
    
    try:
        from glossary_manager import GlossaryManager
        
        # This will create the CSV files if they don't exist
        glossary = GlossaryManager()
        
        csv_files = [
            "glossary/medical_technical_terms.csv",
            "glossary/phrase_translations.csv", 
            "glossary/abbreviations.csv",
            "glossary/post_processing_corrections.csv"
        ]
        
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                size = os.path.getsize(csv_file)
                print(f"✅ {csv_file} exists ({size} bytes)")
            else:
                print(f"❌ {csv_file} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ CSV file test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 SHARED GLOSSARY TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("CSV Files", test_csv_files),
        ("Glossary Manager", test_glossary_manager),
        ("All Translators", test_translators)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Shared glossary system is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
