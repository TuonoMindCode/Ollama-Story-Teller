class VariationConfigurator:
    def set_story_variations(self, current_variations):
        """Set number of story variations to generate"""
        print("\n" + "="*60)
        print("STORY VARIATIONS")
        print("="*60)
        print("How many different stories to generate using the same blueprint:\n")
        
        print(f"Current: {current_variations} {'story' if current_variations == 1 else 'stories'}")
        
        try:
            variations = int(input(f"Enter number of stories (1-20, current: {current_variations}): "))
            if 1 <= variations <= 20:
                print(f"✓ Will generate {variations} {'story' if variations == 1 else 'stories'}")
                result = variations
            else:
                print("❌ Invalid number. Must be between 1-20.")
                result = current_variations
        except ValueError:
            print("❌ Invalid input.")
            result = current_variations
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_variations
        
        input("\nPress Enter to continue...")
        return result
    
    def show_advanced_llm_settings(self, app):
        """Enhanced advanced LLM settings with token distribution controls"""
        # Initialize token distribution settings if they don't exist
        if not hasattr(app, 'bible_tokens_mode'):
            app.bible_tokens_mode = 'auto'
            app.scene_plan_tokens_mode = 'auto'
            app.scene_writing_tokens_mode = 'auto'
            app.manual_bible_tokens = 20000
            app.manual_plan_tokens = 10000
            app.manual_scene_tokens = 16000
    
        while True:
            # Calculate auto token distribution
            total_tokens = app.max_tokens
            auto_bible_tokens = min(total_tokens // 7, 20000)
            auto_plan_tokens = min(total_tokens // 12, 10000)
            auto_scene_tokens = min(total_tokens // 8, 16000)
            
            # Determine actual tokens being used
            bible_tokens = auto_bible_tokens if app.bible_tokens_mode == 'auto' else app.manual_bible_tokens
            plan_tokens = auto_plan_tokens if app.scene_plan_tokens_mode == 'auto' else app.manual_plan_tokens
            scene_tokens = auto_scene_tokens if app.scene_writing_tokens_mode == 'auto' else app.manual_scene_tokens
            
            print("\n" + "="*60)
            print("ADVANCED LLM SETTINGS")
            print("="*60)
            
            print(f"1. Model: {app.selected_model or 'None selected'}")
            print(f"2. Total tokens: {app.max_tokens:,}")
            
            # Token distribution section
            print(f"\n📊 TOKEN DISTRIBUTION:")
            print(f"3. Story Bible: {bible_tokens:,} tokens ({app.bible_tokens_mode})")
            if app.bible_tokens_mode == 'auto':
                print(f"   └─ Auto formula: {total_tokens:,} ÷ 7 = ~{auto_bible_tokens:,} tokens (~{auto_bible_tokens * 0.75:.0f} words)")
            else:
                print(f"   └─ Manual setting: {app.manual_bible_tokens:,} tokens (~{app.manual_bible_tokens * 0.75:.0f} words)")
            
            print(f"4. Scene Plan: {plan_tokens:,} tokens ({app.scene_plan_tokens_mode})")
            if app.scene_plan_tokens_mode == 'auto':
                print(f"   └─ Auto formula: {total_tokens:,} ÷ 12 = ~{auto_plan_tokens:,} tokens (~{auto_plan_tokens * 0.75:.0f} words)")
            else:
                print(f"   └─ Manual setting: {app.manual_plan_tokens:,} tokens (~{app.manual_plan_tokens * 0.75:.0f} words)")
            
            print(f"5. Scene Writing: {scene_tokens:,} tokens ({app.scene_writing_tokens_mode})")
            if app.scene_writing_tokens_mode == 'auto':
                print(f"   └─ Auto formula: {total_tokens:,} ÷ 8 = ~{auto_scene_tokens:,} tokens (~{auto_scene_tokens * 0.75:.0f} words per scene)")
            else:
                print(f"   └─ Manual setting: {app.manual_scene_tokens:,} tokens (~{app.manual_scene_tokens * 0.75:.0f} words per scene)")
            
            # Show total token usage estimate
            total_used = bible_tokens + plan_tokens + scene_tokens
            usage_percent = (total_used / total_tokens * 100) if total_tokens > 0 else 0
            print(f"   📈 Estimated usage per story: {total_used:,} tokens ({usage_percent:.1f}% of available)")
            
    #    defaults = self._get_default_values()
            
            print(f"\n⚙️ GENERATION PARAMETERS:")
            print(f"6. Temperature: {app.temperature} (Ollama default: 0.8, range: 0.0-2.0)")
            print(f"   └─ Controls creativity/randomness. Lower = more focused, Higher = more creative")
            
            print(f"7. Top-p: {app.top_p} (Ollama default: 0.9, range: 0.0-1.0)")
            print(f"   └─ Nucleus sampling. Lower = more focused vocabulary, Higher = more diverse")
            
            print(f"8. Top-k: {app.top_k} (Ollama default: 40, range: 1-100)")
            print(f"   └─ Limits vocabulary to top K tokens. Lower = more focused, Higher = more variety")
            
            print(f"9. Repeat penalty: {app.repeat_penalty} (Ollama default: 1.1, range: 1.0-2.0)")
            print(f"   └─ Reduces repetition. 1.0 = no penalty, Higher = less repetitive")
            
            print(f"10. Seed: {app.seed or 'Random'} (Ollama default: Random)")
            print(f"   └─ Controls randomness. Same seed = reproducible results")
            
            print(f"\n🔧 OTHER SETTINGS:")
            print(f"11. Storyboard reuse: {self._get_reuse_mode_display(app.storyboard_reuse_mode)}")
            print(f"12. Auto-generate audio (F5-TTS): {'Enabled' if app.auto_generate_audio else 'Disabled'}")
            if app.auto_generate_audio:
                print(f"    └─ Will automatically convert generated stories to speech using F5-TTS")
            else:
                print(f"    └─ Stories will be text-only (enable to add F5-TTS audio generation)")
            
            print(f"\n13. Reset all parameters to Ollama defaults")
            print(f"14. Reset token distribution to auto")
            print(f"15. Back to story generation menu")
            
            choice = input(f"\nSelect option (1-15): ").strip()
            
            try:
                if choice == "1":
                    self._select_model(app)
                elif choice == "2":
                    self._set_total_tokens(app)
                elif choice == "3":
                    self._configure_bible_tokens(app, auto_bible_tokens)
                elif choice == "4":
                    self._configure_plan_tokens(app, auto_plan_tokens)
                elif choice == "5":
                    self._configure_scene_tokens(app, auto_scene_tokens)
                elif choice == "6":
                    self._set_temperature(app)
                elif choice == "7":
                    self._set_top_p(app)
                elif choice == "8":
                    self._set_top_k(app)
                elif choice == "9":
                    self._set_repeat_penalty(app)
                elif choice == "10":
                    self._set_seed(app)
                elif choice == "11":
                    self._configure_storyboard_reuse(app)
                elif choice == "12":
                    self._toggle_f5_tts_audio(app)
                elif choice == "13":
                    self._reset_all_to_defaults(app)
                elif choice == "14":
                    self._reset_token_distribution(app)
                elif choice == "15":
                    break
                else:
                    print("❌ Invalid option")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Press Enter to continue...")
    
    def _get_default_values(self):
        """Get the actual default values used by this app"""
        return {
            'temperature': 0.8,
            'top_p': 0.8,      # Your app uses 0.8, not Ollama's 0.9
            'top_k': 40,
            'repeat_penalty': 1.1,
            'seed': None
        }

    def _configure_bible_tokens(self, app, auto_value):
        """Configure story bible token settings"""
        print(f"\n📖 STORY BIBLE TOKEN CONFIGURATION")
        print(f"Current: {auto_value:,} tokens (auto) - approximately {auto_value * 0.75:.0f} words")
        print(f"This controls how comprehensive and detailed the story bible will be.")
        print(f"The story bible establishes characters, world, tone, and plot foundation.")
        print(f"\n1. Keep auto ({auto_value:,} tokens)")
        print(f"2. Set manual amount")
        print(f"3. Back")
        
        choice = input("Select option: ").strip()
        if choice == "1":
            app.bible_tokens_mode = 'auto'
            print("✓ Story bible tokens set to auto")
        elif choice == "2":
            try:
                max_allowed = app.max_tokens // 2
                tokens = int(input(f"Enter bible tokens (2000-{max_allowed}): "))
                if 2000 <= tokens <= max_allowed:
                    app.bible_tokens_mode = 'manual'
                    app.manual_bible_tokens = tokens
                    print(f"✓ Story bible tokens set to {tokens:,} (manual)")
                    print(f"   Expected bible length: ~{tokens * 0.75:.0f} words")
                else:
                    print(f"❌ Invalid token count. Must be between 2,000 and {max_allowed:,}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _configure_plan_tokens(self, app, auto_value):
        """Configure scene plan token settings"""
        print(f"\n📋 SCENE PLAN TOKEN CONFIGURATION")  
        print(f"Current: {auto_value:,} tokens (auto) - approximately {auto_value * 0.75:.0f} words")
        print(f"This controls how detailed the scene-by-scene breakdown will be.")
        print(f"The scene plan structures the entire story flow and pacing.")
        print(f"\n1. Keep auto ({auto_value:,} tokens)")
        print(f"2. Set manual amount")
        print(f"3. Back")
        
        choice = input("Select option: ").strip()
        if choice == "1":
            app.scene_plan_tokens_mode = 'auto'
            print("✓ Scene plan tokens set to auto")
        elif choice == "2":
            try:
                max_allowed = app.max_tokens // 3
                tokens = int(input(f"Enter plan tokens (1500-{max_allowed}): "))
                if 1500 <= tokens <= max_allowed:
                    app.scene_plan_tokens_mode = 'manual'
                    app.manual_plan_tokens = tokens
                    print(f"✓ Scene plan tokens set to {tokens:,} (manual)")
                    print(f"   Expected plan length: ~{tokens * 0.75:.0f} words")
                else:
                    print(f"❌ Invalid token count. Must be between 1,500 and {max_allowed:,}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _configure_scene_tokens(self, app, auto_value):
        """Configure scene writing token settings"""
        print(f"\n✍️ SCENE WRITING TOKEN CONFIGURATION")
        print(f"Current: {auto_value:,} tokens (auto) - approximately {auto_value * 0.75:.0f} words per scene")
        print(f"This controls how long and detailed each individual scene will be.")
        print(f"\nScene length guide:")
        print(f"• 2,000-4,000 tokens = Short scenes (1,500-3,000 words)")
        print(f"• 6,000-10,000 tokens = Medium scenes (4,500-7,500 words)")
        print(f"• 12,000-16,000 tokens = Long scenes (9,000-12,000 words)")
        print(f"• 20,000+ tokens = Very long scenes (15,000+ words)")
        print(f"\n1. Keep auto ({auto_value:,} tokens)")
        print(f"2. Set manual amount")
        print(f"3. Back")
        
        choice = input("Select option: ").strip()
        if choice == "1":
            app.scene_writing_tokens_mode = 'auto'
            print("✓ Scene writing tokens set to auto")
        elif choice == "2":
            try:
                max_allowed = app.max_tokens // 2
                tokens = int(input(f"Enter scene tokens (1000-{max_allowed}): "))
                if 1000 <= tokens <= max_allowed:
                    app.scene_writing_tokens_mode = 'manual'
                    app.manual_scene_tokens = tokens
                    print(f"✓ Scene writing tokens set to {tokens:,} (manual)")
                    print(f"   Expected scene length: ~{tokens * 0.75:.0f} words each")
                else:
                    print(f"❌ Invalid token count. Must be between 1,000 and {max_allowed:,}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def _reset_token_distribution(self, app):
        """Reset all token settings to auto"""
        app.bible_tokens_mode = 'auto'
        app.scene_plan_tokens_mode = 'auto'
        app.scene_writing_tokens_mode = 'auto'
        print("✓ All token distribution settings reset to auto")
        print("  Token amounts will be automatically calculated from total tokens")
    
    def _reset_all_to_defaults(self, app):
        """Reset all LLM parameters to Ollama defaults"""
        print("\n🔄 RESET TO OLLAMA DEFAULTS")
        print("This will reset all generation parameters to Ollama's official default values:")
        print("• Temperature: 0.8")
        print("• Top-p: 0.9")  # Ollama's actual default
        print("• Top-k: 40")
        print("• Repeat penalty: 1.1")
        print("• Seed: Random")
        print("• Token distribution: Auto")
        
        confirm = input("\nReset all parameters to Ollama defaults? (y/n): ").strip().lower()
        if confirm == 'y':
            # Official Ollama defaults
            app.temperature = 0.8
            app.top_p = 0.9      # Corrected to actual Ollama default
            app.top_k = 40
            app.repeat_penalty = 1.1
            app.seed = None
            
            # Reset token distribution to auto
            app.bible_tokens_mode = 'auto'
            app.scene_plan_tokens_mode = 'auto'
            app.scene_writing_tokens_mode = 'auto'
            
            print("✅ All parameters reset to official Ollama defaults")
        else:
            print("❌ Reset cancelled")
    
    def _set_total_tokens(self, app):
        """Set total token limit"""
        print(f"\n🎯 TOTAL TOKEN CONFIGURATION")
        print(f"Current: {app.max_tokens:,} tokens")
        print(f"This is the maximum tokens available for the entire generation process.")
        print(f"\nRecommended values:")
        print(f"• 8,192 - Basic (short stories, quick generation)")
        print(f"• 32,768 - Standard (medium stories, good detail)")
        print(f"• 65,536 - High detail (long stories, comprehensive)")
        print(f"• 131,072 - Maximum detail (very long stories, extensive)")
        
        try:
            tokens = int(input("Enter total tokens (4096-131072): "))
            if 4096 <= tokens <= 131072:
                app.max_tokens = tokens
                print(f"✓ Total tokens set to {tokens:,}")
                # Reset to auto mode when total changes to recalculate distribution
                app.bible_tokens_mode = 'auto'
                app.scene_plan_tokens_mode = 'auto' 
                app.scene_writing_tokens_mode = 'auto'
                print("✓ Token distribution reset to auto (will recalculate)")
            else:
                print("❌ Token count must be between 4,096 and 131,072")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _get_reuse_mode_display(self, mode):
        """Get display text for storyboard reuse mode"""
        modes = {
            "new": "Create new story bible & scene plan",
            "bible_only": "Reuse story bible, new scene plan",
            "both": "Reuse existing story bible & scene plan"
        }
        return modes.get(mode, mode)
    
    def _select_model(self, app):
        """Select Ollama model (placeholder - implement based on your app's model selection)"""
        print("Model selection would go to your main model selection menu")
        input("Press Enter to continue...")
    
    def _configure_storyboard_reuse(self, app):
        """Configure storyboard reuse mode (placeholder)"""
        print("Storyboard reuse configuration...")
        input("Press Enter to continue...")
    
    def _set_temperature(self, app):
        """Set temperature parameter with detailed explanation"""
        print(f"\n🌡️ TEMPERATURE SETTING")
        print(f"Current: {app.temperature} (Ollama default: 0.8)")
        print(f"\nTemperature controls creativity and randomness in text generation:")
        print(f"• 0.0-0.3: Very focused, deterministic (good for technical writing)")
        print(f"• 0.4-0.7: Balanced creativity (good for most stories)")
        print(f"• 0.8-1.2: Creative and varied (Ollama default range)")
        print(f"• 1.3-2.0: Very creative, potentially chaotic")
        
        try:
            temp = float(input("Enter new temperature (0.0-2.0): "))
            if 0.0 <= temp <= 2.0:
                app.temperature = temp
                if temp == 0.8:
                    print(f"✓ Temperature set to {temp} (Ollama default)")
                else:
                    print(f"✓ Temperature set to {temp}")
            else:
                print("❌ Temperature must be between 0.0 and 2.0")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _set_top_p(self, app):
        """Set top_p parameter with detailed explanation"""
        print(f"\n🎯 TOP-P (NUCLEUS SAMPLING) SETTING")
        print(f"Current: {app.top_p} (Ollama default: 0.9)")  # Corrected
        print(f"\nTop-p controls vocabulary diversity by using only the top X% of probable words:")
        print(f"• 0.1-0.3: Very focused vocabulary (repetitive but coherent)")
        print(f"• 0.4-0.7: Balanced vocabulary selection")
        print(f"• 0.8-0.95: Diverse vocabulary (Ollama default range)")
        print(f"• 0.96-1.0: All vocabulary available (can be chaotic)")
        
        try:
            top_p = float(input("Enter new top-p (0.0-1.0): "))
            if 0.0 <= top_p <= 1.0:
                app.top_p = top_p
                if top_p == 0.9:  # Corrected to actual default
                    print(f"✓ Top-p set to {top_p} (Ollama default)")
                else:
                    print(f"✓ Top-p set to {top_p}")
            else:
                print("❌ Top-p must be between 0.0 and 1.0")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _set_top_k(self, app):
        """Set top_k parameter with detailed explanation"""
        print(f"\n🔢 TOP-K (TOKEN FILTERING) SETTING")
        print(f"Current: {app.top_k} (Ollama default: 40, range: 1-100)")
        print(f"\nTop-k limits the model to choosing from only the K most likely next words:")
        print(f"• 1-10: Very restrictive (coherent but repetitive)")
        print(f"• 20-40: Balanced selection (Ollama default range)")
        print(f"• 50-80: More variety in word choice")
        print(f"• 90-100: Maximum vocabulary variety")
        
        try:
            top_k = int(input("Enter new top-k (1-100): "))
            if 1 <= top_k <= 100:
                app.top_k = top_k
                if top_k == 40:
                    print(f"✓ Top-k set to {top_k} (Ollama default)")
                else:
                    print(f"✓ Top-k set to {top_k}")
            else:
                print("❌ Top-k must be between 1 and 100")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _set_repeat_penalty(self, app):
        """Set repeat penalty parameter with detailed explanation"""
        print(f"\n🔄 REPEAT PENALTY SETTING")
        print(f"Current: {app.repeat_penalty} (Ollama default: 1.1, range: 1.0-2.0)")
        print(f"\nRepeat penalty reduces the likelihood of repeating the same words/phrases:")
        print(f"• 1.0: No penalty (may be repetitive)")
        print(f"• 1.05-1.15: Light penalty (Ollama default range, natural flow)")
        print(f"• 1.2-1.4: Moderate penalty (less repetitive)")
        print(f"• 1.5-2.0: Strong penalty (very diverse but may seem unnatural)")
        
        try:
            penalty = float(input("Enter new repeat penalty (1.0-2.0): "))
            if 1.0 <= penalty <= 2.0:
                app.repeat_penalty = penalty
                if penalty == 1.1:
                    print(f"✓ Repeat penalty set to {penalty} (Ollama default)")
                else:
                    print(f"✓ Repeat penalty set to {penalty}")
            else:
                print("❌ Repeat penalty must be between 1.0 and 2.0")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _set_seed(self, app):
        """Set seed parameter with detailed explanation"""
        print(f"\n🎲 SEED (REPRODUCIBILITY) SETTING")
        print(f"Current: {app.seed or 'Random'} (Ollama default: Random)")
        print(f"\nSeed controls randomness and reproducibility:")
        print(f"• Random: Different results each time (recommended for variety)")
        print(f"• Fixed number: Same results with identical settings (good for testing)")
        print(f"• Use same seed to reproduce exact same story multiple times")
        
        seed_input = input("Enter new seed (number or 'random'): ").strip()
        if seed_input.lower() in ['random', 'r', '']:
            app.seed = None
            print("✓ Seed set to random (Ollama default)")
        else:
            try:
                seed = int(seed_input)
                app.seed = seed
                print(f"✓ Seed set to {seed} (stories will be reproducible)")
            except ValueError:
                print("❌ Please enter a valid number or 'random'")
    
    def _toggle_f5_tts_audio(self, app):
        """Toggle F5-TTS audio generation with detailed info"""
        print(f"\n🎵 F5-TTS AUDIO GENERATION")
        print(f"Current status: {'Enabled' if app.auto_generate_audio else 'Disabled'}")
        print(f"\nF5-TTS (Fast, Fine-grained, and Flexible Text-to-Speech):")
        print(f"• Automatically converts generated stories to high-quality speech")
        print(f"• Uses advanced neural text-to-speech technology")
        print(f"• Creates audio files alongside your text stories")
        print(f"• Audio files are saved in the 'audio_stories/' folder")
    
        if hasattr(app, 'reference_audio_file') and app.reference_audio_file:
            print(f"• Reference voice: {app.reference_audio_file}")
    
        current_status = "enabled" if app.auto_generate_audio else "disabled"
        new_status = "disable" if app.auto_generate_audio else "enable"
    
        confirm = input(f"\n{new_status.title()} F5-TTS audio generation? (y/n): ").strip().lower()
        if confirm == 'y':
            app.auto_generate_audio = not app.auto_generate_audio
            new_status_display = "enabled" if app.auto_generate_audio else "disabled"
            print(f"✓ F5-TTS audio generation {new_status_display}")
    
            if app.auto_generate_audio:
                print("  📁 Audio files will be saved to 'audio_stories/' folder")
                print("  🎙️ F5-TTS will use your configured reference voice")
            else:
                print("  📝 Stories will be text-only")
        else:
            print(f"✓ F5-TTS audio generation remains {current_status}")
