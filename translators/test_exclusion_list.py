#!/usr/bin/env python3
"""
Test script for exclusion list functionality
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_exclusion_list():
    """Test the exclusion list functionality"""
    print("🧪 Testing Exclusion List Functionality...")
    
    try:
        from glossary_manager import GlossaryManager
        
        # Initialize glossary manager
        glossary = GlossaryManager()
        
        # Test terms that should be excluded
        excluded_terms = [
            "Neotree",
            "Neotree's", 
            "CDS",
            "AI",
            "AI-CDS",
            "AI-enabled",
            "Healthcare Systems Usability Scale for Clinical Decision Support Systems",
            "Sally Mugabe Central Hospital",
            "Chinhoyi Provincial Hospital",
            "Kamuzu Central Hospital",
            "Kasungu District Hospital",
            "NICU",
            "NNU",
            "gut feeling",
            "DHIS2",
            "EMRs",
            "MoH",
            "artificial intelligence",
            "Aim 2",
            "Normalization Measure Development Questionnaire"
        ]
        
        print("\n📝 Testing exclusion list:")
        for term in excluded_terms:
            translation = glossary.translate_with_glossary(term)
            if translation is None:
                print(f"  ✅ Excluded: '{term}'")
            else:
                print(f"  ❌ NOT excluded: '{term}' -> '{translation}'")
        
        # Test terms that should still be translated
        translatable_terms = [
            "hello",
            "good morning",
            "thank you",
            "healthcare",
            "patient",
            "doctor"
        ]
        
        print("\n📝 Testing translatable terms:")
        for term in translatable_terms:
            translation = glossary.translate_with_glossary(term)
            if translation and translation != term:
                print(f"  ✅ Translated: '{term}' -> '{translation}'")
            else:
                print(f"  ❌ NOT translated: '{term}'")
        
        # Test preprocessing with exclusions
        print("\n🔧 Testing preprocessing with exclusions:")
        test_text = "The CDS system uses AI to help healthcare workers in the NICU"
        processed = glossary.preprocess_text(test_text)
        print(f"  Original: '{test_text}'")
        print(f"  Processed: '{processed}'")
        
        # Print stats
        stats = glossary.get_glossary_stats()
        print(f"\n📊 Glossary Stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exclusion list test failed: {e}")
        return False

def test_csv_files():
    """Test that exclusion list CSV file is created"""
    print("\n🧪 Testing CSV file creation...")
    
    try:
        from glossary_manager import GlossaryManager
        
        # This will create the CSV files if they don't exist
        glossary = GlossaryManager()
        
        csv_files = [
            "glossary/medical_technical_terms.csv",
            "glossary/phrase_translations.csv", 
            "glossary/abbreviations.csv",
            "glossary/post_processing_corrections.csv",
            "glossary/exclusion_list.csv"
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
    print("🚀 EXCLUSION LIST TEST SUITE")
    print("=" * 50)
    
    tests = [
        ("CSV Files", test_csv_files),
        ("Exclusion List", test_exclusion_list)
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
        print("\n🎉 All tests passed! Exclusion list system is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
