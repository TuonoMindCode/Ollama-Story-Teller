class SystemPromptBuilder:
    @staticmethod
    def build_story_generation_system_prompt(content_settings, narrative_consistency, character_count, stage, blueprint_data=None):
        """Build system prompts that enforce perspective from blueprint"""
        
        # Extract perspective and narrative style from blueprint if available
        perspective = None
        narrative_style = None
        
        if blueprint_data:
            perspective = blueprint_data.get('perspective', 'Not chosen')
            narrative_style = blueprint_data.get('narrative_style', 'Not chosen')
        
        # Base system prompt
        if stage == "story_bible":
            system_prompt = "You are a master world-builder and character developer."
        elif stage == "scene_plan":
            system_prompt = "You are an expert story structure planner."
        elif stage == "scene_writing":
            system_prompt = "You are a skilled narrative prose writer."
        else:
            system_prompt = "You are a professional storyteller."
        
        # CRITICAL: Add perspective enforcement to ALL stages
        if perspective and perspective != 'Not chosen':
            system_prompt += f"\n\n🚨 CRITICAL PERSPECTIVE REQUIREMENT:\n"
            
            if perspective == "First person singular":
                if stage == "story_bible":
                    system_prompt += "When creating character profiles and world details, remember this story will be told in FIRST PERSON from the protagonist's perspective. Focus on what the protagonist would know and experience."
                elif stage == "scene_plan":
                    system_prompt += "When planning scenes, remember this story MUST be told in FIRST PERSON using 'I' statements. Plan scenes from the protagonist's direct experience only."
                elif stage == "scene_writing":
                    system_prompt += "MANDATORY: Write every scene in FIRST PERSON using 'I', 'me', 'my', 'myself'.\n"
                    system_prompt += "- NEVER write 'Sarah walked' - ALWAYS write 'I walked'\n"
                    system_prompt += "- NEVER write 'She felt nervous' - ALWAYS write 'I felt nervous'\n"
                    system_prompt += "- Show only what the protagonist sees, thinks, and feels\n"
                    system_prompt += "- Use internal monologue: 'I wondered...', 'I thought...', 'I felt...'\n"
                    
                    if narrative_style and "Romantic Intimate" in narrative_style:
                        system_prompt += "- Focus heavily on internal romantic thoughts and feelings\n"
                        system_prompt += "- Example: 'My heart skipped when she smiled at me. I wondered if she could tell how nervous I was around her.'\n"
            
            elif perspective == "Third person limited":
                if stage == "scene_writing":
                    system_prompt += "MANDATORY: Write in THIRD PERSON LIMITED following the protagonist closely.\n"
                    system_prompt += "- Use the protagonist's name or pronouns (she/he/they)\n"
                    system_prompt += "- Access only the protagonist's thoughts and feelings\n"
                    system_prompt += "- Example: 'Sarah felt her heart skip when Emma smiled. She wondered if Emma could tell how nervous she was.'\n"
        
        # Add content settings
        if content_settings.get('rating') != 'auto':
            system_prompt += f"\nContent Rating: {content_settings.get('rating')}\n"
        
        if content_settings.get('tone') != 'auto':
            system_prompt += f"Story Tone: {content_settings.get('tone')}\n"
        
        if content_settings.get('ending') != 'auto':
            system_prompt += f"Story Ending Style: {content_settings.get('ending')}\n"
        
        # Add narrative style enforcement
        if narrative_style and narrative_style != 'Not chosen':
            system_prompt += f"\nNARRATIVE STYLE: {narrative_style}\n"
            
            if "Romantic Intimate" in narrative_style:
                system_prompt += "Write with deep emotional intimacy, focusing on feelings, thoughts, and romantic tension.\n"
            elif "Action" in narrative_style:
                system_prompt += "Write with fast-paced, dynamic language and quick scene transitions.\n"
            elif "Literary" in narrative_style:
                system_prompt += "Write with rich, descriptive language and literary depth.\n"
            elif "Mysterious" in narrative_style:
                system_prompt += "Write with atmospheric tension and mood-building descriptions.\n"
        
        return system_prompt
