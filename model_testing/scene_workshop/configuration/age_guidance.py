class AgeGuidanceConfigurator:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def configure_age_guidance(self):
        """Configure age guidance enhancement"""
        print("\nAGE GUIDANCE CONFIGURATION")
        print("="*50)
        print("Age guidance adds content appropriateness instructions to your user prompt.")
        print("This helps ensure the AI generates age-appropriate content.")
        print("\nAvailable age guidance options:")
        print("1. All Ages (G) - Suitable for everyone, no mature content")
        print("2. Teen+ (PG-13) - Mild themes, minimal mature content")
        print("3. Young Adult (16+) - Romance themes, mild adult situations")
        print("4. Adult (18+) - Mature themes, adult situations allowed")
        print("5. Custom Age Guidance - Write your own content guidelines")
        print("6. Clear current selection (No age guidance)")
        print("0. Back to main menu")
        
        choice = input("\nSelect age guidance (0-6): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            self._set_age_guidance('all_ages', 'All Ages (G)')
        elif choice == '2':
            self._set_age_guidance('teen', 'Teen+ (PG-13)')
        elif choice == '3':
            self._set_age_guidance('young_adult', 'Young Adult (16+)')
        elif choice == '4':
            self._set_age_guidance('adult', 'Adult (18+)')
        elif choice == '5':
            self._set_custom_age_guidance()
        elif choice == '6':
            self._clear_age_guidance()
        else:
            print("Invalid option.")
        
        input("Press Enter to continue...")

    def _set_age_guidance(self, guidance_key, guidance_name):
        """Set age guidance"""
        if self.workshop.settings:
            self.workshop.settings.set('age_guidance', guidance_key, quiet=True)
            self.workshop.settings.set('age_guidance_name', guidance_name, quiet=True)
            # Store the actual text that will be appended
            guidance_text = self._get_guidance_text(guidance_key)
            self.workshop.settings.set('age_guidance_text', guidance_text, quiet=True)
        
        print(f"✅ {guidance_name} guidance selected")
        
        # Show what this adds to prompts
        guidance_text = self._get_guidance_text(guidance_key)
        print(f"\nThis will add to your user prompt:")
        print(f'"{guidance_text}"')

    def _set_custom_age_guidance(self):
        """Set custom age guidance"""
        print("\nCUSTOM AGE GUIDANCE")
        print("-" * 30)
        print("Enter your custom age/content guidelines (press Enter on empty line to finish):")
        print("This will be added to your user prompt to guide content appropriateness.")
        print()
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        if lines:
            custom_text = '\n'.join(lines)
            
            if self.workshop.settings:
                self.workshop.settings.set('age_guidance', 'custom', quiet=True)
                self.workshop.settings.set('age_guidance_name', 'Custom Guidelines', quiet=True)
                self.workshop.settings.set('age_guidance_text', custom_text, quiet=True)
            
            print("✅ Custom age guidance saved")
            print(f"Preview: {custom_text[:100]}...")
        else:
            print("No content entered.")

    def _clear_age_guidance(self):
        """Clear age guidance"""
        if self.workshop.settings:
            self.workshop.settings.set('age_guidance', None, quiet=True)
            self.workshop.settings.set('age_guidance_name', 'Not selected', quiet=True)
            self.workshop.settings.set('age_guidance_text', None, quiet=True)
        print("✅ Age guidance cleared - no content guidelines will be added to user prompts")

    def _get_guidance_text(self, guidance_key):
        """Get the text that will be added to user prompts"""
        guidance_texts = {
            'all_ages': "Keep content completely family-friendly and appropriate for all ages. No mature themes, violence, or adult situations.",
            
            'teen': "Keep content appropriate for teenagers (PG-13 level). Mild themes are okay, but avoid explicit content, graphic violence, or detailed adult situations.",
            
            'young_adult': "Content should be appropriate for young adults (16+). Romance and mild adult themes are acceptable, but avoid explicit sexual content or graphic violence.",
            
            'adult': "Adult themes and situations are permitted (18+). Include mature content as appropriate for the story, but maintain literary quality."
        }
        return guidance_texts.get(guidance_key, "")

    def get_guidance_enhancement(self):
        """Get the age guidance text to add to user prompts - only if guidance is set"""
        if not self.workshop.settings:
            return ""
        
        # Only return text if age guidance is actually selected
        guidance_key = self.workshop.settings.get('age_guidance')
        if not guidance_key:
            return ""  # No guidance selected, don't add anything
        
        guidance_text = self.workshop.settings.get('age_guidance_text', "")
        if guidance_text:
            return f"\n\nContent Guidelines: {guidance_text}"
        
        return ""

    def get_display_name(self):
        """Get display name for current age guidance"""
        if not self.workshop.settings:
            return 'Not selected'
        
        return self.workshop.settings.get('age_guidance_name', 'Not selected')

    def has_age_guidance(self):
        """Check if age guidance is configured"""
        if not self.workshop.settings:
            return False
        
        guidance_key = self.workshop.settings.get('age_guidance')
        return guidance_key is not None
