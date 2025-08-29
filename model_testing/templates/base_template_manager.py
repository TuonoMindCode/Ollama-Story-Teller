import os
import datetime
from typing import Dict

class BaseTemplateManager:
    """Base class with common template management functionality"""
    
    def __init__(self, templates_folder: str):
        self.templates_folder = templates_folder
    
    def _format_date(self, date_str: str, time_str: str) -> str:
        """Format date and time for display"""
        try:
            if len(date_str) == 8 and len(time_str) == 6:
                dt = datetime.datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                return dt.strftime("%b %d, %H:%M")
        except:
            pass
        return "Unknown"
    
    def _parse_filename(self, filename: str) -> Dict:
        """Parse metadata from filename"""
        name = filename.replace('.txt', '')
        parts = name.split('_')
        
        if len(parts) >= 5:
            return {
                'type': parts[0],
                'genre': parts[2].replace('_', ' ').title(),  # Fixed: .title() not .Title()
                'style': parts[3].replace('_', ' ').title(),  # Fixed: .title() not .Title()
                'date': parts[4],
                'time': parts[5] if len(parts) > 5 else '000000'
            }
        else:
            return {
                'type': parts[0] if parts else 'unknown',
                'genre': 'Unknown',
                'style': 'Unknown',
                'date': 'Unknown',
                'time': '000000'
            }
    
    def _sanitize_filename_part(self, text: str) -> str:
        """Sanitize text for use in filename"""
        if not text:
            return "unknown"
        
        invalid_chars = '<>:"/\\|?*'
        sanitized = text
        
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '')
        
        sanitized = sanitized.replace('"', '').replace("'", '')
        sanitized = sanitized.replace('(', '').replace(')', '')
        sanitized = sanitized.replace('[', '').replace(']', '')
        sanitized = sanitized.replace('{', '').replace('}', '')
        
        sanitized = sanitized.replace(' ', '_').replace('-', '_')
        sanitized = sanitized.replace('.', '_').replace(',', '_')
        
        while '__' in sanitized:
            sanitized = sanitized.replace('__', '_')
        
        sanitized = sanitized.strip('_')
        sanitized = sanitized[:20] if sanitized else "unknown"
        
        return sanitized.lower()
    
    def _view_prompt_content(self, filename: str, prompt_type: str):
        """View prompt content"""
        filepath = os.path.join(self.templates_folder, filename)
        
        if not os.path.exists(filepath):
            print("File not found")
            input("Press Enter to continue...")
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            content_start = 0
            metadata = {}
            
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    if 'Created:' in line:
                        metadata['created'] = line.split('Created:', 1)[1].strip()
                    elif 'Genre:' in line:
                        metadata['genre'] = line.split('Genre:', 1)[1].strip()
                    elif 'Style:' in line:
                        metadata['style'] = line.split('Style:', 1)[1].strip()
                elif line.strip() == '' and i > 0:
                    content_start = i + 1
                    break
            
            prompt_content = '\n'.join(lines[content_start:]).strip()
            
            print("\n" + "="*60)
            print(f"{prompt_type.upper()} PROMPT CONTENT")
            print("="*60)
            print(f"File: {filename}")
            if 'created' in metadata:
                print(f"Created: {metadata['created']}")
            if 'genre' in metadata and 'style' in metadata:
                print(f"Genre: {metadata['genre']} | Style: {metadata['style']}")
            print()
            print("Content:")
            print("─" * 60)
            print(prompt_content)
            print("─" * 60)
            
            print("\nUse This in Scene Workshop")
            print("Delete This Prompt")
            print("Back to Browse")
            
            action = input("\nAction (use/delete/back): ").strip().lower()
            
            if action in ['use', 'u']:
                print("Go to Scene Workshop to use this prompt!")
                input("Press Enter to continue...")
            elif action in ['delete', 'd']:
                self._delete_specific_prompt(filename, prompt_type)
            
        except Exception as e:
            print(f"Error reading file: {e}")
            input("Press Enter to continue...")
    
    def _delete_specific_prompt(self, filename: str, prompt_type: str):
        """Delete a specific prompt file"""
        filepath = os.path.join(self.templates_folder, filename)
        
        print(f"\nDELETE {prompt_type.upper()} PROMPT")
        print("="*40)
        print(f"File: {filename}")
        
        confirm = input("Are you sure you want to delete this prompt? (y/N): ").strip().lower()
        
        if confirm == 'y':
            try:
                os.remove(filepath)
                print("Prompt deleted successfully")
            except Exception as e:
                print(f"Error deleting file: {e}")
        else:
            print("Deletion cancelled")
        
        input("Press Enter to continue...")
