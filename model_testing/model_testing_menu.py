import os
import time
import datetime
from typing import Dict, List, Optional

try:
    from .model_tester import ModelTester
    from .template_manager2 import TemplateManager
    from .scene_workshop.workshop import SceneWorkshop
    from .length_handler import LengthHandler  # Add this import
except ImportError:
    # Fallback for when files don't exist yet
    pass

class ModelTestingMenu:
    def __init__(self, main_app):
        self.app = main_app
        
        # Initialize model tester first (loads saved config)
        self.model_tester = ModelTester(main_app.stories_folder)

        
        # Initialize length handler
        try:
            self.length_handler = LengthHandler()
        except NameError:
            self.length_handler = None
            print("LengthHandler not available - some features may be limited")
        except Exception as e:
            self.length_handler = None
            print(f"LengthHandler error: {e}")
        
        # Initialize other components with the model tester
        try:
           
            from .scene_workshop.workshop import SceneWorkshop
            from .template_manager2 import TemplateManager
            
            
            
            self.template_manager = TemplateManager(self.model_tester)
        
            
       
            self.scene_workshop = SceneWorkshop(self.model_tester, self.template_manager)
        
            
            # Pass length handler to components that need it
            if hasattr(self.scene_workshop, 'set_length_handler') and self.length_handler:
                
                self.scene_workshop.set_length_handler(self.length_handler)
            if hasattr(self.template_manager, 'set_length_handler') and self.length_handler:
                
                self.template_manager.set_length_handler(self.length_handler)
                
            
        except ImportError as e:
            print(f"ImportError - Some testing components not available: {e}")
            import traceback
            traceback.print_exc()
            self.template_manager = None
            self.scene_workshop = None
        except Exception as e:
            print(f"ERROR creating testing components: {e}")
            import traceback
            traceback.print_exc()
            self.template_manager = None
            self.scene_workshop = None
        
    def run_testing_menu(self):
        """Main menu loop"""
        # Initialize components if not already done
        if self.model_tester is None:
            print("Initializing single scene & story components...")
            try:
                from .model_tester import ModelTester
                from .template_manager2 import TemplateManager
                from .scene_workshop.workshop import SceneWorkshop
            
                self.model_tester = ModelTester(self.app.stories_folder)
                self.template_manager = TemplateManager(self.model_tester)
                self.scene_workshop = SceneWorkshop(self.model_tester, self.template_manager)
                print("Single scene & story writer initialized successfully")
            except ImportError as e:
                print(f"Failed to initialize: {e}")
                print("Please ensure all files are created.")
                input("Press Enter to return to main menu...")
                return
    
        while True:
            self.display_main_menu()
        
            try:
                choice = input().strip()
            
                if choice == "1":
                    if self.template_manager:
                        self.template_manager.run_template_menu()
                    else:
                        print("Template Manager not available")
                        input("Press Enter to continue...")
                elif choice == "2":
                    print("DEBUG: Scene Workshop option selected")
                    print(f"DEBUG: self.scene_workshop = {self.scene_workshop}")
                    print(f"DEBUG: self.scene_workshop type = {type(self.scene_workshop)}")
                
                    if self.scene_workshop:
                        print("DEBUG: Calling run_workshop_menu...")
                        self.scene_workshop.run_workshop_menu()
                    else:
                        print("Scene Workshop not available - trying to create it now...")
                    
                        # Try to create it on demand
                        try:
                            from .scene_workshop.workshop import SceneWorkshop
                            workshop = SceneWorkshop(self.model_tester, self.template_manager)
                        
                            if workshop:
                                workshop.run_workshop_menu()
                            else:
                                print("ERROR: SceneWorkshop creation returned None")
                            
                        except ImportError as e:
                            print(f"ImportError: {e}")
                            import traceback
                            traceback.print_exc()
                        except Exception as e:
                            print(f"ERROR creating SceneWorkshop: {e}")
                            import traceback
                            traceback.print_exc()
                    
                        input("Press Enter to continue...")
                elif choice == "3":
                    self.single_scene_story_settings()
                elif choice == "4":
                    break
                else:
                    print("Invalid option. Please select 1-4.")
                    input("Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                input("Press Enter to continue...")
    
    def display_main_menu(self):
        """Display the main menu"""
        if self.model_tester:
            stats = self.model_tester.get_test_results_stats()
        else:
            stats = {'total_sessions': 0, 'total_files': 0, 'formatted_size': '0 B'}
    
        print("\n" + "="*80)
        print("SINGLE SCENE & STORY WRITER")
        print("="*80)
    
        if self.model_tester:
            single_scene_model = self.model_tester.test_config.get('model', 'None selected')
        else:
            single_scene_model = 'Not initialized'
        
        print(f"Single Scene/Story LLM: {single_scene_model}")
        print(f"Multi-Scene Story LLM: {self.app.selected_model or 'None selected'}")
    
        if stats['total_sessions'] > 0:
            print(f"\nGenerated Content: {stats['total_sessions']} sessions | {stats['total_files']} files | {stats['formatted_size']}")
        else:
            print("\nNo content generated yet")
    
        print("\n" + "="*80)
        print("1.  Template Manager (System & User Prompts)")
        print("2.  Scene & Story Creator")
        print("3.  Single Scene & Story LLM Settings") 
        print("4.  Back to Main Menu")
        print("\nSelect option (1-4): ", end="")
    
    def single_scene_story_settings(self):
        """Configure single scene & story LLM settings"""
        # Use the ModelTester's built-in configuration method
        self.model_tester.configure_testing_settings()
    
    def _select_and_save_test_model(self):
        """Select and save test model"""
        models = self.model_tester.get_available_models()
        
        if not models:
            print("\nNo Ollama models found")
            print("Make sure Ollama is running and models are installed")
            input("Press Enter to continue...")
            return
        
        print("\nSELECT TEST MODEL:")
        print("="*40)
        current_model = self.model_tester.test_config.get('model')
        
        for i, model in enumerate(models, 1):
            current = " (current)" if model == current_model else ""
            print(f"{i:2d}. {model}{current}")
        
        print(f"{len(models) + 1}. Clear selection (set to None)")
        
        try:
            choice = int(input(f"\nSelect model (1-{len(models) + 1}): "))
            
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
                self.model_tester.set_model(selected_model)
                
                # Also update all components with new model
                if hasattr(self, 'scene_workshop'):
                    print("Updated Scene Workshop model")
                if hasattr(self, 'template_manager'):
                    print("Updated Template Manager model")
                    
            elif choice == len(models) + 1:
                self.model_tester.set_model(None)
                print("Test model cleared")
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _set_temperature(self):
        """Set temperature setting"""
        try:
            current = self.model_tester.test_config['temperature']
            temp = float(input(f"Temperature (0.0-2.0, current: {current}): "))
            if 0.0 <= temp <= 2.0:
                self.model_tester.test_config['temperature'] = temp
                self.model_tester._save_config()
                print("Temperature updated and saved")
            else:
                print("Temperature must be between 0.0 and 2.0")
        except ValueError:
            print("Invalid input")
        input("Press Enter to continue...")
    
    def _set_top_p(self):
        """Set top-p setting"""
        try:
            current = self.model_tester.test_config['top_p']
            top_p = float(input(f"Top-p (0.0-1.0, current: {current}): "))
            if 0.0 <= top_p <= 1.0:
                self.model_tester.test_config['top_p'] = top_p
                self.model_tester._save_config()
                print("Top-p updated and saved")
            else:
                print("Top-p must be between 0.0 and 1.0")
        except ValueError:
            print("Invalid input")
        input("Press Enter to continue...")
    
    def _set_top_k(self):
        """Set top-k setting"""
        try:
            current = self.model_tester.test_config['top_k']
            top_k = int(input(f"Top-k (current: {current}): "))
            if top_k > 0:
                self.model_tester.test_config['top_k'] = top_k
                self.model_tester._save_config()
                print("Top-k updated and saved")
            else:
                print("Top-k must be positive")
        except ValueError:
            print("Invalid input")
        input("Press Enter to continue...")
    
    def _set_max_tokens(self):
        """Set max tokens setting"""
        try:
            current = self.model_tester.test_config['max_tokens']
            tokens = int(input(f"Max tokens (current: {current}): "))
            if tokens > 0:
                self.model_tester.test_config['max_tokens'] = tokens
                self.model_tester._save_config()
                print("Max tokens updated and saved")
            else:
                print("Max tokens must be positive")
        except ValueError:
            print("Invalid input")
        input("Press Enter to continue...")
    
    def _set_timeout(self):
        """Set timeout setting"""
        try:
            current = self.model_tester.test_config['timeout_seconds']
            print(f"Current timeout: {self.model_tester.get_timeout_display()}")
            print("Enter timeout in seconds (0 = unlimited):")
            print("Common values: 300 (5min), 600 (10min), 1800 (30min), 3600 (1hour)")
            
            timeout = int(input(f"Timeout seconds (current: {current}): "))
            if timeout >= 0:
                self.model_tester.test_config['timeout_seconds'] = timeout
                self.model_tester._save_config()
                print(f"Timeout updated and saved: {self.model_tester.get_timeout_display()}")
                if timeout == 0:
                    print("WARNING: Unlimited timeout set - generation may take very long")
            else:
                print("Timeout must be 0 or positive")
        except ValueError:
            print("Invalid input")
        input("Press Enter to continue...")
