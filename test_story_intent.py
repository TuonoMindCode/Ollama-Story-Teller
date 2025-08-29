#!/usr/bin/env python3
"""
Test the Story Intent Configuration System
"""

from generators.story_intent_config import StoryIntentConfigurator

def test_story_intent():
    """Test the story intent configuration"""
    print("🎯 Testing Story Intent Configuration")
    print("="*50)
    
    # Create configurator
    configurator = StoryIntentConfigurator()
    
    # Show the menu
    configurator.configure_from_menu()
    
    # Show what was configured
    if configurator.configured_intent:
        print("\n✅ FINAL CONFIGURATION:")
        print("="*40)
        for category, value in configurator.configured_intent.items():
            label = configurator.STORY_INTENT_OPTIONS[category]['label']
            print(f"📝 {label}:")
            print(f"   {value}")
            print()
    else:
        print("\n⚠️  No configuration was set")

if __name__ == "__main__":
    test_story_intent()
