"""
Setup Script for ChatGPT Voice Assistant
Creates necessary directories and validates environment
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Create necessary project directories."""
    directories = [
        "models",
        "logs",
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created: {directory}/")
        else:
            print(f"  → Exists: {directory}/")


def check_env_file():
    """Check if .env file exists."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    print("\nChecking environment configuration...")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("  ⚠ .env file not found")
            print("  → Copy .env.example to .env and add your API keys:")
            print("     cp .env.example .env")
        else:
            print("  ✗ Neither .env nor .env.example found")
        return False
    else:
        print("  ✓ .env file exists")
        return True


def check_wake_word_model():
    """Check if wake word model exists."""
    model_path = Path("models/Hey-ChatGPT_en_windows_v3_0_0.ppn")
    
    print("\nChecking wake word model...")
    
    if not model_path.exists():
        print("  ⚠ Wake word model not found")
        print("  → Download from Picovoice Console:")
        print("     1. Go to https://console.picovoice.ai/")
        print("     2. Create wake word 'Hey ChatGPT'")
        print("     3. Download .ppn file for your platform")
        print(f"     4. Place in: {model_path}")
        return False
    else:
        print(f"  ✓ Wake word model found: {model_path}")
        return True


def check_python_version():
    """Verify Python version."""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro}")
        print("  → Python 3.10 or higher required")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    
    required_packages = [
        "openai",
        "pvporcupine",
        "faster_whisper",
        "pyaudio",
        "pyttsx3",
        "numpy",
        "dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n  → Install missing packages:")
        print("     pip install -r requirements.txt")
        return False
    
    return True


def display_next_steps(checks_passed):
    """Display next steps based on validation results."""
    print("\n" + "="*60)
    
    if checks_passed:
        print("✅ Setup Complete! Ready to run.")
        print("="*60)
        print("\nNext steps:")
        print("  1. Ensure your API keys are set in .env")
        print("  2. Run the assistant:")
        print("     python assistant.py")
        print("\nTest individual components:")
        print("  • Wake Word: python wakeword.py")
        print("  • Speech-to-Text: python stt.py")
        print("  • ChatGPT API: python chatgpt_api.py")
        print("  • Text-to-Speech: python tts.py")
    else:
        print("⚠️  Setup Incomplete - Action Required")
        print("="*60)
        print("\nPlease complete the steps above before running the assistant.")
        print("Run this script again to verify: python setup.py")
    
    print("="*60)


def main():
    """Main setup routine."""
    print("\n" + "="*60)
    print("🤖 ChatGPT Voice Assistant - Setup")
    print("="*60)
    print()
    
    # Run all checks
    checks = {
        "python_version": check_python_version(),
        "directories": True,  # Always succeeds (creates dirs)
        "env_file": check_env_file(),
        "wake_word_model": check_wake_word_model(),
        "dependencies": check_dependencies()
    }
    
    # Create directories
    create_directory_structure()
    
    # Determine if all critical checks passed
    critical_checks = ["python_version", "env_file", "dependencies"]
    all_passed = all(checks[key] for key in critical_checks)
    
    # Display results
    display_next_steps(all_passed)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())