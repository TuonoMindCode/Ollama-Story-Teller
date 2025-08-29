import datetime
import os


class MultipleGenerator:
    def __init__(self, workshop):
        self.workshop = workshop
        
    def generate_multiple_scenes(self):
        """Generate multiple scenes with enhanced time tracking and immediate saving"""
        if not self._check_ready():
            print("Configure system prompt, user prompt, and model first")
            input("Press Enter to continue...")
            return

        count = self.workshop.current_settings['scene_count']
        mode = self.workshop.current_settings['parameter_mode']

        print(f"\nGENERATING {count} SCENES")
        print("="*60)
        print(f"Parameter mode: {mode.title()}")
        print(f"Settings: {self.workshop.parameter_manager.get_parameter_display()}")
        print(f"System: {self.workshop.current_settings['system_prompt_name']}")
        print(f"User: {self.workshop.current_settings['user_prompt_name']}")
        print(f"Max tokens per scene: {self.workshop.current_settings.get('max_output_tokens', 2048)}")

        has_improvements = self.workshop.second_prompt.has_second_prompt()
        if has_improvements:
            print(f"Second Prompt: {self.workshop.second_prompt.get_display_name()}")

        confirm = input(f"\nGenerate {count} scene(s) with parameter variation? (y/n): ").lower()
        if confirm != 'y':
            return

        print("\nStarting batch generation...")
        print("Note: Streaming disabled for batch - results only")
        print("Scenes will be appended to file as they complete")
        input("Press Enter to continue or Ctrl+C to cancel...")

        # Build prompts once - access through workshop.generator
        final_system = self.workshop.generator.prompt_builder.build_system_prompt()
        base_user_prompt = self.workshop.generator.prompt_builder.build_user_prompt()
        
        # Apply age guidance and other enhancements like the executor does
        final_user = self.workshop.generator.executor.get_enhanced_user_prompt(base_user_prompt)

        # Initialize timing
        batch_start_time = datetime.datetime.now()
        print(f"\nBatch started at: {batch_start_time.strftime('%H:%M:%S')}")
        print("="*60)

        # Initialize batch data collection
        successful_scenes = 0
        failed_scenes = 0
        scene_times = []
        batch_scene_results = []
        batch_parameters = []

        # Get base filename components for consistent naming
        timestamp = batch_start_time.strftime("%Y%m%d_%H%M%S")
        model_name = self.workshop.model_tester.test_config['model'].replace(':', '_').replace('/', '_')
        base_name = f"workshop_batch_{count}scenes_{timestamp}_{model_name}"

        # Use laboratory folder structure instead of results folder
        scenes_dir = self.workshop.model_tester.laboratory_scenes
        metadata_dir = self.workshop.model_tester.laboratory_metadata
        
        # Ensure directories exist
        os.makedirs(scenes_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)

        # Create the stories file in laboratory/scenes/
        stories_file_path = os.path.join(scenes_dir, f"{base_name}_stories.txt")
        try:
            with open(stories_file_path, 'w', encoding='utf-8') as f:
                f.write("")  # Create empty file
            print(f"📝 Created stories file: laboratory/scenes/{os.path.basename(stories_file_path)}")
        except Exception as e:
            print(f"❌ Error creating stories file: {e}")
            return

        for i in range(count):
            scene_start_time = datetime.datetime.now()
            params = self.workshop.parameter_manager.get_parameter_values(i)
            batch_parameters.append(params)
            
            print(f"\nScene {i+1}/{count} - T={params['temperature']} P={params['top_p']} K={params['top_k']}")
            print(f"Started: {scene_start_time.strftime('%H:%M:%S')} - ", end='', flush=True)
            
            # Update config with scene-specific parameters
            original_config = self.workshop.model_tester.test_config.copy()
            self.workshop.model_tester.test_config.update(params)
            
            try:
                # Access executor through workshop.generator
                result = self.workshop.generator.executor.execute_generation(final_system, final_user, callback=None)
                
                if result and result.get('success'):
                    orig_end_time = datetime.datetime.now()
                    orig_duration = (orig_end_time - scene_start_time).total_seconds()
                    
                    orig_words = result.get('word_count', 0)
                    orig_tokens = result.get('token_count', 0)
                    orig_time = result.get('generation_time', 0)
                    orig_tok_per_sec = orig_tokens / orig_time if orig_time > 0 and orig_tokens > 0 else 0
                    
                    # Format original timing
                    scene_start_formatted = scene_start_time.strftime('%H:%M:%S')
                    orig_end_formatted = orig_end_time.strftime('%H:%M:%S')
                    orig_duration_str = self._format_duration(orig_duration)
                    
                    print(f"-> Original Story     ({scene_start_formatted} → {orig_end_formatted}) {orig_duration_str} → {orig_words} words, {orig_tokens} tokens ({orig_tok_per_sec:.1f} tok/s)")
                    
                    # Append original story to file immediately - clean format
                    try:
                        with open(stories_file_path, 'a', encoding='utf-8') as f:
                            f.write(f"SCENE {i+1} - THE ORIGINAL\n\n")
                            f.write(f"{result['response']}\n\n")
                            f.flush()  # Ensure it's written immediately
                        print(f"   ✅ Original appended to file")
                    except Exception as save_error:
                        print(f"   ❌ Error appending original: {save_error}")
                    
                    # Initialize scene result data
                    scene_result_data = {
                        'success': True,
                        'scene_number': i + 1,
                        'original_response': result['response'],
                        'original_word_count': orig_words,
                        'original_token_count': orig_tokens,
                        'original_generation_time': orig_time,
                        'scene_parameters': params,
                        'improvements': []
                    }
                    
                    # Apply improvements if configured
                    final_result = result
                    if has_improvements:
                        prompts = self.workshop.current_settings.get('second_user_prompts', [])
                        mode_setting = self.workshop.current_settings.get('second_prompt_mode', 'original')
                        
                        # Execute improvements and collect data - access through workshop.generator
                        improvement_result = self.workshop.generator.improvement_processor.execute_improvements_with_progress(
                            result['response'], 
                            final_system, 
                            prompts,
                            mode_setting,
                            result
                        )
                        
                        if improvement_result and improvement_result.get('success'):
                            final_result = improvement_result

                            # Extract improvement data and append each to file immediately
                            all_improvements = improvement_result.get('all_improvements', [])
                            scene_result_data['improvements'] = all_improvements
                            scene_result_data['has_improvements'] = len(all_improvements) > 0
                            
                            # Append each improvement to file immediately - clean format
                            for improvement in all_improvements:
                                if improvement.get('success', True) and improvement.get('response'):
                                    imp_num = improvement.get('improvement_number', 1)
                                    
                                    try:
                                        with open(stories_file_path, 'a', encoding='utf-8') as f:
                                            f.write(f"SCENE {i+1} - IMPROVEMENT {imp_num}\n\n")
                                            f.write(f"{improvement['response']}\n\n")
                                            f.flush()  # Ensure it's written immediately
                                        print(f"   ✅ Improvement {imp_num} appended to file")
                                    except Exception as save_error:
                                        print(f"   ❌ Error appending improvement {imp_num}: {save_error}")
                    
                    # Add scene separator
                    try:
                        with open(stories_file_path, 'a', encoding='utf-8') as f:
                            f.write("="*80 + "\n\n")
                            f.flush()
                    except Exception as save_error:
                        print(f"   ❌ Error adding separator: {save_error}")
                    
                    # Calculate total scene time
                    scene_end_time = datetime.datetime.now()
                    total_scene_duration = (scene_end_time - scene_start_time).total_seconds()
                    scene_times.append(total_scene_duration)
                    
                    # Final scene stats
                    final_words = final_result.get('word_count', orig_words)
                    avg_tok_per_sec = orig_tok_per_sec
                    scene_duration_str = self._format_duration(total_scene_duration)
                    
                    print(f"=> Scene Complete     Total: {scene_duration_str} | Final: {final_words} words | {avg_tok_per_sec:.1f} tok/s avg")
                    
                    # Show time estimates
                    self._show_time_estimates(i, count, scene_times)
                    
                    # Store scene result for stats
                    batch_scene_results.append(scene_result_data)
                    successful_scenes += 1
                    
                else:
                    scene_end_time = datetime.datetime.now()
                    scene_duration = (scene_end_time - scene_start_time).total_seconds()
                    duration_str = self._format_duration(scene_duration)
                    
                    error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                    print(f"-> FAILED            ({scene_start_time.strftime('%H:%M:%S')} → {scene_end_time.strftime('%H:%M:%S')}) {duration_str} - {error_msg}")
                    
                    # Append failed scene to file immediately - clean format
                    try:
                        with open(stories_file_path, 'a', encoding='utf-8') as f:
                            f.write(f"SCENE {i+1} - FAILED\n\n")
                            f.write(f"Error: {error_msg}\n\n")
                            f.write("="*80 + "\n\n")
                            f.flush()
                        print(f"   ✅ Failure appended to file")
                    except Exception as save_error:
                        print(f"   ❌ Error appending failure: {save_error}")
                    
                    # Store failed scene
                    scene_result_data = {
                        'success': False,
                        'scene_number': i + 1,
                        'error': error_msg,
                        'scene_parameters': params
                    }
                    batch_scene_results.append(scene_result_data)
                    failed_scenes += 1
                    
            except Exception as e:
                scene_end_time = datetime.datetime.now()
                scene_duration = (scene_end_time - scene_start_time).total_seconds()
                duration_str = self._format_duration(scene_duration)
                
                print(f"Error after {duration_str}: {str(e)}")
                
                # Append error to file immediately - clean format
                try:
                    with open(stories_file_path, 'a', encoding='utf-8') as f:
                        f.write(f"SCENE {i+1} - ERROR\n\n")
                        f.write(f"Error: {str(e)}\n\n")
                        f.write("="*80 + "\n\n")
                        f.flush()
                    print(f"   ✅ Error appended to file")
                except Exception as save_error:
                    print(f"   ❌ Error appending error: {save_error}")
                
                batch_scene_results.append({
                    'success': False,
                    'scene_number': i + 1,
                    'error': str(e),
                    'scene_parameters': params
                })
                failed_scenes += 1
            finally:
                # Always restore original config
                self.workshop.model_tester.test_config = original_config

        # Create stats file in laboratory/metadata/
        batch_end_time = datetime.datetime.now()
        total_batch_duration = (batch_end_time - batch_start_time).total_seconds()
        
        print(f"\n📁 Creating stats file...")
        
        batch_result = {
            'success': True,
            'type': 'scene_workshop_batch',
            'scene_results': batch_scene_results,
            'batch_parameters': batch_parameters,
            'generation_time': total_batch_duration,
            'scene_count': count,
            'successful_scenes': successful_scenes,
            'failed_scenes': failed_scenes,
            'parameter_mode': mode
        }
        
        # Save stats file to laboratory/metadata/
        self._save_stats_file_only(batch_result, final_system, final_user, base_name, metadata_dir)
        
        # Show final summary
        self._show_final_batch_summary(batch_start_time, batch_end_time, successful_scenes, failed_scenes, scene_times, mode)
        
        total_scenes = successful_scenes + failed_scenes
        print(f"\n✅ Complete! You have:")
        print(f"   • 1 combined stories file with all {total_scenes} scenes" + (f" and improvements" if has_improvements else ""))
        print(f"   • 1 stats file with technical details")
        print(f"   • Stories were saved in real-time as each completed")
        print(f"   • Files saved to laboratory/scenes/ and laboratory/metadata/")
        
        input("Press Enter to continue...")

    def _check_ready(self):
        """Check if the executor is ready"""
        return self.workshop.generator.executor.check_ready()

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
        print("Files saved in laboratory structure - scenes and metadata separated")

    def _save_stats_file_only(self, result, system_prompt, user_prompt, base_name, metadata_dir):
        """Save only the stats file to laboratory/metadata/"""
        try:
            stats_filename = f"{base_name}_stats.txt"
            stats_content = self._format_statistics_output(result, system_prompt, user_prompt, {'name': 'batch'})
            
            stats_path = os.path.join(metadata_dir, stats_filename)
            with open(stats_path, 'w', encoding='utf-8') as f:
                f.write(stats_content)
            
            print(f"✅ Stats file saved: laboratory/metadata/{stats_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving stats file: {e}")
            return False

    def _format_statistics_output(self, result, system_prompt, user_prompt, template_info):
        """Format the statistics/metadata file"""
        stats = f"""================================================================================
MODEL TEST RESULT
================================================================================

Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: {self.workshop.model_tester.test_config['model']}
Test Type: scene_workshop_batch
Template: {template_info.get('name', 'Custom')}
Generation Time: {result.get('generation_time', 0):.2f}s
Timeout Setting: {self.workshop.model_tester.get_timeout_display()}
Word Count: {result.get('word_count', 0)}
Token Count: {result.get('token_count', 0)}
Words per minute: {int(result.get('word_count', 0) * 60 / max(result.get('generation_time', 1), 1))}
Tokens per minute: {int(result.get('token_count', 0) * 60 / max(result.get('generation_time', 1), 1))}
Success: {result.get('success', False)}

SYSTEM PROMPT:
{system_prompt}

USER PROMPT:
{user_prompt}

PARAMETERS USED:
{self._format_parameters_info(result)}

GENERATION SUMMARY:
{self._format_generation_summary(result)}
"""
        return stats

    def _format_parameters_info(self, result):
        """Format parameter information"""
        if result.get('type') == 'scene_workshop_batch':
            batch_parameters = result.get('batch_parameters', [])
            # FIX: Use the correct parameter_mode from result, not from individual parameters
            param_mode = result.get('parameter_mode', 'unknown')  # Changed this line
            
            if param_mode == 'random':
                return f"Mode: Random parameter variation across {len(batch_parameters)} scenes"
            elif param_mode == 'incremental':
                return f"Mode: Incremental parameter progression across {len(batch_parameters)} scenes"
            else:
                return f"Mode: Fixed parameters across {len(batch_parameters)} scenes"
        else:
            parameters_used = result.get('parameters_used', {})
            return f"Temperature: {parameters_used.get('temperature', 'Unknown')}, Top-P: {parameters_used.get('top_p', 'Unknown')}, Top-K: {parameters_used.get('top_k', 'Unknown')}"

    def _format_generation_summary(self, result):
        """Format generation summary"""
        if result.get('type') == 'scene_workshop_batch':
            # FIX: Calculate improvement mode and count from actual data
            scene_results = result.get('scene_results', [])
            total_improvements = 0
            improvement_mode = 'none'
            
            # Count actual improvements from scene results
            for scene_result in scene_results:
                if scene_result.get('improvements'):
                    total_improvements += len(scene_result['improvements'])
                    if improvement_mode == 'none':
                        # Determine mode from workshop settings
                        improvement_mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
        
            return f"""Scene Count: {result.get('scene_count', 0)}
Successful Scenes: {result.get('successful_scenes', 0)}
Improvement Mode: {improvement_mode}
Total Improvements: {total_improvements}"""
        else:
            return f"""Generation Type: Single Scene
Has Improvements: {result.get('has_improvements', False)}
Improvement Count: {result.get('improvement_count', 0)}
Original Word Count: {result.get('original_word_count', 0)}"""
