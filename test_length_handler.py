import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model_testing.length_handler import LengthHandler

# Test the length handler
handler = LengthHandler()

print("Testing Scene Length Selection:")
scene_config = handler.select_content_length('scene')
if scene_config:
    print(f"Selected: {scene_config}")
    max_tokens = handler.get_max_tokens_for_generation(scene_config)
    print(f"Recommended max_tokens: {max_tokens}")

print("\nTesting Story Length Selection:")
story_config = handler.select_content_length('story')
if story_config:
    print(f"Selected: {story_config}")
    max_tokens = handler.get_max_tokens_for_generation(story_config)
    print(f"Recommended max_tokens: {max_tokens}")
