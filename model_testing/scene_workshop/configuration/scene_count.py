class SceneCountConfigurator:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def configure_scene_count(self):
        """Configure scene count for batch generation"""
        print("\nSCENE COUNT CONFIGURATION")
        print("="*40)
        
        current_count = self.workshop.settings.get('scene_count', 1) if self.workshop.settings else 1
        print(f"Current count: {current_count}")
        print("Set how many scenes to generate in batch mode.")
        print("Each scene uses the same prompts but different parameters.")
        
        try:
            count = int(input("Enter scene count (1-50): "))
            if 1 <= count <= 50:
                if self.workshop.settings:
                    self.workshop.settings.set('scene_count', count)
                print(f"✅ Scene count set to {count}")
            else:
                print("Count must be between 1 and 50.")
        except ValueError:
            print("Invalid number.")
        
        input("Press Enter to continue...")
