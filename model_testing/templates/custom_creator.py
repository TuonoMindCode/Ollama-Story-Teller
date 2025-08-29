import os

class CustomCreator:
    """Creates custom user-written system prompts"""
    
    def __init__(self, templates_folder: str, system_prompt_manager):
        self.templates_folder = templates_folder
        self.system_prompt_manager = system_prompt_manager
    
    def create_custom_system_prompt(self):
        """Write custom system prompt"""
        print("\nWRITE CUSTOM SYSTEM PROMPT")
        print("="*40)
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
        
        system_prompt = '\n'.join(lines).strip()
        
        # Get categorization info
        print(f"\nFor organization:")
        genre = input("Genre (e.g., 'Romance', 'Thriller'): ").strip() or "Custom"
        style = input("Style (e.g., 'Descriptive', 'Minimalist'): ").strip() or "Custom"
        
        print(f"\nYour System Prompt:")
        print("="*50)
        print(system_prompt)
        print("="*50)
        
        save = input("\nSave this system prompt? (y/n): ").strip().lower()
        if save == 'y':
            filename = self.system_prompt_manager._save_system_prompt(system_prompt, genre, style)
            print(f"Saved as: {filename}")
        else:
            print("System prompt not saved")
        
        input("Press Enter to continue...")
