"""Comprehensive genre-specific system prompts with detailed techniques"""

DETECTIVE_STYLES = {
    "Classic Mystery": {
        "description": "Traditional whodunit with logical deduction and fair play",
        "techniques": [
            "Present clues fairly to the reader without withholding crucial information",
            "Use logical deduction and step-by-step reasoning in investigations", 
            "Include red herrings that mislead but don't cheat or break fair play rules",
            "Build tension through methodical investigation and gradual revelation",
            "Show the detective's thought process and reasoning clearly to readers",
            "Maintain proper pacing between clue discovery and deduction",
            "Use dialogue to reveal character motivations and advance the mystery"
        ],
        "elements": [
            "Crime scene analysis", "Witness interviews", "Physical evidence examination",
            "Timeline reconstruction", "Motive examination", "Alibi verification",
            "Logical deduction", "Fair play cluing", "Red herrings", "Reveal scenes"
        ],
        "tone": "Intellectual, methodical, fair, engaging"
    },
    
    "Noir & Hard-boiled": {
        "description": "Dark, cynical detective fiction with moral ambiguity",
        "techniques": [
            "Use first-person narration with a world-weary, cynical tone",
            "Create atmospheric descriptions emphasizing urban decay and corruption",
            "Show moral ambiguity where right and wrong are not clearly defined",
            "Include dangerous romantic relationships and femme fatales",
            "Balance violent action with deep psychological insight",
            "Use hardboiled dialogue that's sharp, witty, and realistic",
            "Explore themes of justice, corruption, and personal redemption"
        ],
        "elements": [
            "Dark urban atmosphere", "Corrupt officials", "Femme fatales",
            "Violent confrontations", "Internal monologue", "Moral complexity",
            "Cynical worldview", "Social commentary", "Personal demons"
        ],
        "tone": "Dark, cynical, atmospheric, morally complex"
    },
    
    "Police Procedural": {
        "description": "Realistic police work with authentic procedures and teamwork",
        "techniques": [
            "Show realistic police protocols, procedures, and chain of command",
            "Include accurate forensic science and technical investigation methods",
            "Depict authentic teamwork, department politics, and bureaucracy",
            "Use proper police terminology, codes, and communication methods",
            "Balance procedural details with character development and plot advancement",
            "Show the legal constraints and requirements officers must follow",
            "Include the emotional and psychological impact on law enforcement"
        ],
        "elements": [
            "Forensic analysis", "Department hierarchy", "Legal procedures",
            "Evidence chain of custody", "Warrant requirements", "Team dynamics",
            "Technical equipment", "Interagency cooperation", "Court testimony"
        ],
        "tone": "Professional, detailed, realistic, team-focused"
    },
    
    "Psychological Thriller": {
        "description": "Mind games, psychological manipulation, and mental complexity",
        "techniques": [
            "Explore the complex psychology of both detective and criminal minds",
            "Use unreliable narration to create doubt and psychological tension",
            "Build suspense through psychological pressure rather than physical danger",
            "Show the mental and emotional toll investigation takes on characters",
            "Create intricate mind games between investigator and suspect",
            "Use internal conflict and psychological profiling as key plot elements",
            "Blur the lines between sanity and madness, truth and perception"
        ],
        "elements": [
            "Psychological profiling", "Mind games", "Memory distortion",
            "Mental instability", "Obsession", "Paranoia", "Identity confusion",
            "Manipulation tactics", "Psychological warfare", "Unreliable perception"
        ],
        "tone": "Tense, psychological, unsettling, intellectually complex"
    },
    
    "Cozy Mystery": {
        "description": "Gentle mysteries in small communities with amateur sleuths",
        "techniques": [
            "Focus on puzzle-solving and intellectual challenges over violence",
            "Develop rich community relationships and local character dynamics",
            "Use local knowledge, gossip, and community secrets as investigation tools",
            "Keep violence minimal, tasteful, and typically off-screen",
            "Emphasize character development, relationships, and community setting",
            "Include gentle humor and warm character interactions",
            "Show how amateur detective uses unique skills or knowledge"
        ],
        "elements": [
            "Small town secrets", "Amateur detective", "Community relationships",
            "Local knowledge", "Gentle humor", "Minimal violence", "Cozy settings",
            "Recurring characters", "Community events", "Personal connections"
        ],
        "tone": "Warm, engaging, puzzle-focused, community-oriented"
    },
    
    "Cold Case": {
        "description": "Investigating old unsolved crimes with fresh perspectives",
        "techniques": [
            "Contrast past and present investigation methods and technology",
            "Show how time has changed suspects, witnesses, and evidence",
            "Use flashbacks effectively to reveal past events and clues",
            "Explore how cold cases emotionally affect investigators and families",
            "Show the challenge of reconstructing events from incomplete records",
            "Include the role of new technology in solving old crimes",
            "Balance historical research with modern investigative techniques"
        ],
        "elements": [
            "Old case files", "Aged evidence", "Changed witnesses", "New technology",
            "Historical context", "Family impact", "Memory reliability", "Time pressure",
            "Archive research", "Renewed hope", "Justice delayed"
        ],
        "tone": "Reflective, persistent, hope against odds, historically layered"
    }
}

