import glob
import os

class BlueprintSelector:
    def __init__(self, app_instance):
        self.app = app_instance
    
    def get_available_blueprints(self):
        """Get list of available story blueprints"""
        story_files = glob.glob(os.path.join(self.app.blueprint_folder, "*.story.txt"))
        return [os.path.basename(f) for f in story_files]
    
    def select_blueprint_for_generation(self, current_blueprint):
        """Select blueprint and save it to settings"""
        blueprints = self.get_available_blueprints()
        
        if not blueprints:
            print(f"\n❌ No story blueprints found in {self.app.blueprint_folder}/ folder.")
            print("Please create .story.txt files in the blueprints/ folder or use option 4 to create one.")
            input("Press Enter to continue...")
            return current_blueprint
        
        print("\n" + "="*60)
        print("SELECT BLUEPRINT FOR STORY GENERATION")
        print("="*60)
        
        for i, blueprint in enumerate(blueprints, 1):
            # Show which one is currently selected
            marker = " ✓" if blueprint == (current_blueprint or self.app.selected_blueprint) else ""
            print(f"{i:2d}. {blueprint}{marker}")
        
        print("\nOptions:")
        print(f"{len(blueprints) + 1}. Keep current selection")
        
        try:
            choice = int(input(f"\nSelect blueprint (1-{len(blueprints) + 1}): "))
            if 1 <= choice <= len(blueprints):
                selected = blueprints[choice - 1]
                print(f"✓ Selected blueprint: {selected}")
                result = selected
            elif choice == len(blueprints) + 1:
                print("✓ Keeping current selection")
                result = current_blueprint
            else:
                print("❌ Invalid choice.")
                result = current_blueprint
        except ValueError:
            print("❌ Invalid input.")
            result = current_blueprint
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_blueprint
        
        # FIXED: Use the correct settings manager attribute
        if result:
            # Update the app's current blueprint
            self.app.selected_blueprint = result
            
            # Save to settings using the correct attribute name
            if hasattr(self.app, 'settings') and hasattr(self.app.settings, 'set'):
                try:
                    self.app.settings.set('selected_blueprint', result)
                    print(f"💾 Blueprint saved to settings: {result}")
                except Exception as e:
                    print(f"❌ Error saving to settings: {e}")
            else:
                print("⚠️ Could not save blueprint - settings manager not accessible")
        
        input("Press Enter to continue...")
        return result
