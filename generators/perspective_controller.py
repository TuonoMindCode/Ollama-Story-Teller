class PerspectiveController:
    def __init__(self):
        self.perspective_options = {
            'default': 'Original blueprint perspective',
            'love_interest': 'Tell from love interest POV',  # NEW OPTION
            'role_reversal': 'Tell from antagonist/opposite POV',
            'alternating': 'Alternate between protagonist and antagonist',
            'secondary_character': 'Tell from witness/sidekick POV'
            # REMOVED: 'gender_swap' since we handle that separately now
        }
        
        self.selected_perspective = 'default'
        self.character_mapping = {}
        self.pov_schedule = []  # For alternating perspectives
    
    def configure_perspective(self, blueprint_content):
        """Interactive configuration of perspective options"""
        print("\n🎭 PERSPECTIVE CONTROL")
        print("="*40)
        print("How would you like to tell this story?")
        print()
        
        for key, description in self.perspective_options.items():
            print(f"{key}: {description}")
        
        choice = input("\nSelect perspective mode (default): ").strip().lower()
        
        if choice in self.perspective_options:
            self.selected_perspective = choice
            
            # Configure specific options based on choice
            if choice == 'love_interest':  # NEW
                self._configure_love_interest(blueprint_content)
            elif choice == 'role_reversal':
                self._configure_role_reversal(blueprint_content)
            elif choice == 'alternating':
                self._configure_alternating_pov(blueprint_content)
            elif choice == 'secondary_character':
                self._configure_secondary_character(blueprint_content)
        
        return self.selected_perspective
    
    def _configure_love_interest(self, blueprint_content):  # NEW METHOD
        """Configure love interest perspective"""
        print("\n� LOVE INTEREST POV CONFIGURATION")
        print("This will tell the story from the romantic interest's perspective.")
        
        # Detect if it's a romance story
        genre = self._detect_genre(blueprint_content)
        print(f"Detected genre: {genre}")
        
        if 'romance' in genre:
            print("✓ Will tell story from the love interest's POV")
            print("   Example: Instead of following the pursuer, follow the person being pursued")
            self.character_mapping['love_interest'] = 'romantic_interest_pov'
        else:
            print("⚠️  This doesn't appear to be a romance story, but will attempt to find the secondary main character")
            self.character_mapping['love_interest'] = 'secondary_main_character_pov'

    def _configure_role_reversal(self, blueprint_content):
        """Configure role reversal (protagonist ↔ antagonist)"""
        print("\n🔄 ROLE REVERSAL CONFIGURATION")
        print("This will tell the story from the antagonist's perspective.")
        
        # Detect story type to identify "opposite"
        genre = self._detect_genre(blueprint_content)
        print(f"Detected genre: {genre}")
        
        if 'detective' in genre or 'crime' in genre:
            print("✓ Will tell story from killer/criminal's POV")
            self.character_mapping['role_reversal'] = 'criminal_pov'
        elif 'romance' in genre:
            print("✓ Will tell story from the rival/obstacle's POV")
            self.character_mapping['role_reversal'] = 'romantic_rival'
        else:
            print("✓ Will tell story from antagonist's POV")
            self.character_mapping['role_reversal'] = 'generic_antagonist'
    
    def _configure_alternating_pov(self, blueprint_content):
        """Configure alternating perspectives"""
        print("\n🔀 ALTERNATING POV CONFIGURATION")
        print("Story will alternate between different characters each scene.")
        
        pattern = input("Pattern (1=protag, 2=antag): 1,2,1,2 or 1,1,2,1,2,2: ")
        
        if pattern.strip():
            self.pov_schedule = [int(x.strip()) for x in pattern.split(',') if x.strip().isdigit()]
        else:
            self.pov_schedule = [1, 2, 1, 2]  # Default alternating
        
        print(f"✓ POV schedule: {self.pov_schedule}")
    
    def _detect_genre(self, blueprint_content):
        """Simple genre detection"""
        content_lower = blueprint_content.lower()
        
        if any(word in content_lower for word in ['detective', 'murder', 'crime', 'killer', 'investigation']):
            return 'detective/crime'
        elif any(word in content_lower for word in ['romance', 'love', 'relationship', 'dating']):
            return 'romance'
        elif any(word in content_lower for word in ['thriller', 'suspense', 'chase']):
            return 'thriller'
        else:
            return 'general'
    
    def apply_perspective_to_scene_plan(self, scene_plan, scene_number):
        """Modify scene plan based on selected perspective"""
        if self.selected_perspective == 'default':
            return scene_plan
        
        # This is where the magic happens - transform the scene plan
        if self.selected_perspective == 'alternating':
            return self._apply_alternating_pov(scene_plan, scene_number)
        elif self.selected_perspective == 'role_reversal':
            return self._apply_role_reversal(scene_plan)
        elif self.selected_perspective == 'love_interest':  # NEW
            return self._apply_love_interest_pov(scene_plan)
        elif self.selected_perspective == 'secondary_character':
            return self._apply_secondary_character_pov(scene_plan)
        
        return scene_plan
    
    def _apply_alternating_pov(self, scene_plan, scene_number):
        """Apply alternating POV to scene"""
        if not self.pov_schedule:
            return scene_plan
        
        # Determine whose POV this scene should be
        pov_index = (scene_number - 1) % len(self.pov_schedule)
        pov_character = self.pov_schedule[pov_index]
        
        if pov_character == 1:
            # Protagonist POV
            modifier = "\n\nPERSPECTIVE INSTRUCTION: Tell this scene from the PROTAGONIST's point of view."
        else:
            # Antagonist POV  
            modifier = "\n\nPERSPECTIVE INSTRUCTION: Tell this scene from the ANTAGONIST's point of view. Show their motivations, thoughts, and actions. They should be actively involved or observing the events."
        
        return scene_plan + modifier
    
    def _apply_role_reversal(self, scene_plan):
        """Apply complete role reversal"""
        modifier = "\n\nPERSPECTIVE INSTRUCTION: Tell this story from the ANTAGONIST's perspective. The original protagonist becomes a character they interact with, observe, or oppose."
        return scene_plan + modifier
    
    def _apply_love_interest_pov(self, scene_plan):  # NEW METHOD
        """Apply love interest POV to scene"""
        if 'love_interest' not in self.character_mapping:
            return scene_plan
        
        modifier = "\n\nPERSPECTIVE INSTRUCTION: Tell this scene from the LOVE INTEREST's point of view. Instead of following the main protagonist, follow their romantic interest. Show their thoughts, feelings, and reactions to the protagonist's actions."
        
        return scene_plan + modifier

    def _apply_secondary_character_pov(self, scene_plan):  # ADD THIS METHOD if missing
        """Apply secondary character POV"""
        modifier = "\n\nPERSPECTIVE INSTRUCTION: Tell this scene from a SECONDARY CHARACTER's perspective (witness, sidekick, friend, etc.). This character observes or participates in the events but is not the main protagonist."
        
        return scene_plan + modifier
