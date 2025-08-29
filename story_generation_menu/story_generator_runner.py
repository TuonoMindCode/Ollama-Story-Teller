import time
import os
from generators.story_generator import StoryGenerator
from .system_prompt_builder import SystemPromptBuilder
from blueprint_processor import BlueprintProcessor

class StoryGeneratorRunner:
    def __init__(self, app_instance):
        self.app = app_instance
        # Add blueprint processor
        self.blueprint_processor = None
    
    def _get_blueprint_processor(self):
        """Get or create blueprint processor with current settings"""
        if not self.blueprint_processor:
            ollama_settings = self.app._get_current_llm_settings()
            self.blueprint_processor = BlueprintProcessor(ollama_settings)
        return self.blueprint_processor
    
    def generate_stories_now(self, selected_blueprint, scene_control_mode, num_scenes, 
                           narrative_consistency, content_rating, story_tone, story_ending,
                           character_count, story_variations, story_intent_config=None,
                           perspective_controller=None,
                           profanity_level="moderate", dialogue_intensity="moderate", speech_style="casual",
                           custom_story_title=None):
        """Generate stories with current configuration using system prompts"""
        # Use selected blueprint or fall back to app's selected blueprint
        blueprint_to_use = selected_blueprint or self.app.selected_blueprint
        
        if not blueprint_to_use:
            print("\n❌ No blueprint selected!")
            print("Please select a blueprint first (option 1).")
            input("Press Enter to continue...")
            return
        
        if not self.app.selected_model:
            print("\n❌ No language model selected!")
            print("Please select a model in the main menu first.")
            input("Press Enter to continue...")
            return
        
        print(f"\n{'='*60}")
        print("GENERATING STORIES WITH SYSTEM PROMPTS")
        print("="*60)
        print(f"Blueprint: {blueprint_to_use}")
        print(f"Scene Control: {scene_control_mode.title()}", end="")
        if scene_control_mode == "manual":
            print(f" ({num_scenes} scenes)")
        else:
            print()
        print(f"Consistency: {narrative_consistency.replace('_', ' ').title()}")
        
        # Show content settings - handle custom rating display
        if content_rating == "auto":
            rating_display = "Auto (from blueprint)"
        elif content_rating.startswith("custom:"):
            custom_text = content_rating[7:]
            rating_display = f"Custom: {custom_text}"
        else:
            rating_display = content_rating.title()
        
        tone_display = story_tone.replace('_', ' ').title() if story_tone != "auto" else "Auto (from blueprint)"
        ending_display = story_ending.replace('_', ' ').title() if story_ending != "auto" else "Auto (from blueprint)"
        character_display = character_count.replace('_', ' ').title() if character_count != "auto" else "Auto (from blueprint)"
        
        print(f"Content Rating: {rating_display}")
        print(f"Story Tone: {tone_display}")
        print(f"Story Ending: {ending_display}")
        print(f"Character Count: {character_display}")
        print(f"Variations: {story_variations}")
        print(f"Model: {self.app.selected_model}")
        
        confirm = input(f"\nGenerate {story_variations} {'story' if story_variations == 1 else 'stories'}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("✓ Generation cancelled")
            input("Press Enter to continue...")
            return
        
        # Get gender swap mode from settings (move this early)
        gender_swap_mode = self.app.settings.get("gender_swap_mode", "none")
        
        # Create content settings
        content_settings = {
            'content_rating': content_rating,
            'story_tone': story_tone,  
            'story_ending': story_ending,
            'character_count': character_count
        }
        
        # Create language settings (this was missing!)
        language_settings = {
            'profanity_level': profanity_level,
            'dialogue_intensity': dialogue_intensity,
            'speech_style': speech_style
        }
        
        # BUILD SYSTEM PROMPT SETTINGS
        content_settings_for_prompts = {
            'rating': content_rating,
            'tone': story_tone,
            'ending': story_ending
        }
        
        # NEW: Load blueprint data to extract perspective settings
        blueprint_data = self._load_blueprint_data(blueprint_to_use)
        
        # Build system prompts for different stages WITH BLUEPRINT DATA
        story_bible_system_prompt = SystemPromptBuilder.build_story_generation_system_prompt(
            content_settings_for_prompts, narrative_consistency, character_count, "story_bible", blueprint_data
        )
        
        scene_plan_system_prompt = SystemPromptBuilder.build_story_generation_system_prompt(
            content_settings_for_prompts, narrative_consistency, character_count, "scene_plan", blueprint_data
        )
        
        scene_writing_system_prompt = SystemPromptBuilder.build_story_generation_system_prompt(
            content_settings_for_prompts, narrative_consistency, character_count, "scene_writing", blueprint_data
        )
        
        # Show perspective enforcement status
        perspective = blueprint_data.get('perspective', 'Not chosen') if blueprint_data else 'Not chosen'
        narrative_style = blueprint_data.get('narrative_style', 'Not chosen') if blueprint_data else 'Not chosen'
        
        if perspective != 'Not chosen':
            print(f"🎭 Perspective: {perspective}")
            if narrative_style != 'Not chosen':
                print(f"📝 Style: {narrative_style}")
        
        # Get LLM settings from app
        llm_settings = {
            'model': self.app.selected_model,
            'max_tokens': self.app.max_tokens,
            'temperature': self.app.temperature,
            'top_p': self.app.top_p,
            'top_k': self.app.top_k,
            'repeat_penalty': self.app.repeat_penalty,
            'seed': self.app.seed,
            'gender_swap_mode': gender_swap_mode,
            'blueprint_folder': self.app.blueprint_folder,
            'stats_folder': self.app.multiscene_stats_folder,  # ADD THIS LINE
            'narrative_consistency': narrative_consistency,
            'content_settings': content_settings,
            'language_settings': language_settings,
            'story_intent': story_intent_config,
            'system_prompts': {
                'story_bible': story_bible_system_prompt,
                'scene_plan': scene_plan_system_prompt, 
                'scene_writing': scene_writing_system_prompt
            },
            # Pass app settings for prompt logging
            'app_settings': self.app.settings.settings
        }
        
        # ... rest of existing code remains the same ...
        
        # Create story generator with correct parameters
        generator = StoryGenerator(
            blueprint_to_use,  # blueprint_file parameter
            self.app.stories_folder,  # stories_folder parameter  
            self.app.storyboard_folder,  # storyboard_folder parameter
            llm_settings  # ollama_settings parameter - now includes everything
        )
        
        # Pass the custom title setting to the generator
        generator.custom_story_title = custom_story_title
        
        # NEW: Pass app settings to the generator so it can access token distribution settings
        generator.app_settings = self.app  # This gives generators access to token settings
        
        # Ensure the API handler has access to app settings too
        if hasattr(generator, 'api_handler'):
            generator.api_handler.app_settings = self.app
        
        # Also pass to individual generators
        if hasattr(generator, 'bible_generator') and hasattr(generator.bible_generator, 'api_handler'):
            generator.bible_generator.api_handler.app_settings = self.app
        
        if hasattr(generator, 'scene_planner') and hasattr(generator.scene_planner, 'api_handler'):
            generator.scene_planner.api_handler.app_settings = self.app
        
        if hasattr(generator, 'scene_writer') and hasattr(generator.scene_writer, 'api_handler'):
            generator.scene_writer.api_handler.app_settings = self.app
        
        # Set additional properties that your StoryGenerator expects
        generator.narrative_consistency = narrative_consistency
        generator.content_settings = content_settings
        generator.language_settings = language_settings
        generator.story_intent = story_intent_config
        generator.system_prompts = llm_settings.get('system_prompts', {})
        generator.clean_llm_settings = {
            'model': self.app.selected_model,
            'max_tokens': self.app.max_tokens,
            'temperature': self.app.temperature,
            'top_p': self.app.top_p,
            'top_k': self.app.top_k,
            'repeat_penalty': self.app.repeat_penalty,
            'seed': self.app.seed
        }
        generator.blueprint_folder = self.app.blueprint_folder  # Add this missing property

        # Set the perspective controller if provided
        if perspective_controller:
            generator.perspective_controller = perspective_controller
            print(f"🎭 Perspective: {perspective_controller.selected_perspective.replace('_', ' ').title()}")
        
        # Show gender swap status
        if gender_swap_mode != "none":
            gender_display = {
                "main_lead": "Main lead gender swap",
                "both_leads": "Both leads gender swap"
            }
            print(f"🔄 Gender Swap: {gender_display[gender_swap_mode]}")
        
        # ... rest of existing code for story generation loop ...
        
        print(f"\nGenerating {story_variations} complete stories using {blueprint_to_use}...")
        print("This involves 3 phases per story:")
        print("1. Creating/reusing story bible (with specialized system prompt)")
        print("2. Creating/reusing scene plan (with specialized system prompt)") 
        print("3. Writing all scenes (with specialized system prompt)")
        
        # Show current reuse setting
        if self.app.storyboard_reuse_mode == "new":
            print("📋 Mode: Creating fresh story bible & scene plan for each story")
        elif self.app.storyboard_reuse_mode == "bible_only":
            print("📋 Mode: Reusing story bible, creating new scene plans")
        elif self.app.storyboard_reuse_mode == "both":
            print("📋 Mode: Reusing existing story bible & scene plan")
        
        # Show content overrides built into system prompts
        overrides = []
        if content_rating != "auto":
            if content_rating.startswith("custom:"):
                custom_text = content_rating[7:]
                overrides.append(f"Rating: Custom ({custom_text})")
            else:
                overrides.append(f"Rating: {content_rating.title()}")
        if story_tone != "auto":
            overrides.append(f"Tone: {story_tone.replace('_', ' ').title()}")
        if story_ending != "auto":
            overrides.append(f"Ending: {story_ending.replace('_', ' ').title()}")
        if character_count != "auto":
            overrides.append(f"Characters: {character_count.replace('_', ' ').title()}")
        
        if overrides:
            print(f"🎬 System Prompt Personality: {' | '.join(overrides)}")
        else:
            print("🎬 System Prompt: Using blueprint's natural style")
        
        # Show auto-audio status
        if self.app.auto_generate_audio:
            print("🎵 Auto-audio generation: Enabled")
        
        print("-" * 60)
        
        generated_stories = []
        story_casts = []  # Store cast info for each story
        
        for i in range(1, story_variations + 1):
            print(f"\n{'='*20} STORY {i}/{story_variations} {'='*20}")
            
            # Generate story with processed blueprint
            story_filename, context_tracker = generator.generate_complete_story(blueprint_to_use, i)
            
            # ... rest of existing loop code ...
            
            if story_filename:
                print(f"✓ Story {i} completed successfully!")
                generated_stories.append(story_filename)
                
                # Show cast if auto-tracking was used
                if context_tracker and narrative_consistency == "auto_tracking":
                    cast_summary = context_tracker.get_story_cast()
                    story_casts.append(cast_summary)
                    print(f"\n{cast_summary}")
                
                # Auto-generate audio if enabled
                if self.app.auto_generate_audio:
                    print(f"🎵 Auto-generating audio for story {i}...")
                    if hasattr(self.app, '_auto_generate_audio'):
                        self.app._auto_generate_audio(story_filename)
            else:
                print(f"❌ Error generating story {i}")
            
            if i < story_variations:
                print("Waiting 2 seconds before next story...")
                time.sleep(2)
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"GENERATION COMPLETE!")
        print("="*60)
        print(f"Generated stories: {len(generated_stories)}/{story_variations}")
        
        if narrative_consistency == "auto_tracking" and story_casts:
            print(f"\n🎭 CAST DIVERSITY SUMMARY:")
            total_entities = 0
            for i, cast in enumerate(story_casts, 1):
                entity_count = cast.count('•')
                total_entities += entity_count
                print(f"   Story {i}: {entity_count} unique entities detected")
            print(f"   Total: {total_entities} entity appearances across all stories")
        
        print(f"\nCheck the '{self.app.stories_folder}/' folder for your generated stories.")
        
        if self.app.auto_generate_audio and generated_stories:
            print(f"🎵 Audio files generated in 'audio_stories/' folder.")
        
        print("\n🧠 SYSTEM PROMPT BENEFITS DELIVERED:")
        print("   ✓ Content settings were built into AI personality from start")
        print("   ✓ No fighting against instructions - natural storytelling")
        print("   ✓ All stages maintained consistent personality")
    
    def _load_blueprint_data(self, blueprint_filename):
        """Load and parse blueprint to extract perspective and narrative style settings"""
        try:
            blueprint_path = os.path.join(self.app.blueprint_folder, blueprint_filename)
            
            if not os.path.exists(blueprint_path):
                print(f"⚠️ Blueprint file not found: {blueprint_path}")
                return None
            
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                blueprint_content = f.read()
            
            # Parse blueprint content to extract settings
            blueprint_data = {}
            
            # Look for perspective information in the blueprint
            if "FIRST PERSON" in blueprint_content.upper() or "first person" in blueprint_content:
                if "singular" in blueprint_content.lower():
                    blueprint_data['perspective'] = 'First person singular'
                elif "plural" in blueprint_content.lower():
                    blueprint_data['perspective'] = 'First person plural'
                else:
                    blueprint_data['perspective'] = 'First person singular'  # Default
            elif "THIRD PERSON" in blueprint_content.upper() or "third person" in blueprint_content:
                if "limited" in blueprint_content.lower():
                    blueprint_data['perspective'] = 'Third person limited'
                elif "omniscient" in blueprint_content.lower():
                    blueprint_data['perspective'] = 'Third person omniscient'
                else:
                    blueprint_data['perspective'] = 'Third person limited'  # Default
            elif "SECOND PERSON" in blueprint_content.upper() or "second person" in blueprint_content:
                blueprint_data['perspective'] = 'Second person'
            
            # Look for narrative style information
            if "romantic intimate" in blueprint_content.lower():
                blueprint_data['narrative_style'] = 'Romantic Intimate First Person'
            elif "fast-paced action" in blueprint_content.lower() or "action" in blueprint_content.lower():
                blueprint_data['narrative_style'] = 'Fast-paced Action'
            elif "literary" in blueprint_content.lower() or "descriptive" in blueprint_content.lower():
                blueprint_data['narrative_style'] = 'Descriptive Literary'
            elif "mysterious" in blueprint_content.lower() or "atmospheric" in blueprint_content.lower():
                blueprint_data['narrative_style'] = 'Mysterious Atmospheric'
            
            print(f"📋 Extracted from blueprint: {blueprint_data}")
            return blueprint_data
            
        except Exception as e:
            print(f"⚠️ Error loading blueprint data: {e}")
            return None
