import os
import yaml
from typing import Dict, List
from .model_tester import ModelTester

class TemplateManager:
    def __init__(self, model_tester: ModelTester):
        self.model_tester = model_tester
    
    def run_template_menu(self):
        """Run template management menu"""
        while True:
            print("\n" + "="*60)
            print("📁 TEMPLATE MANAGER")
            print("="*60)
            
            templates = self.model_tester.get_templates()
            total_templates = sum(len(category) for category in templates.values())
            print(f"Total templates: {total_templates}")
            
            print("\n1. View all templates")
            print("2. Create new template")
            print("3. Edit template")
            print("4. Delete template")
            print("5. Export templates")
            print("6. Import templates")
            print("7. Reset to defaults")
            print("8. Back to testing menu")
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == "1":
                self.view_templates()
            elif choice == "2":
                self.create_template()
            elif choice == "3":
                self.edit_template()
            elif choice == "4":
                self.delete_template()
            elif choice == "5":
                self.export_templates()
            elif choice == "6":
                self.import_templates()
            elif choice == "7":
                self.reset_templates()
            elif choice == "8":
                break
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def view_templates(self):
        """View all templates organized by category"""
        templates = self.model_tester.get_templates()
        
        if not templates:
            print("\n❌ No templates found")
            input("Press Enter to continue...")
            return
        
        print("\n📋 ALL TEMPLATES")
        print("="*70)
        
        for category, category_templates in templates.items():
            print(f"\n📁 {category.upper().replace('_', ' ')} ({len(category_templates)} templates):")
            print("-" * 50)
            
            for template in category_templates:
                print(f"  📄 {template['name']}")
                if 'description' in template:
                    print(f"      {template.get('description', 'No description')}")
                
                # Show length info if available
                expected_length = template.get('expected_length', 0)
                if expected_length > 0:
                    print(f"      Target: {expected_length} words")
                
                # Show file info
                filename = os.path.basename(template.get('file', ''))
                print(f"      File: {filename}")
                print()
        
        input("Press Enter to continue...")
    
    def create_template(self):
        """Create a new template"""
        print("\n✨ CREATE NEW TEMPLATE")
        print("="*40)
        
        name = input("Template name: ").strip()
        if not name:
            print("❌ Name is required")
            input("Press Enter to continue...")
            return
        
        # Show existing categories
        templates = self.model_tester.get_templates()
        if templates:
            print("\nExisting categories:")
            for category in templates.keys():
                print(f"  • {category}")
        
        category = input("Category (or create new): ").strip() or 'custom'
        
        print(f"\nCreating template '{name}' in category '{category}'")
        print("-" * 40)
        
        system_prompt = input("System prompt: ").strip()
        user_prompt = input("User prompt: ").strip()
        
        if not user_prompt:
            print("❌ User prompt is required")
            input("Press Enter to continue...")
            return
        
        # Optional fields
        description = input("Description (optional): ").strip()
        
        try:
            expected_length = input("Expected word count (0 for any): ").strip()
            expected_length = int(expected_length) if expected_length else 0
        except ValueError:
            expected_length = 0
        
        tags_input = input("Tags (comma-separated, optional): ").strip()
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        # Create template data
        template_data = {
            'name': name,
            'category': category,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt,
            'expected_length': expected_length
        }
        
        if description:
            template_data['description'] = description
        if tags:
            template_data['tags'] = tags
        
        # Save template
        if self._save_template(template_data, category):
            print(f"✅ Template '{name}' created successfully")
        else:
            print(f"❌ Failed to create template")
        
        input("Press Enter to continue...")
    
    def edit_template(self):
        """Edit an existing template"""
        templates = self.model_tester.get_templates()
        
        if not templates:
            print("❌ No templates to edit")
            input("Press Enter to continue...")
            return
        
        # List all templates with numbers
        all_templates = []
        print("\n📝 SELECT TEMPLATE TO EDIT:")
        print("="*50)
        
        template_num = 1
        for category, category_templates in templates.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for template in category_templates:
                print(f"{template_num:2d}. {template['name']}")
                all_templates.append(template)
                template_num += 1
        
        try:
            choice = int(input(f"\nSelect template (1-{len(all_templates)}): "))
            if 1 <= choice <= len(all_templates):
                template = all_templates[choice - 1]
                self._edit_template_interactive(template)
            else:
                print("❌ Invalid choice")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Invalid input")
            input("Press Enter to continue...")
    
    def _edit_template_interactive(self, template: Dict):
        """Interactive template editing"""
        print(f"\n✏️  EDITING: {template['name']}")
        print("="*50)
        print("(Press Enter to keep current value)\n")
        
        # Edit fields
        new_name = input(f"Name [{template['name']}]: ").strip()
        if new_name:
            template['name'] = new_name
        
        new_description = input(f"Description [{template.get('description', 'None')}]: ").strip()
        if new_description:
            template['description'] = new_description
        
        print(f"\nCurrent system prompt ({len(template['system_prompt'])} chars):")
        print(template['system_prompt'][:100] + ("..." if len(template['system_prompt']) > 100 else ""))
        new_system = input("New system prompt (or Enter to keep): ").strip()
        if new_system:
            template['system_prompt'] = new_system
        
        print(f"\nCurrent user prompt ({len(template['user_prompt'])} chars):")
        print(template['user_prompt'][:100] + ("..." if len(template['user_prompt']) > 100 else ""))
        new_user = input("New user prompt (or Enter to keep): ").strip()
        if new_user:
            template['user_prompt'] = new_user
        
        try:
            current_length = template.get('expected_length', 0)
            new_length = input(f"Expected length [{current_length}]: ").strip()
            if new_length:
                template['expected_length'] = int(new_length)
        except ValueError:
            print("❌ Invalid length, keeping current value")
        
        # Save changes
        try:
            with open(template['file'], 'w', encoding='utf-8') as f:
                # Remove file path before saving
                save_data = {k: v for k, v in template.items() if k not in ['file', 'id']}
                yaml.dump(save_data, f, default_flow_style=False, allow_unicode=True)
            print("✅ Template updated successfully")
        except Exception as e:
            print(f"❌ Error saving template: {e}")
        
        input("Press Enter to continue...")


    def delete_template(self):
        """Delete a template"""
        templates = self.model_tester.get_templates()
        
        if not templates:
            print("❌ No templates to delete")
            input("Press Enter to continue...")
            return
        
        # List templates for deletion
        all_templates = []
        print("\n🗑️  SELECT TEMPLATE TO DELETE:")
        print("="*50)
        
        template_num = 1
        for category, category_templates in templates.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for template in category_templates:
                print(f"{template_num:2d}. {template['name']}")
                all_templates.append(template)
                template_num += 1
        
        try:
            choice = int(input(f"\nSelect template (1-{len(all_templates)}): "))
            if 1 <= choice <= len(all_templates):
                template = all_templates[choice - 1]
                
                print(f"\n⚠️  DELETE: {template['name']}")
                print(f"File: {template['file']}")
                confirm = input("This cannot be undone. Continue? (type 'DELETE'): ").strip()
                
                if confirm == 'DELETE':
                    try:
                        os.remove(template['file'])
                        print("✅ Template deleted successfully")
                    except Exception as e:
                        print(f"❌ Error deleting template: {e}")
                else:
                    print("❌ Deletion cancelled")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
        
        input("Press Enter to continue...")
    
    def export_templates(self):
        """Export templates to a single file"""
        templates = self.model_tester.get_templates()
        
        if not templates:
            print("❌ No templates to export")
            input("Press Enter to continue...")
            return
        
        filename = input("Export filename (default: templates_export.yaml): ").strip()
        if not filename:
            filename = "templates_export.yaml"
        
        try:
            # Prepare export data
            export_data = {}
            for category, category_templates in templates.items():
                export_data[category] = []
                for template in category_templates:
                    # Remove file-specific fields
                    clean_template = {k: v for k, v in template.items() 
                                    if k not in ['file', 'id']}
                    export_data[category].append(clean_template)
            
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)
            
            print(f"✅ Templates exported to: {filename}")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
        
        input("Press Enter to continue...")
    
    def import_templates(self):
        """Import templates from file"""
        filename = input("Import filename: ").strip()
        
        if not os.path.exists(filename):
            print("❌ File not found")
            input("Press Enter to continue...")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = yaml.safe_load(f)
            
            if not isinstance(import_data, dict):
                print("❌ Invalid template file format")
                input("Press Enter to continue...")
                return
            
            imported_count = 0
            for category, category_templates in import_data.items():
                if isinstance(category_templates, list):
                    for template in category_templates:
                        if self._save_template(template, category):
                            imported_count += 1
            
            print(f"✅ Imported {imported_count} templates")
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
        
        input("Press Enter to continue...")
    
    def reset_templates(self):
        """Reset to default templates"""
        print("\n⚠️  RESET TO DEFAULT TEMPLATES")
        print("This will restore built-in templates (won't delete custom ones)")
        
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm == 'y':
            self.model_tester._initialize_builtin_templates()
            print("✅ Default templates restored")
        else:
            print("❌ Reset cancelled")
        
        input("Press Enter to continue...")
    
    def _save_template(self, template_data: Dict, category: str) -> bool:
        """Save template to file"""
        try:
            # Create category folder
            category_folder = os.path.join(self.model_tester.templates_folder, category)
            os.makedirs(category_folder, exist_ok=True)
            
            # Create safe filename
            name = template_data.get('name', 'unnamed')
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_').lower()
            
            template_file = os.path.join(category_folder, f"{safe_name}.yaml")
            
            with open(template_file, 'w', encoding='utf-8') as f:
                yaml.dump(template_data, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"❌ Error saving template: {e}")
            return False
