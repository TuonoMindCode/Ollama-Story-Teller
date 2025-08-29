#!/usr/bin/env python3
"""
AI Story Generator - Main Entry Point
Run this file to start the application
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the application"""
    try:
        from story_app import StoryApp
        
        print("=" * 60)
        print("🎭 AI STORY GENERATOR")
        print("=" * 60)
        print("Starting application...")
        
        app = StoryApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("📦 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("📧 Please report this issue if it persists")
        sys.exit(1)

if __name__ == "__main__":
    main()