import os
from .prompt_manager import PromptManager
from .style_manager import StyleManager
from .parameter_manager import ParameterManager
from .generator import Generator
from .second_prompt import SecondPromptManager
from .results_analyzer import ResultsAnalyzer
from .workshop import SceneWorkshop

class SceneWorkshop:
    def __init__(self, model_tester, template_manager):
        self.model_tester = model_tester
        self.template_manager = template_manager
        self.length_handler = None
        self.current_settings = {}
        
    def set_length_handler(self, length_handler):
        """Set the length handler for this workshop"""
        self.length_handler = length_handler
    
    def generate_with_length_config(self, system_prompt, user_prompt):
        """Generate content using current length configuration"""
        # Get length config from template manager if available
        if hasattr(self.template_manager, 'length_config') and self.template_manager.length_config:
            length_config = self.template_manager.length_config
            
            # Enhance user prompt with length requirements
            enhanced_user_prompt = self.template_manager.enhance_prompt_with_length(user_prompt)
            
            # Get appropriate max_tokens
            max_tokens = self.template_manager.get_max_tokens_for_generation()
            
            # Update model config temporarily
            original_max_tokens = self.model_tester.test_config.get('max_tokens')
            self.model_tester.test_config['max_tokens'] = max_tokens
            
            print(f"Using length config: {length_config['description']}")
            print(f"Target: {length_config['words']} words")
            print(f"Max tokens: {max_tokens}")
            
            try:
                # Generate with enhanced prompt
                result = self.model_tester.test_model(system_prompt, enhanced_user_prompt)
                return result
            finally:
                # Restore original max_tokens
                if original_max_tokens is not None:
                    self.model_tester.test_config['max_tokens'] = original_max_tokens
        else:
            # Use regular generation if no length config
            return self.model_tester.test_model(system_prompt, user_prompt)
    
    def run_workshop_menu(self):
        """Main workshop interface"""
        while True:
            self._display_status()
            
            choice = input("\nSelect option (1-13): ").strip()
            
            if choice == "1":
                self.prompt_manager.select_system_prompt()
            elif choice == "2":
                self.prompt_manager.select_user_prompt()
            elif choice == "3":
                self.style_manager.select_narrative_style()
            elif choice == "4":
                self.style_manager.select_writing_style()
            elif choice == "5":
                self.parameter_manager.configure_parameters()
            elif choice == "6":
                self.second_prompt.select_second_prompt()
            elif choice == "7":
                self.generator.generate_single_scene()
            elif choice == "8":
                self._set_scene_count()
            elif choice == "9":
                self.generator.generate_multiple_scenes()
            elif choice == "10":
                self.parameter_manager.preview_parameter_progression()
            elif choice == "11":
                self.results_analyzer.analyze_recent_results()
            elif choice == "12":
                self._workshop_help()
            elif choice == "13":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def _display_status(self):
        """Display current workshop status"""
        print("\n" + "="*70)
        print("SCENE WORKSHOP")
        print("="*70)
    
        print("Current Settings:")
        print(f"Model: {self.model_tester.get_short_model_name()}")
    
        # Enhanced System Prompt display with preview
        if self.current_settings['system_prompt']:
            sys_prompt = self.current_settings['system_prompt']
            word_count = len(sys_prompt.split())
        
            # Create a 2-line preview (about 100-120 characters)
            if len(sys_prompt) > 120:
                # Find a good break point near 60 characters for first line
                first_break = sys_prompt.find('. ', 40, 80)
                if first_break == -1:
                    first_break = sys_prompt.find(' ', 55, 75)
                if first_break == -1:
                    first_break = 60
                
                first_line = sys_prompt[:first_break].strip()
                remaining = sys_prompt[first_break:].strip()
                
                # Second line - another 60 characters or so
                if len(remaining) > 60:
                    second_break = remaining.find('. ', 40, 80)
                    if second_break == -1:
                        second_break = remaining.find(' ', 55, 75)
                    if second_break == -1:
                        second_break = 60
                    second_line = remaining[:second_break].strip() + "..."
                else:
                    second_line = remaining
                
                preview = f'"{first_line}\n{second_line}"'
            else:
                preview = f'"{sys_prompt}"'
            
            print(f"System Prompt ({word_count} words): {preview}")
        else:
            print("System Prompt: Not selected")
    
        # Enhanced User Prompt display with preview
        if self.current_settings['user_prompt']:
            user_prompt = self.current_settings['user_prompt']
            word_count = len(user_prompt.split())
        
            # Create a 2-line preview
            if len(user_prompt) > 120:
                first_break = user_prompt.find('. ', 40, 80)
                if first_break == -1:
                    first_break = user_prompt.find(' ', 55, 75)
                if first_break == -1:
                    first_break = 60
                
                first_line = user_prompt[:first_break].strip()
                remaining = user_prompt[first_break:].strip()
                
                if len(remaining) > 60:
                    second_break = remaining.find('. ', 40, 80)
                    if second_break == -1:
                        second_break = remaining.find(' ', 55, 75)
                    if second_break == -1:
                        second_break = 60
                    second_line = remaining[:second_break].strip() + "..."
                else:
                    second_line = remaining
                
                preview = f'"{first_line}\n{second_line}"'
            else:
                preview = f'"{user_prompt}"'
            
            print(f"User Prompt ({word_count} words): {preview}")
        else:
            print("User Prompt: Not selected")
    
        print(f"Second User Prompt: {self.second_prompt.get_display_name()}")
        print(f"Parameters: {self.parameter_manager.get_parameter_display()}")
        print(f"Timeout: {self.model_tester.get_timeout_display()}")
        print("="*70)
    
        ready = self._check_ready()
    
        # Enhanced configuration section
        print("\nESSENTIAL Configuration:")
    
        # System Prompt status with source info
        if self.current_settings['system_prompt']:
            sys_source = self._get_prompt_source('system')
            print(f"1. Select System Prompt: {sys_source}")
        else:
            print("1. Select System Prompt: None selected")
        print("   → Load from template file, use built-in instructions, or enter custom AI behavior guidelines")
    
        # User Prompt status with source info
        if self.current_settings['user_prompt']:
            user_source = self._get_prompt_source('user')
            print(f"2. Select User Prompt: {user_source}")
        else:
            print("2. Select User Prompt: None selected (adds perspective guidance to user prompt)")
    
        # Enhanced OPTIONAL Enhancements section
        print("\nOPTIONAL Enhancements:")
    
        # Narrative Style with current selection
        narrative_name = self.current_settings['narrative_style_name']
        if narrative_name and narrative_name != 'Not selected':
            print(f"3. Select Narrative Style: {narrative_name} enhancement added to user prompt")
        else:
            print("3. Select Narrative Style: None selected (adds perspective guidance to user prompt)")
    
        # Writing Style with current selection
        writing_name = self.current_settings['writing_style_name']
        if writing_name and writing_name != 'Not selected':
            print(f"4. Select Writing Style: {writing_name} enhancement added to user prompt")
        else:
            print("4. Select Writing Style: None selected (adds style guidance to user prompt)")
    
        # Parameters with current settings
        param_display = self.parameter_manager.get_parameter_display()
        print(f"5. Configure Parameters & Ranges: {param_display}")
    
        # Second User Prompt with current selection
        second_prompt_display = self.second_prompt.get_display_name()
        if second_prompt_display and second_prompt_display != 'Not selected':
            print(f"6. Select Second User Prompt(s): {second_prompt_display}")
        else:
            print("6. Select Second User Prompt(s): None selected (for story improvement)")
    
        # Show generation section with full descriptions regardless of ready state
        if ready:
            print("\nGeneration:")
        else:
            print("\nGeneration (Need system prompt, user prompt, and model configured first):")
    
        print("7. Generate Single Scene with Streaming")
        print("   → Creates one story with real-time output, applies improvements, saves complete results")
        print(f"8. Scene Count: [{self.current_settings['scene_count']}] - Generate multiple versions of the same scene")
        print("   → Creates X variations using same system/user prompts with different AI parameters + improvements")
        print("9. Generate Multiple Scenes with Variations")
        print("   → Creates batch of stories testing different AI parameters (temperature, top_p, top_k)")
        print("10. Preview Parameter Progression")
        print("    → Shows how parameters will change across multiple scenes before generation")
    
        print("\nAnalysis & Help:")
        print("11. Analyze Recent Results")
        print("    → Compare generated stories, analyze parameter effects, and find optimal settings")
        print("12. Workshop Help & Tips")
        print("    → Detailed guidance on prompts, parameters, and best practices")
        print("13. Back to Testing Menu")
    
    def _check_ready(self):
        """Check if ready to generate"""
        return (
            self.model_tester.test_config.get('model') and
            self.current_settings['system_prompt'] and
            self.current_settings['user_prompt']
        )
    
    def _set_scene_count(self):
        """Set number of scenes to generate"""
        try:
            count = int(input(f"Scene count (1-100) [{self.current_settings['scene_count']}]: ") or self.current_settings['scene_count'])
            if 1 <= count <= 100:
                self.current_settings['scene_count'] = count
                print(f"Scene count set to: {count}")
            else:
                print("Count must be between 1 and 100")
        except ValueError:
            print("Invalid number")
        
        input("Press Enter to continue...")
    
    def _workshop_help(self):
        """Display workshop help and tips"""
        print("\nSCENE WORKSHOP HELP & TIPS")
        print("="*50)
        print("The Scene Workshop helps you test and refine AI story generation.")
        print()
        
        print("GETTING STARTED:")
        print("1. Select a system prompt (defines AI's role and style)")
        print("2. Select a user prompt (describes the scene to generate)")
        print("3. Optionally configure narrative/writing styles")
        print("4. Generate a single scene to test your setup")
        print()
        
        print("SYSTEM PROMPT TIPS:")
        print("• Define the AI's role clearly (e.g., 'You are a romance novelist')")
        print("• Specify preferred writing style and perspective")
        print("• Include focus areas (dialogue, description, emotion)")
        print("• Keep instructions clear and specific")
        print()
        
        print("USER PROMPT TIPS:")
        print("• Be specific about the scene you want")
        print("• Include character details and relationships")
        print("• Specify mood, setting, and key elements")
        print("• Avoid being too prescriptive - leave room for creativity")
        print()
        
        print("PARAMETER GUIDANCE:")
        print("• Temperature: 0.3-0.7 (focused) | 0.8-1.2 (balanced) | 1.3+ (creative)")
        print("• Top-p: 0.7-0.9 (focused) | 0.85-0.95 (balanced) | 0.95+ (diverse)")
        print("• Top-k: 20-40 (focused) | 30-60 (balanced) | 50+ (diverse)")
        print()
        
        print("SECOND USER PROMPT:")
        print("• Applied after initial generation to improve the story")
        print("• Good for adding emotion, detail, or specific elements")
        print("• Test different improvement prompts to see effects")
        print()
        
        print("BATCH TESTING:")
        print("• Use multiple scenes to test parameter variations")
        print("• Incremental mode: gradually changes parameters")
        print("• Random mode: explores parameter space")
        print("• Use results analysis to find optimal settings")
        print()
        
        print("BEST PRACTICES:")
        print("• Start with built-in prompts, then customize")
        print("• Test single scenes before batch generation")
        print("• Save good prompts as templates for reuse")
        print("• Use results analysis to optimize your setup")
        print("• Experiment with different models for comparison")
        
        input("\nPress Enter to continue...")
    
    def _get_prompt_source(self, prompt_type):
        """Get descriptive source information for a prompt"""
        if prompt_type == 'system':
            name = self.current_settings['system_prompt_name']
            prompt = self.current_settings['system_prompt']
            # Check if we have stored the source path
            source_path = self.current_settings.get('system_prompt_source', '')
        else:
            name = self.current_settings['user_prompt_name']
            prompt = self.current_settings['user_prompt']
            # Check if we have stored the source path
            source_path = self.current_settings.get('user_prompt_source', '')
    
        if not prompt:
            return "None selected"
    
        word_count = len(prompt.split())
    
        # If we have a source path, use it
        if source_path:
            if os.path.exists(source_path):
                # Get folder name and filename
                folder_name = os.path.basename(os.path.dirname(source_path))
                filename = os.path.basename(source_path)
                return f"Template: {folder_name}/{filename} ({word_count} words)"
            else:
                # File might have been moved, just show the filename
                filename = os.path.basename(source_path)
                return f"Template: {filename} ({word_count} words)"
    
        # Fallback to parsing the name field
        if name and '[Template:' in name:
            # Extract template name and try to show more info
            template_info = name.replace('[Template: ', '').replace(']', '')
            if 'Unknown' not in template_info and template_info:
                return f"Template: {template_info} ({word_count} words)"
        elif name and '[Built-in:' in name:
            # Extract built-in name
            built_in_name = name.replace('[Built-in: ', '').replace(']', '')
            return f"Built-in: {built_in_name} ({word_count} words)"
        elif name and '/' in name:
            # Looks like a path
            parts = name.split('/')
            if len(parts) >= 2:
                folder = parts[-2]
                filename = parts[-1]
                return f"Template: {folder}/{filename} ({word_count} words)"
            else:
                return f"Template: {parts[-1]} ({word_count} words)"
        elif name and name not in ['Not selected', 'Custom', 'Unknown-Unknown'] and 'Unknown' not in name:
            return f"{name} ({word_count} words)"
        else:
            return f"Custom prompt ({word_count} words)"
