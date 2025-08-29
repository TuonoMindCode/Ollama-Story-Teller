import datetime

class ResultFormatter:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def format_batch_result(self, result, scene_num, total_scenes, mode, params, system_prompt, user_prompt):
        """Format batch result with metadata and ALL versions preserved"""
        is_improved = result.get('type') == 'multi_improvement'
        has_original = 'initial_story' in result
        all_improvements = result.get('all_improvements', [])

        test_info = {
            'model': self.workshop.model_tester.test_config['model'],
            'test_type': 'scene_workshop_batch',
            'template_name': f'Workshop_Scene_{scene_num}_{mode}',
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'second_user_prompts': self.workshop.current_settings.get('second_user_prompts', []),
            'narrative_style': self.workshop.current_settings['narrative_style_name'],
            'writing_style': self.workshop.current_settings['writing_style_name'],
            'batch_number': scene_num,
            'total_in_batch': total_scenes,
            'parameters_used': params,
            'improvement_applied': is_improved,
            'has_original': has_original,
            'improvement_mode': result.get('improvement_mode', 'none'),
            'total_improvements': len(all_improvements)
        }

        # Create enhanced result preserving ALL versions
        enhanced_result = result.copy()

        if is_improved and has_original and all_improvements:
            # Create comprehensive combined response with ALL versions
            original_story = result['initial_story']

            combined_response = f"""=== SCENE {scene_num} - ORIGINAL STORY ===
Parameters: T={params.get('temperature', '?')}, P={params.get('top_p', '?')}, K={params.get('top_k', '?')}
Words: {len(original_story.split())}

{original_story}

=== IMPROVEMENTS APPLIED ({result.get('improvement_mode', 'unknown')} mode) ===
"""

            # Add each improvement with its details
            for idx, improvement in enumerate(all_improvements, 1):
                improvement_response = improvement['response']
                improvement_words = improvement['word_count']
                improvement_prompt = improvement['improvement_prompt']
                short_desc = improvement['short_description']

                combined_response += f"""

--- IMPROVEMENT {idx}/{len(all_improvements)}: {short_desc} ---
Prompt: {improvement_prompt}
Words: {improvement_words}

{improvement_response}

"""

            # Add summary
            final_words = result.get('word_count', 0)
            combined_response += f"""=== SUMMARY ===
Scene: {scene_num}/{total_scenes}
Parameter Mode: {mode}
Improvement Mode: {result.get('improvement_mode', 'unknown')}
Original Story: {len(original_story.split())} words
Total Improvements: {len(all_improvements)}
Final Result: {final_words} words
"""

            enhanced_result['response'] = combined_response
            enhanced_result['original_story'] = original_story
            enhanced_result['all_improvement_stories'] = [imp['response'] for imp in all_improvements]
            enhanced_result['word_count'] = len(combined_response.split())

        elif has_original and not is_improved:
            # Just original story, no improvements
            enhanced_result['response'] = f"""=== SCENE {scene_num} - ORIGINAL STORY (No Improvements) ===
Parameters: T={params.get('temperature', '?')}, P={params.get('top_p', '?')}, K={params.get('top_k', '?')}
Words: {result.get('word_count', 0)}

{result['response']}"""

        return enhanced_result, test_info
    
    def format_original_story(self, result, params):
        """Format the original story for saving"""
        enhanced_result = result.copy()
        enhanced_result['response'] = f"""=== ORIGINAL STORY ===
Parameters: T={params.get('temperature', '?')}, P={params.get('top_p', '?')}, K={params.get('top_k', '?')}
Words: {result.get('word_count', 0)}
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{result['response']}"""
        
        return enhanced_result
    
    def format_improvement_story(self, result, improvement_num, total_improvements, improvement_prompt, short_desc, params, original_story, base_story, mode):
        """Format individual improvement story"""
        enhanced_result = result.copy()
        enhanced_result['response'] = f"""=== IMPROVEMENT {improvement_num}/{total_improvements}: {short_desc.upper()} ===
Improvement Prompt: {improvement_prompt}
Mode: {mode}
Base Used: {"Previous improvement" if mode == 'cumulative' else "Original story"}
Parameters: T={params.get('temperature', '?')}, P={params.get('top_p', '?')}, K={params.get('top_k', '?')}
Words: {result.get('word_count', 0)}
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== IMPROVED STORY ===
{result['response']}

=== BASE STORY USED FOR THIS IMPROVEMENT ===
{base_story[:500]}{"..." if len(base_story) > 500 else ""}

=== ORIGINAL STORY FOR REFERENCE ===
{original_story[:500]}{"..." if len(original_story) > 500 else ""}"""
        
        return enhanced_result
