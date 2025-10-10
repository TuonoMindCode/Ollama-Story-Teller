import random

class ParameterManager:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def get_parameter_display(self):
        """Get display string for current parameter configuration"""
        try:
            mode = self.workshop.current_settings.get('parameter_mode', 'fixed')
            max_tokens = self.workshop.current_settings.get('max_output_tokens', 2048)
            
            if mode == 'fixed':
                # For fixed mode, show the actual configured values, not ranges
                temp = self.workshop.current_settings.get('temperature', 0.8)
                top_p = self.workshop.current_settings.get('top_p', 0.9)
                top_k = self.workshop.current_settings.get('top_k', 40)
                
                base_display = f"Fixed: T={temp}, P={top_p}, K={top_k}"
                
            else:
                # For incremental/random modes, show the ranges
                temp_range = self.workshop.current_settings.get('temp_range')
                if temp_range is None:
                    temp_range = self.workshop.current_settings.get('temperature_range')
                top_p_range = self.workshop.current_settings.get('top_p_range') 
                top_k_range = self.workshop.current_settings.get('top_k_range')
                
                # Provide defaults if ranges are None - use individual values as fallback
                if temp_range is None:
                    current_temp = self.workshop.current_settings.get('temperature', 0.8)
                    temp_range = (current_temp, current_temp)
                if top_p_range is None:
                    current_top_p = self.workshop.current_settings.get('top_p', 0.9)
                    top_p_range = (current_top_p, current_top_p)
                if top_k_range is None:
                    current_top_k = self.workshop.current_settings.get('top_k', 40)
                    top_k_range = (current_top_k, current_top_k)
                
                # Handle both dictionary and tuple formats safely
                try:
                    if isinstance(temp_range, dict):
                        temp_min, temp_max = temp_range.get('min', 0.8), temp_range.get('max', 0.8)
                    elif isinstance(temp_range, (list, tuple)) and len(temp_range) >= 2:
                        temp_min, temp_max = temp_range[0], temp_range[1]
                    else:
                        temp_min = temp_max = self.workshop.current_settings.get('temperature', 0.8)
                except (TypeError, IndexError, KeyError):
                    temp_min = temp_max = 0.8
                    
                try:
                    if isinstance(top_p_range, dict):
                        top_p_min, top_p_max = top_p_range.get('min', 0.9), top_p_range.get('max', 0.9)
                    elif isinstance(top_p_range, (list, tuple)) and len(top_p_range) >= 2:
                        top_p_min, top_p_max = top_p_range[0], top_p_range[1]
                    else:
                        top_p_min = top_p_max = self.workshop.current_settings.get('top_p', 0.9)
                except (TypeError, IndexError, KeyError):
                    top_p_min = top_p_max = 0.9
                    
                try:
                    if isinstance(top_k_range, dict):
                        top_k_min, top_k_max = int(top_k_range.get('min', 40)), int(top_k_range.get('max', 40))
                    elif isinstance(top_k_range, (list, tuple)) and len(top_k_range) >= 2:
                        top_k_min, top_k_max = int(top_k_range[0]), int(top_k_range[1])
                    else:
                        top_k_min = top_k_max = self.workshop.current_settings.get('top_k', 40)
                except (TypeError, IndexError, KeyError, ValueError):
                    top_k_min = top_k_max = 40
                
                if mode == 'incremental':
                    base_display = f"Incremental: T={temp_min}-{temp_max}, P={top_p_min}-{top_p_max}, K={top_k_min}-{top_k_max}"
                elif mode == 'random':
                    base_display = f"Random: T={temp_min}-{temp_max}, P={top_p_min}-{top_p_max}, K={top_k_min}-{top_k_max}"
                else:
                    base_display = f"Unknown mode: {mode}"
            
            return f"{base_display}, MaxTokens={max_tokens}"
            
        except Exception as e:
            # More informative fallback display
            print(f"Debug: Parameter display error: {e}")
            print(f"Debug: Settings type: {type(self.workshop.current_settings)}")
            try:
                mode = self.workshop.current_settings.get('parameter_mode', 'unknown')
                return f"Mode: {mode}, Error: {str(e)}"
            except:
                return f"Parameters: Critical error - {str(e)}"
    
    def get_parameter_values(self, scene_number=0):
        """Get parameter values based on current mode and scene number"""
        try:
            mode = self.workshop.current_settings.get('parameter_mode', 'fixed')
            scene_count = self.workshop.current_settings.get('scene_count', 1)
            max_tokens = self.workshop.current_settings.get('max_output_tokens', 2048)
            
            if mode == 'fixed':
                # For fixed mode, use the actual configured parameter values, not ranges
                base_params = {
                    'temperature': self.workshop.current_settings.get('temperature', 0.8),
                    'top_p': self.workshop.current_settings.get('top_p', 0.9),
                    'top_k': self.workshop.current_settings.get('top_k', 40)
                }
            else:
                # For incremental/random modes, use ranges
                # Get ranges safely - check both naming conventions
                temp_range = self.workshop.current_settings.get('temp_range')
                if temp_range is None:
                    temp_range = self.workshop.current_settings.get('temperature_range')
                    
                top_p_range = self.workshop.current_settings.get('top_p_range') 
                top_k_range = self.workshop.current_settings.get('top_k_range')
                
                # Handle None ranges by providing defaults
                if temp_range is None:
                    temp_range = (0.8, 0.8)
                if top_p_range is None:
                    top_p_range = (0.9, 0.9)
                if top_k_range is None:
                    top_k_range = (40, 40)
                
                # Convert dictionary format to tuple format if needed
                if isinstance(temp_range, dict):
                    temp_range = (temp_range.get('min', 0.8), temp_range.get('max', 0.8))
                if isinstance(top_p_range, dict):
                    top_p_range = (top_p_range.get('min', 0.9), top_p_range.get('max', 0.9))
                if isinstance(top_k_range, dict):
                    top_k_range = (top_k_range.get('min', 40), top_k_range.get('max', 40))
                
                if mode == 'incremental':
                    if scene_count <= 1:
                        base_params = {
                            'temperature': temp_range[0],
                            'top_p': top_p_range[0],
                            'top_k': int(top_k_range[0])
                        }
                    else:
                        progress = scene_number / (scene_count - 1) if scene_count > 1 else 0
                        progress = max(0, min(1, progress))
                        
                        temp = temp_range[0] + (temp_range[1] - temp_range[0]) * progress
                        top_p = top_p_range[0] + (top_p_range[1] - top_p_range[0]) * progress
                        top_k = top_k_range[0] + (top_k_range[1] - top_k_range[0]) * progress
                        
                        base_params = {
                            'temperature': round(temp, 2),
                            'top_p': round(top_p, 2),
                            'top_k': int(round(top_k))
                        }
                elif mode == 'random':
                    temp = random.uniform(temp_range[0], temp_range[1])
                    top_p = random.uniform(top_p_range[0], top_p_range[1])
                    top_k = random.randint(int(top_k_range[0]), int(top_k_range[1]))
                    
                    base_params = {
                        'temperature': round(temp, 2),
                        'top_p': round(top_p, 2),
                        'top_k': top_k
                    }
                else:
                    base_params = {'temperature': 0.8, 'top_p': 0.9, 'top_k': 40}
            
            # Add extended generation options
            base_params.update({
                'options': {
                    'num_predict': max_tokens,
                    'stop': [],
                    'repeat_penalty': 1.1,
                    'repeat_last_n': 64,
                    'temperature': base_params['temperature'],
                    'top_p': base_params['top_p'],
                    'top_k': base_params['top_k'],
                }
            })
            
            return base_params
            
        except Exception as e:
            print(f"Error in get_parameter_values: {e}")
            # Return safe defaults
            return {
                'temperature': 0.8,
                'top_p': 0.9,
                'top_k': 40,
                'options': {
                    'num_predict': 2048,
                    'stop': [],
                    'repeat_penalty': 1.1,
                    'repeat_last_n': 64,
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'top_k': 40,
                }
            }
    
    def configure_parameters(self):
        """Enhanced parameter configuration with instruct model info"""
        while True:
            print("\n⚙️  PARAMETER CONFIGURATION")
            print("="*50)
            
            # Show model type info
            model_name = self.workshop.model_tester.test_config.get('model', 'Not selected')
            is_instruct = self.workshop.model_tester.test_config.get('is_instruct_model', False)
            instruct_format = self.workshop.model_tester.test_config.get('instruct_format', 'none')
            
            print(f"Model: {model_name}")
            print(f"Type: {'Instruct' if is_instruct else 'Base'} model")
            if is_instruct:
                print(f"Format: {instruct_format.upper()}")
            
            print(f"Mode: {self.workshop.current_settings['parameter_mode'].title()}")
            print(f"Settings: {self.get_parameter_display()}")
            print(f"Max Output Tokens: {self.workshop.current_settings.get('max_output_tokens', 2048)}")
            print(f"Timeout: {self.workshop.model_tester.get_timeout_display()}")
            
            # Show thinking mode status
            disable_thinking = self.workshop.current_settings.get('disable_thinking_mode', False)
            thinking_status = "Disabled" if disable_thinking else "Enabled"
            print(f"Thinking Mode: {thinking_status}")
            
            print("\nOptions:")
            print("1. Set parameter mode (Fixed/Incremental/Random)")
            print("2. Configure temperature range")
            print("3. Configure top-p range")
            print("4. Configure top-k range")
            print("5. Configure timeout")
            print("6. Configure max output tokens")
            print("7. Configure model type (Base/Instruct)")
            print("8. Toggle thinking mode (for reasoning models)")  # Add this option
            print("9. Quick presets")
            print("10. Back to workshop")
            
            choice = input("\nSelect option (1-10): ").strip()
            
            if choice == "1":
                self._set_parameter_mode()
            elif choice == "2":
                self._configure_temperature_range()
            elif choice == "3":
                self._configure_top_p_range()
            elif choice == "4":
                self._configure_top_k_range()
            elif choice == "5":
                self._configure_timeout()
            elif choice == "6":
                self._configure_max_tokens()
            elif choice == "7":
                self._configure_model_type()
            elif choice == "8":
                self._configure_thinking_mode()  # Add this method
            elif choice == "9":
                self._quick_parameter_presets()
            elif choice == "10":
                break
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def _set_parameter_mode(self):
        """Set parameter variation mode"""
        print("\nPARAMETER VARIATION MODE")
        print("="*40)
        
        modes = [
            ('fixed', 'Fixed Values', 'Same parameters for all scenes'),
            ('incremental', 'Incremental', 'Parameters increase from min to max across scenes'),
            ('random', 'Random', 'Random values within ranges for each scene')
        ]
        
        current_mode = self.workshop.current_settings['parameter_mode']
        for i, (key, name, desc) in enumerate(modes, 1):
            current = " (current)" if key == current_mode else ""
            print(f"{i}. {name}{current}")
            print(f"   {desc}")
        
        try:
            choice = int(input(f"\nSelect mode (1-{len(modes)}): "))
            if 1 <= choice <= len(modes):
                mode_key = modes[choice - 1][0]
                self.workshop.current_settings['parameter_mode'] = mode_key
                print(f"Parameter mode: {modes[choice - 1][1]}")
                
                if mode_key == 'incremental':
                    print("Tip: First scene uses min values, last scene uses max values")
                elif mode_key == 'random':
                    print("Tip: Each scene gets random values within your ranges")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _configure_temperature_range(self):
        """Configure temperature range or fixed value based on current mode"""
        mode = self.workshop.current_settings.get('parameter_mode', 'fixed')
        
        if mode == 'fixed':
            # For fixed mode, just ask for a single temperature value
            current_temp = self.workshop.current_settings.get('temperature', 0.8)
            
            print(f"\nTEMPERATURE (FIXED MODE)")
            print("="*30)
            print(f"Current: {current_temp}")
            print("Valid: 0.0 - 2.0 (Lower=focused, Higher=creative)")
            print("Recommended: 0.3-0.7 (conservative), 0.8-1.2 (balanced), 1.0-1.6 (creative)")
            
            try:
                temp_input = input(f"Temperature [{current_temp}]: ").strip()
                if temp_input:
                    new_temp = float(temp_input)
                    if 0.0 <= new_temp <= 2.0:
                        self.workshop.current_settings['temperature'] = new_temp
                        # Also set the range to the same value for consistency
                        self.workshop.current_settings['temp_range'] = (new_temp, new_temp)
                        print(f"Fixed temperature: {new_temp}")
                        
                        # Give feedback
                        if new_temp <= 0.7:
                            print("Low temperature: Focused, predictable output")
                        elif new_temp <= 1.2:
                            print("Moderate temperature: Balanced creativity")
                        else:
                            print("High temperature: Very creative, potentially inconsistent")
                    else:
                        print("Temperature must be 0.0 - 2.0")
            except ValueError:
                print("Invalid input")
        
        else:
            # For incremental/random modes, ask for min and max range
            # Get current range, falling back to individual temperature value if range doesn't exist
            current_range = self.workshop.current_settings.get('temp_range')
            if current_range is None:
                current_temp = self.workshop.current_settings.get('temperature', 0.8)
                current_range = (current_temp, current_temp)
                self.workshop.current_settings['temp_range'] = current_range
            
            print(f"\nTEMPERATURE RANGE ({mode.upper()} MODE)")
            print("="*40)
            print(f"Current: {current_range[0]} - {current_range[1]}")
            print("Valid: 0.0 - 2.0 (Lower=focused, Higher=creative)")
            print("Recommended: 0.3-0.7 (conservative), 0.8-1.2 (balanced), 1.0-1.6 (creative)")
            
            if mode == 'incremental':
                print("Note: First scene uses min value, last scene uses max value")
            elif mode == 'random':
                print("Note: Each scene gets random value within this range")
            
            try:
                min_temp = input(f"Min temperature [{current_range[0]}]: ").strip()
                min_temp = float(min_temp) if min_temp else current_range[0]
                
                max_temp = input(f"Max temperature [{current_range[1]}]: ").strip()
                max_temp = float(max_temp) if max_temp else current_range[1]
                
                if min_temp > max_temp:
                    min_temp, max_temp = max_temp, min_temp
                    print("Swapped min/max values")
                
                if 0.0 <= min_temp <= 2.0 and 0.0 <= max_temp <= 2.0:
                    self.workshop.current_settings['temp_range'] = (min_temp, max_temp)
                    # Update individual temperature to middle of range
                    self.workshop.current_settings['temperature'] = (min_temp + max_temp) / 2
                    print(f"Temperature range: {min_temp} - {max_temp}")
                    
                    # Give feedback on selected range
                    if max_temp <= 0.7:
                        print("Low temperature range: Focused, predictable output")
                    elif max_temp <= 1.2:
                        print("Moderate temperature range: Balanced creativity")
                    else:
                        print("High temperature range: Very creative, potentially inconsistent")
                else:
                    print("Values must be 0.0 - 2.0")
            except ValueError:
                print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _configure_top_p_range(self):
        """Configure top-p range or fixed value based on current mode"""
        mode = self.workshop.current_settings.get('parameter_mode', 'fixed')
        
        if mode == 'fixed':
            # For fixed mode, just ask for a single top-p value
            current_top_p = self.workshop.current_settings.get('top_p', 0.9)
            
            print(f"\nTOP-P (FIXED MODE)")
            print("="*20)
            print(f"Current: {current_top_p}")
            print("Valid: 0.0 - 1.0 (Lower=focused, Higher=diverse)")
            print("Recommended: 0.7-0.9 (focused), 0.85-0.95 (balanced), 0.9-1.0 (diverse)")
            
            try:
                top_p_input = input(f"Top-p [{current_top_p}]: ").strip()
                if top_p_input:
                    new_top_p = float(top_p_input)
                    if 0.0 <= new_top_p <= 1.0:
                        self.workshop.current_settings['top_p'] = new_top_p
                        # Also set the range to the same value for consistency
                        self.workshop.current_settings['top_p_range'] = (new_top_p, new_top_p)
                        print(f"Fixed top-p: {new_top_p}")
                        
                        # Give feedback
                        if new_top_p <= 0.8:
                            print("Low top-p: Very focused vocabulary")
                        elif new_top_p <= 0.95:
                            print("Moderate top-p: Good balance")
                        else:
                            print("High top-p: Maximum vocabulary diversity")
                    else:
                        print("Top-p must be 0.0 - 1.0")
            except ValueError:
                print("Invalid input")
        
        else:
            # For incremental/random modes, ask for min and max range
            current_range = self.workshop.current_settings.get('top_p_range')
            
            # Handle different formats and None values
            if current_range is None:
                current_top_p = self.workshop.current_settings.get('top_p', 0.9)
                min_val, max_val = current_top_p, current_top_p
            elif isinstance(current_range, dict):
                # Dictionary format: {'min': 0.8, 'max': 0.9}
                min_val = current_range.get('min', 0.9)
                max_val = current_range.get('max', 0.9)
            elif isinstance(current_range, (list, tuple)) and len(current_range) >= 2:
                # Tuple/list format: (0.8, 0.9)
                min_val, max_val = current_range[0], current_range[1]
            else:
                # Fallback to individual setting
                current_top_p = self.workshop.current_settings.get('top_p', 0.9)
                min_val, max_val = current_top_p, current_top_p
            
            # Store as tuple for consistency
            current_range = (min_val, max_val)
            self.workshop.current_settings['top_p_range'] = current_range
            
            print(f"\nTOP-P RANGE ({mode.upper()} MODE)")
            print("="*30)
            print(f"Current: {min_val} - {max_val}")
            print("Valid: 0.0 - 1.0 (Lower=focused, Higher=diverse)")
            print("Recommended: 0.7-0.9 (focused), 0.85-0.95 (balanced), 0.9-1.0 (diverse)")
            
            if mode == 'incremental':
                print("Note: First scene uses min value, last scene uses max value")
            elif mode == 'random':
                print("Note: Each scene gets random value within this range")
            
            try:
                min_p = input(f"Min top-p [{min_val}]: ").strip()
                min_p = float(min_p) if min_p else min_val
                
                max_p = input(f"Max top-p [{max_val}]: ").strip()
                max_p = float(max_p) if max_p else max_val
                
                if min_p > max_p:
                    min_p, max_p = max_p, min_p
                    print("Swapped min/max values")
                
                if 0.0 <= min_p <= 1.0 and 0.0 <= max_p <= 1.0:
                    self.workshop.current_settings['top_p_range'] = (min_p, max_p)
                    # Update individual top_p to middle of range
                    self.workshop.current_settings['top_p'] = (min_p + max_p) / 2
                    print(f"Top-p range: {min_p} - {max_p}")
                    
                    # Give feedback
                    if max_p <= 0.8:
                        print("Low top-p range: Very focused vocabulary")
                    elif max_p <= 0.95:
                        print("Moderate top-p range: Good balance")
                    else:
                        print("High top-p range: Maximum vocabulary diversity")
                else:
                    print("Values must be 0.0 - 1.0")
            except ValueError:
                print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _configure_top_k_range(self):
        """Configure top-k range or fixed value based on current mode"""
        mode = self.workshop.current_settings.get('parameter_mode', 'fixed')
        
        if mode == 'fixed':
            # For fixed mode, just ask for a single top-k value
            current_top_k = self.workshop.current_settings.get('top_k', 40)
            
            print(f"\nTOP-K (FIXED MODE)")
            print("="*20)
            print(f"Current: {current_top_k}")
            print("Common: 10-80 (Lower=focused, Higher=diverse)")
            print("Recommended: 20-40 (focused), 30-60 (balanced), 50-100 (diverse)")
            
            try:
                top_k_input = input(f"Top-k [{current_top_k}]: ").strip()
                if top_k_input:
                    new_top_k = int(top_k_input)
                    if new_top_k >= 1:
                        self.workshop.current_settings['top_k'] = new_top_k
                        # Also set the range to the same value for consistency
                        self.workshop.current_settings['top_k_range'] = (new_top_k, new_top_k)
                        print(f"Fixed top-k: {new_top_k}")
                        
                        # Give feedback
                        if new_top_k <= 30:
                            print("Low top-k: Very focused word selection")
                        elif new_top_k <= 70:
                            print("Moderate top-k: Good balance")
                        else:
                            print("High top-k: Maximum word choice diversity")
                    else:
                        print("Top-k must be 1 or greater")
            except ValueError:
                print("Invalid input")
        
        else:
            # For incremental/random modes, ask for min and max range
            current_range = self.workshop.current_settings.get('top_k_range')
            
            # Handle different formats and None values
            if current_range is None:
                current_top_k = self.workshop.current_settings.get('top_k', 40)
                min_val, max_val = current_top_k, current_top_k
            elif isinstance(current_range, dict):
                # Dictionary format: {'min': 30, 'max': 50}
                min_val = int(current_range.get('min', 40))
                max_val = int(current_range.get('max', 40))
            elif isinstance(current_range, (list, tuple)) and len(current_range) >= 2:
                # Tuple/list format: (30, 50)
                min_val, max_val = int(current_range[0]), int(current_range[1])
            else:
                # Fallback to individual setting
                current_top_k = self.workshop.current_settings.get('top_k', 40)
                min_val, max_val = current_top_k, current_top_k
            
            # Store as tuple for consistency
            current_range = (min_val, max_val)
            self.workshop.current_settings['top_k_range'] = current_range
            
            print(f"\nTOP-K RANGE ({mode.upper()} MODE)")
            print("="*30)
            print(f"Current: {min_val} - {max_val}")
            print("Common: 10-80 (Lower=focused, Higher=diverse)")
            print("Recommended: 20-40 (focused), 30-60 (balanced), 50-100 (diverse)")
            
            if mode == 'incremental':
                print("Note: First scene uses min value, last scene uses max value")
            elif mode == 'random':
                print("Note: Each scene gets random value within this range")
            
            try:
                min_k = input(f"Min top-k [{min_val}]: ").strip()
                min_k = int(min_k) if min_k else min_val
                
                max_k = input(f"Max top-k [{max_val}]: ").strip()
                max_k = int(max_k) if max_k else max_val
                
                if min_k > max_k:
                    min_k, max_k = max_k, min_k
                    print("Swapped min/max values")
                
                if min_k >= 1 and max_k >= 1:
                    self.workshop.current_settings['top_k_range'] = (min_k, max_k)
                    # Update individual top_k to middle of range
                    self.workshop.current_settings['top_k'] = int((min_k + max_k) / 2)
                    print(f"Top-k range: {min_k} - {max_k}")
                    
                    # Give feedback
                    if max_k <= 30:
                        print("Low top-k range: Very focused word selection")
                    elif max_k <= 70:
                        print("Moderate top-k range: Good balance")
                    else:
                        print("High top-k range: Maximum word choice diversity")
                else:
                    print("Values must be 1 or greater")
            except ValueError:
                print("Invalid input")
        
        input("Press Enter to continue...")
    
    def _configure_timeout(self):
        """Configure timeout"""
        config = self.workshop.model_tester.test_config
        
        print(f"\nTIMEOUT CONFIGURATION")
        print("="*30)
        print(f"Current: {self.workshop.model_tester.get_timeout_display()}")
        print("Options: 0=Unlimited, 300=5min, 600=10min, 1800=30min, 3600=1hour")
        print("Recommendation: 600s (10min) for most models")
        
        try:
            timeout = input(f"Timeout seconds [{config.get('timeout_seconds', 0)}]: ").strip()
            if timeout:
                timeout_val = int(timeout)
                if timeout_val >= 0:
                    config['timeout_seconds'] = timeout_val
                    print(f"Timeout: {self.workshop.model_tester.get_timeout_display()}")
                    if timeout_val == 0:
                        print("Warning: Unlimited timeout - may take very long with large models")
                    elif timeout_val < 300:
                        print("Warning: Short timeout - large models may not complete")
                    else:
                        print("Good timeout setting for most scenarios")
                else:
                    print("Timeout must be 0 or positive")
        except ValueError:
            print("Invalid timeout")
        
        input("Press Enter to continue...")
    
    def _quick_parameter_presets(self):
        """Quick parameter presets for common scenarios"""
        print("\nPARAMETER PRESETS")
        print("="*30)
        
        presets = [
            ("Conservative Writing", (0.3, 0.5), (0.7, 0.85), (20, 30), 'fixed', "Predictable, focused output"),
            ("Balanced Creative", (0.7, 0.9), (0.85, 0.95), (35, 50), 'fixed', "Good creativity/consistency balance"),
            ("High Creativity", (1.0, 1.3), (0.9, 0.98), (50, 70), 'fixed', "Very creative, more unpredictable"),
            ("Explore Conservative", (0.4, 0.8), (0.75, 0.9), (25, 45), 'random', "Test range of conservative settings"),
            ("Explore Creative", (0.8, 1.4), (0.85, 0.98), (40, 80), 'random', "Test range of creative settings"),
            ("Progressive Build", (0.5, 1.2), (0.8, 0.95), (30, 60), 'incremental', "Start conservative, end creative")
        ]
        
        for i, (name, temp, top_p, top_k, mode, desc) in enumerate(presets, 1):
            print(f"{i}. {name}")
            print(f"   {desc}")
            print(f"   Mode: {mode.title()}, T:{temp[0]}-{temp[1]}, P:{top_p[0]}-{top_p[1]}, K:{top_k[0]}-{top_k[1]}")
            print()
        
        try:
            choice = int(input(f"Select preset (1-{len(presets)}, 0 to cancel): "))
            
            if choice == 0:
                return
            elif 1 <= choice <= len(presets):
                name, temp, top_p, top_k, mode, desc = presets[choice - 1]
                
                # Set the parameter mode
                self.workshop.current_settings['parameter_mode'] = mode
                
                # Set the ranges (for all modes)
                self.workshop.current_settings['temperature_range'] = {'min': temp[0], 'max': temp[1]}
                self.workshop.current_settings['top_p_range'] = {'min': top_p[0], 'max': top_p[1]}  
                self.workshop.current_settings['top_k_range'] = {'min': top_k[0], 'max': top_k[1]}
                
                # Use the middle of the range
                mid_temp = (temp[0] + temp[1]) / 2
                mid_top_p = (top_p[0] + top_p[1]) / 2
                mid_top_k = int((top_k[0] + top_k[1]) / 2)

                self.workshop.current_settings['temperature'] = round(mid_temp, 2)
                self.workshop.current_settings['top_p'] = round(mid_top_p, 2)
                self.workshop.current_settings['top_k'] = mid_top_k
                
                # IMPORTANT: For fixed mode, also set the actual parameter values
                if mode == 'fixed':
                    # Use the middle of the range for fixed mode, or the min value
                    self.workshop.current_settings['temperature'] = mid_temp  # Use middle for consistency
                    self.workshop.current_settings['top_p'] = mid_top_p
                    self.workshop.current_settings['top_k'] = mid_top_k
                    
                    print(f"Applied preset: {name}")
                    print(f"Description: {desc}")
                    print(f"Mode: {mode.title()}")
                    print(f"Fixed values: T={mid_temp}, P={mid_top_p}, K={mid_top_k}")
                else:
                    # For incremental/random modes, just confirm the ranges
                    print(f"Applied preset: {name}")
                    print(f"Description: {desc}")
                    print(f"Mode: {mode.title()}")
                    print(f"Ranges: T:{temp[0]}-{temp[1]}, P:{top_p[0]}-{top_p[1]}, K:{top_k[0]}-{top_k[1]}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    def preview_parameter_progression(self):
        """Preview parameter progression with detailed explanations"""
        scene_count = self.workshop.current_settings['scene_count']
        mode = self.workshop.current_settings['parameter_mode']
        
        print(f"\nPARAMETER PROGRESSION PREVIEW")
        print("="*50)
        print(f"Mode: {mode.title()}")
        print(f"Scene count: {scene_count}")
        print(f"Current ranges: {self.get_parameter_display()}")
        print()
        
        if mode == 'fixed':
            params = self.get_parameter_values(0)
            print("All scenes will use identical parameters:")
            print(f"  Temperature: {params['temperature']} (consistency across all scenes)")
            print(f"  Top-p: {params['top_p']}")
            print(f"  Top-k: {params['top_k']}")
            print()
            print("Use this mode when you want consistent style and tone.")
        
        elif mode == 'incremental':
            print("Parameters will gradually change from first to last scene:")
            preview_count = min(scene_count, 8)
            
            for i in range(preview_count):
                params = self.get_parameter_values(i)
                progress = i / (scene_count - 1) if scene_count > 1 else 0
                print(f"  Scene {i+1:2d}: T={params['temperature']:4.2f}, P={params['top_p']:4.2f}, K={params['top_k']:2d} ({progress*100:.0f}% progression)")
            
            if scene_count > 8:
                print(f"  ... and {scene_count - 8} more scenes with continuing progression")
            
            print()
            print("Use this mode to see how parameter changes affect style evolution.")
        
        elif mode == 'random':
            print("Each scene will get random parameters within your ranges:")
            print("Example combinations (actual will vary each time):")
            
            # Use fixed seed for consistent preview
            random.seed(42)
            preview_count = min(scene_count, 8)
            for i in range(preview_count):
                params = self.get_parameter_values(i)
                print(f"  Example {i+1:2d}: T={params['temperature']:4.2f}, P={params['top_p']:4.2f}, K={params['top_k']:2d}")
            
            random.seed()  # Reset seed
            if scene_count > 8:
                print(f"  ... and {scene_count - 8} more random combinations")
            
            print()
            print("Use this mode to explore parameter space and find optimal settings.")
        
        print(f"Total scenes to generate: {scene_count}")
        
        # Estimate time
        avg_time_per_scene = 30  # seconds estimate
        total_time = scene_count * avg_time_per_scene
        if total_time > 300:  # More than 5 minutes
            minutes = total_time // 60
            print(f"Estimated generation time: ~{minutes} minutes")
            if minutes > 10:
                print("Consider reducing scene count or using faster model for testing")
        
        input("\nPress Enter to continue...")

    def _configure_model_type(self):
        """Configure model type from parameter manager"""
        print("\n🤖 MODEL TYPE CONFIGURATION")
        print("="*40)
        
        current = self.workshop.model_tester.test_config.get('is_instruct_model', False)
        model_name = self.workshop.model_tester.test_config.get('model', 'Unknown')
        
        print(f"Current model: {model_name}")
        print(f"Current type: {'Instruct' if current else 'Base'}")
        
        print("\nThis setting affects how prompts are formatted:")
        print("• Base models: Simple concatenation of system + user prompt")
        print("• Instruct models: Special formatting (ChatML, Alpaca, etc.)")
        
        choice = input(f"\nConfigure as instruct model? (y/n) [{['n','y'][current]}]: ").strip().lower()
        
        if choice == 'y':
            self.workshop.model_tester.test_config['is_instruct_model'] = True
            
            # Choose format
            print("\nSelect instruct format:")
            print("1. ChatML (Dolphin, most chat models)")
            print("2. Alpaca (Alpaca, some Llama variants)")
            print("3. Vicuna (Vicuna models)")
            
            format_choice = input("Select format (1-3) [1]: ").strip()
            
            if format_choice == '2':
                self.workshop.model_tester.test_config['instruct_format'] = 'alpaca'
                print("✅ Set to Alpaca format")
            elif format_choice == '3':
                self.workshop.model_tester.test_config['instruct_format'] = 'vicuna'
                print("✅ Set to Vicuna format")
            else:
                self.workshop.model_tester.test_config['instruct_format'] = 'chatml'
                print("✅ Set to ChatML format")
                
        elif choice == 'n':
            self.workshop.model_tester.test_config['is_instruct_model'] = False
            self.workshop.model_tester.test_config.pop('instruct_format', None)
            print("✅ Set to base model")
        
        input("Press Enter to continue...")
    
    def _configure_max_tokens(self):
        """Configure maximum output tokens"""
        current_max = self.workshop.current_settings.get('max_output_tokens', 2048)
        
        print(f"\n📏 MAXIMUM OUTPUT TOKENS")
        print("="*30)
        print(f"Current: {current_max}")
        print("Common values:")
        print("  512  = Short scenes (1-2 paragraphs)")
        print("  1024 = Medium scenes (3-5 paragraphs)")
        print("  2048 = Long scenes (full page)")
        print("  4096 = Very long scenes")
        print("  8192 = Novella-length scenes")
        print()
        print("Note: Higher values take longer and use more resources")
        print("Your current model may have limits on maximum context/output")
        
        try:
            max_tokens = input(f"Max output tokens [{current_max}]: ").strip()
            if max_tokens:
                max_val = int(max_tokens)
                if max_val >= 100:
                    self.workshop.current_settings['max_output_tokens'] = max_val
                    print(f"✅ Max output tokens: {max_val}")
                    
                    # Give feedback on the choice
                    if max_val <= 512:
                        print("💡 Short output: Good for quick tests and dialogue scenes")
                    elif max_val <= 1024:
                        print("💡 Medium output: Good balance of length and speed")
                    elif max_val <= 2048:
                        print("💡 Long output: Full scenes with rich detail")
                    elif max_val <= 4096:
                        print("💡 Very long output: In-depth storytelling")
                        print("⚠️  May take significant time to generate")
                    else:
                        print("💡 Maximum output: Novella-length content")
                        print("⚠️  Very high token count: May take very long to generate")
                        print("⚠️  Ensure your model can handle this context size")
                else:
                    print("❌ Minimum 100 tokens required")
        except ValueError:
            print("❌ Invalid number")
        
        input("Press Enter to continue...")
    
    def _configure_thinking_mode(self):
        """Configure thinking mode for reasoning models"""
        print("\n🧠 THINKING MODE CONFIGURATION")
        print("="*40)
        
        current = self.workshop.current_settings.get('disable_thinking_mode', False)
        model_name = self.workshop.model_tester.test_config.get('model', 'Unknown')
        
        print(f"Current model: {model_name}")
        print(f"Current setting: {'Disabled' if current else 'Enabled'}")
        print()
        print("Some models (Qwen2.5, DeepSeek, o1, etc.) include reasoning/thinking")
        print("steps in their output that show their thought process.")
        print()
        print("THINKING MODE ENABLED (default):")
        print("• Model shows reasoning steps and thinking process")
        print("• Output includes <thinking> tags or reasoning explanations")
        print("• Useful for understanding how the model works")
        print("• Can make output longer and more verbose")
        print()
        print("THINKING MODE DISABLED:")
        print("• Model attempts to suppress reasoning steps")
        print("• Output focuses on final answer/content only")
        print("• Cleaner, more direct responses")
        print("• Better for creative writing and storytelling")
        print()
        
        # Detect if this is likely a thinking model
        thinking_keywords = ['qwen', 'deepseek', 'reasoning', 'think', 'o1']
        likely_thinking_model = any(keyword in model_name.lower() for keyword in thinking_keywords)
        
        if likely_thinking_model:
            print(f"💡 Your model ({model_name}) appears to be a reasoning model")
            print("   that may benefit from thinking mode control.")
        
        choice = input(f"\nDisable thinking mode? (y/n) [{'y' if current else 'n'}]: ").strip().lower()
        
        if choice == 'y':
            self.workshop.current_settings['disable_thinking_mode'] = True
            print("✅ Thinking mode DISABLED - model will try to suppress reasoning steps")
            print("   Better for clean creative writing and storytelling")
        elif choice == 'n':
            self.workshop.current_settings['disable_thinking_mode'] = False
            print("✅ Thinking mode ENABLED - model will show reasoning process")
            print("   Useful for understanding model logic and problem-solving")
        else:
            print("No changes made")
        
        input("Press Enter to continue...")
    
    def generate_variations(self, base_params, count):
        """Generate parameter variations for batch generation"""
        try:
            mode = self.workshop.current_settings.get('parameter_mode', 'fixed')
            variations = []
            
            for i in range(count):
                params = self.get_parameter_values(i)
                params['mode'] = mode
                variations.append(params)
            
            return variations
            
        except Exception as e:
            print(f"Error generating variations: {e}")
            # Return fixed parameters for all scenes
            return [dict(base_params, mode='fixed') for _ in range(count)]
