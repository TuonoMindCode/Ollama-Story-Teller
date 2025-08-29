from .base_system_prompt import BaseSystemPromptManager

class GenreStyleCreator(BaseSystemPromptManager):
    """Creates simple genre and style based system prompts"""
    
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
        
        # Age group selection and rest of the method...
        # (Move the entire _create_genre_style_system_prompt method here)
