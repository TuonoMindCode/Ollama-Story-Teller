class StoryUserPromptBuilder:
    """Comprehensive story user prompt builder with multi-select options"""
    
    def __init__(self, template_manager):
        self.template_manager = template_manager
    
    def create_comprehensive_story_user_prompt(self):
        """Build a comprehensive story user prompt through multi-select interface"""
        print("\n" + "="*80)
        print("COMPREHENSIVE STORY USER PROMPT BUILDER")
        print("="*80)
        print("Select which aspects you want to specify. Leave others as 'auto' for AI to decide.")
        print("Note: Stories require longer output (~700+ tokens). Ensure your model supports this.")
        print()
        
        # Define all story elements
        story_elements = {
            "story_type": {
                "title": "STORY TYPE",
                "options": [
                    "Short story (complete narrative arc)",
                    "Character-driven story (focus on development)",
                    "Plot-driven story (focus on events/action)",
                    "Romance story (love as central theme)",
                    "Mystery/thriller story (suspense and reveals)",
                    "Drama story (emotional conflicts)",
                    "Coming-of-age story (growth and discovery)",
                    "Slice-of-life story (everyday moments)",
                    "Adventure story (journey and challenges)",
                    "Psychological story (internal struggles)"
                ]
            },
            
            "story_length_scope": {
                "title": "STORY LENGTH & SCOPE",
                "options": [
                    "Flash fiction (under 800 words, single moment)",
                    "Short story (800-1500 words, focused narrative)",
                    "Medium story (1500-3000 words, 2-3 scenes)",
                    "Long story (3000-5000 words, multiple scenes)",
                    "Extended story (5000+ words, fully developed)",
                    "Substantial story (3000+ words, fully developed)",
                    "Epic length (7000+ words, comprehensive narrative)",
                    "Single scene story (one location/time, detailed)",
                    "Multi-scene story (several scenes/locations)",
                    "Multiple scenes showing story development (3000+ words)",
                    "Story spanning hours (compressed timeframe)",
                    "Story spanning days (extended development)",
                    "Story spanning weeks/months (long-term arc)",
                    "Story spanning years (life-changing journey)",
                    "Chapter-length (2000-4000 words, part of larger work)",
                    "Novella scope (10000+ words, complex plot)"
                ]
            },
            
            "main_character": {
                "title": "PROTAGONIST",
                "options": [
                    "Female protagonist",
                    "Male protagonist", 
                    "Non-binary protagonist",
                    "Child protagonist (under 12)",
                    "Teen protagonist (13-17)",
                    "Young adult protagonist (18-25)",
                    "Middle-aged protagonist (30-50)",
                    "Older protagonist (50+)",
                    "Professional/career-focused character",
                    "Student character",
                    "Parent character",
                    "Artist/creative character",
                    "Working class character",
                    "Wealthy/privileged character"
                ]
            },
            
            "supporting_characters": {
                "title": "SUPPORTING CHARACTERS",
                "options": [
                    "Love interest (romantic partner)",
                    "Best friend/close friend",
                    "Family members (parents, siblings)",
                    "Mentor or guide figure",
                    "Antagonist/opponent",
                    "Coworkers or colleagues",
                    "Neighbors or community members",
                    "Children (if protagonist is parent)",
                    "Authority figures",
                    "Strangers who impact the story",
                    "Multiple supporting characters",
                    "Minimal supporting cast"
                ]
            },
            
            "central_conflict": {
                "title": "CENTRAL CONFLICT",
                "options": [
                    "Internal conflict (character vs. self)",
                    "Relationship conflict (character vs. character)",
                    "Societal conflict (character vs. society)",
                    "Environmental conflict (character vs. nature/circumstances)",
                    "Moral dilemma (right vs. wrong)",
                    "Choice between two goods (difficult decision)",
                    "Past vs. present (dealing with history)",
                    "Dreams vs. reality (aspirations vs. circumstances)",
                    "Love vs. duty (heart vs. obligation)",
                    "Individual vs. family expectations",
                    "Career vs. personal life",
                    "Fear vs. courage (overcoming limitations)"
                ]
            },
            
            "story_arc": {
                "title": "NARRATIVE ARC",
                "options": [
                    "Classic three-act structure (setup, confrontation, resolution)",
                    "Hero's journey (call to adventure, trials, return)",
                    "Character transformation arc (change and growth)",
                    "Redemption arc (from flawed to redeemed)",
                    "Fall from grace arc (from high to low)",
                    "Coming-of-age arc (innocence to maturity)",
                    "Romance arc (meeting to love)",
                    "Mystery arc (question to answer)",
                    "Circular story (ending where it began)",
                    "Open ending (unresolved conclusion)",
                    "Twist ending (surprise revelation)",
                    "Bittersweet ending (mixed emotions)"
                ]
            },
            
            "setting_world": {
                "title": "SETTING & WORLD",
                "options": [
                    "Contemporary real world",
                    "Historical period (specify era)",
                    "Future/science fiction world",
                    "Fantasy world with magic",
                    "Small town/rural setting",
                    "Urban/city setting",
                    "Suburban setting",
                    "Workplace setting (office, restaurant, etc.)",
                    "School/university setting",
                    "Home/domestic setting",
                    "Travel/journey setting",
                    "Specific location (beach, mountains, etc.)",
                    "Multiple locations throughout story"
                ]
            },
            
            "themes": {
                "title": "THEMES & MESSAGES",
                "options": [
                    "Love and relationships",
                    "Family bonds and conflicts",
                    "Friendship and loyalty",
                    "Personal growth and change",
                    "Forgiveness and redemption",
                    "Courage and overcoming fear",
                    "Identity and self-discovery",
                    "Loss and grief",
                    "Hope and resilience",
                    "Justice and morality",
                    "Dreams and aspirations",
                    "Acceptance and belonging",
                    "Second chances",
                    "The power of choice"
                ]
            },
            
            "tone_mood": {
                "title": "OVERALL TONE & MOOD",
                "options": [
                    "Heartwarming and uplifting",
                    "Romantic and passionate",
                    "Melancholic and reflective",
                    "Humorous and light",
                    "Dramatic and intense",
                    "Mysterious and suspenseful",
                    "Dark and serious",
                    "Nostalgic and wistful",
                    "Hopeful and optimistic",
                    "Realistic and gritty",
                    "Dreamy and atmospheric",
                    "Energetic and dynamic"
                ]
            },
            
            "pacing_style": {
                "title": "PACING & STYLE",
                "options": [
                    "Fast-paced with quick developments",
                    "Slow and contemplative",
                    "Building tension throughout",
                    "Alternating between action and reflection",
                    "Dialogue-heavy storytelling",
                    "Action-oriented narrative",
                    "Descriptive and atmospheric",
                    "Character introspection focused",
                    "Plot-driven progression",
                    "Emotional beats emphasis",
                    "Realistic everyday pacing",
                    "Dramatic peaks and valleys"
                ]
            },
            
            "story_catalyst": {
                "title": "STORY CATALYST (WHAT STARTS IT)",
                "options": [
                    "Life-changing news or discovery",
                    "Meeting someone new/important",
                    "Loss or ending of something significant",
                    "Unexpected opportunity",
                    "Crisis or emergency situation",
                    "Return to a place from the past",
                    "Deadline or time pressure",
                    "Secret being revealed",
                    "Accident or chance encounter",
                    "Decision that must be made",
                    "Celebration or milestone event",
                    "Conflict or confrontation"
                ]
            },
            
            "emotional_journey": {
                "title": "EMOTIONAL JOURNEY",
                "options": [
                    "From sadness to happiness",
                    "From fear to courage",
                    "From loneliness to connection",
                    "From anger to forgiveness",
                    "From confusion to clarity",
                    "From despair to hope",
                    "From closed-off to vulnerable",
                    "From selfish to selfless",
                    "From naive to wise",
                    "From broken to healed",
                    "From lost to found",
                    "Emotional rollercoaster (mixed journey)"
                ]
            },
            
            "point_of_view": {
                "title": "NARRATIVE PERSPECTIVE",
                "options": [
                    "First person (I) - protagonist",
                    "First person (I) - supporting character",
                    "Second person (you) for intimacy",
                    "Consistent I/you perspective - protagonist as 'I', other lead as 'you'",
                    "Mixed perspective (I and you) - intimate dialogue between two characters",
                    "Third person limited - protagonist",
                    "Third person limited - supporting character",
                    "Third person limited - multiple characters",
                    "Third person omniscient",
                    "Present tense for immediacy",
                    "Past tense for storytelling feel",
                    "Stream of consciousness style",
                    "Internal monologue heavy",
                    "Dialogue-focused minimal narration",
                    "Epistolary (letters/diary format)",
                    "Multiple POV chapters",
                    "Single POV throughout"
                ]
            },
            
            "content_boundaries": {
                "title": "CONTENT BOUNDARIES",
                "options": [
                    "Family-friendly/all ages appropriate",
                    "Young adult appropriate (teen themes)",
                    "Mature themes but no explicit content",
                    "Romance with sensual elements allowed",
                    "Adult content/intimate scenes allowed",
                    "Violence/conflict acceptable",
                    "Strong language acceptable", 
                    "Dark themes (trauma, loss) acceptable",
                    "LGBTQ+ themes and characters",
                    "Mental health topics acceptable",
                    "Social issues and politics okay",
                    "Keep content light and positive"
                ]
            },
            
            "story_focus": {
                "title": "PRIMARY STORY FOCUS",
                "options": [
                    "Character development and growth",
                    "Relationship dynamics (romantic/platonic)",
                    "Family relationships and bonds",
                    "Career and professional life",
                    "Personal dreams and aspirations",
                    "Overcoming personal challenges",
                    "Social issues and community",
                    "Adventure and discovery",
                    "Mystery and problem-solving",
                    "Moral and ethical questions",
                    "Life transitions and changes",
                    "Healing and recovery"
                ]
            }
        }
        
        # Show all categories with their current status (auto by default)
        selected_elements = {}
        for category in story_elements.keys():
            selected_elements[category] = "auto"
        
        while True:
            self._display_current_selections(story_elements, selected_elements)
            
            print("\nActions:")
            print("1-15: Configure category (enter category number)")
            print("G: Generate story user prompt with current settings")
            print("R: Reset all to auto")
            print("Q: Quit without saving")
            
            choice = input("\nChoice: ").strip().upper()
            
            if choice == 'G':
                self._generate_story_user_prompt(selected_elements)
                break
            elif choice == 'R':
                for category in selected_elements.keys():
                    selected_elements[category] = "auto"
                print("All categories reset to auto")
                input("Press Enter to continue...")
            elif choice == 'Q':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(story_elements):
                category_index = int(choice) - 1
                category_key = list(story_elements.keys())[category_index]
                selected_elements[category_key] = self._configure_category(story_elements[category_key])
            else:
                print("Invalid choice")
                input("Press Enter to continue...")
    
    def _display_current_selections(self, story_elements, selected_elements):
        """Display current selection status for all categories"""
        print("\n" + "="*70)
        print("STORY USER PROMPT CONFIGURATION")
        print("="*70)
        
        category_keys = list(story_elements.keys())
        for i, category_key in enumerate(category_keys, 1):
            title = story_elements[category_key]["title"]
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
    
        custom_option_num = len(category_data['options']) + 1
        print(f"{custom_option_num:2d}. CUSTOM - Write your own description")
    
        # Add examples option for certain categories
        examples_option_num = custom_option_num + 1
        show_examples = category_data['title'] in ['STORY LENGTH & SCOPE', 'NARRATIVE PERSPECTIVE', 'CENTRAL CONFLICT']
    
        if show_examples:
            print(f"{examples_option_num:2d}. EXAMPLES - See custom examples for this category")
    
        print()
    
        user_input = input(f"Your choices (e.g., 1,3,5), custom text, or Enter for auto: ").strip()
    
        if not user_input:
            return "auto"
    
        # Check for examples option
        if show_examples and user_input == str(examples_option_num):
            self._show_custom_examples(category_data['title'])
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

    def _show_custom_examples(self, category_title):
        """Show custom examples for specific categories"""
        print("\n" + "="*80)
        print(f"CUSTOM EXAMPLES FOR {category_title}")
        print("="*80)
    
        if category_title == "STORY LENGTH & SCOPE":
            examples = [
                ("Word Count Focused", "4000-6000 words with rich character development and detailed scenes"),
                ("Quality Over Quantity", "Around 2500 words, focusing on quality over quantity with deep emotional moments"),
                ("Epic Scope", "Minimum 8000 words - epic scope with multiple plot threads"),
                ("Three-Act Structure", "Three distinct acts with clear transitions, approximately 3500 words total"),
                ("Interconnected Scenes", "Five interconnected scenes building to climax, 4000+ words"),
                ("Slow-Burn", "Slow-burn development over 6000+ words with gradual revelation"),
                ("Single Location/Multiple Times", "Single location but multiple time periods, showing change over time - 3000+ words"),
                ("Journey Story", "Journey story with 4-5 different locations, substantial development at each - 5000+ words"),
                ("Real-Time", "Real-time story unfolding over exactly one hour, highly detailed - 2500+ words"),
                ("Intimate Epic", "Intimate two-character focus but epic emotional scope, 4500+ words minimum")
            ]
    
        elif category_title == "NARRATIVE PERSPECTIVE":
            examples = [
                ("Alternating First Person", "Alternating chapters between 'I' perspectives of two main characters"),
                ("Direct Address", "Protagonist speaks directly to reader as confidant throughout"),
                ("Memory Narrative", "Older character remembering and telling story to younger generation"),
                ("Diary/Journal Style", "Written as private journal entries revealing inner thoughts"),
                ("Interview Format", "Story told through character being interviewed about past events"),
                ("Letters Between Characters", "Story unfolds through exchange of letters or emails"),
                ("Unreliable Narrator", "First person narrator who may not be telling complete truth"),
                ("Collective Voice", "Community or group telling story from shared perspective"),
                ("Future Looking Back", "Character in future reflecting on pivotal past events"),
                ("Stream of Consciousness", "Raw, unfiltered thoughts flowing naturally without structure")
            ]
    
        elif category_title == "CENTRAL CONFLICT":
            examples = [
                ("Moral Compromise", "Character must choose between personal gain and doing what's right"),
                ("Loyalty vs Truth", "Protecting someone they love means hiding important truth from others"),
                ("Past vs Future", "Old dreams conflicting with new responsibilities and realities"),
                ("Identity Crisis", "Character discovering their whole life/identity was built on lies"),
                ("Competing Loves", "Heart torn between two people who represent different life paths"),
                ("Professional vs Personal", "Career success requires sacrificing family relationships"),
                ("Forgiveness Challenge", "Must forgive someone who caused deep, lasting hurt"),
                ("Secret Burden", "Carrying knowledge that could destroy others if revealed"),
                ("Time Pressure Decision", "Limited time to make choice that will define their future"),
                ("Generational Conflict", "Breaking family traditions while honoring family bonds")
            ]
    
        else:
            examples = [("Example 1", "Custom example for this category")]
    
        print("Copy any of these examples or use them as inspiration:")
        print()
    
        for i, (title, example) in enumerate(examples, 1):
            print(f"{i:2d}. {title}:")
            print(f"    \"{example}\"")
            print()
    
        input("Press Enter to return to category selection...")
    
    def _generate_story_user_prompt(self, selected_elements):
        """Generate the final user prompt based on selections"""
        print(f"\n{'='*80}")
        print("GENERATING COMPREHENSIVE STORY USER PROMPT")
        print(f"{'='*80}")
        
        # Build the AI instruction for creating the user prompt
        ai_system_prompt = """You are an expert creative writing prompt creator. Create a comprehensive story user prompt based on the user's specifications. 

For elements marked as "auto", you should include instructions for the AI to decide those aspects appropriately. 

The user prompt should:
- Be detailed and specific where the user made selections
- Include "AI should decide" language for auto elements
- Flow naturally as a single coherent prompt
- Be around 200-300 words (stories need detailed prompts)
- Focus on WHAT should happen in the story, not HOW to write it
- Emphasize that this should be a complete story with beginning, middle, and end
- Remind the AI to aim for 700+ words for a full story
- Give the AI creative freedom while meeting the specified requirements"""
        
        # Build the specification text
        specs = []
        for category, selections in selected_elements.items():
            category_name = category.replace('_', ' ').title()
            if selections == "auto":
                specs.append(f"{category_name}: AI should decide")
            else:
                specs.append(f"{category_name}: {', '.join(selections)}")
        
        specifications = "\n".join(specs)
        
        ai_user_prompt = f"""Create a comprehensive story user prompt with these specifications:

{specifications}

The prompt should tell the AI to write a complete story (not just a scene) with proper beginning, middle, and end. For "auto" elements, include phrases like "AI should determine appropriate..." or "choose suitable..." 

The prompt should emphasize writing a full story of at least 700 words.

Return only the user prompt, nothing else."""
        
        # Check if model is available
        if not self.template_manager.model_tester.test_config.get('model'):
            print("No model selected. Please configure a model first.")
            input("Press Enter to continue...")
            return
        
        print("Generating your comprehensive story user prompt...")
        
        result = self.template_manager.model_tester.stream_ollama_request(
            ai_system_prompt,
            ai_user_prompt,
            self.template_manager.model_tester.test_config,
            callback=None
        )
        
        if result['success']:
            generated_prompt = result['response'].strip()
            
            print(f"\nYOUR COMPREHENSIVE STORY USER PROMPT:")
            print("="*70)
            print(generated_prompt)
            print("="*70)
            print(f"Word count: {len(generated_prompt.split())} words")
            
            # Show what was specified vs auto
            print(f"\nSPECIFICATIONS SUMMARY:")
            for category, selections in selected_elements.items():
                category_name = category.replace('_', ' ').title()
                if selections == "auto":
                    print(f"• {category_name}: AI will decide")
                else:
                    print(f"• {category_name}: {len(selections)} specific choice(s)")
            
            save = input(f"\nSave this story user prompt? (y/n): ").strip().lower()
            if save == 'y':
                # Get a name for the prompt
                prompt_name = input("Enter a name for this prompt (or press Enter for auto-name): ").strip()
                if not prompt_name:
                    specified_count = sum(1 for sel in selected_elements.values() if sel != "auto")
                    prompt_name = f"comprehensive_story_{specified_count}_specified"
                
                # Clean the name for filename
                safe_name = prompt_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
                
                if self.template_manager.save_user_prompt_template(safe_name, generated_prompt):
                    print(f"Story user prompt saved successfully!")
                else:
                    print("Failed to save prompt.")
            else:
                print("Story user prompt not saved.")
        else:
            print(f"Failed to generate prompt: {result.get('error', 'Unknown error')}")
        
        input("\nPress Enter to continue...")
