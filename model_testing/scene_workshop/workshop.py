import datetime
import os
import time
from .settings_proxy import SettingsProxy

class SceneWorkshop:
    def __init__(self, model_tester, template_manager=None):
     
        
        self.model_tester = model_tester
        self.template_manager = template_manager
        self.length_handler = None
        
        # Use persistent settings with error handling
        try:
       
            from .settings_manager import SceneWorkshopSettings
            self.settings = SceneWorkshopSettings()
           
        except Exception as e:
          
            import traceback
            traceback.print_exc()
            self.settings = None
        
        # Create settings proxy
        try:
           
            if self.settings:
                self.current_settings = SettingsProxy(self.settings)
               
            else:
                self.current_settings = {}
                
        except Exception as e:
            print(f"ERROR: Failed to create SettingsProxy: {e}")
            self.current_settings = {}
        
        # Initialize configuration modules
        try:
        
            from .configuration.system_prompt import SystemPromptConfigurator
            from .configuration.user_prompt import UserPromptConfigurator
            from .configuration.styles import StylesConfigurator
            from .configuration.scene_count import SceneCountConfigurator
            from .configuration.age_guidance import AgeGuidanceConfigurator  # Add this
            
            self.system_prompt_config = SystemPromptConfigurator(self)
            self.user_prompt_config = UserPromptConfigurator(self)
            self.styles_config = StylesConfigurator(self)
            self.scene_count_config = SceneCountConfigurator(self)
            self.age_guidance_config = AgeGuidanceConfigurator(self)  # Add this
            
            
            from .parameter_manager import ParameterManager
            self.parameter_manager = ParameterManager(self)
            
            from .second_prompt import SecondPromptManager
            self.second_prompt = SecondPromptManager(self)
            
            
            from .batch_generator import BatchGenerator
            self.batch_generator = BatchGenerator(self)
            
            
            from .generator import Generator
            self.generator = Generator(self)  # Instead of = None
            
    
        except Exception as e:
            print(f"ERROR: Failed to create components: {e}")
            import traceback
            traceback.print_exc()
            # Set fallbacks
            self.system_prompt_config = None
            self.user_prompt_config = None
            self.styles_config = None
            self.scene_count_config = None
            self.parameter_manager = None
            self.second_prompt = None
            self.batch_generator = None
            self.generator = None
            self.age_guidance_config = None  # Add this
        
        

    def set_length_handler(self, length_handler):
        """Set the length handler for this workshop"""
        self.length_handler = length_handler
    
    def generate_with_length_config(self, system_prompt, user_prompt):
        """Generate content using current length configuration"""
        if hasattr(self.template_manager, 'length_config') and self.template_manager and self.template_manager.length_config:
            length_config = self.template_manager.length_config
            
            enhanced_user_prompt = self.template_manager.enhance_prompt_with_length(user_prompt)
            max_tokens = self.template_manager.get_max_tokens_for_generation()
            
            original_max_tokens = self.model_tester.test_config.get('max_tokens')
            self.model_tester.test_config['max_tokens'] = max_tokens
            
            print(f"Using length config: {length_config['description']}")
            print(f"Target: {length_config['words']} words")
            print(f"Max tokens: {max_tokens}")
            
            try:
                result = self.model_tester.test_model(system_prompt, enhanced_user_prompt)
                return result
            finally:
                if original_max_tokens is not None:
                    self.model_tester.test_config['max_tokens'] = original_max_tokens
        else:
            return self.model_tester.test_model(system_prompt, user_prompt)

    def show_main_menu(self):
        """Display main workshop menu with persistent settings"""
        while True:
            try:
                print("\n" + "="*70)
                print("SCENE WORKSHOP")
                print("="*70)
                print("Current Settings:")
                
                # Get model name (from model_tester)
                model_name = self.model_tester.test_config.get('model', 'Not selected')
                if model_name:
                    # Clean up model name for display
                    model_display = model_name.replace(':', '_')
                else:
                    model_display = 'Not selected'
                
                print(f"Model: {model_display}")
                
                # Use safe access with try-catch for all settings
                try:
                    system_prompt_name = self.settings.get('system_prompt_name', 'Not selected') if self.settings else 'Not selected'
                except Exception as e:
                    print(f"Warning: Could not load system_prompt_name: {e}")
                    system_prompt_name = 'Not selected'
                
                try:
                    user_prompt_name = self.settings.get('user_prompt_name', 'Not selected') if self.settings else 'Not selected'
                except Exception as e:
                    print(f"Warning: Could not load user_prompt_name: {e}")
                    user_prompt_name = 'Not selected'
                
                try:
                    param_display = self.parameter_manager.get_parameter_display() if self.parameter_manager else "Parameter manager not available"
                except Exception as e:
                    print(f"Warning: Could not load parameters: {e}")
                    param_display = "Error loading parameters"
                
                try:
                    second_prompt_display = self._get_second_prompt_display()
                except Exception as e:
                    print(f"Warning: Could not load second prompts: {e}")
                    second_prompt_display = "Error loading"
                
                try:
                    narrative_style_name = self.settings.get('narrative_style_name', 'Not selected') if self.settings else 'Not selected'
                except Exception as e:
                    print(f"Warning: Could not load narrative_style_name: {e}")
                    narrative_style_name = 'Not selected'
                
                try:
                    writing_style_name = self.settings.get('writing_style_name', 'Not selected') if self.settings else 'Not selected'
                except Exception as e:
                    print(f"Warning: Could not load writing_style_name: {e}")
                    writing_style_name = 'Not selected'
                
                try:
                    age_guidance_name = self.settings.get('age_guidance_name', 'None (no restrictions)') if self.settings else 'None (no restrictions)'
                except Exception as e:
                    print(f"Warning: Could not load age_guidance_name: {e}")
                    age_guidance_name = 'None (no restrictions)'
                
                try:
                    scene_count = self.settings.get('scene_count', 1) if self.settings else 1
                except Exception as e:
                    print(f"Warning: Could not load scene_count: {e}")
                    scene_count = 1
                
                try:
                    timeout = self.settings.get('timeout_seconds', 0) if self.settings else 0
                    timeout_display = "Unlimited (no timeout)" if timeout == 0 else f"{timeout}s"
                except Exception as e:
                    print(f"Warning: Could not load timeout: {e}")
                    timeout_display = "Error loading timeout"
                
                print(f"System Prompt: {system_prompt_name}")
                print(f"User Prompt: {user_prompt_name}")
                print(f"Second User Prompt: {second_prompt_display}")
                print(f"Parameters: {param_display}")
                print(f"Timeout: {timeout_display}")
                print("="*70)
                
                print("\nESSENTIAL Configuration:")
                print("1. Select System Prompt: " + system_prompt_name)
                print("   → Load from template file, use built-in instructions, or enter custom AI behavior guidelines")
                print("2. Select User Prompt: " + user_prompt_name)
                print("   → Load scene template, use built-in scenario, or create custom story prompt")
                
                print("\nOPTIONAL Enhancements:")
                print("3. Select Narrative Style: " + narrative_style_name + " (adds perspective guidance to user prompt)")
                print("4. Select Writing Style: " + writing_style_name + " (adds style guidance to user prompt)")
                print("5. Configure Parameters & Ranges: " + param_display)
                print("6. Select Second User Prompt(s): " + second_prompt_display + " (for story improvement)")
                print("7. Age Guidance: " + age_guidance_name + " (adds age guidance to user prompt)")  # Add this line
                
                print("\nGeneration (Need system prompt, user prompt, and model configured first):")
                print("8. Generate Single Scene with Streaming")  # Changed from 7
                print("   → Creates one story with real-time output, applies improvements, saves complete results")
                print(f"9. Scene Count: [{scene_count}] - Generate multiple versions of the same scene")  # Changed from 8
                print("   → Creates X variations using same system/user prompts with different AI parameters + improvements")
                print("10. Generate Multiple Scenes with Variations")  # Changed from 9
                print("   → Creates batch of stories testing different AI parameters (temperature, top_p, top_k)")
                print("11. Preview Parameter Progression")  # Changed from 10
                print("    → Shows how parameters will change across multiple scenes before generation")
                
                print("\nSETTINGS MANAGEMENT:")
                print("12. Reset All Settings to Defaults")  # Changed from 11
                print("    → Clear all selections and reset parameters")
                print("13. Reset Parameters to Ollama Defaults")  # Changed from 12
                print("    → Keep prompts/styles, reset only T/P/K/MaxTokens to Ollama defaults")
                print("14. Debug Settings (Show Raw Settings)")  # Changed from 13
                print("    → Display internal settings for troubleshooting")
                
                print("\n0. Back to Single Story Writer")  # Changed from "Back to Testing Menu"
                
                choice = input("\nSelect option (0-14): ").strip()
                
                if choice == '0':
                    break
                elif choice == '1':
                    self._configure_system_prompt()
                elif choice == '2':
                    self._configure_user_prompt()
                elif choice == '3':
                    self._configure_narrative_style()
                elif choice == '4':
                    self._configure_writing_style()
                elif choice == '5':
                    self._configure_parameters()
                elif choice == '6':
                    self._configure_second_prompt()
                elif choice == '7':  # New age guidance option
                    self._configure_age_guidance()
                elif choice == '8':  # Updated numbers
                    if self.generator:
                        self.generator.generate_single_scene()
                    else:
                        print("Generator not available - coming soon!")
                        input("Press Enter to continue...")
                elif choice == '9':
                    self._configure_scene_count()
                elif choice == '10':
                    if self.generator:
                        self.generator.generate_multiple_scenes()  # This method already exists!
                    else:
                        print("Generator not available")
                elif choice == '11':
                    self._preview_parameter_progression()
                elif choice == '12':
                    self._reset_all_settings()
                elif choice == '13':
                    self._reset_parameters_to_ollama_defaults()
                elif choice == '14':
                    self._debug_settings()
                else:
                    print("Invalid option. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nExiting Scene Workshop...")
                break
            except Exception as e:
                print(f"\nUnexpected error in main menu: {e}")
                print(f"Error type: {type(e).__name__}")
                import traceback
                traceback.print_exc()
                
                # Try to reset settings to recover
                print("\nAttempting to reset settings to recover...")
                try:
                    if self.settings:
                        self.settings.reset_to_defaults()
                        print("✅ Settings reset successfully")
                except Exception as reset_error:
                    print(f"❌ Could not reset settings: {reset_error}")
                    print("You may need to delete the settings file manually")
                
                input("Press Enter to continue...")

    def run_workshop_menu(self):
        """Alias for show_main_menu for backward compatibility"""
        return self.show_main_menu()

    def _get_second_prompt_display(self):
        """Get display string for second prompts"""
        if self.second_prompt:
            return self.second_prompt.get_display_name()
        else:
            return "Not available"

    def _configure_system_prompt(self):
        """Configure system prompt using dedicated configurator"""
        if self.system_prompt_config:
            self.system_prompt_config.configure_system_prompt()
        else:
            print("System prompt configurator not available")
            input("Press Enter to continue...")

    def _configure_user_prompt(self):
        """Configure user prompt using dedicated configurator"""
        if self.user_prompt_config:
            self.user_prompt_config.configure_user_prompt()
        else:
            print("User prompt configurator not available")
            input("Press Enter to continue...")

    def _configure_narrative_style(self):
        """Configure narrative style using dedicated configurator"""
        if self.styles_config:
            self.styles_config.configure_narrative_style()
        else:
            print("Styles configurator not available")
            input("Press Enter to continue...")

    def _configure_writing_style(self):
        """Configure writing style using dedicated configurator"""
        if self.styles_config:
            self.styles_config.configure_writing_style()
        else:
            print("Styles configurator not available")
            input("Press Enter to continue...")

    def _configure_parameters(self):
        """Configure parameters"""
        if self.parameter_manager:
            self.parameter_manager.configure_parameters()
        else:
            print("Parameter manager not available")
            input("Press Enter to continue...")

    def _configure_second_prompt(self):
        """Configure second prompt"""
        if self.second_prompt:
            self.second_prompt.select_second_prompt()
        else:
            print("Second prompt manager not available")
            input("Press Enter to continue...")

    def _configure_scene_count(self):
        """Configure scene count using dedicated configurator"""
        if self.scene_count_config:
            self.scene_count_config.configure_scene_count()
        else:
            print("Scene count configurator not available")
            input("Press Enter to continue...")

    def _preview_parameter_progression(self):
        """Preview parameter progression"""
        if self.parameter_manager:
            self.parameter_manager.preview_parameter_progression()
        else:
            print("Parameter manager not available")
            input("Press Enter to continue...")

    def _configure_age_guidance(self):
        """Configure age guidance using dedicated configurator"""
        if self.age_guidance_config:
            self.age_guidance_config.configure_age_guidance()
        else:
            print("Age guidance configurator not available")
            input("Press Enter to continue...")

    def _reset_all_settings(self):
        """Reset all settings to defaults"""
        if self.settings:
            confirm = input("Reset all settings to defaults? (y/n): ").lower()
            if confirm == 'y':
                if self.settings.reset_to_defaults():
                    print("✅ Settings reset to defaults")
                else:
                    print("❌ Failed to reset settings")
            else:
                print("Reset cancelled")
        else:
            print("Settings system not available")
        input("Press Enter to continue...")

    def _reset_parameters_to_ollama_defaults(self):
        """Reset parameters to Ollama defaults"""
        if self.settings:
            confirm = input("Reset parameters to Ollama defaults? (y/n): ").lower()
            if confirm == 'y':
                if self.settings.reset_to_ollama_defaults():
                    print("✅ Parameters reset to Ollama defaults")
                else:
                    print("❌ Failed to reset parameters")
            else:
                print("Reset cancelled")
        else:
            print("Settings system not available")
        input("Press Enter to continue...")

    def _debug_settings(self):
        """Debug settings display"""
        print("\nDEBUG SETTINGS")
        print("="*50)
        try:
            print("Settings object type:", type(self.settings))
            if self.settings:
                print("Settings file path:", getattr(self.settings, 'settings_file', 'Unknown'))
                print("Raw settings:")
                if hasattr(self.settings, 'settings'):
                    for key, value in self.settings.settings.items():
                        print(f"  {key}: {repr(value)}")
                else:
                    print("  No settings attribute found")
            else:
                print("Settings object is None")
                
            print("\nProxy object type:", type(self.current_settings))
            
        except Exception as e:
            print(f"Error during debug: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to continue...")

    def get_enhanced_user_prompt(self, base_user_prompt):
        """Get user prompt with all enhancements applied"""
        if not base_user_prompt:
            return base_user_prompt
        
        enhanced_prompt = base_user_prompt
        
        # Add narrative style enhancement
        narrative_style = self.settings.get('narrative_style') if self.settings else None
        if narrative_style:
            # Add narrative style text based on selection
            # Implementation depends on your narrative style system
            pass
        
        # Add writing style enhancement  
        writing_style = self.settings.get('writing_style') if self.settings else None
        if writing_style:
            # Add writing style text based on selection
            # Implementation depends on your writing style system
            pass
        
        # Add age guidance enhancement
        if self.age_guidance_config:
            age_enhancement = self.age_guidance_config.get_guidance_enhancement()
            if age_enhancement:
                enhanced_prompt += age_enhancement
        
        return enhanced_prompt
