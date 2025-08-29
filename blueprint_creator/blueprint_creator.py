"""
Blueprint Creator - Main class for creating story blueprints
"""

import os
import json
import requests
from datetime import datetime
from .menu_handlers import MenuHandlers
from .config import *

class BlueprintCreator:
    def __init__(self, blueprint_folder):
        self.blueprint_folder = blueprint_folder
        self.menu_handlers = MenuHandlers(self)
        self.available_models = []
        
        # Ensure blueprint folder exists
        os.makedirs(blueprint_folder, exist_ok=True)
    
    def create_blueprint(self):
        """Main blueprint creation workflow"""
        print("\n" + "="*60)
        print("BLUEPRINT CREATOR")
        print("="*60)
        print("Create a new story blueprint that defines the structure,")
        print("characters, and narrative elements for story generation.")
        print("="*60)
        
        # Initialize blueprint data with defaults
        blueprint_data = {
            'name': 'untitled_blueprint',
            'genre': 'Not chosen',
            'subgenre': 'Not chosen',
            'storytelling_style': 'Not chosen',
            'target_audience': 'Not chosen',  # NEW
            'perspective': 'Not chosen',
            'narrative_style': 'Not chosen',  # ADD THIS LINE
            'setting_type': 'Not chosen',
            'tone': 'Not chosen',
            'complexity': 'Not chosen',
            'language_settings': ('moderate', 'moderate', 'casual'),  # NEW
            'special_elements': [],
            'custom_instructions': 'Not chosen',
            'llm_model': 'mistral:latest',
            'max_tokens': 8192,
            'target_length': 'Long (15-20 scenes)',
            'protagonist_gender': 'Not chosen',
            'counterpart_type': 'Not chosen',
            'counterpart_gender': 'Not chosen'
        }
        
        # Main creation loop
        while True:
            self.display_blueprint_menu(blueprint_data)
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    self.menu_handlers.set_blueprint_name(blueprint_data)
                elif choice == "2":
                    self.menu_handlers.set_genre(blueprint_data)
                elif choice == "3":
                    self.menu_handlers.set_subgenre(blueprint_data)
                elif choice == "4":
                    self.menu_handlers.set_target_audience(blueprint_data)  # NEW
                elif choice == "5":
                    self.menu_handlers.set_storytelling_style(blueprint_data)
                elif choice == "6":
                    self.menu_handlers.set_perspective(blueprint_data)
                elif choice == "7":
                    self.menu_handlers.set_narrative_style(blueprint_data)  # ADD THIS LINE
                elif choice == "8":
                    self.menu_handlers.set_language_style(blueprint_data)  # NEW
                elif choice == "9":
                    self.menu_handlers.set_setting_type(blueprint_data)
                elif choice == "10":
                    self.menu_handlers.set_tone(blueprint_data)
                elif choice == "11":
                    self.menu_handlers.set_complexity(blueprint_data)
                elif choice == "12":
                    self.menu_handlers.set_special_elements(blueprint_data)
                elif choice == "13":
                    self.menu_handlers.set_custom_instructions(blueprint_data)
                elif choice == "14":
                    self.menu_handlers.set_llm_model(blueprint_data)
                elif choice == "15":
                    self.menu_handlers.set_max_tokens(blueprint_data)
                elif choice == "16":
                    self.menu_handlers.set_target_length(blueprint_data)
                elif choice == "17":
                    self.menu_handlers.set_protagonist_gender(blueprint_data)
                elif choice == "18":
                    self.menu_handlers.set_counterpart_character(blueprint_data)
                elif choice == "19":
                    self.menu_handlers.set_counterpart_gender(blueprint_data)
                elif choice == "20":
                    # Generate Blueprint
                    if self.validate_blueprint_data(blueprint_data):
                        generated_file = self.generate_blueprint(blueprint_data)
                        if generated_file:
                            return generated_file
                    else:
                        input("Press Enter to continue...")
                elif choice == "21":
                    # Cancel
                    confirm = input("Exit without saving? (y/n): ").strip().lower()
                    if confirm == 'y':
                        print("❌ Blueprint creation cancelled")
                        return None
                else:
                    print("❌ Invalid option. Please select 1-21.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n❌ Blueprint creation cancelled")
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")
    
    def display_blueprint_menu(self, blueprint_data):
        """Display the blueprint creation menu"""
        print("\n" + "="*60)
        print("BLUEPRINT CREATION")
        print("="*60)
        print(f"1. Blueprint name: {blueprint_data['name']}")
        print(f"2. Genre: {blueprint_data['genre']}")
        print(f"3. Subgenre: {blueprint_data['subgenre']}")
        print(f"4. Target Audience: {blueprint_data.get('target_audience', 'Not chosen')}")
        print(f"5. Storytelling style: {blueprint_data['storytelling_style']}")
        print(f"6. Perspective: {blueprint_data['perspective']}")
        print(f"7. Narrative Style: {blueprint_data.get('narrative_style', 'Not chosen')}")
        print(f"8. Language Style: {self._format_language_display(blueprint_data)}")
        print(f"9. Setting type: {blueprint_data['setting_type']}")
        print(f"10. Tone: {blueprint_data['tone']}")
        print(f"11. Complexity: {blueprint_data['complexity']}")
        print(f"12. Special elements: {', '.join(blueprint_data['special_elements']) if blueprint_data['special_elements'] else 'Not chosen'}")
        print(f"13. Custom instructions: {blueprint_data['custom_instructions']}")
        print(f"14. LLM Model: {blueprint_data['llm_model']}")
        print(f"15. Max tokens (blueprint length): {blueprint_data['max_tokens']:,}")
        print(f"16. Target story length: {blueprint_data['target_length']}")
        print(f"17. Protagonist gender: {blueprint_data['protagonist_gender']}")
        
        # Fix the counterpart character display
        counterpart_type = blueprint_data['counterpart_type']
        counterpart_gender = blueprint_data.get('counterpart_gender', 'Not chosen')
        
        if counterpart_type != 'Not chosen' and counterpart_gender != 'Not chosen':
            print(f"18. Counterpart character: {counterpart_type} ({counterpart_gender})")
        else:
            print(f"18. Counterpart character: {counterpart_type}")
        
        print(f"19. Counterpart gender: {counterpart_gender}")
        print("20. Generate Blueprint with Ollama")
        print("21. Cancel")

        # Show completion status
        completion = self.calculate_completion_percentage(blueprint_data)
        print(f"\n📊 Configuration Complete: {completion}%")
    
        if completion < 50:
            print("💡 TIP: Configure at least Genre, Perspective, and Tone before generating")
        elif completion < 75:
            print("💡 TIP: Add more details for a richer blueprint")
        else:
            print("✅ Ready to generate! Your blueprint will be comprehensive")
    
        print("\n" + "="*60)
        print("Select option (1-21): ", end="")
    
    def calculate_completion_percentage(self, blueprint_data):
        """Calculate how complete the blueprint configuration is"""
        total_fields = 13  # Updated to include counterpart gender
        completed_fields = 0
        
        if blueprint_data['name'] != 'untitled_blueprint':
            completed_fields += 1
        if blueprint_data['genre'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['subgenre'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['storytelling_style'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['target_audience'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['perspective'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['narrative_style'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['setting_type'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['tone'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['complexity'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['protagonist_gender'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data['counterpart_type'] != 'Not chosen':
            completed_fields += 1
        if blueprint_data.get('counterpart_gender', 'Not chosen') != 'Not chosen':
            completed_fields += 1
        if blueprint_data['target_length'] != 'Not chosen':
            completed_fields += 1
        
        return int((completed_fields / total_fields) * 100)
    
    def validate_blueprint_data(self, blueprint_data):
        """Validate that essential blueprint data is provided"""
        required_fields = ['genre', 'perspective', 'tone']
        missing_fields = []
        
        for field in required_fields:
            if blueprint_data.get(field, 'Not chosen') == 'Not chosen':
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            print(f"\n❌ Missing required fields: {', '.join(missing_fields)}")
            print("Please configure these essential elements before generating.")
            return False
        
        return True
    
    def generate_blueprint(self, blueprint_data):
        """Generate a full blueprint using AI"""
        print("\n🚀 GENERATING BLUEPRINT...")
        print("="*50)
        
        # Create the prompt for blueprint generation
        prompt = self.generate_blueprint_prompt(blueprint_data)
        
        print("📝 Sending request to Ollama...")
        print(f"Model: {blueprint_data['llm_model']}")
        print(f"Max Tokens: {blueprint_data['max_tokens']:,}")
        
        try:
            # Send request to Ollama
            response = self.call_ollama_api(
                blueprint_data['llm_model'], 
                prompt, 
                blueprint_data['max_tokens']
            )
            
            if response:
                # Show the generated blueprint and get user decision
                decision = self._show_blueprint_preview(response, blueprint_data)
                
                if decision == 'save':
                    # Generate filename with genre and date
                    filename = self._generate_blueprint_filename(blueprint_data)
                    filepath = os.path.join(self.blueprint_folder, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(response)
                    
                    print(f"✅ Blueprint saved successfully!")
                    print(f"📁 Saved as: {filename}")
                    print(f"📏 Length: {len(response):,} characters")
                    
                    input("\nPress Enter to continue...")
                    return filename
                elif decision == 'regenerate':
                    # Recursively call generate_blueprint to try again
                    print("\n🔄 Regenerating blueprint...")
                    return self.generate_blueprint(blueprint_data)
                else:  # cancel
                    print("❌ Blueprint generation cancelled")
                    return None
            else:
                print("❌ Failed to generate blueprint")
                return None
                
        except Exception as e:
            print(f"❌ Error generating blueprint: {e}")
            return None

    def generate_blueprint_prompt(self, blueprint_data):
        """Generate the prompt for blueprint creation"""
        prompt = "You are a master storyteller and blueprint creator. You will create a comprehensive story blueprint that guides future story generation.\n\n"
        
        # CRITICAL PERSPECTIVE ENFORCEMENT
        perspective = blueprint_data.get('perspective', 'Not chosen')
        narrative_style = blueprint_data.get('narrative_style', 'Not chosen')
        
        if perspective != 'Not chosen':
            prompt += "🚨 CRITICAL NARRATIVE REQUIREMENTS:\n"
            prompt += f"PERSPECTIVE: {perspective}\n"
            
            if perspective == "First person singular":
                prompt += "MANDATORY: All future stories using this blueprint MUST be written entirely in FIRST PERSON using 'I' statements.\n"
                prompt += "- Every sentence must be from the protagonist's viewpoint using 'I', 'me', 'my', 'myself'\n"
                prompt += "- NO third person descriptions like 'Sarah walked' - it must be 'I walked'\n"
                prompt += "- NO omniscient narration - only what the protagonist sees, thinks, and feels\n"
                prompt += "- Example: 'I felt my heart racing as I saw her smile' NOT 'Sarah felt her heart racing'\n"
            elif perspective == "First person plural":
                prompt += "MANDATORY: All future stories using this blueprint MUST be written in FIRST PERSON PLURAL using 'We' statements.\n"
                prompt += "- Every sentence from the group's collective viewpoint using 'we', 'us', 'our'\n"
                prompt += "- Example: 'We decided to enter the building' NOT 'They decided to enter'\n"
            elif perspective == "Second person":
                prompt += "MANDATORY: All future stories using this blueprint MUST be written in SECOND PERSON using 'You' statements.\n"
                prompt += "- Every sentence directed at the reader using 'you', 'your', 'yourself'\n"
                prompt += "- Example: 'You feel your heart racing' NOT 'I felt my heart racing'\n"
            elif perspective == "Third person limited":
                prompt += "MANDATORY: All future stories using this blueprint MUST be written in THIRD PERSON LIMITED.\n"
                prompt += "- Follow ONE character's perspective closely using their name or 'she/he/they'\n"
                prompt += "- Access to only that character's thoughts and feelings\n"
                prompt += "- Example: 'Sarah felt her heart racing' with access to Sarah's inner thoughts only\n"
            elif perspective == "Third person omniscient":
                prompt += "MANDATORY: All future stories using this blueprint MUST be written in THIRD PERSON OMNISCIENT.\n"
                prompt += "- Access to multiple characters' thoughts and feelings\n"
                prompt += "- Can reveal information unknown to individual characters\n"
            
            prompt += f"\nThis perspective choice is ABSOLUTE and must be maintained throughout the entire story.\n"
            prompt += "Include specific perspective instructions in the blueprint to ensure story generators follow this exactly.\n\n"
        
        # NARRATIVE STYLE ENFORCEMENT
        if narrative_style != 'Not chosen':
            prompt += f"NARRATIVE WRITING STYLE: {narrative_style}\n"
            
            if "Romantic Intimate" in narrative_style:
                if perspective == "First person singular":
                    prompt += "STYLE REQUIREMENTS: Deep internal monologue focusing on emotions, thoughts, and romantic feelings.\n"
                    prompt += "- Heavy use of internal thoughts: 'I wondered if she felt the same way I did'\n"
                    prompt += "- Emotional introspection: 'My heart skipped when she smiled at me'\n"
                    prompt += "- Intimate observations: 'I couldn't help but notice how her eyes sparkled'\n"
                else:
                    prompt += "STYLE REQUIREMENTS: Intimate emotional focus with deep character interiority.\n"
                    prompt += "- Focus on romantic tension and emotional development\n"
                    prompt += "- Rich emotional language and sensory details\n"
            elif "Action" in narrative_style:
                prompt += "STYLE REQUIREMENTS: Fast-paced, dynamic writing with short, punchy sentences.\n"
                prompt += "- Quick dialogue and rapid scene transitions\n"
                prompt += "- Focus on movement and immediate action\n"
            elif "Literary" in narrative_style:
                prompt += "STYLE REQUIREMENTS: Rich, descriptive language with literary depth.\n"
                prompt += "- Beautiful, evocative descriptions\n"
                prompt += "- Metaphorical and symbolic language\n"
            elif "Mysterious" in narrative_style:
                prompt += "STYLE REQUIREMENTS: Atmospheric writing that builds suspense and mood.\n"
                prompt += "- Focus on creating tension and mystery\n"
                prompt += "- Environmental details that enhance mood\n"
            
            prompt += "\n"
        
        # Add target audience information - UPDATED SECTION
        if blueprint_data.get('target_audience', 'Not chosen') != 'Not chosen':
            audience = blueprint_data['target_audience']
            
            prompt += f"TARGET AUDIENCE: {audience}\n"
            
            # Add audience-specific guidelines - UPDATED CONDITIONS
            if audience == 'Children: Ages 3-8: Simple stories, animated style, no scary content':
                prompt += "CONTENT GUIDELINES: Child-friendly content only - no scary elements, death, or violence. Focus on wonder, friendship, and simple problem-solving.\n"
            elif audience == 'Family: Ages 8+: Family-friendly with mild conflict, life lessons':
                prompt += "CONTENT GUIDELINES: Family-friendly content - mild conflict resolution, positive messages, no graphic content.\n"
            elif audience == 'Teen: Ages 13+: Coming-of-age themes, mild language, relationship drama':
                prompt += "CONTENT GUIDELINES: Teen-appropriate themes - coming-of-age, relationships, mild language, age-appropriate challenges.\n"
            elif audience == 'Adult: Ages 18+: Mature themes, complex relationships, realistic content':
                prompt += "CONTENT GUIDELINES: Adult-appropriate content - mature themes, complex character relationships, realistic scenarios.\n"
            elif audience.startswith('Custom:'):
                # Extract the custom guidelines after "Custom: "
                custom_guidelines = audience[8:]  # Remove "Custom: " prefix
                prompt += f"CONTENT GUIDELINES: {custom_guidelines}\n"
        
        # Add language guidelines
        language_settings = blueprint_data.get('language_settings')
        if language_settings:
            from story_generation_menu.language_configurator import LanguageConfigurator
            language_config = LanguageConfigurator()
            language_addition = language_config.get_language_prompt_addition(*language_settings)
            prompt += language_addition
        
        # Core story elements
        prompt += f"BLUEPRINT NAME: {blueprint_data['name']}\n"
        prompt += f"GENRE: {blueprint_data['genre']}\n"
        
        if blueprint_data['subgenre'] != 'Not chosen':
            prompt += f"SUBGENRE: {blueprint_data['subgenre']}\n"
        
        if blueprint_data['target_audience'] != 'Not chosen':
            prompt += f"TARGET AUDIENCE: {blueprint_data['target_audience']}\n"
        
        prompt += f"STORYTELLING STYLE: {blueprint_data['storytelling_style']}\n"
        prompt += f"NARRATIVE PERSPECTIVE: {blueprint_data['perspective']}\n"
        prompt += f"NARRATIVE WRITING STYLE: {blueprint_data['narrative_style']}\n"
        
        # Add language settings if chosen
        if blueprint_data.get('language_settings', ('moderate', 'moderate', 'casual')) != ('moderate', 'moderate', 'casual'):
            prompt += f"LANGUAGE STYLE: {blueprint_data['language_settings'][0]}/{blueprint_data['language_settings'][1]}/{blueprint_data['language_settings'][2]}\n"
            prompt += "Write the blueprint keeping this language style in mind for future story generation.\n"
        else:
            prompt += "LANGUAGE STYLE: Standard\n"
        
        prompt += f"SETTING: {blueprint_data['setting_type']}\n"
        prompt += f"TONE: {blueprint_data['tone']}\n"
        prompt += f"COMPLEXITY: {blueprint_data['complexity']}\n"
        
        if blueprint_data['protagonist_gender'] != 'Not chosen':
            prompt += f"PROTAGONIST GENDER: {blueprint_data['protagonist_gender']}\n"
        
        if blueprint_data['counterpart_type'] != 'Not chosen':
            prompt += f"COUNTERPART CHARACTER: {blueprint_data['counterpart_type']}"
            if blueprint_data.get('counterpart_gender', 'Not chosen') != 'Not chosen':
                prompt += f" ({blueprint_data['counterpart_gender']})"
            prompt += "\n"
        
        if blueprint_data['target_length'] != 'Not chosen':
            prompt += f"TARGET STORY LENGTH: {blueprint_data['target_length']}\n"
        
        if blueprint_data['special_elements']:
            prompt += f"SPECIAL ELEMENTS: {', '.join(blueprint_data['special_elements'])}\n"
        
        if blueprint_data['custom_instructions'] != 'Not chosen':
            prompt += f"CUSTOM REQUIREMENTS: {blueprint_data['custom_instructions']}\n"
        
        prompt += "\n" + "="*60 + "\n\n"
        
        prompt += """Create a detailed story blueprint that includes:

1. STORY OVERVIEW
   - Core premise and hook
   - Central conflict
   - Unique selling point

2. CHARACTER PROFILES
   - Protagonist: background, motivations, character arc
   - Counterpart character: role, relationship to protagonist
   - Supporting characters: key relationships and functions

3. PLOT STRUCTURE
   - Beginning: setup and inciting incident
   - Middle: rising action and complications
   - Climax: major confrontation or revelation
   - Resolution: how conflicts resolve

4. WORLD BUILDING
   - Setting details and atmosphere
   - Rules of the world (if applicable)
   - Cultural/social context

5. THEMES AND SUBTEXT
   - Central themes to explore
   - Underlying messages
   - Character growth arcs

6. SCENE SUGGESTIONS
   - Key scenes that must be included
   - Potential subplot developments
   - Pacing recommendations

7. DIALOGUE AND VOICE NOTES
   - Character speech patterns
   - Narrative voice consistency
   - Tone maintenance guidelines

8. CRITICAL PERSPECTIVE GUIDELINES
   - MANDATORY perspective instructions for story generation
   - Specific examples of correct vs incorrect narrative voice
   - Reminders about maintaining consistent viewpoint throughout"""

        # Add perspective-specific blueprint instructions
        if perspective != 'Not chosen':
            prompt += f"\n\n🚨 PERSPECTIVE ENFORCEMENT FOR BLUEPRINT:\n"
            prompt += f"Include a dedicated section called 'NARRATIVE PERSPECTIVE REQUIREMENTS' that explicitly states:\n"
            
            if perspective == "First person singular":
                prompt += f"- 'This story MUST be written entirely in first person from the protagonist's perspective'\n"
                prompt += f"- 'Every sentence must use I/me/my/myself - NO exceptions'\n"
                prompt += f"- 'NO third person descriptions like \"[protagonist name] walked\" - must be \"I walked\"'\n"
                prompt += f"- 'Story generators must maintain this perspective throughout every scene'\n"
                prompt += f"- 'System prompts must enforce first-person perspective at every generation stage'\n"
                prompt += f"- 'Story bible, scene plans, and scene writing must all respect first-person perspective'\n"
                
                if "Romantic Intimate" in narrative_style:
                    prompt += f"- 'Focus on internal thoughts and feelings: \"I wondered if she noticed me watching her\"'\n"
                    prompt += f"- 'Use intimate internal monologue: \"My heart raced as I realized I was falling for her\"'\n"
        
        prompt += f"\n\nThe blueprint should be comprehensive enough to guide story generation while leaving room for creative variation. Focus on creating compelling characters and conflicts that naturally drive the plot forward.\n\n"
        prompt += f"Write this as a complete, ready-to-use story blueprint that story generators will follow exactly, especially regarding perspective and narrative style."

        return prompt
    
    def save_blueprint_template(self, blueprint_data):
        """Save blueprint configuration as a template (without AI generation)"""
        try:
            filename = f"{blueprint_data['name']}_template.json"
            filepath = os.path.join(self.blueprint_folder, filename)
            
            # Add metadata
            blueprint_data['created_at'] = datetime.now().isoformat()
            blueprint_data['type'] = 'template'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(blueprint_data, f, indent=2, ensure_ascii=False)
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving template: {e}")
            return None
    
    def call_ollama_api(self, model, prompt, max_tokens):
        """Call Ollama API to generate blueprint"""
        try:
            url = "http://localhost:11434/api/generate"
            
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "option4s": {
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            print("🔄 Generating blueprint... (this may take a few minutes)")
            
            response = requests.post(url, json=data, timeout=300)  # 5 minute timeout
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out. Try reducing max tokens or using a faster model.")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Ollama. Make sure it's running with 'ollama serve'")
            return None
        except Exception as e:
            print(f"❌ Error calling Ollama API: {e}")
            return None

    def _format_language_display(self, blueprint_data):
        """Format language settings for display"""
        settings = blueprint_data.get('language_settings', ('moderate', 'moderate', 'casual'))
        if settings == ('moderate', 'moderate', 'casual'):
            return "Standard"
        return f"{settings[0]}/{settings[1]}/{settings[2]}"

    def _generate_blueprint_filename(self, blueprint_data):
        """Generate a filename with genre, name, and date"""
        from datetime import datetime
        
        # Get components
        genre = blueprint_data.get('genre', 'unknown').lower().replace(' ', '_')
        name = blueprint_data.get('name', 'untitled').replace(' ', '_')
        date = datetime.now().strftime('%Y%m%d')
        
        # Clean up genre for filename
        genre = ''.join(c for c in genre if c.isalnum() or c in ['_', '-'])
        name = ''.join(c for c in name if c.isalnum() or c in ['_', '-'])
        
        # Create filename: genre-name-date.story.txt
        filename = f"{genre}-{name}-{date}.story.txt"
        
        return filename

    def _show_blueprint_preview(self, blueprint_content, blueprint_data):
        """Show blueprint preview and get user decision"""
        while True:
            print("\n" + "="*70)
            print("📋 BLUEPRINT PREVIEW")
            print("="*70)
            
            # Show first part of the blueprint
            preview_length = 1000  # Show first 1000 characters
            if len(blueprint_content) > preview_length:
                preview = blueprint_content[:preview_length] + "..."
                print(f"Preview (first {preview_length} characters of {len(blueprint_content):,} total):")
            else:
                preview = blueprint_content
                print(f"Complete blueprint ({len(blueprint_content):,} characters):")
            
            print("-" * 70)
            print(preview)
            print("-" * 70)
            
            if len(blueprint_content) > preview_length:
                print(f"\n... and {len(blueprint_content) - preview_length:,} more characters")
            
            # Show filename that will be used
            filename = self._generate_blueprint_filename(blueprint_data)
            print(f"\n📁 Will be saved as: {filename}")
            
            print("\n" + "="*70)
            print("BLUEPRINT ACTIONS")
            print("="*70)
            print("1. 💾 Save this blueprint")
            print("2. 📄 View full blueprint")
            print("3. 🔄 Regenerate new blueprint")
            print("4. ❌ Cancel (don't save)")
            
            choice = input("\nSelect action (1-4): ").strip()
            
            if choice == "1":
                return 'save'
            elif choice == "2":
                self._show_full_blueprint(blueprint_content)
                # Continue the loop to show options again
            elif choice == "3":
                confirm = input("\nRegenerate blueprint? This will create a new version (y/n): ").strip().lower()
                if confirm == 'y':
                    return 'regenerate'
                # Continue the loop if they don't confirm
            elif choice == "4":
                confirm = input("\nCancel without saving? (y/n): ").strip().lower()
                if confirm == 'y':
                    return 'cancel'
                # Continue the loop if they don't confirm
            else:
                print("❌ Invalid option. Please select 1-4.")
                input("Press Enter to continue...")

    def _show_full_blueprint(self, blueprint_content):
        """Show the complete blueprint with pagination"""
        lines = blueprint_content.split('\n')
        lines_per_page = 30
        current_page = 0
        total_pages = (len(lines) + lines_per_page - 1) // lines_per_page
        
        while True:
            print("\n" + "="*70)
            print(f"📋 FULL BLUEPRINT - PAGE {current_page + 1} of {total_pages}")
            print("="*70)
            
            # Show current page
            start_line = current_page * lines_per_page
            end_line = min(start_line + lines_per_page, len(lines))
            
            for i in range(start_line, end_line):
                print(lines[i])
            
            print("\n" + "="*70)
            print("Navigation: [N]ext page | [P]revious page | [B]ack to actions")
            
            if current_page < total_pages - 1:
                print("           [ENTER] for next page")
            
            nav = input("Select: ").strip().lower()
            
            if nav in ['n', 'next', ''] and current_page < total_pages - 1:
                current_page += 1
            elif nav in ['p', 'prev', 'previous'] and current_page > 0:
                current_page -= 1
            elif nav in ['b', 'back']:
                break
            elif nav == '' and current_page >= total_pages - 1:
                break
            else:
                if current_page >= total_pages - 1:
                    print("End of blueprint reached.")
                    input("Press Enter to go back to actions...")
                    break
                else:
                    print("❌ Invalid option.")
                    input("Press Enter to continue...")


def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_available_ollama_models():
    """Get list of available Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except:
        return []


def get_model_description(model_name):
    """Get a description for a model"""
    descriptions = {
        'llama2': ' - General purpose, good balance',
        'mistral': ' - Fast and efficient',
        'dolphin': ' - Uncensored, creative',
        'codellama': ' - Code-focused',
        'neural-chat': ' - Conversational',
        'mixtral': ' - High quality, slower'
    }
    
    for key, desc in descriptions.items():
        if key in model_name.lower():
            return desc
    return ' - Custom model'


def get_time_estimate(tokens):
    """Get time estimate for token generation"""
    if tokens <= 4096:
        return "1-3 minutes"
    elif tokens <= 8192:
        return "2-5 minutes"
    elif tokens <= 16384:
        return "5-10 minutes"
    elif tokens <= 32768:
        return "10-20 minutes"
    elif tokens <= 65536:
        return "20-40 minutes"
    else:
        return "40+ minutes"
