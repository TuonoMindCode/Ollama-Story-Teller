import os

class SystemPromptConfigurator:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def configure_system_prompt(self):
        """Configure system prompt with persistent saving"""
        print("\nSYSTEM PROMPT CONFIGURATION")
        print("="*50)
        print("The system prompt defines the AI's role and behavior.")
        print("Choose from templates or create custom instructions.")
        print("\nOptions:")
        print("1. Load from template file")
        print("2. Use built-in Creative Writer")
        print("3. Use built-in Technical Writer")
        print("4. Enter custom system prompt")
        print("5. Clear current selection")
        print("0. Back to main menu")
        
        choice = input("\nSelect option (0-5): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            self._load_from_file()
        elif choice == '2':
            self._use_builtin_creative_writer()
        elif choice == '3':
            self._use_builtin_technical_writer()
        elif choice == '4':
            self._enter_custom_prompt()
        elif choice == '5':
            self._clear_prompt()
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

    def _load_from_file(self):
        """Load system prompt from template file - UPDATED for laboratory structure"""
        # Updated to use new laboratory folder structure
        template_dir = "laboratory/templates/system_prompts"
        
        if not os.path.exists(template_dir):
            print(f"Template directory not found: {template_dir}")
            print("Creating template directory...")
            try:
                os.makedirs(template_dir, exist_ok=True)
                print(f"✅ Created directory: {template_dir}")
                print("You can now add .txt files to this directory for system prompts.")
            except Exception as e:
                print(f"❌ Failed to create directory: {e}")
            input("Press Enter to continue...")
            return
        
        files = [f for f in os.listdir(template_dir) if f.endswith('.txt')]
        
        if not files:
            print("No template files found.")
            print(f"Add .txt files to: {template_dir}")
            print("\nTip: Use the Template Manager to create system prompt templates,")
            print("or manually create .txt files in the laboratory/templates/system_prompts/ folder.")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable system prompt templates:")
        for i, filename in enumerate(files, 1):
            filepath = os.path.join(template_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    word_count = len(content.split())
                    preview = content[:60] + "..." if len(content) > 60 else content
                print(f"{i:2d}. {filename:<25} ({word_count:3d} words) - {preview}")
            except Exception as e:
                print(f"{i:2d}. {filename:<25} (Error reading file: {e})")
        
        print(" 0. Cancel")
        
        try:
            choice = int(input(f"\nSelect template (0-{len(files)}): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(files):
                selected_file = files[choice - 1]
                filepath = os.path.join(template_dir, selected_file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                # Save to persistent settings (quietly)
                if self.workshop.settings:
                    self.workshop.settings.set('system_prompt', content, quiet=True)
                    self.workshop.settings.set('system_prompt_name', f'Template: {selected_file.replace(".txt", "")}', quiet=True)
                    self.workshop.settings.set('system_prompt_source', filepath, quiet=True)
                
                print(f"✅ System prompt loaded from {selected_file}")
                print(f"Preview: {content[:100]}...")
                
                # Check for matching user prompt and warn if needed
                self._check_prompt_compatibility(selected_file)
                
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
        
        input("Press Enter to continue...")

    def _check_prompt_compatibility(self, system_filename):
        """Check if there's a matching user prompt and provide guidance - UPDATED paths"""
        base_name = system_filename.replace('.txt', '')
        
        # Updated to use new laboratory folder structure
        user_template_dir = "laboratory/templates/user_prompts"
        matching_user_file = os.path.join(user_template_dir, f"{base_name}.txt")
        
        if os.path.exists(matching_user_file):
            print(f"\n💡 TEMPLATE PAIRING DETECTED")
            print(f"Found matching user prompt: {base_name}.txt")
            print("This system prompt is designed to work with its matching user prompt.")
            
            # Check current user prompt
            current_user_name = self.workshop.settings.get('user_prompt_name', 'Not selected') if self.workshop.settings else 'Not selected'
            
            if f"Template: {base_name}" not in current_user_name:
                print(f"⚠️  WARNING: Your current user prompt is '{current_user_name}'")
                print(f"Consider selecting the matching '{base_name}.txt' user prompt for best results.")
                
                load_matching = input("Would you like to load the matching user prompt now? (y/n): ").lower()
                if load_matching == 'y':
                    self._load_matching_user_prompt(matching_user_file, base_name)
        else:
            # Check if this is a story-type prompt without a match
            if 'story' in base_name.lower():
                print(f"\n⚠️  PROMPT TYPE WARNING")
                print(f"'{base_name}' appears to be a story-oriented system prompt.")
                print("Make sure your user prompt is also story-oriented, not scene-oriented.")
                print("Story prompts generate complete narratives, while scene prompts focus on specific moments.")

    def _load_matching_user_prompt(self, user_filepath, base_name):
        """Load the matching user prompt"""
        try:
            with open(user_filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if self.workshop.settings:
                self.workshop.settings.set('user_prompt', content, quiet=True)
                self.workshop.settings.set('user_prompt_name', f'Template: {base_name}', quiet=True)
                self.workshop.settings.set('user_prompt_source', user_filepath, quiet=True)
            
            print(f"✅ Matching user prompt loaded: {base_name}.txt")
            print(f"Preview: {content[:100]}...")
            
        except Exception as e:
            print(f"❌ Failed to load matching user prompt: {e}")

    def _use_builtin_creative_writer(self):
        """Use built-in creative writer system prompt"""
        creative_prompt = """You are a skilled creative writer specializing in vivid, engaging storytelling. Your writing style includes:

- Rich, descriptive language that paints clear mental pictures
- Strong character development and emotional depth  
- Compelling dialogue that reveals personality and advances plot
- Atmospheric details that immerse readers in the scene
- Varied sentence structure for natural rhythm and flow
- Show-don't-tell techniques to engage readers actively

Focus on creating memorable, emotionally resonant scenes that leave lasting impressions. Write with passion and creativity while maintaining narrative coherence."""

        if self.workshop.settings:
            self.workshop.settings.set('system_prompt', creative_prompt, quiet=True)
            self.workshop.settings.set('system_prompt_name', 'Built-in: Creative Writer', quiet=True)
            self.workshop.settings.set('system_prompt_source', None, quiet=True)
        
        print("✅ Built-in Creative Writer system prompt selected")
        print(f"Preview: {creative_prompt[:100]}...")
        input("Press Enter to continue...")

    def _use_builtin_technical_writer(self):
        """Use built-in technical writer system prompt"""
        technical_prompt = """You are a precise technical writer focused on clear, informative communication. Your writing style includes:

- Clear, concise language that conveys information efficiently
- Logical structure and organization
- Accurate, factual content with attention to detail
- Professional tone appropriate for the subject matter
- Step-by-step explanations when needed
- Consistent terminology and style

Focus on delivering information clearly and effectively, ensuring readers can easily understand and follow your content."""

        if self.workshop.settings:
            self.workshop.settings.set('system_prompt', technical_prompt, quiet=True)
            self.workshop.settings.set('system_prompt_name', 'Built-in: Technical Writer', quiet=True)
            self.workshop.settings.set('system_prompt_source', None, quiet=True)
        
        print("✅ Built-in Technical Writer system prompt selected")
        print(f"Preview: {technical_prompt[:100]}...")
        input("Press Enter to continue...")

    def _enter_custom_prompt(self):
        """Enter custom system prompt"""
        print("\nENTER CUSTOM SYSTEM PROMPT")
        print("-" * 30)
        print("Enter your custom system prompt (press Enter on empty line to finish):")
        print("(This defines the AI's role, behavior, and writing style)")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        if lines:
            custom_prompt = '\n'.join(lines)
            
            # Option to save as template
            save_template = input("\nWould you like to save this as a template file? (y/n): ").lower()
            if save_template == 'y':
                filename = input("Enter filename (without .txt extension): ").strip()
                if filename:
                    self._save_as_template(custom_prompt, filename, 'system_prompts')
            
            if self.workshop.settings:
                self.workshop.settings.set('system_prompt', custom_prompt, quiet=True)
                self.workshop.settings.set('system_prompt_name', 'Custom System Prompt', quiet=True)
                self.workshop.settings.set('system_prompt_source', None, quiet=True)
            
            print("✅ Custom system prompt saved")
            print(f"Preview: {custom_prompt[:100]}...")
        else:
            print("No content entered.")
        
        input("Press Enter to continue...")

    def _save_as_template(self, content, filename, prompt_type):
        """Save prompt as template file - UPDATED for laboratory structure"""
        # Updated to use new laboratory folder structure
        template_dir = f"laboratory/templates/{prompt_type}"
        os.makedirs(template_dir, exist_ok=True)
        
        filepath = os.path.join(template_dir, f"{filename}.txt")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Template saved as: {filepath}")
        except Exception as e:
            print(f"❌ Failed to save template: {e}")

    def _clear_prompt(self):
        """Clear current system prompt"""
        if self.workshop.settings:
            self.workshop.settings.set('system_prompt', None, quiet=True)
            self.workshop.settings.set('system_prompt_name', 'Not selected', quiet=True)
            self.workshop.settings.set('system_prompt_source', None, quiet=True)
        print("✅ System prompt cleared")
        input("Press Enter to continue...")
