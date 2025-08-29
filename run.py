#!/usr/bin/env python3
"""
Simple launcher for the Story Generator
Double-click this file or run: python run.py
"""
import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        input("Press Enter to exit...")
        sys.exit(1)

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import requests
        print("✅ Dependencies check passed")
        return True
    except ImportError:
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("💡 Try running: pip install -r requirements.txt")
            input("Press Enter to exit...")
            return False

def main():
    """Main launcher function"""
    print("🚀 Starting AI Story Generator...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Import and run the main application
    try:
        from story_app import StoryApp
        app = StoryApp()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()