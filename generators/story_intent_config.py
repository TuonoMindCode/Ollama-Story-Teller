"""
Story Intent Configuration System
Allows users to define key story elements, goals, and direction
"""

from .narrative_style_examples import NARRATIVE_STYLE_EXAMPLES, show_all_style_examples

class StoryIntentConfigurator:
    """Handles configuration of story direction, goals, and key elements"""
    
    STORY_INTENT_OPTIONS = {
        "protagonist_goal": {
            "label": "Main Character's Goal",
            "description": "What does your protagonist want to achieve?",
            "examples": [
                "Seeks redemption for past mistakes",
                "Wants to find their true identity", 
                "Trying to save someone they love",
                "Pursuing a lifelong dream",
                "Escaping a dangerous situation",
                "Seeking revenge against those who wronged them",
                "Learning to trust others again",
                "Discovering hidden family secrets",
                "Overcoming a personal fear or weakness",
                "Fighting for justice in an unjust world",
                "Proving their worth to others",
                "Breaking free from family expectations",
                "Finding their place in the world",
                "Mastering a difficult skill or art",
                "Uncovering a conspiracy or hidden truth"
            ]
        },
        "story_theme": {
            "label": "Central Theme/Message",
            "description": "What deeper meaning should the story convey?",
            "examples": [
                "Love conquers all obstacles",
                "Truth always comes to light",
                "Sometimes you must lose everything to find yourself",
                "Family bonds are stronger than blood",
                "Courage isn't the absence of fear, but acting despite it",
                "The past doesn't define your future",
                "True strength comes from vulnerability",
                "Sometimes the greatest enemy is yourself",
                "Hope can survive even in darkness",
                "Change is the only constant in life",
                "Power corrupts, but love redeems",
                "Second chances can change everything",
                "Sometimes the journey matters more than the destination",
                "What makes us human is our capacity for growth",
                "Every ending is a new beginning"
            ]
        },
        "story_outcome": {
            "label": "Desired Story Outcome",
            "description": "How should the story conclude?",
            "examples": [
                "Bittersweet victory with personal growth",
                "Triumphant success after great struggle",
                "Tragic but meaningful sacrifice",
                "Unexpected twist that changes everything", 
                "Quiet, contemplative resolution",
                "Open ending that leaves questions",
                "Full circle return to the beginning",
                "Complete transformation of the protagonist",
                "Restoration of what was lost",
                "New beginning after destruction",
                "Pyrrhic victory with heavy cost",
                "Redemption through selfless action",
                "Acceptance of unchangeable circumstances",
                "Unity after division and conflict",
                "Wisdom gained through hardship"
            ]
        },
        "key_events": {
            "label": "Must-Include Story Moments",
            "description": "What crucial scenes or events must happen?",
            "examples": [
                "A moment of betrayal by someone trusted",
                "A discovery that changes everything",
                "A choice between two impossible options",
                "A reunion after long separation",
                "A sacrifice that saves others",
                "A confrontation with the main antagonist",
                "A moment of complete despair before hope returns",
                "A revelation about the protagonist's past",
                "A test of the protagonist's core values",
                "A point of no return decision",
                "A mentor figure's death or departure",
                "An unexpected alliance with an enemy",
                "A moment where the protagonist almost gives up",
                "A scene showing the cost of the protagonist's choices",
                "A final showdown that tests everything learned"
            ]
        },
        "emotional_journey": {
            "label": "Emotional Arc",
            "description": "How should the protagonist change emotionally?",
            "examples": [
                "From broken to healed",
                "From naive to wise",
                "From selfish to selfless",
                "From fearful to brave",
                "From isolated to connected",
                "From angry to forgiving",
                "From lost to found",
                "From weak to strong",
                "From hopeless to hopeful",
                "From prideful to humble",
                "From cynical to believing",
                "From dependent to independent",
                "From bitter to compassionate",
                "From reckless to responsible",
                "From doubtful to confident"
            ]
        },
        "story_tone": {
            "label": "Overall Story Tone",
            "description": "What mood and atmosphere should dominate?",
            "examples": [
                "Dark and gritty with moments of hope",
                "Light-hearted with serious undertones",
                "Mysterious and suspenseful throughout",
                "Epic and grandiose in scope",
                "Intimate and character-focused",
                "Action-packed and fast-paced",
                "Contemplative and philosophical",
                "Romantic with emotional depth",
                "Comedic but with heart",
                "Tragic with beautiful moments",
                "Adventurous and optimistic",
                "Psychological and introspective",
                "Nostalgic and melancholic",
                "Inspiring and uplifting",
                "Complex moral ambiguity"
            ]
        },
        "narrative_style": {
            "label": "Narrative Style & Perspective",
            "description": "How should the story be told and from whose perspective?",
            "examples": [
                # CLEAR First Person Options
                "First Person Basic - Protagonist is 'I', others are 'he/she'. Example: 'I walked into the room and saw him standing there.'",
                
                "First Person with Inner Thoughts - Protagonist is 'I' with rich internal voice. Example: 'I walked in. *This can't be good,* I thought, seeing his expression.'",
                
                "Intimate First Person - Very personal 'I' voice with deep emotions. Example: 'I felt my heart shatter as I watched her leave. The pain was unbearable.'",
                
                # CLEAR Second Person Options
                "Second Person Romance - Protagonist is 'I', LOVE INTEREST is 'you', others are 'he/she'. Example: 'I smiled at you. \"I've missed you,\" I whispered as you took my hand.'",
                
                "Second Person Intimate - Very personal connection between 'I' and 'you'. Example: 'I couldn't stop looking at you. Everything about you drew me in.'",
                
                # ... other options ...
            ]
        },
        
        "inner_thoughts_style": {
            "label": "Inner Thoughts & Mental Voice",
            "description": "How should the character's internal thinking be presented?",
            "examples": [
                "Stream of consciousness - Raw, unfiltered thoughts: 'God why did I say that stupid stupid what's wrong with me...'",
                "Italicized thoughts - Clean separation: 'I smiled politely. *This is a disaster,* I thought.'",
                "Integrated naturally - Thoughts woven into narrative: 'I smiled, knowing this was a complete disaster.'",
                "Direct internal dialogue - Character talking to themselves: 'Come on, Sarah, you can do this.'",
                "Observational commentary - Character analyzing their surroundings and people",
                "Emotional reactions - Focus on feelings: 'My heart sank as I realized the truth.'",
                "Analytical thinking - Problem-solving and reasoning internal voice",
                "Anxious/worried thoughts - Constant concern and overthinking",
                "Confident internal voice - Self-assured internal commentary",
                "Conflicted thoughts - Internal debates and contradictions",
                "Memory-triggered thoughts - Past experiences influencing present thinking",
                "Sensory-driven thoughts - Internal reactions to what they see, hear, smell, feel"
            ]
        },
        
        "dialogue_style": {
            "label": "Dialogue & Character Interaction Style",
            "description": "How should characters speak and interact?",
            "examples": [
                "Natural conversational - Realistic, everyday speech patterns",
                "Witty and sharp - Quick, clever exchanges and banter",
                "Emotional and heartfelt - Deep, meaningful conversations",
                "Subtext heavy - Characters saying one thing but meaning another",
                "Period-appropriate - Historical or era-specific speech patterns",
                "Professional/formal - Business or formal social interactions",
                "Casual and modern - Contemporary, relaxed speech",
                "Romantic and intimate - Tender, loving exchanges",
                "Tense and confrontational - Conflict-driven dialogue",
                "Humorous and playful - Light, funny conversations",
                "Dramatic and intense - High-stakes, emotional exchanges",
                "Mysterious and cryptic - Hints and hidden meanings in speech"
            ]
        },
        
        "custom_requirements": {
            "label": "Custom Story Requirements",
            "description": "Specify exactly what should happen or be included in your story",
            "examples": [
                # Plot Requirements
                "The story must include a car chase scene in the middle",
                "There should be a dramatic confrontation between the protagonist and their sibling",
                "The protagonist must discover a hidden letter that changes everything",
                "Include a scene where the main character gets lost in the woods",
                "The story should feature a wedding that goes wrong",
                
                # Character Requirements  
                "Include a wise elderly character who gives crucial advice",
                "The protagonist must have a loyal dog companion throughout",
                "There should be a mysterious stranger who appears three times",
                "Include twins who are complete opposites of each other",
                "The main character should have a secret they're hiding from everyone",
                
                # Setting Requirements
                "The story must take place during a thunderstorm",
                "Include scenes in both a library and a coffee shop",
                "The story should span exactly one week",
                "Part of the story must happen on a train",
                "Include a scene in an abandoned building",
                
                # Object/McGuffin Requirements
                "A mysterious old photograph plays a key role in the plot",
                "There's an important family heirloom that gets lost and found",
                "A smartphone with a cracked screen becomes crucial to the story",
                "Include a handwritten journal with missing pages",
                "A music box that plays a specific melody is important",
                
                # Relationship Requirements
                "Two characters who hate each other must work together",
                "Include a reunion between old friends after many years",
                "The protagonist must choose between two people they care about",
                "There should be a mentor-student relationship that goes wrong",
                "Include a character who turns out to be related to the protagonist",
                
                # Emotional Requirements
                "The story must include a moment where the protagonist breaks down crying",
                "Include a scene of pure joy and celebration",
                "There should be a moment of complete silence and reflection",
                "The protagonist must face their greatest fear",
                "Include a scene where someone admits they were wrong",
                
                # Twist Requirements
                "The helpful character turns out to be the antagonist",
                "Something the protagonist believed about their past is completely false",
                "The 'victim' is actually the one in control",
                "The solution to the problem makes things worse initially",
                "The ending reveals the story was being told by someone unexpected"
            ]
        },
    }
    
    def __init__(self):
        self.configured_intent = {}
    
    def configure_interactive(self):
        """Interactive configuration of story intent"""
        print("\n🎯 STORY INTENT CONFIGURATION")
        print("="*60)
        print("Define the key elements that should drive your story...")
        print("(You can skip any category by pressing Enter)")
        
        for category, config in self.STORY_INTENT_OPTIONS.items():
            if category != "custom_requirements":
                self._configure_category(category, config)
        
        # Summary
        if self.configured_intent:
            print("\n✅ STORY INTENT SUMMARY:")
            print("-" * 40)
            for category, value in self.configured_intent.items():
                label = self.STORY_INTENT_OPTIONS[category]['label']
                print(f"📝 {label}: {value}")
        else:
            print("\n⚠️ No story intent configured - using default generation")
        
        return self.configured_intent
    
    def _configure_category(self, category, config):
        """Configure a single category of story intent"""
        print(f"\n📝 {config['label']}:")
        print(f"   {config['description']}")
        
        # Special handling for narrative style
        if category == "narrative_style":
            print("\n   📚 Would you like to see detailed examples of different styles?")
            see_examples = input("   Type 'yes' to see examples, or Enter to continue: ").strip().lower()
            if see_examples in ['yes', 'y']:
                show_all_style_examples()
        
        print("\n   Examples:")
        
        # Show first 8 examples
        for i, example in enumerate(config['examples'][:8], 1):
            # Truncate long examples for menu
            display_example = example[:100] + "..." if len(example) > 100 else example
            print(f"   {i}. {display_example}")
        
        if len(config['examples']) > 8:
            print(f"   ... and {len(config['examples']) - 8} more options")
        
        print(f"   {len(config['examples'][:8]) + 1}. [See all examples]")
        print(f"   {len(config['examples'][:8]) + 2}. [Write custom]")
        
        while True:
            choice = input(f"\nSelect option (1-{len(config['examples'][:8]) + 2}) or Enter to skip: ").strip()
            
            if choice == '':
                break
            elif choice.isdigit():
                choice_num = int(choice)
                if 1 <= choice_num <= len(config['examples'][:8]):
                    self.configured_intent[category] = config['examples'][choice_num - 1]
                    print(f"   ✓ Selected: {config['examples'][choice_num - 1]}")
                    break
                elif choice_num == len(config['examples'][:8]) + 1:
                    self._show_all_examples(config)
                elif choice_num == len(config['examples'][:8]) + 2:
                    custom = input("   Enter your custom option: ").strip()
                    if custom:
                        self.configured_intent[category] = custom
                        print(f"   ✓ Custom option saved: {custom}")
                        break
                else:
                    print("   ❌ Invalid choice. Please try again.")
            else:
                print("   ❌ Please enter a number or press Enter to skip.")
    
    def _show_all_examples(self, config):
        """Show all examples for a category"""
        print(f"\n   All examples for {config['label']}:")
        for i, example in enumerate(config['examples'], 1):
            print(f"   {i}. {example}")
        
        while True:
            choice = input(f"\nSelect example (1-{len(config['examples'])}) or Enter to go back: ").strip()
            if choice == '':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(config['examples']):
                category = None
                for cat, conf in self.STORY_INTENT_OPTIONS.items():
                    if conf == config:
                        category = cat
                        break
                
                if category:
                    self.configured_intent[category] = config['examples'][int(choice) - 1]
                    print(f"   ✓ Selected: {config['examples'][int(choice) - 1]}")
                return
            else:
                print("   ❌ Invalid choice. Please try again.")
    
    def load_from_file(self, filepath):
        """Load story intent configuration from file"""
        try:
            import json
            with open(filepath, 'r', encoding='utf-8') as f:
                self.configured_intent = json.load(f)
            print(f"✅ Story intent loaded from {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to load story intent: {e}")
            return False
    
    def save_to_file(self, filepath):
        """Save story intent configuration to file"""
        try:
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.configured_intent, f, indent=2, ensure_ascii=False)
            print(f"✅ Story intent saved to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to save story intent: {e}")
            return False
    
    def get_formatted_intent_for_prompts(self):
        """Get formatted story intent for inclusion in AI prompts"""
        if not self.configured_intent:
            return ""
        
        # Get basic story intent
        formatted = "\n\nSTORY INTENT REQUIREMENTS:\n"
        formatted += "The story MUST incorporate these key elements:\n"
        
        for category, value in self.configured_intent.items():
            if category == "custom_requirements":
                # Handle custom requirements specially
                if isinstance(value, list):
                    formatted += "\nCUSTOM STORY REQUIREMENTS (MANDATORY):\n"
                    for req in value:
                        formatted += f"• {req}\n"
                else:
                    formatted += f"• Custom Requirement: {value}\n"
            elif category not in ["narrative_style", "inner_thoughts_style", "dialogue_style"]:
                label = self.STORY_INTENT_OPTIONS[category]['label']
                formatted += f"• {label}: {value}\n"
        
        # Add narrative guidance separately for emphasis
        narrative_guidance = self.get_narrative_guidance_for_prompts()
        formatted += narrative_guidance
        
        formatted += "\nEnsure all story elements work together to achieve these goals."
        formatted += "\nThe custom requirements are MANDATORY and must be included in the story."
        return formatted
    
    def get_narrative_guidance_for_prompts(self):
        """Get specific narrative style guidance for AI prompts"""
        if not self.configured_intent:
            return ""
    
        guidance = ""
    
        if "narrative_style" in self.configured_intent:
            style = self.configured_intent["narrative_style"]
            guidance += f"\n\nNARRATIVE STYLE REQUIREMENTS:\n"
            guidance += f"CRITICAL: Write in this exact style: {style}\n"
    
            # FIXED: Second Person Intimate should use "you"
            if "Second Person Romance" in style or "Second Person Intimate" in style:
                guidance += "PRONOUNS:\n"
                guidance += "- Protagonist: 'I', 'me', 'my'\n"
                guidance += "- Love interest: 'you', 'your' (NEVER 'she/her' or 'he/him')\n"
                guidance += "- Other characters: 'she/her', 'he/him', 'they/them'\n"
                guidance += "- Focus on the intimate connection between 'I' and 'you'\n"
                guidance += "- Example: 'I looked at you across the room. You were breathtaking.'\n"
                guidance += "- DO NOT use 'she' or 'he' for the love interest - always 'you'\n"
    
            elif "First Person" in style:
                guidance += "PRONOUNS:\n"
                guidance += "- Protagonist: 'I', 'me', 'my'\n"
                guidance += "- Love interest: 'she/her' or 'he/him' (NOT 'you')\n"
                guidance += "- Other characters: 'she/her', 'he/him', 'they/them'\n"
                guidance += "- Include rich inner thoughts and observations\n"
                guidance += "- Example: 'I looked at her across the room. *She's beautiful,* I thought.'\n"
    
        return guidance
    
    def get_emotional_journey_guidance(self):
        """Get specific emotional journey guidance for AI prompts"""
        if not self.configured_intent:
            return ""
            
        if "emotional_journey" in self.configured_intent:
            journey = self.configured_intent["emotional_journey"]
            return f"\n\nEMOTIONAL JOURNEY:\nThe protagonist should change emotionally: {journey}"
        return ""
    
    def get_intent_summary(self):
        """Get a brief summary of configured intent"""
        if not self.configured_intent:
            return "No specific story intent configured"
        
        summary_parts = []
        for category, value in self.configured_intent.items():
            label = self.STORY_INTENT_OPTIONS[category]['label']
            # Truncate long values for summary
            short_value = value[:50] + "..." if len(value) > 50 else value
            summary_parts.append(f"{label}: {short_value}")
        
        return " | ".join(summary_parts)
    
    def clear_intent(self):
        """Clear all configured story intent"""
        self.configured_intent = {}
        print("✅ Story intent cleared")
    
    def quick_configure(self, **kwargs):
        """Quick configuration via keyword arguments"""
        for category, value in kwargs.items():
            if category in self.STORY_INTENT_OPTIONS:
                self.configured_intent[category] = value
            else:
                print(f"⚠️ Unknown story intent category: {category}")
        
        return self.configured_intent
    
    def configure_from_menu(self):
        """Standalone configuration menu for story intent"""
        while True:
            print("\n🎯 STORY INTENT CONFIGURATION MENU")
            print("="*50)
            
            if self.configured_intent:
                print("✅ Current Configuration:")
                for category, value in self.configured_intent.items():
                    label = self.STORY_INTENT_OPTIONS[category]['label']
                    if category == "custom_requirements":
                        # Show custom requirements differently
                        print(f"   📝 {label}:")
                        if isinstance(value, list):
                            for req in value:
                                print(f"      • {req}")
                        else:
                            print(f"      • {value}")
                    else:
                        short_value = value[:50] + "..." if len(value) > 50 else value
                        print(f"   📝 {label}: {short_value}")
            else:
                print("⚠️  No story intent configured yet")
            
            print("\nOptions:")
            print("1. Configure All Categories (Full Setup)")
            print("2. Configure Narrative Style Only")
            print("3. Configure Custom Story Requirements")  # NEW
            print("4. Configure Specific Category")
            print("5. View Current Settings")
            print("6. Clear All Settings")
            print("7. Save Configuration to File")
            print("8. Load Configuration from File")
            print("9. View Style Examples") 
            print("10. Return to Main Menu")
            
            choice = input("\nSelect option (1-10): ").strip()
            
            if choice == '1':
                self.configure_interactive()
            elif choice == '2':
                self._configure_narrative_style_only()
            elif choice == '3':  # NEW
                self._configure_custom_requirements()
            elif choice == '4':
                self._configure_specific_category()
            elif choice == '5':
                self._view_current_settings()
            elif choice == '6':
                self.clear_intent()
            elif choice == '7':
                self._save_configuration_menu()
            elif choice == '8':
                self._load_configuration_menu()
            elif choice == '9':
                self._show_style_examples_menu()
            elif choice == '10':
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def _configure_narrative_style_only(self):
        """Configure only the narrative style"""
        print("\n📖 NARRATIVE STYLE CONFIGURATION")
        print("-" * 40)
        
        category = "narrative_style"
        if category in self.STORY_INTENT_OPTIONS:
            config = self.STORY_INTENT_OPTIONS[category]
            self._configure_category(category, config)
        
        if "narrative_style" in self.configured_intent:
            print(f"\n✅ Narrative style set: {self.configured_intent['narrative_style'][:100]}...")
    
    def _configure_specific_category(self):
        """Allow user to configure just one specific category"""
        print("\n📝 SELECT CATEGORY TO CONFIGURE")
        print("-" * 40)
        
        categories = list(self.STORY_INTENT_OPTIONS.keys())
        for i, category in enumerate(categories, 1):
            label = self.STORY_INTENT_OPTIONS[category]['label']
            current = "✓" if category in self.configured_intent else " "
            print(f"{i}. [{current}] {label}")
        
        try:
            choice = int(input(f"\nSelect category (1-{len(categories)}): ").strip())
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                config = self.STORY_INTENT_OPTIONS[category]
                self._configure_category(category, config)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a number.")
    
    def _view_current_settings(self):
        """Display all current settings in detail"""
        print("\n📋 CURRENT STORY INTENT SETTINGS")
        print("=" * 60)
        
        if not self.configured_intent:
            print("⚠️  No configuration set")
            return
        
        for category, value in self.configured_intent.items():
            label = self.STORY_INTENT_OPTIONS[category]['label']
            print(f"\n📝 {label}:")
            print(f"   {value}")
        
        print("\n" + "=" * 60)
        input("Press Enter to continue...")
    
    def _save_configuration_menu(self):
        """Menu for saving configuration"""
        if not self.configured_intent:
            print("⚠️  No configuration to save")
            return
        
        filename = input("Enter filename (without extension): ").strip()
        if filename:
            filepath = f"story_configs/{filename}.json"
            import os
            os.makedirs("story_configs", exist_ok=True)
            self.save_to_file(filepath)
    
    def _load_configuration_menu(self):
        """Menu for loading configuration"""
        import os
        config_dir = "story_configs"
        
        if not os.path.exists(config_dir):
            print("⚠️  No saved configurations found")
            return
        
        files = [f for f in os.listdir(config_dir) if f.endswith('.json')]
        if not files:
            print("⚠️  No configuration files found")
            return
        
        print("\n📁 SAVED CONFIGURATIONS:")
        for i, filename in enumerate(files, 1):
            print(f"{i}. {filename.replace('.json', '')}")
        
        try:
            choice = int(input(f"\nSelect file (1-{len(files)}): ").strip())
            if 1 <= choice <= len(files):
                filepath = os.path.join(config_dir, files[choice - 1])
                self.load_from_file(filepath)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Please enter a number.")
    
    def _show_style_examples_menu(self):
        """Menu for viewing style examples"""
        try:
            from .narrative_style_examples import show_all_style_examples
            show_all_style_examples()
        except ImportError:
            print("⚠️  Style examples not available")
    
    def _configure_custom_requirements(self):
        """Configure custom story requirements"""
        print("\n📝 CUSTOM STORY REQUIREMENTS")
        print("="*50)
        print("Specify exactly what should happen or be included in your story.")
        print("You can add multiple requirements.")
        
        current_requirements = self.configured_intent.get("custom_requirements", [])
        if not isinstance(current_requirements, list):
            current_requirements = [current_requirements] if current_requirements else []
        
        while True:
            print(f"\n📋 Current Requirements ({len(current_requirements)}):")
            if current_requirements:
                for i, req in enumerate(current_requirements, 1):
                    print(f"   {i}. {req}")
            else:
                print("   (No requirements set)")
            
            print("\nOptions:")
            print("1. Add New Requirement")
            print("2. Choose from Examples")
            print("3. Remove a Requirement")
            print("4. Clear All Requirements")
            print("5. Done")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                req = input("\nEnter your custom requirement: ").strip()
                if req:
                    current_requirements.append(req)
                    print(f"✅ Added: {req}")
            
            elif choice == '2':
                self._add_requirement_from_examples(current_requirements)
            
            elif choice == '3':
                if current_requirements:
                    self._remove_requirement(current_requirements)
                else:
                    print("❌ No requirements to remove")
            
            elif choice == '4':
                if current_requirements:
                    confirm = input("Clear all requirements? (y/n): ").strip().lower()
                    if confirm == 'y':
                        current_requirements.clear()
                        print("✅ All requirements cleared")
                else:
                    print("❌ No requirements to clear")
            
            elif choice == '5':
                break
            
            else:
                print("❌ Invalid choice")
        
        # Save the requirements
        if current_requirements:
            self.configured_intent["custom_requirements"] = current_requirements
            print(f"\n✅ Saved {len(current_requirements)} custom requirements")
        elif "custom_requirements" in self.configured_intent:
            del self.configured_intent["custom_requirements"]
            print("\n✅ Custom requirements cleared")
    
    def _add_requirement_from_examples(self, current_requirements):
        """Add requirement from example list"""
        config = self.STORY_INTENT_OPTIONS["custom_requirements"]
        
        print(f"\n📚 Example Requirements:")
        for i, example in enumerate(config['examples'][:15], 1):  # Show first 15
            print(f"   {i}. {example}")
        
        if len(config['examples']) > 15:
            print(f"   ... and {len(config['examples']) - 15} more")
        
        print(f"   {len(config['examples'][:15]) + 1}. See all examples")
        
        try:
            choice = int(input(f"\nSelect example (1-{len(config['examples'][:15]) + 1}) or 0 to cancel: ").strip())
            
            if choice == 0:
                return
            elif 1 <= choice <= len(config['examples'][:15]):
                req = config['examples'][choice - 1]
                current_requirements.append(req)
                print(f"✅ Added: {req}")
            elif choice == len(config['examples'][:15]) + 1:
                self._show_all_requirement_examples(current_requirements)
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
    
    def _show_all_requirement_examples(self, current_requirements):
        """Show all requirement examples"""
        config = self.STORY_INTENT_OPTIONS["custom_requirements"]
        
        print(f"\n📚 All Example Requirements:")
        for i, example in enumerate(config['examples'], 1):
            print(f"   {i}. {example}")
        
        try:
            choice = int(input(f"\nSelect example (1-{len(config['examples'])}) or 0 to cancel: ").strip())
            
            if choice == 0:
                return
            elif 1 <= choice <= len(config['examples']):
                req = config['examples'][choice - 1]
                current_requirements.append(req)
                print(f"✅ Added: {req}")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
    
    def _remove_requirement(self, current_requirements):
        """Remove a requirement"""
        print("\n❌ Remove Requirement:")
        for i, req in enumerate(current_requirements, 1):
            print(f"   {i}. {req}")
        
        try:
            choice = int(input(f"\nSelect requirement to remove (1-{len(current_requirements)}): ").strip())
            
            if 1 <= choice <= len(current_requirements):
                removed = current_requirements.pop(choice - 1)
                print(f"✅ Removed: {removed}")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
