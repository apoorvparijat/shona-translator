#!/usr/bin/env python3
"""
Fix googletrans dependency conflicts
"""

import subprocess
import sys

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔧 Fixing googletrans dependency conflicts...")
    print("=" * 50)
    
    # Step 1: Check current installation
    print("1. Checking current googletrans installation...")
    success, stdout, stderr = run_command("pip show googletrans")
    if success:
        print("   ✅ googletrans is installed")
        print(f"   Version info: {stdout.strip()}")
    else:
        print("   ❌ googletrans not found")
    
    # Step 2: Uninstall current version
    print("\n2. Uninstalling current googletrans...")
    success, stdout, stderr = run_command("pip uninstall googletrans -y")
    if success:
        print("   ✅ googletrans uninstalled")
    else:
        print("   ⚠️  Could not uninstall (may not be installed)")
    
    # Step 3: Install correct version
    print("\n3. Installing Google Translate requirements...")
    success, stdout, stderr = run_command("pip install -r requirements-google.txt")
    if success:
        print("   ✅ Google Translate requirements installed successfully")
    else:
        print("   ❌ Failed to install Google Translate requirements")
        print(f"   Error: {stderr}")
        return False
    
    # Step 4: Test the installation
    print("\n4. Testing googletrans installation...")
    test_code = """
import googletrans
from googletrans import Translator
translator = Translator()
result = translator.translate("hello", src='en', dest='es')
print(f"Test translation: {result.text}")
"""
    
    success, stdout, stderr = run_command(f'python3 -c "{test_code}"')
    if success:
        print("   ✅ googletrans working correctly!")
        print(f"   Test result: {stdout.strip()}")
    else:
        print("   ❌ googletrans test failed")
        print(f"   Error: {stderr}")
        return False
    
    print("\n🎉 googletrans dependency conflict fixed!")
    print("You can now use the Google Translate translator.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
