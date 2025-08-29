import os
import requests
from datetime import datetime

class APIHandler:
    def __init__(self, llm_settings, prompt_logger=None):
        self.llm_settings = llm_settings
        self.prompt_logger = prompt_logger
        
        # Add configurable timeout with no default timeout
        self.request_timeout = llm_settings.get('request_timeout', None)  # None = no timeout
        
        # Extract the new mode settings
        self.thinking_mode_enabled = llm_settings.get('thinking_mode_enabled', False)
        self.instruct_mode_enabled = llm_settings.get('instruct_mode_enabled', False)
    
    def make_api_call_with_system_prompt(self, system_prompt, user_prompt, max_tokens, stage="unknown"):
        """Make API call with system prompt and log the exchange"""
        
        try:
            # Prepare the API request
            url = "http://localhost:11434/api/generate"
            
            # Apply instruct mode formatting if enabled
            if self.instruct_mode_enabled:
                system_prompt = self._format_instruct_system_prompt(system_prompt)
                user_prompt = self._format_instruct_user_prompt(user_prompt)
            
            # Build the full prompt (system + user)
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{user_prompt}"
            else:
                full_prompt = user_prompt
            
            # Add thinking mode control
            if not self.thinking_mode_enabled:
                full_prompt = self._add_no_thinking_instructions(full_prompt)
            
            data = {
                "model": self.llm_settings['model'],
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": self.llm_settings.get('temperature', 0.8),
                    "top_p": self.llm_settings.get('top_p', 0.9),
                    "top_k": self.llm_settings.get('top_k', 40),
                    "repeat_penalty": self.llm_settings.get('repeat_penalty', 1.1)
                }
            }
            
            # Add model-specific thinking control to options
            if not self.thinking_mode_enabled:
                model_name = self.llm_settings['model'].lower()
                
                # DeepSeek R1 specific
                if 'deepseek' in model_name and 'r1' in model_name:
                    data["options"]["reasoning"] = False
                
                # Qwen QwQ specific
                if 'qwen' in model_name and ('qwq' in model_name or 'reasoning' in model_name):
                    data["options"]["show_reasoning"] = False
                
                # Generic thinking model options
                if any(keyword in model_name for keyword in ['thinking', 'reasoning', 'o1']):
                    data["options"]["thinking"] = False
                    data["options"]["show_thoughts"] = False
            
            # Add seed if specified
            seed = self.llm_settings.get('seed')
            if seed is not None:
                data["options"]["seed"] = seed
            
            # Make the API call with configurable timeout
            if self.request_timeout:
                print(f"   ⏱️ Using {self.request_timeout}s timeout")
                response = requests.post(url, json=data, timeout=self.request_timeout)
            else:
                print(f"   ♾️ Using no timeout (unlimited wait)")
                response = requests.post(url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                # Post-process if thinking mode is disabled (fallback cleanup)
                if not self.thinking_mode_enabled:
                    response_text = self._clean_thinking_output(response_text)
                
                # Log the exchange
                if self.prompt_logger and self.prompt_logger.logging_enabled:
                    self.prompt_logger.log_prompt_exchange(
                        stage=stage,
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        response=response_text,
                        max_tokens=max_tokens
                    )
                
                return response_text
            else:
                error_msg = f"API Error: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                
                # Log the error too
                if self.prompt_logger and self.prompt_logger.logging_enabled:
                    self.prompt_logger.log_prompt_exchange(
                        stage=f"{stage}_ERROR",
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        response=error_msg,
                        max_tokens=max_tokens
                    )
                
                return None
                
        except Exception as e:
            error_msg = f"Exception during API call: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Log the exception
            if self.prompt_logger and self.prompt_logger.logging_enabled:
                self.prompt_logger.log_prompt_exchange(
                    stage=f"{stage}_EXCEPTION",
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    response=error_msg,
                    max_tokens=max_tokens
                )
            
            return None
    
    def make_api_call(self, prompt, max_tokens, stage="unknown"):
        """Make API call without system prompt"""
        return self.make_api_call_with_system_prompt(None, prompt, max_tokens, stage)

    def _add_no_thinking_instructions(self, prompt):
        """Add model-specific no-thinking instructions to prompt"""
        model_name = self.llm_settings['model'].lower()
        
        # Model-specific prefixes and suffixes
        thinking_control_instructions = []
        
        # DeepSeek R1
        if 'deepseek' in model_name and 'r1' in model_name:
            thinking_control_instructions.extend([
                "<|no_reasoning|>",
                "INSTRUCTION: Do not show reasoning steps or thinking process.",
                "Respond directly with your final answer only."
            ])
        
        # Qwen QwQ 
        elif 'qwen' in model_name and ('qwq' in model_name or 'reasoning' in model_name):
            thinking_control_instructions.extend([
                "<|no_think|>",
                "SYSTEM: Disable thinking mode. Provide direct answers only."
            ])
        
        # OpenAI o1-style models
        elif 'o1' in model_name or 'reasoning' in model_name:
            thinking_control_instructions.extend([
                "REASONING_MODE: OFF",
                "OUTPUT_FORMAT: Direct answer only, no thinking steps shown."
            ])
        
        # Generic thinking models
        elif any(keyword in model_name for keyword in ['thinking', 'thought', 'reason']):
            thinking_control_instructions.extend([
                "<|direct_answer|>",
                "IMPORTANT: Provide only your final answer without showing reasoning, thinking, or analysis steps."
            ])
        
        # General fallback for all models when thinking is disabled
        thinking_control_instructions.extend([
            "",
            "RESPONSE INSTRUCTION: Provide only your final answer without showing your reasoning process, thinking steps, or analysis.",
            "Do not include <thinking>, <reasoning>, or similar tags in your response."
        ])
        
        # Combine instructions with original prompt
        control_text = "\n".join(thinking_control_instructions)
        return f"{control_text}\n\n{prompt}"

    def _format_instruct_system_prompt(self, system_prompt):
        """Format system prompt for instruct models"""
        if not system_prompt:
            return system_prompt
            
        return f"""You are an AI assistant specialized in creative writing and storytelling.

INSTRUCTIONS:
{system_prompt}

Please follow these instructions carefully and provide high-quality, detailed responses."""

    def _format_instruct_user_prompt(self, user_prompt):
        """Format user prompt for instruct models"""
        return f"""TASK:
{user_prompt}

Please complete this task following the system instructions provided above."""

    def _clean_thinking_output(self, content):
        """Remove thinking tags and reasoning artifacts from output (fallback cleanup)"""
        if not content:
            return content
            
        import re
        
        # Remove common thinking tags (comprehensive list)
        patterns = [
            # Standard thinking tags
            r'<thinking>.*?</thinking>',
            r'<reason>.*?</reason>',
            r'<reasoning>.*?</reasoning>',
            r'<analysis>.*?</analysis>',
            r'<thought>.*?</thought>',
            
            # Bracket style
            r'\[thinking\].*?\[/thinking\]',
            r'\[reasoning\].*?\[/reasoning\]',
            r'\[analysis\].*?\[/analysis\]',
            r'\[thought\].*?\[/thought\]',
            
            # Model-specific patterns
            r'<\|thinking\|>.*?<\|/thinking\|>',
            r'<\|reason\|>.*?<\|/reason\|>',
            r'<\|analysis\|>.*?<\|/analysis\|>',
            
            # Step-by-step reasoning patterns
            r'Let me think.*?(?=\n\n|\n[A-Z]|\Z)',
            r'I need to consider.*?(?=\n\n|\n[A-Z]|\Z)',
            r'First, I should.*?(?=\n\n|\n[A-Z]|\Z)',
            
            # Control tokens
            r'<\|no_reasoning\|>',
            r'<\|no_think\|>',
            r'<\|direct_answer\|>',
            r'REASONING_MODE: OFF',
            r'OUTPUT_FORMAT: Direct answer only.*?\n'
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up extra whitespace and empty lines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()
        
        return content
