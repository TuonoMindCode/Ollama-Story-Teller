import os
import re
import time
import shutil
from datetime import datetime
from .story_utils import StoryUtils

class SceneWriter:
    def __init__(self, api_handler, story_intent_config, system_prompts, context_tracker=None, perspective_controller=None):
        self.api_handler = api_handler
        self.story_intent_config = story_intent_config
        self.system_prompts = system_prompts
        self.context_tracker = context_tracker
        self.perspective_controller = perspective_controller
        
        # Define scene token options
        self.SCENE_TOKENS = {
            "short_scene": 2000,    # ~1,500 words
            "normal_scene": 4000,   # ~3,000 words  
            "long_scene": 6000,     # ~4,500 words
            "epic_scene": 8000      # ~6,000 words (max recommended)
        }
    
    def generate_scene_with_prompts(self, scene_description, story_bible, scene_plan, scene_number, total_scenes):
        """Generate scene and return both content and the prompts used"""
        print(f"✍️ Writing scene {scene_number}/{total_scenes} with specialized system prompt...")
        
        # DEBUG: Check if we have access to app settings
        print(f"   🔍 API handler exists: {hasattr(self, 'api_handler')}")
        if hasattr(self, 'api_handler'):
            print(f"   🔍 LLM settings exist: {hasattr(self.api_handler, 'llm_settings')}")
            if hasattr(self.api_handler, 'llm_settings'):
                print(f"   🔍 App settings exist: {hasattr(self.api_handler, 'app_settings')}")
                print(f"   🔍 Max tokens in LLM settings: {self.api_handler.llm_settings.get('max_tokens', 'NOT FOUND')}")

        # BUILD SYSTEM PROMPT (capture it before use)
        base_system_prompt = self.system_prompts.get('scene_writing', '')
        
        # Add story intent requirements
        intent_addition = self.story_intent_config.get_formatted_intent_for_prompts()
        system_prompt = base_system_prompt + intent_addition
        
        if system_prompt:
            print(f"   ✓ Using specialized scene writing system prompt")
            if intent_addition:
                print("   🎯 Story intent requirements included")
                print(f"   📏 System prompt length: {len(system_prompt)} chars")
                # Show narrative style being used
                if "narrative_style" in self.story_intent_config.configured_intent:
                    style = self.story_intent_config.configured_intent["narrative_style"]
                    if "First Person" in style:
                        print("   📝 Writing in First Person POV")
                    elif "Second Person" in style:
                        print("   💕 Writing in Second Person Romance style")
        else:
            print("   ⚠ No system prompt - using default behavior")
        
        # Build context for auto-tracking
        context_info = ""
        if self.context_tracker:
            context_info = f"\n\nKNOWN ENTITIES (maintain consistency):\n{self.context_tracker.get_context_summary()}"
        
        # Apply perspective modifications to scene description
        modified_scene_description = scene_description
        if self.perspective_controller:
            modified_scene_description = self.perspective_controller.apply_perspective_to_scene_plan(scene_description, scene_number)
        
        # Build HEAVILY reinforced user prompt
        story_requirements_reminder = self._build_story_requirements_reminder()
        
        # Calculate max tokens using new system
        max_tokens = self._calculate_scene_tokens()
        
        # BUILD USER PROMPT (capture it before use)
        user_prompt = f"""Write this scene in full narrative prose - WRITE A DETAILED SCENE ({max_tokens * 0.75:.0f}-{max_tokens:.0f} words):

SCENE TO WRITE:
{modified_scene_description}

STORY BIBLE (for consistency):
{story_bible}

SCENE CONTEXT: Scene {scene_number} of {total_scenes}{context_info}{story_requirements_reminder}

WRITING REQUIREMENTS:
- Write a detailed, engaging scene of approximately {max_tokens * 0.75:.0f} words
- Include rich dialogue and character interactions
- Provide vivid descriptions of settings, actions, and emotions
- Show the key events and conversations for this scene
- Write detailed internal thoughts and character psychology
- Use sensory details and atmospheric descriptions
- Expand story moments into full dramatic sequences
- Think of this as a substantial scene that advances the plot

Write an engaging, detailed scene that:
- Brings this moment to life with vivid description
- Maintains consistency with established characters and world
- Advances the plot through events and interactions
- Develops characters through dialogue and actions
- Uses compelling narrative prose throughout
- Fits naturally with the overall story tone and style
- FOLLOWS THE EXACT PRONOUN USAGE specified above (this is critical!)
- INCLUDES any mandatory events if they belong in this scene

CRITICAL: Write until you have created a rich, detailed narrative experience."""
        
        # Make API call with debug info
        print(f"   🔧 Sending {max_tokens:,} tokens to Ollama API...")
        response = self.api_handler.make_api_call_with_system_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=max_tokens,
            stage="scene_writing"
        )
        
        if response:
            actual_words = len(response.split())
            expected_words = max_tokens * 0.75
            print(f"   ✅ Scene {scene_number} completed: {actual_words:,} words (expected ~{expected_words:.0f})")
            if actual_words < max_tokens * 0.3:  # Much shorter than expected
                print(f"   ⚠️ Scene much shorter than expected - check Ollama model limits")
        
        # RETURN BOTH CONTENT AND PROMPTS
        return {
            'content': response,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }

    def generate_scene(self, scene_description, story_bible, scene_plan, scene_number, total_scenes):
        """Original method - returns only content for backward compatibility"""
        result = self.generate_scene_with_prompts(scene_description, story_bible, scene_plan, scene_number, total_scenes)
        return result['content'] if result else None
    
    def _calculate_scene_tokens(self):
        """Calculate tokens per scene using new SCENE_TOKENS system"""
        if hasattr(self.api_handler, 'llm_settings'):
            # Check if app has scene token settings
            app_settings = getattr(self.api_handler, 'app_settings', None)
            if app_settings:
                scene_size = getattr(app_settings, 'scene_size', 'normal_scene')
                if scene_size in self.SCENE_TOKENS:
                    max_tokens = self.SCENE_TOKENS[scene_size]
                    print(f"   🎯 Using {scene_size}: {max_tokens:,} tokens (~{max_tokens * 0.75:.0f} words)")
                    return max_tokens
                elif scene_size == 'custom':
                    custom_tokens = getattr(app_settings, 'custom_scene_tokens', self.SCENE_TOKENS['normal_scene'])
                    print(f"   🎯 Using custom: {custom_tokens:,} tokens (~{custom_tokens * 0.75:.0f} words)")
                    return custom_tokens
            
            # Fallback: try old auto calculation but with limits
            total_tokens = self.api_handler.llm_settings.get('max_tokens', 4000)
            calculated_tokens = min(total_tokens // 8, self.SCENE_TOKENS['epic_scene'])
            
            # Make sure it's at least a reasonable minimum
            calculated_tokens = max(calculated_tokens, self.SCENE_TOKENS['short_scene'])
            
            print(f"   🎯 Using fallback calculation: {calculated_tokens:,} tokens (~{calculated_tokens * 0.75:.0f} words)")
            return calculated_tokens
        else:
            # Ultimate fallback
            fallback_tokens = self.SCENE_TOKENS['normal_scene']
            print(f"   ⚠️ Using default: {fallback_tokens:,} tokens (~{fallback_tokens * 0.75:.0f} words)")
            return fallback_tokens
    
    def _build_story_requirements_reminder(self):
        """Build story requirements reminder text"""
        story_requirements_reminder = ""
        if self.story_intent_config.configured_intent:
            story_requirements_reminder = "\n\nCRITICAL WRITING INSTRUCTIONS:\n"
            
            # STRONG Narrative style enforcement
            if "narrative_style" in self.story_intent_config.configured_intent:
                style = self.story_intent_config.configured_intent["narrative_style"]
                story_requirements_reminder += f"WRITING STYLE: {style}\n"
                
                if "Second Person" in style:
                    story_requirements_reminder += "MANDATORY PRONOUNS:\n"
                    story_requirements_reminder += "- Protagonist: 'I' (never change this)\n" 
                    story_requirements_reminder += "- Love interest: 'you' (NEVER 'she' or 'he')\n"
                    story_requirements_reminder += "- Other characters: 'she', 'he', 'they'\n"
                    story_requirements_reminder += "- WRONG: 'I looked at her' - CORRECT: 'I looked at you'\n"
                    story_requirements_reminder += "- WRONG: 'She smiled' - CORRECT: 'You smiled'\n"
                    story_requirements_reminder += "- Example: 'I watched you move across the room. You were graceful.'\n"
                    
                elif "First Person" in style:
                    story_requirements_reminder += "MANDATORY PRONOUNS:\n"
                    story_requirements_reminder += "- Protagonist: 'I' (never change this)\n"
                    story_requirements_reminder += "- Love interest: 'she/her' or 'he/him' (NOT 'you')\n"
                    story_requirements_reminder += "- Example: 'I watched her move across the room. She was graceful.'\n"
            
            # Custom requirements for this scene
            if "custom_requirements" in self.story_intent_config.configured_intent:
                requirements = self.story_intent_config.configured_intent["custom_requirements"]
                if isinstance(requirements, list):
                    story_requirements_reminder += "\nMANDATORY EVENTS (check if any apply to this scene):\n"
                    for req in requirements:
                        story_requirements_reminder += f"- {req}\n"
                else:
                    story_requirements_reminder += f"\nMANDATORY EVENT: {requirements}\n"
        
        # If no special requirements, return empty string (follow blueprint naturally)
        if not story_requirements_reminder.strip():
            return ""
        
        return story_requirements_reminder