from .base_system_prompt import BaseSystemPromptManager

class DetectiveCreator(BaseSystemPromptManager):
    """Creates comprehensive detective system prompts"""
    
    def create_comprehensive_detective_system_prompt(self):
        """Create comprehensive detective system prompt with genre techniques"""
        print("\nCREATE COMPREHENSIVE DETECTIVE SYSTEM PROMPT")
        print("="*60)
        print("I'll create a detailed detective writing system prompt using established")
        print("detective/mystery genre techniques and conventions.")
        
        print("\nChoose detective subgenre:")
        subgenres = [
            ("Classic Whodunit", "Traditional puzzle mystery with logical clues and reveals"),
            ("Hard-boiled Detective", "Gritty urban crime with cynical protagonist"),
            ("Cozy Mystery", "Gentle mysteries in small communities, amateur detectives"),
            ("Police Procedural", "Realistic law enforcement investigation methods"),
            ("Psychological Thriller", "Mind games, unreliable narrators, psychological clues"),
            ("Amateur Sleuth", "Non-professional detective solving crimes through curiosity"),
            ("Private Investigator", "Professional private detective handling complex cases"),
            ("Historical Mystery", "Detective stories set in past time periods")
        ]
        
        for i, (name, desc) in enumerate(subgenres, 1):
            print(f"{i}. {name} - {desc}")
        
        try:
            choice = int(input(f"\nSelect detective subgenre (1-{len(subgenres)}): "))
            if 1 <= choice <= len(subgenres):
                subgenre, description = subgenres[choice - 1]
            else:
                print("Invalid choice, using Classic Whodunit")
                subgenre, description = subgenres[0]
        except ValueError:
            print("Invalid input, using Classic Whodunit")
            subgenre, description = subgenres[0]
        
        print(f"\nChoose detective techniques to emphasize:")
        print("1. Systematic Investigation (methodical clue discovery, logical deduction)")
        print("2. Psychological Analysis (character motivation, behavioral insights)")
        print("3. Atmospheric Tension (mood building, environmental storytelling)")
        print("4. Interrogation Mastery (dialogue-driven investigation, witness psychology)")
        print("5. All of the above (comprehensive detective approach)")
        
        try:
            tech_choice = int(input("Select technique focus (1-5): "))
        except ValueError:
            tech_choice = 5
        
        print(f"\nChoose narrative perspective:")
        perspectives = [
            ("Detective's POV", "Close following of detective's thought process and discoveries"),
            ("Multiple POV", "Detective, suspects, and witnesses perspectives for full picture"),
            ("Victim-Centered", "Investigation that honors the victim's story and perspective"),
            ("Omniscient Observer", "All-seeing narrator who controls information flow to readers")
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
        
        # Create comprehensive detective system prompt
        technique_focus = {
            1: "Focus on methodical investigation through systematic clue discovery, logical deduction chains, and evidence analysis that builds the case step by step.",
            2: "Emphasize deep psychological analysis of suspects, victims, and witnesses, exploring what drives people to crime and how trauma shapes behavior.",
            3: "Build atmospheric tension through environmental storytelling, mood creation, and sense of place that makes settings feel ominous and meaningful.",
            4: "Master interrogation scenes through realistic dialogue, psychological pressure, and the art of reading people to extract truth from deception.",
            5: "Blend all detective techniques - systematic investigation, psychological insight, atmospheric tension, and interrogation mastery into a comprehensive approach."
        }
        
        # Detective genre conventions
        detective_conventions = """Apply established detective genre conventions:
- Fair play mystery construction where readers can solve alongside the detective
- Strategic placement of clues and red herrings that mislead without cheating
- Logical progression from crime scene to investigation to deduction to revelation
- Complex but believable character motivations for both perpetrators and victims
- Realistic procedural accuracy in forensic details and investigation methods
- Balanced pacing between discovery, analysis, and dramatic confrontation"""
        
        system_prompt = f"""You are an accomplished {subgenre.lower()} writer who crafts intricate detective stories with compelling mysteries and satisfying revelations. Write from {selected_perspective.lower()} perspective, creating methodical investigative narratives that challenge and reward readers.

{technique_focus[tech_choice]}

{detective_conventions}

Create detective scenes with:
• Methodical investigation that reveals information at the perfect pace
• Sharp observational details that serve as both clues and atmosphere
• Realistic dialogue during interrogations that reveals character psychology
• Logical deduction sequences that readers can follow and appreciate
• Environmental storytelling where settings provide crucial information
• Procedural accuracy that maintains believability and respect for the craft
• Fair play mystery elements where astute readers can solve the puzzle

Write with the investigative rigor and genre mastery that define quality detective literature, focusing on logical mystery construction, psychological depth, and procedural authenticity while maintaining narrative tension and reader engagement."""
        
        print(f"\nComprehensive {subgenre} Detective System Prompt:")
        print("="*60)
        print(system_prompt)
        print("="*60)
        
        save = input(f"\nSave this comprehensive detective system prompt? (y/n): ").strip().lower()
        if save == 'y':
            filename = self._save_system_prompt(system_prompt, f"Detective_{subgenre.replace(' ', '_')}", "Comprehensive")
            print(f"Saved as: {filename}")
            print(f"This system prompt integrates detective genre techniques and craft mastery!")
        else:
            print("System prompt not saved")
        
        input("Press Enter to continue...")
