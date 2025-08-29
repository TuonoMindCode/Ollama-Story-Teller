import datetime
import os

class ImprovementProcessor:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def execute_improvements_with_progress(self, original_response, system_prompt, prompts, mode, original_result, enable_streaming=False):
        """Execute improvements with real-time progress display - with optional streaming"""
        from ..generation.executor import GenerationExecutor
        from ..generation.streaming import StreamingCallbacks
        
        executor = GenerationExecutor(self.workshop)
        current_response = original_response
        all_improvements = []

        for idx, improvement_prompt in enumerate(prompts, 1):
            # Start improvement
            imp_start_time = datetime.datetime.now()

            # Create short description for the prompt
            short_desc = self._get_short_description(improvement_prompt)

            print(f"\n   -> Improvement {idx}/{len(prompts)}: [{short_desc}]")
            # REMOVE THIS LINE: print(f"      Started: {imp_start_time.strftime('%H:%M:%S')}")

            if enable_streaming:
                print(f"      Started: {imp_start_time.strftime('%H:%M:%S')}")  # Keep for streaming
                print(f"      Streaming output:")
                print("      " + "-" * 50)
            else:
                print(f"      Started: {imp_start_time.strftime('%H:%M:%S')} - ", end='', flush=True)

            try:
                # Execute single improvement
                if mode == 'cumulative':
                    # Use the current (improved) response as base
                    base_response = current_response
                else:
                    # Always use original response as base
                    base_response = original_response

                # Create the improvement request
                improvement_system = system_prompt
                improvement_user = f"Here is a story:\n\n{base_response}\n\n{improvement_prompt}"

                # Create streaming callback if enabled
                improvement_callback = None
                if enable_streaming:
                    improvement_callback = StreamingCallbacks.improvement_callback

                # Execute improvement
                result = executor.execute_generation(improvement_system, improvement_user, improvement_callback)

                imp_end_time = datetime.datetime.now()
                imp_duration = (imp_end_time - imp_start_time).total_seconds()

                if result and result.get('success'):
                    self._handle_successful_improvement(
                        result, idx, len(prompts), improvement_prompt, short_desc, mode,
                        base_response, all_improvements, current_response, imp_start_time,
                        imp_end_time, imp_duration, enable_streaming
                    )

                    # Update current response for next iteration ONLY if cumulative mode
                    if mode == 'cumulative':
                        current_response = result['response']

                else:
                    self._handle_failed_improvement(
                        result, imp_duration, enable_streaming
                    )

            except Exception as e:
                self._handle_improvement_exception(e, imp_start_time, enable_streaming)

        # Create final result - PRESERVE ALL VERSIONS
        return self._create_final_result(all_improvements, original_response, original_result, mode)
    
    def execute_improvements_with_immediate_saving(self, original_response, system_prompt, prompts, mode, original_result, session_folder, final_system, final_user, params, original_filepath):
        """Execute improvements with immediate file saving after each one"""
        from ..generation.executor import GenerationExecutor
        from ..generation.streaming import StreamingCallbacks
        from ..storage.file_saver import FileSaver
        
        executor = GenerationExecutor(self.workshop)
        file_saver = FileSaver(self.workshop)
        current_response = original_response
        saved_filepaths = [original_filepath]  # Track all saved files
        
        for idx, improvement_prompt in enumerate(prompts, 1):
            # Start improvement
            imp_start_time = datetime.datetime.now()
            
            # Create short description for the prompt
            short_desc = self._get_short_description(improvement_prompt)
            
            print(f"\n   -> Improvement {idx}/{len(prompts)}: [{short_desc}]")
            print(f"      Started: {imp_start_time.strftime('%H:%M:%S')}")
            print(f"      Streaming output:")
            print("      " + "-" * 50)
            
            try:
                # Execute single improvement with streaming
                if mode == 'cumulative':
                    base_response = current_response
                else:
                    base_response = original_response
                
                # Create the improvement request
                improvement_system = system_prompt
                improvement_user = f"Here is a story:\n\n{base_response}\n\n{improvement_prompt}"
                
                # Execute improvement
                result = executor.execute_generation(improvement_system, improvement_user, StreamingCallbacks.improvement_callback)
                
                imp_end_time = datetime.datetime.now()
                imp_duration = (imp_end_time - imp_start_time).total_seconds()
                
                if result and result.get('success'):
                    # Handle successful improvement and save immediately
                    improvement_filepath = self._handle_successful_immediate_save(
                        result, idx, len(prompts), improvement_prompt, short_desc,
                        imp_start_time, imp_end_time, imp_duration, file_saver,
                        session_folder, final_system, final_user, params,
                        original_response, base_response, mode
                    )
                    
                    saved_filepaths.append(improvement_filepath)
                    print(f"      💾 Improvement {idx} saved to: {os.path.basename(improvement_filepath)}")
                    
                    # Update current response for next iteration if cumulative mode
                    if mode == 'cumulative':
                        current_response = result['response']
                    
                else:
                    # Handle failed improvement
                    self._handle_failed_improvement(
                        result, idx, improvement_prompt, short_desc,
                        imp_duration, file_saver, session_folder, saved_filepaths
                    )
                    
            except Exception as e:
                self._handle_exception_immediate_save(
                    e, idx, improvement_prompt, short_desc, imp_start_time,
                    file_saver, session_folder, saved_filepaths
                )

        # Create summary file with links to all individual files
        summary_filepath = file_saver.save_session_summary(
            session_folder, saved_filepaths, original_response, prompts, mode, params
        )
        
        # FIX: Check if summary_filepath is not None before using it
        if summary_filepath:
            print(f"\n📋 Session summary saved to: {os.path.basename(summary_filepath)}")
        else:
            print(f"\n❌ Could not create session summary file")
        
        # Return success result
        return {
            'success': True,
            'type': 'improvements_with_immediate_saving',
            'saved_files': saved_filepaths,
            'total_improvements_attempted': len(prompts),
            'summary_file': summary_filepath  # This can be None, which is fine
        }
    
    def _get_short_description(self, improvement_prompt):
        """Get short description for the improvement prompt"""
        if "tension" in improvement_prompt.lower():
            return "Add tension"
        elif "unexpected" in improvement_prompt.lower():
            return "Add unexpected"
        elif "dialogue" in improvement_prompt.lower():
            return "Improve dialogue"
        elif "emotion" in improvement_prompt.lower():
            return "Add emotion"
        elif "pacing" in improvement_prompt.lower():
            return "Improve pacing"
        elif "sensory" in improvement_prompt.lower():
            return "Add sensory details"
        else:
            return improvement_prompt[:15] + "..."
    
    def _handle_successful_improvement(self, result, idx, total, improvement_prompt, short_desc, mode, base_response, all_improvements, current_response, start_time, end_time, duration, enable_streaming):
        """Handle successful improvement"""
        imp_words = result.get('word_count', 0)
        imp_tokens = result.get('token_count', 0)
        imp_time = result.get('generation_time', 0)
        imp_tok_per_sec = imp_tokens / imp_time if imp_time > 0 and imp_tokens > 0 else 0
        
        # Format timing
        imp_end_formatted = end_time.strftime('%H:%M:%S')
        imp_minutes = int(duration // 60)
        imp_seconds = int(duration % 60)
        imp_duration_str = f"{imp_minutes}m{imp_seconds:02d}s"
        
        if enable_streaming:
            print(f"\n      " + "-" * 50)
            print(f"      ✅ Completed: {start_time.strftime('%H:%M:%S')} → {imp_end_formatted} ({imp_duration_str})")
            print(f"      📊 Result: {imp_words} words, {imp_tokens} tokens ({imp_tok_per_sec:.1f} tok/s)")
        else:
            print(f"({start_time.strftime('%H:%M:%S')} → {imp_end_formatted}) {imp_duration_str} → {imp_words} words, {imp_tokens} tokens ({imp_tok_per_sec:.1f} tok/s)")
        
        # Store improvement details - PRESERVE EACH VERSION
        improvement_data = {
            'improvement_number': idx,
            'response': result['response'],  # Store the actual improved story
            'word_count': imp_words,
            'token_count': imp_tokens,
            'generation_time': imp_time,
            'improvement_prompt': improvement_prompt,
            'short_description': short_desc,
            'base_used': 'cumulative' if mode == 'cumulative' else 'original',
            'base_story': base_response  # Store what was used as base for this improvement
        }
        all_improvements.append(improvement_data)
    
    def _handle_failed_improvement(self, result, duration, enable_streaming):
        """Handle failed improvement"""
        imp_minutes = int(duration // 60)
        imp_seconds = int(duration % 60)
        imp_duration_str = f"{imp_minutes}m{imp_seconds:02d}s"
        error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
        
        if enable_streaming:
            print(f"\n      " + "-" * 50)
            print(f"      ❌ FAILED ({imp_duration_str}) - {error_msg}")
        else:
            print(f"FAILED ({imp_duration_str}) - {error_msg}")
    
    def _handle_improvement_exception(self, e, start_time, enable_streaming):
        """Handle improvement exception"""
        imp_end_time = datetime.datetime.now()
        imp_duration = (imp_end_time - start_time).total_seconds()
        imp_minutes = int(imp_duration // 60)
        imp_seconds = int(imp_duration % 60)
        
        if enable_streaming:
            print(f"\n      " + "-" * 50)
            print(f"      ❌ ERROR after {imp_minutes}m{imp_seconds:02d}s: {str(e)}")
        else:
            print(f"ERROR after {imp_minutes}m{imp_seconds:02d}s: {str(e)}")
    
    def _create_final_result(self, all_improvements, original_response, original_result, mode):
        """Create final result preserving all versions"""
        if all_improvements:
            # Determine which version to use as the "final" result
            if mode == 'cumulative':
                # Use the last improvement (which built on all previous ones)
                final_improvement = all_improvements[-1]
                final_response = final_improvement['response']
                final_word_count = final_improvement['word_count']
            else:
                # In original mode, we could use the last improvement or combine somehow
                # For now, let's use the last improvement but note it's based on original
                final_improvement = all_improvements[-1]
                final_response = final_improvement['response']
                final_word_count = final_improvement['word_count']

            result = {
                'success': True,
                'response': final_response,  # The "primary" response for display
                'word_count': final_word_count,
                'token_count': final_improvement['token_count'],
                'generation_time': original_result['generation_time'],  # Keep original time for speed calc
                'type': 'multi_improvement',
                'initial_story': original_response,  # PRESERVE ORIGINAL
                'all_improvements': all_improvements,  # PRESERVE ALL IMPROVEMENT VERSIONS
                'improvement_mode': mode,
                'total_improvements': len(all_improvements)
            }

            return result
        else:
            # No successful improvements, return original unchanged
            return original_result
    
    def _handle_successful_immediate_save(self, result, idx, total, improvement_prompt, short_desc, start_time, end_time, duration, file_saver, session_folder, system_prompt, user_prompt, params, original_response, base_response, mode):
        """Handle successful improvement with immediate saving"""
        imp_words = result.get('word_count', 0)
        imp_tokens = result.get('token_count', 0)
        imp_time = result.get('generation_time', 0)
        imp_tok_per_sec = imp_tokens / imp_time if imp_time > 0 and imp_tokens > 0 else 0
        
        # Format timing
        imp_end_formatted = end_time.strftime('%H:%M:%S')
        imp_minutes = int(duration // 60)
        imp_seconds = int(duration % 60)
        imp_duration_str = f"{imp_minutes}m{imp_seconds:02d}s"
        
        print(f"\n      " + "-" * 50)
        print(f"      ✅ Completed: {start_time.strftime('%H:%M:%S')} → {imp_end_formatted} ({imp_duration_str})")
        print(f"      📊 Result: {imp_words} words, {imp_tokens} tokens ({imp_tok_per_sec:.1f} tok/s)")
        
        # Save improvement immediately
        improvement_filepath = file_saver.save_improvement_story(
            result, idx, total, improvement_prompt, short_desc,
            session_folder, system_prompt, user_prompt, params,
            original_response, base_response, mode
        )
        
        return improvement_filepath
    
    def _handle_failed_improvement(self, result, idx, improvement_prompt, short_desc, duration, file_saver, session_folder, saved_filepaths):
        """Handle failed improvement with immediate saving"""
        imp_minutes = int(duration // 60)
        imp_seconds = int(duration % 60)
        imp_duration_str = f"{imp_minutes}m{imp_seconds:02d}s"
        error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
    
        print(f"\n      " + "-" * 50)
        print(f"      ❌ FAILED ({imp_duration_str}) - {error_msg}")
    
        # Save error info
        error_filepath = file_saver.save_failed_improvement(
            idx, improvement_prompt, short_desc, error_msg, 
            session_folder, imp_duration_str
        )
        if error_filepath:
            saved_filepaths.append(error_filepath)
    
    def _handle_exception_immediate_save(self, e, idx, improvement_prompt, short_desc, start_time, file_saver, session_folder, saved_filepaths):
        """Handle exception with immediate saving"""
        imp_end_time = datetime.datetime.now()
        imp_duration = (imp_end_time - start_time).total_seconds()
        imp_minutes = int(imp_duration // 60)
        imp_seconds = int(imp_duration % 60)
        
        print(f"\n      " + "-" * 50)
        print(f"      ❌ ERROR after {imp_minutes}m{imp_seconds:02d}s: {str(e)}")
        
        # Save error info
        error_filepath = file_saver.save_failed_improvement(
            idx, improvement_prompt, short_desc, str(e), 
            session_folder, f"{imp_minutes}m{imp_seconds:02d}s"
        )
        if error_filepath:
            saved_filepaths.append(error_filepath)
