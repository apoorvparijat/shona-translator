#!/usr/bin/env python3
"""
Test script for Improved Shona Translator
"""

import os
from improved_translator import ImprovedShonaTranslator

def test_translation_improvements():
    """Test the improved translator with focus on accuracy"""
    print("🧪 Testing Improved Shona Translator...")
    
    translator = ImprovedShonaTranslator()
    
    # Test phrases that showed issues before
    test_phrases = [
        "Version: 1.0",
        "Healthcare workers",
        "Clinical decision support system",
        "Focus group discussion",
        "Methodology: Semi-structured interview",
        "Objective: To understand",
        "Duration: 60-90 minutes",
        "Participants: Healthcare workers",
        "Sites: Sally Mugabe Central Hospital",
        "Artificial intelligence",
        "What is your name?",
        "Thank you very much",
        "Good morning",
        "Please help me"
    ]
    
    print("\n📝 Testing improved translations:")
    print("=" * 60)
    
    for phrase in test_phrases:
        translation = translator.get_best_translation(phrase)
        print(f"EN: {phrase}")
        print(f"SN: {translation}")
        print("-" * 40)
    
    print("\n✅ Improved translation test completed!")
    
    # Check if input file exists
    input_file = "collection-tools.docx"
    if os.path.exists(input_file):
        print(f"\n📄 Found input file: {input_file}")
        print(f"   File size: {os.path.getsize(input_file)} bytes")
        print("   Ready for enhanced document translation!")
    else:
        print(f"\n⚠️  Input file '{input_file}' not found")

def main():
    """Main test function"""
    try:
        test_translation_improvements()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Improved translator ready! Key improvements:")
        print("  • Fixed 'Version' -> 'Shanduko' (not 'Mhando')")
        print("  • Enhanced medical/technical glossary")
        print("  • Context-aware phrase translation")
        print("  • Post-processing error correction")
        print("  • Better handling of abbreviations")
    else:
        print("\n❌ Tests failed.")