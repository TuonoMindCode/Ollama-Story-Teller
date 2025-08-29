import re

class PromptBuilder:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def build_system_prompt(self):
        """Build system prompt without additional style enhancements"""
        base_system = self.workshop.current_settings['system_prompt']
        
        # System prompt stays as-is - no automatic style additions
        # The user's selected system prompt template should contain all needed instructions
        
        return base_system
    
    def build_user_prompt(self):
        """Build enhanced user prompt with style reinforcement"""
        base_user = self.workshop.current_settings['user_prompt']
        enhanced_user = base_user
        
        # Add narrative style reinforcement to USER PROMPT ONLY
        if self.workshop.current_settings['narrative_style']:
            narrative_style = self.workshop.current_settings['narrative_style']
            
            if narrative_style == 'first_inner':
                enhanced_user += " IMPORTANT: Write entirely in first person using 'I' throughout. Focus on internal thoughts and feelings."
            elif narrative_style == 'second_romance':
                enhanced_user = self._convert_to_second_person(enhanced_user)
                enhanced_user += " CRITICAL: Use 'I' for the protagonist and 'you' for the other person. Never use names or third-person pronouns."
            elif narrative_style == 'third_limited':
                enhanced_user += " IMPORTANT: Write in third person limited perspective, staying with one character's viewpoint."
            elif narrative_style == 'stream':
                enhanced_user += " IMPORTANT: Write in stream of consciousness style with flowing, connected thoughts."
        
        # Add writing style reinforcement to USER PROMPT ONLY
        if self.workshop.current_settings['writing_style']:
            writing_style = self.workshop.current_settings['writing_style']
            
            if writing_style == 'literary':
                enhanced_user += " Use rich, literary prose with metaphors and deeper meaning."
            elif writing_style == 'minimalist':
                enhanced_user += " Write in simple, direct language. Be concise and understated."
            elif writing_style == 'dialogue':
                enhanced_user += " Focus heavily on dialogue. Let conversations drive the scene."
            elif writing_style == 'descriptive':
                enhanced_user += " Include rich sensory details and atmospheric descriptions."
        
        return enhanced_user
    
    def _convert_to_second_person(self, original_prompt):
        """Convert user prompt to second-person perspective"""
        converted = original_prompt
        
        # Common conversions
        replacements = {
            r'\bMr\.\s*\w+': 'you',
            r'\bMs\.\s*\w+': 'you', 
            r'\bMrs\.\s*\w+': 'you',
            r'\bDr\.\s*\w+': 'you',
            r'\bhis\b': 'your',
            r'\bher\b': 'your',
            r'\bhim\b': 'you',
            r'\bhe\b': 'you',
            r'\bhis\s+': 'your ',
            r'\bher\s+': 'your ',
        }
        
        for pattern, replacement in replacements.items():
            converted = re.sub(pattern, replacement, converted, flags=re.IGNORECASE)
        
        # Add explicit second-person instruction
        second_person_instruction = "WRITE THIS SCENE using 'I' for the protagonist and 'you' for the other person. Never use names, 'he', 'him', 'she', 'her' - always refer to the other person as 'you'. "
        
        return second_person_instruction + converted
    
    def enhance_system_prompt_for_clean_endings(self, system_prompt):
        """Add instructions to prevent meta-commentary"""
        ending_guidance = """

IMPORTANT WRITING RULES:
- Stay within the scene throughout - never step outside to explain or analyze
- End with dialogue, action, or character thoughts - not commentary about the writing
- Do not explain the point of view, themes, or literary techniques
- Do not summarize what happened or what the scene accomplished
- Let the story speak for itself without author intrusion"""
    
        return system_prompt + ending_guidance

    def display_enhanced_statistics(self, result, total_duration):
        """Enhanced statistics with better formatting and insights"""
        if result and result.get('success'):
            response_text = result.get('response', '')
            word_count = len(response_text.split())
            char_count = len(response_text)
            generation_time = result.get('generation_time', 0)
            
            print("\n" + "="*70)
            print("📊 GENERATION STATISTICS")
            print("="*70)
            print(f"✅ Status: COMPLETED SUCCESSFULLY")
            print(f"📝 Content: {word_count:,} words | {char_count:,} characters")
            print(f"⏱️  Speed: {word_count/generation_time:.1f} words/second")
            print(f"🕐 Time: {self._format_time(generation_time)} generation")
            
            # Quality metrics
            avg_sentence_length = word_count / max(response_text.count('.') + response_text.count('!') + response_text.count('?'), 1)
            dialogue_count = response_text.count('"')
            
            print(f"📊 Quality: {avg_sentence_length:.1f} avg words/sentence | {dialogue_count} dialogue marks")
            
            # Check for meta-commentary
            meta_phrases = ["point of view", "this scene", "the narrative", "this story", "the reader"]
            meta_count = sum(1 for phrase in meta_phrases if phrase.lower() in response_text.lower())
            if meta_count > 0:
                print(f"⚠️  Warning: Possible meta-commentary detected ({meta_count} instances)")
    
    def validate_before_generation(self):
        """Validate settings before starting generation"""
        issues = []
        
        # Check for overly long user prompts that might cause meta-commentary
        user_prompt = self.prompt_builder.build_user_prompt()
        if len(user_prompt.split()) > 200:
            issues.append("User prompt very long - may cause explanatory endings")
        
        # Check system prompt for story-ending guidance
        system_prompt = self.prompt_builder.build_system_prompt()
        if "stay in scene" not in system_prompt.lower() and "don't explain" not in system_prompt.lower():
            issues.append("System prompt lacks ending guidance - may get meta-commentary")
        
        if issues:
            print("⚠️  POTENTIAL ISSUES DETECTED:")
            for issue in issues:
                print(f"   • {issue}")
            proceed = input("Continue anyway? (y/n): ").strip().lower()
            return proceed == 'y'
        
        return True
