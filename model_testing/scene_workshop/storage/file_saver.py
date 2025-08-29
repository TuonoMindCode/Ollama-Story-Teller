import os
import datetime

class FileSaver:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def save_original_story(self, result, session_folder, system_prompt, user_prompt, params):
        """Save the original story immediately - return single filepath for compatibility"""
        from .result_formatter import ResultFormatter
        formatter = ResultFormatter(self.workshop)
        
        test_info = {
            'model': self.workshop.model_tester.test_config['model'],
            'test_type': 'scene_workshop_original',
            'template_name': 'Workshop_Original_Story',
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'narrative_style': self.workshop.current_settings['narrative_style_name'],
            'writing_style': self.workshop.current_settings['writing_style_name'],
            'parameters_used': params,
            'story_version': 'original'
        }
        
        enhanced_result = formatter.format_original_story(result, params)
        filepath = self.workshop.model_tester.save_test_result(enhanced_result, test_info, session_folder)
        
        # FIX: Always return a single filepath, not a tuple
        if isinstance(filepath, tuple):
            return filepath[0]  # Return just the story filepath
        return filepath
    
    def save_batch_result(self, result, scene_num, total_scenes, mode, params, session_folder, system_prompt, user_prompt):
        """Save batch result with metadata"""
        from .result_formatter import ResultFormatter
        formatter = ResultFormatter(self.workshop)
        
        enhanced_result, test_info = formatter.format_batch_result(
            result, scene_num, total_scenes, mode, params, system_prompt, user_prompt
        )
        
        self.workshop.model_tester.save_test_result(enhanced_result, test_info, session_folder)
    
    def save_improvement_story(self, result, improvement_num, total_improvements, improvement_prompt, short_desc, session_folder, system_prompt, user_prompt, params, original_story, base_story, mode):
        """Save individual improvement story immediately - return single filepath for compatibility"""
        from .result_formatter import ResultFormatter
        formatter = ResultFormatter(self.workshop)
        
        test_info = {
            'model': self.workshop.model_tester.test_config['model'],
            'test_type': 'scene_workshop_improvement',
            'template_name': f'Workshop_Improvement_{improvement_num}_{short_desc.replace(" ", "_")}',
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'improvement_prompt': improvement_prompt,
            'improvement_number': improvement_num,
            'total_improvements': total_improvements,
            'improvement_mode': mode,
            'parameters_used': params,
            'story_version': f'improvement_{improvement_num}'
        }
        
        enhanced_result = formatter.format_improvement_story(
            result, improvement_num, total_improvements, improvement_prompt, 
            short_desc, params, original_story, base_story, mode
        )
        
        filepath = self.workshop.model_tester.save_test_result(enhanced_result, test_info, session_folder)
        
        # FIX: Always return a single filepath, not a tuple
        if isinstance(filepath, tuple):
            return filepath[0]  # Return just the story filepath
        return filepath
    
    def save_failed_improvement(self, improvement_num, improvement_prompt, short_desc, error_msg, session_folder, duration):
        """Save information about failed improvement attempt"""
        # FIX: Handle None session_folder
        if session_folder is None:
            print("Warning: No session folder provided, cannot save failure log")
            return None
        
        try:
            filename = f"failed_improvement_{improvement_num}_{short_desc.replace(' ', '_').lower()}.txt"
            filepath = os.path.join(session_folder, filename)
            
            content = f"""=== FAILED IMPROVEMENT {improvement_num} ===
Description: {short_desc}
Improvement Prompt: {improvement_prompt}
Error: {error_msg}
Duration: {duration}
Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This improvement attempt failed. The original story and any previous successful improvements are still available in other files in this session folder.
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
        except Exception as e:
            print(f"      Warning: Could not save failure log: {e}")
            return None
    
    def save_session_summary(self, session_folder, saved_filepaths, original_story, prompts, mode, params):
        """Create a summary file linking to all individual story files"""
        # FIX: Handle None session_folder
        if session_folder is None:
            print("Warning: No session folder provided, cannot save session summary")
            return None
            
        try:
            filename = "session_summary.txt"
            filepath = os.path.join(session_folder, filename)
            
            # FIX: Filter out None filepaths
            valid_filepaths = [fp for fp in saved_filepaths if fp is not None]
            
            content = f"""=== SCENE WORKSHOP SESSION SUMMARY ===
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Parameters: T={params.get('temperature', '?')}, P={params.get('top_p', '?')}, K={params.get('top_k', '?')}
Improvement Mode: {mode}
Total Improvements Attempted: {len(prompts)}
Total Files Saved: {len(valid_filepaths)}

=== FILES IN THIS SESSION ===
"""
            
            for i, filepath in enumerate(valid_filepaths, 1):
                filename = os.path.basename(filepath)
                if 'original' in filename.lower():
                    content += f"{i}. {filename} (Original Story)\n"
                elif 'improvement' in filename.lower():
                    content += f"{i}. {filename} (Improvement Story)\n"
                elif 'failed' in filename.lower():
                    content += f"{i}. {filename} (Failed Attempt Log)\n"
                else:
                    content += f"{i}. {filename}\n"
            
            content += f"""
=== IMPROVEMENT PROMPTS USED ===
"""
            
            for i, prompt in enumerate(prompts, 1):
                content += f"{i}. {prompt}\n"
            
            content += f"""
=== ORIGINAL STORY (First 500 characters) ===
{original_story[:500]}{"..." if len(original_story) > 500 else ""}

To see the full stories and improvements, open the individual files listed above.
Each file contains the complete story version with context and metadata.
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return filepath
        except Exception as e:
            print(f"Warning: Could not save session summary: {e}")
            return None