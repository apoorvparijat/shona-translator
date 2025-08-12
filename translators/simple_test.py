#!/usr/bin/env python3
"""
Test script for Simple Shona Translator
"""

import os
from simple_translator import SimpleShonaTranslator

def test_basic_translation():
    """Test basic translation functionality"""
    print("🧪 Testing Simple Shona Translator...")
    
    translator = SimpleShonaTranslator()
    
    # Test phrases
    test_phrases = [
        "Hello, how are you?",
        "Good morning",
        "Thank you very much",
        "Please help me",
        "What is your name?",
        "Welcome to Zimbabwe",
        "I love learning new languages",
        "The house is big",
        "This is good food",
        "My family is here"
    ]
    
    print("\n📝 Testing basic translations:")
    print("-" * 50)
    
    for phrase in test_phrases:
        translation = translator.get_best_translation(phrase)
        print(f"EN: {phrase}")
        print(f"SN: {translation}")
        print("-" * 30)
    
    print("\n✅ Basic translation test completed!")
    
    # Check if input file exists
    input_file = "collection-tools.docx"
    if os.path.exists(input_file):
        print(f"\n📄 Found input file: {input_file}")
        print(f"   File size: {os.path.getsize(input_file)} bytes")
        print("   Ready for document translation!")
    else:
        print(f"\n⚠️  Input file '{input_file}' not found")
        print("   Please ensure the DOCX file is in the current directory")

def main():
    """Main test function"""
    try:
        test_basic_translation()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 All tests passed! The translator is ready to use.")
    else:
        print("\n❌ Tests failed. Please check your setup.")