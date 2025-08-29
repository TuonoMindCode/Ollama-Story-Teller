import os
import glob
from datetime import datetime

class PromptManager:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def select_system_prompt(self):
        """System prompt selection with full template browsing"""
        while True:
            print("\nSELECT SYSTEM PROMPT")
            print("="*40)
            print("1. Choose from built-in prompts")
            print("2. Browse template files")
            print("3. Enter custom system prompt")
            print("4. View current system prompt")
            print("5. Clear current selection")
            print("6. Back to workshop")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._choose_builtin_system_prompts()
                break
            elif choice == "2":
                if self._browse_system_prompt_templates():
                    break
            elif choice == "3":
                self._enter_custom_system_prompt()
                break
            elif choice == "4":
                self._view_current_system_prompt()
            elif choice == "5":
                self._clear_system_prompt()
            elif choice == "6":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def select_user_prompt(self):
        """User prompt selection with full template browsing"""
        while True:
            print("\nSELECT USER PROMPT")
            print("="*40)
            print("1. Choose from built-in prompts")
            print("2. Browse template files")
            print("3. Enter custom user prompt")
            print("4. View current user prompt")
            print("5. Clear current selection")
            print("6. Back to workshop")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._choose_builtin_user_prompts()
                break
            elif choice == "2":
                if self._browse_user_prompt_templates():
                    break
            elif choice == "3":
                self._enter_custom_user_prompt()
                break
            elif choice == "4":
                self._view_current_user_prompt()
            elif choice == "5":
                self._clear_user_prompt()
            elif choice == "6":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def _choose_builtin_system_prompts(self):
        """Choose from built-in system prompts with detailed descriptions"""
        prompts = [
            ("General Creative Writer", 
             "You are a skilled creative writer. Write engaging, detailed scenes with vivid descriptions and compelling characters.",
             "Good all-purpose system prompt for most creative writing tasks."),
            
            ("Romance Novelist", 
             "You are an accomplished romance novelist. Focus on emotional depth, character chemistry, and intimate moments. Use sensual language and explore the feelings between characters.",
             "Specialized for romantic scenes with emotional focus."),
            
            ("Literary Fiction Author", 
             "You are a literary fiction author known for rich prose, deep character development, and meaningful themes. Use sophisticated language and explore the human condition.",
             "Creates more sophisticated, literary-style content."),
            
            ("Dialogue Master", 
             "You are a master of dialogue. Focus on creating natural, engaging conversations that reveal character personality and advance the plot. Make each character's voice distinct.",
             "Emphasizes realistic, character-driven dialogue."),
            
            ("Atmospheric Writer", 
             "You are skilled at creating rich, immersive atmospheres. Focus on sensory details, mood, and setting. Make readers feel like they are physically present in the scene.",
             "Creates vivid, immersive scene descriptions."),
            
            ("Minimalist Style", 
             "You write in a clean, minimalist style like Hemingway. Use simple, direct language. Let actions and dialogue speak for themselves. Avoid unnecessary description.",
             "Clean, understated writing style.")
        ]
        
        print("\nBUILT-IN SYSTEM PROMPTS")
        print("="*60)
        for i, (name, prompt, desc) in enumerate(prompts, 1):
            print(f"{i}. {name}")
            print(f"   Description: {desc}")
            print(f"   Preview: {prompt[:80]}...")
            print()
        
        try:
            choice = int(input(f"Select prompt (1-{len(prompts)}, 0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(prompts):
                name, prompt, desc = prompts[choice - 1]
                
                print(f"\nSelected: {name}")
                print(f"Full prompt:")
                print("-" * 50)
                print(prompt)
                print("-" * 50)
                
                confirm = input("\nUse this system prompt? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.workshop.current_settings['system_prompt'] = prompt
                    self.workshop.current_settings['system_prompt_name'] = f"[Built-in: {name}]"
                    self.workshop.current_settings['system_prompt_source'] = 'built-in'  # Mark as built-in
                    print(f"System prompt set: {name}")
                else:
                    print("System prompt not selected")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _choose_builtin_user_prompts(self):
        """Choose from built-in user prompts with scenarios"""
        prompts = [
            ("Coffee Shop Meeting", 
             "Write a scene where two people meet unexpectedly in a busy coffee shop. There's an instant connection between them.",
             "Classic meet-cute scenario"),
            
            ("Difficult Conversation", 
             "Write a scene where two characters must have a difficult conversation that will change their relationship forever.",
             "Emotional, dialogue-heavy scene"),
            
            ("Secret Revealed", 
             "Write a scene where a character discovers a secret that changes everything they thought they knew.",
             "Plot twist and emotional revelation"),
            
            ("Quiet Moment", 
             "Write a scene showing a quiet, intimate moment between two characters. Focus on subtle emotions and unspoken understanding.",
             "Character study, atmospheric"),
            
            ("Confrontation", 
             "Write a scene where two characters confront each other about a long-standing conflict. Emotions run high.",
             "Tension and conflict resolution"),
            
            ("Memory Lane", 
             "Write a scene where a character revisits a meaningful place from their past, triggering powerful memories and emotions.",
             "Nostalgic, introspective"),
            
            ("First Date Nerves", 
             "Write a scene of a first date where both characters are nervous but trying to impress each other. Include awkward but endearing moments.",
             "Romance with humor"),
            
            ("Late Night Diner", 
             "Write a scene set in a 24-hour diner at 3 AM. Two strangers end up sharing more than just coffee.",
             "Atmospheric, intimate conversation")
        ]
        
        print("\nBUILT-IN USER PROMPTS")
        print("="*60)
        for i, (name, prompt, desc) in enumerate(prompts, 1):
            print(f"{i}. {name}")
            print(f"   Type: {desc}")
            print(f"   Prompt: {prompt}")
            print()
        
        try:
            choice = int(input(f"Select prompt (1-{len(prompts)}, 0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(prompts):
                name, prompt, desc = prompts[choice - 1]
                self.workshop.current_settings['user_prompt'] = prompt
                self.workshop.current_settings['user_prompt_name'] = f"[Built-in: {name}]"
                self.workshop.current_settings['user_prompt_source'] = 'built-in'  # Mark as built-in
                print(f"User prompt set: {name}")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _browse_system_prompt_templates(self):
        """Browse and select from system prompt template files"""
        if not self.workshop.template_manager:
            print("Template Manager not available")
            input("Press Enter to continue...")
            return False
        
        # Get system prompt templates
        templates = self._get_system_prompt_templates()
        
        if not templates:
            print("\nNo system prompt templates found")
            print("Create some templates in Template Manager first!")
            print("\nTo create templates:")
            print("1. Go to Template Manager from main testing menu")
            print("2. Select 'Create System Prompt Template'")
            print("3. Choose genre and style, then write your prompt")
            input("Press Enter to continue...")
            return False
        
        while True:
            print("\nBROWSE SYSTEM PROMPT TEMPLATES")
            print("="*60)
            print(f"Found {len(templates)} system prompt templates:")
            print()
            
            # Group templates by genre/style for better display
            grouped = {}
            for filename, metadata in templates:
                key = f"{metadata.get('genre', 'Unknown')} - {metadata.get('style', 'Unknown')}"
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append((filename, metadata))
            
            template_list = []
            for group_name, group_templates in grouped.items():
                print(f"= {group_name} =")
                for filename, metadata in group_templates:
                    template_list.append((filename, metadata))
                    date_str = self._format_date(metadata.get('date'), metadata.get('time'))
                    print(f"{len(template_list):2d}. {filename}")
                    print(f"    Created: {date_str}")
                print()
            
            print("Enter number to PREVIEW and SELECT, or 0 to go back")
            
            try:
                choice = int(input("Choice: "))
                
                if choice == 0:
                    return False
                elif 1 <= choice <= len(template_list):
                    filename, metadata = template_list[choice - 1]
                    if self._preview_and_select_system_template(filename, metadata):
                        return True
                else:
                    print("Invalid choice")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input")
                input("Press Enter to continue...")
    
    def _browse_user_prompt_templates(self):
        """Browse and select from user prompt template files"""
        if not self.workshop.template_manager:
            print("Template Manager not available")
            input("Press Enter to continue...")
            return False
        
        templates = self._get_user_prompt_templates()
        
        if not templates:
            print("\nNo user prompt templates found")
            print("Create some templates in Template Manager first!")
            input("Press Enter to continue...")
            return False
        
        while True:
            print("\nBROWSE USER PROMPT TEMPLATES")
            print("="*60)
            print(f"Found {len(templates)} user prompt templates:")
            print()
            
            for i, (filename, metadata) in enumerate(templates, 1):
                date_str = self._format_date(metadata.get('date'), metadata.get('time'))
                # Clean up filename for display
                display_name = filename.replace('user_prompt_', '').replace('.txt', '').replace('_', ' ').title()
                print(f"{i:2d}. {display_name}")
                print(f"    File: {filename}")
                print(f"    Created: {date_str}")
                print()
            
            print("Enter number to PREVIEW and SELECT, or 0 to go back")
            
            try:
                choice = int(input("Choice: "))
                
                if choice == 0:
                    return False
                elif 1 <= choice <= len(templates):
                    filename, metadata = templates[choice - 1]
                    if self._preview_and_select_user_template(filename, metadata):
                        return True
                else:
                    print("Invalid choice")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input")
                input("Press Enter to continue...")
    
    def _get_system_prompt_templates(self):
        """Get list of system prompt templates"""
        if not self.workshop.template_manager:
            return []
        
        try:
            templates_folder = self.workshop.template_manager.templates_folder
            if not os.path.exists(templates_folder):
                return []
            
            # Look for system prompt template files
            pattern = os.path.join(templates_folder, "system_prompt_*.txt")
            files = glob.glob(pattern)
            
            templates = []
            for file_path in files:
                filename = os.path.basename(file_path)
                metadata = self._parse_template_metadata(file_path)
                templates.append((filename, metadata))
            
            # Sort by creation date (newest first)
            templates.sort(key=lambda x: (x[1].get('date', ''), x[1].get('time', '')), reverse=True)
            return templates
            
        except Exception as e:
            print(f"Error reading templates: {e}")
            return []
    
    def _get_user_prompt_templates(self):
        """Get list of user prompt templates"""
        if not self.workshop.template_manager:
            return []
        
        try:
            templates_folder = self.workshop.template_manager.templates_folder
            if not os.path.exists(templates_folder):
                return []
            
            # Look for user prompt template files
            pattern = os.path.join(templates_folder, "user_prompt_*.txt")
            files = glob.glob(pattern)
            
            templates = []
            for file_path in files:
                filename = os.path.basename(file_path)
                metadata = self._parse_template_metadata(file_path)
                templates.append((filename, metadata))
            
            # Sort by creation date (newest first)
            templates.sort(key=lambda x: (x[1].get('date', ''), x[1].get('time', '')), reverse=True)
            return templates
            
        except Exception as e:
            print(f"Error reading templates: {e}")
            return []
    
    def _parse_template_metadata(self, file_path):
        """Parse metadata from template file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            metadata = {}
            for line in lines[:10]:  # Check first 10 lines for metadata
                if line.startswith('# '):
                    if 'Genre:' in line:
                        metadata['genre'] = line.split('Genre:')[1].strip()
                    elif 'Style:' in line:
                        metadata['style'] = line.split('Style:')[1].strip()
                    elif 'Date:' in line:
                        metadata['date'] = line.split('Date:')[1].strip()
                    elif 'Time:' in line:
                        metadata['time'] = line.split('Time:')[1].strip()
            
            return metadata
            
        except Exception:
            return {}
    
    def _preview_and_select_system_template(self, filename, metadata):
        """Preview system template and allow selection"""
        templates_folder = self.workshop.template_manager.templates_folder
        filepath = os.path.join(templates_folder, filename)
        
        if not os.path.exists(filepath):
            print("Template file not found")
            input("Press Enter to continue...")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Remove metadata lines from content
            lines = content.split('\n')
            content_lines = []
            for line in lines:
                if not line.startswith('# '):
                    content_lines.append(line)
            
            clean_content = '\n'.join(content_lines).strip()
            
            print(f"\nSYSTEM PROMPT TEMPLATE PREVIEW")
            print("="*60)
            print(f"File: {filename}")
            print(f"Genre: {metadata.get('genre', 'Unknown')}")
            print(f"Style: {metadata.get('style', 'Unknown')}")
            print(f"Created: {self._format_date(metadata.get('date'), metadata.get('time'))}")
            print()
            
            # Analyze prompt features
            print("Detected Features:")
            content_lower = clean_content.lower()
            features = []
            if 'first person' in content_lower or '"i"' in content_lower:
                features.append("First Person Guidance")
            if 'second person' in content_lower or '"you"' in content_lower:
                features.append("Second Person Style")
            if 'dialogue' in content_lower:
                features.append("Dialogue Focus")
            if 'sensory' in content_lower or 'sensual' in content_lower:
                features.append("Sensory Details")
            if 'romance' in content_lower:
                features.append("Romance Elements")
            if 'internal' in content_lower or 'thoughts' in content_lower:
                features.append("Internal Monologue")
            
            for feature in features[:4]:  # Show max 4 features
                print(f"• {feature}")
            print()
            
            print("Content:")
            print("-" * 60)
            print(clean_content)
            print("-" * 60)
            
            action = input(f"\nUse this system prompt? (y/n): ").strip().lower()
            
            if action == 'y':
                self.workshop.current_settings['system_prompt'] = clean_content
                
                # Store source information for better display
                folder_name = os.path.basename(templates_folder)
                self.workshop.current_settings['system_prompt_source'] = filepath
                self.workshop.current_settings['system_prompt_name'] = f"[Template: {folder_name}/{filename}]"
                
                # Also store genre/style info if available
                genre = metadata.get('genre', 'Unknown')
                style = metadata.get('style', 'Unknown')
                if genre != 'Unknown' and style != 'Unknown':
                    self.workshop.current_settings['system_prompt_description'] = f"{genre} - {style}"
                
                print(f"Selected system prompt: {folder_name}/{filename}")
                input("Press Enter to continue...")
                return True
            
        except Exception as e:
            print(f"Error reading template: {e}")
            input("Press Enter to continue...")
        
        return False
    
    def _preview_and_select_user_template(self, filename, metadata):
        """Preview user template and allow selection"""
        templates_folder = self.workshop.template_manager.templates_folder
        filepath = os.path.join(templates_folder, filename)
        
        if not os.path.exists(filepath):
            print("Template file not found")
            input("Press Enter to continue...")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            print(f"\nUSER PROMPT TEMPLATE PREVIEW")
            print("="*60)
            print(f"File: {filename}")
            print(f"Created: {self._format_date(metadata.get('date'), metadata.get('time'))}")
            print()
            print("Content:")
            print("-" * 60)
            print(content)
            print("-" * 60)
            
            action = input(f"\nUse this user prompt? (y/n): ").strip().lower()
            
            if action == 'y':
                self.workshop.current_settings['user_prompt'] = content
                
                # Store source information for better display
                folder_name = os.path.basename(templates_folder)
                self.workshop.current_settings['user_prompt_source'] = filepath
                self.workshop.current_settings['user_prompt_name'] = f"[Template: {folder_name}/{filename}]"
                
                display_name = filename.replace('user_prompt_', '').replace('.txt', '').replace('_', ' ').title()
                print(f"Selected user prompt: {folder_name}/{filename}")
                input("Press Enter to continue...")
                return True
            
        except Exception as e:
            print(f"Error reading template: {e}")
            input("Press Enter to continue...")
        
        return False
    
    def _format_date(self, date_str, time_str):
        """Format date and time for display"""
        if date_str and time_str:
            return f"{date_str} {time_str}"
        elif date_str:
            return date_str
        else:
            return "Unknown"
    
    def _view_current_system_prompt(self):
        """View the currently selected system prompt"""
        if self.workshop.current_settings['system_prompt']:
            print(f"\nCURRENT SYSTEM PROMPT")
            print("="*50)
            print(f"Name: {self.workshop.current_settings['system_prompt_name']}")
            print(f"Length: {len(self.workshop.current_settings['system_prompt'])} characters")
            print()
            print("Content:")
            print("-" * 50)
            print(self.workshop.current_settings['system_prompt'])
            print("-" * 50)
        else:
            print("\nNo system prompt currently selected")
        
        input("Press Enter to continue...")
    
    def _view_current_user_prompt(self):
        """View the currently selected user prompt"""
        if self.workshop.current_settings['user_prompt']:
            print(f"\nCURRENT USER PROMPT")
            print("="*50)
            print(f"Name: {self.workshop.current_settings['user_prompt_name']}")
            print(f"Length: {len(self.workshop.current_settings['user_prompt'])} characters")
            print()
            print("Content:")
            print("-" * 50)
            print(self.workshop.current_settings['user_prompt'])
            print("-" * 50)
        else:
            print("\nNo user prompt currently selected")
        
        input("Press Enter to continue...")
    
    def _clear_system_prompt(self):
        """Clear the current system prompt selection"""
        if self.workshop.current_settings['system_prompt']:
            print(f"Current: {self.workshop.current_settings['system_prompt_name']}")
            confirm = input("Clear system prompt selection? (y/n): ").strip().lower()
            if confirm == 'y':
                self.workshop.current_settings['system_prompt'] = None
                self.workshop.current_settings['system_prompt_name'] = 'Not selected'
                print("System prompt cleared")
        else:
            print("No system prompt currently selected")
        
        input("Press Enter to continue...")
    
    def _clear_user_prompt(self):
        """Clear the current user prompt selection"""
        if self.workshop.current_settings['user_prompt']:
            print(f"Current: {self.workshop.current_settings['user_prompt_name']}")
            confirm = input("Clear user prompt selection? (y/n): ").strip().lower()
            if confirm == 'y':
                self.workshop.current_settings['user_prompt'] = None
                self.workshop.current_settings['user_prompt_name'] = 'Not selected'
                print("User prompt cleared")
        else:
            print("No user prompt currently selected")
        
        input("Press Enter to continue...")
    
    def _enter_custom_system_prompt(self):
        """Enter custom system prompt with helpful guidance"""
        print("\nENTER CUSTOM SYSTEM PROMPT")
        print("="*40)
        print("Tips for effective system prompts:")
        print("• Define the AI's role (e.g., 'You are a romance novelist')")
        print("• Specify writing style preferences")
        print("• Include perspective instructions (first/second/third person)")
        print("• Mention focus areas (dialogue, description, emotion)")
        print("• Keep it clear and specific")
        print()
        print("Enter your system prompt (press Enter twice when done):")
        print()
        
        lines = []
        empty_line_count = 0
        
        while True:
            line = input()
            if not line:
                empty_line_count += 1
                if empty_line_count >= 2 or (empty_line_count >= 1 and lines):
                    break
            else:
                empty_line_count = 0
                lines.append(line)
        
        if not lines:
            print("No system prompt entered")
            input("Press Enter to continue...")
            return
        
        custom_prompt = '\n'.join(lines).strip()
        
        print(f"\nYour System Prompt:")
        print("="*50)
        print(custom_prompt)
        print("="*50)
        print(f"Length: {len(custom_prompt)} characters")
        
        use = input("\nUse this system prompt? (y/n): ").strip().lower()
        if use == 'y':
            self.workshop.current_settings['system_prompt'] = custom_prompt
            self.workshop.current_settings['system_prompt_name'] = "[Custom]"
            self.workshop.current_settings['system_prompt_source'] = 'custom'  # Mark as custom
            print("Custom system prompt set")
            
            # Ask if they want to save as template
            save = input("Save as template for future use? (y/n): ").strip().lower()
            if save == 'y' and self.workshop.template_manager:
                self._save_as_system_template(custom_prompt)
        else:
            print("System prompt not used")
        
        input("Press Enter to continue...")
    
    def _enter_custom_user_prompt(self):
        """Enter custom user prompt with helpful guidance"""
        print("\nENTER CUSTOM USER PROMPT")
        print("="*40)
        print("Tips for effective user prompts:")
        print("• Be specific about the scene you want")
        print("• Include character details if relevant")
        print("• Specify the mood or tone")
        print("• Mention key elements (dialogue, action, emotion)")
        print("• Keep it focused but descriptive")
        print()
        print("Enter your user prompt (press Enter twice when done):")
        print()
        
        lines = []
        empty_line_count = 0
        
        while True:
            line = input()
            if not line:
                empty_line_count += 1
                if empty_line_count >= 2 or (empty_line_count >= 1 and lines):
                    break
            else:
                empty_line_count = 0
                lines.append(line)
        
        if not lines:
            print("No user prompt entered")
            input("Press Enter to continue...")
            return
        
        custom_prompt = '\n'.join(lines).strip()
        
        print(f"\nYour User Prompt:")
        print("="*50)
        print(custom_prompt)
        print("="*50)
        print(f"Length: {len(custom_prompt)} characters")
        
        use = input("\nUse this user prompt? (y/n): ").strip().lower()
        if use == 'y':
            self.workshop.current_settings['user_prompt'] = custom_prompt
            self.workshop.current_settings['user_prompt_name'] = "[Custom]"
            self.workshop.current_settings['user_prompt_source'] = 'custom'  # Mark as custom
            print("Custom user prompt set")
            
            # Ask if they want to save as template
            save = input("Save as template for future use? (y/n): ").strip().lower()
            if save == 'y' and self.workshop.template_manager:
                self._save_as_user_template(custom_prompt)
        else:
            print("User prompt not used")
        
        input("Press Enter to continue...")
    
    def _save_as_system_template(self, content):
        """Save custom system prompt as template"""
        try:
            print("\nSAVE AS SYSTEM PROMPT TEMPLATE")
            print("-" * 40)
            
            genre = input("Genre (e.g., Romance, Thriller, Literary): ").strip()
            style = input("Style (e.g., Minimalist, Descriptive, Dialogue): ").strip()
            
            if not genre:
                genre = "Custom"
            if not style:
                style = "Mixed"
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_prompt_{genre}_{style}_{timestamp}.txt"
            
            # Create content with metadata
            template_content = f"# Genre: {genre}\n# Style: {style}\n# Date: {datetime.now().strftime('%Y-%m-%d')}\n# Time: {datetime.now().strftime('%H:%M:%S')}\n\n{content}"
            
            filepath = os.path.join(self.workshop.template_manager.templates_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            print(f"Template saved: {filename}")
            
        except Exception as e:
            print(f"Error saving template: {e}")
        
        input("Press Enter to continue...")
    
    def _save_as_user_template(self, content):
        """Save custom user prompt as template"""
        try:
            print("\nSAVE AS USER PROMPT TEMPLATE")
            print("-" * 40)
            
            name = input("Template name (e.g., coffee_shop_meeting): ").strip()
            if not name:
                name = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Clean name for filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower()
            
            filename = f"user_prompt_{safe_name}.txt"
            
            filepath = os.path.join(self.workshop.template_manager.templates_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Template saved: {filename}")
            
        except Exception as e:
            print(f"Error saving template: {e}")
        
        input("Press Enter to continue...")
