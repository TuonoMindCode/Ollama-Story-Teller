import json
import os
from pathlib import Path

class SceneWorkshopSettings:
    def __init__(self):
        # Move settings file to project root
        self.settings_file = Path("workshop_settings.json")
        self.old_settings_file = Path("model_testing/scene_workshop/workshop_settings.json")
        
        self.default_settings = {
            'model': None,
            'system_prompt': None,
            'system_prompt_name': 'Not selected',
            'user_prompt': None,
            'user_prompt_name': 'Not selected',
            'narrative_style': None,
            'narrative_style_name': 'Not selected',
            'writing_style': None,
            'writing_style_name': 'Not selected',
            'second_user_prompts': [],
            'second_user_prompt_names': [],
            'second_prompt_mode': 'original',
            'scene_count': 3,
            'parameter_mode': 'fixed',
            'temperature': 0.8,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048,
            'timeout_seconds': 0,
            'temperature_range': {'min': 0.1, 'max': 1.0},
            'top_p_range': {'min': 0.1, 'max': 1.0},
            'top_k_range': {'min': 1, 'max': 100},
            'disable_thinking_mode': False,
            'system_prompt_source': None,
            'user_prompt_source': None,
            'age_guidance': None,
            'age_guidance_name': 'Not selected',
            'age_guidance_text': None
        }
        
        # Initialize settings first
        self.settings = {}
        
        # Migrate existing settings if needed
        self._migrate_settings_if_needed()
        
        # Load existing settings or create defaults
        self.settings = self.load_settings()
        
        # Test save on initialization to ensure it works
        if not self.settings_file.exists() or len(self.settings) == 0:
            self.save_settings(quiet=True)
    
    def _migrate_settings_if_needed(self):
        """Migrate settings from old location to new location"""
        if self.old_settings_file.exists() and not self.settings_file.exists():
            try:
                # Copy the settings to the new location
                import shutil
                shutil.move(str(self.old_settings_file), str(self.settings_file))
                print(f"✅ Migrated workshop settings to project root: {self.settings_file}")
                
                # Clean up empty directory if possible
                try:
                    if self.old_settings_file.parent.exists() and not any(self.old_settings_file.parent.iterdir()):
                        self.old_settings_file.parent.rmdir()
                except:
                    pass  # Don't worry if we can't remove the directory
                    
            except Exception as e:
                print(f"⚠️ Could not migrate settings file: {e}")
    
    def load_settings(self):
        """Load settings from file, return defaults if file doesn't exist"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    
                # Merge with defaults to ensure all keys exist
                settings = self.default_settings.copy()
                settings.update(loaded_settings)
                
                return settings
            else:
                return self.default_settings.copy()
                
        except Exception as e:
            print(f"Warning: Could not load workshop settings ({e}). Using defaults.")
            return self.default_settings.copy()
    
    def save_settings(self, quiet=False):
        """Save current settings to file"""
        try:
            # Ensure we have valid settings to save
            if not self.settings:
                self.settings = self.default_settings.copy()
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            if not quiet:
                print(f"✅ Settings saved")
            return True
            
        except Exception as e:
            if not quiet:
                print(f"❌ Warning: Could not save workshop settings: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        success = self.save_settings()
        if success:
            print("✅ Settings reset to defaults")
        return success
    
    def reset_to_ollama_defaults(self):
        """Reset parameters to Ollama defaults"""
        ollama_defaults = {
            'temperature': 0.8,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048,
            'timeout_seconds': 0
        }
        
        # Ensure we have settings first
        if not self.settings:
            self.settings = self.default_settings.copy()
        
        # Keep other settings, just reset parameters
        self.settings.update(ollama_defaults)
        success = self.save_settings()
        if success:
            print("✅ Parameters reset to Ollama defaults")
        return success
    
    def get(self, key, default=None):
        """Get a setting value with safe fallback"""
        try:
            # Ensure settings exist
            if not hasattr(self, 'settings') or not self.settings:
                self.settings = self.default_settings.copy()
            
            # Return value or fallback to default_settings, then provided default
            if key in self.settings:
                return self.settings[key]
            elif key in self.default_settings:
                return self.default_settings[key]
            else:
                return default
                
        except Exception as e:
            return default
    
    def set(self, key, value, quiet=False):
        """Set a setting value and save"""
        try:
            # Ensure settings exist
            if not hasattr(self, 'settings') or not self.settings:
                self.settings = self.default_settings.copy()
            
            old_value = self.settings.get(key, 'Not set')
            self.settings[key] = value
            
            success = self.save_settings(quiet=True)  # Always quiet save for individual sets
            
            # Only show message if explicitly not quiet and value actually changed
            if not quiet and old_value != value:
                # Don't show the verbose change message, just confirm the action
                pass
            
            return success
            
        except Exception as e:
            if not quiet:
                print(f"Error setting '{key}': {e}")
            return False
    
    def update(self, updates, quiet=False):
        """Update multiple settings at once"""
        try:
            # Ensure settings exist
            if not hasattr(self, 'settings') or not self.settings:
                self.settings = self.default_settings.copy()
            
            self.settings.update(updates)
            success = self.save_settings(quiet=True)
            
            if success and not quiet:
                print(f"✅ Settings updated")
            return success
            
        except Exception as e:
            if not quiet:
                print(f"Error updating settings: {e}")
            return False
    
    def get_parameter_display(self):
        """Get formatted parameter display string"""
        try:
            mode = self.get('parameter_mode', 'fixed')
            
            if mode == 'fixed':
                temp = self.get('temperature', 0.8)
                top_p = self.get('top_p', 0.9)
                top_k = self.get('top_k', 40)
                max_tokens = self.get('max_output_tokens', 2048)
                return f"Fixed: T={temp}, P={top_p}, K={top_k}, MaxTokens={max_tokens}"
                
            elif mode == 'random':
                t_range = self.get('temperature_range', {'min': 0.1, 'max': 1.0})
                p_range = self.get('top_p_range', {'min': 0.1, 'max': 1.0})
                k_range = self.get('top_k_range', {'min': 1, 'max': 100})
                max_tokens = self.get('max_output_tokens', 2048)
                return f"Random: T={t_range['min']}-{t_range['max']}, P={p_range['min']}-{p_range['max']}, K={k_range['min']}-{k_range['max']}, MaxTokens={max_tokens}"
                
            else:  # linear/incremental
                t_range = self.get('temperature_range', {'min': 0.1, 'max': 1.0})
                p_range = self.get('top_p_range', {'min': 0.1, 'max': 1.0})
                k_range = self.get('top_k_range', {'min': 1, 'max': 100})
                max_tokens = self.get('max_output_tokens', 2048)
                return f"Incremental: T={t_range['min']}-{t_range['max']}, P={p_range['min']}-{p_range['max']}, K={k_range['min']}-{k_range['max']}, MaxTokens={max_tokens}"
                
        except Exception as e:
            return "Error loading parameters"
    
    def get_settings_info(self):
        """Get debug info about settings file"""
        info = {
            'settings_file': str(self.settings_file),
            'file_exists': self.settings_file.exists(),
            'directory_exists': True,  # Root directory always exists
            'can_write': os.access('.', os.W_OK),  # Check if we can write to current directory
            'settings_loaded': bool(self.settings),
            'settings_count': len(self.settings) if self.settings else 0
        }
        
        if self.settings_file.exists():
            try:
                info['file_size'] = self.settings_file.stat().st_size
                info['file_modified'] = self.settings_file.stat().st_mtime
            except:
                info['file_size'] = 'Unknown'
                info['file_modified'] = 'Unknown'
        
        return info
