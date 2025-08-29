import os  # ADD THIS
from datetime import datetime

class ScenePlanner:
    def __init__(self, api_handler, story_intent_config, system_prompts, storyboard_folder, perspective_controller=None):
        self.api_handler = api_handler
        self.story_intent_config = story_intent_config
        self.system_prompts = system_prompts
        self.storyboard_folder = storyboard_folder
        self.perspective_controller = perspective_controller
    
    def generate_scene_plan(self, story_bible_content, blueprint_name):
        """Generate scene plan with ENFORCED custom requirements"""
        print("📋 Generating scene plan with specialized system prompt...")
        
        # Get the specialized system prompt for scene planning
        base_system_prompt = self.system_prompts.get('scene_plan', '')
        
        # Add story intent requirements
        intent_addition = self.story_intent_config.get_formatted_intent_for_prompts()
        system_prompt = base_system_prompt + intent_addition
        
        # Build ULTRA-SPECIFIC user prompt that FORCES compliance
        custom_requirements_enforcement = self._build_requirements_enforcement()
        
        # Add perspective instructions if configured
        perspective_instructions = ""
        if self.perspective_controller and self.perspective_controller.selected_perspective != 'default':
            perspective_instructions = self._build_perspective_instructions()

        # FIXED: Build the user_prompt (this was missing the "user_" part)
        user_prompt = f"""Create a scene-by-scene plan based on this story bible:

{story_bible_content}{custom_requirements_enforcement}{perspective_instructions}

SCENE PLANNING RULES:
1. Follow the mandatory requirements above EXACTLY - they override everything else
2. If a requirement specifies a location, use that exact location
3. If a requirement specifies an action, include that exact action
4. Build the rest of the story around these mandatory elements
5. If no specific requirements exist, follow the story bible naturally

FORMAT REQUIREMENT - Use this EXACT format:

SCENE 1: [Title - must reflect any mandatory requirements for this scene]
Setting: [Location appropriate to the story]  
Key Events: [What happens - include mandatory events if specified]
Requirements Met: [List specific requirements fulfilled, or "None" if no specific requirements]

SCENE 2: [Title]
Setting: [Location]
Key Events: [What happens]
Requirements Met: [Any requirements for this scene, or "None"]

Continue this pattern. Do NOT use ## or ** formatting - use simple "SCENE X:" headers.

Create a complete scene breakdown that tells the full story from beginning to end."""
    
        # NEW: Use token distribution settings from app
        max_tokens = 2500  # fallback default
    
        if hasattr(self.api_handler, 'llm_settings'):
            # Check if app has token distribution settings
            app_settings = getattr(self.api_handler, 'app_settings', None)
            if app_settings:
                # Use app's token distribution settings
                if getattr(app_settings, 'scene_plan_tokens_mode', 'auto') == 'auto':
                    total_tokens = self.api_handler.llm_settings.get('max_tokens', 2500)
                    max_tokens = min(total_tokens // 12, 10000)
                    print(f"   🎯 Using {max_tokens:,} tokens for scene planning (auto: {total_tokens:,} ÷ 12)")
                else:
                    max_tokens = getattr(app_settings, 'manual_plan_tokens', 10000)
                    print(f"   🎯 Using {max_tokens:,} tokens for scene planning (manual setting)")
            else:
                # Fallback to old auto calculation
                total_tokens = self.api_handler.llm_settings.get('max_tokens', 2500)
                max_tokens = min(total_tokens // 12, 10000)
                print(f"   🎯 Using {max_tokens:,} tokens for scene planning (auto fallback)")
        else:
            print(f"   ⚠️ Using fallback {max_tokens} tokens (no LLM settings found)")
    
        # Make API call with the correctly named user_prompt variable
        response = self.api_handler.make_api_call_with_system_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,  # ✅ Now this variable is properly defined
            max_tokens=max_tokens,
            stage="scene_plan"
        )
        
        if not response:
            print("❌ Failed to generate scene plan")
            return None
        
        # Save scene plan
        plan_filename = f"{blueprint_name.replace('.story.txt', '')}_plan.txt"
        plan_path = os.path.join(self.storyboard_folder, plan_filename)
        
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(f"SCENE PLAN - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")
            f.write(response)
        
        print(f"   ✓ Scene plan saved: {plan_filename}")
        return response
    
    def _build_requirements_enforcement(self):
        """Build custom requirements enforcement text"""
        custom_requirements_enforcement = ""
        if "custom_requirements" in self.story_intent_config.configured_intent:
            requirements = self.story_intent_config.configured_intent["custom_requirements"]
            if isinstance(requirements, list):
                custom_requirements_enforcement = "\n\n" + "="*80 + "\n"
                custom_requirements_enforcement += "MANDATORY REQUIREMENTS - THESE OVERRIDE THE STORY BIBLE IF NEEDED:\n"
                custom_requirements_enforcement += "="*80 + "\n"
                for i, req in enumerate(requirements, 1):
                    custom_requirements_enforcement += f"REQUIREMENT {i}: {req}\n"
                    
                    # Try to identify which scene this applies to
                    if "first scene" in req.lower() or "scene 1" in req.lower():
                        custom_requirements_enforcement += f"   → MUST be implemented in SCENE 1\n"
                    elif "second scene" in req.lower() or "scene 2" in req.lower():
                        custom_requirements_enforcement += f"   → MUST be implemented in SCENE 2\n"
                    elif "final scene" in req.lower() or "last scene" in req.lower():
                        custom_requirements_enforcement += f"   → MUST be implemented in the FINAL SCENE\n"
                    else:
                        custom_requirements_enforcement += f"   → MUST be implemented in an appropriate scene\n"
                
                custom_requirements_enforcement += "="*80 + "\n"
                custom_requirements_enforcement += "CRITICAL INSTRUCTIONS:\n"
                custom_requirements_enforcement += "- These requirements OVERRIDE any conflicting elements in the story bible\n"
                custom_requirements_enforcement += "- Follow the exact locations and actions specified in requirements\n"
                custom_requirements_enforcement += "- Do NOT change or interpret these requirements - follow them exactly\n"
                custom_requirements_enforcement += "- If no specific requirements exist, follow the story bible naturally\n"
                custom_requirements_enforcement += "="*80 + "\n"
        
        return custom_requirements_enforcement
    
    def _build_perspective_instructions(self):
        """Build perspective-specific instructions"""
        # ... your existing method ...