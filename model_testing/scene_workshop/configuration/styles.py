class StylesConfigurator:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def configure_narrative_style(self):
        """Configure narrative style enhancement"""
        print("\nNARRATIVE STYLE CONFIGURATION")
        print("="*50)
        print("Narrative styles add perspective guidance to your user prompt.")
        print("This helps ensure consistent point-of-view throughout the scene.")
        print("\nAvailable styles:")
        print("1. First Person Inner Focus - Uses 'I' with emphasis on internal thoughts")
        print("2. Second Person Romance - Uses 'I' for protagonist, 'you' for other person")  
        print("3. Third Person Limited - Stays with one character's perspective")
        print("4. Stream of Consciousness - Flowing, connected thoughts")
        print("5. Clear current selection")
        print("0. Back to main menu")
        
        choice = input("\nSelect narrative style (0-5): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            self._set_narrative_style('first_inner', 'First Person Inner Focus')
        elif choice == '2':
            self._set_narrative_style('second_romance', 'Second Person Romance')
        elif choice == '3':
            self._set_narrative_style('third_limited', 'Third Person Limited')
        elif choice == '4':
            self._set_narrative_style('stream', 'Stream of Consciousness')
        elif choice == '5':
            self._clear_narrative_style()
        else:
            print("Invalid option.")
        
        input("Press Enter to continue...")

    def configure_writing_style(self):
        """Configure writing style enhancement"""
        print("\nWRITING STYLE CONFIGURATION")
        print("="*50)
        print("Writing styles add tone and technique guidance to your user prompt.")
        print("This influences the AI's prose style and approach.")
        print("\nAvailable styles:")
        print("1. Literary - Rich prose with metaphors and deeper meaning")
        print("2. Minimalist - Simple, direct language that's concise")
        print("3. Dialogue Heavy - Focus on conversations driving the scene")
        print("4. Descriptive - Rich sensory details and atmosphere")
        print("5. Clear current selection")
        print("0. Back to main menu")
        
        choice = input("\nSelect writing style (0-5): ").strip()
        
        if choice == '0':
            return
        elif choice == '1':
            self._set_writing_style('literary', 'Literary')
        elif choice == '2':
            self._set_writing_style('minimalist', 'Minimalist')
        elif choice == '3':
            self._set_writing_style('dialogue', 'Dialogue Heavy')
        elif choice == '4':
            self._set_writing_style('descriptive', 'Descriptive')
        elif choice == '5':
            self._clear_writing_style()
        else:
            print("Invalid option.")
        
        input("Press Enter to continue...")

    def _set_narrative_style(self, style_key, style_name):
        """Set narrative style"""
        if self.workshop.settings:
            self.workshop.settings.set('narrative_style', style_key)
            self.workshop.settings.set('narrative_style_name', style_name)
        print(f"✅ {style_name} selected")

    def _clear_narrative_style(self):
        """Clear narrative style"""
        if self.workshop.settings:
            self.workshop.settings.set('narrative_style', None)
            self.workshop.settings.set('narrative_style_name', 'Not selected')
        print("✅ Narrative style cleared")

    def _set_writing_style(self, style_key, style_name):
        """Set writing style"""
        if self.workshop.settings:
            self.workshop.settings.set('writing_style', style_key)
            self.workshop.settings.set('writing_style_name', style_name)
        print(f"✅ {style_name} style selected")

    def _clear_writing_style(self):
        """Clear writing style"""
        if self.workshop.settings:
            self.workshop.settings.set('writing_style', None)
            self.workshop.settings.set('writing_style_name', 'Not selected')
        print("✅ Writing style cleared")
