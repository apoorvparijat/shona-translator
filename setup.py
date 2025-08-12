#!/usr/bin/env python3
"""
Setup script for Shona Translator
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        env_content = """# Optional: OpenAI API Key for enhanced translation quality
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Note: Google Translate is used as the primary service and doesn't require an API key
# OpenAI is optional but provides better context-aware translations"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file - you can optionally add your OpenAI API key")
    else:
        print("ℹ️  .env file already exists")

def main():
    print("🚀 Setting up Shona Translator...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Create .env file
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. (Optional) Edit .env file to add your OpenAI API key for better translations")
    print("2. Run: python shona_translator.py")
    print("3. Your translated document will be saved as 'collection-tools_shona.docx'")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)