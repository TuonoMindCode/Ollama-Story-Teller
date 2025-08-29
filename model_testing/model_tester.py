import requests
import json
import os
import time
import datetime
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

class ModelTester:
    def __init__(self, stories_folder: str):
        self.stories_folder = stories_folder
        
        # Updated to use laboratory folder at project root, not relative to stories folder
        self.laboratory_base = "laboratory"
        self.laboratory_scenes = os.path.join(self.laboratory_base, 'scenes')
        self.laboratory_metadata = os.path.join(self.laboratory_base, 'metadata')  
        self.laboratory_templates = os.path.join(self.laboratory_base, 'templates')
        
        # Move config file to project root
        self.config_file = "test_config.json"
        
        # Create necessary folders with new structure
        os.makedirs(self.laboratory_scenes, exist_ok=True)
        os.makedirs(self.laboratory_metadata, exist_ok=True)
        os.makedirs(self.laboratory_templates, exist_ok=True)
        os.makedirs(os.path.join(self.laboratory_templates, 'system_prompts'), exist_ok=True)
        os.makedirs(os.path.join(self.laboratory_templates, 'user_prompts'), exist_ok=True)
        
        # Migrate existing config if it exists in the old location
        self._migrate_config_if_needed()
        
        # Load saved configuration
        self.test_config = self._load_config()
        
        self.current_session = None
        self.test_cancelled = False
    
    def _migrate_config_if_needed(self):
        """Migrate config from old location to new location"""
        old_config_path = os.path.join(self.laboratory_metadata, 'test_config.json')
        
        if os.path.exists(old_config_path) and not os.path.exists(self.config_file):
            try:
                # Copy the config to the new location
                import shutil
                shutil.move(old_config_path, self.config_file)
                print(f"✅ Migrated test configuration to project root: {self.config_file}")
            except Exception as e:
                print(f"⚠️ Could not migrate config file: {e}")
    
    def _load_config(self) -> Dict:
        """Load test configuration from file"""
        default_config = {
            'model': None,
            'max_tokens': 4000,
            'temperature': 0.8,
            'top_p': 0.9,
            'top_k': 40,
            'repeat_penalty': 1.1,
            'seed': None,
            'timeout_seconds': 0,
            'connection_timeout': 30
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Update default with saved values
                    default_config.update(saved_config)
                    print(f"Loaded test configuration from: {self.config_file}")
                    print(f"Model: {saved_config.get('model', 'None')}")
            except Exception as e:
                print(f"Could not load test config: {e}")
        
        return default_config
    
    def _save_config(self):
        """Save current test configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_config, f, indent=2)
        except Exception as e:
            print(f"Could not save test config: {e}")
    
    def set_model(self, model_name: str):
        """Set and save the test model"""
        self.test_config['model'] = model_name
        self._save_config()
        print(f"Test model set and saved: {model_name}")
    
    def estimate_tokens(self, text: str) -> int:
        """Rough estimation of tokens from text"""
        if not text:
            return 0
        
        char_count = len(text)
        estimated_tokens = char_count / 4
        word_count = len(text.split())
        estimated_tokens = max(word_count, min(estimated_tokens, char_count / 3))
        
        return int(estimated_tokens)
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            return []
        except:
            return []
    
    def stream_ollama_request(self, system_prompt: str, user_prompt: str, 
                             config: Dict = None, callback=None) -> Dict:
        """Stream request to Ollama with configurable timeout"""
        if config is None:
            config = self.test_config
        
        payload = {
            "model": config['model'],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": True,
            "options": {
                "num_predict": config['max_tokens'],
                "temperature": config['temperature'],
                "top_p": config['top_p'],
                "top_k": config['top_k'],
                "repeat_penalty": config['repeat_penalty']
            }
        }
        
        if config.get('seed') is not None:
            payload["options"]["seed"] = config['seed']
        
        start_time = time.time()
        full_response = ""
        actual_tokens_used = 0
        
        # Determine timeouts
        connection_timeout = config.get('connection_timeout', 30)
        read_timeout = config.get('timeout_seconds', 0)
        
        # Set up timeout configuration
        if read_timeout == 0:
            # No timeout - wait forever
            timeout_config = (connection_timeout, None)  # (connection_timeout, read_timeout)
            timeout_display = "unlimited"
        else:
            timeout_config = (connection_timeout, read_timeout)
            timeout_display = f"{read_timeout}s"
        
        try:
            if callback and read_timeout > 60:  # Show timeout info for long waits
                callback(f"[Starting generation with {timeout_display} timeout...]\n", "")
            elif callback and read_timeout == 0:
                callback(f"[Starting generation with unlimited timeout - this may take a very long time...]\n", "")
            
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=payload,
                stream=True,
                timeout=timeout_config
            )
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'response': '',
                    'generation_time': 0,
                    'word_count': 0,
                    'token_count': 0,
                    'estimated_tokens': 0,
                    'timeout_used': timeout_display
                }
            
            last_activity = time.time()
            
            for line in response.iter_lines():
                if self.test_cancelled:
                    return {
                        'success': False,
                        'error': 'Test cancelled by user',
                        'response': full_response,
                        'generation_time': time.time() - start_time,
                        'word_count': len(full_response.split()),
                        'token_count': actual_tokens_used,
                        'estimated_tokens': self.estimate_tokens(full_response),
                        'timeout_used': timeout_display
                    }
                
                if line:
                    last_activity = time.time()
                    try:
                        data = json.loads(line.decode('utf-8'))
                        
                        if 'message' in data and 'content' in data['message']:
                            content = data['message']['content']
                            full_response += content
                            if callback:
                                callback(content, full_response)
                        
                        if data.get('done', False):
                            if 'eval_count' in data:
                                actual_tokens_used = data['eval_count']
                            
                    except json.JSONDecodeError:
                        continue
            
            generation_time = time.time() - start_time
            word_count = len(full_response.split())
            
            if actual_tokens_used == 0:
                actual_tokens_used = self.estimate_tokens(full_response)
            
            return {
                'success': True,
                'response': full_response,
                'generation_time': generation_time,
                'word_count': word_count,
                'token_count': actual_tokens_used,
                'estimated_tokens': self.estimate_tokens(full_response),
                'config_used': config.copy(),
                'timeout_used': timeout_display
            }
            
        except requests.exceptions.ReadTimeout:
            return {
                'success': False,
                'error': f'Generation timed out after {read_timeout} seconds. Try increasing timeout or use unlimited timeout for large models.',
                'response': full_response,
                'generation_time': time.time() - start_time,
                'word_count': len(full_response.split()) if full_response else 0,
                'token_count': actual_tokens_used or self.estimate_tokens(full_response),
                'estimated_tokens': self.estimate_tokens(full_response),
                'timeout_used': timeout_display,
                'timeout_exceeded': True
            }
        except requests.exceptions.ConnectTimeout:
            return {
                'success': False,
                'error': f'Could not connect to Ollama within {connection_timeout} seconds. Is Ollama running?',
                'response': '',
                'generation_time': 0,
                'word_count': 0,
                'token_count': 0,
                'estimated_tokens': 0,
                'timeout_used': timeout_display
            }
        except Exception as e:
            word_count = len(full_response.split()) if full_response else 0
            return {
                'success': False,
                'error': str(e),
                'response': full_response,
                'generation_time': time.time() - start_time,
                'word_count': word_count,
                'token_count': actual_tokens_used or self.estimate_tokens(full_response),
                'estimated_tokens': self.estimate_tokens(full_response),
                'timeout_used': timeout_display
            }
    
    def get_timeout_display(self) -> str:
        """Get human-readable timeout setting"""
        timeout = self.test_config.get('timeout_seconds', 0)
        if timeout == 0:
            return "Unlimited (no timeout)"
        elif timeout < 60:
            return f"{timeout} seconds"
        elif timeout < 3600:
            minutes = timeout // 60
            seconds = timeout % 60
            if seconds == 0:
                return f"{minutes} minutes"
            else:
                return f"{minutes}m {seconds}s"
        else:
            hours = timeout // 3600
            minutes = (timeout % 3600) // 60
            if minutes == 0:
                return f"{hours} hours"
            else:
                return f"{hours}h {minutes}m"
    
    def get_short_model_name(self) -> str:
        """Get shortened model name for filenames"""
        model = self.test_config.get('model', 'unknown')
        if not model or model == 'unknown':
            return 'unknown'
        
        # Remove common prefixes and make it filename-safe
        short_name = model
        
        # Remove common repo prefixes
        if 'hf.co/' in short_name:
            short_name = short_name.split('/')[-1]
        if ':' in short_name:
            short_name = short_name.split(':')[0]
        
        # Remove problematic characters for filenames
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            short_name = short_name.replace(char, '')
        
        # Limit length and clean up
        short_name = short_name[:20]
        short_name = short_name.replace('-', '_').replace('.', '_')
        
        return short_name.lower()
    
    def create_session_folder(self, test_type: str) -> str:
        """Create a new test session folder in laboratory/scenes/"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = f"{test_type}_{timestamp}"
        session_folder = os.path.join(self.laboratory_scenes, session_name)
        os.makedirs(session_folder, exist_ok=True)
        
        self.current_session = session_folder
        return session_folder
    
    def save_test_result(self, result: Dict, test_info: Dict, session_folder: str):
        """Save test result with new laboratory structure - separate story from metadata"""
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        short_model = self.get_short_model_name()
        test_type = test_info.get('test_type', 'test')
        
        # Base filename without extension
        base_filename = f"{short_model}_{test_type}_{timestamp}"
        
        # Save the story file to laboratory/scenes/
        story_filename = f"{base_filename}.txt"
        story_filepath = os.path.join(self.laboratory_scenes, story_filename)
        
        # Save metadata to laboratory/metadata/
        metadata_filename = f"{base_filename}_meta.json"
        metadata_filepath = os.path.join(self.laboratory_metadata, metadata_filename)
        
        # Write story file (just the generated content)
        with open(story_filepath, 'w', encoding='utf-8') as f:
            if result.get('success', False):
                f.write(result.get('response', ''))
            else:
                f.write(f"ERROR: {result.get('error', 'Unknown error')}")
        
        # Write metadata file (system prompt, user prompt, stats)
        metadata = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'model': test_info.get('model', 'Unknown'),
            'test_type': test_info.get('test_type', 'Unknown'),
            'template_name': test_info.get('template_name', 'Custom'),
            'generation_time': result.get('generation_time', 0),
            'timeout_used': result.get('timeout_used', 'Unknown'),
            'timeout_exceeded': result.get('timeout_exceeded', False),
            'word_count': result.get('word_count', 0),
            'token_count': result.get('token_count', 0),
            'estimated_tokens': result.get('estimated_tokens', 0),
            'success': result.get('success', False),
            'system_prompt': test_info.get('system_prompt', 'Not specified'),
            'user_prompt': test_info.get('user_prompt', 'Not specified'),
            'config_used': result.get('config_used', {}),
            'story_file': story_filename,
            'error': result.get('error', None) if not result.get('success', False) else None
        }
        
        # Add performance metrics
        if result.get('generation_time', 0) > 0:
            metadata['words_per_minute'] = (result.get('word_count', 0) / result['generation_time']) * 60
            metadata['tokens_per_minute'] = (result.get('token_count', 0) / result['generation_time']) * 60
        
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return story_filepath, metadata_filepath
    
    def get_folder_size(self, folder_path: str) -> int:
        """Calculate total size of a folder in bytes"""
        if not os.path.exists(folder_path):
            return 0
        
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except (OSError, PermissionError):
            return 0
        
        return total_size
    
    def format_size(self, size_bytes: int) -> str:
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(size_bytes)
        
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        elif size >= 100:
            return f"{size:.0f} {units[unit_index]}"
        elif size >= 10:
            return f"{size:.1f} {units[unit_index]}"
        else:
            return f"{size:.2f} {units[unit_index]}"
    
    def count_files_in_folder(self, folder_path: str) -> int:
        """Count total files in a folder"""
        if not os.path.exists(folder_path):
            return 0
        
        file_count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                file_count += len(filenames)
        except (OSError, PermissionError):
            return 0
        
        return file_count
    
    def get_test_results_stats(self) -> Dict:
        """Get statistics about laboratory content"""
        if not os.path.exists(self.laboratory_base):
            return {
                'total_sessions': 0,
                'total_files': 0,
                'total_size': 0,
                'formatted_size': '0 B'
            }
        
        total_size = self.get_folder_size(self.laboratory_base)
        total_files = self.count_files_in_folder(self.laboratory_base)
        
        # Count story files in scenes folder
        story_count = 0
        if os.path.exists(self.laboratory_scenes):
            story_count = len([f for f in os.listdir(self.laboratory_scenes) if f.endswith('.txt')])
        
        return {
            'total_sessions': story_count,  # Story count instead of sessions
            'total_files': total_files,
            'total_size': total_size,
            'formatted_size': self.format_size(total_size)
        }
    
    def configure_testing_settings(self):
        """Configure testing parameters"""
        while True:
            print("\n" + "="*50)
            print("TESTING CONFIGURATION")
            print("="*50)
            print(f"1. Model: {self.test_config.get('model', 'Not selected')}")
            print(f"2. Temperature: {self.test_config.get('temperature', 0.8)}")
            print(f"3. Top-p: {self.test_config.get('top_p', 0.9)}")
            print(f"4. Top-k: {self.test_config.get('top_k', 40)}")
            print(f"5. Max tokens: {self.test_config.get('max_tokens', 2048)}")
            print(f"6. Timeout: {self.get_timeout_display()}")
            
            # Add the instruct model option
            instruct_status = "Yes" if self.test_config.get('is_instruct_model', False) else "No"
            instruct_format = self.test_config.get('instruct_format', 'none')
            if self.test_config.get('is_instruct_model', False):
                print(f"7. Instruct Model: {instruct_status} ({instruct_format.upper()})")
            else:
                print(f"7. Instruct Model: {instruct_status}")
            
            print("8. Back to testing menu")
            
            choice = input(f"\nSelect option (1-8): ").strip()
            
            if choice == '1':
                self._select_model()
            elif choice == '2':
                self._configure_temperature()
            elif choice == '3':
                self._configure_top_p()
            elif choice == '4':
                self._configure_top_k()
            elif choice == '5':
                self._configure_max_tokens()
            elif choice == '6':
                self._configure_timeout()
            elif choice == '7':
                self._configure_instruct_model()
            elif choice == '8':
                break
            else:
                print("Invalid option. Please try again.")
    
    def _configure_instruct_model(self):
        """Configure whether this is an instruct model"""
        current = self.test_config.get('is_instruct_model', False)
        current_format = self.test_config.get('instruct_format', 'chatml')
        model_name = self.test_config.get('model', 'Unknown')
        
        print(f"\nINSTRUCT MODEL CONFIGURATION")
        print("="*40)
        print(f"Current model: {model_name}")
        print(f"Current setting: {'Yes' if current else 'No'}")
        if current:
            print(f"Current format: {current_format.upper()}")
        print()
        print("Instruct models are fine-tuned to follow instructions and use")
        print("special prompt templates like ChatML or Alpaca format.")
        print()
        print("Examples of instruct models:")
        print("• qwen2.5-instruct (instruct - ChatML)")
        print("• dolphin-mixtral (instruct - ChatML)")
        print("• llama2-chat (instruct - ChatML)")
        print("• codellama:instruct (instruct - ChatML)")
        print("• mistral:instruct (instruct - ChatML)")
        print("• alpaca models (instruct - Alpaca)")
        print()
        print("Examples of base models:")
        print("• llama2 (base - simple prompts)")
        print("• mistral (base - simple prompts)")
        print("• codellama (base - simple prompts)")
        print()
        
        choice = input("Is this an instruct model? (y/n): ").lower().strip()
        
        if choice == 'y':
            self.test_config['is_instruct_model'] = True
            print("✅ Marked as instruct model")
            
            # Choose format
            print("\nSelect instruction format:")
            print("1. ChatML (most modern instruct models - Qwen, Dolphin, etc.)")
            print("2. Alpaca (older Alpaca-style models)")
            print("3. Vicuna (Vicuna-style models)")
            
            format_choice = input("Select format (1-3) [1]: ").strip()
            
            if format_choice == '2':
                self.test_config['instruct_format'] = 'alpaca'
                print("✅ Set to Alpaca format")
            elif format_choice == '3':
                self.test_config['instruct_format'] = 'vicuna'
                print("✅ Set to Vicuna format")
            else:
                self.test_config['instruct_format'] = 'chatml'
                print("✅ Set to ChatML format (recommended)")
                
            self._save_config()
            print("✅ Configuration saved!")
                
        elif choice == 'n':
            self.test_config['is_instruct_model'] = False
            self.test_config.pop('instruct_format', None)  # Remove format if set
            self._save_config()
            print("✅ Marked as base model - will use simple prompt format")
        else:
            print("Invalid choice.")
        
        input("Press Enter to continue...")
    
    def _select_model(self):
        """Enhanced model selection - DISABLED auto-detection"""
        print("\nMODEL SELECTION")
        print("="*30)
        
        available_models = self.get_available_models()
        
        if not available_models:
            print("No models found. Is Ollama running?")
            input("Press Enter to continue...")
            return
        
        print("Available models:")
        for i, model in enumerate(available_models, 1):
            current = " (current)" if model == self.test_config.get('model') else ""
            print(f"{i:2d}. {model}{current}")
        
        print(" 0. Cancel")
        
        try:
            choice = int(input(f"\nSelect model (0-{len(available_models)}): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(available_models):
                selected_model = available_models[choice - 1]
                self.test_config['model'] = selected_model
                
                # Remove auto-detection - always default to base model
                # User can manually change this in option 7 if needed
                self.test_config['is_instruct_model'] = False
                self.test_config.pop('instruct_format', None)  # Remove any existing format
                
                self._save_config()
                print(f"✅ Model selected: {selected_model}")
                
        except ValueError:
            print("Invalid input.")
        
        input("Press Enter to continue...")
    
    def _configure_temperature(self):
        """Configure temperature setting"""
        current = self.test_config.get('temperature', 0.8)
        
        print(f"\nTEMPERATURE CONFIGURATION")
        print("="*30)
        print(f"Current: {current}")
        print("Range: 0.0 - 2.0 (Lower = focused, Higher = creative)")
        print("Common values: 0.1 (very focused), 0.7 (balanced), 1.2 (creative)")
        
        try:
            temp_input = input(f"Temperature [{current}]: ").strip()
            if temp_input:
                temp = float(temp_input)
                if 0.0 <= temp <= 2.0:
                    self.test_config['temperature'] = temp
                    self._save_config()
                    print(f"✅ Temperature set to {temp}")
                else:
                    print("Temperature must be between 0.0 and 2.0")
        except ValueError:
            print("Invalid temperature value")
        
        input("Press Enter to continue...")
    
    def _configure_top_p(self):
        """Configure top-p setting"""
        current = self.test_config.get('top_p', 0.9)
        
        print(f"\nTOP-P CONFIGURATION")
        print("="*20)
        print(f"Current: {current}")
        print("Range: 0.0 - 1.0 (Lower = focused, Higher = diverse)")
        print("Common values: 0.7 (focused), 0.9 (balanced), 0.95 (diverse)")
        
        try:
            p_input = input(f"Top-p [{current}]: ").strip()
            if p_input:
                top_p = float(p_input)
                if 0.0 <= top_p <= 1.0:
                    self.test_config['top_p'] = top_p
                    self._save_config()
                    print(f"✅ Top-p set to {top_p}")
                else:
                    print("Top-p must be between 0.0 and 1.0")
        except ValueError:
            print("Invalid top-p value")
        
        input("Press Enter to continue...")
    
    def _configure_top_k(self):
        """Configure top-k setting"""
        current = self.test_config.get('top_k', 40)
        
        print(f"\nTOP-K CONFIGURATION")
        print("="*20)
        print(f"Current: {current}")
        print("Range: 1+ (Lower = focused, Higher = diverse)")
        print("Common values: 20 (focused), 40 (balanced), 80 (diverse)")
        
        try:
            k_input = input(f"Top-k [{current}]: ").strip()
            if k_input:
                top_k = int(k_input)
                if top_k >= 1:
                    self.test_config['top_k'] = top_k
                    self._save_config()
                    print(f"✅ Top-k set to {top_k}")
                else:
                    print("Top-k must be 1 or greater")
        except ValueError:
            print("Invalid top-k value")
        
        input("Press Enter to continue...")
    
    def _configure_max_tokens(self):
        """Configure max tokens setting"""
        current = self.test_config.get('max_tokens', 2048)
        
        print(f"\nMAX TOKENS CONFIGURATION")
        print("="*25)
        print(f"Current: {current}")
        print("Common values: 512 (short), 2048 (medium), 4096 (long), 8192 (very long)")
        
        try:
            tokens_input = input(f"Max tokens [{current}]: ").strip()
            if tokens_input:
                max_tokens = int(tokens_input)
                if max_tokens >= 100:
                    self.test_config['max_tokens'] = max_tokens
                    self._save_config()
                    print(f"✅ Max tokens set to {max_tokens}")
                else:
                    print("Max tokens must be at least 100")
        except ValueError:
            print("Invalid max tokens value")
        
        input("Press Enter to continue...")
    
    def _configure_timeout(self):
        """Configure timeout setting"""
        current = self.test_config.get('timeout_seconds', 0)
        
        print(f"\nTIMEOUT CONFIGURATION")
        print("="*22)
        print(f"Current: {self.get_timeout_display()}")
        print("Options: 0 = Unlimited, 300 = 5min, 600 = 10min, 1800 = 30min")
        
        try:
            timeout_input = input(f"Timeout seconds [{current}]: ").strip()
            if timeout_input:
                timeout = int(timeout_input)
                if timeout >= 0:
                    self.test_config['timeout_seconds'] = timeout
                    self._save_config()
                    print(f"✅ Timeout set to {self.get_timeout_display()}")
                else:
                    print("Timeout must be 0 or positive")
        except ValueError:
            print("Invalid timeout value")
        
        input("Press Enter to continue...")

    def test_model(self, system_prompt: str, user_prompt: str):
        """Test model with given prompts - legacy method for compatibility"""
        return self.stream_ollama_request(system_prompt, user_prompt)
