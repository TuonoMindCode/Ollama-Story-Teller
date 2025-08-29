"""
Language & Dialogue Style Configuration
Controls how characters speak and what language they use
"""

class LanguageConfigurator:
    """Configure language style, profanity, and dialogue characteristics"""
    
    LANGUAGE_STYLES = {
        "profanity_level": {
            "clean": "No profanity or crude language",
            "mild": "Occasional mild language (damn, hell, etc.)",
            "moderate": "Standard adult language with some profanity",
            "unrestricted": "No language limitations",
            "custom": "Define your own language guidelines"
        },
        
        "dialogue_intensity": {
            "restrained": "Polite, controlled speech even in emotional moments",
            "moderate": "Natural emotional expression with some intensity",
            "passionate": "Emotionally charged, intense dialogue",
            "raw": "Unfiltered, brutally honest communication",
            "custom": "Custom intensity level"
        },
        
        "speech_style": {
            "formal": "Proper grammar, sophisticated vocabulary",
            "casual": "Natural, everyday conversational style",
            "street": "Urban, colloquial language and slang",
            "period": "Historical or era-appropriate speech patterns",
            "professional": "Business/workplace appropriate language",
            "intimate": "Personal, tender communication style",
            "custom": "Custom speech style"
        }
    }
    
    def configure_language_style(self, current_profanity="moderate", current_intensity="moderate", current_style="casual"):
        """Configure language and dialogue style"""
        
        while True:
            print("\n🗣️ LANGUAGE & DIALOGUE STYLE")
            print("="*50)
            print("Configure how characters speak and what language they use")
            print("-"*50)
            
            # Display current settings
            profanity_desc = self.LANGUAGE_STYLES["profanity_level"].get(current_profanity, current_profanity)
            intensity_desc = self.LANGUAGE_STYLES["dialogue_intensity"].get(current_intensity, current_intensity)
            style_desc = self.LANGUAGE_STYLES["speech_style"].get(current_style, current_style)
            
            print(f"1. Profanity Level: {current_profanity.title()} - {profanity_desc}")
            print(f"2. Dialogue Intensity: {current_intensity.title()} - {intensity_desc}")
            print(f"3. Speech Style: {current_style.title()} - {style_desc}")
            print("4. View Language Examples")
            print("5. Reset to Defaults")
            print("6. Done")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                current_profanity = self._configure_profanity_level(current_profanity)
            elif choice == "2":
                current_intensity = self._configure_dialogue_intensity(current_intensity)
            elif choice == "3":
                current_style = self._configure_speech_style(current_style)
            elif choice == "4":
                self._show_language_examples()
            elif choice == "5":
                current_profanity, current_intensity, current_style = "moderate", "moderate", "casual"
                print("✅ Reset to default language settings")
            elif choice == "6":
                break
            else:
                print("❌ Invalid choice")
        
        return current_profanity, current_intensity, current_style
    
    def _configure_profanity_level(self, current):
        """Configure profanity level"""
        print("\n🗣️ LANGUAGE LEVEL")
        print("-"*30)
        
        for i, (level, desc) in enumerate(self.LANGUAGE_STYLES["profanity_level"].items(), 1):
            marker = "✓" if level == current else " "
            print(f"{i}. [{marker}] {level.title()} - {desc}")
        
        try:
            choice = int(input(f"\nSelect level (1-{len(self.LANGUAGE_STYLES['profanity_level'])}): "))
            levels = list(self.LANGUAGE_STYLES["profanity_level"].keys())
            
            if 1 <= choice <= len(levels):
                selected = levels[choice - 1]
                
                if selected == "custom":
                    custom_desc = input("Describe your custom language guidelines: ").strip()
                    if custom_desc:
                        return f"custom:{custom_desc}"
                    return current
                
                return selected
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
        
        return current
    
    def _configure_dialogue_intensity(self, current):
        """Configure dialogue intensity"""
        print("\n🔥 DIALOGUE INTENSITY")
        print("-"*30)
        
        for i, (level, desc) in enumerate(self.LANGUAGE_STYLES["dialogue_intensity"].items(), 1):
            marker = "✓" if level == current else " "
            print(f"{i}. [{marker}] {level.title()} - {desc}")
        
        try:
            choice = int(input(f"\nSelect intensity (1-{len(self.LANGUAGE_STYLES['dialogue_intensity'])}): "))
            levels = list(self.LANGUAGE_STYLES["dialogue_intensity"].keys())
            
            if 1 <= choice <= len(levels):
                selected = levels[choice - 1]
                
                if selected == "custom":
                    custom_desc = input("Describe your custom intensity level: ").strip()
                    if custom_desc:
                        return f"custom:{custom_desc}"
                    return current
                
                return selected
        except ValueError:
            print("❌ Please enter a number")
        
        return current
    
    def _configure_speech_style(self, current):
        """Configure speech style"""
        print("\n💬 SPEECH STYLE")
        print("-"*30)
        
        for i, (style, desc) in enumerate(self.LANGUAGE_STYLES["speech_style"].items(), 1):
            marker = "✓" if style == current else " "
            print(f"{i}. [{marker}] {style.title()} - {desc}")
        
        try:
            choice = int(input(f"\nSelect style (1-{len(self.LANGUAGE_STYLES['speech_style'])}): "))
            styles = list(self.LANGUAGE_STYLES["speech_style"].keys())
            
            if 1 <= choice <= len(styles):
                selected = styles[choice - 1]
                
                if selected == "custom":
                    custom_desc = input("Describe your custom speech style: ").strip()  
                    if custom_desc:
                        return f"custom:{custom_desc}"
                    return current
                
                return selected
        except ValueError:
            print("❌ Please enter a number")
        
        return current
    
    def _show_language_examples(self):
        """Show examples of different language styles"""
        print("\n📚 LANGUAGE STYLE EXAMPLES")
        print("="*50)
        
        examples = {
            "Clean + Restrained": "\"I'm quite upset about this situation. It's very frustrating.\"",
            "Mild + Moderate": "\"Damn it, this is really getting on my nerves!\"", 
            "Strong + Passionate": "\"This is fucking ridiculous! I can't take this shit anymore!\"",
            "Uncensored + Raw": "\"What the hell is wrong with you? This whole damn thing is fucked up!\"",
            "Formal + Professional": "\"I must express my profound disappointment with these circumstances.\"",
            "Street + Raw": "\"Yo, this is some bullshit, man. I ain't dealing with this crap.\"",
            "Intimate + Passionate": "\"God, I need you so much. You drive me absolutely crazy.\"",
        }
        
        for style, example in examples.items():
            print(f"\n{style}:")
            print(f"  {example}")
        
        input("\nPress Enter to continue...")
    
    def get_language_prompt_addition(self, profanity_level, dialogue_intensity, speech_style):
        """Get language style addition for AI prompts"""
        if all(setting in ["moderate", "casual"] for setting in [profanity_level, dialogue_intensity, speech_style]):
            return ""  # Default settings, no special instructions needed
        
        addition = "\n\nLANGUAGE & DIALOGUE REQUIREMENTS:\n"
        
        # Profanity guidelines - UPDATED
        if profanity_level == "clean":
            addition += "- Use NO profanity or crude language whatsoever\n"
        elif profanity_level == "mild":
            addition += "- Use only mild language (damn, hell, etc.) sparingly\n"
        elif profanity_level == "moderate":
            addition += "- Use standard adult language with some profanity when appropriate\n"
        elif profanity_level == "unrestricted":
            addition += "- No language limitations - use any language as needed for the story\n"
        elif profanity_level.startswith("custom:"):
            addition += f"- Language guidelines: {profanity_level[7:]}\n"
        
        # Intensity guidelines
        if dialogue_intensity == "restrained":
            addition += "- Keep dialogue polite and controlled even in emotional moments\n"
        elif dialogue_intensity == "passionate":
            addition += "- Use emotionally charged, intense dialogue\n"
        elif dialogue_intensity == "raw":
            addition += "- Use unfiltered, brutally honest communication\n"
        elif dialogue_intensity.startswith("custom:"):
            addition += f"- Dialogue intensity: {dialogue_intensity[7:]}\n"
        
        # Style guidelines
        if speech_style == "formal":
            addition += "- Use proper grammar and sophisticated vocabulary\n"
        elif speech_style == "street":
            addition += "- Use urban, colloquial language and appropriate slang\n"
        elif speech_style == "professional":
            addition += "- Use business/workplace appropriate language\n"
        elif speech_style == "intimate":
            addition += "- Use personal, tender communication style\n"
        elif speech_style.startswith("custom:"):
            addition += f"- Speech style: {speech_style[7:]}\n"
        
        return addition
    
    def get_language_display(self, profanity_level, dialogue_intensity, speech_style):
        """Get display text for current language settings"""
        parts = []
        if profanity_level != "moderate":
            parts.append(f"Language: {profanity_level.title()}")
        if dialogue_intensity != "moderate":
            parts.append(f"Intensity: {dialogue_intensity.title()}")
        if speech_style != "casual":
            parts.append(f"Style: {speech_style.title()}")
        
        return " | ".join(parts) if parts else "Standard Language"
    
    def check_content_conflicts(self, content_rating, profanity_level, dialogue_intensity):
        """Check for conflicts between content rating and language settings"""
        conflicts = []
        
        # Define what's allowed for each content rating - UPDATED
        allowed_profanity = {
            "family": ["clean"],
            "teen": ["clean", "mild"],
            "adult": ["clean", "mild", "moderate", "unrestricted"],
            "auto": ["clean", "mild", "moderate", "unrestricted"]  # No restrictions
        }
        
        allowed_intensity = {
            "family": ["restrained"],
            "teen": ["restrained", "moderate"], 
            "adult": ["restrained", "moderate", "passionate", "raw"],
            "auto": ["restrained", "moderate", "passionate", "raw"]  # No restrictions
        }
        
        # Extract base content rating (handle custom ratings)
        base_rating = content_rating.split(":")[0] if ":" in content_rating else content_rating
        base_profanity = profanity_level.split(":")[0] if ":" in profanity_level else profanity_level
        base_intensity = dialogue_intensity.split(":")[0] if ":" in dialogue_intensity else dialogue_intensity
        
        # Check profanity conflicts
        if base_rating in allowed_profanity:
            if base_profanity not in allowed_profanity[base_rating]:
                conflicts.append({
                    "type": "profanity",
                    "message": f"'{profanity_level}' language conflicts with '{content_rating}' content rating",
                    "suggestion": f"Use {' or '.join(allowed_profanity[base_rating])} language instead"
                })
        
        # Check intensity conflicts  
        if base_rating in allowed_intensity:
            if base_intensity not in allowed_intensity[base_rating]:
                conflicts.append({
                    "type": "intensity", 
                    "message": f"'{dialogue_intensity}' intensity conflicts with '{content_rating}' content rating",
                    "suggestion": f"Use {' or '.join(allowed_intensity[base_rating])} intensity instead"
                })
        
        return conflicts
    
    def resolve_conflicts_menu(self, content_rating, profanity_level, dialogue_intensity, speech_style):
        """Show conflict resolution menu"""
        conflicts = self.check_content_conflicts(content_rating, profanity_level, dialogue_intensity)
        
        if not conflicts:
            return profanity_level, dialogue_intensity, speech_style  # No conflicts
        
        print("\n⚠️ CONTENT CONFLICTS DETECTED")
        print("="*50)
        print(f"Content Rating: {content_rating}")
        print(f"Language Settings: {profanity_level} + {dialogue_intensity}")
        print("-"*50)
        
        for i, conflict in enumerate(conflicts, 1):
            print(f"{i}. {conflict['message']}")
            print(f"   💡 {conflict['suggestion']}")
        
        print("\nResolution Options:")
        print("1. Auto-fix language to match content rating")
        print("2. Change content rating to 'Adult' to allow current language")
        print("3. Manually adjust language settings")
        print("4. Keep conflicts (may produce inconsistent results)")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            return self._auto_fix_language(content_rating)
        elif choice == "2":
            print("✅ Content rating will be changed to 'Adult' to allow your language settings")
            return profanity_level, dialogue_intensity, speech_style, "adult"  # Return new content rating
        elif choice == "3":
            print("\nManually adjust your language settings:")
            return self.configure_language_style(profanity_level, dialogue_intensity, speech_style)
        else:
            print("⚠️ Keeping conflicting settings - results may be inconsistent")
            return profanity_level, dialogue_intensity, speech_style
    
    def _auto_fix_language(self, content_rating):
        """Auto-fix language settings to match content rating"""
        base_rating = content_rating.split(":")[0] if ":" in content_rating else content_rating
        
        if base_rating == "family":
            fixed_profanity = "clean"
            fixed_intensity = "restrained"
        elif base_rating == "teen":
            fixed_profanity = "mild"
            fixed_intensity = "moderate"
        else:  # adult or auto
            fixed_profanity = "moderate"
            fixed_intensity = "moderate"
        
        print(f"✅ Auto-fixed language settings:")
        print(f"   Profanity: {fixed_profanity}")
        print(f"   Intensity: {fixed_intensity}")
        
        return fixed_profanity, fixed_intensity, "casual"  # Reset to default style
    
    def get_safe_defaults_for_rating(self, content_rating):
        """Get safe default language settings for a content rating"""
        base_rating = content_rating.split(":")[0] if ":" in content_rating else content_rating
        
        defaults = {
            "family": ("clean", "restrained", "casual"),
            "teen": ("mild", "moderate", "casual"), 
            "adult": ("moderate", "moderate", "casual"),
            "auto": ("moderate", "moderate", "casual")
        }
        
        return defaults.get(base_rating, ("moderate", "moderate", "casual"))
