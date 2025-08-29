import os
import time
from .story_utils import StoryUtils

class BibleGenerator:
    """Handles Phase 1: Story Bible Creation"""
    
    def __init__(self, blueprint_folder, storyboard_folder, llm_settings, reuse_mode="new"):
        self.blueprint_folder = blueprint_folder
        self.storyboard_folder = storyboard_folder
        self.llm_settings = llm_settings
        self.reuse_mode = reuse_mode
    
    def estimate_bible_generation_time(self, blueprint_length, has_user_elements=False):
        """Estimate time needed for bible generation based on blueprint complexity"""
        # Base time estimates (in seconds)
        base_time = 25  # Minimum time for simple bible
        
        # Add time based on blueprint complexity
        blueprint_tokens = StoryUtils.estimate_tokens(str(blueprint_length))
        complexity_time = blueprint_tokens / 150  # More complex blueprint = more time
        
        # Add extra time if user elements need to be incorporated
        user_element_time = 15 if has_user_elements else 0
        
        estimated = base_time + complexity_time + user_element_time
        return min(estimated, 180)  # Cap at 3 minutes
    
    def create_story_bible(self, blueprint_name, run_number):
        """Phase 1: Create detailed story bible"""
        story_name = blueprint_name.replace('.story.txt', '')
        bible_path = os.path.join(self.storyboard_folder, f"{story_name}.storyboard.story.txt")
        
        # Check reuse mode for story bible
        if self.reuse_mode in ["bible_only", "both"] and os.path.exists(bible_path):
            print(f"  ✓ Reusing existing story bible: {bible_path}")
            bible_size = os.path.getsize(bible_path)
            print(f"  📊 Existing file size: {bible_size:,} bytes")
            print(f"  ⏱️  Phase 1 completed instantly (reused existing file)")
            return bible_path
        
        # Read blueprint and check for user elements
        story_template_path = os.path.join(self.blueprint_folder, blueprint_name)
        story_template = StoryUtils.read_file(story_template_path)
        if not story_template:
            print(f"  ❌ Error: Could not read {blueprint_name}")
            return None
        
        # Check for custom user elements
        user_file = blueprint_name.replace('.story.txt', '.story.user.txt')
        user_path = os.path.join(self.blueprint_folder, user_file)
        user_elements = StoryUtils.read_file(user_path)
        
        # Show phase statistics
        estimated_time = self.estimate_bible_generation_time(len(story_template), bool(user_elements))
        StoryUtils.show_phase_statistics(1, "Story Bible Creation", estimated_time)
        
        phase_start = time.time()
        
        # Create new story bible (either mode is "new" or file doesn't exist)
        if self.reuse_mode == "new" and os.path.exists(bible_path):
            # Create new version with run number
            bible_path = os.path.join(self.storyboard_folder, f"{story_name}.storyboard.story.run{run_number:02d}.txt")
            print(f"  📝 Creating new version: run{run_number:02d}")
        
        print(f"  📋 Blueprint: {blueprint_name} ({len(story_template):,} chars)")
        
        # Create user prompt
        user_prompt = f"Create a detailed story bible using this template:\n\n{story_template}"
        
        if user_elements:
            user_prompt += f"\n\nIMPORTANT: Include these specific elements in your story:\n{user_elements}\n\nMake sure to incorporate all the custom elements while following the template structure."
            print(f"  ✓ Found custom user elements ({len(user_elements):,} chars)")
            print("    🎯 Will incorporate custom elements into story bible")
        
        # Generate story bible with base system prompt
        system_prompt = "You are an expert story planner. Create a comprehensive story bible with all characters, plot elements, clues, suspects, motives, and timeline. Be detailed and specific."
        
        story_bible = StoryUtils.call_ollama(
            self.llm_settings, 
            system_prompt, 
            user_prompt, 
            self.blueprint_folder, 
            blueprint_name,
            "Story Bible Generation"
        )
        
        if story_bible.startswith("Error:"):
            print(f"  ❌ Failed to generate story bible: {story_bible}")
            return None
        
        # Analyze generated bible
        bible_words = len(story_bible.split())
        bible_chars = len(story_bible)
        
        # Save story bible
        if StoryUtils.write_file(bible_path, story_bible):
            phase_duration = time.time() - phase_start
            print(f"\n  ✅ Phase 1 completed!")
            print(f"  📁 Story bible saved: {bible_path}")
            print(f"  ⏱️  Total phase time: {StoryUtils.format_duration(phase_duration)}")
            print(f"  📊 Bible stats: {bible_words:,} words | {bible_chars:,} characters")
            
            # Quality indicators
            if bible_words > 1000:
                print(f"  🎯 Quality: Comprehensive bible (excellent detail level)")
            elif bible_words > 500:
                print(f"  🎯 Quality: Detailed bible (good detail level)")
            else:
                print(f"  ⚠️  Quality: Brief bible (may need more detail)")
            
            return bible_path
        else:
            return None