import requests
import json
import os
import time
import glob
from pathlib import Path
import sys

from generators.story_generator import StoryGenerator
from blueprint_creator import BlueprintCreator
# Remove the direct import of F5TTSHandler
# from f5tts_handler import F5TTSHandler
from settings_manager import SettingsManager  # Add this import
from story_analyzer import StoryAnalyzer
from story_log_analyzer import StoryLogAnalyzer
from settings_ui import SettingsUI
from story_generation_menu.main_menu import StoryGenerationMenu
from folder_manager import FolderManager
from logging_config import LoggingConfig

import datetime

# Add F5-TTS dependency check
def check_f5tts_dependencies():
    try:
        import gradio_client
        import huggingface_hub
        return True
    except ImportError:
        return False

HAS_F5_TTS = check_f5tts_dependencies()

class OllamaStoryTeller:
    def __init__(self):
        # Initialize settings manager first
        self.settings = SettingsManager()
        
        # Updated folder structure - multiscene organization
        self.blueprint_folder = "multiscene/blueprints"
        self.storyboard_folder = "multiscene/storyboards" 
        self.stories_folder = "multiscene/stories"
        self.audio_folder = "multiscene/audio"  # renamed from audio_stories
        self.multiscene_stats_folder = "multiscene/stats"  # new
        
        # Laboratory organization
        self.laboratory_templates_folder = "laboratory/templates"  # new
        self.laboratory_scenes_folder = "laboratory/scenes"  # replaces model_tests
        self.laboratory_metadata_folder = "laboratory/metadata"  # new for prompts + stats
        
        # Update settings using batch update to avoid multiple saves
        folder_settings = {
            "blueprint_folder": self.blueprint_folder,
            "storyboard_folder": self.storyboard_folder,
            "stories_folder": self.stories_folder
        }
        self.settings.update_multiple(folder_settings, save_immediately=False)
        
        # Load other settings from manager
        self.selected_blueprint = self.settings.get("selected_blueprint")
        self.selected_model = self.settings.get("selected_model")  # Now None by default
        self.max_tokens = self.settings.get("max_tokens")
        self.temperature = self.settings.get("temperature")
        self.top_p = self.settings.get("top_p")
        self.top_k = self.settings.get("top_k")
        self.repeat_penalty = self.settings.get("repeat_penalty")
        self.seed = self.settings.get("seed")
        self.num_runs = self.settings.get("num_runs")
        self.storyboard_reuse_mode = self.settings.get("storyboard_reuse_mode")
        self.auto_generate_audio = self.settings.get("auto_generate_audio")
        self.available_models = []
        self.available_blueprints = []
        self.gender_swap_mode = self.settings.get("gender_swap_mode")
        self.story_log_analyzer = None  # Will be initialized when needed
        
        # Add new settings
        self.thinking_mode_enabled = self.settings.get("thinking_mode_enabled")
        self.instruct_mode_enabled = self.settings.get("instruct_mode_enabled")
        
        # Update app_folders for size calculation
        self.app_folders = {
            'multiscene_blueprints': self.blueprint_folder,
            'multiscene_storyboards': self.storyboard_folder, 
            'multiscene_stories': self.stories_folder,
            'multiscene_audio': self.audio_folder,
            'multiscene_stats': self.multiscene_stats_folder,
            'laboratory_templates': self.laboratory_templates_folder,
            'laboratory_scenes': self.laboratory_scenes_folder,
            'laboratory_metadata': self.laboratory_metadata_folder,
            'support_references': 'support/references',
            'support_logs': 'support/logs',
            'support_generators': 'support/generators'
        }
        
        # Initialize folder manager
        self.folder_manager = FolderManager(self.app_folders)
        
        # Initialize logging configuration manager
        self.logging_config = LoggingConfig(self.settings, self.stories_folder)
        
        # Initialize blueprint creator
        self.blueprint_creator = BlueprintCreator(self.blueprint_folder)
        # Initialize F5-TTS handler with conditional import
        if HAS_F5_TTS:
            from f5tts_handler import F5TTSHandler
            self.f5tts_handler = F5TTSHandler(self.audio_folder)  # updated folder
            self._load_f5tts_settings()
        else:
            self.f5tts_handler = None
        
        self.story_analyzer = None 
        self.settings_ui = SettingsUI(self)
        self.story_generation_menu = StoryGenerationMenu(self)
        
        # Initialize model testing menu with error handling
        self.model_testing_menu = None
        try:
            from model_testing.model_testing_menu import ModelTestingMenu
            self.model_testing_menu = ModelTestingMenu(self)
        except ImportError as e:
            print(f"Warning: Model testing module not available: {e}")
            print("   Model testing features will be disabled.")
            
        # Create necessary folders with new structure
        folders_to_create = [
            self.blueprint_folder, self.storyboard_folder, self.stories_folder, 
            self.audio_folder, self.multiscene_stats_folder,
            self.laboratory_templates_folder, self.laboratory_scenes_folder, 
            self.laboratory_metadata_folder,
            "support/references", "support/logs", "support/generators"
        ]
        
        for folder in folders_to_create:
            os.makedirs(folder, exist_ok=True)

    # ... rest of the methods remain unchanged until we update other components ...
    
    def _load_f5tts_settings(self):
        """Load F5-TTS settings into handler"""
        if not HAS_F5_TTS or not self.f5tts_handler:
            return
            
        # ... existing F5-TTS settings loading code unchanged ...
        self.f5tts_handler.f5tts_server_url = self.settings.get("f5tts_server_url")
        self.f5tts_handler.f5tts_selected_ref = self.settings.get("f5tts_selected_ref")
        self.f5tts_handler.f5tts_ref_text = self.settings.get("f5tts_ref_text")
        self.f5tts_handler.f5tts_remove_silence = self.settings.get("f5tts_remove_silence")
        self.f5tts_handler.f5tts_cross_fade = self.settings.get("f5tts_cross_fade")
        self.f5tts_handler.f5tts_nfe = self.settings.get("f5tts_nfe")
        self.f5tts_handler.f5tts_speed = self.settings.get("f5tts_speed")
        self.f5tts_handler.tts_timing_data = self.settings.get("f5tts_timing_data")
        self.f5tts_handler.tts_processed_count = self.settings.get("f5tts_processed_count")
    def _get_current_llm_settings(self):
        """Get current LLM settings for analyzer and generators"""
        return {
            'model': self.selected_model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'repeat_penalty': self.repeat_penalty,
            'seed': self.seed,
            'gender_swap_mode': self.settings.get("gender_swap_mode", "none"),
            'thinking_mode_enabled': self.thinking_mode_enabled,
            'instruct_mode_enabled': self.instruct_mode_enabled
        }
    def analyze_story(self):
        """Delegate to story analyzer with current settings"""
        # Initialize or update analyzer with current settings
        llm_settings = self._get_current_llm_settings()
        self.story_analyzer = StoryAnalyzer(self.stories_folder, self.blueprint_folder, llm_settings)
        self.story_analyzer.analyze_story()
    def _save_f5tts_settings(self):
        """Save F5-TTS settings from handler"""
        f5tts_updates = {
            "f5tts_server_url": self.f5tts_handler.f5tts_server_url,
            "f5tts_selected_ref": self.f5tts_handler.f5tts_selected_ref,
            "f5tts_ref_text": self.f5tts_handler.f5tts_ref_text,
            "f5tts_remove_silence": self.f5tts_handler.f5tts_remove_silence,
            "f5tts_cross_fade": self.f5tts_handler.f5tts_cross_fade,
            "f5tts_nfe": self.f5tts_handler.f5tts_nfe,
            "f5tts_speed": self.f5tts_handler.f5tts_speed,
            "f5tts_timing_data": self.f5tts_handler.tts_timing_data,
            "f5tts_processed_count": self.f5tts_handler.tts_processed_count
        }
        self.settings.update_multiple(f5tts_updates, save_immediately=True)
        # If reference audio was removed, automatically disable auto-generate
        if not self.f5tts_handler.f5tts_selected_ref and self.auto_generate_audio:
            print("\nReference audio was removed. Auto-generate audio has been disabled.")
            self.auto_generate_audio = False
            self.settings.set("auto_generate_audio", False)
    def get_available_models(self):
        """Get list of available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            return ["llama2", "dolphin3:latest", "mistral"]
        except:
            return ["llama2", "dolphin3:latest", "mistral"]

    def get_available_blueprints(self):
        """Get list of available story blueprints"""
        story_files = glob.glob(os.path.join(self.blueprint_folder, "*.story.txt"))
        return [os.path.basename(f) for f in story_files]
    
    def select_blueprint(self):
        """Let user select a story blueprint"""
        blueprints = self.get_available_blueprints()
        
        if not blueprints:
            print(f"\nNo story blueprints found in {self.blueprint_folder}/ folder.")
            print("Please create .story.txt files in the blueprints/ folder.")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable blueprints:")
        for i, blueprint in enumerate(blueprints, 1):
            print(f"{i}. {blueprint}")
        
        try:
            choice = int(input(f"Select blueprint (1-{len(blueprints)}): "))
            if 1 <= choice <= len(blueprints):
                self.selected_blueprint = blueprints[choice - 1]
                self.settings.set("selected_blueprint", self.selected_blueprint)  # Save setting
                print(f"Selected: {self.selected_blueprint}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error: {e}")
        
        input("Press Enter to continue...")

    def select_model(self):
        """Let user select Ollama model"""
        models = self.get_available_models()
        
        print("\nAvailable models:")
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        
        try:
            choice = int(input(f"Select model (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                self.selected_model = models[choice - 1]
                self.settings.set("selected_model", self.selected_model)  # Save setting
                print(f"Selected: {self.selected_model}")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
        except Exception as e:
            print(f"Error: {e}")
        
        input("Press Enter to continue...")

    def settings_manager_menu(self):
        """Settings manager menu"""
        while True:
            print("\n" + "="*60)
            print("SETTINGS MANAGER")
            print("="*60)
            print("1. View all settings")
            print("2. Reset to defaults")
            print("3. Export settings to file")
            print("4. Import settings from file")
            print("5. Back to main menu")
            
            try:
                choice = input("\nSelect option (1-5): ").strip()
                
                if choice == "1":
                    self.settings.display_settings_summary()
                    input("\nPress Enter to continue...")
                elif choice == "2":
                    confirm = input("Are you sure you want to reset all settings? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.settings.reset_to_defaults()
                        # Reload settings into app
                        self.__init__()
                        print("Settings reset and reloaded")
                    input("Press Enter to continue...")
                elif choice == "3":
                    filename = input("Enter export filename (default: exported_settings.json): ").strip()
                    if not filename:
                        filename = "exported_settings.json"
                    self.settings.export_settings(filename)
                    input("Press Enter to continue...")
                elif choice == "4":
                    filename = input("Enter import filename: ").strip()
                    if filename and os.path.exists(filename):
                        self.settings.import_settings(filename)
                        # Reload settings into app
                        self.__init__()
                        print("Settings imported and reloaded")
                    else:
                        print("File not found")
                    input("Press Enter to continue...")
                elif choice == "5":
                    break
                else:
                    print("Invalid option")
                    input("Press Enter to continue...")
                    
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")

    def run_f5tts_menu(self):
        """Run F5-TTS menu with dependency check"""
        if not HAS_F5_TTS:
            print("\n" + "="*60)
            print("F5-TTS AUDIO GENERATION - MISSING DEPENDENCIES")
            print("="*60)
            print("F5-TTS requires additional packages that are not installed.")
            print()
            print("Please install the required packages:")
            print("pip install gradio-client==1.11.0 huggingface-hub==0.34.2")
            print()
            print("After installation, restart the application to use F5-TTS.")
            input("\nPress Enter to continue...")
            return
            
        self.f5tts_handler.run_f5tts_menu()
        self._save_f5tts_settings()  # Save F5-TTS settings when returning

    def advanced_settings_menu(self):
        """Show advanced settings menu"""
        while True:
            print("\n" + "="*60)
            print("ADVANCED SETTINGS")
            print("="*60)
            print(f"1. Select Model: {self.selected_model or 'None selected'}")
            print(f"2. Select Blueprint: {self.selected_blueprint or 'None selected'}")
            print(f"3. Max tokens: {self.max_tokens:,}")
            print(f"4. Temperature (creativity): {self.temperature}")
            print(f"5. Top-p (nucleus sampling): {self.top_p}")
            print(f"6. Top-k (token filtering): {self.top_k}")
            print(f"7. Repeat penalty: {self.repeat_penalty}")
            print(f"8. Seed (reproducibility): {self.seed or 'Random'}")
            
            reuse_display = {
                "new": "Create new story bible & scene plan",
                "bible_only": "Reuse story bible, new scene plan", 
                "both": "Reuse story bible & scene plan"
            }
            print(f"9. Storyboard reuse: {reuse_display[self.storyboard_reuse_mode]}")
            print(f"10. {self.settings.get_auto_audio_display_text()}")
            
            # Clearer reasoning control display
            reasoning_status = "Try to disable" if not self.thinking_mode_enabled else "No change"
            instruct_status = "Enabled" if self.instruct_mode_enabled else "Disabled"
            print(f"11. If model is reasoning/thinking: {reasoning_status}")
            print(f"12. Instruct mode (instruction prompts): {instruct_status}")
            
            print("13. Prompt Logging & Debugging")
            print("14. Back to main menu")
            
            try:
                choice = input(f"\nSelect option (1-14): ").strip()
                
                if choice == "1":
                    self.select_model()
                elif choice == "2":
                    self.select_blueprint()
                elif choice == "3":
                    self.settings_ui.set_max_tokens()
                elif choice == "4":
                    self.settings_ui.set_temperature()
                elif choice == "5":
                    self.settings_ui.set_top_p()
                elif choice == "6":
                    self.settings_ui.set_top_k()
                elif choice == "7":
                    self.settings_ui.set_repeat_penalty()
                elif choice == "8":
                    self.settings_ui.set_seed()
                elif choice == "9":
                    self.settings_ui.set_storyboard_reuse()
                elif choice == "10":
                    self.settings_ui.toggle_auto_audio()
                elif choice == "11":
                    self.settings_ui.toggle_reasoning_control()  # Update method name
                elif choice == "12":
                    self.settings_ui.toggle_instruct_mode()
                elif choice == "13":
                    self.logging_config.configure_logging_settings()
                elif choice == "14":
                    break
                else:
                    print("Invalid option. Please select 1-14.")
                    input("Press Enter to continue...")
                    
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")

    def run(self):
        """Main application loop with updated menu options"""
        while True:
            self.display_menu()
            
            try:
                choice = input().strip().lower()
                
                if choice == "1":
                    self.story_generation_menu.run_story_generation_menu()
                elif choice == "1a":
                    self.create_blueprint()
                elif choice == "1b":
                    self.analyze_story()
                elif choice == "1c":
                    self.analyze_logs()
                elif choice == "2":
                    if self.model_testing_menu is None:
                        print("Single Scene Laboratory is not available")
                    else:
                        self.model_testing_menu.run_testing_menu()
                elif choice == "3":
                    if not HAS_F5_TTS:
                        print("\n" + "="*60)
                        print("F5-TTS AUDIO GENERATION - MISSING DEPENDENCIES")
                        print("="*60)
                        print("F5-TTS requires additional packages that are not installed.")
                        print()
                        print("Please install the required packages:")
                        print("pip install gradio-client==1.11.0 huggingface-hub==0.34.2")
                        print()
                        print("After installation, restart the application to use F5-TTS.")
                        input("\nPress Enter to continue...")
                        continue
                    self.run_f5tts_menu()
                elif choice == "4":
                    self.settings_manager_menu()
                elif choice == "5":
                    self.advanced_settings_menu()
                elif choice == "6":
                    self.show_detailed_folder_stats()
                elif choice == "7":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please select 1, 1a, 1b, 1c, or 2-7.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")

    def display_menu(self):
        """Display main menu with folder usage statistics"""
        # Delegate to folder manager
        self.folder_manager.display_folder_stats_in_menu(
            self.selected_model, 
            self.selected_blueprint
        )
        
        print("\n" + "="*70)
        print("1. Generate Multi-Scene Stories")
        print("   1a. Create New Blueprint")
        print("   1b. Analyze Existing Story")
        print("   1c. Analyze Prompt Logs")
        print("")
        print("2. Single Scene & Story Laboratory")
        
        # Conditional display for F5-TTS
        if HAS_F5_TTS:
            print("3. F5-TTS Audio Generation")
        else:
            print("3. F5-TTS Audio Generation (missing imports, disabled)")
        
        print("4. Settings Manager")
        print("5. Advanced Settings (Model, Tokens, etc.)")
        print("6. View Detailed Folder Statistics")
        print("7. Exit")
        print("\nSelect option (1, 1a, 1b, 1c, 2-7): ", end="")

    def show_detailed_folder_stats(self):
        """Show detailed folder statistics - delegate to folder manager"""
        self.folder_manager.show_detailed_folder_stats()

    # The following methods have been removed and moved to folder_manager.py:
    # - get_folder_size()
    # - format_size()
    # - count_files_in_folder()
    # - get_folder_stats()
    # - show_detailed_folder_stats()

    def analyze_logs(self):
        """Delegate to log analyzer with current settings"""
        llm_settings = self._get_current_llm_settings()
        self.story_log_analyzer = StoryLogAnalyzer(self.stories_folder, llm_settings)
        self.story_log_analyzer.analyze_logs()

    def create_blueprint(self):
        """Create a new blueprint using the blueprint creator"""
        new_blueprint = self.blueprint_creator.create_blueprint()
        
        if new_blueprint:
            # Ask if they want to use this blueprint immediately
            use_now = input("\nUse this blueprint now? (y/n): ").strip().lower()
            if use_now == 'y':
                self.selected_blueprint = new_blueprint
                self.settings.set("selected_blueprint", self.selected_blueprint)
                print(f"Now using blueprint: {new_blueprint}")

    def get_model_mode_display(self):
        """Get display text for model modes in story generation center"""
        mode_parts = []
        
        # Reasoning control
        reasoning_status = "Try to disable" if not self.thinking_mode_enabled else "No change"
        mode_parts.append(f"Reasoning: {reasoning_status}")
        
        # Instruct mode
        instruct_status = "On" if self.instruct_mode_enabled else "Off"
        mode_parts.append(f"Instruct: {instruct_status}")
        
        return " | ".join(mode_parts)

if __name__ == "__main__":
    app = OllamaStoryTeller()
    app.run()