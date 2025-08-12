#!/usr/bin/env python3
"""
Simple test runner for Shona Translator using Python's built-in unittest discovery
"""

import unittest
import sys
import os

def run_tests():
    """Run all tests using unittest discovery"""
    # Add the current directory to Python path so imports work
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Discover and run all tests in the __tests__ directory
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), '__tests__')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

if __name__ == '__main__':
    print("🧪 SHONA TRANSLATOR TESTS")
    print("=" * 40)
    
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 40)
    print("📋 SUMMARY")
    print("=" * 40)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed.")
        sys.exit(1)
