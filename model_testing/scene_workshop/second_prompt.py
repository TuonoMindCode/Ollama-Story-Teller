class SecondPromptManager:
    def __init__(self, workshop):
        self.workshop = workshop
        
        # Add second prompt settings to workshop if they don't exist
        if 'second_user_prompts' not in self.workshop.current_settings:
            self.workshop.current_settings['second_user_prompts'] = []  # List of prompts
            self.workshop.current_settings['second_prompt_mode'] = 'original'  # 'original' or 'chained'
            self.workshop.current_settings['second_prompt_names'] = []
    
    def get_display_name(self):
        """Get display name for current second prompts"""
        prompts = self.workshop.current_settings.get('second_user_prompts', [])
        if not prompts:
            return 'Not selected'
        
        count = len(prompts)
        mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
        mode_text = "chained" if mode == 'chained' else "from original"
        
        return f'{count} prompt(s) - {mode_text}'
    
    def has_second_prompt(self):
        """Check if second prompts are configured"""
        prompts = self.workshop.current_settings.get('second_user_prompts', [])
        return len(prompts) > 0
    
    def select_second_prompt(self):
        """Select multiple second user prompts with processing mode"""
        while True:
            print("\n" + "="*60)
            print("SECOND USER PROMPT CONFIGURATION")
            print("="*60)
            
            prompts = self.workshop.current_settings.get('second_user_prompts', [])
            mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
            
            print("Current Configuration:")
            if prompts:
                print(f"Number of improvement prompts: {len(prompts)}")
                print(f"Processing mode: {mode.title()}")
                print()
                print("Selected prompts:")
                for i, prompt in enumerate(prompts, 1):
                    preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
                    print(f"  {i}. {preview}")
                print()
            else:
                print("No improvement prompts selected")
                print()
            
            print("PROCESSING MODES:")
            print("• Original: Each improvement uses the original story")
            print("• Chained: Each improvement uses the previous improved version")
            print()
            
            print("Options:")
            print("1. Add improvement prompt")
            print("2. Remove improvement prompt")
            print("3. Clear all prompts")
            print("4. Set processing mode (Original vs Chained)")
            print("5. Preview improvement workflow")
            print("6. Back to workshop")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._add_improvement_prompt()
            elif choice == "2":
                self._remove_improvement_prompt()
            elif choice == "3":
                self._clear_all_prompts()
            elif choice == "4":
                self._set_processing_mode()
            elif choice == "5":
                self._preview_workflow()
            elif choice == "6":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def _add_improvement_prompt(self):
        """Add an improvement prompt"""
        # Check current prompt count
        current_prompts = self.workshop.current_settings.get('second_user_prompts', [])
        if len(current_prompts) >= 3:
            print("Maximum of 3 improvement prompts allowed")
            input("Press Enter to continue...")
            return
        
        print("\nADD IMPROVEMENT PROMPT")
        print("="*40)
        
        built_in_prompts = {
            1: "Make this story more alive and emotional. Add deeper feelings and vivid descriptions.",
            2: "Improve the dialogue to make it more natural and engaging. Add character personality.",
            3: "Enhance the atmosphere and setting descriptions. Make the scene more immersive.",
            4: "Add more tension and dramatic moments. Increase the emotional stakes.",
            5: "Include more sensory details - what characters see, hear, smell, and feel.",
            6: "Make the characters more relatable and human. Add subtle personality traits.",
            7: "Improve the pacing and flow. Make transitions between actions smoother.",
            8: "Add unexpected elements or subtle plot developments to increase interest.",
            9: "Deepen the emotional connections between characters and their motivations.",
            10: "Focus on showing rather than telling. Convert exposition into action and dialogue.",
            11: "Add internal monologue to reveal character thoughts and feelings.",
            12: "Create custom improvement prompt"
        }
        
        print("Built-in improvement prompts:")
        for key, value in built_in_prompts.items():
            print(f"{key:2d}. {value}")
        
        try:
            choice = int(input(f"\nSelect prompt to add (1-{len(built_in_prompts)}): "))
            
            if choice == 12:  # Custom prompt
                custom_prompt = input("Enter custom improvement prompt: ").strip()
                if not custom_prompt:
                    print("Empty prompt cancelled.")
                    input("Press Enter to continue...")
                    return
                
                selected_prompt = custom_prompt
                prompt_name = f"Custom: {custom_prompt[:30]}..."
                
            elif 1 <= choice <= 11:
                selected_prompt = built_in_prompts[choice]
                prompt_name = f"Built-in: Option {choice}"
            else:
                print("Invalid choice.")
                input("Press Enter to continue...")
                return
            
            # Add to lists using proper method
            current_prompts = self.workshop.current_settings.get('second_user_prompts', [])
            current_names = self.workshop.current_settings.get('second_prompt_names', [])
            
            # Create new lists with the added prompt
            new_prompts = current_prompts + [selected_prompt]
            new_names = current_names + [prompt_name]
            
            # Save the updated lists
            self.workshop.current_settings['second_user_prompts'] = new_prompts
            self.workshop.current_settings['second_prompt_names'] = new_names
            
            print(f"Added improvement prompt: {prompt_name}")
            
        except ValueError:
            print("Invalid input.")
        
        input("Press Enter to continue...")
    
    def _remove_improvement_prompt(self):
        """Remove an improvement prompt"""
        prompts = self.workshop.current_settings.get('second_user_prompts', [])
        names = self.workshop.current_settings.get('second_prompt_names', [])
        
        if not prompts:
            print("No improvement prompts to remove")
            input("Press Enter to continue...")
            return
        
        print("\nREMOVE IMPROVEMENT PROMPT")
        print("="*40)
        
        for i, name in enumerate(names, 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input(f"\nSelect prompt to remove (1-{len(prompts)}): "))
            
            if 1 <= choice <= len(prompts):
                # Create new lists without the removed item
                new_names = names[:choice-1] + names[choice:]
                new_prompts = prompts[:choice-1] + prompts[choice:]
                
                removed_name = names[choice - 1]
                
                # Save the updated lists
                self.workshop.current_settings['second_user_prompts'] = new_prompts
                self.workshop.current_settings['second_prompt_names'] = new_names
                
                print(f"Removed: {removed_name}")
            else:
                print("Invalid choice.")
                
        except ValueError:
            print("Invalid input.")
        
        input("Press Enter to continue...")
    
    def _clear_all_prompts(self):
        """Clear all improvement prompts"""
        prompts = self.workshop.current_settings.get('second_user_prompts', [])
        
        if not prompts:
            print("No prompts to clear")
            input("Press Enter to continue...")
            return
        
        confirm = input(f"Clear all {len(prompts)} improvement prompt(s)? (y/n): ").strip().lower()
        if confirm == 'y':
            self.workshop.current_settings['second_user_prompts'] = []
            self.workshop.current_settings['second_prompt_names'] = []
            print("All improvement prompts cleared")
        
        input("Press Enter to continue...")
    
    def _set_processing_mode(self):
        """Set processing mode for multiple prompts"""
        print("\nSET PROCESSING MODE")
        print("="*30)
        
        current_mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
        
        print("Processing modes:")
        print(f"1. Original mode {'(current)' if current_mode == 'original' else ''}")
        print("   Each improvement prompt processes the original story")
        print("   Result: Original → Improved1, Original → Improved2, Original → Improved3")
        print()
        print(f"2. Chained mode {'(current)' if current_mode == 'chained' else ''}")
        print("   Each improvement prompt processes the previous result")
        print("   Result: Original → Improved1 → Improved2 → Improved3")
        
        choice = input("\nSelect mode (1-2): ").strip()
        
        if choice == "1":
            self.workshop.current_settings['second_prompt_mode'] = 'original'
            print("Set to Original mode")
        elif choice == "2":
            self.workshop.current_settings['second_prompt_mode'] = 'chained'
            print("Set to Chained mode")
        else:
            print("Invalid choice")
        
        input("Press Enter to continue...")
    
    def _preview_workflow(self):
        """Preview the improvement workflow"""
        prompts = self.workshop.current_settings.get('second_user_prompts', [])
        mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
        names = self.workshop.current_settings.get('second_prompt_names', [])
        
        if not prompts:
            print("No improvement prompts configured")
            input("Press Enter to continue...")
            return
        
        print("\nIMPROVEMENT WORKFLOW PREVIEW")
        print("="*50)
        print(f"Mode: {mode.title()}")
        print(f"Number of improvement steps: {len(prompts)}")
        print()
        
        if mode == 'original':
            print("Workflow (Original mode):")
            print("1. Generate original story")
            for i, name in enumerate(names, 2):
                print(f"{i}. Apply improvement: {name}")
                print(f"   Input: Original story")
            print(f"\nFinal result: {len(prompts)} improved versions of the original story")
            
        else:  # chained
            print("Workflow (Chained mode):")
            print("1. Generate original story")
            for i, name in enumerate(names, 2):
                input_source = "Original story" if i == 2 else f"Result from step {i-1}"
                print(f"{i}. Apply improvement: {name}")
                print(f"   Input: {input_source}")
            print(f"\nFinal result: One story improved through {len(prompts)} iterations")
        
        print(f"\nDetailed prompts:")
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt}")
        
        input("\nPress Enter to continue...")
    
    def execute_improvements(self, initial_story, system_prompt):
        """Execute all improvement prompts based on mode"""
        prompts = self.workshop.current_settings.get('second_user_prompts', [])
        mode = self.workshop.current_settings.get('second_prompt_mode', 'original')
        names = self.workshop.current_settings.get('second_prompt_names', [])
        
        if not prompts:
            return None
        
      
        results = []
        current_story = initial_story
        
        for i, (prompt, name) in enumerate(zip(prompts, names), 1):
            # Suppress individual step output - generator will format it
            
            # Determine input story
            input_story = initial_story if mode == 'original' else current_story
            
            # Execute improvement
            improvement_result = self._execute_single_improvement(input_story, system_prompt, prompt, i)
            
            if improvement_result and improvement_result.get('success'):
                results.append(improvement_result)
                
                # Update current story for chained mode
                if mode == 'chained':
                    current_story = improvement_result['response']
            else:
                # For chained mode, if one step fails, we can't continue
                if mode == 'chained':
                    break
        
        # Create combined result
        if results:
            final_result = self._create_combined_result(initial_story, results, mode, prompts)
            return final_result
        
        return None
    
    def _execute_single_improvement(self, story, system_prompt, improvement_prompt, step_num):
        """Execute a single improvement step"""
        try:
            import requests
            import time
            
            improvement_user_prompt = f"""Here is a story:

{story}

{improvement_prompt}

Please provide the improved version. Keep the same characters and general situation, but enhance it according to the request. Return only the improved story without any additional commentary."""

            data = {
                "model": self.workshop.model_tester.test_config['model'],
                "prompt": f"System: {system_prompt}\n\nUser: {improvement_user_prompt}",
                "options": {
                    "num_predict": self.workshop.model_tester.test_config.get('max_tokens', 4000),
                    "temperature": self.workshop.model_tester.test_config.get('temperature', 0.8),
                    "top_p": self.workshop.model_tester.test_config.get('top_p', 0.9),
                    "top_k": self.workshop.model_tester.test_config.get('top_k', 40),
                    "repeat_penalty": self.workshop.model_tester.test_config.get('repeat_penalty', 1.1)
                },
                "stream": False
            }
            
            seed = self.workshop.model_tester.test_config.get('seed')
            if seed is not None:
                data["options"]["seed"] = seed
            
            start_time = time.time()
            timeout = self.workshop.model_tester.test_config.get('timeout_seconds', 0)
            timeout_val = None if timeout == 0 else timeout
            
            response = requests.post("http://localhost:11434/api/generate", 
                                   json=data, timeout=timeout_val)
            end_time = time.time()
            
            response.raise_for_status()
            api_result = response.json()
            
            result = {
                'success': True,
                'response': api_result.get('response', ''),
                'generation_time': end_time - start_time,
                'word_count': len(api_result.get('response', '').split()),
                'token_count': api_result.get('eval_count', 0),
                'improvement_prompt': improvement_prompt,
                'step_number': step_num,
                'type': 'improvement'
            }
            
            return result
            
        except Exception as e:
            print(f"  Error in step {step_num}: {e}")
            return None
    
    def _create_combined_result(self, original_story, improvement_results, mode, prompts):
        """Create combined result showing all versions"""
        combined_sections = [f"=== ORIGINAL STORY ===\n{original_story}"]
        
        total_time = sum(r['generation_time'] for r in improvement_results)
        final_story = improvement_results[-1]['response'] if improvement_results else original_story
        
        if mode == 'original':
            # Show all improvements from original
            for i, result in enumerate(improvement_results, 1):
                section = f"""=== IMPROVED VERSION {i} ===
Improvement Prompt: {result['improvement_prompt']}

{result['response']}"""
                combined_sections.append(section)
                
            # Summary
            summary = f"""=== IMPROVEMENT SUMMARY ===
Mode: Original (each improvement from original story)
Improvement steps: {len(improvement_results)}
Original words: {len(original_story.split())}"""
            
            for i, result in enumerate(improvement_results, 1):
                summary += f"\nImproved version {i} words: {result['word_count']}"
                
        else:  # chained
            # Show progression through chain
            current_story = original_story
            for i, result in enumerate(improvement_results, 1):
                section = f"""=== IMPROVEMENT STEP {i} ===
Improvement Prompt: {result['improvement_prompt']}
Input: {"Original story" if i == 1 else f"Result from step {i-1}"}

{result['response']}"""
                combined_sections.append(section)
            
            # Summary
            summary = f"""=== IMPROVEMENT SUMMARY ===
Mode: Chained (each improvement builds on previous)
Improvement steps: {len(improvement_results)}
Original words: {len(original_story.split())}
Final words: {improvement_results[-1]['word_count'] if improvement_results else 0}
Total improvement time: {total_time:.1f} seconds"""
        
        combined_sections.append(summary)
        combined_response = "\n\n".join(combined_sections)
        
        # Create final result
        final_result = {
            'success': True,
            'response': combined_response,
            'generation_time': total_time,
            'word_count': len(combined_response.split()),
            'token_count': sum(r.get('token_count', 0) for r in improvement_results),
            'type': 'multi_improvement',
            'improvement_mode': mode,
            'improvement_count': len(improvement_results),
            'initial_story': original_story,
            'final_story': final_story,
            'all_improvements': improvement_results
        }
        
        return final_result
