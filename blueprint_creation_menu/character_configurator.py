class CharacterConfigurator:
    def __init__(self):
        self.gender_options = {
            'auto': 'Let the story determine gender',
            'male': 'Male protagonist',
            'female': 'Female protagonist',
            'non_binary': 'Non-binary protagonist',
            'unspecified': 'Gender-neutral writing'
        }
    
    def configure_protagonist_gender(self, current_gender='auto'):
        """Configure the protagonist's gender for blueprint creation"""
        print("\n👤 PROTAGONIST GENDER")
        print("="*40)
        print("Set the gender for the main character in this blueprint:")
        print()
        
        for key, description in self.gender_options.items():
            marker = "✓" if key == current_gender else " "
            print(f"[{marker}] {key}: {description}")
        
        while True:
            choice = input(f"\nSelect gender ({current_gender}): ").strip().lower()
            
            if not choice:
                return current_gender
            elif choice in self.gender_options:
                return choice
            else:
                print("❌ Invalid option. Please choose from the list above.")
    
    def get_gender_blueprint_instructions(self, gender):
        """Get instructions to add to blueprint based on gender choice"""
        if gender == 'male':
            return "The protagonist is male. Use he/him pronouns."
        elif gender == 'female':
            return "The protagonist is female. Use she/her pronouns."
        elif gender == 'non_binary':
            return "The protagonist is non-binary. Use they/them pronouns."
        elif gender == 'unspecified':
            return "Write in a gender-neutral style. Avoid gendered pronouns when possible."
        else:  # auto
            return ""
