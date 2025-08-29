#!/usr/bin/env python3
"""
Story Generation Center - Main Interface
Provides easy access to all story generation features
"""

import os
from generators.story_generator import StoryGenerator
from generators.story_intent_config import StoryIntentConfigurator

class StoryGenerationCenter:
    def __init__(self):
        # Initialize directories
        self.blueprint_folder = "blueprints"
        self.storyboard_folder = "storyboards" 
        self.stories_folder = "stories"
        
        # Initialize story intent configurator
        self.story_intent_config = StoryIntentConfigurator()
        
        # Default LLM settings for STORY GENERATION (not blueprint creation)
        self.llm_settings = {
            'model': 'llama2',
            'temperature': 0.7,
            'max_tokens': 4000,      # ✅ Controls scene length
            'scene_tokens': 4000,    # ✅ Specific setting for scenes
            'bible_tokens': 6000,    # ✅ Specific setting for story bible
            'plan_tokens': 3000,     # ✅ Specific setting for scene plan
            'system_prompts': {
                'story_bible': 'You are a professional story developer...',
                'scene_plan': 'You are an expert at breaking stories into scenes...',
                'scene_writing': 'You are a skilled creative writer...'
            }
        }
    
    def run(self):
        """Main menu loop"""
        while True:
            self.show_main_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.configure_story_intent()
            elif choice == '2':
                self.generate_story()
            elif choice == '3':
                self.view_blueprints()
            elif choice == '4':
                self.view_generated_stories()
            elif choice == '5':
                self.settings_menu()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def show_main_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🎬 STORY GENERATION CENTER")
        print("="*60)
        
        # Show current story intent status
        if self.story_intent_config.configured_intent:
            intent_summary = self.story_intent_config.get_intent_summary()
            print(f"📝 Story Intent: {intent_summary[:50]}...")
        else:
            print("📝 Story Intent: Not configured")
        
        print("\nOptions:")
        print("1. 🎯 Configure Story Intent (Narrative Style, Goals, etc.)")
        print("2. 🎬 Generate Story")
        print("3. 📋 View Available Blueprints")
        print("4. 📚 View Generated Stories")
        print("5. ⚙️  Settings")
        print("6. 🚪 Exit")
    
    def configure_story_intent(self):
        """Configure story intent using the dedicated interface"""
        self.story_intent_config.configure_from_menu()
    
    def generate_story(self):
        """Generate a story using current configuration"""
        # Check if we have blueprints
        if not os.path.exists(self.blueprint_folder):
            print("❌ No blueprints folder found. Please create blueprints first.")
            return
        
        blueprints = [f for f in os.listdir(self.blueprint_folder) if f.endswith('.txt')]
        if not blueprints:
            print("❌ No blueprint files found. Please add some blueprints first.")
            return
        
        # Select blueprint
        print("\n📋 AVAILABLE BLUEPRINTS:")
        for i, blueprint in enumerate(blueprints, 1):
            print(f"{i}. {blueprint}")
        
        try:
            choice = int(input(f"\nSelect blueprint (1-{len(blueprints)}): ").strip())
            if 1 <= choice <= len(blueprints):
                selected_blueprint = blueprints[choice - 1]
                
                # Create story generator with current intent configuration
                generator = StoryGenerator(
                    blueprint_folder=self.blueprint_folder,
                    storyboard_folder=self.storyboard_folder,
                    stories_folder=self.stories_folder,
                    llm_settings=self.llm_settings,
                    story_intent=self.story_intent_config
                )
                
                # Generate the story
                print(f"\n🎬 Generating story from: {selected_blueprint}")
                story_filename, context_tracker = generator.generate_complete_story(selected_blueprint)
                
                if story_filename:
                    print(f"✅ Story generated successfully: {story_filename}")
                else:
                    print("❌ Story generation failed")
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a number.")
    
    def view_blueprints(self):
        """View available blueprints"""
        if not os.path.exists(self.blueprint_folder):
            print("❌ No blueprints folder found.")
            return
        
        blueprints = [f for f in os.listdir(self.blueprint_folder) if f.endswith('.txt')]
        if not blueprints:
            print("❌ No blueprint files found.")
            return
        
        print(f"\n📋 BLUEPRINTS IN {self.blueprint_folder}/:")
        for blueprint in blueprints:
            print(f"   📄 {blueprint}")
    
    def view_generated_stories(self):
        """View generated stories"""
        if not os.path.exists(self.stories_folder):
            print("❌ No stories folder found.")
            return
        
        stories = [f for f in os.listdir(self.stories_folder) if f.endswith('.txt')]
        if not stories:
            print("❌ No generated stories found.")
            return
        
        print(f"\n📚 GENERATED STORIES IN {self.stories_folder}/:")
        for story in sorted(stories, reverse=True):  # Most recent first
            print(f"   📖 {story}")
    
    def settings_menu(self):
        """Settings and configuration menu"""
        while True:
            print("\n⚙️ SETTINGS MENU")
            print("-" * 30)
            print("1. Change Ollama Model")
            print("2. Adjust Temperature")
            print("3. Set Scene Length (tokens)")
            print("4. Set Story Bible Length (tokens)")  
            print("5. Set Scene Plan Length (tokens)")
            print("6. View Current Settings")
            print("7. Back to Main Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                new_model = input(f"Current model: {self.llm_settings['model']}\nEnter new model: ").strip()
                if new_model:
                    self.llm_settings['model'] = new_model
                    print(f"✅ Model changed to: {new_model}")
            elif choice == '2':
                try:
                    new_temp = float(input(f"Current temperature: {self.llm_settings['temperature']}\nEnter new temperature (0.0-1.0): ").strip())
                    if 0.0 <= new_temp <= 1.0:
                        self.llm_settings['temperature'] = new_temp
                        print(f"✅ Temperature changed to: {new_temp}")
                    else:
                        print("❌ Temperature must be between 0.0 and 1.0")
                except ValueError:
                    print("❌ Please enter a valid number")
            elif choice == '3':
                self._set_scene_tokens()
            elif choice == '4':
                self._set_bible_tokens()
            elif choice == '5':
                self._set_plan_tokens()
            elif choice == '6':
                self._show_detailed_settings()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice")

    def _set_scene_tokens(self):
        """Set tokens for scene generation"""
        print(f"\nCurrent scene token limit: {self.llm_settings['scene_tokens']:,}")
        print("This controls how long each individual scene will be.")
        print("\nRecommended values:")
        print("• 1,000-2,000 tokens = Short scenes (~750-1,500 words)")
        print("• 3,000-4,000 tokens = Medium scenes (~2,250-3,000 words)")
        print("• 5,000-8,000 tokens = Long scenes (~3,750-6,000 words)")
        print("• 10,000+ tokens = Very long scenes (6,000+ words)")
        
        try:
            new_tokens = int(input("Enter scene token limit (1000-32000): ").strip())
            if 1000 <= new_tokens <= 32000:
                self.llm_settings['scene_tokens'] = new_tokens
                self.llm_settings['max_tokens'] = new_tokens  # Update main setting too
                print(f"✅ Scene tokens set to: {new_tokens:,}")
                print(f"   Expected scene length: ~{new_tokens * 0.75:.0f} words")
            else:
                print("❌ Token count must be between 1,000 and 32,000")
        except ValueError:
            print("❌ Please enter a valid number")

    def _set_bible_tokens(self):
        """Set tokens for story bible generation"""
        print(f"\nCurrent story bible token limit: {self.llm_settings['bible_tokens']:,}")
        try:
            new_tokens = int(input("Enter bible token limit (2000-16000): ").strip())
            if 2000 <= new_tokens <= 16000:
                self.llm_settings['bible_tokens'] = new_tokens
                print(f"✅ Bible tokens set to: {new_tokens:,}")
            else:
                print("❌ Token count must be between 2,000 and 16,000")
        except ValueError:
            print("❌ Please enter a valid number")

    def _set_plan_tokens(self):
        """Set tokens for scene plan generation"""
        print(f"\nCurrent scene plan token limit: {self.llm_settings['plan_tokens']:,}")
        try:
            new_tokens = int(input("Enter plan token limit (1500-8000): ").strip())
            if 1500 <= new_tokens <= 8000:
                self.llm_settings['plan_tokens'] = new_tokens
                print(f"✅ Plan tokens set to: {new_tokens:,}")
            else:
                print("❌ Token count must be between 1,500 and 8,000")
        except ValueError:
            print("❌ Please enter a valid number")

    def _show_detailed_settings(self):
        """Show all current settings"""
        print(f"\n📊 CURRENT SETTINGS:")
        print(f"Model: {self.llm_settings['model']}")
        print(f"Temperature: {self.llm_settings['temperature']}")
        print(f"Scene Length: {self.llm_settings['scene_tokens']:,} tokens (~{self.llm_settings['scene_tokens'] * 0.75:.0f} words)")
        print(f"Story Bible Length: {self.llm_settings['bible_tokens']:,} tokens")
        print(f"Scene Plan Length: {self.llm_settings['plan_tokens']:,} tokens")

if __name__ == "__main__":
    center = StoryGenerationCenter()
    center.run()
