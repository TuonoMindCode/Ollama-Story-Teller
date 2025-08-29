import requests
import time
import json

class GenerationExecutor:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def check_ready(self):
        """Check if system prompt, user prompt, and model are configured"""
        try:
            # Check if we have required settings
            system_prompt = self.workshop.settings.get('system_prompt') if self.workshop.settings else None
            user_prompt = self.workshop.settings.get('user_prompt') if self.workshop.settings else None
            model = self.workshop.model_tester.test_config.get('model') if self.workshop.model_tester and self.workshop.model_tester.test_config else None
            
            if not system_prompt:
                print("❌ No system prompt configured. Please select a system prompt first.")
                return False
                
            if not user_prompt:
                print("❌ No user prompt configured. Please select a user prompt first.")
                return False
                
            if not model:
                print("❌ No model configured. Please select a model first.")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error checking readiness: {e}")
            return False

    def execute_generation(self, system_prompt, user_prompt, callback=None):
        """Execute the actual generation with instruct model support"""
        try:
            max_tokens = self.workshop.current_settings.get('max_output_tokens', 2048)
            formatted_prompt = self._format_prompt_for_model(system_prompt, user_prompt)
            
            # Determine stop tokens based on model type
            stop_tokens = []
            is_instruct = self.workshop.model_tester.test_config.get('is_instruct_model', False)
            if is_instruct:
                instruct_format = self.workshop.model_tester.test_config.get('instruct_format', 'chatml')
                if instruct_format == 'chatml':
                    stop_tokens = ["<|im_end|>"]
                elif instruct_format == 'alpaca':
                    stop_tokens = ["### Instruction:", "### Response:"]
            
            data = {
                "model": self.workshop.model_tester.test_config['model'],
                "prompt": formatted_prompt,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": self.workshop.model_tester.test_config.get('temperature', 0.8),
                    "top_p": self.workshop.model_tester.test_config.get('top_p', 0.9),
                    "top_k": self.workshop.model_tester.test_config.get('top_k', 40),
                    "repeat_penalty": self.workshop.model_tester.test_config.get('repeat_penalty', 1.1),
                    "stop": stop_tokens
                },
                "stream": callback is not None
            }
            
            seed = self.workshop.model_tester.test_config.get('seed')
            if seed is not None:
                data["options"]["seed"] = seed
            
            if callback:
                print("Generating with max_tokens:", max_tokens)
                if stop_tokens:
                    print("Stop tokens:", stop_tokens)
            
            start_time = time.time()
            timeout = self.workshop.model_tester.test_config.get('timeout_seconds', 0)
            timeout_val = None if timeout == 0 else timeout
            
            response = requests.post("http://localhost:11434/api/generate", 
                                   json=data, 
                                   timeout=timeout_val,
                                   stream=callback is not None)
        
            if callback and data["stream"]:
                full_response = ""
                final_tokens = 0
                prompt_tokens = 0
                
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = line.decode('utf-8')
                            if chunk.startswith('data: '):
                                chunk = chunk[6:]
                            
                            chunk_data = json.loads(chunk)
                            
                            if 'response' in chunk_data:
                                content = chunk_data['response']
                                full_response += content
                                callback(content, full_response)
                                
                            if chunk_data.get('done', False):
                                # Get final token counts from Ollama
                                final_tokens = chunk_data.get('eval_count', 0)
                                prompt_tokens = chunk_data.get('prompt_eval_count', 0)
                                break
                                
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            continue
                
                end_time = time.time()
                
                result = {
                    'success': True,
                    'response': full_response,
                    'generation_time': end_time - start_time,
                    'word_count': len(full_response.split()),
                    'token_count': final_tokens,
                    'prompt_token_count': prompt_tokens,
                    'type': 'streaming',
                    'max_tokens_used': max_tokens,
                    'stop_tokens_used': stop_tokens
                }
                
            else:
                response.raise_for_status()
                end_time = time.time()
                api_result = response.json()
                
                result = {
                    'success': True,
                    'response': api_result.get('response', ''),
                    'generation_time': end_time - start_time,
                    'word_count': len(api_result.get('response', '').split()),
                    'token_count': api_result.get('eval_count', 0),
                    'prompt_token_count': api_result.get('prompt_eval_count', 0),
                    'type': 'batch',
                    'max_tokens_used': max_tokens
                }
            
            return result
            
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _format_prompt_for_model(self, system_prompt, user_prompt):
        """Format prompt based on whether it's an instruct model"""
        is_instruct = self.workshop.model_tester.test_config.get('is_instruct_model', False)
        
        # Check if thinking mode is disabled
        disable_thinking = self.workshop.current_settings.get('disable_thinking_mode', False)
        
        # Add thinking mode instructions to system prompt if needed
        if disable_thinking:
            thinking_instruction = "\n\nIMPORTANT: Do not show your reasoning process, thinking steps, or use <thinking> tags. Provide only the final response directly without explaining your thought process."
            system_prompt = system_prompt + thinking_instruction
    
        if not is_instruct:
            return system_prompt + "\n\n" + user_prompt
        
        instruct_format = self.workshop.model_tester.test_config.get('instruct_format', 'chatml')
        
        if instruct_format == 'chatml':
            return self._build_chatml_prompt(system_prompt, user_prompt)
        elif instruct_format == 'alpaca':
            return self._build_alpaca_prompt(system_prompt, user_prompt)
        elif instruct_format == 'vicuna':
            return self._build_vicuna_prompt(system_prompt, user_prompt)
        else:
            return self._build_chatml_prompt(system_prompt, user_prompt)
    
    def _build_chatml_prompt(self, system_prompt, user_prompt):
        """Build ChatML format prompt"""
        result = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
        result += f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        result += "<|im_start|>assistant\n"
        return result
    
    def _build_alpaca_prompt(self, system_prompt, user_prompt):
        """Build Alpaca format prompt"""
        result = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n"
        result += f"### Instruction:\n{system_prompt}\n\n{user_prompt}\n\n"
        result += f"### Response:\n"
        return result
    
    def _build_vicuna_prompt(self, system_prompt, user_prompt):
        """Build Vicuna format prompt"""
        result = f"A chat between a curious user and an artificial intelligence assistant. "
        result += f"The assistant gives helpful, detailed, and polite answers to the user's questions.\n\n"
        result += f"System: {system_prompt}\n\n"
        result += f"USER: {user_prompt}\n\n"
        result += f"ASSISTANT: "
        return result

    def get_enhanced_user_prompt(self, base_user_prompt):
        """Get user prompt with all enhancements applied from workshop configurators"""
        if not base_user_prompt:
            return base_user_prompt
        
        enhanced_prompt = base_user_prompt
        
        # Add narrative style enhancement if available
        if hasattr(self.workshop, 'styles_config') and self.workshop.styles_config:
            narrative_enhancement = self._get_narrative_enhancement()
            if narrative_enhancement:
                enhanced_prompt += narrative_enhancement
        
        # Add writing style enhancement if available
        if hasattr(self.workshop, 'styles_config') and self.workshop.styles_config:
            writing_enhancement = self._get_writing_enhancement()
            if writing_enhancement:
                enhanced_prompt += writing_enhancement
        
        # Add age guidance enhancement if available
        if hasattr(self.workshop, 'age_guidance_config') and self.workshop.age_guidance_config:
            age_enhancement = self.workshop.age_guidance_config.get_guidance_enhancement()
            if age_enhancement:
                enhanced_prompt += age_enhancement
        
        return enhanced_prompt

    def _get_narrative_enhancement(self):
        """Get narrative style enhancement text"""
        if not self.workshop.settings:
            return ""
        
        narrative_style = self.workshop.settings.get('narrative_style')
        if not narrative_style:
            return ""
        
        narrative_enhancements = {
            'first_inner': "\n\nNarrative Style: Write in first person ('I') with emphasis on internal thoughts and feelings. Focus on the protagonist's inner experience.",
            'second_romance': "\n\nNarrative Style: Use first person ('I') for the protagonist and second person ('you') for the romantic interest. Create intimate, direct connection.",
            'third_limited': "\n\nNarrative Style: Write in third person limited, staying with one character's perspective throughout. Show their thoughts and feelings.",
            'stream': "\n\nNarrative Style: Use stream of consciousness - flowing, connected thoughts with minimal punctuation breaks. Let ideas flow naturally."
        }
        
        return narrative_enhancements.get(narrative_style, "")

    def _get_writing_enhancement(self):
        """Get writing style enhancement text"""
        if not self.workshop.settings:
            return ""
        
        writing_style = self.workshop.settings.get('writing_style')
        if not writing_style:
            return ""
        
        writing_enhancements = {
            'literary': "\n\nWriting Style: Use rich, literary prose with metaphors and deeper meaning. Craft elegant, sophisticated language with layers of meaning.",
            'minimalist': "\n\nWriting Style: Use simple, direct language. Be concise and precise. Focus on essential details only. Short, impactful sentences.",
            'dialogue': "\n\nWriting Style: Focus heavily on dialogue to drive the scene. Use conversation to reveal character and advance the plot. Minimal description tags.",
            'descriptive': "\n\nWriting Style: Include rich sensory details and atmospheric descriptions. Paint vivid pictures with words. Focus on setting and mood."
        }
        
        return writing_enhancements.get(writing_style, "")