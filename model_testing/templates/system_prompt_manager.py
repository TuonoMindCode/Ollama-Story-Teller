import os
import glob
import datetime
from typing import Dict, List, Optional, Tuple
from .base_template_manager import BaseTemplateManager
from .genre_style_creator import GenreStyleCreator
from .custom_creator import CustomCreator
from .romance_creator import RomanceCreator
from .ai_comprehensive_creator import AIComprehensiveCreator

class SystemPromptManager(BaseTemplateManager):
    def __init__(self, templates_folder: str, model_tester):
        super().__init__(templates_folder)
        self.model_tester = model_tester
        
        # Genre and style options
        self.genres = ['Romance', 'Thriller', 'Literary', 'Sci-Fi', 'Fantasy', 'Mystery', 'Horror', 'General', 'Other']
        self.writing_styles = ['Minimalist', 'Descriptive', 'Literary', 'Dialogue-Heavy', 'Action-Packed', 'Atmospheric', 'Other']
        
        # Initialize creator
        self.genre_style_creator = GenreStyleCreator(templates_folder, self)
        self.custom_creator = CustomCreator(templates_folder, self)
        self.romance_creator = RomanceCreator(templates_folder, self)
        self.ai_comprehensive_creator = AIComprehensiveCreator(templates_folder, self)
    
    def run_system_prompt_manager(self):
        """System prompt manager menu"""
        while True:
            system_prompts = self._get_system_prompts()
            
            print("\n" + "="*50)
            print("SYSTEM PROMPT MANAGER")
            print("="*50)
            print(f"Found {len(system_prompts)} system prompts")
            print()
            print("1. Choose Genre & Style (choose built-in genre and style, ~20 word system prompt)")
            print("2. Ollama LLM build a comprehensive creative story system prompt")
            print("3. Create Comprehensive Romance System Prompt (detailed romance techniques)")
            print("4. Create Comprehensive Detective System Prompt (detailed detective techniques)")
            print("5. Write Custom System Prompt (write your own from scratch)")
            print("6. Browse/View System Prompts")
            print("7. Delete System Prompt")
            print("8. Back to Template Manager")
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == "1":
                self._create_genre_style_system_prompt()
            elif choice == "2":
                self._ai_generate_comprehensive_system_prompt()
            elif choice == "3":
                self._create_comprehensive_romance_system_prompt()
            elif choice == "4":
                self._create_comprehensive_detective_system_prompt()
            elif choice == "5":
                self._write_custom_system_prompt()
            elif choice == "6":
                self._browse_system_prompts()
            elif choice == "7":
                self._delete_system_prompt()
            elif choice == "8":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def _create_genre_style_system_prompt(self):
        """Create simple genre/style system prompt"""
        self.genre_style_creator.create_genre_style_system_prompt()
    
    def _ai_generate_comprehensive_system_prompt(self):
        """AI comprehensive system prompt"""
        self.ai_comprehensive_creator.create_ai_comprehensive_system_prompt()
    
    def _create_comprehensive_romance_system_prompt(self):
        """Romance system prompt"""
        self.romance_creator.create_comprehensive_romance_system_prompt()
    
    def _create_comprehensive_detective_system_prompt(self):
        """Create comprehensive detective system prompt with scene-specific techniques"""
        print("\nCREATE COMPREHENSIVE DETECTIVE SCENE SYSTEM PROMPT")
        print("="*60)
        print("I'll create a detailed detective scene writing system prompt using established")
        print("detective/mystery scene techniques and conventions.")
        print()
        print("This focuses on writing individual SCENES (interrogation, evidence review,")
        print("crime scene investigation, chase) with proper pacing and atmosphere.")
        
        print("\nChoose detective scene type:")
        scene_types = [
            ("Crime Scene Investigation", "Examining clues, processing evidence, initial discovery"),
            ("Interrogation Scene", "Questioning suspects, psychological pressure, revealing truth"),
            ("Evidence Review", "Police station discussion, connecting dots, theory building"),
            ("Chase/Pursuit", "Action sequences with tension and pacing"),
            ("Revelation Scene", "Confronting the culprit, explaining the solution"),
            ("Witness Interview", "Gathering information, reading between the lines"),
            ("Stakeout/Surveillance", "Tension building, observation, waiting for action"),
            ("General Detective Scene", "Any detective scene with mystery elements")
        ]
        
        for i, (name, desc) in enumerate(scene_types, 1):
            print(f"{i}. {name} - {desc}")
        
        try:
            choice = int(input(f"\nSelect scene type (1-{len(scene_types)}): "))
            if 1 <= choice <= len(scene_types):
                scene_type, description = scene_types[choice - 1]
            else:
                print("Invalid choice, using General Detective Scene")
                scene_type, description = scene_types[-1]
        except ValueError:
            print("Invalid input, using General Detective Scene")
            scene_type, description = scene_types[-1]
        
        print(f"\nChoose scene writing techniques:")
        print("1. Tension Building (stretch the scene, build suspense, use pacing)")
        print("2. Dialogue Mastery (realistic conversation, subtext, character voice)")
        print("3. Environmental Storytelling (setting details reveal clues and mood)")
        print("4. Internal Detective Process (show thinking, deduction, observation)")
        print("5. All techniques (comprehensive scene writing)")
        
        try:
            tech_choice = int(input("Select technique focus (1-5): "))
        except ValueError:
            tech_choice = 5
        
        print(f"\nChoose narrative perspective:")
        perspectives = [
            ("Detective's Close POV", "Intimate access to detective's thoughts and observations"),
            ("Third Person Observer", "Outside view that shows all characters and actions"),
            ("First Person Detective", "Direct 'I investigated' perspective for intimacy"),
            ("Multiple Character POV", "Switch between detective, suspect, witness viewpoints")
        ]
        
        for i, (name, desc) in enumerate(perspectives, 1):
            print(f"{i}. {name} - {desc}")
        
        try:
            persp_choice = int(input(f"Select perspective (1-{len(perspectives)}): "))
            if 1 <= persp_choice <= len(perspectives):
                selected_perspective = perspectives[persp_choice - 1][0]
            else:
                selected_perspective = perspectives[0][0]
        except ValueError:
            selected_perspective = perspectives[0][0]
        
        # Create scene-specific detective system prompt
        technique_focus = {
            1: "Focus on building tension throughout the scene. Use pacing to stretch moments of discovery, create pauses for impact, and build suspense through what's not said. Make readers feel the weight of each clue and revelation.",
            2: "Master realistic dialogue with subtext. Show character personalities through speech patterns, use interrogation techniques, and reveal information through what people don't say as much as what they do.",
            3: "Use environmental details to tell the story. Let the setting reveal clues, create atmosphere, and reflect the emotional tone. Every detail should serve the investigation and mood.",
            4: "Show the detective's thinking process. Include observations, logical deductions, and moments of insight. Let readers follow the detective's mind as they piece together evidence.",
            5: "Blend all scene techniques - tension building, realistic dialogue, environmental storytelling, and detective reasoning into a comprehensive scene-writing approach."
        }
        
        # Scene-specific detective conventions
        scene_conventions = """Apply established detective scene writing conventions:
- Build scenes with clear beginning, rising tension, and satisfying payoff
- Use scene pacing to control information reveal and maintain reader engagement  
- Include realistic procedural details that add authenticity without slowing pace
- Show character dynamics through action and dialogue during investigations
- Create atmospheric details that enhance mood without overwhelming the mystery
- End scenes with hooks, revelations, or new questions that propel the story forward"""
        
        system_prompt = f"""You are an accomplished detective scene writer who crafts compelling {scene_type.lower()} scenes with proper pacing and atmospheric tension. Write from {selected_perspective.lower()} perspective, creating engaging investigative scenes that draw readers in and maintain suspense.

{technique_focus[tech_choice]}

{scene_conventions}

Create detective scenes with:
• Proper scene pacing that builds tension and maintains reader engagement
• Realistic dialogue during investigations that reveals character and information
• Environmental details that serve both atmosphere and investigation
• Clear scene structure with setup, development, and satisfying conclusion
• Authentic procedural elements that add believability without slowing pace
• Character dynamics that show relationships and conflicts during investigation
• Strategic information reveal that keeps readers guessing and engaged

Write detective scenes using the established techniques that make mystery scenes compelling - focus on scene craft, character interaction, and the gradual revelation of information that keeps readers turning pages."""
            
        print(f"\nComprehensive Detective Scene System Prompt:")
        print("="*60)
        print(system_prompt)
        print("="*60)
        print(f"Scene Type: {scene_type}")
        print(f"Focus: Scene-specific detective writing techniques")
        print(f"Purpose: Writing individual detective scenes with proper pacing")
        
        save = input(f"\nSave this detective scene system prompt? (y/n): ").strip().lower()
        if save == 'y':
            filename = self._save_system_prompt(system_prompt, f"Detective_Scene_{scene_type.replace(' ', '_')}", "Scene_Writing")
            print(f"Saved as: {filename}")
            print(f"This system prompt focuses on scene craft and pacing!")
        else:
            print("System prompt not saved")
        
        input("Press Enter to continue...")
    
    def _write_custom_system_prompt(self):
        """Custom system prompt"""
        self.custom_creator.create_custom_system_prompt()
    
    def _save_system_prompt(self, prompt: str, genre: str, style: str) -> str:
        """Save system prompt to file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        genre_clean = self._sanitize_filename_part(genre)
        style_clean = self._sanitize_filename_part(style)
        
        filename = f"system_prompt_{genre_clean}_{style_clean}_{timestamp}.txt"
        filepath = os.path.join(self.templates_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt.strip())
        
        return filename
    
    def _sanitize_filename_part(self, text: str) -> str:
        """Sanitize text for use in filename"""
        if not text:
            return "unknown"
        
        invalid_chars = '<>:"/\\|?*'
        sanitized = text
        
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '')
        
        sanitized = sanitized.replace('"', '').replace("'", '')
        sanitized = sanitized.replace('(', '').replace(')', '')
        sanitized = sanitized.replace('[', '').replace(']', '')
        sanitized = sanitized.replace('{', '').replace('}', '')
        
        sanitized = sanitized.replace(' ', '_').replace('-', '_')
        sanitized = sanitized.replace('.', '_').replace(',', '_')
        
        while '__' in sanitized:
            sanitized = sanitized.replace('__', '_')
        
        sanitized = sanitized.strip('_')
        sanitized = sanitized[:20] if sanitized else "unknown"
        
        return sanitized.lower()
    
    def _browse_system_prompts(self):
        """Browse and view system prompts"""
        system_prompts = self._get_system_prompts()
        
        if not system_prompts:
            print("\nNo system prompts found")
            input("Press Enter to continue...")
            return
        
        while True:
            print("\n" + "="*60)
            print("BROWSE SYSTEM PROMPTS")
            print("="*60)
            print(f"Found {len(system_prompts)} system prompts:")
            print()
            
            for i, (filename, metadata) in enumerate(system_prompts, 1):
                date_str = self._format_date(metadata['date'], metadata['time'])
                print(f"{i:2d}. {filename}")
                print(f"    Genre: {metadata['genre']} | Style: {metadata['style']} | Created: {date_str}")
            
            print("\nEnter number to VIEW content, or:")
            print("D + number to DELETE (e.g., 'D2' to delete item 2)")
            print("0 to go back")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "0":
                break
            elif choice.upper().startswith('D'):
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(system_prompts):
                        self._delete_specific_prompt(system_prompts[idx][0], 'system')
                        system_prompts = self._get_system_prompts()
                    else:
                        print("Invalid item number")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid format. Use 'D' followed by number (e.g., 'D2')")
                    input("Press Enter to continue...")
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(system_prompts):
                        self._view_prompt_content(system_prompts[idx][0], 'system')
                    else:
                        print("Invalid item number")
                        input("Press Enter to continue...")
                except ValueError:
                    print("Invalid input")
                    input("Press Enter to continue...")
    
    def _delete_system_prompt(self):
        """Delete system prompt menu"""
        system_prompts = self._get_system_prompts()
        
        if not system_prompts:
            print("\nNo system prompts to delete")
            input("Press Enter to continue...")
            return
        
        print("\n" + "="*50)
        print("DELETE SYSTEM PROMPT")
        print("="*50)
        
        for i, (filename, metadata) in enumerate(system_prompts, 1):
            date_str = self._format_date(metadata['date'], metadata['time'])
            print(f"{i:2d}. {filename}")
            print(f"    Genre: {metadata['genre']} | Style: {metadata['style']} | Created: {date_str}")
        
        try:
            choice = int(input(f"\nSelect prompt to delete (1-{len(system_prompts)}, 0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(system_prompts):
                self._delete_specific_prompt(system_prompts[choice - 1][0], 'system')
            else:
                print("Invalid choice")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
    
    def _get_system_prompts(self) -> List[Tuple[str, Dict]]:
        """Get list of system prompt files with metadata"""
        pattern = os.path.join(self.templates_folder, "system_prompt_*.txt")
        files = glob.glob(pattern)
        
        prompts = []
        for filepath in sorted(files, key=os.path.getmtime, reverse=True):
            filename = os.path.basename(filepath)
            metadata = self._parse_filename(filename)
            prompts.append((filename, metadata))
        
        return prompts