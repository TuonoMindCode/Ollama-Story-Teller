import re
from typing import Dict, Set, List

class AutoStoryContext:
    """Automatically tracks famous locations that appear in scenes"""
    
    def __init__(self):
        # Track what appeared where - only locations
        self.entities_in_story: Dict[str, List[int]] = {}  # location_name -> [scene_numbers]
        self.entity_roles: Dict[str, str] = {}  # location_name -> type (landmark, city, etc.)
        self.current_scene = 0
    
    def auto_detect_entities(self, scene_content: str, scene_number: int):
        """Automatically find famous locations in scene"""
        # Enhanced pattern to catch location names
        patterns = [
            # Famous landmarks/buildings
            r'\b(?:White House|Eiffel Tower|Big Ben|Statue of Liberty|Golden Gate Bridge)\b',
            r'\b(?:Empire State Building|Times Square|Central Park|Hyde Park)\b',
            r'\b(?:Buckingham Palace|Tower of London|Notre Dame|Louvre)\b',
            r'\b(?:Sydney Opera House|London Bridge|Brooklyn Bridge)\b',
            
            # Major cities (with context to avoid false matches)
            r'\b(?:New York|Los Angeles|Chicago|Houston|Philadelphia|Phoenix|San Antonio)\b(?:\s+City)?',
            r'\b(?:London|Paris|Tokyo|Berlin|Rome|Madrid|Amsterdam|Vienna)\b',
            r'\b(?:Sydney|Melbourne|Toronto|Vancouver|Montreal)\b',
            
            # Natural landmarks
            r'\b(?:Grand Canyon|Mount Everest|Niagara Falls|Yellowstone)\b',
            r'\b(?:Amazon|Sahara Desert|Rocky Mountains|Alps)\b',
            
            # Pattern for "Place Name + descriptor"
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Bridge|Park|Hotel|Station|Building|Tower|Mall|Airport|Museum|Cathedral|Castle)\b',
        ]
        
        found_locations = set()
        for pattern in patterns:
            matches = re.findall(pattern, scene_content, re.IGNORECASE)
            found_locations.update(matches)
        
        # Process all found locations
        for location in found_locations:
            location = location.strip()
            if len(location) > 2:
                # Add to tracking
                if location not in self.entities_in_story:
                    self.entities_in_story[location] = []
                if scene_number not in self.entities_in_story[location]:
                    self.entities_in_story[location].append(scene_number)
                
                # Determine location type
                if location not in self.entity_roles:
                    self.entity_roles[location] = self._guess_location_type(location, scene_content)
    
    def _guess_location_type(self, location: str, scene_content: str) -> str:
        """Determine what type of location this is"""
        location_lower = location.lower()
        
        # Famous landmarks
        landmarks = ['white house', 'eiffel tower', 'big ben', 'statue of liberty', 'golden gate bridge',
                    'empire state building', 'times square', 'buckingham palace', 'tower of london',
                    'notre dame', 'louvre', 'sydney opera house']
        
        if any(landmark in location_lower for landmark in landmarks):
            return "landmark"
        
        # Natural features
        natural = ['grand canyon', 'mount everest', 'niagara falls', 'yellowstone', 'amazon',
                  'sahara', 'rocky mountains', 'alps']
        
        if any(natural_place in location_lower for natural_place in natural):
            return "natural_landmark"
        
        # Cities
        major_cities = ['new york', 'los angeles', 'chicago', 'london', 'paris', 'tokyo', 'berlin',
                       'rome', 'madrid', 'sydney', 'melbourne', 'toronto', 'vancouver']
        
        if any(city in location_lower for city in major_cities):
            return "city"
        
        # Buildings/structures
        if any(word in location_lower for word in ['bridge', 'building', 'tower', 'hotel', 'station']):
            return "building"
        
        # Parks/outdoor spaces  
        if any(word in location_lower for word in ['park', 'garden', 'square']):
            return "outdoor_space"
        
        return "location"
    
    def get_consistency_context(self, scene_number: int) -> str:
        """Generate context for locations that appeared in previous scenes"""
        if not self.entities_in_story:
            return ""
        
        context_parts = []
        
        # Group locations by type
        previous_locations = {}
        for location, scenes in self.entities_in_story.items():
            previous_scenes = [s for s in scenes if s < scene_number]
            if previous_scenes:
                first_scene = min(previous_scenes)
                location_type = self.entity_roles.get(location, "location")
                if location_type not in previous_locations:
                    previous_locations[location_type] = []
                previous_locations[location_type].append(f"{location} (first appeared scene {first_scene})")
        
        if previous_locations:
            context_parts.append("LOCATION CONSISTENCY TRACKING - These places were already featured:")
            
            # Organize by type for clarity
            type_order = ["landmark", "city", "natural_landmark", "building", "outdoor_space", "location"]
            type_titles = {
                "landmark": "Famous Landmarks",
                "city": "Cities", 
                "natural_landmark": "Natural Features",
                "building": "Buildings/Structures",
                "outdoor_space": "Parks/Outdoor Spaces",
                "location": "Other Locations"
            }
            
            for location_type in type_order:
                if location_type in previous_locations:
                    title = type_titles.get(location_type, location_type.replace('_', ' ').title())
                    context_parts.append(f"\n{title}:")
                    for location in previous_locations[location_type]:
                        context_parts.append(f"  • {location}")
            
            context_parts.append("\nIMPORTANT: Maintain consistency with how these locations were previously described.")
            context_parts.append("Use their established appearance, atmosphere, and distinctive features.")
        
        return "\n".join(context_parts)

    def get_story_cast(self) -> str:
        """Get organized summary of all locations in the story"""
        if not self.entities_in_story:
            return "No notable locations detected."
        
        # Group by type
        locations_by_type = {}
        for location, scenes in self.entities_in_story.items():
            location_type = self.entity_roles.get(location, "location")
            if location_type not in locations_by_type:
                locations_by_type[location_type] = []
            scene_list = ", ".join(map(str, sorted(scenes)))
            locations_by_type[location_type].append(f"{location} (scenes: {scene_list})")
        
        summary = ["STORY LOCATIONS:"]
        summary.append("=" * 40)
        
        # Display in logical order
        type_order = ["landmark", "city", "natural_landmark", "building", "outdoor_space", "location"]
        type_titles = {
            "landmark": "🏛️ FAMOUS LANDMARKS",
            "city": "🌆 CITIES",
            "natural_landmark": "🏔️ NATURAL FEATURES", 
            "building": "🏢 BUILDINGS/STRUCTURES",
            "outdoor_space": "🌳 PARKS/OUTDOOR SPACES",
            "location": "📍 OTHER LOCATIONS"
        }
        
        for location_type in type_order:
            if location_type in locations_by_type:
                summary.append(f"\n{type_titles[location_type]}:")
                for location in sorted(locations_by_type[location_type]):
                    summary.append(f"  • {location}")
        
        return "\n".join(summary)

    def get_entities_count(self) -> Dict[str, int]:
        """Get count of locations by type"""
        counts = {}
        for location_type in self.entity_roles.values():
            counts[location_type] = counts.get(location_type, 0) + 1
        return counts