import os
import datetime
import glob
from typing import Dict, List, Optional, Tuple
from .base_template_manager import BaseTemplateManager

class UserPromptManager(BaseTemplateManager):
    def __init__(self, templates_folder: str, model_tester):
        super().__init__(templates_folder)
        self.model_tester = model_tester
    
    def run_user_prompt_manager(self):
        """User prompt manager menu"""
        while True:
            user_prompts = self._get_user_prompts()
            
            print("\n" + "="*50)
            print("USER PROMPT MANAGER")
            print("="*50)
            print(f"Found {len(user_prompts)} user prompts")
            print()
            print("1. Write Scene Prompt (write your own scene description)")
            print("2. AI-Generate Scene Ideas (get 5 random creative scene ideas)")
            print("3. AI-Generate Detailed Scene Setup (comprehensive scene with all details)")
            print("4. AI-Generate Scene Type Variations (multiple versions of same scene type)")
            print("5. Choose from Scene Templates (pre-built common scenes)")
            print("6. Browse/View User Prompts")
            print("7. Delete User Prompt")
            print("8. Back to Template Manager")
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == "1":
                self._write_custom_user_prompt()
            elif choice == "2":
                self._ai_generate_scene_ideas()
            elif choice == "3":
                self._ai_generate_detailed_scene_setup()
            elif choice == "4":
                self._ai_generate_scene_type_variations()
            elif choice == "5":
                self._choose_scene_templates()
            elif choice == "6":
                self._browse_user_prompts()
            elif choice == "7":
                self._delete_user_prompt()
            elif choice == "8":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def _write_custom_user_prompt(self):
        """Write custom user prompt"""
        print("\nWRITE CUSTOM USER PROMPT")
        print("="*40)
        print("Enter your user prompt (press Enter twice when done):")
        print("\nExample: 'Write a scene where two old friends meet at a coffee shop after years apart.'")
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
        
        user_prompt = '\n'.join(lines).strip()
        
        # Get scene type for categorization
        print(f"\nFor organization:")
        scene_type = input("Scene type/description (e.g., 'coffee shop meeting'): ").strip() or "custom scene"
        
        print(f"\nYour User Prompt:")
        print("="*50)
        print(user_prompt)
        print("="*50)
        
        save = input("\nSave this user prompt? (y/n): ").strip().lower()
        if save == 'y':
            filename = self._save_user_prompt(user_prompt, scene_type)
            print(f"Saved as: {filename}")
        else:
            print("User prompt not saved")
        
        input("Press Enter to continue...")
    
    def _ai_generate_scene_ideas(self):
        """AI-generate random scene ideas"""
        print("\nAI-GENERATE SCENE IDEAS")
        print("="*40)
        print("I'll generate creative scene ideas for you to choose from.")
        
        # Optional theme
        theme = input("Optional theme (e.g., 'workplace', 'family', 'romance'): ").strip()
        
        if not self.model_tester.test_config.get('model'):
            print("No model selected. Please configure a model first.")
            input("Press Enter to continue...")
            return
        
        print("\nGenerating scene ideas...")
        
        ai_system_prompt = """You are a creative writing coach who generates interesting, specific scene ideas for writers. Create scene prompts that are:

- Specific and concrete (not vague)
- Include clear character relationships
- Have built-in conflict or tension
- Are suitable for short scenes (not full stories)
- Give writers a clear starting point

Generate 5 different scene ideas, each as a single sentence starting with "Write a scene where..."."""
        
        theme_part = f" with a {theme} theme" if theme else ""
        ai_user_prompt = f"Generate 5 creative, specific scene ideas{theme_part}. Each should be a complete sentence starting with 'Write a scene where...' and include characters, setting, and conflict/tension. Make them varied and interesting."
        
        result = self.model_tester.stream_ollama_request(
            ai_system_prompt,
            ai_user_prompt,
            self.model_tester.test_config,
            callback=None
        )
        
        if result['success']:
            scene_ideas = result['response'].strip()
            
            print(f"\nAI-Generated Scene Ideas:")
            print("="*50)
            print(scene_ideas)
            print("="*50)
            
            save_choice = input("\nSave one of these ideas? Enter line number or 'n' for none: ").strip()
            
            if save_choice.lower() != 'n':
                try:
                    lines = scene_ideas.split('\n')
                    # Filter for actual scene lines
                    scene_lines = [line.strip() for line in lines if line.strip() and 'write a scene where' in line.lower()]
                    
                    if save_choice.isdigit():
                        choice_idx = int(save_choice) - 1
                        if 0 <= choice_idx < len(scene_lines):
                            selected_scene = scene_lines[choice_idx]
                            scene_type = f"ai generated {theme}" if theme else "ai generated"
                            filename = self._save_user_prompt(selected_scene, scene_type)
                            print(f"Saved selected scene as: {filename}")
                        else:
                            print("Invalid line number")
                            input("Press Enter to continue...")
                    else:
                        print("Invalid input")
                        input("Press Enter to continue...")
                except (ValueError, IndexError):
                    print("Invalid selection")
                    input("Press Enter to continue...")
            else:
                print("No scene ideas saved")
                input("Press Enter to continue...")
        else:
            print(f"Failed to generate scene ideas: {result.get('error', 'Unknown error')}")
            input("Press Enter to continue...")
    
    def _ai_generate_detailed_scene_setup(self):
        """AI-generate detailed scene setup with perspective specification"""
        print("\nAI-GENERATE DETAILED SCENE SETUP")
        print("="*50)
        print("I'll create a detailed, comprehensive scene prompt with specific setup.")
        
        print("\nWhat kind of scene do you want?")
        basic_idea = input("\nBasic scene idea: ").strip()
        if not basic_idea:
            print("No scene idea provided")
            input("Press Enter to continue...")
            return
        
        print("\nOptional details:")
        characters = input("Characters (e.g., 'two sisters', 'boss and employee'): ").strip()
        location = input("Location (e.g., 'busy restaurant', 'quiet park'): ").strip()
        conflict = input("Conflict/tension (e.g., 'money problems', 'betrayal'): ").strip()
        perspective = input("Perspective (e.g., 'from her POV', 'first person', 'using I and you'): ").strip()
        
        if not self.model_tester.test_config.get('model'):
            print("No model selected. Configure a model first.")
            input("Press Enter to continue...")
            return
        
        print("\nCreating detailed scene setup...")
        
        ai_system_prompt = """You are a creative writing coach who creates detailed, specific scene prompts for writers. Your prompts include:

- Clear character setup and relationships
- Specific setting details and atmosphere  
- Concrete conflict or dramatic tension
- Sensory details and mood
- Clear perspective specification (first person using "I", second person using "you", etc.)
- A clear dramatic goal

Create prompts that give writers everything they need including the exact narrative perspective."""
        
        perspective_part = f" from this perspective: {perspective}" if perspective else ""
        
        ai_user_prompt = f"""Create a detailed, comprehensive scene prompt based on this idea:

BASIC IDEA: {basic_idea}

Additional details provided:
- Characters: {characters if characters else 'Not specified'}
- Location: {location if location else 'Not specified'}  
- Conflict/Tension: {conflict if conflict else 'Not specified'}
- Perspective: {perspective if perspective else 'Not specified - but include clear perspective guidance'}

The scene prompt should:
1. Start with "Write a scene where..." or "From her perspective, write a scene where..."
2. Include specific character details and their relationship
3. Describe the setting with atmospheric details
4. Include the conflict or dramatic tension clearly
5. SPECIFY the narrative perspective (first person using "I", second person using "you", etc.)
6. Mention sensory details or mood elements
7. Give the writer a clear dramatic goal
8. Be 2-3 sentences long but packed with specific, vivid details

If romance/intimate scene, make sure to specify using "I" for the protagonist and "you" for the love interest{perspective_part}.

Just return the scene prompt, nothing else."""
        
        result = self.model_tester.stream_ollama_request(
            ai_system_prompt,
            ai_user_prompt,
            self.model_tester.test_config,
            callback=None
        )
        
        if result['success']:
            generated_prompt = result['response'].strip()
            
            print(f"\nAI-Generated Detailed Scene Setup:")
            print("="*60)
            print(generated_prompt)
            print("="*60)
            
            save = input("\nSave this detailed scene prompt? (y/n): ").strip().lower()
            if save == 'y':
                filename = self._save_user_prompt(generated_prompt, basic_idea)
                print(f"Saved as: {filename}")
            else:
                print("Scene prompt not saved")
                input("Press Enter to continue...")
        else:
            print(f"Failed to generate scene prompt: {result.get('error', 'Unknown error')}")
            input("Press Enter to continue...")
    
    def _ai_generate_scene_type_variations(self):
        """Generate multiple variations of a specific scene type"""
        print("\nAI-GENERATE SCENE TYPE VARIATIONS")
        print("="*50)
        print("I'll create multiple variations of the same scene type")
        print("(e.g., 5 different 'first date' scenarios)")
        
        print("\nWhat scene type do you want variations of?")
        scene_type = input("Scene type (e.g., 'first date', 'job interview', 'family dinner'): ").strip()
        if not scene_type:
            print("No scene type provided")
            input("Press Enter to continue...")
            return
        
        print("\nOptional details:")
        genre = input("Genre context (Romance/Thriller/Drama/etc.): ").strip() or "General"
        setting_style = input("Setting style (Modern/Historical/Fantasy/etc.): ").strip() or "Any"
        
        if not self.model_tester.test_config.get('model'):
            print("No model selected. Configure a model first.")
            input("Press Enter to continue...")
            return
        
        print(f"\nGenerating {scene_type} scene variations...")
        
        ai_system_prompt = f"""You are a creative writing coach who generates multiple variations of the same scene type. Create 5 different versions of "{scene_type}" scenes that:

- Have the same basic scene type but different specific situations
- Include different character combinations and relationships
- Use different settings and atmospheres
- Have different conflicts or tensions
- Are each complete, specific scene prompts

Each should be a complete sentence starting with "Write a scene where..." and be specific enough that a writer knows exactly what to write."""
        
        ai_user_prompt = f"""Generate 5 different variations of "{scene_type}" scenes.

Context:
- Genre: {genre}
- Setting style: {setting_style}

Make each variation:
1. Specific and detailed
2. Include clear character relationships
3. Have a different setting or situation
4. Include built-in conflict or tension
5. Be ready to use as-is

Format as a numbered list, each starting with "Write a scene where..."

Just return the 5 scene variations, nothing else."""
        
        result = self.model_tester.stream_ollama_request(
            ai_system_prompt,
            ai_user_prompt,
            self.model_tester.test_config,
            callback=None
        )
        
        if result['success']:
            scene_variations = result['response'].strip()
            
            print(f"\n{scene_type.title()} Scene Variations:")
            print("="*60)
            print(scene_variations)
            print("="*60)
            
            save_choice = input("\nSave one of these variations? Enter number (1-5) or 'n' for none: ").strip()
            
            if save_choice.lower() != 'n':
                try:
                    if save_choice.isdigit() and 1 <= int(save_choice) <= 5:
                        lines = scene_variations.split('\n')
                        # Find the selected variation
                        selected_line = None
                        line_count = 0
                        
                        for line in lines:
                            if line.strip() and ('write a scene where' in line.lower() or line.strip().startswith(save_choice + '.')):
                                line_count += 1
                                if line_count == int(save_choice):
                                    selected_line = line.strip()
                                    # Remove number prefix if present
                                    if selected_line.startswith(save_choice + '.'):
                                        selected_line = selected_line[2:].strip()
                                    break
                        
                        if selected_line:
                            scene_type_clean = f"{scene_type}_variation"
                            filename = self._save_user_prompt(selected_line, scene_type_clean)
                            print(f"Saved selected variation as: {filename}")
                        else:
                            print("Could not find selected variation")
                            input("Press Enter to continue...")
                    else:
                        print("Invalid selection. Enter 1-5.")
                        input("Press Enter to continue...")
                except (ValueError, IndexError):
                    print("Invalid selection")
                    input("Press Enter to continue...")
            else:
                print("No variations saved")
                input("Press Enter to continue...")
        else:
            print(f"Failed to generate variations: {result.get('error', 'Unknown error')}")
            input("Press Enter to continue...")
    
    def _choose_scene_templates(self):
        """Choose from predefined scene templates"""
        print("\nSCENE TEMPLATES")
        print("="*30)
        
        templates = [
            ("Coffee Shop Meeting", "Write a scene where two characters meet unexpectedly at a busy coffee shop."),
            ("Job Interview Gone Wrong", "Write a scene where a job interview takes an unexpected turn."),
            ("Family Dinner Tension", "Write a scene where family tensions surface during dinner."),
            ("Old Friends Reunion", "Write a scene where old friends meet after years apart and discover how much has changed."),
            ("Elevator Stuck", "Write a scene where strangers are stuck in an elevator together."),
            ("Late Night Diner", "Write a scene set in a 24-hour diner where secrets are revealed."),
            ("Hospital Waiting Room", "Write a scene in a hospital waiting room where emotions run high."),
            ("Bookstore Encounter", "Write a scene where someone discovers an important clue in a bookstore."),
            ("Park Bench Conversation", "Write a scene where two people have a life-changing conversation on a park bench."),
            ("Library Research", "Write a scene where someone researching in a library makes an unexpected discovery.")
        ]
        
        for i, (name, prompt) in enumerate(templates, 1):
            print(f"{i:2d}. {name}")
            print(f"    {prompt}")
            print()
        
        try:
            choice = int(input(f"Select template to save (1-{len(templates)}, 0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(templates):
                name, prompt = templates[choice - 1]
                filename = self._save_user_prompt(prompt, name.lower().replace(' ', '_'))
                print(f"Saved template as: {filename}")
            else:
                print("Invalid choice")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
    
    def _browse_user_prompts(self):
        """Browse and view user prompts"""
        user_prompts = self._get_user_prompts()
        
        if not user_prompts:
            print("\nNo user prompts found")
            print("Create some user prompts first!")
            input("Press Enter to continue...")
            return
        
        while True:
            print("\n" + "="*60)
            print("BROWSE USER PROMPTS")
            print("="*60)
            print(f"Found {len(user_prompts)} user prompts:")
            print()
            
            for i, (filename, metadata) in enumerate(user_prompts, 1):
                date_str = self._format_date(metadata['date'], metadata['time'])
                scene_type = metadata.get('genre', 'Unknown')
                print(f"{i:2d}. {filename}")
                print(f"    Scene Type: {scene_type} | Created: {date_str}")
            
            print("\nEnter number to VIEW content, or:")
            print("D + number to DELETE (e.g., 'D2' to delete item 2)")
            print("0 to go back")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "0":
                break
            elif choice.upper().startswith('D'):
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(user_prompts):
                        self._delete_specific_prompt(user_prompts[idx][0], 'user')
                        user_prompts = self._get_user_prompts()  # Refresh list
                    else:
                        print("Invalid item number")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid format. Use 'D' followed by number")
                    input("Press Enter to continue...")
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(user_prompts):
                        self._view_prompt_content(user_prompts[idx][0], 'user')
                    else:
                        print("Invalid item number")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid input")
                    input("Press Enter to continue...")
    
    def _delete_user_prompt(self):
        """Delete user prompt menu"""
        user_prompts = self._get_user_prompts()
        
        if not user_prompts:
            print("\nNo user prompts to delete")
            input("Press Enter to continue...")
            return
        
        print("\n" + "="*50)
        print("DELETE USER PROMPT")
        print("="*50)
        
        for i, (filename, metadata) in enumerate(user_prompts, 1):
            date_str = self._format_date(metadata['date'], metadata['time'])
            scene_type = metadata.get('genre', 'Unknown')
            print(f"{i:2d}. {filename}")
            print(f"    Scene Type: {scene_type} | Created: {date_str}")
        
        try:
            choice = int(input(f"\nSelect prompt to delete (1-{len(user_prompts)}, 0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(user_prompts):
                self._delete_specific_prompt(user_prompts[choice - 1][0], 'user')
            else:
                print("Invalid choice")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
    
    def _save_user_prompt(self, prompt: str, scene_type: str) -> str:
        """Save user prompt to file with clean content (no metadata headers)"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        scene_clean = self._sanitize_filename_part(scene_type)
        
        filename = f"user_prompt_{scene_clean}_{timestamp}.txt"
        filepath = os.path.join(self.templates_folder, filename)
        
        # Save only the prompt content, no metadata headers
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt.strip())
        
        return filename
    
    def _get_user_prompts(self) -> List[Tuple[str, Dict]]:
        """Get list of user prompt files with metadata"""
        pattern = os.path.join(self.templates_folder, "user_prompt_*.txt")
        files = glob.glob(pattern)
        
        prompts = []
        for filepath in sorted(files, key=os.path.getmtime, reverse=True):
            filename = os.path.basename(filepath)
            metadata = self._parse_filename(filename)
            prompts.append((filename, metadata))
        
        return prompts
