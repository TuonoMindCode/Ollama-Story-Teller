class SceneUserPromptBuilder:
    """Comprehensive scene user prompt builder with multi-select options"""
    
    def __init__(self, template_manager):
        self.template_manager = template_manager
    
    def create_comprehensive_scene_user_prompt(self):
        """Build a comprehensive scene user prompt through multi-select interface"""
        print("\n" + "="*80)
        print("COMPREHENSIVE SCENE USER PROMPT BUILDER")
        print("="*80)
        print("Select which aspects you want to specify. Leave others as 'auto' for AI to decide.")
        print()
        
        # Define all scene elements
        scene_elements = self._get_scene_elements()
        
        # Show all categories with their current status (auto by default)
        selected_elements = {}
        for category in scene_elements.keys():
            selected_elements[category] = "auto"
        
        while True:
            self._display_current_selections(scene_elements, selected_elements)
            
            print("\nActions:")
            print("1-15: Configure category (enter category number)")
            print("G: Generate scene user prompt with current settings")
            print("R: Reset all to auto")
            print("Q: Quit without saving")
            
            choice = input("\nChoice: ").strip().upper()
            
            if choice == 'G':
                self._generate_scene_user_prompt(selected_elements)
                break
            elif choice == 'R':
                for category in selected_elements.keys():
                    selected_elements[category] = "auto"
                print("All categories reset to auto")
                input("Press Enter to continue...")
            elif choice == 'Q':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(scene_elements):
                category_index = int(choice) - 1
                category_key = list(scene_elements.keys())[category_index]
                selected_elements[category_key] = self._configure_category(scene_elements[category_key])
            else:
                print("Invalid choice")
                input("Press Enter to continue...")
    
    def _get_scene_elements(self):
        """Return the scene elements structure"""
        return {
            "scene_type": {
                "title": "SCENE TYPE",
                "options": [
                    "Dialogue-focused (conversation heavy)",
                    "Action scene (movement, conflict, tension)",
                    "Emotional scene (feelings, reactions, introspection)",
                    "Descriptive scene (setting, atmosphere, world-building)",
                    "Transitional scene (moving between locations/events)",
                    "Confrontation scene (argument, disagreement)",
                    "Revelation scene (secrets revealed, discoveries)",
                    "Bonding scene (relationship building, connection)"
                ]
            },
            
            "characters": {
                "title": "CHARACTER SETUP",
                "options": [
                    "Solo character (internal monologue/actions)",
                    "Two characters (intimate, focused interaction)",
                    "Small group (3-4 characters, manageable dynamics)",
                    "Larger group (5+ characters, complex interactions)",
                    "Strangers meeting for first time",
                    "Close friends or family",
                    "Romantic partners or potential partners",
                    "Enemies or rivals",
                    "Mentor and student relationship",
                    "Authority figure and subordinate"
                ]
            },
            
            "setting_time": {
                "title": "SETTING & TIME",
                "options": [
                    "Indoor setting (home, office, building)",
                    "Outdoor setting (nature, street, public space)",
                    "Morning (dawn, early morning energy)",
                    "Afternoon (midday, active time)",
                    "Evening (sunset, winding down)",
                    "Night (late, intimate, mysterious)",
                    "Modern contemporary setting",
                    "Historical period setting",
                    "Fantasy/magical world",
                    "Science fiction/futuristic",
                    "Small town/rural setting",
                    "Urban/city setting"
                ]
            },
            
            "mood_tone": {
                "title": "MOOD & ATMOSPHERE",
                "options": [
                    "Tense and suspenseful",
                    "Romantic and intimate",
                    "Light and humorous",
                    "Dark and serious",
                    "Melancholic and reflective",
                    "Energetic and upbeat",
                    "Mysterious and intriguing",
                    "Peaceful and calming",
                    "Dramatic and intense",
                    "Nostalgic and wistful",
                    "Awkward and uncomfortable",
                    "Warm and cozy"
                ]
            },
            
            "conflict_tension": {
                "title": "CONFLICT & TENSION",
                "options": [
                    "Internal conflict (character's inner struggle)",
                    "Interpersonal conflict (between characters)",
                    "External obstacle or challenge",
                    "Moral dilemma or difficult choice",
                    "Misunderstanding or miscommunication",
                    "Competing goals or desires",
                    "Past issues resurfacing",
                    "Secret being kept or revealed",
                    "Time pressure or urgency",
                    "No major conflict (peaceful interaction)"
                ]
            },
            
            "scene_purpose": {
                "title": "SCENE PURPOSE & GOALS",
                "options": [
                    "Character development and growth",
                    "Relationship building or strain",
                    "Plot advancement and story progress",
                    "World-building and atmosphere",
                    "Information sharing or revelation",
                    "Emotional catharsis or release",
                    "Setting up future events",
                    "Resolving previous issues",
                    "Creating mystery or questions",
                    "Providing comic relief",
                    "Building suspense or anticipation"
                ]
            },
            
            "dialogue_action": {
                "title": "DIALOGUE & ACTION BALANCE",
                "options": [
                    "Dialogue-heavy (lots of conversation)",
                    "Action-heavy (movement, physical activity)",
                    "Balanced dialogue and action",
                    "Mostly internal thoughts and observations",
                    "Heavy on environmental description",
                    "Fast-paced and dynamic",
                    "Slow and contemplative",
                    "Realistic everyday conversation",
                    "Dramatic or heightened dialogue",
                    "Subtle subtext and implications"
                ]
            },
            
            "main_character": {
                "title": "MAIN CHARACTER DETAILS",
                "options": [
                    "Female protagonist",
                    "Male protagonist", 
                    "Non-binary protagonist",
                    "Young adult character (18-25)",
                    "Middle-aged character (30-50)",
                    "Older character (50+)",
                    "Professional/career-focused character",
                    "Student character",
                    "Parent character",
                    "Single character (no romantic partner)"
                ]
            },
            
            "secondary_character": {
                "title": "SECONDARY CHARACTER",
                "options": [
                    "Opposite gender love interest",
                    "Same gender love interest", 
                    "Best friend/close friend",
                    "Family member (sibling, parent, etc.)",
                    "Coworker or boss",
                    "Stranger/new person",
                    "Ex-partner or former friend",
                    "Mentor or teacher figure",
                    "Rival or competitor",
                    "Authority figure (police, doctor, etc.)"
                ]
            },
            
            "relationship_dynamic": {
                "title": "RELATIONSHIP DYNAMIC",
                "options": [
                    "First meeting/strangers",
                    "Established romantic relationship",
                    "New romantic attraction/tension",
                    "Friends to lovers potential", 
                    "Enemies to lovers tension",
                    "Reconnecting after time apart",
                    "Professional relationship",
                    "Family dynamics",
                    "Mentor/student relationship",
                    "Power imbalance (boss/employee, etc.)"
                ]
            },
            
            "emotional_stakes": {
                "title": "EMOTIONAL STAKES",
                "options": [
                    "Life-changing decision to make",
                    "Secret that could change everything",
                    "Fear of vulnerability/opening up",
                    "Past trauma affecting present",
                    "Career or dream at risk",
                    "Relationship at a turning point",
                    "Family expectations vs. personal desires",
                    "Moral dilemma or ethical choice",
                    "Time pressure/deadline stress",
                    "Social pressure or judgment"
                ]
            },
            
            "scene_location": {
                "title": "SPECIFIC LOCATION",
                "options": [
                    "Coffee shop or cafe",
                    "Home/apartment (kitchen, living room)",
                    "Workplace (office, restaurant, etc.)",
                    "Car or during travel",
                    "Park or outdoor public space",
                    "Restaurant or bar",
                    "Hospital or medical setting",
                    "School or university",
                    "Shopping area or mall",
                    "Beach, lake, or nature setting"
                ]
            },
            
            "scene_catalyst": {
                "title": "WHAT TRIGGERS THE SCENE",
                "options": [
                    "Unexpected encounter/meeting",
                    "Planned meeting that goes differently",
                    "Emergency or crisis situation",
                    "Celebration or happy occasion",
                    "Argument or confrontation brewing",
                    "Discovery of something important",
                    "Deadline or time pressure",
                    "Someone asking for help",
                    "Misunderstanding that needs clearing",
                    "Life change announcement"
                ]
            },
            
            "point_of_view": {
                "title": "NARRATIVE PERSPECTIVE",
                "options": [
                    "First person (I) - main character",
                    "First person (I) - secondary character", 
                    "Second person (you) for intimacy",
                    "Mixed perspective (I and you) - intimate dialogue between two characters",
                    "Third person limited - main character",
                    "Third person limited - secondary character",
                    "Third person omniscient",
                    "Internal monologue heavy",
                    "Dialogue-focused minimal narration",
                    "Stream of consciousness style",
                    "Present tense for immediacy"
                ]
            },
            
            "content_boundaries": {
                "title": "CONTENT BOUNDARIES",
                "options": [
                    "Family-friendly/all ages appropriate",
                    "Mature themes but no explicit content",
                    "Romance with sensual tension allowed",
                    "Adult content/intimate scenes allowed",
                    "Violence/conflict acceptable",
                    "Strong language acceptable", 
                    "Dark themes (trauma, loss) acceptable",
                    "LGBTQ+ themes and characters",
                    "Mental health topics acceptable",
                    "Keep content light and positive"
                ]
            }
        }
    
    def _display_current_selections(self, scene_elements, selected_elements):
        """Display current selection status for all categories"""
        print("\n" + "="*70)
        print("SCENE USER PROMPT CONFIGURATION")
        print("="*70)
        
        category_keys = list(scene_elements.keys())
        for i, category_key in enumerate(category_keys, 1):
            title = scene_elements[category_key]["title"]
            status = selected_elements[category_key]
            
            if status == "auto":
                status_display = "AUTO (AI will decide)"
            else:
                if isinstance(status, list):
                    status_display = f"{len(status)} option(s) selected: {', '.join(status[:2])}{'...' if len(status) > 2 else ''}"
                else:
                    status_display = str(status)
            
            print(f"{i:2d}. {title:<25}: {status_display}")
    
    def _configure_category(self, category_data):
        """Configure a specific category"""
        print(f"\n{'='*60}")
        print(f"CONFIGURE {category_data['title']}")
        print(f"{'='*60}")
        print("Select options (comma-separated numbers), enter custom text, or press Enter for auto:")
        print()
        
        for i, option in enumerate(category_data['options'], 1):
            print(f"{i:2d}. {option}")
        
        print(f"{len(category_data['options']) + 1:2d}. CUSTOM - Write your own description")
        
        # Add examples option for narrative perspective
        if category_data['title'] == "NARRATIVE PERSPECTIVE":
            print(f"{len(category_data['options']) + 2:2d}. EXAMPLES - See writing samples for each perspective")
        
        print()
        
        user_input = input(f"Your choices (e.g., 1,3,5), custom text, or Enter for auto: ").strip()
        
        if not user_input:
            return "auto"
        
        # Check for examples option
        examples_option_num = len(category_data['options']) + 2
        if category_data['title'] == "NARRATIVE PERSPECTIVE" and user_input == str(examples_option_num):
            self._show_narrative_examples()
            return self._configure_category(category_data)  # Show menu again after examples
        
        # Check if it's a custom text input (not just numbers and commas)
        if not all(c.isdigit() or c in ',. ' for c in user_input):
            # This is custom text
            print(f"Custom setting: {user_input}")
            input("Press Enter to continue...")
            return [f"CUSTOM: {user_input}"]
        
        # Handle number selections
        try:
            choices = [int(x.strip()) for x in user_input.split(',')]
            
            selected_options = []
            custom_option_num = len(category_data['options']) + 1
            
            for choice in choices:
                if 1 <= choice <= len(category_data['options']):
                    selected_options.append(category_data['options'][choice-1])
                elif choice == custom_option_num:
                    # User selected custom option
                    custom_text = input("Enter your custom description: ").strip()
                    if custom_text:
                        selected_options.append(f"CUSTOM: {custom_text}")
            
            if selected_options:
                print(f"Selected: {', '.join(selected_options)}")
                input("Press Enter to continue...")
                return selected_options
            else:
                print("No valid selections - setting to auto")
                input("Press Enter to continue...")
                return "auto"
        except ValueError:
            # If parsing as numbers failed, treat as custom text
            print(f"Custom setting: {user_input}")
            input("Press Enter to continue...")
            return [f"CUSTOM: {user_input}"]
    
    def _generate_scene_user_prompt(self, selected_elements):
        """Generate the final user prompt based on selections - FIXED VERSION"""
        print(f"\n{'='*80}")
        print("GENERATING COMPREHENSIVE SCENE USER PROMPT")
        print(f"{'='*80}")
        
        # Count specified vs auto
        specified_count = sum(1 for sel in selected_elements.values() if sel != "auto")
        auto_count = len(selected_elements) - specified_count
        
        # Give helpful feedback
        if specified_count == 0:
            print("⚠️  ALL CATEGORIES SET TO AUTO")
            print("The system will automatically choose specific options for a concrete prompt.")
            proceed = input("Continue? (y/n): ").strip().lower()
            if proceed != 'y':
                return
        elif specified_count <= 5:
            print(f"📝 MOSTLY AUTO ({specified_count} categories specified, {auto_count} auto)")
            print("The system will choose concrete options for auto categories.")
        else:
            print(f"🎯 HIGHLY SPECIFIED ({specified_count} categories specified)")
        
        # For auto selections, pick concrete choices instead of "AI should decide"
        import random
        scene_elements = self._get_scene_elements()
        
        concrete_selections = {}
        for category, selections in selected_elements.items():
            if selections == "auto":
                # Pick a random concrete choice from available options
                available_options = scene_elements[category]["options"]
                concrete_selections[category] = [random.choice(available_options)]
            else:
                concrete_selections[category] = selections
        
        # Build the AI instruction for creating a CONCRETE user prompt
        ai_system_prompt = """You are an expert creative writing prompt creator. Create a comprehensive, specific scene user prompt based on the provided specifications.

The user prompt should:
- Be detailed and specific using the provided choices
- Flow naturally as a single coherent prompt  
- Be around 150-250 words
- Focus on WHAT should happen in the scene, not HOW to write it
- Give concrete, actionable instructions to the AI
- Never use phrases like "AI should decide" - always be specific"""
        
        # Build concrete specifications
        specs = []
        for category, selections in concrete_selections.items():
            category_name = category.replace('_', ' ').title()
            specs.append(f"{category_name}: {', '.join(selections)}")
        
        specifications = "\n".join(specs)
        
        ai_user_prompt = f"""Create a comprehensive scene user prompt with these specifications:

{specifications}

The prompt should be concrete and specific, telling the AI exactly what scene to create. Do not use "AI should decide" language - be specific about all elements.

Return only the user prompt, nothing else."""
        
        # Check if model is available
        if not self.template_manager.model_tester.test_config.get('model'):
            print("No model selected. Please configure a model first.")
            input("Press Enter to continue...")
            return
        
        print("Generating your comprehensive scene user prompt...")
        
        result = self.template_manager.model_tester.stream_ollama_request(
            ai_system_prompt,
            ai_user_prompt,
            self.template_manager.model_tester.test_config,
            callback=None
        )
        
        if result['success']:
            generated_prompt = result['response'].strip()
            
            print(f"\nYOUR COMPREHENSIVE SCENE USER PROMPT:")
            print("="*70)
            print(generated_prompt)
            print("="*70)
            print(f"Word count: {len(generated_prompt.split())} words")
            
            # Show what was specified vs auto-chosen
            print(f"\nSPECIFICATIONS SUMMARY:")
            for category, original_selection in selected_elements.items():
                category_name = category.replace('_', ' ').title()
                if original_selection == "auto":
                    chosen = concrete_selections[category][0]
                    print(f"• {category_name}: Auto-chosen → {chosen}")
                else:
                    print(f"• {category_name}: User specified → {', '.join(original_selection)}")
            
            save = input(f"\nSave this scene user prompt? (y/n): ").strip().lower()
            if save == 'y':
                # Get a name for the prompt
                prompt_name = input("Enter a name for this prompt (or press Enter for auto-name): ").strip()
                if not prompt_name:
                    specified_count = sum(1 for sel in selected_elements.values() if sel != "auto")
                    prompt_name = f"comprehensive_scene_{specified_count}_specified"
                
                # Clean the name for filename
                safe_name = prompt_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
                
                if self.template_manager.save_user_prompt_template(safe_name, generated_prompt):
                    print(f"Scene user prompt saved successfully!")
                else:
                    print("Failed to save prompt.")
            else:
                print("Scene user prompt not saved.")
        else:
            print(f"Failed to generate prompt: {result.get('error', 'Unknown error')}")
        
        input("\nPress Enter to continue...")
    
    def _show_narrative_examples(self):
        """Show examples of different narrative perspectives"""
        print("\n" + "="*80)
        print("NARRATIVE PERSPECTIVE EXAMPLES")
        print("="*80)
        print("Here's how the same scene looks in different perspectives:")
        print()
        
        examples = [
            ("First person (I) - main character", 
             'I walked into the coffee shop and saw him sitting at our usual table. My heart skipped a beat as our eyes met across the room.'),
            
            ("First person (I) - secondary character", 
             'I watched her walk into the coffee shop, noting how she hesitated when she saw me. Her eyes widened with surprise.'),
            
            ("Second person (you) for intimacy", 
             'You walk into the coffee shop and see him at your usual table. Your heart skips a beat as his eyes meet yours across the room.'),
            
            ("Mixed perspective (I and you) - intimate dialogue", 
             'I walk into the coffee shop and see you at our usual table. "You came," you say softly. My heart races as I sit across from you. "I wasn\'t sure you would." The waitress approaches us, but neither of us looks away.'),
            
            ("Third person limited - main character", 
             'Sarah walked into the coffee shop and saw him sitting at their usual table. Her heart skipped a beat as their eyes met across the room.'),
        ]
        
        for i, (perspective, example) in enumerate(examples, 1):
            print(f"{i:2d}. {perspective.upper()}")
            print(f"    Example: {example}")
            print()
        
        input("Press Enter to return to perspective selection...")
