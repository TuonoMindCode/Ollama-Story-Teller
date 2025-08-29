"""Story elements settings handlers"""
from ..config import *
from generators.narrative_style_examples import NARRATIVE_STYLE_EXAMPLES, show_all_style_examples

class StoryElementsHandler:
    def __init__(self, blueprint_creator):
        self.bc = blueprint_creator

    def set_storytelling_style(self, blueprint_data):
        """Set storytelling style"""
        print("\n" + "-"*40)
        print("STORYTELLING STYLE")
        print("-"*40)
        print("Choose how your story unfolds and is structured.\n")

        print("Available storytelling styles:")
        for i, style in enumerate(STORYTELLING_STYLES, 1):
            print(f"{i:2d}. {style}")
        print(f"{len(STORYTELLING_STYLES)+1}. Keep current ({blueprint_data['storytelling_style']})")

        try:
            choice = int(input(f"Select style (1-{len(STORYTELLING_STYLES)+1}): "))
            if 1 <= choice <= len(STORYTELLING_STYLES):
                blueprint_data['storytelling_style'] = STORYTELLING_STYLES[choice-1]
                print(f"✓ Storytelling style set to: {STORYTELLING_STYLES[choice-1]}")
            else:
                print("✓ Style unchanged")
        except ValueError:
            print("❌ Invalid input, style unchanged")

        input("Press Enter to continue...")

    def set_perspective(self, blueprint_data):
        """Set narrative perspective with detailed examples"""
        print("\n" + "-"*60)
        print("NARRATIVE PERSPECTIVE")
        print("-"*60)
        print("Choose the narrative viewpoint for your story. This affects how")
        print("the story is told and what the reader experiences.\n")

        # Define perspectives with detailed examples - UPDATED WITH ALL EXAMPLES
        perspective_examples = {
            "First person singular": {
                "description": "Story told by one character using 'I', 'me', 'my'",
                "example": "I walked into the dark alley, my heart pounding. I knew someone was following me, but I couldn't see who.",
                "good_for": "Personal, intimate stories; mysteries where reader discovers clues with protagonist; emotional journeys",
                "limitations": "Reader only knows what the narrator knows; can't show other characters' thoughts"
            },
            "First person plural": {
                "description": "Story told by a group using 'we', 'us', 'our'",
                "example": "We entered the abandoned house together, our flashlights cutting through the darkness. We all felt the same chill down our spines.",
                "good_for": "Group adventures; collective experiences; community stories; cult or group dynamics",
                "limitations": "Harder to develop individual characters; can feel impersonal"
            },
            "Second person": {
                "description": "Story told directly to the reader using 'you', 'your'",
                "example": "You push open the creaky door and step inside. Your eyes adjust to the dim light as you realize you're not alone.",
                "good_for": "Interactive feeling; horror; choose-your-own-adventure style; immersive experiences",
                "limitations": "Can feel gimmicky; difficult to sustain; not suitable for all genres"
            },
            "Third person limited": {
                "description": "Follows one character closely, using 'he', 'she', 'they' but only knowing their thoughts",
                "example": "Sarah walked into the room, her palms sweating. She could see David watching her, but she had no idea what he was thinking.",
                "good_for": "Most common choice; combines intimacy with flexibility; mystery; character development",
                "limitations": "Limited to one character's knowledge and perspective"
            },
            "Third person omniscient": {
                "description": "All-knowing narrator who can reveal any character's thoughts and information",
                "example": "Sarah entered nervously, unaware that David had been planning this confrontation for weeks. Meanwhile, outside, the storm was gathering strength.",
                "good_for": "Complex plots; multiple storylines; epic/fantasy; when you need to show the 'big picture'",
                "limitations": "Can feel distant; harder to create suspense; risk of info-dumping"
            },
            "Third person multiple": {
                "description": "Switches between different characters' limited perspectives in different scenes",
                "example": "Chapter 1 - Sarah's POV: 'I have to tell him the truth.' Chapter 2 - David's POV: 'Something's wrong with Sarah, but I can't figure out what.'",
                "good_for": "Complex relationships; multiple storylines; showing different sides of events; ensemble casts",
                "limitations": "Can be confusing; requires clear transitions; harder to maintain consistent voice"
            },
            "Mixed perspectives": {
                "description": "Combines different perspectives throughout the story for artistic effect",
                "example": "I remember that day clearly (1st person). You wouldn't believe what happened next (2nd person). Sarah had no idea what was coming (3rd person).",
                "good_for": "Experimental fiction; artistic storytelling; meta-narratives; complex literary works",
                "limitations": "Very challenging; can confuse readers; requires skilled execution"
            }
        }

        print("📖 PERSPECTIVE OPTIONS:")
        for i, perspective in enumerate(PERSPECTIVES, 1):
            info = perspective_examples.get(perspective, {
                "description": perspective, 
                "example": "Example not available", 
                "good_for": "Various story types", 
                "limitations": "Depends on execution"
            })
            print(f"\n{i}. {perspective.upper()}")
            print(f"   📝 {info['description']}")
            print(f"   💭 Example: \"{info['example']}\"")

        current_perspective = blueprint_data['perspective']
        print(f"\n{len(PERSPECTIVES)+1}. Keep current ({current_perspective})")

        try:
            choice = int(input(f"\nSelect perspective (1-{len(PERSPECTIVES)+1}): "))
            if 1 <= choice <= len(PERSPECTIVES):
                selected_perspective = PERSPECTIVES[choice-1]
                blueprint_data['perspective'] = selected_perspective
                print(f"✅ Perspective set to: {selected_perspective}")
            else:
                print("✅ Perspective unchanged")
        except ValueError:
            print("❌ Invalid input, perspective unchanged")

        input("\nPress Enter to continue...")

    def set_narrative_style(self, blueprint_data):
        """Set narrative writing style with examples"""
        print("\n" + "-"*70)
        print("NARRATIVE WRITING STYLE")
        print("-"*70)
        print("Choose the writing style and voice for your stories.")
        print("This affects the mood, tone, and how the story feels to read.")
        print("Different from perspective (who tells the story), this is HOW it's told.\n")

        # Extract style names from your examples
        styles = []
        for style_key, style_data in NARRATIVE_STYLE_EXAMPLES.items():
            styles.append(style_data['name'])

        print("📖 AVAILABLE NARRATIVE STYLES:")
        print("="*70)

        for i, style in enumerate(styles, 1):
            print(f"{i:2d}. {style}")

        print(f"{len(styles)+1}. View detailed examples of all styles")
        print(f"{len(styles)+2}. Keep current ({blueprint_data.get('narrative_style', 'Not chosen')})")

        try:
            choice = int(input(f"\nSelect style (1-{len(styles)+2}): "))

            if 1 <= choice <= len(styles):
                selected_style = styles[choice-1]
                blueprint_data['narrative_style'] = selected_style
                print(f"✅ Narrative style set to: {selected_style}")

            elif choice == len(styles)+1:
                # Show all examples
                print("\n🎭 DETAILED STYLE EXAMPLES")
                show_all_style_examples()

            else:
                print("✅ Narrative style unchanged")

        except ValueError:
            print("❌ Invalid input, narrative style unchanged")

        input("Press Enter to continue...")

    def set_language_style(self, blueprint_data):
        """Set language and dialogue style"""
        print("\n" + "-"*50)
        print("LANGUAGE & DIALOGUE STYLE")
        print("-"*50)

        # Check if target audience is set - if so, show recommendations
        audience = blueprint_data.get('target_audience', 'Not chosen')
        if audience != 'Not chosen':
            print(f"Current target audience: {audience.title()}")
            recommended = blueprint_data.get('language_settings', ('moderate', 'moderate', 'casual'))
            print(f"Recommended for {audience}: {recommended[0]} profanity, {recommended[1]} intensity, {recommended[2]} style")
            print("You can override these recommendations below.\n")

        try:
            # Import the language configurator
            from story_generation_menu.language_configurator import LanguageConfigurator
            language_config = LanguageConfigurator()

            # Get current settings or defaults
            current_settings = blueprint_data.get('language_settings', ('moderate', 'moderate', 'casual'))
            profanity, intensity, style = current_settings

            # Configure language
            new_profanity, new_intensity, new_style = language_config.configure_language_style(
                profanity, intensity, style
            )

            # Check for conflicts with target audience
            if audience != 'Not chosen':
                content_rating = blueprint_data.get('content_rating', 'adult')
                conflicts = language_config.check_content_conflicts(content_rating, new_profanity, new_intensity)

                if conflicts:
                    print(f"\n⚠️ Your language settings may conflict with {audience} audience!")
                    result = language_config.resolve_conflicts_menu(
                        content_rating, new_profanity, new_intensity, new_style
                    )

                    if len(result) == 4:  # Content rating was changed
                        new_profanity, new_intensity, new_style, new_rating = result
                        blueprint_data['content_rating'] = new_rating
                        blueprint_data['target_audience'] = 'adult'  # Update audience too
                    else:
                        new_profanity, new_intensity, new_style = result

            # Save the settings
            blueprint_data['language_settings'] = (new_profanity, new_intensity, new_style)

            print(f"✅ Language style set: {new_profanity} + {new_intensity} + {new_style}")
        
        except ImportError:
            print("❌ Language configurator not available. Using simple configuration.")
            self._simple_language_config(blueprint_data)

    def _simple_language_config(self, blueprint_data):
        """Simple language configuration fallback"""
        print("1. Clean language (no profanity)")
        print("2. Mild language (occasional mild profanity)")
        print("3. Moderate language (some profanity)")
        print("4. Strong language (frequent profanity)")
        print("5. Keep current")
        
        try:
            choice = int(input("Select language level (1-5): "))
            if choice == 1:
                blueprint_data['language_settings'] = ('clean', 'restrained', 'casual')
            elif choice == 2:
                blueprint_data['language_settings'] = ('mild', 'moderate', 'casual')
            elif choice == 3:
                blueprint_data['language_settings'] = ('moderate', 'moderate', 'casual')
            elif choice == 4:
                blueprint_data['language_settings'] = ('strong', 'passionate', 'casual')
            print("✅ Language settings updated")
        except ValueError:
            print("❌ Invalid input")

    def set_setting_type(self, blueprint_data):
        """Set setting type"""
        print("\n" + "-"*40)
        print("SETTING TYPE")
        print("-"*40)

        print("Available settings:")
        for i, setting in enumerate(SETTING_TYPES, 1):
            print(f"{i:2d}. {setting}")
        print(f"{len(SETTING_TYPES)+1}. Keep current ({blueprint_data['setting_type']})")

        try:
            choice = int(input(f"Select setting (1-{len(SETTING_TYPES)+1}): "))
            if 1 <= choice <= len(SETTING_TYPES):
                blueprint_data['setting_type'] = SETTING_TYPES[choice-1]
                print(f"✓ Setting set to: {SETTING_TYPES[choice-1]}")
            else:
                print("✓ Setting unchanged")
        except ValueError:
            print("❌ Invalid input, setting unchanged")

        input("Press Enter to continue...")

    def set_tone(self, blueprint_data):
        """Set story tone"""
        print("\n" + "-"*40)
        print("STORY TONE")
        print("-"*40)

        print("Available tones:")
        for i, tone in enumerate(TONES, 1):
            print(f"{i:2d}. {tone}")
        print(f"{len(TONES)+1}. Keep current ({blueprint_data['tone']})")

        try:
            choice = int(input(f"Select tone (1-{len(TONES)+1}): "))
            if 1 <= choice <= len(TONES):
                blueprint_data['tone'] = TONES[choice-1]
                print(f"✓ Tone set to: {TONES[choice-1]}")
            else:
                print("✓ Tone unchanged")
        except ValueError:
            print("❌ Invalid input, tone unchanged")

        input("Press Enter to continue...")

    def set_complexity(self, blueprint_data):
        """Set story complexity"""
        print("\n" + "-"*40)
        print("STORY COMPLEXITY")
        print("-"*40)

        print("Available complexity levels:")
        for i, complexity in enumerate(COMPLEXITIES, 1):
            print(f"{i}. {complexity}")
        print(f"{len(COMPLEXITIES)+1}. Keep current ({blueprint_data['complexity']})")

        try:
            choice = int(input(f"Select complexity (1-{len(COMPLEXITIES)+1}): "))
            if 1 <= choice <= len(COMPLEXITIES):
                blueprint_data['complexity'] = COMPLEXITIES[choice-1]
                print(f"✓ Complexity set to: {COMPLEXITIES[choice-1]}")
            else:
                print("✓ Complexity unchanged")
        except ValueError:
            print("❌ Invalid input, complexity unchanged")

        input("Press Enter to continue...")

    def set_special_elements(self, blueprint_data):
        """Set special story elements"""
        print("\n" + "-"*40)
        print("SPECIAL ELEMENTS")
        print("-"*40)

        print("Available elements (select multiple with commas):")
        for i, element in enumerate(SPECIAL_ELEMENTS, 1):
            print(f"{i:2d}. {element}")

        if blueprint_data['special_elements']:
            print(f"\nCurrently selected: {', '.join(blueprint_data['special_elements'])}")

        print(f"\nEnter numbers separated by commas (e.g., 1,3,7)")
        print("Press Enter to keep current selection")
        print("Type 'clear' to remove all selections")

        selection = input("Selection: ").strip()

        if selection.lower() == 'clear':
            blueprint_data['special_elements'] = []
            print("✓ All special elements cleared")
        elif selection:
            try:
                selected_nums = [int(x.strip()) for x in selection.split(',')]
                selected_elements = []
                for num in selected_nums:
                    if 1 <= num <= len(SPECIAL_ELEMENTS):
                        selected_elements.append(SPECIAL_ELEMENTS[num-1])

                blueprint_data['special_elements'] = selected_elements
                if selected_elements:
                    print("✓ Selected elements:")
                    for element in selected_elements:
                        print(f"  • {element}")
                else:
                    print("✓ No valid elements selected")
            except ValueError:
                print("❌ Invalid input, selection unchanged")
        else:
            print("✓ Selection unchanged")

        input("Press Enter to continue...")

    def set_custom_instructions(self, blueprint_data):
        """Set custom instructions"""
        print("\n" + "-"*40)
        print("CUSTOM INSTRUCTIONS")
        print("-"*40)
        print("Add specific requirements or details for your blueprint.")
        print("Examples:")
        print("• 'Include a dog as a key character'")
        print("• 'Set in 1920s Chicago during Prohibition'")
        print("• 'The killer must be someone unexpected'")

        if blueprint_data['custom_instructions'] != 'Not chosen':
            print(f"\nCurrent: {blueprint_data['custom_instructions']}")

        print("\nEnter instructions (or press Enter to keep current):")
        instructions = input("Instructions: ").strip()

        if instructions:
            blueprint_data['custom_instructions'] = instructions
            print("✓ Custom instructions updated")
        else:
            print("✓ Instructions unchanged")

        input("Press Enter to continue...")