ROMANCE_STYLES = {
    "Contemporary Romance": {
        "description": "Modern love stories with realistic relationships and current settings",
        "techniques": [
            "Create authentic modern dialogue and situations",
            "Balance romantic tension with realistic relationship challenges",
            "Show character growth through romantic development",
            "Include contemporary social issues and cultural contexts"
        ],
        "elements": ["Modern settings", "Career conflicts", "Family dynamics", "Personal growth"],
        "tone": "Realistic, relatable, emotionally satisfying"
    },
    
    "Historical Romance": {
        "description": "Love stories set in past eras with period-accurate details",
        "techniques": [
            "Research and include accurate historical details and customs",
            "Create period-appropriate dialogue and social constraints",
            "Show how historical context affects romantic relationships",
            "Balance historical accuracy with romantic fantasy elements"
        ],
        "elements": ["Historical accuracy", "Social constraints", "Period customs", "Cultural conflicts"],
        "tone": "Romantic, historically rich, culturally immersive"
    }
}

FANTASY_STYLES = {
    "High Fantasy": {
        "description": "Epic fantasy worlds with complex magic systems and grand quests",
        "techniques": [
            "Build consistent, detailed magical systems with clear rules and limitations",
            "Create rich worldbuilding with unique cultures, histories, and geographies",
            "Develop epic conflicts between good and evil with high stakes",
            "Show character growth through heroic journeys and magical challenges"
        ],
        "elements": ["Magic systems", "Worldbuilding", "Epic quests", "Mythical creatures"],
        "tone": "Epic, magical, heroic, grand in scope"
    },
    
    "Urban Fantasy": {
        "description": "Fantasy elements hidden within modern urban settings",
        "techniques": [
            "Blend supernatural elements seamlessly with contemporary urban life",
            "Create hidden magical societies operating alongside normal world",
            "Show the contrast between mundane and magical reality",
            "Use urban settings as both backdrop and integral plot element"
        ],
        "elements": ["Hidden magic", "Urban settings", "Secret societies", "Modern problems"],
        "tone": "Modern, mysterious, edgy, urban"
    }
}

SCIFI_STYLES = {
    "Hard Science Fiction": {
        "description": "Scientifically accurate SF with detailed technical explanations",
        "techniques": [
            "Base speculative elements on real scientific principles and research",
            "Include detailed technical explanations that feel authentic",
            "Explore the realistic consequences of technological advancement",
            "Balance scientific accuracy with storytelling needs"
        ],
        "elements": ["Scientific accuracy", "Technical details", "Future technology", "Scientific method"],
        "tone": "Intellectual, technical, scientifically grounded"
    },
    
    "Space Opera": {
        "description": "Grand space adventures with galactic scope and epic conflicts",
        "techniques": [
            "Create vast galactic civilizations with complex politics and conflicts",
            "Include epic space battles and advanced technology",
            "Develop multiple alien species with unique cultures and motivations",
            "Balance action, adventure, and character development across galactic settings"
        ],
        "elements": ["Galactic empires", "Space battles", "Alien species", "Advanced technology"],
        "tone": "Epic, adventurous, grand in scale, action-packed"
    }
}

def build_comprehensive_prompt(style_data, selected_techniques=None, word_count=None, additional_elements=None):
    """Build a comprehensive system prompt from style data"""
    
    # Base prompt structure
    base_prompt = f"""You are an expert {style_data.get('tone', 'professional')} writer specializing in {style_data['description']}.

CORE WRITING TECHNIQUES:
"""
    
    # Add techniques
    techniques = selected_techniques if selected_techniques else style_data['techniques']
    for i, technique in enumerate(techniques, 1):
        base_prompt += f"{i}. {technique}\n"
    
    base_prompt += f"\nKEY ELEMENTS TO INCLUDE:\n"
    
    # Add elements
    elements = style_data['elements']
    if additional_elements:
        elements.extend(additional_elements)
    
    elements_text = ", ".join(elements)
    base_prompt += f"{elements_text}\n"
    
    base_prompt += f"\nTONE AND STYLE:\n"
    base_prompt += f"Maintain a {style_data['tone']} tone throughout the scene.\n"
    
    if word_count:
        base_prompt += f"\nLENGTH REQUIREMENT:\n"
        base_prompt += f"Write approximately {word_count} words.\n"
    
    base_prompt += f"\nFOCUS:\n"
    base_prompt += f"Create engaging, well-paced scenes that exemplify the best of this genre while maintaining authenticity and reader engagement."
    
    return base_prompt
