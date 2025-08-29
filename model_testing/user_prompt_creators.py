from .templates.scene_user_prompt_builder import SceneUserPromptBuilder

class UserPromptCreators:
    def __init__(self, template_manager):
        self.template_manager = template_manager
        # Initialize the comprehensive builder
        self.scene_builder = SceneUserPromptBuilder(template_manager)
    
    def create_scenario_prompt(self):
        """Create scenario-based scene prompts that work with any genre"""
        content_label = self.template_manager.content_type.capitalize()
        
        print(f"\n{'='*70}")
        print(f"SCENARIO-BASED {content_label.upper()} USER PROMPT")
        print(f"{'='*70}")
        print("Create user prompts based on universal story scenarios.")
        print("These work with ANY system prompt (romance, detective, horror, etc.)")
        print()
        
        # Universal scenarios that work across all genres
        scenarios = [
            "Two strangers are trapped together during a storm and must rely on each other",
            "A character discovers something hidden that changes everything they believed",
            "Someone returns after a long absence to find everything has changed", 
            "A secret that someone has kept for years is about to be revealed",
            "Two characters with opposing goals are forced to work together",
            "A character faces an impossible choice between two things they value",
            "Someone finds a mysterious object that doesn't belong to them",
            "A misunderstanding leads to escalating conflict between characters",
            "A character must confront someone they've been avoiding",
            "Two people who never talk are stuck alone together for hours",
            "A character receives unexpected news that changes their plans",
            "Someone must choose between telling the truth or protecting feelings",
            "A character's biggest fear becomes reality in an unexpected way",
            "Two characters swap roles or positions for a day",
            "A character must defend a decision they're not sure about"
        ]
        
        print(f"📋 UNIVERSAL SCENARIOS ({len(scenarios)} available):")
        print("-" * 70)
        for i, scenario in enumerate(scenarios, 1):
            print(f"{i:2d}. {scenario}")
        
        try:
            choice = int(input(f"\nSelect scenario (1-{len(scenarios)}): "))
            if not (1 <= choice <= len(scenarios)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
                
            selected_scenario = scenarios[choice - 1]
            
            # Show customization options
            print(f"\n🎯 SELECTED SCENARIO:")
            print(f'"{selected_scenario}"')
            print()
            print("📝 CUSTOMIZATION OPTIONS:")
            print("1. Use scenario as-is")
            print("2. Add specific character details")
            print("3. Add location/setting details") 
            print("4. Add emotional stakes")
            print("5. Fully customize the prompt")
            
            custom_choice = int(input("Select customization (1-5): "))
            
            final_prompt = selected_scenario
            
            if custom_choice == 2:
                char_detail = input("Add character detail (e.g., 'who used to be partners'): ").strip()
                if char_detail:
                    final_prompt = selected_scenario.replace("Two characters", f"Two characters {char_detail}")
                    final_prompt = final_prompt.replace("A character", f"A character {char_detail}")
                    
            elif custom_choice == 3:
                location = input("Specify location/setting: ").strip()
                if location:
                    final_prompt += f" The scene takes place in {location}."
                    
            elif custom_choice == 4:
                stakes = input("Add what's at stake: ").strip()
                if stakes:
                    final_prompt += f" The outcome will determine {stakes}."
                    
            elif custom_choice == 5:
                print("Current prompt:")
                print(f'"{final_prompt}"')
                custom_prompt = input("\nEnter your customized version: ").strip()
                if custom_prompt:
                    final_prompt = custom_prompt
            
            # Show preview and save
            print(f"\n📋 FINAL PROMPT PREVIEW:")
            print("=" * 70)
            print(f'"{final_prompt}"')
            print("=" * 70)
            
            save_choice = input("\nSave this user prompt template? (y/n): ").strip().lower()
            if save_choice == 'y':
                name = input("Template name (e.g., 'trapped_strangers', 'secret_revealed'): ").strip()
                if name:
                    if self.template_manager.save_user_prompt_template(name, final_prompt):
                        print(f"\n✅ Scenario user prompt saved!")
                        print(f"📁 Filename: user_prompt_{self.template_manager.content_type}_{name}.txt")
                        print(f"🎯 Works with: Any system prompt (romance, horror, detective, etc.)")
                else:
                    print("No name provided. Template not saved.")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
        
    def create_character_focused_prompt(self):
        """Create character-focused prompts that work with any genre"""
        content_label = self.template_manager.content_type.capitalize()
        
        print(f"\n{'='*70}")
        print(f"CHARACTER-FOCUSED {content_label.upper()} USER PROMPT")
        print(f"{'='*70}")
        print("Create prompts focused on character development and relationships.")
        print("These work with ANY genre - the system prompt determines the style.")
        print()
        
        character_prompts = [
            "Write a scene where the main character reveals a hidden talent or skill",
            "Show the protagonist at their most vulnerable moment",
            "Two characters who usually agree have their first serious argument",
            "A character must choose between personal loyalty and doing what's right",
            "Show a character's true personality when they think no one is watching",
            "A character confronts someone who has disappointed them",
            "Write a scene where a character's past catches up with them",
            "Two characters bond over a shared experience or memory",
            "A character stands up for their beliefs despite pressure to conform",
            "Show a character learning something important about themselves",
            "A character must apologize for something they've done wrong",
            "Two characters with different backgrounds find common ground",
            "A character faces their biggest insecurity or self-doubt",
            "Show a character making a difficult sacrifice for someone else",
            "A character's carefully constructed facade begins to crack"
        ]
        
        print(f"👥 CHARACTER-FOCUSED PROMPTS ({len(character_prompts)} available):")
        print("-" * 70)
        for i, prompt in enumerate(character_prompts, 1):
            print(f"{i:2d}. {prompt}")
        
        try:
            choice = int(input(f"\nSelect character prompt (1-{len(character_prompts)}): "))
            if not (1 <= choice <= len(character_prompts)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
                
            selected_prompt = character_prompts[choice - 1]
            
            # Optional customization
            print(f"\n🎯 SELECTED PROMPT:")
            print(f'"{selected_prompt}"')
            print()
            
            customize = input("Add character details? (y/n): ").strip().lower()
            final_prompt = selected_prompt
            
            if customize == 'y':
                char_name = input("Character name (optional): ").strip()
                char_trait = input("Key character trait (e.g., 'shy detective', 'stubborn artist'): ").strip()
                relationship = input("Relationship context (e.g., 'to their partner', 'with their rival'): ").strip()
                
                if char_name:
                    final_prompt = final_prompt.replace("the main character", char_name)
                    final_prompt = final_prompt.replace("the protagonist", char_name)
                    final_prompt = final_prompt.replace("A character", char_name)
                    
                if char_trait:
                    final_prompt += f" The character is {char_trait}."
                    
                if relationship:
                    final_prompt = final_prompt.replace("someone", relationship)
            
            # Show preview and save
            print(f"\n📋 FINAL PROMPT PREVIEW:")
            print("=" * 70)
            print(f'"{final_prompt}"')
            print("=" * 70)
            
            save_choice = input("\nSave this user prompt template? (y/n): ").strip().lower()
            if save_choice == 'y':
                name = input("Template name (e.g., 'character_vulnerable', 'hidden_talent'): ").strip()
                if name:
                    if self.template_manager.save_user_prompt_template(name, final_prompt):
                        print(f"\n✅ Character-focused user prompt saved!")
                        print(f"📁 Filename: user_prompt_{self.template_manager.content_type}_{name}.txt")
                        print(f"🎯 Works with: Any system prompt - genre determined by system prompt")
                else:
                    print("No name provided. Template not saved.")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def create_genre_user_prompt(self):
        """Create genre-flexible user prompts with style hints"""
        content_label = self.template_manager.content_type.capitalize()
        
        print(f"\n{'='*70}")
        print(f"GENRE-FLEXIBLE {content_label.upper()} USER PROMPT")
        print(f"{'='*70}")
        print("Create prompts that can adapt to different genres.")
        print("These provide genre hints but work with any system prompt.")
        print()
        
        flexible_prompts = [
            {
                "base": "Two characters meet for the first time in an unexpected place",
                "romance": "Focus on instant attraction and nervous chemistry",
                "detective": "One character seems suspicious or out of place", 
                "horror": "The location has an ominous or unsettling atmosphere",
                "fantasy": "Magic or supernatural elements are subtly present"
            },
            {
                "base": "A character discovers something hidden in an old building",
                "romance": "It's a love letter or romantic memento from the past",
                "detective": "It's evidence related to an unsolved mystery",
                "horror": "It's something that should have stayed buried",
                "fantasy": "It's a magical artifact or ancient relic"
            },
            {
                "base": "Two characters are forced to work together despite their differences",
                "romance": "Their bickering masks underlying attraction",
                "detective": "They must solve a case that affects them both",
                "horror": "They must survive a terrifying threat together", 
                "fantasy": "They must complete a magical quest or ritual"
            },
            {
                "base": "A character returns to their hometown after many years away",
                "romance": "They encounter their first love who never left",
                "detective": "They're investigating something from their past",
                "horror": "The town harbors dark secrets they tried to escape",
                "fantasy": "The town has been changed by magical forces"
            }
        ]
        
        print(f"🎭 GENRE-FLEXIBLE PROMPTS ({len(flexible_prompts)} available):")
        print("-" * 70)
        for i, prompt_data in enumerate(flexible_prompts, 1):
            print(f"{i:2d}. {prompt_data['base']}")
        
        try:
            choice = int(input(f"\nSelect base prompt (1-{len(flexible_prompts)}): "))
            if not (1 <= choice <= len(flexible_prompts)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
                
            selected_data = flexible_prompts[choice - 1]
            base_prompt = selected_data['base']
            
            print(f"\n🎯 SELECTED BASE PROMPT:")
            print(f'"{base_prompt}"')
            print()
            print("📝 GENRE ADAPTATION OPTIONS:")
            print("1. Keep it universal (works with any system prompt)")
            print("2. Add romance hints")
            print("3. Add detective/mystery hints") 
            print("4. Add horror/suspense hints")
            print("5. Add fantasy/magical hints")
            print("6. Create custom adaptation")
            
            adapt_choice = int(input("Select adaptation (1-6): "))
            
            final_prompt = base_prompt
            
            if adapt_choice == 2:
                final_prompt += f" {selected_data['romance']}"
            elif adapt_choice == 3:
                final_prompt += f" {selected_data['detective']}"
            elif adapt_choice == 4:
                final_prompt += f" {selected_data['horror']}"
            elif adapt_choice == 5:
                final_prompt += f" {selected_data['fantasy']}"
            elif adapt_choice == 6:
                custom_hint = input("Add your custom genre hint: ").strip()
                if custom_hint:
                    final_prompt += f" {custom_hint}"
            
            # Show preview and save
            print(f"\n📋 FINAL PROMPT PREVIEW:")
            print("=" * 70)
            print(f'"{final_prompt}"')
            print("=" * 70)
            
            save_choice = input("\nSave this user prompt template? (y/n): ").strip().lower()
            if save_choice == 'y':
                name = input("Template name (e.g., 'meet_unexpected', 'return_hometown'): ").strip()
                if name:
                    if self.template_manager.save_user_prompt_template(name, final_prompt):
                        print(f"\n✅ Genre-flexible user prompt saved!")
                        print(f"📁 Filename: user_prompt_{self.template_manager.content_type}_{name}.txt")
                        print(f"🎯 Flexibility: Works with any system prompt, genre hints included")
                else:
                    print("No name provided. Template not saved.")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
        
    def create_custom_user_prompt(self):
        """Create custom user prompt and save as template"""
        content_label = self.template_manager.content_type.capitalize() if self.template_manager.content_type else "User"
        
        print(f"\n{'='*60}")
        print(f"CREATE CUSTOM {content_label.upper()} USER PROMPT")
        print(f"{'='*60}")
        print("Enter your user prompt content (press Enter on empty line to finish):")
        print("This describes the scene/story you want the AI to write.")
        print()
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        if not lines:
            print("No content entered.")
            input("Press Enter to continue...")
            return
        
        content = '\n'.join(lines)
        
        # Get template name
        print(f"\nPreview ({len(content.split())} words):")
        print("-" * 40)
        print(content[:200] + "..." if len(content) > 200 else content)
        print("-" * 40)
        
        name = input("\nEnter template name (e.g., 'romance_cafe', 'detective_crime_scene'): ").strip()
        if not name:
            print("No name provided. Template not saved.")
            input("Press Enter to continue...")
            return
        
        # Save template
        if self.template_manager.save_user_prompt_template(name, content):
            print(f"Template can now be used in Scene Workshop!")
    
    def create_ai_generated_user_prompt(self):
        """Create comprehensive AI-generated user prompt with multi-select options"""
        if self.template_manager.content_type == 'scene':
            # Use the comprehensive scene builder
            self.scene_builder.create_comprehensive_scene_user_prompt()
        elif self.template_manager.content_type == 'story':
            # For now, use a simple version for stories - we can expand this later
            print(f"AI-generated {self.template_manager.content_type} user prompt")
            print("(Comprehensive story user prompt builder coming soon)")
            input("Press Enter to continue...")
        else:
            print("Please select content type first!")
            input("Press Enter to continue...")
