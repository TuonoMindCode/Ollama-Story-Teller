import os
from typing import Dict

class GenreStyleCreator:
    """Creates simple genre and style based system prompts"""
    
    def __init__(self, templates_folder: str, system_prompt_manager):
        self.templates_folder = templates_folder
        self.system_prompt_manager = system_prompt_manager
        self.genres = system_prompt_manager.genres
        self.writing_styles = system_prompt_manager.writing_styles
    
    def create_genre_style_system_prompt(self):
        """Create system prompt by choosing genre and style"""
        print("\nCHOOSE GENRE & STYLE")
        print("="*50)
        print("To build this system prompt, we need to know:")
        print("• Who this story is for (age group/audience)")
        print("• What genre you want to write in")
        print("• What writing style to use")
        print()
        print("This creates a simple, general system prompt that gets saved to a file")
        print("so you can edit it later if needed.")
        print(f"Storage location: {os.path.basename(self.templates_folder)}/")
        print()
        
        # Select age group/audience first
        print("Age Groups/Audiences:")
        age_groups = [
            ("Middle Grade", "Ages 8-12, simple language, age-appropriate themes"),
            ("Young Adult", "Ages 13-17, coming-of-age themes, complex emotions"),
            ("New Adult", "Ages 18-25, college/early career, relationships, identity"),
            ("Adult", "Ages 25+, mature themes, complex relationships"),
            ("Literary Adult", "Sophisticated readers, complex prose, deeper themes"),
            ("General Audience", "Accessible to most adult readers"),
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
                selected_age_group = custom_audience if custom_audience else "General"
                
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        # Select genre
        print(f"\nGenres for {selected_age_group}:")
        for i, genre in enumerate(self.genres, 1):
            print(f"{i:2d}. {genre}")
        
        try:
            genre_choice = int(input(f"\nSelect genre (1-{len(self.genres)}): "))
            if not (1 <= genre_choice <= len(self.genres)):
                print("Invalid genre choice")
                input("Press Enter to continue...")
                return
            selected_genre = self.genres[genre_choice - 1]
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        # Select writing style
        print(f"\nWriting Styles for {selected_genre} ({selected_age_group}):")
        for i, style in enumerate(self.writing_styles, 1):
            print(f"{i:2d}. {style}")
        
        try:
            style_choice = int(input(f"\nSelect writing style (1-{len(self.writing_styles)}): "))
            if not (1 <= style_choice <= len(self.writing_styles)):
                print("Invalid style choice")
                input("Press Enter to continue...")
                return
            selected_style = self.writing_styles[style_choice - 1]
        except ValueError:
            print("Invalid input")
            input("Press Enter to continue...")
            return
        
        # Create basic system prompt
        system_prompt = self._generate_basic_system_prompt(selected_genre, selected_style, selected_age_group)
        
        # Show preview and save
        print(f"\nGenerated System Prompt:")
        print("="*60)
        print(system_prompt)
        print("="*60)
        print(f"Target Audience: {selected_age_group}")
        print(f"Genre: {selected_genre}")
        print(f"Style: {selected_style}")
        
        save = input("\nSave this system prompt? (y/n): ").strip().lower()
        if save == 'y':
            filename = self.system_prompt_manager._save_system_prompt(system_prompt, f"{selected_genre}_{selected_age_group}", selected_style)
            print(f"Saved as: {filename}")
        else:
            print("System prompt not saved")
        
        input("Press Enter to continue...")
    
    def _generate_basic_system_prompt(self, genre: str, style: str, age_group: str) -> str:
        """Generate a basic system prompt based on genre, style, and age group"""
        base = "You are a skilled writer who specializes in"
        
        # Age-appropriate genre descriptions (condensed version)
        age_considerations = {
            'Middle Grade': {
                'Romance': 'age-appropriate friendship stories with gentle emotional connections',
                'Thriller': 'exciting adventure stories with age-appropriate suspense',
                'General': 'engaging stories appropriate for middle-grade readers',
            },
            'Young Adult': {
                'Romance': 'coming-of-age romance with emotional growth and first love',
                'Thriller': 'intense YA thrillers with teen protagonists facing real dangers',
                'General': 'compelling stories about teenage experiences and challenges',
            },
            'Adult': {
                'Romance': 'mature romance with complex relationships and emotional depth',
                'Thriller': 'suspenseful thrillers with sophisticated plots and adult themes',
                'General': 'sophisticated storytelling for adult readers',
            }
        }
        
        # Get description or use genre name
        genre_descriptions = age_considerations.get(age_group, {})
        genre_part = genre_descriptions.get(genre, f"{genre.lower()} fiction")
        
        # Style additions
        style_additions = {
            'Minimalist': 'Use clean, direct language and let subtext carry meaning.',
            'Descriptive': 'Create vivid imagery with rich sensory details.',
            'Literary': 'Employ sophisticated prose with layered meaning.',
            'Other': 'Develop a distinctive and engaging writing voice.'
        }
        
        style_part = style_additions.get(style, 'Write with engaging style and clear voice.')
        
        return f"{base} {genre_part}. {style_part}"
