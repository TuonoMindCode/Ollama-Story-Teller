import requests
import json
import os
import re
import time
from datetime import datetime, timedelta

class StoryUtils:
    """Shared utilities for story generation components"""
    
    @staticmethod
    def read_file(file_path):
        """Read file content safely"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
    
    @staticmethod
    def write_file(file_path, content):
        """Write content to file safely"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    @staticmethod
    def get_unique_filename(base_path, extension):
        """Generate unique filename if file already exists"""
        if not os.path.exists(base_path):
            return base_path
        
        # File exists, create version with timestamp
        base_name = base_path.replace(extension, '')
        timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
        return f"{base_name}{timestamp}{extension}"
    
    @staticmethod
    def get_base_system_prompt(blueprint_folder, blueprint_name):
        """Get base system prompt for this blueprint if it exists"""
        # Convert detective.story.txt → detective.system.txt
        system_file = blueprint_name.replace('.story.txt', '.system.txt')
        system_path = os.path.join(blueprint_folder, system_file)
        
        base_system = StoryUtils.read_file(system_path)
        if base_system:
            print(f"  ✓ Found base system prompt: {system_file}")
            return base_system
        
        # Fallback to generic system prompt
        return "You are a professional creative writer with expertise in storytelling, character development, and narrative structure."
    
    @staticmethod
    def estimate_tokens(text):
        """Rough estimate of tokens in text (1 token ≈ 4 characters)"""
        return len(text) // 4
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in human-readable format with clear hours/minutes"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:  # Less than 1 hour
            minutes = seconds / 60
            if minutes < 10:
                return f"{minutes:.1f}m"
            else:
                return f"{int(minutes)}m"
        else:  # 1 hour or more
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            
            if remaining_minutes == 0:
                return f"{hours}h"
            else:
                return f"{hours}h {remaining_minutes}m"
    
    @staticmethod
    def call_ollama(llm_settings, system_prompt, user_prompt, blueprint_folder=None, blueprint_name=None, phase_name="Generation"):
        """Call Ollama API with current settings, timing, and progress tracking"""
        print(f"  🔄 {phase_name} in progress...")
        start_time = time.time()
        
        url = "http://localhost:11434/api/generate"
        
        # Get base system prompt and combine it
        if blueprint_folder and blueprint_name:
            base_system = StoryUtils.get_base_system_prompt(blueprint_folder, blueprint_name)
            combined_system = f"{base_system}\n\n{system_prompt}"
        else:
            combined_system = system_prompt
        
        full_prompt = f"System: {combined_system}\n\nUser: {user_prompt}\n\nAssistant:"
        
        # Estimate input tokens
        input_tokens = StoryUtils.estimate_tokens(full_prompt)
        max_tokens = llm_settings['max_tokens']
        
        print(f"    📊 Input: ~{input_tokens:,} tokens | Max output: {max_tokens:,} tokens")
        print(f"    🎛️  Temp: {llm_settings['temperature']} | Top-p: {llm_settings['top_p']} | Model: {llm_settings['model']}")
        
        options = {
            "num_predict": max_tokens,
            "temperature": llm_settings['temperature'],
            "top_p": llm_settings['top_p'],
            "top_k": llm_settings['top_k'],
            "repeat_penalty": llm_settings['repeat_penalty']
        }
        
        if llm_settings['seed'] is not None:
            options["seed"] = llm_settings['seed']
        
        data = {
            "model": llm_settings['model'],
            "prompt": full_prompt,
            "stream": False,
            "options": options
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            
            end_time = time.time()
            duration = end_time - start_time
            
            response_text = result.get("response", "No response generated")
            output_tokens = StoryUtils.estimate_tokens(response_text)
            total_tokens = input_tokens + output_tokens
            
            # Calculate generation speed
            tokens_per_second = output_tokens / duration if duration > 0 else 0
            
            print(f"  ✅ {phase_name} completed!")
            print(f"    ⏱️  Duration: {StoryUtils.format_duration(duration)}")
            print(f"    📈 Output: ~{output_tokens:,} tokens | Total: ~{total_tokens:,} tokens")
            print(f"    🚀 Speed: ~{tokens_per_second:.1f} tokens/sec")
            
            return response_text
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"  ❌ {phase_name} failed after {StoryUtils.format_duration(duration)}")
            return f"Error: {e}"
    
    @staticmethod
    def calculate_max_scenes(max_tokens):
        """Calculate maximum scenes based on available tokens"""
        # Estimate tokens per scene and add buffer for story bible/scene plan processing
        tokens_per_scene = 1500  # Conservative estimate for scene generation
        overhead_tokens = 2000   # Buffer for story bible and scene plan processing
        
        available_for_scenes = max_tokens - overhead_tokens
        max_scenes = max(8, min(30, available_for_scenes // tokens_per_scene))  # Min 8, max 30 scenes
        
        print(f"  📊 Max tokens: {max_tokens:,} → Target scenes: {max_scenes}")
        return max_scenes
    
    @staticmethod
    def show_phase_statistics(phase_number, phase_name, estimated_time=None, scenes_count=None):
        """Show statistics before starting a phase"""
        print(f"\n📋 PHASE {phase_number}: {phase_name.upper()}")
        print("─" * 50)
        
        if estimated_time:
            print(f"  ⏱️  Estimated time: {StoryUtils.format_duration(estimated_time)}")
        
        if scenes_count:
            print(f"  📝 Scenes to process: {scenes_count}")
            if estimated_time and scenes_count:
                time_per_scene = estimated_time / scenes_count
                print(f"  ⚡ Est. time per scene: {StoryUtils.format_duration(time_per_scene)}")
        
        print()