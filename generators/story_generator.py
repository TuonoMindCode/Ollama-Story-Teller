from .api_handler import APIHandler
from .prompt_logger import PromptLogger
from .generation_stats import GenerationStats
from .perspective_controller import PerspectiveController
from .story_validator import StoryValidator
from .story_bible_generator import StoryBibleGenerator
from .scene_planner import ScenePlanner
from .scene_writer import SceneWriter

from database.story_context import AutoStoryContext
import os
import json
import time
from datetime import datetime
from .context_tracker import ContextTracker
from .story_intent_config import StoryIntentConfigurator
from blueprint_processor import BlueprintProcessor

class StoryGenerator:
    def __init__(self, blueprint_file, stories_folder, storyboard_folder, ollama_settings):
        
        # Store basic settings
        self.blueprint_file = blueprint_file
        self.stories_folder = stories_folder
        self.storyboard_folder = storyboard_folder
        self.stats_folder = ollama_settings.get('stats_folder', 'multiscene/stats')  # ADD THIS LINE
        self.ollama_settings = ollama_settings

        # Add blueprint processor
        self.blueprint_processor = BlueprintProcessor(ollama_settings)
        
        # Initialize properties that may be set later
        self.narrative_consistency = ollama_settings.get('narrative_consistency', 'auto_tracking')
        self.content_settings = ollama_settings.get('content_settings', {})
        self.language_settings = ollama_settings.get('language_settings', {})
        self.story_intent = ollama_settings.get('story_intent')
        self.system_prompts = ollama_settings.get('system_prompts', {})
        self.blueprint_folder = ollama_settings.get('blueprint_folder', 'blueprints')
        self.app_settings = ollama_settings.get('app_settings', {})
        
        # Extract app settings for prompt logging
        self.app_settings = ollama_settings.get('app_settings', {})
        
        # Clean LLM settings (remove non-LLM specific settings)
        self.clean_llm_settings = {
            'model': ollama_settings.get('model'),
            'max_tokens': ollama_settings.get('max_tokens', 4096),
            'temperature': ollama_settings.get('temperature', 0.8),
            'top_p': ollama_settings.get('top_p', 0.9),
            'top_k': ollama_settings.get('top_k', 40),
            'repeat_penalty': ollama_settings.get('repeat_penalty', 1.1),
            'seed': ollama_settings.get('seed')
        }
        
        # Initialize perspective controller
        self.perspective_controller = PerspectiveController()
        
        # Initialize location tracker for auto-tracking mode - UPDATED COMMENT
        self.context_tracker = None
        if self.narrative_consistency == "auto_tracking":
            self.context_tracker = ContextTracker()
        
        # Story intent configuration
        self.story_intent_config = self.story_intent or StoryIntentConfigurator()
        
        # Initialize all the specialized modules
        self.prompt_logger = PromptLogger(
            self.stories_folder, 
            self.clean_llm_settings,
            app_settings=self.app_settings
        )
        self.api_handler = APIHandler(self.clean_llm_settings, self.prompt_logger)
        self.generation_stats = GenerationStats()
        self.story_validator = StoryValidator(self.story_intent_config)
        
        # Generators that depend on the above
        self.bible_generator = StoryBibleGenerator(
            self.api_handler, self.story_intent_config, self.system_prompts, self.storyboard_folder
        )
        self.scene_planner = ScenePlanner(
            self.api_handler, self.story_intent_config, self.system_prompts, 
            self.storyboard_folder, self.perspective_controller
        )
        self.scene_writer = SceneWriter(
            self.api_handler, self.story_intent_config, self.system_prompts, 
            self.context_tracker, self.perspective_controller
        )
        
        print(f"🎬 StoryGenerator initialized with {len(self.system_prompts)} system prompts")
        if self.perspective_controller:
            print("🎭 Perspective control available")
    
    def configure_story_intent(self):
        """Configure story intent interactively"""
        return self.story_intent_config.configure_interactive()
    
    def configure_perspective(self, blueprint_content):
        """🎭 NEW: Configure perspective options"""
        return self.perspective_controller.configure_perspective(blueprint_content)
    
    def generate_complete_story(self, blueprint_name, story_number=1):
        """Generate complete story using all specialized modules"""
        print(f"\n🎬 GENERATING COMPLETE STORY #{story_number}")
        print("="*50)
        
        # Load and process blueprint
        blueprint_path = os.path.join(self.blueprint_folder, blueprint_name)
        if not os.path.exists(blueprint_path):
            print(f"❌ Blueprint not found: {blueprint_name}")
            return None, None

        with open(blueprint_path, 'r', encoding='utf-8') as f:
            original_blueprint = f.read()

        # Apply gender swap if configured
        gender_swap_mode = self.ollama_settings.get('gender_swap_mode', 'none')
        if gender_swap_mode != "none":
            print(f"🔄 Applying gender swap: {gender_swap_mode}")
            blueprint_content = self.blueprint_processor.process_blueprint(original_blueprint, gender_swap_mode)
        else:
            blueprint_content = original_blueprint

        print(f"📋 Using blueprint: {blueprint_name}")
        
        # Phase 1: Generate story bible (use processed blueprint)
        bible_start = time.time()
        story_bible = self.bible_generator.generate_story_bible(
            blueprint_content, blueprint_name, self.content_settings, self.language_settings
        )
        bible_time = time.time() - bible_start
        print(f"   ⏱️ Story bible generated in {bible_time:.1f}s")
        
        if not story_bible:
            return None, None

        # Phase 2: Generate scene plan  
        plan_start = time.time()  
        scene_plan = self.scene_planner.generate_scene_plan(story_bible, blueprint_name)
        plan_time = time.time() - plan_start
        print(f"   ⏱️ Scene plan generated in {plan_time:.1f}s")
        
        if not scene_plan:
            return None, None

        # Validate custom requirements
        self.story_validator.validate_custom_requirements_in_plan(scene_plan)

        # Phase 3: Generate all scenes
        scenes = self.story_validator.extract_scenes_from_plan(scene_plan)
        if not scenes:
            print("❌ No scenes found in scene plan")
            return None, None

        # Set up progress tracking
        self.generation_stats.start_generation(len(scenes))
        
        print(f"📝 Writing {len(scenes)} scenes...")
        self.generation_stats.show_progress()
        
        # CHANGED: Store clean story content WITH scene numbers for readability
        clean_story_scenes = []  # Store scenes with their numbers for the story file
        detailed_scene_info = []  # Scene metadata with prompts instead of content
    
        for i, scene_desc in enumerate(scenes, 1):
            scene_start = time.time()
            
            # Try new method first, fall back to old method if it doesn't exist
            try:
                scene_result = self.scene_writer.generate_scene_with_prompts(
                    scene_desc, story_bible, scene_plan, i, len(scenes)
                )
                if scene_result and scene_result.get('content'):
                    scene_content = scene_result['content']
                    system_prompt = scene_result.get('system_prompt', 'System prompt not captured')
                    user_prompt = scene_result.get('user_prompt', 'User prompt not captured')
                else:
                    scene_content = None
                    system_prompt = 'Method failed'
                    user_prompt = 'Method failed'
            except AttributeError:
                # Fallback to old method if new method doesn't exist yet
                scene_content = self.scene_writer.generate_scene(
                    scene_desc, story_bible, scene_plan, i, len(scenes)
                )
                system_prompt = 'Old method used - prompts not captured'
                user_prompt = 'Old method used - prompts not captured'
            
            scene_time = time.time() - scene_start
            
            if scene_content:
                # Calculate scene stats
                word_count = len(scene_content.split())
                char_count = len(scene_content)
                
                # Update progress tracking
                self.generation_stats.complete_scene(scene_time, word_count, char_count)
                
                # Show scene completion stats
                self.generation_stats.show_scene_completion(i, scene_time, word_count, char_count)
                
                # Show overall progress
                self.generation_stats.show_progress()
                
                # MODIFIED: Add scene header to content for story file
                scene_with_header = f"Scene {i}\n\n{scene_content}"
                clean_story_scenes.append(scene_with_header)
                
                # METADATA: Store detailed scene info with PROMPTS instead of content
                scene_metadata = {
                    'scene_number': i,
                    'completed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'word_count': word_count,
                    'char_count': char_count,
                    'generation_time': scene_time,
                    'system_prompt': system_prompt,
                    'user_prompt': user_prompt,
                }
                detailed_scene_info.append(scene_metadata)
                
            else:
                print(f"❌ Failed to generate scene {i}")
                return None, None

        # Show final statistics
        total_time = time.time() - self.generation_stats.stats['start_time']
        self.generation_stats.show_final_stats(total_time)
        
        # Join story scenes with headers and separators
        complete_story_with_scenes = "\n\n" + "="*50 + "\n\n".join(clean_story_scenes) + "\n\n" + "="*50
        
        # Generate or get story title
        story_title = self._generate_or_get_story_title(complete_story_with_scenes, blueprint_name)
        
        # Save story file with scene headers
        story_filename = self._save_clean_story_file(complete_story_with_scenes, story_title, blueprint_name, story_number)
        
        # Save detailed metadata file with all scene stats and prompts
        metadata_filename = self._save_detailed_metadata_file(blueprint_name, story_number, story_title, detailed_scene_info)
        
        print(f"✅ Clean story saved: {story_filename}")
        print(f"📊 Detailed metadata saved to stats: {metadata_filename}")
        
        # Show logging information if enabled
        if self.prompt_logger and self.prompt_logger.logging_enabled and self.prompt_logger.prompt_log_file:
            log_filename = os.path.basename(self.prompt_logger.prompt_log_file)
            logs_dir = os.path.dirname(self.prompt_logger.prompt_log_file)
            print(f"📝 Prompt log saved: {log_filename}")
            print(f"📁 Log location: {logs_dir}")
        
        return story_filename, self.context_tracker

    def _save_detailed_metadata_file(self, blueprint_name, story_number, story_title, detailed_scene_info):
        """Save detailed metadata file with scene statistics and prompts used"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create metadata filename
        safe_title = "".join(c for c in story_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        
        metadata_filename = f"{safe_title}_{timestamp}_v{story_number}_DETAILED.txt"
        metadata_path = os.path.join(self.stats_folder, metadata_filename)
        
        # Ensure stats folder exists
        os.makedirs(self.stats_folder, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"DETAILED STORY METADATA - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Story Title: {story_title}\n")
            f.write(f"Blueprint: {blueprint_name}\n")
            f.write(f"Version: {story_number}\n")
            f.write("="*60 + "\n\n")
            
            # Write story metadata
            existing_metadata = self._build_story_metadata(blueprint_name)
            f.write(existing_metadata)
            
            # Write overall statistics
            total_words = sum(scene['word_count'] for scene in detailed_scene_info)
            total_chars = sum(scene['char_count'] for scene in detailed_scene_info)
            total_time = sum(scene['generation_time'] for scene in detailed_scene_info)
            
            f.write(f"\nOVERALL STATISTICS:\n")
            f.write(f"Total Scenes: {len(detailed_scene_info)}\n")
            f.write(f"Total Words: {total_words:,}\n")
            f.write(f"Total Characters: {total_chars:,}\n")
            f.write(f"Total Generation Time: {self.generation_stats._format_time(total_time)}\n")
            f.write(f"Average Words per Scene: {total_words/len(detailed_scene_info):.1f}\n")
            
            # MODIFIED: Write detailed scene breakdown with PROMPTS instead of full content
            f.write(f"\n{'='*60}\n")
            f.write("DETAILED SCENE BREAKDOWN WITH PROMPTS USED\n")
            f.write("="*60 + "\n\n")
            
            for scene in detailed_scene_info:
                f.write(f"=== SCENE {scene['scene_number']} ===\n")
                f.write(f"Completed at: {scene['completed_at']}\n")
                f.write(f"Word count: {scene['word_count']:,} words\n")
                f.write(f"Character count: {scene['char_count']:,} characters\n")
                f.write(f"Generation time: {scene['generation_time']:.1f}s\n")
                f.write("-" * 50 + "\n\n")
                
                # NEW: Write system prompt
                f.write("SYSTEM PROMPT:\n")
                f.write(scene['system_prompt'])
                f.write("\n\n")
                
                # NEW: Write user prompt  
                f.write("USER PROMPT:\n")
                f.write(scene['user_prompt'])
                f.write("\n\n")
                
                f.write("=" * 80 + "\n\n")  # Scene separator
    
        return metadata_filename

    def _build_story_metadata(self, blueprint_name):
        """Build comprehensive story metadata for the file header"""
        metadata = ""
        
        # System prompts info
        metadata += f"System Prompts: {'ENABLED' if self.system_prompts else 'DISABLED'}\n"
        
        # Perspective info
        if hasattr(self, 'perspective_controller') and self.perspective_controller.selected_perspective != 'default':
            metadata += f"Perspective: {self.perspective_controller.selected_perspective.replace('_', ' ').title()}\n"
            
            if self.perspective_controller.selected_perspective == 'alternating':
                metadata += f"POV Schedule: {self.perspective_controller.pov_schedule}\n"
        
        # Story intent info
        if hasattr(self, 'story_intent_config') and self.story_intent_config.configured_intent:
            intent_summary = []
            
            if "narrative_style" in self.story_intent_config.configured_intent:
                intent_summary.append(f"Style: {self.story_intent_config.configured_intent['narrative_style']}")
            
            if "custom_requirements" in self.story_intent_config.configured_intent:
                reqs = self.story_intent_config.configured_intent["custom_requirements"]
                req_count = len(reqs) if isinstance(reqs, list) else 1
                intent_summary.append(f"Custom Requirements: {req_count}")
            
            if intent_summary:
                metadata += f"Story Intent: {', '.join(intent_summary)}\n"
        
        # Content settings
        if hasattr(self, 'content_settings') and self.content_settings:
            content_info = []
            if self.content_settings.get('content_rating', 'auto') != 'auto':
                content_info.append(f"Rating: {self.content_settings['content_rating']}")
            if self.content_settings.get('story_tone', 'auto') != 'auto':
                content_info.append(f"Tone: {self.content_settings['story_tone']}")
            
            if content_info:
                metadata += f"Content: {', '.join(content_info)}\n"
        
        return metadata

    def _generate_or_get_story_title(self, story_content, blueprint_name):
        """Generate story title using Ollama or use custom title"""
        # Check if custom title was set
        if hasattr(self, 'custom_story_title') and self.custom_story_title:
            print(f"📖 Using custom title: \"{self.custom_story_title}\"")
            return self.custom_story_title
        
        # Auto-generate title using Ollama
        print("🤖 Auto-generating story title with Ollama...")
        
        # Extract first 1500 characters for title generation (enough context, not too much)
        story_preview = story_content[:1500] if len(story_content) > 1500 else story_content
        # Remove scene headers and metadata for cleaner preview
        clean_preview = self._clean_story_preview(story_preview)

        title_prompt = f"""Based on this story beginning, create a compelling and appropriate title:

