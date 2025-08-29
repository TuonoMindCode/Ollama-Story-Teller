import datetime
import os
import time

class BatchGenerator:
    def __init__(self, workshop):
        self.workshop = workshop
        # Use your existing executor
        from .generation.executor import GenerationExecutor
        self.executor = GenerationExecutor(workshop)

    def generate_multiple_scenes(self):
        """Generate multiple scenes with parameter variations - Option 10"""
        # Quick validation
        system_prompt = self.workshop.settings.get('system_prompt') if self.workshop.settings else None
        user_prompt = self.workshop.settings.get('user_prompt') if self.workshop.settings else None
        
        if not system_prompt or not user_prompt:
            print("❌ Need both system and user prompts configured first")
            input("Press Enter to continue...")
            return

        scene_count = self.workshop.settings.get('scene_count', 3) if self.workshop.settings else 3
        
        print(f"🚀 BATCH GENERATION: {scene_count} SCENES")
        print("="*50)
        print(f"Model: {self.workshop.model_tester.test_config['model']}")
        
        # Get enhanced user prompt (with age guidance, etc.)
        enhanced_user_prompt = self.executor.get_enhanced_user_prompt(user_prompt)
        
        # Generate different parameters for each scene
        parameter_sets = self._create_parameter_variations(scene_count)
        
        # Check for improvements
        second_prompts = self.workshop.settings.get('second_user_prompts', []) if self.workshop.settings else []
        second_prompt_names = self.workshop.settings.get('second_user_prompt_names', []) if self.workshop.settings else []
        improvements_per_scene = len(second_prompts)
        
        # Show what we'll generate
        print(f"\nGenerating {scene_count} scenes with parameter variations:")
        for i, params in enumerate(parameter_sets, 1):
            print(f"  Scene {i}: T={params['temperature']:.2f}, P={params['top_p']:.2f}, K={params['top_k']}")
        
        if improvements_per_scene > 0:
            print(f"\nImprovements per scene: {improvements_per_scene} (using original story each time)")
            for i, name in enumerate(second_prompt_names, 1):
                short_name = self._extract_short_name(name)
                print(f"  Improvement {i}: [{short_name}]")
        else:
            print("\nNo improvements configured - generating original stories only")
        
        input("\nPress Enter to start batch generation...")
        
        # Start batch timing
        batch_start_time = time.time()
        results = []
        
        print("\n" + "="*80)
        print("BATCH GENERATION PROGRESS")
        print("="*80)
        
        for scene_idx, params in enumerate(parameter_sets, 1):
            scene_start_time = time.time()
            scene_start_str = datetime.datetime.now().strftime("%H:%M:%S")
            
            print(f"\nStarted: {scene_start_str} - Scene {scene_idx}/{scene_count}")
            
            # Apply parameters to model tester
            self._apply_parameters_to_model(params)
            
            # Generate original story
            original_start_time = time.time()
            original_start_str = datetime.datetime.now().strftime("%H:%M:%S")
            
            print(f"   -> Original Story     ", end="", flush=True)
            
            result = self.executor.execute_generation(system_prompt, enhanced_user_prompt)
            
            original_end_time = time.time()
            original_end_str = datetime.datetime.now().strftime("%H:%M:%S")
            
            if result.get('success'):
                original_duration = original_end_time - original_start_time
                original_words = result.get('word_count', 0)
                original_tokens = result.get('token_count', 0)
                original_tok_per_sec = original_tokens / max(original_duration, 1)
                
                duration_str = self._format_duration(original_duration)
                
                print(f"({original_start_str} → {original_end_str}) {duration_str} → {original_words} words, {original_tokens} tokens ({original_tok_per_sec:.1f} tok/s)")
                
                # Store original result
                scene_result = {
                    'success': True,
                    'original_response': result['response'],
                    'original_word_count': original_words,
                    'original_token_count': original_tokens,
                    'original_generation_time': original_duration,
                    'scene_parameters': params,
                    'scene_number': scene_idx,
                    'improvements': []
                }
                
                # Apply improvements - each uses the ORIGINAL story as input
                if improvements_per_scene > 0:
                    improvement_results = self._apply_improvements_from_original(
                        result['response'],  # Original story
                        system_prompt,
                        second_prompts,
                        second_prompt_names,
                        improvements_per_scene
                    )
                    scene_result['improvements'] = improvement_results
                
                # Calculate scene totals
                scene_end_time = time.time()
                scene_total_duration = scene_end_time - scene_start_time
                
                # Get final stats (last successful improvement or original)
                final_words, final_tokens = self._calculate_final_stats(scene_result)
                avg_tok_per_sec = final_tokens / max(scene_total_duration, 1)
                scene_duration_str = self._format_duration(scene_total_duration)
                
                print(f"=> Scene Complete     Total: {scene_duration_str} | Final: {final_words} words | {avg_tok_per_sec:.1f} tok/s avg")
                
                # Calculate and show ETA
                self._show_eta(scene_idx, scene_count, batch_start_time)
                
                results.append(scene_result)
                
            else:
                print(f"FAILED - {result.get('error', 'Unknown error')}")
                scene_result = {
                    'success': False,
                    'error': result.get('error'),
                    'scene_parameters': params,
                    'scene_number': scene_idx
                }
                results.append(scene_result)
            
            # Restore original parameters
            self._restore_original_parameters()
        
        # Save results and show summary
        self._save_batch_results(results, system_prompt, enhanced_user_prompt, parameter_sets)
        self._show_final_summary(results, batch_start_time)
        
        input("\nPress Enter to continue...")

    def _apply_improvements_from_original(self, original_story, system_prompt, improvement_prompts, improvement_names, total_improvements):
        """Apply improvements, each using the original story as input"""
        improvement_results = []
        
        for imp_idx, (improvement_prompt, improvement_name) in enumerate(zip(improvement_prompts, improvement_names), 1):
            imp_start_time = time.time()
            imp_start_str = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Extract short name for display
            short_name = self._extract_short_name(improvement_name)
            print(f"   -> Improvement {imp_idx}/{total_improvements}: [{short_name}]")
            print(f"      Started: {imp_start_str} - ", end="", flush=True)
            
            # Create improvement prompt that includes the original story
            full_improvement_prompt = f"""Here is a story:

{original_story}

{improvement_prompt}

Please rewrite the story with these improvements:"""
            
            # Generate the improved version
            improvement_result = self.executor.execute_generation(system_prompt, full_improvement_prompt)
            
            imp_end_time = time.time()
            imp_end_str = datetime.datetime.now().strftime("%H:%M:%S")
            imp_duration = imp_end_time - imp_start_time
            
            if improvement_result.get('success'):
                imp_words = improvement_result.get('word_count', 0)
                imp_tokens = improvement_result.get('token_count', 0)
                imp_tok_per_sec = imp_tokens / max(imp_duration, 1)
                
                imp_duration_str = self._format_duration(imp_duration)
                print(f"({imp_start_str} → {imp_end_str}) {imp_duration_str} → {imp_words} words, {imp_tokens} tokens ({imp_tok_per_sec:.1f} tok/s)")
                
                improvement_results.append({
                    'success': True,
                    'response': improvement_result['response'],
                    'word_count': imp_words,
                    'token_count': imp_tokens,
                    'generation_time': imp_duration,
                    'improvement_prompt': improvement_prompt,
                    'improvement_name': improvement_name,
                    'improvement_number': imp_idx
                })
            else:
                print(f"FAILED - {improvement_result.get('error', 'Unknown error')}")
                improvement_results.append({
                    'success': False,
                    'error': improvement_result.get('error'),
                    'improvement_prompt': improvement_prompt,
                    'improvement_name': improvement_name,
                    'improvement_number': imp_idx
                })
        
        return improvement_results

    def _create_stories_content(self, results):
        """Create stories file content with proper formatting"""
        stories = []
        
        for result in results:
            scene_num = result.get('scene_number', 0)
            
            if result.get('success'):
                # Add original story
                original_section = f"""SCENE {scene_num} - THE ORIGINAL

{result['original_response']}"""
                stories.append(original_section)
                
                # Add improvements
                for improvement in result.get('improvements', []):
                    if improvement.get('success', True):
                        imp_num = improvement.get('improvement_number', 1)
                        improvement_section = f"""SCENE {scene_num} - IMPROVEMENT {imp_num}

{improvement['response']}"""
                        stories.append(improvement_section)
            else:
                # Failed scene
                error_section = f"""SCENE {scene_num} - FAILED

Error: {result.get('error', 'Generation failed')}"""
                stories.append(error_section)
        
        return "\n\n".join(stories)

    def _create_stats_content(self, results, system_prompt, user_prompt, parameter_sets):
        """Create statistics file content"""
        successful_results = [r for r in results if r.get('success')]
        
        # Calculate totals
        total_original_words = sum(r.get('original_word_count', 0) for r in successful_results)
        total_original_tokens = sum(r.get('original_token_count', 0) for r in successful_results)
        total_original_time = sum(r.get('original_generation_time', 0) for r in successful_results)
        
        total_improvement_words = 0
        total_improvement_tokens = 0
        total_improvement_time = 0
        total_improvements = 0
        
        for r in successful_results:
            for imp in r.get('improvements', []):
                if imp.get('success', True):
                    total_improvement_words += imp.get('word_count', 0)
                    total_improvement_tokens += imp.get('token_count', 0)
                    total_improvement_time += imp.get('generation_time', 0)
                    total_improvements += 1
        
        total_words = total_original_words + total_improvement_words
        total_tokens = total_original_tokens + total_improvement_tokens
        total_time = total_original_time + total_improvement_time
        
        stats = f"""================================================================================
MODEL TEST RESULT
================================================================================

Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: {self.workshop.model_tester.test_config['model']}
Test Type: scene_workshop_batch
Template: Batch_{len(results)}_scenes
Generation Time: {total_time:.2f}s
Timeout Setting: {self.workshop.settings.get('timeout_seconds', 0) if self.workshop.settings else 0}s
Word Count: {total_words}
Token Count: {total_tokens}
Words per minute: {int(total_words * 60 / max(total_time, 1))}
Tokens per minute: {int(total_tokens * 60 / max(total_time, 1))}
Success: {len(successful_results) == len(results)}

SYSTEM PROMPT:
{system_prompt}

USER PROMPT:
{user_prompt}

BATCH SUMMARY:
Total Scenes: {len(results)}
Successful Scenes: {len(successful_results)}
Failed Scenes: {len(results) - len(successful_results)}
Parameter Mode: {parameter_sets[0].get('mode', 'unknown') if parameter_sets else 'unknown'}
Total Original Stories: {len(successful_results)}
Total Improvements: {total_improvements}

ORIGINAL STORIES:
Words: {total_original_words}, Tokens: {total_original_tokens}, Time: {total_original_time:.1f}s

IMPROVEMENTS:
Words: {total_improvement_words}, Tokens: {total_improvement_tokens}, Time: {total_improvement_time:.1f}s

SCENE DETAILS:
"""
        
        for result in results:
            scene_num = result.get('scene_number', 0)
            params = result.get('scene_parameters', {})
            
            if result.get('success'):
                original_words = result.get('original_word_count', 0)
                original_tokens = result.get('original_token_count', 0)
                original_time = result.get('original_generation_time', 0)
                
                stats += f"""Scene {scene_num}: SUCCESS - T={params.get('temperature', 0)}, P={params.get('top_p', 0)}, K={params.get('top_k', 0)}
   Original: {original_words} words, {original_tokens} tokens in {original_time:.1f}s
"""
                
                for improvement in result.get('improvements', []):
                    if improvement.get('success', True):
                        imp_num = improvement.get('improvement_number', 1)
                        imp_words = improvement.get('word_count', 0)
                        imp_tokens = improvement.get('token_count', 0)
                        imp_time = improvement.get('generation_time', 0)
                        stats += f"""   Improvement {imp_num}: {imp_words} words, {imp_tokens} tokens in {imp_time:.1f}s
"""
            else:
                stats += f"""Scene {scene_num}: FAILED - T={params.get('temperature', 0)}, P={params.get('top_p', 0)}, K={params.get('top_k', 0)} - Error: {result.get('error', 'Unknown')}
"""
        
        return stats

    def _apply_parameters_to_model(self, params):
        """Apply parameters to model tester and store originals"""
        config = self.workshop.model_tester.test_config
        
        # Store originals
        self._original_params = {
            'temperature': config.get('temperature'),
            'top_p': config.get('top_p'),
            'top_k': config.get('top_k')
        }
        
        # Apply new parameters
        config['temperature'] = params['temperature']
        config['top_p'] = params['top_p']
        config['top_k'] = params['top_k']

    def _restore_original_parameters(self):
        """Restore original parameters"""
        if hasattr(self, '_original_params'):
            config = self.workshop.model_tester.test_config
            for key, value in self._original_params.items():
                if value is not None:
                    config[key] = value

    def _calculate_final_stats(self, scene_result):
        """Calculate final word and token counts"""
        original_words = scene_result.get('original_word_count', 0)
        original_tokens = scene_result.get('original_token_count', 0)
        
        if scene_result.get('improvements'):
            # Get the last successful improvement
            last_successful = None
            total_improvement_tokens = 0
            
            for imp in scene_result['improvements']:
                if imp.get('success', True):
                    last_successful = imp
                    total_improvement_tokens += imp.get('token_count', 0)
            
            if last_successful:
                final_words = last_successful['word_count']
                final_tokens = original_tokens + total_improvement_tokens
            else:
                final_words = original_words
                final_tokens = original_tokens
        else:
            final_words = original_words
            final_tokens = original_tokens
        
        return final_words, final_tokens

    def _show_eta(self, current_scene, total_scenes, batch_start_time):
        """Calculate and show ETA for remaining scenes"""
        if current_scene < total_scenes:
            elapsed_batch_time = time.time() - batch_start_time
            avg_time_per_scene = elapsed_batch_time / current_scene
            remaining_scenes = total_scenes - current_scene
            estimated_remaining_time = remaining_scenes * avg_time_per_scene
            
            next_scene_eta = datetime.datetime.now() + datetime.timedelta(seconds=avg_time_per_scene)
            batch_eta = datetime.datetime.now() + datetime.timedelta(seconds=estimated_remaining_time)
            
            remaining_str = self._format_duration(estimated_remaining_time)
            
            print(f"   Next scene {current_scene + 1}/{total_scenes} ETA: {next_scene_eta.strftime('%H:%M:%S')} | All scenes: {batch_eta.strftime('%H:%M:%S')} ({remaining_str} remaining)")

    def _show_final_summary(self, results, batch_start_time):
        """Show final batch summary"""
        batch_end_time = time.time()
        total_batch_time = batch_end_time - batch_start_time
        successful = [r for r in results if r.get('success')]
        
        # Calculate totals
        total_words = 0
        total_tokens = 0
        
        for r in successful:
            final_words, final_tokens = self._calculate_final_stats(r)
            total_words += final_words
            total_tokens += final_tokens
        
        print(f"\n" + "="*80)
        print(f"✅ BATCH COMPLETED")
        print(f"Successful: {len(successful)}/{len(results)}")
        print(f"Total time: {self._format_duration(total_batch_time)}")
        print(f"Total words: {total_words}")
        print(f"Total tokens: {total_tokens}")
        print(f"Average tokens/second: {total_tokens / max(total_batch_time, 1):.1f}")

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

    def _extract_short_name(self, improvement_name):
        """Extract a short name from improvement name for display"""
        if "Built-in:" in improvement_name:
            if "Option 1" in improvement_name:
                return "Add emotion"
            elif "Option 2" in improvement_name:
                return "Add dialogue"
            elif "Option 3" in improvement_name:
                return "Add atmosphere"
            elif "Option 4" in improvement_name:
                return "Add tension"
            elif "Option 5" in improvement_name:
                return "Add sensory"
            elif "Option 6" in improvement_name:
                return "Add character"
            elif "Option 7" in improvement_name:
                return "Add pacing"
            elif "Option 8" in improvement_name:
                return "Add unexpected"
            elif "Option 9" in improvement_name:
                return "Add connection"
            elif "Option 10" in improvement_name:
                return "Show don't tell"
            elif "Option 11" in improvement_name:
                return "Add thoughts"
            else:
                return improvement_name.replace("Built-in: ", "")[:15]
        elif "Custom:" in improvement_name:
            return improvement_name.replace("Custom: ", "")[:20]
        else:
            return improvement_name[:15]

    def _create_parameter_variations(self, count):
        """Create different parameter sets for each scene"""
        parameter_mode = self.workshop.settings.get('parameter_mode', 'incremental') if self.workshop.settings else 'incremental'
        
        base_temp = self.workshop.settings.get('temperature', 0.8) if self.workshop.settings else 0.8
        base_top_p = self.workshop.settings.get('top_p', 0.9) if self.workshop.settings else 0.9
        base_top_k = self.workshop.settings.get('top_k', 40) if self.workshop.settings else 40
        
        if parameter_mode == 'random':
            return self._create_random_variations(count, base_temp, base_top_p, base_top_k)
        else:
            # Incremental/linear progression
            return self._create_incremental_variations(count, base_temp, base_top_p, base_top_k)

    def _create_incremental_variations(self, count, base_temp, base_top_p, base_top_k):
        """Create incremental parameter variations"""
        variations = []
        
        # Get ranges
        temp_range = self.workshop.settings.get('temperature_range', {'min': 0.1, 'max': 1.0}) if self.workshop.settings else {'min': 0.1, 'max': 1.0}
        top_p_range = self.workshop.settings.get('top_p_range', {'min': 0.1, 'max': 1.0}) if self.workshop.settings else {'min': 0.1, 'max': 1.0}
        top_k_range = self.workshop.settings.get('top_k_range', {'min': 1, 'max': 100}) if self.workshop.settings else {'min': 1, 'max': 100}
        
        for i in range(count):
            if count == 1:
                # Single scene - use base values
                temp = base_temp
                top_p = base_top_p
                top_k = base_top_k
            else:
                # Multiple scenes - create progression
                progress = i / (count - 1)  # 0.0 to 1.0
                
                temp = temp_range['min'] + progress * (temp_range['max'] - temp_range['min'])
                top_p = top_p_range['min'] + progress * (top_p_range['max'] - top_p_range['min'])
                top_k = int(top_k_range['min'] + progress * (top_k_range['max'] - top_k_range['min']))
            
            variations.append({
                'temperature': round(temp, 2),
                'top_p': round(top_p, 2),
                'top_k': top_k,
                'mode': 'incremental'
            })
        
        return variations

    def _create_random_variations(self, count, base_temp, base_top_p, base_top_k):
        """Create random parameter variations"""
        import random
        variations = []
        
        temp_range = self.workshop.settings.get('temperature_range', {'min': 0.1, 'max': 1.0}) if self.workshop.settings else {'min': 0.1, 'max': 1.0}
        top_p_range = self.workshop.settings.get('top_p_range', {'min': 0.1, 'max': 1.0}) if self.workshop.settings else {'min': 0.1, 'max': 1.0}
        top_k_range = self.workshop.settings.get('top_k_range', {'min': 1, 'max': 100}) if self.workshop.settings else {'min': 1, 'max': 100}
        
        for i in range(count):
            temp = random.uniform(temp_range['min'], temp_range['max'])
            top_p = random.uniform(top_p_range['min'], top_p_range['max'])
            top_k = random.randint(top_k_range['min'], top_k_range['max'])
            
            variations.append({
                'temperature': round(temp, 2),
                'top_p': round(top_p, 2),
                'top_k': top_k,
                'mode': 'random'
            })
        
        return variations

    def _save_batch_results(self, results, system_prompt, user_prompt, parameter_sets):
        """Save batch results to files"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = self.workshop.model_tester.test_config['model'].replace(':', '_').replace('/', '_')
            
            # Create base filename
            base_name = f"batch_{len(results)}scenes_{timestamp}_{model_name}"
            
            # Save statistics file
            stats_filename = f"{base_name}_stats.txt"
            stats_content = self._create_stats_content(results, system_prompt, user_prompt, parameter_sets)
            
            results_folder = getattr(self.workshop.model_tester, 'results_folder', 'results')
            os.makedirs(results_folder, exist_ok=True)
            
            stats_path = os.path.join(results_folder, stats_filename)
            with open(stats_path, 'w', encoding='utf-8') as f:
                f.write(stats_content)
            
            # Save stories file
            stories_filename = f"{base_name}_stories.txt"
            stories_content = self._create_stories_content(results)
            
            stories_path = os.path.join(results_folder, stories_filename)
            with open(stories_path, 'w', encoding='utf-8') as f:
                f.write(stories_content)
            
            print(f"\n✅ Files saved:")
            print(f"   Statistics: {stats_filename}")
            print(f"   Stories: {stories_filename}")
            
        except Exception as e:
            print(f"❌ Error saving files: {e}")
