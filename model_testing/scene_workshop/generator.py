import datetime
import os
import time

class Generator:
    def __init__(self, workshop):
        self.workshop = workshop
        
        # Initialize components
        from .generation.prompt_builder import PromptBuilder
        from .generation.executor import GenerationExecutor
        from .generation.streaming import StreamingCallbacks
        from .storage.file_saver import FileSaver
        from .improvements.processor import ImprovementProcessor
        from .multiple_generator import MultipleGenerator
        
        self.prompt_builder = PromptBuilder(workshop)
        self.executor = GenerationExecutor(workshop)
        self.callbacks = StreamingCallbacks()
        self.file_saver = FileSaver(workshop)
        self.improvement_processor = ImprovementProcessor(workshop)
        self.multiple_generator = MultipleGenerator(workshop)
    
    def generate_single_scene(self):
        """Generate single scene with streaming and detailed completion statistics"""
        if not self.executor.check_ready():
            print("Configure system prompt, user prompt, and model first")
            input("Press Enter to continue...")
            return

        # Get parameters for single scene (scene 0)
        params = self.workshop.parameter_manager.get_parameter_values(0)

        # Update model tester config temporarily
        original_config = self.workshop.model_tester.test_config.copy()
        self.workshop.model_tester.test_config.update(params)

        # Build system and user prompts
        final_system = self.prompt_builder.build_system_prompt()
        final_user = self.prompt_builder.build_user_prompt()

        print(f"\nGENERATING SCENE WITH STREAMING")
        print("="*60)
        print(f"System: {self.workshop.current_settings['system_prompt_name']}")
        print(f"User: {self.workshop.current_settings['user_prompt_name']}")

        # Show enhancements if applied
        if self.workshop.current_settings['narrative_style_name'] != 'Not selected':
            print(f"Narrative: {self.workshop.current_settings['narrative_style_name']}")
        if self.workshop.current_settings['writing_style_name'] != 'Not selected':
            print(f"Writing: {self.workshop.current_settings['writing_style_name']}")
        if self.workshop.second_prompt.has_second_prompt():
            print(f"Second Prompt: {self.workshop.second_prompt.get_display_name()}")

        print(f"Parameters: T={params['temperature']}, P={params['top_p']}, K={params['top_k']}")
        
        # Show model type info
        model_name = self.workshop.model_tester.test_config.get('model', 'Unknown')
        is_instruct = self.workshop.model_tester.test_config.get('is_instruct_model', False)
        if is_instruct:
            instruct_format = self.workshop.model_tester.test_config.get('instruct_format', 'chatml')
            print(f"Model: {model_name} (Instruct - {instruct_format.upper()})")
        else:
            print(f"Model: {model_name} (Base)")

        print(f"\nSTREAMING OUTPUT:")
        print("-" * 60)

        # Track start time for total timing
        total_start_time = time.time()
        
        result = self.executor.execute_generation(final_system, final_user, self.callbacks.default_callback)

        # Calculate total time including any overhead
        total_end_time = time.time()
        total_duration = total_end_time - total_start_time

        print("\n" + "-" * 60)

        # SHOW DETAILED COMPLETION STATISTICS
        if result and result.get('success'):
            # Calculate statistics
            response_text = result.get('response', '')
            word_count = result.get('word_count', len(response_text.split()))
            token_count = result.get('token_count', 0)
            generation_time = result.get('generation_time', 0)
            max_tokens_used = result.get('max_tokens_used', 0)
            
            # Calculate speeds
            words_per_second = word_count / generation_time if generation_time > 0 else 0
            tokens_per_second = token_count / generation_time if generation_time > 0 and token_count > 0 else 0
            
            # Format timing
            gen_minutes = int(generation_time // 60)
            gen_seconds = generation_time % 60
            total_minutes = int(total_duration // 60)
            total_seconds = total_duration % 60
            
            print("✅ ORIGINAL STORY COMPLETED!")
            print(f"📊 GENERATION STATISTICS:")
            print(f"   Words Generated: {word_count:,}")
            if token_count > 0:
                print(f"   Tokens Generated: {token_count:,}")
                print(f"   Tokens per Second: {tokens_per_second:.1f}")
            else:
                estimated_tokens = int(word_count * 1.3)
                print(f"   Estimated Tokens: {estimated_tokens:,}")
                print(f"   Estimated Tok/Sec: {estimated_tokens/generation_time:.1f}")
            
            print(f"   Words per Second: {words_per_second:.1f}")
            print(f"   Max Tokens Limit: {max_tokens_used:,}")
            
            if gen_minutes > 0:
                print(f"   Generation Time: {gen_minutes}m {gen_seconds:.1f}s")
            else:
                print(f"   Generation Time: {gen_seconds:.2f}s")
                
            if total_duration != generation_time:
                if total_minutes > 0:
                    print(f"   Total Time: {total_minutes}m {total_seconds:.1f}s (including processing)")
                else:
                    print(f"   Total Time: {total_seconds:.2f}s (including processing)")
            
            # Show efficiency metrics
            if max_tokens_used > 0:
                usage_percent = (token_count / max_tokens_used * 100) if token_count > 0 else (word_count * 1.3 / max_tokens_used * 100)
                print(f"   Token Usage: {usage_percent:.1f}% of limit")
            
            # FIXED: Save without creating session folder - use None or create a simple timestamp
            session_folder = None  # Don't create unnecessary folders
            
            # FIXED: Handle the tuple return from save_original_story
            save_result = self.file_saver.save_original_story(result, session_folder, final_system, final_user, params)
            
            # Handle both old and new return formats
            if isinstance(save_result, tuple):
                story_filepath, metadata_filepath = save_result
                print(f"💾 Story saved to: laboratory/scenes/{os.path.basename(story_filepath)}")
                print(f"📊 Metadata saved to: laboratory/metadata/{os.path.basename(metadata_filepath)}")
                main_filepath = story_filepath
            else:
                # Old single file format
                main_filepath = save_result
                print(f"💾 Original saved to: {os.path.basename(main_filepath)}")
            
            # Handle second prompt(s) if configured - WITH IMMEDIATE SAVING
            if self.workshop.second_prompt.has_second_prompt():
                prompts = self.workshop.current_settings.get('second_user_prompts', [])
                mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
            
                print(f"\nApplying {len(prompts)} improvement prompt(s) in {mode} mode...")
            
                # Execute improvements with immediate saving after each one
                final_result = self.improvement_processor.execute_improvements_with_immediate_saving(
                    result['response'], 
                    final_system, 
                    prompts, 
                    mode, 
                    result,
                    session_folder,
                    final_system,
                    final_user,
                    params,
                    main_filepath  # Use the main filepath
                )
            
                if final_result and final_result.get('success'):
                    print(f"\n✅ All improvements completed and saved individually!")
                    print(f"📁 Results in laboratory folders")
                else:
                    print("❌ Some improvements failed. Check individual files.")
        else:
            # Show error statistics
            error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
            partial_response = result.get('response', '') if result else ''
            partial_words = len(partial_response.split()) if partial_response else 0
            
            print("❌ GENERATION FAILED!")
            print(f"📊 FAILURE STATISTICS:")
            print(f"   Error: {error_msg}")
            print(f"   Time Elapsed: {total_duration:.2f}s")
            if partial_words > 0:
                print(f"   Partial Words Generated: {partial_words}")
                print(f"   Partial Response Length: {len(partial_response)} characters")

        # Restore original config
        self.workshop.model_tester.test_config = original_config
        
        input("\nPress Enter to continue...")
    
    def generate_multiple_scenes(self):
        """Delegate to the multiple generator"""
        return self.multiple_generator.generate_multiple_scenes()

    def _show_time_estimates(self, current_index, total_count, scene_times):
        """Show time estimates for remaining scenes"""
        if current_index > 0:  # After first scene
            avg_time = sum(scene_times) / len(scene_times)
            remaining_scenes = total_count - (current_index + 1)
            
            if remaining_scenes > 0:
                next_scene_finish = datetime.datetime.now() + datetime.timedelta(seconds=avg_time)
                all_scenes_finish = datetime.datetime.now() + datetime.timedelta(seconds=remaining_scenes * avg_time)
                
                remaining_minutes = int((remaining_scenes * avg_time) // 60)
                remaining_hours = int(remaining_minutes // 60)
                remaining_minutes = remaining_minutes % 60
                
                if remaining_hours > 0:
                    print(f"   Next scene {current_index+2}/{total_count} ETA: {next_scene_finish.strftime('%H:%M:%S')} | All scenes: {all_scenes_finish.strftime('%H:%M:%S')} ({remaining_hours}h {remaining_minutes}m remaining)")
                else:
                    print(f"   Next scene {current_index+2}/{total_count} ETA: {next_scene_finish.strftime('%H:%M:%S')} | All scenes: {all_scenes_finish.strftime('%H:%M:%S')} ({remaining_minutes}m remaining)")
    
    def _format_duration(self, seconds):
        """Format duration in human readable format"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m{secs:02d}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours}h{minutes:02d}m{secs:02d}s"

    def _show_final_batch_summary(self, batch_start_time, batch_end_time, successful_scenes, failed_scenes, scene_times, mode):
        """Show final batch summary without duplicate file saving"""
        total_batch_duration = (batch_end_time - batch_start_time).total_seconds()
        total_hours = int(total_batch_duration // 3600)
        total_minutes = int((total_batch_duration % 3600) // 60)
        total_seconds = int(total_batch_duration % 60)
        
        print(f"\n" + "="*60)
        print(f"BATCH GENERATION COMPLETE")
        print(f"Started: {batch_start_time.strftime('%H:%M:%S')}")
        print(f"Finished: {batch_end_time.strftime('%H:%M:%S')}")
        
        if total_hours > 0:
            print(f"Total duration: {total_hours}h {total_minutes}m {total_seconds}s")
        else:
            print(f"Total duration: {total_minutes}m {total_seconds}s")
        
        total_scenes = successful_scenes + failed_scenes
        print(f"Successful: {successful_scenes}/{total_scenes}")
        if failed_scenes > 0:
            print(f"Failed: {failed_scenes}/{total_scenes}")
        
        if scene_times:
            avg_scene_time = sum(scene_times) / len(scene_times)
            avg_minutes = int(avg_scene_time // 60)
            avg_seconds = int(avg_scene_time % 60)
            print(f"Average per scene: {avg_minutes}m {avg_seconds}s")
        
        print(f"Parameter mode: {mode.title()}")
        print("Files saved in laboratory structure with story/metadata separation")

def _save_stats_file_only(self, result, system_prompt, user_prompt, base_name, results_dir):
    """Save only the stats file"""
    try:
        stats_filename = f"{base_name}_stats.txt"
        stats_content = self._format_statistics_output(result, system_prompt, user_prompt, {'name': 'batch'})
        
        stats_path = os.path.join(results_dir, stats_filename)
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(stats_content)
        
        print(f"✅ Stats file saved: {stats_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving stats file: {e}")
        return False