{clean_preview}

Requirements:
- Create only the title, nothing else
- No quotes around the title
- Make it engaging and capture the story's essence
- Keep it concise (2-8 words typically)
- Match the genre and tone of the story"""

        try:
            title = self.api_handler.make_api_call_with_system_prompt(
                system_prompt="You are an expert at creating compelling story titles. You always respond with just the title and nothing else - no quotes, no explanations, no additional text.",
                user_prompt=title_prompt,
                max_tokens=20,  # Short response for just a title
                stage="title_generation"
            )
            
            if title and title.strip():
                # Clean up the title (remove quotes, extra whitespace, newlines)
                clean_title = title.strip().strip('"').strip("'").strip().replace('\n', ' ').strip()
                
                # Validate title length
                if len(clean_title) > 100:
                    clean_title = clean_title[:100].strip()
                
                if clean_title:
                    print(f"✅ Generated title: \"{clean_title}\"")
                    return clean_title
            
            # If we get here, title generation failed
            fallback_title = self._create_fallback_title(blueprint_name)
            print(f"⚠️ Title generation failed, using fallback: \"{fallback_title}\"")
            return fallback_title
                
        except Exception as e:
            print(f"⚠️ Title generation error: {e}")
            fallback_title = self._create_fallback_title(blueprint_name)
            print(f"⚠️ Using fallback title: \"{fallback_title}\"")
            return fallback_title

    def _clean_story_preview(self, preview):
        """Clean story preview for title generation"""
        # Remove scene headers like "=== SCENE 1 ==="
        import re
        cleaned = re.sub(r'=== SCENE \d+ ===\n.*?\n.*?\n.*?\n-+\n*', '', preview)
        cleaned = re.sub(r'\n+', '\n', cleaned)  # Remove extra newlines
        return cleaned.strip()

    def _create_fallback_title(self, blueprint_name):
        """Create fallback title from blueprint name"""
        # Extract genre from blueprint name for fallback
        name_lower = blueprint_name.lower()
        
        if 'romance' in name_lower:
            return "Hearts Entwined"
        elif 'mystery' in name_lower or 'detective' in name_lower:
            return "The Investigation"
        elif 'thriller' in name_lower:
            return "Edge of Danger"
        elif 'fantasy' in name_lower:
            return "Realm of Magic"
        elif 'horror' in name_lower:
            return "Shadows and Fear"
        elif 'western' in name_lower:
            return "Frontier Tales"
        elif 'comedy' in name_lower:
            return "Laughing Matters"
        else:
            return "An Untold Story"

    def _save_clean_story_file(self, story_content, story_title, blueprint_name, story_number):
        """Save story file with scene headers for better readability"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create clean filename from title
        safe_title = "".join(c for c in story_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]  # Limit length
        
        story_filename = f"{safe_title}_{timestamp}_v{story_number}.txt"
        story_path = os.path.join(self.stories_folder, story_filename)
        
        # Create content with title and organized scenes
        clean_content = f"{story_title}\n\n{story_content}"
        
        with open(story_path, 'w', encoding='utf-8') as f:
            f.write(clean_content)
        
        return story_filename

    def generate_story(self):
        """Generate a complete story using the blueprint"""
        try:
            # Load the original blueprint
            blueprint_path = os.path.join("blueprints", self.blueprint_file)
            if not os.path.exists(blueprint_path):
                raise FileNotFoundError(f"Blueprint file not found: {blueprint_path}")
            
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                original_blueprint = f.read()
            
            # Apply gender swap if configured
            gender_swap_mode = self.ollama_settings.get('gender_swap_mode', 'none')
            processed_blueprint = self.blueprint_processor.process_blueprint(
                original_blueprint, 
                gender_swap_mode
            )
            
            # Use processed blueprint for story generation
            self.blueprint_content = processed_blueprint
            
            # Continue with existing story generation logic...
            print(f"Generating story from blueprint: {self.blueprint_file}")
            if gender_swap_mode != "none":
                print(f"Applied gender swap mode: {gender_swap_mode}")
            
            # Generate story bible
            story_bible = self._generate_story_bible()
            
            # ... rest of existing generate_story method ...
            
        except Exception as e:
            print(f"Error generating story: {e}")
            return None

    def _generate_story_bible(self):
        """Generate story bible from processed blueprint"""
        # Use self.blueprint_content (which is now the processed version)
        # ... rest of existing story bible generation logic unchanged ...
        pass

    def read_blueprint_settings(self, blueprint_path):
        """Read token settings and other config from blueprint file"""
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract max tokens from blueprint
            max_tokens = 8192  # default
            if "Max tokens used:" in content:
                import re
                match = re.search(r'Max tokens used: ([\d,]+)', content)
                if match:
                    max_tokens = int(match.group(1).replace(',', ''))
            
            return {
                'max_tokens': max_tokens,
                # Add other settings as needed
            }
        except Exception as e:
            print(f"⚠️ Could not read blueprint settings: {e}")
            return {'max_tokens': 8192}
    
    # Legacy methods for backward compatibility (simplified)
    def generate_story_bible(self, blueprint_content, blueprint_name):
        """Legacy method - delegates to bible_generator"""
        return self.bible_generator.generate_story_bible(
            blueprint_content, blueprint_name, self.content_settings, self.language_settings
        )
    
    def generate_scene_plan(self, story_bible_content, blueprint_name):
        """Legacy method - delegates to scene_planner"""
        return self.scene_planner.generate_scene_plan(story_bible_content, blueprint_name)
    
    def generate_scene(self, scene_description, story_bible, scene_plan, scene_number, total_scenes):
        """Legacy method - delegates to scene_writer"""
        # ✅ FIXED: Remove the extra parameters that were causing the error
        return self.scene_writer.generate_scene(
            scene_description, story_bible, scene_plan, scene_number, total_scenes
            # ❌ REMOVED: The old code was trying to pass extra parameters
        )