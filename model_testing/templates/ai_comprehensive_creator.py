import os
from .age_specific_options import AgeSpecificOptions

class AIComprehensiveCreator:
    """Creates AI-generated comprehensive system prompts"""
    
    def __init__(self, templates_folder: str, system_prompt_manager):
        self.templates_folder = templates_folder
        self.system_prompt_manager = system_prompt_manager
    
    def create_ai_comprehensive_system_prompt(self):
        """AI-generate comprehensive creative story system prompt"""
        print("\nOLLAMA LLM BUILD COMPREHENSIVE SYSTEM PROMPT")
        print("="*60)
        print("I'll help you create a comprehensive system prompt that defines")
        print("HOW the AI should write stories (style, techniques, perspective).")
        print()
        print("First, let's specify the target audience for age-appropriate writing:")
        
        # Select age group/audience first
        print("\nAge Groups/Audiences:")
        age_groups = [
            ("Children", "Ages 5-8, simple stories, basic vocabulary"),
            ("Middle Grade", "Ages 8-12, growing independence, age-appropriate challenges"),
            ("Young Adult", "Ages 13-17, coming-of-age themes, identity exploration"),
            ("Adult", "Ages 18+, mature themes, complex relationships and situations"),
            ("New Adult", "Ages 18-25, college/early career, transitional life stages"),
            ("General Audience", "Accessible to most readers regardless of age"),
            ("Other", "Specify your own target audience")
        ]
        
        for i, (name, description) in enumerate(age_groups, 1):
            print(f"{i:2d}. {name} - {description}")
        
        try:
            age_choice = int(input(f"\nSelect age group/audience (1-{len(age_groups)}): "))
            if not (1 <= age_choice <= len(age_groups)):
                print("Invalid age group choice")
                input("Press Enter to continue...")
                return
            selected_age_group = age_groups[age_choice - 1][0]
            
            if selected_age_group == "Other":
                custom_audience = input("Describe your target audience: ").strip()
                selected_age_group = custom_audience if custom_audience else "General Audience"
                
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        print(f"\nWriting for: {selected_age_group}")
        
        # Get age-specific options
        age_specific_options = AgeSpecificOptions.get_options(selected_age_group)
        
        # Show age-appropriate writing techniques
        print(f"\n{selected_age_group} Writing Techniques:")
        for i, (technique, description) in enumerate(age_specific_options['techniques'], 1):
            print(f"{i:2d}. {technique} - {description}")
        
        try:
            tech_choice = int(input(f"\nSelect writing technique (1-{len(age_specific_options['techniques'])}): "))
            if not (1 <= tech_choice <= len(age_specific_options['techniques'])):
                print("Invalid technique choice")
                input("Press Enter to continue...")
                return
            selected_technique = age_specific_options['techniques'][tech_choice - 1][0]
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        # Show age-appropriate narrative perspectives
        print(f"\n{selected_age_group} Narrative Perspectives:")
        for i, (perspective, description) in enumerate(age_specific_options['perspectives'], 1):
            print(f"{i:2d}. {perspective} - {description}")
        
        try:
            persp_choice = int(input(f"\nSelect narrative perspective (1-{len(age_specific_options['perspectives'])}): "))
            if not (1 <= persp_choice <= len(age_specific_options['perspectives'])):
                print("Invalid perspective choice")
                input("Press Enter to continue...")
                return
            selected_perspective = age_specific_options['perspectives'][persp_choice - 1][0]
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        # Show age-appropriate writing styles
        print(f"\n{selected_age_group} Writing Styles:")
        for i, (style, description) in enumerate(age_specific_options['styles'], 1):
            print(f"{i:2d}. {style} - {description}")
        
        try:
            style_choice = int(input(f"\nSelect writing style (1-{len(age_specific_options['styles'])}): "))
            if not (1 <= style_choice <= len(age_specific_options['styles'])):
                print("Invalid style choice")
                input("Press Enter to continue...")
                return
            selected_style = age_specific_options['styles'][style_choice - 1][0]
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        print(f"\nOptional - help categorize:")
        genre = input("Primary genre (Adventure/Fantasy/Contemporary/etc.): ").strip() or "Creative"
        
        if not self.system_prompt_manager.model_tester.test_config.get('model'):
            print("No model selected. Please configure a model first.")
            input("Press Enter to continue...")
            return
        
        print("\nGenerating comprehensive system prompt...")
        print(f"• Target Audience: {selected_age_group}")
        print(f"• Technique: {selected_technique}")
        print(f"• Perspective: {selected_perspective}")
        print(f"• Style: {selected_style}")
        print(f"• Genre: {genre}")
        
        # Generate the system prompt using AI
        self._generate_with_ai(selected_age_group, selected_technique, selected_perspective, selected_style, genre, age_specific_options)
    
    def _generate_with_ai(self, age_group, technique, perspective, style, genre, age_options):
        """Generate system prompt using AI"""
        
        # Get detailed descriptions for the AI prompt
        technique_detail = next((desc for tech, desc in age_options['techniques'] if tech == technique), "")
        perspective_detail = next((desc for persp, desc in age_options['perspectives'] if persp == perspective), "")
        style_detail = next((desc for st, desc in age_options['styles'] if st == style), "")
        
        ai_system_prompt = """You are an expert creative writing instructor who creates comprehensive system prompts for AI story writers targeting specific age groups. 

Your system prompts should cover:
- Age-appropriate writing philosophy and approach
- Narrative techniques suitable for the target audience
- Character development methods for that age group
- Dialogue and voice principles appropriate for readers
- Pacing and structure guidelines for the age group
- Language complexity and tone direction
- Age-specific genre conventions

Create system prompts that give clear direction on HOW to write for the specific age group without specifying WHAT to write about."""
        
        ai_user_prompt = f"""Create a comprehensive system prompt for {age_group} creative writing with these specifications:

TECHNIQUE: {technique}
- {technique_detail}

PERSPECTIVE: {perspective}  
- {perspective_detail}

STYLE: {style}
- {style_detail}

GENRE CONTEXT: {genre}
AGE GROUP: {age_group}

The system prompt should:
- Be 4-6 sentences long and comprehensive
- Start with "You are an accomplished {age_group.lower()} writer who..."
- Integrate all three elements (technique, perspective, style) naturally
- Focus on HOW to write for {age_group} readers
- Include specific guidance appropriate for this age group
- Be applicable across many different {age_group} stories
- Emphasize the selected technique, perspective, and style

Just return the system prompt, nothing else."""
        
        result = self.system_prompt_manager.model_tester.stream_ollama_request(
            ai_system_prompt,
            ai_user_prompt,
            self.system_prompt_manager.model_tester.test_config,
            callback=None
        )
        
        if result['success']:
            generated_prompt = result['response'].strip()
            
            print(f"\nComprehensive {age_group} System Prompt:")
            print("="*70)
            print(generated_prompt)
            print("="*70)
            print(f"Target Audience: {age_group}")
            print(f"Technique: {technique}")
            print(f"Perspective: {perspective}")
            print(f"Style: {style}")
            print(f"Genre: {genre}")
            
            save = input(f"\nSave this comprehensive system prompt? (y/n): ").strip().lower()
            if save == 'y':
                filename = self.system_prompt_manager._save_system_prompt(generated_prompt, f"{genre}_{age_group}", f"{technique}_{perspective}_{style}")
                print(f"Saved as: {filename}")
                print(f"Location: {self.system_prompt_manager.templates_folder}")
            else:
                print("System prompt not saved")
        else:
            print(f"Failed to generate: {result.get('error', 'Unknown error')}")
        
        input("Press Enter to continue...")
