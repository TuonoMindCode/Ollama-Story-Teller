class SceneConfigurator:
    def configure_scene_control(self, current_mode, current_scenes):
        """Configure scene control settings"""
        print("\n" + "="*60)
        print("SCENE CONTROL CONFIGURATION")
        print("="*60)
        print("Control how many scenes your story will have:\n")
        
        print("SCENE CONTROL MODES:")
        print("┌────────────────────────────────────────────────────────────┐")
        print("│ Mode   │ Description                                        │")
        print("├────────┼────────────────────────────────────────────────────┤")
        print("│ Auto   │ AI decides scene count based on story complexity  │")
        print("│ Manual │ You specify exact number of scenes                │")
        print("└────────┴────────────────────────────────────────────────────┘")
        
        print(f"\nCurrent: {current_mode.title()}", end="")
        if current_mode == "manual":
            print(f" ({current_scenes} scenes)")
        else:
            print()
        
        print("\nOptions:")
        print("1. Auto - Let AI decide scene count (recommended)")
        print("2. Manual - Specify exact number of scenes")
        print("3. Keep current setting")
        
        try:
            choice = input("Select (1-3): ").strip()
            
            if choice == "1":
                result_mode = "auto"
                result_scenes = "auto"
                print("✓ Set to Auto scene control")
            elif choice == "2":
                result_mode = "manual"
                try:
                    scenes = int(input("Enter number of scenes (3-20): "))
                    if 3 <= scenes <= 20:
                        result_scenes = scenes
                        print(f"✓ Set to Manual: {scenes} scenes")
                    else:
                        print("❌ Invalid number. Must be between 3-20.")
                        input("Press Enter to continue...")
                        return current_mode, current_scenes
                except ValueError:
                    print("❌ Invalid input.")
                    input("Press Enter to continue...")
                    return current_mode, current_scenes
            elif choice == "3":
                result_mode = current_mode
                result_scenes = current_scenes
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
                result_mode = current_mode
                result_scenes = current_scenes
        except Exception as e:
            print(f"❌ Error: {e}")
            result_mode = current_mode
            result_scenes = current_scenes
        
        input("\nPress Enter to continue...")
        return result_mode, result_scenes
