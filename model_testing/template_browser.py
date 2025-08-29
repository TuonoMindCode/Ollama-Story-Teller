import os

class TemplateBrowser:
    def __init__(self, template_manager):
        self.template_manager = template_manager

    def browse_system_prompts(self):
        """Browse and view system prompt templates"""
        print(f"Browse {self.template_manager.content_type} system prompts")
        
        system_prompts = self.template_manager.list_system_prompts()
        
        if not system_prompts:
            print("No system prompt templates found.")
            input("Press Enter to continue...")
            return
        
        print(f"\n📋 SYSTEM PROMPT TEMPLATES:")
        print("-" * 60)
        for i, filename in enumerate(system_prompts, 1):
            filepath = os.path.join(self.template_manager.system_prompts_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    word_count = len(content.split())
                    preview = content[:80] + "..." if len(content) > 80 else content
                print(f"{i:2d}. {filename}")
                print(f"    Words: {word_count} | Preview: {preview}")
                print()
            except:
                print(f"{i:2d}. {filename} (Error reading file)")
                print()
        
        input("Press Enter to continue...")

    def browse_user_prompts(self):
        """Browse and view user prompt templates"""
        print(f"Browse {self.template_manager.content_type} user prompts")
        
        user_prompts = self.template_manager.list_user_prompts()
        
        if not user_prompts:
            print("No user prompt templates found.")
            input("Press Enter to continue...")
            return
        
        print(f"\n📋 USER PROMPT TEMPLATES:")
        print("-" * 60)
        for i, filename in enumerate(user_prompts, 1):
            filepath = os.path.join(self.template_manager.user_prompts_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    word_count = len(content.split())
                    preview = content[:80] + "..." if len(content) > 80 else content
                print(f"{i:2d}. {filename}")
                print(f"    Words: {word_count} | Preview: {preview}")
                print()
            except:
                print(f"{i:2d}. {filename} (Error reading file)")
                print()
        
        input("Press Enter to continue...")

    def delete_templates(self):
        """Delete templates with type awareness"""
        print(f"\n{'='*60}")
        print("DELETE TEMPLATES")
        print(f"{'='*60}")
        print("Choose template type to delete from:")
        print()
        print("1. System Prompts")
        print("2. User Prompts")
        print("3. Back to Template Manager")
        
        try:
            choice = int(input("Select option (1-3): "))
            
            if choice == 1:
                self._delete_system_templates()
            elif choice == 2:
                self._delete_user_templates()
            elif choice == 3:
                return
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")
        
        input("Press Enter to continue...")
    
    def _delete_system_templates(self):
        """Delete system prompt templates"""
        system_prompts = self.template_manager.list_system_prompts()
        
        if not system_prompts:
            print("No system prompt templates to delete.")
            return
        
        print(f"\n🗑️  SYSTEM PROMPT TEMPLATES:")
        print("-" * 50)
        for i, filename in enumerate(system_prompts, 1):
            print(f"{i:2d}. {filename}")
        
        try:
            choice = int(input(f"\nSelect template to delete (1-{len(system_prompts)}): "))
            if 1 <= choice <= len(system_prompts):
                filename = system_prompts[choice - 1]
                filepath = os.path.join(self.template_manager.system_prompts_dir, filename)
                
                print(f"\n⚠️  DELETE: {filename}")
                confirm = input("This cannot be undone. Type 'DELETE' to confirm: ").strip()
                
                if confirm == 'DELETE':
                    try:
                        os.remove(filepath)
                        print(f"✅ Template '{filename}' deleted successfully.")
                    except Exception as e:
                        print(f"❌ Error deleting template: {e}")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")
    
    def _delete_user_templates(self):
        """Delete user prompt templates"""
        user_prompts = self.template_manager.list_user_prompts()
        
        if not user_prompts:
            print("No user prompt templates to delete.")
            return
        
        print(f"\n🗑️  USER PROMPT TEMPLATES:")
        print("-" * 50)
        for i, filename in enumerate(user_prompts, 1):
            print(f"{i:2d}. {filename}")
        
        try:
            choice = int(input(f"\nSelect template to delete (1-{len(user_prompts)}): "))
            if 1 <= choice <= len(user_prompts):
                filename = user_prompts[choice - 1]
                filepath = os.path.join(self.template_manager.user_prompts_dir, filename)
                
                print(f"\n⚠️  DELETE: {filename}")
                confirm = input("This cannot be undone. Type 'DELETE' to confirm: ").strip()
                
                if confirm == 'DELETE':
                    try:
                        os.remove(filepath)
                        print(f"✅ Template '{filename}' deleted successfully.")
                    except Exception as e:
                        print(f"❌ Error deleting template: {e}")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")

    def view_saved_templates(self):
        """View all saved templates organized by type"""
        print(f"\n{'='*60}")
        print("SAVED TEMPLATES OVERVIEW")
        print(f"{'='*60}")

        # Show system prompts
        system_prompts = self.template_manager.list_system_prompts()
        print("SYSTEM PROMPTS:")
        if system_prompts:
            for filename in system_prompts:
                filepath = os.path.join(self.template_manager.system_prompts_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        word_count = len(content.split())
                        preview = content[:60] + "..." if len(content) > 60 else content
                    print(f"  • {filename:<30} ({word_count:3d} words) - {preview}")
                except:
                    print(f"  • {filename:<30} (Error reading)")
        else:
            print("  No system prompts found")

        print()

        # Show user prompts
        user_prompts = self.template_manager.list_user_prompts()
        print("USER PROMPTS:")
        if user_prompts:
            for filename in user_prompts:
                filepath = os.path.join(self.template_manager.user_prompts_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        word_count = len(content.split())
                        preview = content[:60] + "..." if len(content) > 60 else content
                    print(f"  • {filename:<30} ({word_count:3d} words) - {preview}")
                except:
                    print(f"  • {filename:<30} (Error reading)")
        else:
            print("  No user prompts found")

        print(f"\nTemplates location: {self.template_manager.template_base_dir}")
        print("These templates can be used in Scene Workshop.")
        input("Press Enter to continue...")