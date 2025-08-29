class ContextTracker:
    """Tracks story context for narrative consistency in auto-tracking mode"""
    
    def __init__(self):
        self.characters = {}
        self.locations = {}
        self.plot_points = []
        self.themes = []
        self.objects = {}
        
    def analyze_and_track_content(self, content):
        """Analyze content and extract/track entities for consistency"""
        # This is a placeholder implementation
        # In a full implementation, you might use NLP to extract entities
        
        # For now, we'll do basic tracking
        lines = content.split('\n')
        for line in lines:
            # Simple character detection (names in quotes or capitalized words)
            words = line.split()
            for word in words:
                if word.istitle() and len(word) > 2:
                    # Potential character name
                    if word not in self.characters:
                        self.characters[word] = {
                            'mentions': 1,
                            'first_seen': len(self.plot_points)
                        }
                    else:
                        self.characters[word]['mentions'] += 1
        
        # Track this content as a plot point
        self.plot_points.append({
            'content_preview': content[:100] + "..." if len(content) > 100 else content,
            'scene_number': len(self.plot_points) + 1
        })
    
    def get_context_summary(self):
        """Get a summary of tracked context for consistency"""
        summary_parts = []
        
        if self.characters:
            char_list = [f"{name} (mentioned {info['mentions']} times)" 
                        for name, info in self.characters.items()]
            summary_parts.append(f"Characters: {', '.join(char_list[:5])}")  # Top 5
        
        if self.locations:
            loc_list = list(self.locations.keys())
            summary_parts.append(f"Locations: {', '.join(loc_list[:3])}")  # Top 3
        
        if self.plot_points:
            summary_parts.append(f"Scenes written: {len(self.plot_points)}")
        
        return '\n'.join(summary_parts) if summary_parts else "No context tracked yet"
    
    def get_character_info(self, character_name):
        """Get information about a specific character"""
        return self.characters.get(character_name, None)
    
    def add_character(self, name, description):
        """Manually add character information"""
        if name not in self.characters:
            self.characters[name] = {
                'mentions': 0,
                'first_seen': len(self.plot_points),
                'description': description
            }
    
    def add_location(self, name, description):
        """Manually add location information"""
        self.locations[name] = {
            'description': description,
            'first_seen': len(self.plot_points)
        }
    
    def get_story_cast(self):
        """Get a summary of story characters (method that was missing)"""
        if not self.characters:
            return "No characters tracked yet"
        
        cast_summary = []
        for char_name, char_info in self.characters.items():
            mentions = char_info.get('mentions', 0)
            cast_summary.append(f"{char_name} (mentioned {mentions} times)")
        
        return "Story Cast: " + ", ".join(cast_summary[:5])  # Top 5 characters
