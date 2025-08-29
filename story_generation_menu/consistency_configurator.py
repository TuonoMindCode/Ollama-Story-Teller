class ConsistencyConfigurator:
    def configure_narrative_consistency(self, current_consistency):
        """Configure narrative consistency method"""
        print("\n" + "="*60)
        print("NARRATIVE CONSISTENCY CONFIGURATION")
        print("="*60)
        print("Control how well your story maintains consistency across scenes:\n")
        
        print("CONSISTENCY METHODS:")
        print("┌─────────────────┬──────────────────────────────────────────────┐")
        print("│ Method          │ Description                                  │")
        print("├─────────────────┼──────────────────────────────────────────────┤")
        print("│ Auto Tracking   │ Automatically detects famous locations      │")
        print("│                 │ and maintains consistent descriptions       │")
        print("├─────────────────┼──────────────────────────────────────────────┤")
        print("│ Basic           │ Standard: Uses story bible for consistency  │")
        print("├─────────────────┼──────────────────────────────────────────────┤")
        print("│ None            │ Minimal: Each scene independent             │")
        print("└─────────────────┴──────────────────────────────────────────────┘")
        
        current_display = current_consistency.replace('_', ' ').title()
        print(f"\nCurrent: {current_display}")
        
        print("\nAUTO TRACKING EXAMPLES:")
        print("• Locations: 'White House', 'Eiffel Tower', 'Central Park'")
        print("• Cities: 'Paris', 'London', 'Tokyo', 'New York'")
        print("• Landmarks: 'Golden Gate Bridge', 'Statue of Liberty'")
        print("• Natural places: 'Grand Canyon', 'Mount Everest'")
        print("• ALL maintain consistent descriptions and atmosphere!")
        
        print("\nOptions:")
        print("1. Auto Tracking - Famous locations get consistent descriptions")
        print("2. Basic Consistency (Current System)")
        print("3. No Consistency Tracking")
        print("4. Keep current setting")
        
        try:
            choice = input("Select (1-4): ").strip()
            
            if choice == "1":
                result = "auto_tracking"
                print("✓ Set to Auto Tracking")
                print("  📍 LOCATIONS: Famous places will be consistently described")
                print("  🏛️ Landmarks: White House, Eiffel Tower, etc.")
                print("  🌍 Cities: Paris, Tokyo, New York, etc.")
                print("  🏞️ Natural places: Grand Canyon, Mount Everest, etc.")
                print("  ✨ Automatic consistency across all scenes!")
            elif choice == "2":
                result = "basic"
                print("✓ Set to Basic Consistency")
            elif choice == "3":
                result = "none"
                print("✓ Set to No Consistency Tracking")
            elif choice == "4":
                result = current_consistency
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
                result = current_consistency
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_consistency
        
        input("\nPress Enter to continue...")
        return result
