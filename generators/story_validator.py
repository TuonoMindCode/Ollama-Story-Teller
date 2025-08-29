class StoryValidator:
    def __init__(self, story_intent_config):
        self.story_intent_config = story_intent_config
    
    def validate_custom_requirements_in_plan(self, scene_plan):
        """Enhanced validation of custom requirements - GENERIC VERSION"""
        if "custom_requirements" not in self.story_intent_config.configured_intent:
            return
            
        requirements = self.story_intent_config.configured_intent["custom_requirements"]
        if not isinstance(requirements, list):
            requirements = [requirements]
    
        print("🔍 Validating custom requirements in scene plan...")
    
        plan_lower = scene_plan.lower()
    
        for i, req in enumerate(requirements, 1):
            print(f"   🔍 Checking requirement {i}: {req}")
        
            # Generic keyword checking - extract key terms from requirement
            req_words = req.lower().split()
            important_words = [word for word in req_words if len(word) > 3 and word not in ['should', 'must', 'have', 'with', 'the', 'and', 'for', 'this', 'that']]
        
            found_words = [word for word in important_words if word in plan_lower]
            missing_words = [word for word in important_words if word not in plan_lower]
        
            if found_words:
                print(f"   ✅ Requirement {i}: Found keywords: {', '.join(found_words)}")
        
            if missing_words:
                print(f"   ⚠️ Requirement {i}: Missing keywords: {', '.join(missing_words)}")
                print(f"      This requirement may not be fully implemented")
    
    def extract_scenes_from_plan(self, scene_plan):
        """Extract individual scene descriptions from scene plan - IMPROVED VERSION"""
        scenes = []
        lines = scene_plan.split('\n')
        current_scene = []
        
        print("🔍 Extracting scenes from plan...")
        print(f"   📄 Plan contains {len(lines)} lines")
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Look for different scene markers - INCLUDING ## format
            scene_markers = [
                'SCENE ',           # Original format: "SCENE 1:"
                '**SCENE ',         # Markdown format: "**SCENE 1:**"
                'Scene ',           # Alternative: "Scene 1:"
                '## SCENE ',        # Header format: "## SCENE 1" ✓ This is what you have
                '###SCENE ',        # Another header format
                'ACT I',            # Sometimes acts are marked
                'ACT II',
                'ACT III'
            ]
            
            # Check if this line starts a new scene
            is_scene_start = any(line_stripped.upper().startswith(marker.upper()) for marker in scene_markers)
            
            if is_scene_start:
                # Save previous scene if we have one
                if current_scene:
                    scene_text = '\n'.join(current_scene).strip()
                    if scene_text:  # Only add non-empty scenes
                        scenes.append(scene_text)
                        print(f"   ✓ Extracted scene {len(scenes)}: {scene_text.split(':')[0] if ':' in scene_text else 'Unnamed'}")
                
                # Start new scene
                current_scene = [line]
                print(f"   🔍 Found scene marker at line {line_num}: {line_stripped[:50]}...")
            elif current_scene:
                # Add to current scene
                current_scene.append(line)
        
        # Don't forget the last scene
        if current_scene:
            scene_text = '\n'.join(current_scene).strip()
            if scene_text:
                scenes.append(scene_text)
                print(f"   ✓ Extracted scene {len(scenes)}: {scene_text.split(':')[0] if ':' in scene_text else 'Final scene'}")
        
        print(f"   📊 Total scenes extracted: {len(scenes)}")
        
        # Show what we extracted for debugging
        if scenes:
            print("   📋 Extracted scenes:")
            for i, scene in enumerate(scenes, 1):
                first_line = scene.split('\n')[0][:60] + "..." if len(scene.split('\n')[0]) > 60 else scene.split('\n')[0]
                print(f"      {i}. {first_line}")
        else:
            print("   ❌ No scenes were extracted")
            print("   🔍 Debugging - first 10 lines of plan:")
            for i, line in enumerate(lines[:10], 1):
                print(f"      {i}: '{line.strip()}'")
        
        return scenes
