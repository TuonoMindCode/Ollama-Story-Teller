"""Character settings handlers"""
from ..config import *

class CharacterSettingsHandler:
    def __init__(self, blueprint_creator):
        self.bc = blueprint_creator

    def set_protagonist_gender(self, blueprint_data):
        """Set protagonist gender"""
        print("\n" + "-"*40)
        print("PROTAGONIST GENDER")
        print("-"*40)
        print("Choose the gender of the main character (protagonist).\n")

        print("Gender options:")
        for i, gender in enumerate(GENDERS, 1):
            print(f"{i}. {gender}")
        print(f"{len(GENDERS)+1}. Keep current ({blueprint_data.get('protagonist_gender', 'Not chosen')})")

        try:
            choice = int(input(f"Select gender (1-{len(GENDERS)+1}): "))
            if 1 <= choice <= len(GENDERS):
                blueprint_data['protagonist_gender'] = GENDERS[choice-1]
                print(f"✓ Protagonist gender set to: {GENDERS[choice-1]}")
            else:
                print("✓ Gender unchanged")
        except ValueError:
            print("❌ Invalid input")

        input("Press Enter to continue...")

    def set_counterpart_character(self, blueprint_data):
        """Set the counterpart/opposing character"""
        print("\n" + "-"*40)
        print("COUNTERPART CHARACTER")
        print("-"*40)
        print("Choose the main counterpart to your protagonist.")
        print("This could be the antagonist, love interest, or other key opposing character.\n")

        # Get genre-specific counterparts
        genre = blueprint_data.get('genre', 'Not chosen')
        if genre == 'Not chosen':
            print("❌ Please select a genre first")
            input("Press Enter to continue...")
            return

        counterparts = PROTAGONIST_COUNTERPARTS.get(genre, ["Antagonist", "Love Interest", "Rival", "Ally"])

        print(f"Counterpart options for {genre}:")
        for i, counterpart in enumerate(counterparts, 1):
            print(f"{i}. {counterpart}")
        print(f"{len(counterparts)+1}. Keep current ({blueprint_data.get('counterpart_type', 'Not chosen')})")

        try:
            choice = int(input(f"Select counterpart (1-{len(counterparts)+1}): "))
            if 1 <= choice <= len(counterparts):
                blueprint_data['counterpart_type'] = counterparts[choice-1]
                print(f"✓ Counterpart set to: {counterparts[choice-1]}")

                # Now ask for counterpart gender
                self._set_counterpart_gender(blueprint_data)
            else:
                print("✓ Counterpart unchanged")
        except ValueError:
            print("❌ Invalid input")

        input("Press Enter to continue...")

    def set_counterpart_gender(self, blueprint_data):
        """Set counterpart character gender (public method)"""
        if blueprint_data.get('counterpart_type', 'Not chosen') == 'Not chosen':
            print("❌ Please select a counterpart character first")
            input("Press Enter to continue...")
            return
        
        print("\n" + "-"*40)
        print("COUNTERPART GENDER")
        print("-"*40)
        print(f"Set the gender for the {blueprint_data['counterpart_type']}.\n")
        
        self._set_counterpart_gender(blueprint_data)
        input("Press Enter to continue...")

    def _set_counterpart_gender(self, blueprint_data):
        """Set counterpart character gender (internal method)"""
        counterpart_type = blueprint_data.get('counterpart_type', 'counterpart')
        current_gender = blueprint_data.get('counterpart_gender', 'Not chosen')
        
        print(f"Choose gender for the {counterpart_type}:")
        for i, gender in enumerate(GENDERS, 1):
            print(f"{i}. {gender}")
        print(f"{len(GENDERS)+1}. Keep current ({current_gender})")

        try:
            choice = int(input(f"Select gender (1-{len(GENDERS)+1}): "))
            if 1 <= choice <= len(GENDERS):
                blueprint_data['counterpart_gender'] = GENDERS[choice-1]
                print(f"✓ {counterpart_type} gender set to: {GENDERS[choice-1]}")
                # Force save the data immediately
                print(f"DEBUG: Saved counterpart_gender as: {blueprint_data['counterpart_gender']}")
            elif choice == len(GENDERS)+1:
                print("✓ Gender unchanged")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
