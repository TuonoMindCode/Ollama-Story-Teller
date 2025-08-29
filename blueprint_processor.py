import requests
import json

class BlueprintProcessor:
    """Handles blueprint modifications like gender swapping"""
    
    def __init__(self, ollama_settings):
        self.ollama_settings = ollama_settings
    
    def process_blueprint(self, blueprint_content, gender_swap_mode):
        """Process blueprint with specified modifications"""
        
        # Check for force gender setting first (highest priority)
        force_gender = self.ollama_settings.get('force_protagonist_gender', 'auto')
        if force_gender != 'auto':
            print(f"🎯 Forcing protagonist gender to: {force_gender}")
            return self._force_protagonist_gender(blueprint_content, force_gender)
        
        # Check for perspective controller gender swap
        perspective_controller = self.ollama_settings.get('perspective_controller')
        if perspective_controller and hasattr(perspective_controller, 'selected_perspective'):
            if perspective_controller.selected_perspective == 'gender_swap':
                print("🔄 Applying gender swap via perspective controller")
                return self._apply_smart_gender_swap(blueprint_content, "main_lead")
        
        # Finally check old gender swap mode
        if gender_swap_mode != "none":
            print(f"🔄 Applying gender swap mode: {gender_swap_mode}")
            return self._apply_smart_gender_swap(blueprint_content, gender_swap_mode)
        
        return blueprint_content
    
    def _check_ollama_connection(self):
        """Check if Ollama server is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _apply_smart_gender_swap(self, blueprint_content, swap_mode):
        """Apply intelligent gender swapping using same settings as story generation"""
        
        if swap_mode == "main_lead":
            instruction = """Analyze this story blueprint and perform INTELLIGENT gender swapping of ONLY the main protagonist.

PROCESS:
1. First, identify who the main protagonist is (the character we follow, regardless of current gender)
2. Determine their current gender from context clues
3. Swap ONLY the main protagonist's gender (male→female or female→male)
4. Keep ALL other characters exactly the same gender
5. Adjust relationship dynamics naturally (if protector becomes female, she's still the protector)
6. Update pronouns and gender-specific terms only for the main protagonist

IMPORTANT: Focus on the CHARACTER ROLE, not just pronouns. The story structure stays the same, only the main character's gender changes."""
            
        elif swap_mode == "both_leads":
            instruction = """Analyze this story blueprint and perform INTELLIGENT gender swapping of the TWO main characters.

PROCESS:
1. Identify the main protagonist (the character we follow most)
2. Identify the second most important character (usually romantic interest, antagonist, or deuteragonist)
3. Determine their current genders from context clues
4. Swap BOTH of their genders (male→female, female→male)
5. Keep ALL other supporting characters exactly the same gender
6. Adjust relationship dynamics naturally while preserving their roles
7. Update pronouns and gender-specific terms for these two characters only

IMPORTANT: 
- If it's a romance: male protagonist + female love interest → female protagonist + male love interest
- If it's a thriller: male protagonist + male antagonist → female protagonist + female antagonist
- The CHARACTER ROLES and story structure stay the same, only genders change"""
        
        system_prompt = """You are an expert story analyst and editor who performs intelligent character gender modifications. You understand character roles, story dynamics, and relationship structures.

Your job is to:
1. Analyze the story to identify character roles and relationships
2. Perform precise gender swaps while preserving all story elements
3. Maintain character personalities, motivations, and story functions
4. Keep the exact same plot, settings, and story structure
5. Only change what's necessary for the gender swap to work naturally"""

        user_prompt = f"""{instruction}

ORIGINAL BLUEPRINT:
{blueprint_content}

Return the modified blueprint with intelligent gender swaps applied. Maintain the exact same format and structure, but with the specified characters' genders changed appropriately."""

        try:
            print("🧠 Processing gender swap (this may take several minutes like story generation)...")
            
            # Use the SAME settings as story generation - no timeout
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.ollama_settings['model'],
                    "system": system_prompt,
                    "prompt": user_prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.ollama_settings.get('temperature', 0.8),  # Use same as story
                        "top_p": self.ollama_settings.get('top_p', 0.9),
                        "top_k": self.ollama_settings.get('top_k', 40),
                        "repeat_penalty": self.ollama_settings.get('repeat_penalty', 1.1),
                        "num_predict": self.ollama_settings.get('max_tokens', 4096)  # Use same as story
                    }
                }
                # NO timeout parameter - let it take as long as it needs, just like story generation
            )
            
            if response.status_code == 200:
                result = response.json()
                modified_blueprint = result.get('response', blueprint_content)
                print("✅ Smart gender swap applied to blueprint")
                return modified_blueprint
            else:
                print(f"❌ Error processing blueprint: {response.status_code}")
                return blueprint_content
                
        except Exception as e:
            print(f"❌ Error applying gender swap: {e}")
            print("   Using original blueprint without gender swap.")
            return blueprint_content

    def _force_protagonist_gender(self, blueprint_content, target_gender):
        """Force the protagonist to be a specific gender"""
        
        if not self._check_ollama_connection():
            print("❌ Ollama server not running. Using original blueprint.")
            return blueprint_content
        
        instruction = f"""Rewrite this story blueprint to make the main protagonist {target_gender}.

PROCESS:
1. Identify who the main protagonist is (the character we follow most)
2. Change the protagonist to be {target_gender} regardless of current gender
3. Keep ALL other characters exactly the same
4. Adjust pronouns, names, and descriptions for the protagonist only
5. Maintain all plot points, relationships, and story structure
6. If needed, adjust gender-specific jobs/backgrounds for realism

IMPORTANT: Only change the protagonist's gender. Keep the story, plot, and all other characters identical."""

        system_prompt = f"""You are a precise story editor. Your job is to modify the protagonist's gender to be {target_gender} while keeping everything else exactly the same. Make natural, appropriate changes to pronouns and descriptions."""

        user_prompt = f"""{instruction}

ORIGINAL BLUEPRINT:
{blueprint_content}

Return the modified blueprint with protagonist gender changed to {target_gender}: """

        try:
            print(f"🧠 Processing protagonist gender change to {target_gender}...")
            
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.ollama_settings['model'],
                    "system": system_prompt,
                    "prompt": user_prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.ollama_settings.get('temperature', 0.8),
                        "top_p": self.ollama_settings.get('top_p', 0.9),
                        "top_k": self.ollama_settings.get('top_k', 40),
                        "repeat_penalty": self.ollama_settings.get('repeat_penalty', 1.1),
                        "num_predict": self.ollama_settings.get('max_tokens', 4096)
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                modified_blueprint = result.get('response', blueprint_content)
                print(f"✅ Protagonist gender forced to {target_gender}")
                return modified_blueprint
            else:
                print(f"❌ Error processing blueprint: {response.status_code}")
                return blueprint_content
                
        except Exception as e:
            print(f"❌ Error forcing gender: {e}")
            return blueprint_content
