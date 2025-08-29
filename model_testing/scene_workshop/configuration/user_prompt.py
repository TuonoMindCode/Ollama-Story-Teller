import os

class UserPromptConfigurator:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def configure_user_prompt(self):
        """Configure user prompt with persistent saving"""
        print("\nUSER PROMPT CONFIGURATION")
        print("="*50)
        print("The user prompt provides the scene context and story instructions.")
        print("This is what you want the AI to write about.")
        
        # Show current system prompt for context
        current_system = self.workshop.settings.get('system_prompt_name', 'Not selected') if self.workshop.settings else 'Not selected'
        print(f"\nCurrent system prompt: {current_system}")
        
        print("\nOptions:")
        print("1. Load from template file")
        print("2. Use built-in Romance Scene")
        print("3. Use built-in Action Scene") 
        print("4. Use built-in Dialogue Scene")
        print("5. Enter custom user prompt")
        print("6. Clear current selection")
        print("0. Back to main menu")
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            self._load_from_file()
        elif choice == '2':
            self._use_builtin_romance_scene()
        elif choice == '3':
            self._use_builtin_action_scene()
        elif choice == '4':
            self._use_builtin_dialogue_scene()
        elif choice == '5':
            self._enter_custom_prompt()
        elif choice == '6':
            self._clear_prompt()
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

    def _load_from_file(self):
        """Load user prompt from template file - UPDATED for laboratory structure"""
        # Updated to use new laboratory folder structure
        template_dir = "laboratory/templates/user_prompts"
        
        if not os.path.exists(template_dir):
            print(f"Template directory not found: {template_dir}")
            print("Creating template directory...")
            try:
                os.makedirs(template_dir, exist_ok=True)
                print(f"✅ Created directory: {template_dir}")
                print("You can now add .txt files to this directory for user prompts.")
            except Exception as e:
                print(f"❌ Failed to create directory: {e}")
            input("Press Enter to continue...")
            return
        
        all_files = [f for f in os.listdir(template_dir) if f.endswith('.txt')]
        
        if not all_files:
            print("No template files found.")
            print(f"Add .txt files to: {template_dir}")
            print("\nTip: Use the Template Manager to create user prompt templates,")
            print("or manually create .txt files in the laboratory/templates/user_prompts/ folder.")
            input("Press Enter to continue...")
            return
        
        # Check if current system prompt has a matching template
        current_system_name = self.workshop.settings.get('system_prompt_name', '') if self.workshop.settings else ''
        system_template_name = None
        
        if 'Template:' in current_system_name:
            system_template_name = current_system_name.replace('Template: ', '').strip()
        
        # Categorize files
        matching_files = []
        other_files = []
        
        for filename in all_files:
            base_name = filename.replace('.txt', '')
            if system_template_name and base_name == system_template_name:
                matching_files.append(filename)
            else:
                other_files.append(filename)
        
        print("\nAvailable user prompt templates:")
        
        # Show matching files first
        file_list = []
        if matching_files:
            print("\n🎯 RECOMMENDED (matches your system prompt):")
            for filename in matching_files:
                file_list.append(filename)
                self._display_file_info(len(file_list), filename, template_dir, "🎯")
        
        if other_files:
            print(f"\n📝 OTHER TEMPLATES:")
            for filename in other_files:
                file_list.append(filename)
                self._display_file_info(len(file_list), filename, template_dir)
        
        print(" 0. Cancel")
        
        try:
            choice = int(input(f"\nSelect template (0-{len(file_list)}): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(file_list):
                selected_file = file_list[choice - 1]
                filepath = os.path.join(template_dir, selected_file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                # Check compatibility
                self._check_prompt_compatibility(selected_file)
                
                # Save to persistent settings
                if self.workshop.settings:
                    self.workshop.settings.set('user_prompt', content)
                    self.workshop.settings.set('user_prompt_name', f'Template: {selected_file.replace(".txt", "")}')
                    self.workshop.settings.set('user_prompt_source', filepath)
                
                print(f"✅ User prompt loaded from {selected_file}")
                print(f"Preview: {content[:150]}...")
                
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
        
        input("Press Enter to continue...")

    def _display_file_info(self, index, filename, template_dir, prefix=""):
        """Display file information in the list"""
        filepath = os.path.join(template_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                word_count = len(content.split())
                preview = content[:60] + "..." if len(content) > 60 else content
            print(f"{index:2d}. {prefix} {filename:<25} ({word_count:3d} words) - {preview}")
        except Exception as e:
            print(f"{index:2d}. {prefix} {filename:<25} (Error reading file: {e})")

    def _check_prompt_compatibility(self, user_filename):
        """Check compatibility between system and user prompts"""
        current_system_name = self.workshop.settings.get('system_prompt_name', '') if self.workshop.settings else ''
        base_name = user_filename.replace('.txt', '')
        
        # Check if names match
        if 'Template:' in current_system_name:
            system_template_name = current_system_name.replace('Template: ', '').strip()
            if base_name == system_template_name:
                print(f"\n✅ PERFECT MATCH!")
                print(f"This user prompt is designed to work with your current system prompt.")
                return
        
        # Check for type mismatches
        system_is_story = 'story' in current_system_name.lower()
        user_is_story = 'story' in base_name.lower()
        
        if system_is_story and not user_is_story:
            print(f"\n⚠️  TYPE MISMATCH WARNING")
            print(f"Your system prompt appears to be story-oriented: '{current_system_name}'")
            print(f"But this user prompt appears to be scene-oriented: '{base_name}'")
            print("This may produce inconsistent results. Consider using matching prompt types.")
        elif not system_is_story and user_is_story:
            print(f"\n⚠️  TYPE MISMATCH WARNING")
            print(f"Your system prompt appears to be scene-oriented: '{current_system_name}'")
            print(f"But this user prompt appears to be story-oriented: '{base_name}'")
            print("This may produce inconsistent results. Consider using matching prompt types.")

    def _use_builtin_romance_scene(self):
        """Use built-in romance scene prompt"""
        romance_prompt = """Write a romantic scene between two characters who have been friends for years but are just realizing their deeper feelings. 

The scene should take place in a cozy coffee shop on a rainy evening. One character has just returned from a long trip abroad and they're catching up. Include meaningful dialogue, subtle romantic tension, and sensory details about the warm atmosphere contrasting with the storm outside.

Focus on the emotional undercurrent and the moment of realization. Make it tender and authentic."""

        if self.workshop.settings:
            self.workshop.settings.set('user_prompt', romance_prompt)
            self.workshop.settings.set('user_prompt_name', 'Built-in: Romance Scene')
            self.workshop.settings.set('user_prompt_source', None)
        
        print("✅ Built-in Romance Scene prompt selected")
        print(f"Preview: {romance_prompt[:150]}...")
        input("Press Enter to continue...")

    def _use_builtin_action_scene(self):
        """Use built-in action scene prompt"""
        action_prompt = """Write an intense action scene where a skilled thief is trying to escape from a high-security building after a heist has gone wrong. 

The protagonist must navigate laser security systems, avoid guards, and deal with a betrayal from their partner. The scene should be fast-paced with detailed descriptions of their movements, the environment, and the increasing tension as time runs out.

Include physical obstacles, split-second decisions, and a clever escape solution. Make it thrilling and cinematic."""

        if self.workshop.settings:
            self.workshop.settings.set('user_prompt', action_prompt)
            self.workshop.settings.set('user_prompt_name', 'Built-in: Action Scene')
            self.workshop.settings.set('user_prompt_source', None)
        
        print("✅ Built-in Action Scene prompt selected")
        print(f"Preview: {action_prompt[:150]}...")
        input("Press Enter to continue...")

    def _use_builtin_dialogue_scene(self):
        """Use built-in dialogue scene prompt"""
        dialogue_prompt = """Write a scene that is primarily dialogue-driven, where two siblings are having a difficult conversation about their recently deceased parent's estate. 

One sibling wants to sell the family home, while the other wants to keep it. The scene should reveal their different personalities, their relationship dynamics, and underlying emotions about loss and family history.

Use dialogue to show their conflict, but also their love for each other. Include minimal action tags and focus on what they say and how they say it to reveal character and advance the emotional conflict."""

        if self.workshop.settings:
            self.workshop.settings.set('user_prompt', dialogue_prompt)
            self.workshop.settings.set('user_prompt_name', 'Built-in: Dialogue Scene')
            self.workshop.settings.set('user_prompt_source', None)
        
        print("✅ Built-in Dialogue Scene prompt selected")
        print(f"Preview: {dialogue_prompt[:150]}...")
        input("Press Enter to continue...")

    def _enter_custom_prompt(self):
        """Enter custom user prompt"""
        print("\nENTER CUSTOM USER PROMPT")
        print("-" * 30)
        print("Enter your custom user prompt (press Enter on empty line to finish):")
        print("(This describes the scene/story you want the AI to write)")
        
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
                    self._save_as_template(custom_prompt, filename, 'user_prompts')
            
            if self.workshop.settings:
                self.workshop.settings.set('user_prompt', custom_prompt)
                self.workshop.settings.set('user_prompt_name', 'Custom User Prompt')
                self.workshop.settings.set('user_prompt_source', None)
            
            print("✅ Custom user prompt saved")
            print(f"Preview: {custom_prompt[:150]}...")
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
        """Clear current user prompt"""
        if self.workshop.settings:
            self.workshop.settings.set('user_prompt', None)
            self.workshop.settings.set('user_prompt_name', 'Not selected')
            self.workshop.settings.set('user_prompt_source', None)
        print("✅ User prompt cleared")
        input("Press Enter to continue...")
