import os

class RomanceCreator:
    """Creates comprehensive romance system prompts"""
    
    def __init__(self, templates_folder: str, system_prompt_manager):
        self.templates_folder = templates_folder
        self.system_prompt_manager = system_prompt_manager
    
    def create_comprehensive_romance_system_prompt(self):
        """Create comprehensive romance system prompt with genre techniques"""
        print("\nCREATE COMPREHENSIVE ROMANCE SYSTEM PROMPT")
        print("="*60)
        print("I'll create a detailed romance writing system prompt using established")
        print("romance genre techniques and conventions.")
        
        print("\nChoose romance subgenre:")
        subgenres = [
            ("Contemporary", "Modern day, realistic settings"),
            ("Historical", "Period settings, historical context"),
            ("Paranormal", "Supernatural elements, fantasy"),
            ("Dark Romance", "Intense, complex emotions and conflicts"),
            ("Romantic Suspense", "Mystery/thriller with romance elements")
        ]
        
        for i, (name, desc) in enumerate(subgenres, 1):
            print(f"{i}. {name} - {desc}")
        
        try:
            choice = int(input(f"\nSelect subgenre (1-{len(subgenres)}): "))
            if 1 <= choice <= len(subgenres):
                subgenre, description = subgenres[choice - 1]
            else:
                print("Invalid choice, using Contemporary")
                subgenre, description = subgenres[0]
        except ValueError:
            print("Invalid input, using Contemporary")
            subgenre, description = subgenres[0]
        
        print(f"\nChoose narrative techniques to emphasize:")
        print("1. Heavy internal monologue (thoughts and feelings)")
        print("2. Rich sensory descriptions (atmosphere and physical sensations)")
        print("3. Dialogue-driven chemistry (conversation and subtext)")
        print("4. Slow burn tension building")
        print("5. All of the above (comprehensive)")
        
        try:
            tech_choice = int(input("Select technique focus (1-5): "))
        except ValueError:
            tech_choice = 5
        
        # Create comprehensive romance system prompt
        technique_focus = {
            1: "Focus heavily on internal monologue, revealing every nuance of the protagonist's thoughts and emotional responses.",
            2: "Emphasize rich sensory descriptions - textures, scents, atmospheric details, and meaningful physical moments.",
            3: "Drive the narrative through dialogue rich with subtext, playful exchanges, and unspoken desires.",
            4: "Build romantic tension gradually through small moments, meaningful glances, and slowly developing intimacy.",
            5: "Blend all romance techniques - internal thoughts, sensory details, meaningful dialogue, and carefully building tension."
        }
        
        # Romance genre conventions
        romance_conventions = """Apply established romance genre conventions:
- Witty dialogue and natural character chemistry
- Emotional depth and authentic character development
- Strong narrative voice and compelling internal conflict
- Balanced pacing between action and introspection
- Vivid sensory details that create atmosphere
- Realistic relationship dynamics and character growth"""
        
        system_prompt = f"""You are an accomplished {subgenre.lower()} romance writer who crafts deeply engaging, emotionally resonant scenes. Write from a first-person female perspective using "I" for the protagonist and "you" when addressing or thinking about the love interest, creating intimate reader connection.

{technique_focus[tech_choice]}

{romance_conventions}

Create scenes with:
• Layered internal monologue that reveals character depth
• Sensory details that immerse readers in the moment
• Natural dialogue that builds chemistry and tension
• Pacing that maintains reader engagement
• Authentic character voices and believable interactions
• Descriptive language that creates vivid mental imagery

Write with the emotional depth and narrative techniques that define quality romance literature, focusing on character development, authentic relationships, and engaging storytelling."""
        
        print(f"\nComprehensive {subgenre} Romance System Prompt:")
        print("="*60)
        print(system_prompt)
        print("="*60)
        
        save = input(f"\nSave this comprehensive romance system prompt? (y/n): ").strip().lower()
        if save == 'y':
            filename = self.system_prompt_manager._save_system_prompt(system_prompt, f"Romance_{subgenre}", "Comprehensive")
            print(f"Saved as: {filename}")
            print(f"This system prompt integrates narrative techniques and genre conventions!")
        else:
            print("System prompt not saved")
        
        input("Press Enter to continue...")
