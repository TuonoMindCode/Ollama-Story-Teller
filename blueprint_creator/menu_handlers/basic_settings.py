"""Basic blueprint settings handlers"""
from ..config import *

class BasicSettingsHandler:
    def __init__(self, blueprint_creator):
        self.bc = blueprint_creator

    def set_blueprint_name(self, blueprint_data):
        """Set blueprint name"""
        print("\n" + "-"*40)
        print("BLUEPRINT NAME")
        print("-"*40)

        name = input(f"Enter blueprint name (current: {blueprint_data['name']}): ").strip()

        if name:
            # Clean filename
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_').lower()
            blueprint_data['name'] = safe_name
            print(f"✓ Blueprint name set to: {safe_name}")
        else:
            print("✓ Name unchanged")

        input("Press Enter to continue...")

    def set_genre(self, blueprint_data):
        """Set genre"""
        print("\n" + "-"*40)
        print("GENRE SELECTION")
        print("-"*40)

        print("Available genres:")
        for i, genre in enumerate(GENRES, 1):
            print(f"{i:2d}. {genre}")
        print(f"{len(GENRES)+1}. Keep current ({blueprint_data['genre']})")

        try:
            choice = int(input(f"Select genre (1-{len(GENRES)+1}): "))
            if 1 <= choice <= len(GENRES):
                blueprint_data['genre'] = GENRES[choice-1]
                print(f"✓ Genre set to: {GENRES[choice-1]}")
                # Reset subgenre when genre changes
                blueprint_data['subgenre'] = 'Not chosen'
            else:
                print("✓ Genre unchanged")
        except ValueError:
            print("❌ Invalid input, genre unchanged")

        input("Press Enter to continue...")

    def set_subgenre(self, blueprint_data):
        """Set subgenre"""
        print("\n" + "-"*40)
        print("SUBGENRE SELECTION")
        print("-"*40)

        if blueprint_data['genre'] == 'Not chosen':
            print("❌ Please select a genre first")
            input("Press Enter to continue...")
            return

        available_subgenres = SUBGENRES.get(blueprint_data['genre'], [])

        if not available_subgenres:
            print(f"No specific subgenres available for {blueprint_data['genre']}")
            input("Press Enter to continue...")
            return

        print(f"Subgenres for {blueprint_data['genre']}:")
        for i, subgenre in enumerate(available_subgenres, 1):
            print(f"{i}. {subgenre}")
        print(f"{len(available_subgenres)+1}. Keep current ({blueprint_data['subgenre']})")

        try:
            choice = int(input(f"Select subgenre (1-{len(available_subgenres)+1}): "))
            if 1 <= choice <= len(available_subgenres):
                blueprint_data['subgenre'] = available_subgenres[choice-1]
                print(f"✓ Subgenre set to: {available_subgenres[choice-1]}")
            else:
                print("✓ Subgenre unchanged")
        except ValueError:
            print("❌ Invalid input, subgenre unchanged")

        input("Press Enter to continue...")

    def set_target_audience(self, blueprint_data):
        """Set target audience and content rating"""
        print("\n" + "-"*50)
        print("TARGET AUDIENCE & CONTENT RATING")
        print("-"*50)
        print("Choose who this story is designed for. This affects content,")
        print("language, themes, and story elements.\n")

        audience_options = {
            "children": {
                "description": "Ages 3-8: Simple stories, animated style, no scary content",
                "content_rating": "children",
                "language": ("clean", "restrained", "casual"),
                "restrictions": ["No violence", "No death", "No scary themes", "Simple vocabulary"]
            },
            "family": {
                "description": "Ages 8+: Family-friendly with mild conflict, life lessons",
                "content_rating": "family",
                "language": ("clean", "restrained", "casual"),
                "restrictions": ["No graphic violence", "No death scenes", "No adult themes", "Positive messages"]
            },
            "teen": {
                "description": "Ages 13+: Coming-of-age themes, mild language, relationship drama",
                "content_rating": "teen",
                "language": ("mild", "moderate", "casual"),
                "restrictions": ["Mild language OK", "Romance without explicit content", "Some conflict"]
            },
            "adult": {
                "description": "Ages 18+: Mature themes, complex relationships, realistic content",
                "content_rating": "adult",
                "language": ("moderate", "moderate", "casual"),
                "restrictions": ["All themes allowed", "Realistic language", "Complex subjects"]
            }
        }

        print("Available audiences:")
        for i, (key, info) in enumerate(audience_options.items(), 1):
            print(f"{i}. {key.title()}: {info['description']}")
        
        print(f"5. Custom: Write your own content guidelines")

        current = blueprint_data.get('target_audience', 'Not chosen')
        print(f"6. Keep current ({current})")

        try:
            choice = int(input(f"\nSelect audience (1-6): "))
            keys = list(audience_options.keys())

            if 1 <= choice <= len(keys):
                selected = keys[choice-1]
                audience_info = audience_options[selected]

                blueprint_data['target_audience'] = selected
                blueprint_data['content_rating'] = audience_info['content_rating']
                blueprint_data['language_settings'] = audience_info['language']

                print(f"✅ Target audience set to: {selected.title()}")
                print(f"📝 Content rating: {audience_info['content_rating']}")
                print(f"🗣️ Language: {audience_info['language'][0]} profanity, {audience_info['language'][1]} intensity")

                # Show restrictions
                print("\n📋 Content guidelines:")
                for restriction in audience_info['restrictions']:
                    print(f"   • {restriction}")

                # Auto-adjust genre elements based on audience
                self._adjust_genre_for_audience(blueprint_data, selected)

            elif choice == 5:
                # Custom content guidelines
                self._set_custom_content_guidelines(blueprint_data)
                
            elif choice == 6:
                print("✅ Audience unchanged")
            else:
                print("❌ Invalid choice")

        except ValueError:
            print("❌ Invalid input")

        input("Press Enter to continue...")

    def _set_custom_content_guidelines(self, blueprint_data):
        """Set custom content guidelines"""
        print("\n" + "-"*50)
        print("CUSTOM CONTENT GUIDELINES")
        print("-"*50)
        print("Define your own content restrictions and themes.\n")
        
        print("Examples of custom guidelines:")
        print("• Unrestricted content, all themes and topics allowed")
        print("• Uncensored storytelling with mature themes")
        print("• No content limitations, dark themes permitted")
        print("• Adult themes with realistic consequences")
        print("• Mature content with psychological depth")
        print("• No restrictions on violence, language, or adult situations")
        print("• Dark fantasy with morally complex characters")
        print("• Realistic adult relationships and conflicts")
        
        print(f"\nCurrent: {blueprint_data.get('target_audience', 'Not chosen')}")
        
        custom_guidelines = input("\nEnter your custom content guidelines: ").strip()
        
        if custom_guidelines:
            # Store with "Custom: " prefix to identify it as custom
            blueprint_data['target_audience'] = f"Custom: {custom_guidelines}"
            blueprint_data['content_rating'] = 'custom'
            blueprint_data['language_settings'] = ('unrestricted', 'unrestricted', 'casual')
            
            print(f"✅ Custom guidelines set:")
            print(f"   {custom_guidelines}")
            print(f"📝 Content rating: custom")
            print(f"🗣️ Language: unrestricted")
        else:
            print("❌ No guidelines entered, audience unchanged")

    def _adjust_genre_for_audience(self, blueprint_data, audience):
        """Automatically adjust genre elements based on target audience"""
        # If it's a detective/mystery story for children or family
        if (blueprint_data.get('genre') == 'Mystery' and
            audience in ['children', 'family']):

            print("\n💡 GENRE ADJUSTMENT")
            print("Detective/Mystery story adjusted for family audience:")
            print("• No murders - focus on missing items, puzzles, or mysteries")
            print("• Friendly detective character")
            print("• Solutions through cleverness, not violence")

            # Update custom instructions
            family_mystery_note = "Family-friendly mystery: no murders or violence, focus on puzzles and missing items that can be solved through cleverness and teamwork"

            current_instructions = blueprint_data.get('custom_instructions', 'Not chosen')
            if current_instructions == 'Not chosen':
                blueprint_data['custom_instructions'] = family_mystery_note
            else:
                blueprint_data['custom_instructions'] += f". {family_mystery_note}"

        # Horror for children becomes "spooky but not scary"
        elif (blueprint_data.get('genre') == 'Horror' and
              audience == 'children'):

            print("\n💡 GENRE ADJUSTMENT")
            print("Horror story adjusted for children:")
            print("• 'Spooky' atmosphere instead of scary")
            print("• Friendly monsters or silly scares")
            print("• Happy, reassuring ending")

            spooky_note = "Child-friendly spooky story: friendly monsters, silly scares, no real danger, happy ending that shows there was nothing to fear"
            current_instructions = blueprint_data.get('custom_instructions', 'Not chosen')
            if current_instructions == 'Not chosen':
                blueprint_data['custom_instructions'] = spooky_note
            else:
                blueprint_data['custom_instructions'] += f". {spooky_note}"
