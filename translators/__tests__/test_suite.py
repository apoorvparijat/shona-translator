#!/usr/bin/env python3
"""
Comprehensive test suite for the Shona Translator project
Runs all tests using the standard Python unittest framework
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from test_glossary_manager import TestGlossaryManager
from test_base_translator import TestBaseShonaTranslator
from test_mymemory_translator import TestMyMemoryShonaTranslator
from test_google_translator import TestGoogleShonaTranslator
from test_openai_translator import TestOpenAIShonaTranslator


def create_test_suite():
    """Create and return a test suite with all test cases"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestGlossaryManager))
    test_suite.addTest(unittest.makeSuite(TestBaseShonaTranslator))
    test_suite.addTest(unittest.makeSuite(TestMyMemoryShonaTranslator))
    test_suite.addTest(unittest.makeSuite(TestGoogleShonaTranslator))
    test_suite.addTest(unittest.makeSuite(TestOpenAIShonaTranslator))
    
    return test_suite


def run_tests():
    """Run all tests and return the result"""
    # Create test suite
    suite = create_test_suite()
    
    # Create test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("🧪 SHONA TRANSLATOR TEST SUITE")
    print("=" * 50)
    
    # Run all tests
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n❌ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed! Shona Translator is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)
