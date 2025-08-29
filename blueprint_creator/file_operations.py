"""File operations for blueprint creation"""

import os
import time

class FileOperations:
    def __init__(self, blueprint_folder):
        self.blueprint_folder = blueprint_folder
    
    def save_generated_blueprint(self, blueprint_data, content):
        """Save the generated blueprint to file"""
        try:
            # Create filename with genre and subgenre
            name = blueprint_data['name']
            genre = blueprint_data['genre'].lower().replace(' ', '_').replace('/', '_')
            
            if blueprint_data['subgenre'] != 'Not chosen':
                subgenre = blueprint_data['subgenre'].lower().replace(' ', '_').replace('/', '_')
                filename = f"{name}.{genre}.{subgenre}.story.txt"
            else:
                filename = f"{name}.{genre}.story.txt"
            
            filepath = os.path.join(self.blueprint_folder, filename)
            
            # Create full content with metadata
            full_content = self.create_full_blueprint_content(blueprint_data, content)
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(full_content)
            
            print(f"✅ Blueprint saved as: {filename}")
            print(f"   Location: {filepath}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving blueprint: {e}")
            return None

    def create_full_blueprint_content(self, blueprint_data, generated_content):
        """Create the full blueprint content with metadata"""
        content = []
        
        # Header with metadata
        content.append("STORY BLUEPRINT")
        content.append("=" * 50)
        content.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"Name: {blueprint_data['name']}")
        content.append(f"Genre: {blueprint_data['genre']}")
        content.append(f"Created with: {blueprint_data['llm_model']}")
        content.append(f"Max tokens used: {blueprint_data['max_tokens']:,}")
        content.append(f"Target story length: {blueprint_data['target_length']}")
        
        if blueprint_data['subgenre'] != 'Not chosen':
            content.append(f"Subgenre: {blueprint_data['subgenre']}")
        
        # Add generation stats
        word_count = len(generated_content.split())
        char_count = len(generated_content)
        content.append(f"Generated content - Words: {word_count:,}, Characters: {char_count:,}")
        
        content.append("")
        content.append("SPECIFICATIONS USED:")
        
        for key, value in blueprint_data.items():
            if key not in ['name', 'genre', 'subgenre', 'llm_model', 'max_tokens', 'target_length'] and value != 'Not chosen' and value:
                if key == 'special_elements' and value:
                    content.append(f"- Special elements: {', '.join(value)}")
                elif value != 'Not chosen':
                    formatted_key = key.replace('_', ' ').title()
                    content.append(f"- {formatted_key}: {value}")
        
        content.append("")
        content.append("GENERATED BLUEPRINT:")
        content.append("-" * 40)
        content.append(generated_content)
        
        return "\n".join(content)
