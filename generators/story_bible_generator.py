import os
from datetime import datetime

class StoryBibleGenerator:
    def __init__(self, api_handler, story_intent_config, system_prompts, storyboard_folder):
        self.api_handler = api_handler
        self.story_intent_config = story_intent_config
        self.system_prompts = system_prompts
        self.storyboard_folder = storyboard_folder
    
    def generate_story_bible(self, blueprint_content, blueprint_name, content_settings=None, language_settings=None):
        """Generate story bible using specialized system prompt with story intent"""
        print("📖 Generating story bible with specialized system prompt...")
        
        # Get the specialized system prompt for story bible creation
        base_system_prompt = self.system_prompts.get('story_bible', '')
        
        # Add story intent requirements to BOTH system and user prompts
        intent_addition = self.story_intent_config.get_formatted_intent_for_prompts()
        system_prompt = base_system_prompt + intent_addition
        
        if system_prompt:
            print("   ✓ Using specialized story bible system prompt")
            if intent_addition:
                print("   🎯 Story intent requirements included")
                print(f"   📏 System prompt length: {len(system_prompt)} chars")
        else:
            print("   ⚠ No system prompt - using default behavior")
        
        # Build comprehensive user prompt that includes ALL settings
        story_configuration_summary = self._build_configuration_summary(content_settings, language_settings)
        
        user_prompt = f"""WRITE A STORY BIBLE NOW using this blueprint:

{blueprint_content}

{story_configuration_summary}

CREATE a detailed story bible that includes:
- Character profiles with names, descriptions, and motivations
- Setting details and atmosphere
- Complete plot structure from beginning to end
- Key scenes and events
- Tone and style guidelines

DO NOT ask questions. DO NOT request more information. WRITE the story bible immediately using the blueprint provided above."""
        
        # NEW: Use token distribution settings from app
        max_tokens = 2000  # fallback default
    
        if hasattr(self.api_handler, 'llm_settings'):
            # Check if app has token distribution settings
            app_settings = getattr(self.api_handler, 'app_settings', None)
            if app_settings:
                # Use app's token distribution settings
                if getattr(app_settings, 'bible_tokens_mode', 'auto') == 'auto':
                    total_tokens = self.api_handler.llm_settings.get('max_tokens', 2000)
                    max_tokens = min(total_tokens // 7, 20000)
                    print(f"   🎯 Using {max_tokens:,} tokens for story bible (auto: {total_tokens:,} ÷ 7)")
                else:
                    max_tokens = getattr(app_settings, 'manual_bible_tokens', 20000)
                    print(f"   🎯 Using {max_tokens:,} tokens for story bible (manual setting)")
            else:
                # Fallback to old auto calculation
                total_tokens = self.api_handler.llm_settings.get('max_tokens', 2000)
                max_tokens = min(total_tokens // 7, 20000)
                print(f"   🎯 Using {max_tokens:,} tokens for story bible (auto fallback)")
        else:
            print(f"   ⚠️ Using fallback {max_tokens} tokens (no LLM settings found)")
        
        # Make API call with enhanced prompts and dynamic tokens
        response = self.api_handler.make_api_call_with_system_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,  # ✅ Now uses app's token distribution settings!
            stage="story_bible"
        )
        
        if not response:
            print("❌ Failed to generate story bible")
            return None
        
        # Save story bible
        bible_filename = f"{blueprint_name.replace('.story.txt', '')}_bible.txt"
        bible_path = os.path.join(self.storyboard_folder, bible_filename)
        
        with open(bible_path, 'w', encoding='utf-8') as f:
            f.write(f"STORY BIBLE - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(response)
            
            # Add configuration summary at the end for reference
            f.write(f"\n\n{'='*60}\n")
            f.write("STORY CONFIGURATION REFERENCE\n")
            f.write("="*60 + "\n")
            f.write(story_configuration_summary)
    
        print(f"   ✓ Story bible saved: {bible_filename}")
        return response

    def _build_configuration_summary(self, content_settings=None, language_settings=None):
        """Build a comprehensive summary of all story configuration settings"""
        summary = "\nSTORY CONFIGURATION SETTINGS:\n"
        summary += "="*50 + "\n"
        
        # Custom Requirements (MOST IMPORTANT)
        if "custom_requirements" in self.story_intent_config.configured_intent:
            requirements = self.story_intent_config.configured_intent["custom_requirements"]
            summary += "MANDATORY STORY REQUIREMENTS:\n"
            if isinstance(requirements, list):
                for i, req in enumerate(requirements, 1):
                    summary += f"{i}. {req}\n"
            else:
                summary += f"1. {requirements}\n"
            summary += "\n"
        
        # Narrative Style
        if "narrative_style" in self.story_intent_config.configured_intent:
            style = self.story_intent_config.configured_intent["narrative_style"]
            summary += f"NARRATIVE STYLE: {style}\n"
            
            # Add specific pronoun guidance
            if "First Person" in style and "Second Person" not in style:
                summary += "- Write as 'I' for protagonist, 'she/he' for others\n"
            elif "Second Person" in style:
                summary += "- Write as 'I' for protagonist, 'you' for love interest, 'she/he' for others\n"
            summary += "\n"
        
        # Story Intent Elements
        intent_elements = [
            ("protagonist_goal", "Protagonist's Goal"),
            ("story_theme", "Central Theme"),
            ("story_outcome", "Desired Outcome"),
            ("emotional_journey", "Emotional Arc"),
            ("story_tone", "Story Tone")
        ]
        
        for key, label in intent_elements:
            if key in self.story_intent_config.configured_intent:
                value = self.story_intent_config.configured_intent[key]
                summary += f"{label.upper()}: {value}\n"
        
        # Content Rating and Language - ONLY IF NOT DEFAULT/AUTO
        if content_settings:
            content_rating = content_settings.get('content_rating', 'auto')
            if content_rating != "auto":
                summary += f"\nCONTENT RATING: {content_rating.title()}\n"
        
        # FIX: Only add language settings if they're not default/standard
        if language_settings:
            profanity = language_settings.get('profanity_level', 'moderate')
            intensity = language_settings.get('dialogue_intensity', 'moderate')
            style = language_settings.get('speech_style', 'casual')
            
            # Only add language instructions if settings are non-standard
            is_standard_language = (
                profanity == 'moderate' and 
                intensity == 'moderate' and 
                style == 'casual'
            )
            
            if not is_standard_language:
                lang_summary = f"{profanity.title()} language, {intensity.title()} intensity, {style.title()} style"
                summary += f"LANGUAGE STYLE: {lang_summary}\n"
        
        # Only add the enforcement notice if we actually have requirements
        has_requirements = (
            "custom_requirements" in self.story_intent_config.configured_intent or
            "narrative_style" in self.story_intent_config.configured_intent or
            (content_settings and content_settings.get('content_rating', 'auto') != 'auto') or
            (language_settings and not is_standard_language)
        )
        
        if has_requirements:
            summary += "="*50 + "\n"
            summary += "All elements above MUST be incorporated into the story bible and followed throughout the story.\n"
        else:
            summary += "Follow the blueprint's natural style and tone.\n"
        
        return summary
