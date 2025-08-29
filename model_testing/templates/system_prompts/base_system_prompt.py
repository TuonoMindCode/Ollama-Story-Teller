import os
import datetime
from typing import Dict, List, Tuple

class BaseSystemPromptManager:
    """Base class for system prompt management"""
    
    def __init__(self, templates_folder: str, model_tester):
        self.templates_folder = templates_folder
        self.model_tester = model_tester
        
        # Genre and style options
        self.genres = ['Romance', 'Thriller', 'Literary', 'Sci-Fi', 'Fantasy', 'Mystery', 'Horror', 'General', 'Other']
        self.writing_styles = ['Minimalist', 'Descriptive', 'Literary', 'Dialogue-Heavy', 'Action-Packed', 'Atmospheric', 'Other']
    
    def _save_system_prompt(self, prompt: str, genre: str, style: str) -> str:
        """Save system prompt to file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        genre_clean = self._sanitize_filename_part(genre)
        style_clean = self._sanitize_filename_part(style)
        
        filename = f"system_prompt_{genre_clean}_{style_clean}_{timestamp}.txt"
        filepath = os.path.join(self.templates_folder, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt.strip())
        
        return filename
    
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
