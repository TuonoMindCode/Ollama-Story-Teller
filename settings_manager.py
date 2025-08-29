import json
import os
from typing import Dict, Any

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            # Main app settings
            "selected_blueprint": None,
            "selected_model": None,
            "max_tokens": 4096,
            "temperature": 0.8,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "seed": None,
            "num_runs": 1,
            "storyboard_reuse_mode": "new",
            "auto_generate_audio": False,
            
            # NEW: Add thinking and instruct mode settings - DISABLED by default
            "thinking_mode_enabled": False,    # Most models don't show reasoning
            "instruct_mode_enabled": False,    # Most models aren't instruct-tuned
            
            # NEW: Story Generation Menu Settings
            "scene_control_mode": "auto",
            "num_scenes": "auto",
            "narrative_consistency": "auto_tracking",
            "story_variations": 1,
            
            # Content settings
            "content_rating": "auto",
            "story_tone": "auto",
            "story_ending": "auto",
            "character_count": "auto",
            
            # Language settings
            "profanity_level": "moderate",
            "dialogue_intensity": "moderate",
            "speech_style": "casual",
            
            # Story intent settings
            "story_intent_configured": False,
            "story_intent_data": {},
            
            # Perspective settings
            "perspective_configured": False,
            "perspective_selected": "default",
            "perspective_mapping": {},
            "perspective_schedule": [],
            
            # F5-TTS settings
            "f5tts_server_url": "http://127.0.0.1:7860",
            "f5tts_selected_ref": None,
            "f5tts_ref_text": "",
            "f5tts_remove_silence": False,
            "f5tts_cross_fade": 0.15,
            "f5tts_nfe": 16,
            "f5tts_speed": 1.0,
            "f5tts_timing_data": [],
            "f5tts_processed_count": 0,
            
            # Folders
            "blueprint_folder": "blueprints",
            "storyboard_folder": "storyboards", 
            "stories_folder": "stories",
            "audio_folder": "audio_stories",
            
            # Added setting
            "gender_swap_mode": "none",  # Options: "none", "main_lead", "both_leads"
            "force_protagonist_gender": "auto",  # Options: "auto", "male", "female"
            
            # Add these to your default settings dictionary
            "enable_prompt_logging": False,  # Changed from True to False
            "log_retention_days": 30,       # How long to keep logs (0 = keep forever)
            "detailed_logging": True,       # Include full prompts in logs vs summary only
        }
        
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file, or return defaults if file doesn't exist"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                
                # Merge with defaults to handle new settings
                settings = self.default_settings.copy()
                settings.update(saved_settings)
                
                print(f"✓ Settings loaded from {self.settings_file}")
                return settings
                
            except Exception as e:
                print(f"⚠️  Error loading settings: {e}")
                print("Using default settings...")
                return self.default_settings.copy()
        else:
            print(f"📝 No settings file found. Using defaults.")
            return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            # Create backup of existing settings
            if os.path.exists(self.settings_file):
                backup_file = f"{self.settings_file}.backup"
                import shutil
                shutil.copy2(self.settings_file, backup_file)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Settings saved to {self.settings_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving settings: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any, save_immediately: bool = True):
        """Set a setting value"""
        self.settings[key] = value
        if save_immediately:
            self.save_settings()
    
    def update_multiple(self, updates: Dict[str, Any], save_immediately: bool = True):
        """Update multiple settings at once"""
        self.settings.update(updates)
        if save_immediately:
            self.save_settings()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save_settings()
        print("✓ Settings reset to defaults")
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all current settings"""
        return self.settings.copy()
    
    def export_settings(self, export_file: str) -> bool:
        """Export settings to a different file"""
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            print(f"✓ Settings exported to {export_file}")
            return True
        except Exception as e:
            print(f"❌ Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_file: str) -> bool:
        """Import settings from a different file"""
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Validate imported settings against defaults
            valid_settings = {}
            for key, value in imported_settings.items():
                if key in self.default_settings:
                    valid_settings[key] = value
                else:
                    print(f"⚠️  Skipping unknown setting: {key}")
            
            self.settings.update(valid_settings)
            self.save_settings()
            print(f"✓ Settings imported from {import_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error importing settings: {e}")
            return False
    
    def get_auto_audio_display_text(self) -> str:
        """Get the display text for auto-generate audio option"""
        ref_audio = self.get('f5tts_selected_ref')
        auto_enabled = self.get('auto_generate_audio')
        
        if ref_audio:
            # Get just the filename without path
            ref_filename = os.path.basename(ref_audio)
            # Remove extension for cleaner display
            ref_name = os.path.splitext(ref_filename)[0]
            status_text = f"Auto-generate audio after stories (ref audio: {ref_name}): {'Enabled' if auto_enabled else 'Disabled'}"
        else:
            status_text = f"Auto-generate audio after stories (ref audio not selected): {'Disabled' if not auto_enabled else 'Enabled (will fail)'}"
        
        return status_text
    
    def display_settings_summary(self):
        """Display a summary of current settings"""
        print("\n" + "="*60)
        print("CURRENT SETTINGS SUMMARY")
        print("="*60)
        
        print("\n📚 STORY GENERATION:")
        print(f"  Blueprint: {self.get('selected_blueprint') or 'None selected'}")
        print(f"  Model: {self.get('selected_model') or 'None selected'}")
        print(f"  Max tokens: {self.get('max_tokens'):,}")
        print(f"  Temperature: {self.get('temperature')}")
        print(f"  Runs: {self.get('num_runs')}")
        print(f"  Reuse mode: {self.get('storyboard_reuse_mode')}")
        
        # NEW: Story generation menu settings
        print(f"\n STORY CONFIGURATION:")
        print(f"  Scene Control: {self.get('scene_control_mode', 'auto').title()}")
        print(f"  Narrative Consistency: {self.get('narrative_consistency', 'auto_tracking').replace('_', ' ').title()}")
        print(f"  Content Rating: {self.get('content_rating', 'auto').title()}")
        print(f"  Story Tone: {self.get('story_tone', 'auto').replace('_', ' ').title()}")
        print(f"  Language: {self.get('profanity_level', 'moderate').title()}/{self.get('dialogue_intensity', 'moderate').title()}")
        print(f"  Perspective: {self.get('perspective_selected', 'default').replace('_', ' ').title()}")
        print(f"  Story Variations: {self.get('story_variations', 1)}")
        
        print("\n🎵 F5-TTS:")
        print(f"  Server: {self.get('f5tts_server_url')}")
        print(f"  Reference audio: {self.get('f5tts_selected_ref') or 'None selected'}")
        print(f"  Auto-generate: {'Enabled' if self.get('auto_generate_audio') else 'Disabled'}")
        print(f"  Speed: {self.get('f5tts_speed')}")
        print(f"  NFE: {self.get('f5tts_nfe')}")
        
        print("\n📁 FOLDERS:")
        print(f"  Stories: {self.get('stories_folder')}")
        print(f"  Audio: {self.get('audio_folder')}")
        print(f"  Blueprints: {self.get('blueprint_folder')}")
    
    def save_story_generation_settings(self, main_menu_instance):
        """Save story generation menu settings to the main settings file"""
        story_settings = {
            # Basic settings
            "scene_control_mode": main_menu_instance.scene_control_mode,
            "num_scenes": main_menu_instance.num_scenes,
            "narrative_consistency": main_menu_instance.narrative_consistency,
            "story_variations": main_menu_instance.story_variations,
            
            # Content settings
            "content_rating": main_menu_instance.content_rating,
            "story_tone": main_menu_instance.story_tone,
            "story_ending": main_menu_instance.story_ending,
            "character_count": main_menu_instance.character_count,
            
            # Language settings
            "profanity_level": main_menu_instance.profanity_level,
            "dialogue_intensity": main_menu_instance.dialogue_intensity,
            "speech_style": main_menu_instance.speech_style,
            
            # Story intent settings
            "story_intent_configured": bool(main_menu_instance.story_intent_config.configured_intent),
            "story_intent_data": main_menu_instance.story_intent_config.configured_intent,
            
            # Perspective settings
            "perspective_configured": getattr(main_menu_instance, 'perspective_configured', False),
            "perspective_selected": main_menu_instance.perspective_controller.selected_perspective if hasattr(main_menu_instance, 'perspective_controller') else 'default',
            "perspective_mapping": getattr(main_menu_instance.perspective_controller, 'character_mapping', {}) if hasattr(main_menu_instance, 'perspective_controller') else {},
            "perspective_schedule": getattr(main_menu_instance.perspective_controller, 'pov_schedule', []) if hasattr(main_menu_instance, 'perspective_controller') else []
        }
        
        # Update the main settings with story generation settings
        self.update_multiple(story_settings, save_immediately=True)
        print("💾 Story generation settings saved!")
    
    def load_story_generation_settings(self, main_menu_instance):
        """Load story generation settings into the main menu instance"""
        try:
            # Basic settings
            main_menu_instance.scene_control_mode = self.get('scene_control_mode', 'auto')
            main_menu_instance.num_scenes = self.get('num_scenes', 'auto')
            main_menu_instance.narrative_consistency = self.get('narrative_consistency', 'auto_tracking')
            main_menu_instance.story_variations = self.get('story_variations', 1)
            
            # Content settings
            main_menu_instance.content_rating = self.get('content_rating', 'auto')
            main_menu_instance.story_tone = self.get('story_tone', 'auto')
            main_menu_instance.story_ending = self.get('story_ending', 'auto')
            main_menu_instance.character_count = self.get('character_count', 'auto')
            
            # Language settings
            main_menu_instance.profanity_level = self.get('profanity_level', 'moderate')
            main_menu_instance.dialogue_intensity = self.get('dialogue_intensity', 'moderate')
            main_menu_instance.speech_style = self.get('speech_style', 'casual')
            
            # Story intent settings
            if self.get('story_intent_configured', False) and self.get('story_intent_data'):
                main_menu_instance.story_intent_config.configured_intent = self.get('story_intent_data', {})
            
            # Perspective settings
            if hasattr(main_menu_instance, 'perspective_controller'):
                main_menu_instance.perspective_configured = self.get('perspective_configured', False)
                main_menu_instance.perspective_controller.selected_perspective = self.get('perspective_selected', 'default')
                main_menu_instance.perspective_controller.character_mapping = self.get('perspective_mapping', {})
                main_menu_instance.perspective_controller.pov_schedule = self.get('perspective_schedule', [])
            
            print("💾 Story generation settings loaded!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load story generation settings: {e}")
            return False