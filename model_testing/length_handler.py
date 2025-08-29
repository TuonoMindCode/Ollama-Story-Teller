class LengthHandler:
    def __init__(self):
        self.length_presets = {
            'short_scene': {
                'words': '300-500',
                'tokens': '400-650',
                'description': 'Brief focused scene'
            },
            'medium_scene': {
                'words': '800-1200', 
                'tokens': '1040-1560',
                'description': 'Detailed scene with depth'
            },
            'long_scene': {
                'words': '1500-2000',
                'tokens': '1950-2600', 
                'description': 'Highly detailed, immersive scene'
            },
            'short_story': {
                'words': '1000-1500',
                'tokens': '1300-1950',
                'description': 'Compact complete story'
            },
            'medium_story': {
                'words': '2500-3500',
                'tokens': '3250-4550',
                'description': 'Substantial story with development'
            },
            'long_story': {
                'words': '4000-6000',
                'tokens': '5200-7800',
                'description': 'Epic detailed story'
            },
            'custom': {
                'words': 'Custom',
                'tokens': 'Custom',
                'description': 'Specify your own length'
            }
        }
    
    def select_content_length(self, content_type):
        """Select desired length for story or scene"""
        print(f"\n{'='*60}")
        print(f"{content_type.upper()} LENGTH SELECTION")
        print(f"{'='*60}")
        print("Choose the desired length for your content:")
        print()
        
        # Filter presets based on content type
        if content_type == 'scene':
            available_keys = ['short_scene', 'medium_scene', 'long_scene', 'custom']
        else:  # story
            available_keys = ['short_story', 'medium_story', 'long_story', 'custom']
        
        # Display options
        for i, key in enumerate(available_keys, 1):
            preset = self.length_presets[key]
            print(f"{i}. {preset['description'].title()}")
            print(f"   Words: {preset['words']} | Tokens: ~{preset['tokens']}")
            print()
        
        try:
            choice = int(input(f"Select length (1-{len(available_keys)}): "))
            
            if 1 <= choice <= len(available_keys):
                selected_key = available_keys[choice - 1]
                
                if selected_key == 'custom':
                    return self._handle_custom_length()
                else:
                    preset = self.length_presets[selected_key]
                    return {
                        'type': 'preset',
                        'key': selected_key,
                        'words': preset['words'],
                        'tokens': preset['tokens'],
                        'description': preset['description'],
                        'system_prompt_instruction': self._create_system_prompt_instruction(preset['words']),
                        'user_prompt_instruction': self._create_user_prompt_instruction(preset['words'])
                    }
            else:
                print("Invalid choice.")
                return None
                
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
    
    def _handle_custom_length(self):
        """Handle custom length input"""
        print("\nCustom Length Configuration:")
        print("You can specify either words or tokens (words recommended)")
        print()
        
        length_type = input("Specify by (w)ords or (t)okens? [w]: ").strip().lower() or 'w'
        
        if length_type.startswith('w'):
            try:
                min_words = int(input("Minimum words: "))
                max_words_input = input("Maximum words (optional, press Enter to skip): ").strip()
                max_words = int(max_words_input) if max_words_input else min_words
                
                if max_words < min_words:
                    max_words = min_words
                
                word_range = f"{min_words}-{max_words}" if max_words != min_words else str(min_words)
                estimated_tokens = f"{int(min_words * 1.3)}-{int(max_words * 1.3)}"
                
                return {
                    'type': 'custom',
                    'words': word_range,
                    'tokens': estimated_tokens,
                    'description': f'Custom {word_range} words',
                    'system_prompt_instruction': self._create_system_prompt_instruction(word_range),
                    'user_prompt_instruction': self._create_user_prompt_instruction(word_range)
                }
                
            except ValueError:
                print("Invalid number input.")
                return None
        else:
            try:
                min_tokens = int(input("Minimum tokens: "))
                max_tokens_input = input("Maximum tokens (optional, press Enter to skip): ").strip()
                max_tokens = int(max_tokens_input) if max_tokens_input else min_tokens
                
                if max_tokens < min_tokens:
                    max_tokens = min_tokens
                
                token_range = f"{min_tokens}-{max_tokens}" if max_tokens != min_tokens else str(min_tokens)
                estimated_words = f"{int(min_tokens / 1.3)}-{int(max_tokens / 1.3)}"
                
                return {
                    'type': 'custom',
                    'words': estimated_words,
                    'tokens': token_range,
                    'description': f'Custom {token_range} tokens',
                    'system_prompt_instruction': self._create_system_prompt_instruction(estimated_words),
                    'user_prompt_instruction': self._create_user_prompt_instruction(estimated_words)
                }
                
            except ValueError:
                print("Invalid number input.")
                return None
    
    def _create_system_prompt_instruction(self, length_spec):
        """Create system prompt instruction for length - formal tone"""
        if '-' in str(length_spec):
            min_val, max_val = length_spec.split('-')
            return f"Your stories should be comprehensive and well-developed, typically {min_val}-{max_val} words long."
        else:
            return f"Your stories should be comprehensive and well-developed, typically {length_spec} words long."
    
    def _create_user_prompt_instruction(self, length_spec):
        """Create user prompt instruction for length - direct tone"""
        if '-' in str(length_spec):
            min_val, max_val = length_spec.split('-')
            return f"Make this story substantial and detailed - at least {min_val} words."
        else:
            return f"Make this story substantial and detailed - at least {length_spec} words."
    
    def get_max_tokens_for_generation(self, length_config):
        """Calculate max_tokens setting for Ollama based on length config"""
        if length_config['type'] == 'preset':
            key = length_config['key']
            if 'short' in key:
                return 2048
            elif 'medium' in key:
                return 4096
            elif 'long' in key:
                return 8192
        else:  # custom
            # Extract token estimate and add buffer
            token_str = length_config['tokens']
            if '-' in token_str:
                max_tokens = int(token_str.split('-')[1])
            else:
                max_tokens = int(token_str)
            
            # Add 20% buffer and round up to nearest 1024
            buffered = int(max_tokens * 1.2)
            return ((buffered + 1023) // 1024) * 1024
        
        return 4096  # default
