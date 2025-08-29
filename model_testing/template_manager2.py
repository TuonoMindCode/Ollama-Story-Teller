import os
from typing import Dict, List, Optional, Tuple
from .model_tester import ModelTester
from .quick_scene_prompts import QUICK_SCENE_PROMPTS, QUICK_STORY_PROMPTS
from .comprehensive_detective_prompts import DETECTIVE_STYLES, build_comprehensive_prompt
from .comprehensive_fantasy_prompts import FANTASY_STYLES, build_fantasy_prompt

# Import the new modular files
from .user_prompt_creators import UserPromptCreators
from .system_prompt_creators import SystemPromptCreators  
from .template_browser import TemplateBrowser
# Fix this import - it should go to the templates subfolder
from .templates.story_user_prompt_builder import StoryUserPromptBuilder

class TemplateManager:
    def __init__(self, model_tester):
        self.model_tester = model_tester
        self.content_type = None  # 'story' or 'scene'
        # Use the same folder structure as Scene Workshop
        self.template_base_dir = "laboratory/templates"
        self.system_prompts_dir = os.path.join(self.template_base_dir, "system_prompts")
        self.user_prompts_dir = os.path.join(self.template_base_dir, "user_prompts")
        
        # Ensure directories exist
        os.makedirs(self.system_prompts_dir, exist_ok=True)
        os.makedirs(self.user_prompts_dir, exist_ok=True)
        
        # Initialize the modular components
        self.user_prompt_creators = UserPromptCreators(self)
        self.system_prompt_creators = SystemPromptCreators(self)
        self.template_browser = TemplateBrowser(self)
    
    def run_template_menu(self):
        """Main template manager menu"""
        while True:
            self.display_template_menu()
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    self.select_content_type()
                elif choice == "2":
                    self.system_prompt_menu()
                elif choice == "3":
                    self.user_prompt_menu()
                elif choice == "4":
                    self.template_browser.view_saved_templates()
                elif choice == "5":
                    self.template_browser.delete_templates()
                elif choice == "6":
                    break
                else:
                    print("Invalid option. Please select 1-6.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user")
                input("Press Enter to continue...")
    
    def display_template_menu(self):
        """Display template manager menu with better explanation"""
        print("\n" + "="*80)
        print("TEMPLATE MANAGER - Create & Manage Reusable AI Prompts")
        print("="*80)
        print("WHAT ARE TEMPLATES?")
        print("Templates are pre-written prompts you can reuse for consistent AI generation.")
        print()
        print("SYSTEM PROMPTS: Tell the AI HOW to write (style, tone, format)")
        print("   Example: 'Write romantic scenes with detailed emotions and dialogue'")
        print()
        print("USER PROMPTS: Tell the AI WHAT to write about (story/scene content)")
        print("   Example: 'Two characters meeting for the first time at a coffee shop'")
        print()
        
        # Show current content type selection with clearer messaging
        if self.content_type:
            print(f"CURRENT FOCUS: {self.content_type.upper()} templates")
            print(f"   (Menu options are now customized for {self.content_type} creation)")
        else:
            print("CONTENT TYPE: Not Selected")
            print("   (You must choose Story or Scene first to see appropriate options)")
        
        print("\n" + "="*80)
        print("1. Select Content Type (Story or Scene) - REQUIRED FIRST STEP")
        
        # Show dynamic menu options based on content type
        if self.content_type:
            content_label = self.content_type.capitalize()
            print(f"2. {content_label} System Prompts (How AI should write)")
            print(f"3. {content_label} User Prompts (What AI should write about)")
        else:
            print("2. System Prompts (Select content type first)")
            print("3. User Prompts (Select content type first)")
            
        print("4. Browse Saved Templates")
        print("5. Delete Templates")
        print("6. Back to Main Menu")
        print("\nSelect option (1-6): ", end="")
    
    def select_content_type(self):
        """Select content type with clear explanation"""
        print("\n" + "="*70)
        print("CONTENT TYPE SELECTION")
        print("="*70)
        print("Choose what type of content your templates will generate:")
        print()
        print("SCENE Templates (Option 1):")
        print("   • Single scenes, moments, or character interactions")
        print("   • Shorter content (typically 200-1000 words)")
        print("   • Focus: Dialogue, action, specific moments")
        print("   • Example: A conversation, a fight scene, a romantic moment")
        print("   • Files saved as: system_prompt_scene_[name].txt")
        print()
        print("STORY Templates (Option 2):")
        print("   • Complete stories with beginning, middle, end")  
        print("   • Longer content (typically 1000+ words)")
        print("   • Focus: Full narrative arcs, character development")
        print("   • Example: Complete short stories, story chapters")
        print("   • Files saved as: system_prompt_story_[name].txt")
        print()
        print("TIP: Choose based on what you want to create most often.")
        print("     You can always come back and switch between them!")
        print()
        print("1. Scene Templates (For individual scenes/moments)")
        print("2. Story Templates (For complete stories)")
        
        try:
            choice = int(input("\nSelect content type (1-2): "))
            
            if choice == 1:
                self.content_type = 'scene'
                print(f"\nContent type set to: SCENE TEMPLATES")
                print("You can now create templates for generating individual scenes.")
                print("Menu options will now show 'Scene System Prompts', 'Scene User Prompts', etc.")
                return True
            elif choice == 2:
                self.content_type = 'story'
                print(f"\nContent type set to: STORY TEMPLATES") 
                print("You can now create templates for generating complete stories.")
                print("Menu options will now show 'Story System Prompts', 'Story User Prompts', etc.")
                return True
            else:
                print("Invalid choice. Please select 1 or 2.")
                return False
                
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")
            return False
        
        input("\nPress Enter to continue...")
    
    def system_prompt_menu(self):
        """System prompt management menu"""
        if not self.content_type:
            print("\nCONTENT TYPE REQUIRED")
            print("You must select Story or Scene content type first!")
            print("This determines what kind of system prompts you can create.")
            print("   - Scene system prompts: Optimized for single scenes")
            print("   - Story system prompts: Optimized for complete narratives")
            input("\nPress Enter to go back and select content type...")
            return
            
        while True:
            self.display_system_prompt_menu()
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    self.choose_genre_style()
                elif choice == "2":
                    self.system_prompt_creators.create_ai_generated_prompt()
                elif choice == "3":
                    self.system_prompt_creators.create_comprehensive_romance_prompt()
                elif choice == "4":
                    self.system_prompt_creators.create_comprehensive_detective_prompt()
                elif choice == "5":
                    self.system_prompt_creators.create_comprehensive_fantasy_prompt()
                elif choice == "6":
                    self.system_prompt_creators.create_comprehensive_scifi_prompt()
                elif choice == "7":
                    self.system_prompt_creators.create_custom_system_prompt()
                elif choice == "8":
                    self.template_browser.browse_system_prompts()
                elif choice == "9":
                    break
                else:
                    print("Invalid option. Please select 1-9.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user")
                input("Press Enter to continue...")
    
    def user_prompt_menu(self):
        """User prompt management menu"""
        if not self.content_type:
            print("\nCONTENT TYPE REQUIRED")
            print("You must select Story or Scene content type first!")
            print("This determines what kind of user prompts you can create.")
            print("   - Scene user prompts: Describe specific scenes to generate")
            print("   - Story user prompts: Describe complete stories to generate")
            input("\nPress Enter to go back and select content type...")
            return
        
        while True:
            self.display_user_prompt_menu()
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    self.user_prompt_creators.create_ai_generated_user_prompt()
                elif choice == "2":
                    self.user_prompt_creators.create_scenario_prompt()
                elif choice == "3":
                    self.user_prompt_creators.create_character_focused_prompt()
                elif choice == "4":
                    self.user_prompt_creators.create_genre_user_prompt()
                elif choice == "5":
                    self.user_prompt_creators.create_custom_user_prompt()
                elif choice == "6":
                    # Add the comprehensive story builder for stories
                    if self.content_type == 'story':
                        self.show_story_user_prompt_builder()
                    else:
                        self.template_browser.browse_user_prompts()
                elif choice == "7":
                    if self.content_type == 'story':
                        self.template_browser.browse_user_prompts()
                    else:
                        break
                elif choice == "8":
                    if self.content_type == 'story':
                        break
                    else:
                        print("Invalid option. Please select 1-7.")
                        input("Press Enter to continue...")
                else:
                    max_option = 8 if self.content_type == 'story' else 7
                    print(f"Invalid option. Please select 1-{max_option}.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user")
                input("Press Enter to continue...")
    
    def display_system_prompt_menu(self):
        """Display system prompt menu with content type awareness"""
        content_label = self.content_type.capitalize()
        
        print(f"\n{'='*75}")
        print(f"{content_label.upper()} SYSTEM PROMPTS - How AI Should Write")
        print(f"{'='*75}")
        print("WHAT ARE SYSTEM PROMPTS?")
        print(f"System prompts tell the AI HOW to write your {content_label.lower()}s:")
        print(f"• Writing style (formal, casual, poetic)")
        print(f"• Tone and mood (dark, humorous, romantic)")
        print(f"• Format preferences (dialogue-heavy, descriptive)")
        print(f"• Genre conventions (fantasy magic, sci-fi tech)")
        print()
        print(f"These save as: system_prompt_{self.content_type}_[name].txt")
        print(f"Perfect for: Consistent {content_label.lower()} style across multiple generations")
        print()
        
        print("CREATION OPTIONS:")
        print("1. Quick Genre & Style (Simple ~20 word prompts)")
        print(f"2. AI-Generated Comprehensive {content_label} System Prompt")
        print(f"3. Comprehensive Romance {content_label} Writing Style")
        print(f"4. Comprehensive Detective {content_label} Writing Style") 
        print(f"5. Comprehensive Fantasy {content_label} Writing Style")
        print(f"6. Comprehensive Sci-Fi {content_label} Writing Style")
        print(f"7. Write Custom {content_label} System Prompt")
        print(f"8. Browse/View Saved {content_label} System Prompts")
        print("9. Back to Template Manager")
        print("\nSelect option (1-9): ", end="")
    
    def display_user_prompt_menu(self):
        """Display user prompt menu"""
        content_label = self.content_type.capitalize()
        
        print(f"\n{'='*75}")
        print(f"{content_label.upper()} USER PROMPTS - What AI Should Write About") 
        print(f"{'='*75}")
        print("WHAT ARE USER PROMPTS?")
        print(f"User prompts tell the AI WHAT {content_label.lower()} to create:")
        print(f"• Plot ideas and scenarios")
        print(f"• Character descriptions and relationships")
        print(f"• Settings and environments")
        print(f"• Specific events or conflicts to include")
        print()
        print(f"These save as: user_prompt_{self.content_type}_[name].txt")
        print(f"Note: Length requirements added automatically during generation")
        print(f"Perfect for: Reusing {content_label.lower()} concepts you like")
        print()

        print("CREATION OPTIONS:")
        print(f"1. AI-Generated Comprehensive {content_label} User Prompt")
        print(f"2. Scenario-Based {content_label} Prompt")
        print(f"3. Character-Focused {content_label} Prompt") 
        print(f"4. Genre-Specific {content_label} Prompt")
        print(f"5. Write Custom {content_label} User Prompt")
        
        # Add comprehensive builder for stories
        if self.content_type == 'story':
            print(f"6. Comprehensive Story Builder (Multi-Select Interface)")
            print(f"7. Browse/View Saved {content_label} User Prompts")
            print("8. Back to Template Manager")
            print("\nSelect option (1-8): ", end="")
        else:
            print(f"6. Browse/View Saved {content_label} User Prompts")
            print("7. Back to Template Manager")
            print("\nSelect option (1-7): ", end="")
    
    def choose_genre_style(self):
        """Quick genre & style selection with ~20 word prompts"""
        print(f"\n{'='*70}")
        print(f"QUICK {self.content_type.upper()} GENRE & STYLE SELECTION")
        print(f"{'='*70}")
        print("Choose your genre and style for a simple ~20 word system prompt")
        print("These prompts focus on tone, mood, and key elements for effective generation.")
        
        # Select appropriate prompts based on content type
        if self.content_type == 'scene':
            prompts_dict = QUICK_SCENE_PROMPTS
        elif self.content_type == 'story':
            prompts_dict = QUICK_STORY_PROMPTS
        else:
            print("Please select content type first!")
            input("Press Enter to continue...")
            return
        
        # Show available genres
        genres = list(prompts_dict.keys())
        print(f"\nAVAILABLE GENRES ({len(genres)} total):")
        print("-" * 50)
        for i, genre in enumerate(genres, 1):
            style_count = len(prompts_dict[genre])
            print(f"{i:2d}. {genre:<18} ({style_count} styles available)")
        
        try:
            genre_choice = int(input(f"\nSelect genre (1-{len(genres)}): "))
            if not (1 <= genre_choice <= len(genres)):
                print("Invalid choice.")
                input("Press Enter to continue...")
                return
                
            selected_genre = genres[genre_choice - 1]
            styles = prompts_dict[selected_genre]
            
            print(f"\nAVAILABLE STYLES FOR {selected_genre.upper()}:")
            print("=" * 60)
            style_list = list(styles.keys())
            
            for i, style in enumerate(style_list, 1):
                print(f"{i:2d}. {style}")
                print(f"    └─ {styles[style]}")
                print()
            
            style_choice = int(input(f"Select style (1-{len(style_list)}): "))
            if not (1 <= style_choice <= len(style_list)):
                print("Invalid choice.")
                input("Press Enter to continue...")
                return
                
            selected_style = style_list[style_choice - 1]
            selected_prompt = styles[selected_style]
            
            # Show preview
            print(f"\nSELECTED PROMPT PREVIEW:")
            print("=" * 50)
            print(f"Genre: {selected_genre}")
            print(f"Style: {selected_style}")
            print(f"Prompt ({len(selected_prompt.split())} words):")
            print(f'"{selected_prompt}"')
            print("=" * 50)
            
            # Confirm and save
            save_choice = input("\nSave this template? (y/n): ").strip().lower()
            if save_choice != 'y':
                print("Template not saved.")
                input("Press Enter to continue...")
                return
            
            # Create safe filename
            safe_genre = selected_genre.replace(" ", "_").replace("&", "and").lower()
            safe_style = selected_style.replace(" ", "_").replace("&", "and").lower()
            template_name = f"{safe_genre}_{safe_style}"
            
            # Save the template
            if self.save_system_prompt_template(template_name, selected_prompt):
                print(f"\nQuick style template saved successfully!")
                print(f"Filename: system_prompt_{self.content_type}_{template_name}.txt")
                print(f"Usage: This template can now be selected in Scene Workshop")
                print(f"Note: Length requirements will be added automatically when used")
            else:
                print("Failed to save template.")
            
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error: {e}")
        
        input("Press Enter to continue...")
    
    # Core file management methods stay here
    def save_system_prompt_template(self, name, content):
        """Save system prompt as .txt file in templates/system_prompts/"""
        if self.content_type:
            filename = f"system_prompt_{self.content_type}_{name}.txt"
        else:
            filename = f"system_prompt_{name}.txt"
        
        filepath = os.path.join(self.system_prompts_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"System prompt template saved: {filename}")
            print(f"Location: {filepath}")
            return True
        except Exception as e:
            print(f"Failed to save template: {e}")
            return False
    
    def save_user_prompt_template(self, name, content):
        """Save user prompt as .txt file in templates/user_prompts/"""
        if self.content_type:
            filename = f"user_prompt_{self.content_type}_{name}.txt"
        else:
            filename = f"user_prompt_{name}.txt"
        
        filepath = os.path.join(self.user_prompts_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"User prompt template saved: {filename}")
            print(f"Location: {filepath}")
            return True
        except Exception as e:
            print(f"Failed to save template: {e}")
            return False
    
    def list_system_prompts(self):
        """List all system prompt templates"""
        if not os.path.exists(self.system_prompts_dir):
            return []
        
        files = [f for f in os.listdir(self.system_prompts_dir) if f.endswith('.txt')]
        return sorted(files)
    
    def list_user_prompts(self):
        """List all user prompt templates"""
        if not os.path.exists(self.user_prompts_dir):
            return []
        
        files = [f for f in os.listdir(self.user_prompts_dir) if f.endswith('.txt')]
        return sorted(files)
    
    def show_story_user_prompt_builder(self):
        """Show the story user prompt builder"""
        story_builder = StoryUserPromptBuilder(self)
        story_builder.create_comprehensive_story_user_prompt()
