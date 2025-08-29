import os

class SettingsUI:
    def __init__(self, app_instance):
        self.app = app_instance
    
    def set_max_tokens(self):
        """Set maximum tokens with helpful guidance"""
        print("\n" + "="*60)
        print("MAX TOKENS CONFIGURATION")
        print("="*60)
        print("Tokens determine the maximum length of generated stories.")
        print("More tokens = longer stories, but require more memory/time.\n")
        
        print("RECOMMENDED TOKEN SETTINGS:")
        print("┌────────────┬─────────────┬──────────────────────────────┐")
        print("│ Tokens     │ Story Length│ Memory/Hardware Requirements │")
        print("├────────────┼─────────────┼──────────────────────────────┤")
        print("│ 1,024      │ Short       │ 4GB RAM - Basic hardware    │")
        print("│ 2,048      │ Medium      │ 6GB RAM - Standard setup    │")
        print("│ 4,096      │ Long        │ 8GB RAM - Good performance  │")
        print("│ 8,192      │ Very Long   │ 12GB RAM - High-end setup   │")
        print("│ 16,384     │ Epic        │ 16GB RAM - Powerful system  │")
        print("│ 32,768     │ Novel-like  │ 24GB RAM - Workstation      │")
        print("│ 65,536     │ Book length │ 32GB RAM - Server grade     │")
        print("│ 131,072    │ Maximum     │ 64GB RAM - High-end server  │")
        print("└────────────┴─────────────┴──────────────────────────────┘")
        
        print(f"\nCurrent setting: {self.app.max_tokens:,} tokens")
        print("\nCOMMON CHOICES:")
        print("1. 1024    - Quick short stories")
        print("2. 2048    - Standard stories")
        print("3. 4096    - Detailed stories (default)")
        print("4. 8192    - Long detailed stories")
        print("5. 16384   - Epic stories (recommended for rich narratives)")
        print("6. 32768   - Very long stories")
        print("7. 65536   - Book-length stories")
        print("8. 131072  - Maximum length stories")
        print("9. Custom  - Enter your own value")
        print("10. Keep current setting")
        
        try:
            choice = input(f"\nSelect option (1-10): ").strip()
            
            token_options = {
                "1": 1024,
                "2": 2048,
                "3": 4096,
                "4": 8192,
                "5": 16384,
                "6": 32768,
                "7": 65536,
                "8": 131072
            }
            
            if choice in token_options:
                self.app.max_tokens = token_options[choice]
                self.app.settings.set("max_tokens", self.app.max_tokens)
                print(f"✓ Max tokens set to: {self.app.max_tokens:,}")
                
                if self.app.max_tokens <= 2048:
                    length_estimate = "short story (500-1000 words)"
                elif self.app.max_tokens <= 4096:
                    length_estimate = "standard story (1000-2000 words)"
                elif self.app.max_tokens <= 8192:
                    length_estimate = "long story (2000-4000 words)"
                elif self.app.max_tokens <= 16384:
                    length_estimate = "epic story (4000-8000 words)"
                elif self.app.max_tokens <= 32768:
                    length_estimate = "very long story (8000-15000 words)"
                elif self.app.max_tokens <= 65536:
                    length_estimate = "book-length story (15000-30000 words)"
                else:  # 131,072
                    length_estimate = "maximum length story (30000+ words)"
                
                print(f"  Expected output: {length_estimate}")
                
                # Add warning for very high token counts
                if self.app.max_tokens >= 65536:
                    print("  ⚠️  WARNING: Very high token count requires significant memory and time!")
                    print("     Ensure your system has adequate RAM and be prepared for long generation times.")
                    
            elif choice == "9":
                custom_tokens = int(input("Enter custom token count (1-131072): "))
                if 1 <= custom_tokens <= 131072:
                    self.app.max_tokens = custom_tokens
                    self.app.settings.set("max_tokens", self.app.max_tokens)
                    print(f"✓ Max tokens set to: {self.app.max_tokens:,}")
                    
                    # Show estimate for custom value
                    if custom_tokens <= 2048:
                        length_estimate = "short story (500-1000 words)"
                    elif custom_tokens <= 4096:
                        length_estimate = "standard story (1000-2000 words)"
                    elif custom_tokens <= 8192:
                        length_estimate = "long story (2000-4000 words)"
                    elif custom_tokens <= 16384:
                        length_estimate = "epic story (4000-8000 words)"
                    elif custom_tokens <= 32768:
                        length_estimate = "very long story (8000-15000 words)"
                    elif custom_tokens <= 65536:
                        length_estimate = "book-length story (15000-30000 words)"
                    else:
                        length_estimate = "maximum length story (30000+ words)"
                    
                    print(f"  Expected output: {length_estimate}")
                    
                    if custom_tokens >= 65536:
                        print("  ⚠️  WARNING: Very high token count requires significant memory and time!")
                else:
                    print("❌ Invalid token count. Must be between 1 and 131,072.")
            elif choice == "10":
                print(f"✓ Keeping current setting: {self.app.max_tokens:,} tokens")
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def set_temperature(self):
        """Set temperature (creativity/randomness)"""
        print("\n" + "="*60)
        print("TEMPERATURE SETTING (Creativity Control)")
        print("="*60)
        print("Temperature controls how creative/random the AI responses are.")
        print("Lower = more focused and consistent")
        print("Higher = more creative and unpredictable\n")
        
        print("RECOMMENDED SETTINGS:")
        print("┌─────────────┬─────────────────┬────────────────────────────┐")
        print("│ Temperature │ Style           │ Best for                   │")
        print("├─────────────┼─────────────────┼────────────────────────────┤")
        print("│ 0.1-0.3     │ Very focused    │ Technical, factual stories │")
        print("│ 0.4-0.6     │ Balanced        │ Consistent narratives      │")
        print("│ 0.7-0.9     │ Creative        │ Imaginative stories        │")
        print("│ 1.0-1.2     │ Very creative   │ Experimental fiction       │")
        print("│ 1.3+        │ Chaotic         │ Surreal, abstract stories  │")
        print("└─────────────┴─────────────────┴────────────────────────────┘")
        
        print(f"\nCurrent: {self.app.temperature}")
        print("\n1. Conservative (0.3) - Very focused")
        print("2. Balanced (0.6) - Consistent")
        print("3. Creative (0.8) - Imaginative")
        print("4. Experimental (1.0) - Very creative")
        print("5. Custom - Enter your own")
        print("6. Keep current")
        
        try:
            choice = input("Select (1-6): ").strip()
            
            if choice == "1":
                self.app.temperature = 0.3
                self.app.settings.set("temperature", self.app.temperature)
            elif choice == "2":
                self.app.temperature = 0.6
                self.app.settings.set("temperature", self.app.temperature)
            elif choice == "3":
                self.app.temperature = 0.8
                self.app.settings.set("temperature", self.app.temperature)
            elif choice == "4":
                self.app.temperature = 1.0
                self.app.settings.set("temperature", self.app.temperature)
            elif choice == "5":
                temp = float(input("Enter temperature (0.0-2.0): "))
                if 0.0 <= temp <= 2.0:
                    self.app.temperature = temp
                    self.app.settings.set("temperature", self.app.temperature)
                else:
                    print("❌ Temperature should be between 0.0 and 2.0")
                    input("Press Enter to continue...")
                    return
            elif choice == "6":
                print(f"✓ Keeping current: {self.app.temperature}")
                input("Press Enter to continue...")
                return
            else:
                print("❌ Invalid choice")
                input("Press Enter to continue...")
                return
                
            print(f"✓ Temperature set to: {self.app.temperature}")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def set_top_p(self):
        """Set top-p (nucleus sampling)"""
        print("\n" + "="*60)
        print("TOP-P SETTING (Nucleus Sampling)")
        print("="*60)
        print("Top-p controls vocabulary diversity by considering only")
        print("the most probable tokens that sum to this percentage.\n")
        
        print("RECOMMENDED SETTINGS:")
        print("┌─────────┬─────────────────┬────────────────────────────┐")
        print("│ Top-p   │ Vocabulary      │ Best for                   │")
        print("├─────────┼─────────────────┼────────────────────────────┤")
        print("│ 0.5     │ Very limited    │ Formal, structured writing │")
        print("│ 0.7     │ Moderate        │ Professional stories       │")
        print("│ 0.9     │ Diverse         │ Creative storytelling      │")
        print("│ 0.95    │ Very diverse    │ Experimental writing       │")
        print("│ 1.0     │ No limit        │ Maximum creativity         │")
        print("└─────────┴─────────────────┴────────────────────────────┘")
        
        print(f"\nCurrent: {self.app.top_p}")
        
        try:
            value = input("Enter top-p value (0.1-1.0, or press Enter to keep current): ").strip()
            if not value:
                print(f"✓ Keeping current: {self.app.top_p}")
            else:
                value = float(value)
                if 0.1 <= value <= 1.0:
                    self.app.top_p = value
                    self.app.settings.set("top_p", self.app.top_p)
                    print(f"✓ Top-p set to: {self.app.top_p}")
                else:
                    print("❌ Top-p should be between 0.1 and 1.0")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def set_top_k(self):
        """Set top-k (token filtering)"""
        print("\n" + "="*60)
        print("TOP-K SETTING (Token Filtering)")
        print("="*60)
        print("Top-k limits the AI to consider only the K most likely")
        print("next tokens. Lower values = more focused responses.\n")
        
        print("RECOMMENDED SETTINGS:")
        print("┌─────────┬─────────────────┬────────────────────────────┐")
        print("│ Top-k   │ Token Pool      │ Best for                   │")
        print("├─────────┼─────────────────┼────────────────────────────┤")
        print("│ 10-20   │ Very focused    │ Technical, precise writing │")
        print("│ 30-50   │ Balanced        │ Standard storytelling      │")
        print("│ 60-80   │ Creative        │ Varied, interesting prose  │")
        print("│ 100+    │ Very diverse    │ Experimental fiction       │")
        print("│ -1      │ Disabled        │ Maximum token variety      │")
        print("└─────────┴─────────────────┴────────────────────────────┘")
        
        print(f"\nCurrent: {self.app.top_k}")
        
        try:
            value = input("Enter top-k value (1-200, -1 to disable, or press Enter to keep current): ").strip()
            if not value:
                print(f"✓ Keeping current: {self.app.top_k}")
            else:
                value = int(value)
                if value == -1 or (1 <= value <= 200):
                    self.app.top_k = value
                    self.app.settings.set("top_k", self.app.top_k)
                    print(f"✓ Top-k set to: {self.app.top_k}")
                else:
                    print("❌ Top-k should be between 1-200 or -1 to disable")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def set_repeat_penalty(self):
        """Set repeat penalty"""
        print("\n" + "="*60)
        print("REPEAT PENALTY SETTING")
        print("="*60)
        print("Controls how much the AI avoids repeating words/phrases.")
        print("Higher values = less repetition, but may affect flow.\n")
        
        print("RECOMMENDED SETTINGS:")
        print("┌─────────────┬─────────────────┬────────────────────────────┐")
        print("│ Penalty     │ Repetition      │ Best for                   │")
        print("├─────────────┼─────────────────┼────────────────────────────┤")
        print("│ 1.0         │ No penalty      │ Natural flow (may repeat)  │")
        print("│ 1.05-1.1    │ Slight penalty  │ Balanced, natural stories  │")
        print("│ 1.1-1.15    │ Moderate        │ Varied vocabulary          │")
        print("│ 1.2+        │ Strong penalty  │ Highly varied (may be odd) │")
        print("└─────────────┴─────────────────┴────────────────────────────┘")
        
        print(f"\nCurrent: {self.app.repeat_penalty}")
        
        try:
            value = input("Enter repeat penalty (1.0-1.5, or press Enter to keep current): ").strip()
            if not value:
                print(f"✓ Keeping current: {self.app.repeat_penalty}")
            else:
                value = float(value)
                if 1.0 <= value <= 1.5:
                    self.app.repeat_penalty = value
                    self.app.settings.set("repeat_penalty", self.app.repeat_penalty)
                    print(f"✓ Repeat penalty set to: {self.app.repeat_penalty}")
                else:
                    print("❌ Repeat penalty should be between 1.0 and 1.5")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def set_seed(self):
        """Set seed for reproducibility"""
        print("\n" + "="*60)
        print("SEED SETTING (Reproducibility)")
        print("="*60)
        print("Seeds control randomness. Same seed = identical results.")
        print("Useful for testing or getting consistent outputs.\n")
        
        print("OPTIONS:")
        print("• Random (None) - Different story each time")
        print("• Fixed number - Same story with same inputs")
        print("• Useful for A/B testing different prompts")
        
        print(f"\nCurrent: {self.app.seed or 'Random'}")
        print("\n1. Keep random (recommended for variety)")
        print("2. Set fixed seed for reproducibility")
        print("3. Generate random seed and use it")
        
        try:
            choice = input("Select (1-3): ").strip()
            
            if choice == "1":
                self.app.seed = None
                self.app.settings.set("seed", self.app.seed)
                print("✓ Using random seeds")
            elif choice == "2":
                seed_value = int(input("Enter seed number (any integer): "))
                self.app.seed = seed_value
                self.app.settings.set("seed", self.app.seed)
                print(f"✓ Seed set to: {self.app.seed}")
            elif choice == "3":
                import random
                self.app.seed = random.randint(1, 1000000)
                self.app.settings.set("seed", self.app.seed)
                print(f"✓ Generated seed: {self.app.seed}")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def set_num_runs(self):
        """Set number of story runs"""
        try:
            runs = int(input(f"Enter number of runs 1-20 (current: {self.app.num_runs}): "))
            if 1 <= runs <= 20:
                self.app.num_runs = runs
                self.app.settings.set("num_runs", self.app.num_runs)
                print(f"✓ Number of runs set to: {self.app.num_runs}")
            else:
                print("❌ Invalid number. Must be between 1-20.")
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")

    def set_storyboard_reuse(self):
        """Set storyboard reuse behavior"""
        print("\n" + "="*60)
        print("STORYBOARD REUSE SETTINGS")
        print("="*60)
        print("Control whether to reuse existing storyboard files or create new ones.\n")
        
        print("REUSE OPTIONS:")
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│ Option │ Story Bible      │ Scene Plan       │ Result        │")
        print("├────────┼──────────────────┼──────────────────┼───────────────┤")
        print("│ 1      │ Create New       │ Create New       │ Fresh story   │")
        print("│ 2      │ Reuse Existing   │ Create New       │ Same plot,    │")
        print("│        │                  │                  │ new scenes    │")
        print("│ 3      │ Reuse Existing   │ Reuse Existing   │ Identical     │")
        print("│        │                  │                  │ structure     │")
        print("└────────┴──────────────────┴──────────────────┴───────────────┘")
        
        print(f"\nCurrent setting: ", end="")
        if self.app.storyboard_reuse_mode == "new":
            print("Create new story bible & scene plan")
        elif self.app.storyboard_reuse_mode == "bible_only":
            print("Reuse story bible, create new scene plan")
        elif self.app.storyboard_reuse_mode == "both":
            print("Reuse both story bible & scene plan")
        
        print("\nSelect option:")
        print("1. Create new story bible & scene plan (default)")
        print("2. Reuse story bible, create new scene plan")
        print("3. Reuse both story bible & scene plan")
        print("4. Keep current setting")
        
        try:
            choice = input("Select (1-4): ").strip()
            
            if choice == "1":
                self.app.storyboard_reuse_mode = "new"
                self.app.settings.set("storyboard_reuse_mode", self.app.storyboard_reuse_mode)
                print("✓ Set to: Create new story bible & scene plan")
            elif choice == "2":
                self.app.storyboard_reuse_mode = "bible_only"
                self.app.settings.set("storyboard_reuse_mode", self.app.storyboard_reuse_mode)
                print("✓ Set to: Reuse story bible, create new scene plan")
            elif choice == "3":
                self.app.storyboard_reuse_mode = "both"
                self.app.settings.set("storyboard_reuse_mode", self.app.storyboard_reuse_mode)
                print("✓ Set to: Reuse both story bible & scene plan")
            elif choice == "4":
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def toggle_auto_audio(self):
        """Toggle automatic audio generation after story creation"""
        print("\n" + "="*60)
        print("AUTO-GENERATE AUDIO SETTING")
        print("="*60)
        print("When enabled, audio files will be automatically generated")
        print("after each story is created (requires F5-TTS setup).\n")
        
        # Check current F5-TTS reference audio status
        ref_audio = self.app.settings.get('f5tts_selected_ref')
        current_auto = self.app.auto_generate_audio
        
        if ref_audio:
            ref_filename = os.path.basename(ref_audio)
            ref_name = os.path.splitext(ref_filename)[0]
            print(f"✓ F5-TTS reference audio: {ref_name}")
            print(f"Current setting: {'Enabled' if current_auto else 'Disabled'}")
            
            print("\n1. Enable auto-generate audio")
            print("2. Disable auto-generate audio")
            print("3. Keep current setting")
            
            try:
                choice = input("Select (1-3): ").strip()
                
                if choice == "1":
                    self.app.auto_generate_audio = True
                    self.app.settings.set("auto_generate_audio", True)
                    print(f"✓ Auto-generate audio enabled with reference: {ref_name}")
                elif choice == "2":
                    self.app.auto_generate_audio = False
                    self.app.settings.set("auto_generate_audio", False)
                    print("✓ Auto-generate audio disabled")
                elif choice == "3":
                    print("✓ Keeping current setting")
                else:
                    print("❌ Invalid choice")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("❌ No F5-TTS reference audio selected!")
            print("Cannot enable auto-generate audio without reference audio.")
            print("\nOptions:")
            print("1. Go to F5-TTS settings to select reference audio")
            print("2. Force enable (will fail during generation)")
            print("3. Keep disabled")
            
            try:
                choice = input("Select (1-3): ").strip()
                
                if choice == "1":
                    print("👉 Go to F5-TTS Audio Generation (option 14) to select reference audio first.")
                elif choice == "2":
                    confirm = input("⚠️  This will enable auto-audio but it will fail without reference audio. Continue? (y/n): ").strip().lower()
                    if confirm == 'y':
                        self.app.auto_generate_audio = True
                        self.app.settings.set("auto_generate_audio", True)
                        print("⚠️  Auto-generate audio enabled (will fail without reference audio)")
                    else:
                        print("✓ Cancelled")
                elif choice == "3":
                    self.app.auto_generate_audio = False
                    self.app.settings.set("auto_generate_audio", False)
                    print("✓ Auto-generate audio remains disabled")
                else:
                    print("❌ Invalid choice")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def toggle_thinking_mode(self):
        """Toggle thinking mode for models that support reasoning display"""
        print("\n" + "="*60)
        print("THINKING MODE CONFIGURATION")
        print("="*60)
        print("Thinking mode controls whether you see the model's reasoning process.")
        print("This is useful for thinking/reasoning models that show their work.\n")
        
        current_enabled = self.app.thinking_mode_enabled
        
        if current_enabled:
            print("CURRENTLY ENABLED")
            print("• Shows the model's step-by-step reasoning")
            print("• Longer, more detailed responses")
            print("• Helpful for understanding the model's logic")
            print("• May include thinking artifacts like <thinking>...</thinking> tags")
            print()
            print("Disable thinking mode?")
            print("• Only final answers will be shown")
            print("• Shorter, cleaner responses")
            print("• Hides the reasoning process")
        else:
            print("CURRENTLY DISABLED")
            print("• Only final answers are shown")
            print("• Shorter, cleaner responses")
            print("• Reasoning process is hidden")
            print()
            print("Enable thinking mode?")
            print("• Shows the model's step-by-step reasoning")
            print("• More detailed responses")
            print("• Helpful for debugging story quality issues")
        
        print(f"\n1. {'Disable' if current_enabled else 'Enable'} thinking mode")
        print("2. Keep current setting")
        
        try:
            choice = input("Select (1-2): ").strip()
            
            if choice == "1":
                self.app.thinking_mode_enabled = not current_enabled
                self.app.settings.set("thinking_mode_enabled", self.app.thinking_mode_enabled)
                
                status = "enabled" if self.app.thinking_mode_enabled else "disabled"
                print(f"✓ Thinking mode {status}")
            elif choice == "2":
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")

    def toggle_instruct_mode(self):
        """Toggle instruct mode for instruct-tuned models"""
        print("\n" + "="*60)
        print("INSTRUCT MODE CONFIGURATION")
        print("="*60)
        print("Instruct mode optimizes prompts for instruction-following models.")
        print("Best for models with 'instruct', 'chat', or 'it' in their names.\n")
        
        current_enabled = self.app.instruct_mode_enabled
        
        if current_enabled:
            print("CURRENTLY ENABLED")
            print("• Uses instruction-optimized prompt formatting")
            print("• Better for models trained on instruction datasets")
            print("• Includes clear task definitions and examples")
            print("• Best for instruct/chat models")
            print()
            print("Disable instruct mode?")
            print("• Uses standard prompt formatting")
            print("• Better for base/completion models")
            print("• More natural language prompts")
        else:
            print("CURRENTLY DISABLED")
            print("• Uses standard prompt formatting")
            print("• Better for base/completion models")
            print("• More natural language prompts")
            print()
            print("Enable instruct mode?")
            print("• Uses instruction-optimized formatting")
            print("• Better for instruct-tuned models")
            print("• Clearer task definitions")
        
        print(f"\n1. {'Disable' if current_enabled else 'Enable'} instruct mode")
        print("2. Keep current setting")
        
        try:
            choice = input("Select (1-2): ").strip()
            
            if choice == "1":
                self.app.instruct_mode_enabled = not current_enabled
                self.app.settings.set("instruct_mode_enabled", self.app.instruct_mode_enabled)
                
                status = "enabled" if self.app.instruct_mode_enabled else "disabled"
                print(f"✓ Instruct mode {status}")
            elif choice == "2":
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")

    def toggle_hide_reasoning(self):
        """Toggle hiding reasoning for thinking models"""
        print("\n" + "="*60)
        print("HIDE MODEL REASONING")
        print("="*60)
        print("This setting controls whether thinking models show their reasoning process.")
        print("It only affects models that can display their 'thinking' (like DeepSeek-R1, o1, etc.)")
        print("Regular models are unaffected by this setting.\n")
        
        currently_hidden = not self.app.thinking_mode_enabled
        
        if currently_hidden:
            print("CURRENTLY: REASONING IS HIDDEN")
            print("• Thinking models show only final answers")
            print("• Reasoning process is suppressed")
            print("• Cleaner, shorter responses")
            print("• Regular models work normally")
            print()
            print("Show reasoning from thinking models?")
            print("• See the model's step-by-step thinking")
            print("• Longer, more detailed responses")
            print("• Helpful for understanding model logic")
        else:
            print("CURRENTLY: REASONING IS SHOWN")
            print("• Thinking models show their reasoning process")
            print("• You can see step-by-step thinking")
            print("• More detailed but longer responses")
            print("• Regular models work normally")
            print()
            print("Hide reasoning from thinking models?")
            print("• Only final answers will be shown")
            print("• Shorter, cleaner responses")
            print("• Reasoning process suppressed")
        
        print(f"\n1. {'Show' if currently_hidden else 'Hide'} reasoning from thinking models")
        print("2. Keep current setting")
        
        try:
            choice = input("Select (1-2): ").strip()
            
            if choice == "1":
                # Note: We store the opposite because thinking_mode_enabled means "show reasoning"
                self.app.thinking_mode_enabled = currently_hidden
                self.app.settings.set("thinking_mode_enabled", self.app.thinking_mode_enabled)
                
                if self.app.thinking_mode_enabled:
                    print("✓ Thinking models will show their reasoning")
                else:
                    print("✓ Thinking models will hide their reasoning")
            elif choice == "2":
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")

    def toggle_reasoning_control(self):
        """Toggle reasoning control for thinking models"""
        print("\n" + "="*60)
        print("REASONING/THINKING MODEL CONTROL")
        print("="*60)
        print("This setting controls what happens when using reasoning/thinking models.")
        print("Examples: DeepSeek-R1, o1, Qwen-QwQ, etc.")
        print("Regular models (like Llama, Mistral) are unaffected.\n")
        
        currently_trying_to_disable = not self.app.thinking_mode_enabled
        
        if currently_trying_to_disable:
            print("CURRENT SETTING: TRY TO DISABLE")
            print("• Attempts to hide reasoning from thinking models")
            print("• Uses model-specific control methods")
            print("• Shows only final answers")
            print("• Regular models work normally")
            print()
            print("Change to NO CHANGE?")
            print("• Let thinking models show their full reasoning")
            print("• See the model's step-by-step thinking process")
            print("• More detailed but longer responses")
        else:
            print("CURRENT SETTING: NO CHANGE")
            print("• Thinking models show their full reasoning process")
            print("• You can see step-by-step thinking")
            print("• More detailed but longer responses") 
            print("• Regular models work normally")
            print()
            print("Change to TRY TO DISABLE?")
            print("• Attempts to hide reasoning from thinking models")
            print("• Shorter, cleaner responses")
            print("• Uses model-specific suppression methods")
        
        action_text = "No change" if currently_trying_to_disable else "Try to disable"
        print(f"\n1. Change to: {action_text}")
        print("2. Keep current setting")
        
        try:
            choice = input("Select (1-2): ").strip()
            
            if choice == "1":
                # Note: We store the opposite because thinking_mode_enabled means "show reasoning"
                self.app.thinking_mode_enabled = currently_trying_to_disable
                self.app.settings.set("thinking_mode_enabled", self.app.thinking_mode_enabled)
                
                if self.app.thinking_mode_enabled:
                    print("✓ Set to: No change (thinking models will show reasoning)")
                else:
                    print("✓ Set to: Try to disable (thinking models will try to hide reasoning)")
            elif choice == "2":
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")