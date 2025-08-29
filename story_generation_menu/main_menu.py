import time
import glob
import os
from .blueprint_selector import BlueprintSelector
from .content_configurator import ContentConfigurator
from .scene_configurator import SceneConfigurator
from .consistency_configurator import ConsistencyConfigurator
from .variation_configurator import VariationConfigurator
from .story_generator_runner import StoryGeneratorRunner
# NEW: Import story intent configurator
from generators.story_intent_config import StoryIntentConfigurator
# Add import
from .language_configurator import LanguageConfigurator
from generators.perspective_controller import PerspectiveController

class StoryGenerationMenu:
    def __init__(self, app_instance):
        self.app = app_instance
        
        # Initialize all configurators
        self.blueprint_selector = BlueprintSelector(app_instance)
        self.content_configurator = ContentConfigurator()
        self.scene_configurator = SceneConfigurator()
        self.consistency_configurator = ConsistencyConfigurator()
        self.variation_configurator = VariationConfigurator()
        self.story_runner = StoryGeneratorRunner(app_instance)
        
        # NEW: Initialize story intent configurator
        self.story_intent_config = StoryIntentConfigurator()
        
        # Add story title setting
        self.custom_story_title = None  # None = auto-generate, string = custom title
        
        # NEW: Add language configurator
        self.language_configurator = LanguageConfigurator()
        
        # NEW: Add perspective controller
        from generators.perspective_controller import PerspectiveController
        self.perspective_controller = PerspectiveController()
        self.perspective_configured = False
        
        # Story generation specific settings
        self.selected_blueprint = None
        self.scene_control_mode = "auto"  # auto, manual
        self.num_scenes = "auto"  # auto, or number
        self.narrative_consistency = "auto_tracking"  # auto_tracking, basic, none
        self.story_variations = 1
        
        # Content and tone settings - NOW WITH CHARACTER COUNT
        self.content_rating = "auto"  # auto, family, teen, adult, custom:description
        self.story_tone = "auto"  # auto, comedy, light_comedy, romantic_comedy, etc.
        self.story_ending = "auto"  # auto, happy, dark, bittersweet, open, tragic
        self.character_count = "auto"  # NEW: auto, minimal, small_cast, large_cast
        
        # NEW: Add language settings
        self.profanity_level = "moderate"
        self.dialogue_intensity = "moderate" 
        self.speech_style = "casual"
        
        # FIX: Use the correct settings manager attribute name
        if hasattr(app_instance, 'settings'):
            self.settings_manager = app_instance.settings
        else:
            print("⚠️ No settings manager found, settings won't be saved")
            self.settings_manager = None
        
        # Auto-load story generation settings on startup if settings manager exists
        if self.settings_manager and hasattr(self.settings_manager, 'load_story_generation_settings'):
            self.settings_manager.load_story_generation_settings(self)
        elif self.settings_manager:
            # Try to load basic settings from the existing settings manager
            self._load_basic_settings()
    
    def display_story_generation_menu(self):
        """Display the story generation configuration menu"""
        print("\n" + "="*60)
        print("STORY GENERATION CENTER")
        print("="*60)
        
        # Display current settings
        blueprint_display = self.selected_blueprint or self.app.selected_blueprint or "None selected"
        
        # Story title display
        title_display = f'"{self.custom_story_title}"' if self.custom_story_title else "Auto-generate"
        
        scene_display = f"{self.scene_control_mode.title()} ({self.num_scenes} scenes)" if self.num_scenes != "auto" else f"{self.scene_control_mode.title()}"
        consistency_display = self.narrative_consistency.replace('_', ' ').title()
        
        # Format content settings display
        rating_display = self.content_configurator.get_rating_display(self.content_rating)
        tone_display = self.story_tone.replace('_', ' ').title() if self.story_tone != "auto" else "Auto (from blueprint)"
        ending_display = self.story_ending.replace('_', ' ').title() if self.story_ending != "auto" else "Auto (from blueprint)"
        character_display = self.character_count.replace('_', ' ').title() if self.character_count != "auto" else "Auto (from blueprint)"
        
        # NEW: Add language settings
        language_display = self.language_configurator.get_language_display(
            self.profanity_level, self.dialogue_intensity, self.speech_style)
        
        # Create clearer perspective display
        current_force_gender = self.app.settings.get("force_protagonist_gender", "auto")
        
        # Build display text
        perspective_parts = []
        
        # Add gender part
        if current_force_gender == "female":
            perspective_parts.append("Female protagonist")
        elif current_force_gender == "male":
            perspective_parts.append("Male protagonist")
        else:
            perspective_parts.append("Blueprint gender")
        
        # Add perspective part
        if hasattr(self, 'perspective_controller') and hasattr(self, 'perspective_configured') and self.perspective_configured:
            perspective = self.perspective_controller.selected_perspective
            if perspective == "love_interest":
                perspective_parts.append("Love interest POV")
            elif perspective == "role_reversal":
                perspective_parts.append("Antagonist POV")
            elif perspective == "alternating":
                perspective_parts.append("Alternating POV")
            elif perspective == "secondary_character":
                perspective_parts.append("Sidekick POV")
            else:
                perspective_parts.append("Original POV")
        else:
            perspective_parts.append("Original POV")
        
        perspective_display = " | ".join(perspective_parts)
        
        # Story intent display
        if self.story_intent_config.configured_intent:
            intent_summary = self.story_intent_config.get_intent_summary()
            intent_display = intent_summary[:50] + "..." if len(intent_summary) > 50 else intent_summary
        else:
            intent_display = "Not configured"
        
        print(f"1. Blueprint: {blueprint_display}")
        print(f"2. Story Title: {title_display}")
        print(f"3. Scene Control: {scene_display}")
        print(f"4. Narrative Consistency: {consistency_display}")
        print(f"5. Content Rating: {rating_display}")
        print(f"6. Story Tone: {tone_display}")
        print(f"7. Story Ending: {ending_display}")
        print(f"8. Character Count: {character_display}")
        print(f"9. Story Intent & Style: {intent_display}")
        print(f"10. Perspective & POV: {perspective_display}")  # This will now show gender swap
        print(f"11. Language & Dialogue: {language_display}")
        print(f"12. Story Variations: {self.story_variations}")
        print("13. Advanced LLM Settings")
        print("14. Generate Stories Now!")
        print("15. Back to Main Menu")
        print("-" * 60)
        
        # Enhanced LLM settings display
        model_display = self.app.selected_model or 'None selected'
        print(f"Model: {model_display}")
        print(f"Tokens: {self.app.max_tokens:,} | Temp: {self.app.temperature} | Top-p: {self.app.top_p} | Top-k: {self.app.top_k}")
        print(f"Repeat Penalty: {self.app.repeat_penalty} | Seed: {self.app.seed or 'Random'} | Auto-Audio: {'On' if self.app.auto_generate_audio else 'Off'}")
        
        # Add the model modes display line
        model_modes = self.app.get_model_mode_display()
        print(f"{model_modes}")
        
        print("\nSelect option (1-15): ", end="")  # Updated number
    
    def configure_perspective(self):
        """Configure perspective and POV options"""
        while True:
            print("\n🎭 PERSPECTIVE & POINT OF VIEW CONFIGURATION")
            print("="*60)
            
            # Show current settings
            current_force_gender = self.app.settings.get("force_protagonist_gender", "auto")
            force_display = {
                "auto": "Use blueprint as written",
                "female": "Female protagonist",
                "male": "Male protagonist"
            }
            
            current_perspective = "Default"
            if hasattr(self, 'perspective_controller'):
                perspective = getattr(self.perspective_controller, 'selected_perspective', 'default')
                if perspective == "default":
                    current_perspective = "Original blueprint perspective"
                elif perspective == "love_interest":
                    current_perspective = "Love interest POV"
                elif perspective == "role_reversal":
                    current_perspective = "Antagonist/villain POV"
                elif perspective == "alternating":
                    current_perspective = "Alternating between characters"
                elif perspective == "secondary_character":
                    current_perspective = "Witness/sidekick POV"
            
            print(f"📋 Current Settings:")
            print(f"   Character Gender: {force_display[current_force_gender]}")
            print(f"   Story Perspective: {current_perspective}")
            
            print("\n" + "="*60)
            print("🚻 CHARACTER GENDER (Who is the protagonist?)")
            print("="*60)
            print("1. Use blueprint as written")
            print("2. Force protagonist to be FEMALE")
            print("3. Force protagonist to be MALE")
            
            print("\n" + "="*60)
            print("👁️  STORY PERSPECTIVE (Whose viewpoint do we follow?)")
            print("="*60)
            print("4. Original blueprint perspective (follow main character)")
            print("5. Follow the love interest instead")
            print("6. Follow the antagonist/villain instead")
            print("7. Follow a witness/sidekick character")
            print("8. Alternate between multiple characters")
            
            print("\n" + "="*60)
            print("9. Back to story generation menu")
            
            try:
                choice = input("\nSelect option (1-9): ").strip()
                
                # CHARACTER GENDER OPTIONS
                if choice == "1":
                    self.app.settings.set("force_protagonist_gender", "auto")
                    print("✓ Will use blueprint's original character gender")
                    
                elif choice == "2":
                    self.app.settings.set("force_protagonist_gender", "female")
                    print("✓ Will force protagonist to be FEMALE")
                    
                elif choice == "3":
                    self.app.settings.set("force_protagonist_gender", "male")
                    print("✓ Will force protagonist to be MALE")
                
                # STORY PERSPECTIVE OPTIONS
                elif choice == "4":
                    if hasattr(self, 'perspective_controller'):
                        self.perspective_controller.selected_perspective = "default"
                        self.perspective_configured = True
                    print("✓ Will use original blueprint perspective (follow main character)")
                    
                elif choice == "5":
                    if hasattr(self, 'perspective_controller'):
                        self.perspective_controller.selected_perspective = "love_interest"
                        self.perspective_configured = True
                    print("✓ Will follow the love interest's perspective")
                    print("   Example: In romance, follow the person being pursued instead of the pursuer")
                    
                elif choice == "6":
                    if hasattr(self, 'perspective_controller'):
                        self.perspective_controller.selected_perspective = "role_reversal"
                        self.perspective_configured = True
                    print("✓ Will follow the antagonist/villain perspective")
                    print("   Example: Follow the killer instead of the detective, the rival instead of the hero")
                    
                elif choice == "7":
                    if hasattr(self, 'perspective_controller'):
                        self.perspective_controller.selected_perspective = "secondary_character"
                        self.perspective_configured = True
                    print("✓ Will follow a witness/sidekick perspective")
                    print("   Example: Follow the best friend watching the romance unfold")
                    
                elif choice == "8":
                    # For alternating, we might need blueprint analysis
                    if not self.selected_blueprint and not self.app.selected_blueprint:
                        print("❌ Please select a blueprint first for alternating perspective!")
                        input("Press Enter to continue...")
                        continue
                    
                    if hasattr(self, 'perspective_controller'):
                        self.perspective_controller.selected_perspective = "alternating"
                        self.perspective_configured = True
                        print("✓ Will alternate between multiple character perspectives")
                        print("   Example: Chapter 1 from hero POV, Chapter 2 from love interest POV, etc.")
                
                elif choice == "9":
                    break
                    
                else:
                    print("❌ Invalid option")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")
    
    def configure_story_intent(self):
        """Configure story intent and narrative style"""
        print("\n🎯 STORY INTENT & NARRATIVE STYLE")
        print("="*50)
        print("Configure the story's direction, goals, and writing style...")
        
        # Show quick menu for story intent
        self.story_intent_config.configure_from_menu()
        
        # Show summary of what was configured
        if self.story_intent_config.configured_intent:
            print("\n✅ Story intent configured successfully!")
            
            # Show key configured items
            for category, value in self.story_intent_config.configured_intent.items():
                label = self.story_intent_config.STORY_INTENT_OPTIONS[category]['label']
                if category == "custom_requirements":
                    print(f"📝 {label}: {len(value) if isinstance(value, list) else 1} requirement(s)")
                else:
                    short_value = value[:50] + "..." if len(value) > 50 else value
                    print(f"📝 {label}: {short_value}")
        else:
            print("\n⚠️ No story intent was configured")
        
        input("\nPress Enter to continue...")

    def _load_basic_settings(self):
        """Load basic settings from the existing settings manager"""
        try:
            if hasattr(self.settings_manager, 'get'):
                # Load any existing story generation settings
                self.story_variations = self.settings_manager.get('story_variations', 1)
                self.content_rating = self.settings_manager.get('content_rating', 'auto')
                self.story_tone = self.settings_manager.get('story_tone', 'auto')
                self.story_ending = self.settings_manager.get('story_ending', 'auto')
                self.character_count = self.settings_manager.get('character_count', 'auto')
                self.profanity_level = self.settings_manager.get('profanity_level', 'moderate')
                self.dialogue_intensity = self.settings_manager.get('dialogue_intensity', 'moderate')
                self.speech_style = self.settings_manager.get('speech_style', 'casual')
                self.scene_control_mode = self.settings_manager.get('scene_control_mode', 'auto')
                self.narrative_consistency = self.settings_manager.get('narrative_consistency', 'auto_tracking')
                print("💾 Basic story generation settings loaded")
        except Exception as e:
            print(f"⚠️ Could not load settings: {e}")
    
    def _save_basic_settings(self):
        """Save basic settings to the existing settings manager"""
        try:
            if hasattr(self.settings_manager, 'set'):
                # Save story generation settings to the main settings
                settings_to_save = {
                    'story_variations': self.story_variations,
                    'content_rating': self.content_rating,
                    'story_tone': self.story_tone,
                    'story_ending': self.story_ending,
                    'character_count': self.character_count,
                    'profanity_level': self.profanity_level,
                    'dialogue_intensity': self.dialogue_intensity,
                    'speech_style': self.speech_style,
                    'scene_control_mode': self.scene_control_mode,
                    'narrative_consistency': self.narrative_consistency
                }
                
                for key, value in settings_to_save.items():
                    self.settings_manager.set(key, value, save_immediately=False)
                
                # Save all at once
                if hasattr(self.settings_manager, 'save_settings'):
                    self.settings_manager.save_settings()
                    print("💾 Story generation settings saved")
        except Exception as e:
            print(f"⚠️ Could not save settings: {e}")
    
    def _configure_story_title(self):
        """Configure story title options"""
        print("\n📖 STORY TITLE CONFIGURATION")
        print("="*50)
        
        if self.custom_story_title:
            print(f"Current: Custom title - \"{self.custom_story_title}\"")
        else:
            print("Current: Auto-generate (Ollama will create title based on story content)")
        
        print("\nOptions:")
        print("1. Auto-generate title (recommended - Ollama creates based on story)")
        print("2. Set custom title")
        print("3. Back")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            self.custom_story_title = None
            print("✓ Story title will be auto-generated by Ollama")
            print("  The AI will create an appropriate title based on the story content")
        elif choice == "2":
            title = input("Enter custom story title: ").strip()
            if title:
                self.custom_story_title = title
                print(f"✓ Custom title set: \"{title}\"")
            else:
                print("❌ Title cannot be empty")
        elif choice == "3":
            pass
        else:
            print("❌ Invalid option")
        
        input("Press Enter to continue...")

    def run_story_generation_menu(self):
        """Main story generation menu loop"""
        while True:
            self.display_story_generation_menu()
            
            try:
                choice = input("Select option (1-15): ").strip()
                
                if choice == "1":
                    self.selected_blueprint = self.blueprint_selector.select_blueprint_for_generation(self.selected_blueprint)
                elif choice == "2":
                    self._configure_story_title()
                elif choice == "3":
                    self.scene_control_mode, self.num_scenes = self.scene_configurator.configure_scene_control(
                        self.scene_control_mode, self.num_scenes)
                elif choice == "4":
                    self.narrative_consistency = self.consistency_configurator.configure_narrative_consistency(
                        self.narrative_consistency)
                elif choice == "5":  # Content Rating
                    old_rating = self.content_rating
                    self.content_rating = self.content_configurator.configure_content_rating(self.content_rating)
                    
                    # Check if content rating change affects language settings
                    if old_rating != self.content_rating:
                        conflicts = self.language_configurator.check_content_conflicts(
                            self.content_rating, self.profanity_level, self.dialogue_intensity)
                        
                        if conflicts:
                            print(f"\n⚠️ Content rating change created language conflicts!")
                            result = self.language_configurator.resolve_conflicts_menu(
                                self.content_rating, self.profanity_level,
                                self.dialogue_intensity, self.speech_style)
                            
                            if len(result) == 4:  # Content rating was changed
                                self.profanity_level, self.dialogue_intensity, self.speech_style, self.content_rating = result
                            else:
                                self.profanity_level, self.dialogue_intensity, self.speech_style = result
                
                elif choice == "6":
                    self.story_tone = self.content_configurator.configure_story_tone(self.story_tone)
                elif choice == "7":
                    self.story_ending = self.content_configurator.configure_story_ending(self.story_ending)
                elif choice == "8":
                    self.character_count = self.content_configurator.configure_character_count(self.character_count)
                elif choice == "9":  # Story Intent Configuration
                    self.configure_story_intent()
                elif choice == "10":  # Perspective Configuration
                    self.configure_perspective()
                elif choice == "11":  # Language Settings
                    old_profanity = self.profanity_level
                    old_intensity = self.dialogue_intensity
                    
                    self.profanity_level, self.dialogue_intensity, self.speech_style = \
                        self.language_configurator.configure_language_style(
                            self.profanity_level, self.dialogue_intensity, self.speech_style)
                    
                    # Check for conflicts after language change
                    if (old_profanity != self.profanity_level or old_intensity != self.dialogue_intensity):
                        conflicts = self.language_configurator.check_content_conflicts(
                            self.content_rating, self.profanity_level, self.dialogue_intensity)
                        
                        if conflicts:
                            print(f"\n⚠️ Language settings conflict with content rating!")
                            result = self.language_configurator.resolve_conflicts_menu(
                                self.content_rating, self.profanity_level,
                                self.dialogue_intensity, self.speech_style)
                            
                            if len(result) == 4:  # Content rating was changed
                                self.profanity_level, self.dialogue_intensity, self.speech_style, self.content_rating = result
                            else:
                                self.profanity_level, self.dialogue_intensity, self.speech_style = result
                
                elif choice == "12":  # Story Variations
                    self.story_variations = self.variation_configurator.set_story_variations(self.story_variations)
                elif choice == "13":  # Advanced LLM Settings
                    self.variation_configurator.show_advanced_llm_settings(self.app)
                elif choice == "14":  # Generate Stories
                    self.story_runner.generate_stories_now(
                        self.selected_blueprint,
                        self.scene_control_mode,
                        self.num_scenes,
                        self.narrative_consistency,
                        self.content_rating,
                        self.story_tone,
                        self.story_ending,
                        self.character_count,
                        self.story_variations,
                        self.story_intent_config,
                        self.perspective_controller,
                        self.profanity_level,
                        self.dialogue_intensity,
                        self.speech_style,
                        self.custom_story_title  # Pass the title setting
                    )
                elif choice == "15":  # Back to Main Menu
                    # Auto-save story generation settings on exit if possible
                    if self.settings_manager and hasattr(self.settings_manager, 'save_story_generation_settings'):
                        self.settings_manager.save_story_generation_settings(self)
                    elif self.settings_manager:
                        self._save_basic_settings()
                    break
                else:
                    print("❌ Invalid option. Please select 1-15.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")
