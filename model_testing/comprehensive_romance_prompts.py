"""Comprehensive Romance scene system prompts with detailed techniques"""

ROMANCE_STYLES = {
    "Contemporary Romance": {
        "description": "Modern love stories with realistic relationships, current settings, and relatable conflicts",
        "techniques": [
            "Create authentic modern dialogue that reflects contemporary speech patterns",
            "Balance romantic tension with realistic relationship challenges and obstacles",
            "Show character growth through romantic development and emotional vulnerability",
            "Include contemporary social issues and cultural contexts that affect relationships",
            "Use modern technology and social media as both connection and conflict tools",
            "Develop workplace dynamics, career conflicts, and work-life balance issues",
            "Show family dynamics and how they influence romantic relationships"
        ],
        "elements": [
            "Modern settings", "Career conflicts", "Family dynamics", "Personal growth",
            "Social media influence", "Contemporary culture", "Realistic obstacles",
            "Modern communication", "Urban lifestyle", "Current social issues"
        ],
        "tone": "Realistic, relatable, emotionally satisfying, contemporary"
    },
    
    "Historical Romance": {
        "description": "Love stories set in past eras with period-accurate details, customs, and social constraints",
        "techniques": [
            "Research and include accurate historical details, customs, and social expectations",
            "Create period-appropriate dialogue while keeping it accessible to modern readers",
            "Show how historical context and social constraints affect romantic relationships",
            "Include accurate details about clothing, mannerisms, and daily life of the era",
            "Balance historical accuracy with romantic fantasy and emotional satisfaction",
            "Show class differences, arranged marriages, and societal expectations of the time",
            "Use historical events and settings as both backdrop and plot catalyst"
        ],
        "elements": [
            "Historical accuracy", "Period customs", "Social constraints", "Class differences",
            "Arranged marriages", "Historical events", "Period dialogue", "Cultural traditions",
            "Societal expectations", "Historical settings", "Traditional courtship", "Era-specific conflicts"
        ],
        "tone": "Romantic, historically rich, culturally immersive, traditionally elegant"
    },
    
    "Paranormal Romance": {
        "description": "Romance with supernatural elements, magical creatures, and otherworldly settings",
        "techniques": [
            "Blend supernatural elements seamlessly with romantic relationship development",
            "Create consistent supernatural world-building with clear rules and limitations",
            "Show how supernatural abilities or nature affects romantic relationships",
            "Balance paranormal action with intimate romantic and emotional scenes",
            "Include supernatural politics and conflicts that threaten the romantic relationship",
            "Show the challenges of human-supernatural or supernatural-supernatural relationships",
            "Use supernatural bonds, mates, or connections as romantic plot devices"
        ],
        "elements": [
            "Supernatural creatures", "Magic systems", "Otherworldly settings", "Supernatural politics",
            "Magical bonds", "Paranormal abilities", "Supernatural threats", "Human-supernatural relations",
            "Magical conflicts", "Supernatural societies", "Paranormal romance tropes", "Mystical connections"
        ],
        "tone": "Mystical, passionate, supernaturally charged, emotionally intense"
    },
    
    "Romantic Suspense": {
        "description": "Romance combined with mystery, danger, and suspenseful plots that threaten the relationship",
        "techniques": [
            "Balance romantic development with suspenseful plot advancement equally",
            "Use danger and mystery to bring romantic characters together organically",
            "Create external threats that test and strengthen the romantic relationship",
            "Show how trust develops between characters in dangerous circumstances",
            "Include investigation, mystery-solving, and protective instincts as romantic elements",
            "Balance action scenes with intimate moments and emotional vulnerability",
            "Use secrets, hidden identities, and revelations to create romantic tension"
        ],
        "elements": [
            "Mystery elements", "External danger", "Protective instincts", "Trust building",
            "Secret identities", "Investigation plots", "Life-threatening situations", "Suspenseful pacing",
            "Hidden secrets", "Romantic protection", "Dangerous attraction", "Thriller elements"
        ],
        "tone": "Suspenseful, passionate, dangerous, emotionally charged"
    },
    
    "Friends to Lovers": {
        "description": "Romance that develops from established friendship, showing the transition from platonic to romantic love",
        "techniques": [
            "Show the gradual shift from friendship to romantic awareness convincingly",
            "Include moments of realization where characters see each other differently",
            "Show the fear of risking a valued friendship for potential romantic love",
            "Use shared history, inside jokes, and deep knowledge to build romantic foundation",
            "Include jealousy when one friend dates others as a catalyst for recognition",
            "Show how existing intimacy and trust translates into romantic relationship",
            "Balance maintaining friendship dynamics with developing romantic tension"
        ],
        "elements": [
            "Established friendship", "Gradual realization", "Shared history", "Deep trust",
            "Fear of change", "Jealousy catalysts", "Inside jokes", "Comfortable intimacy",
            "Friend group dynamics", "Transition anxiety", "Romantic awakening", "Friendship foundation"
        ],
        "tone": "Warm, comfortable, gradually passionate, emotionally secure"
    },
    
    "Enemies to Lovers": {
        "description": "Romance that develops from initial conflict, hostility, or opposition between characters",
        "techniques": [
            "Create believable reasons for initial antagonism that can be overcome",
            "Show gradual understanding and respect developing beneath the conflict",
            "Use verbal sparring and heated arguments to build romantic tension",
            "Include moments where characters see past their assumptions about each other",
            "Show how opposition can mask attraction and create passionate intensity",
            "Use forced proximity or shared challenges to break down barriers",
            "Balance maintaining conflict tension with showing character growth and change"
        ],
        "elements": [
            "Initial conflict", "Verbal sparring", "Gradual understanding", "Hidden attraction",
            "Forced proximity", "Character assumptions", "Passionate intensity", "Conflict resolution",
            "Personal growth", "Barrier breakdown", "Romantic tension", "Heated encounters"
        ],
        "tone": "Intense, passionate, conflicted, dramatically satisfying"
    },
    
    "Second Chance Romance": {
        "description": "Romance between characters who had a previous relationship that ended, now reuniting",
        "techniques": [
            "Show realistic reasons why the relationship ended and how characters have grown",
            "Include unresolved feelings, regret, and the weight of shared history",
            "Show how characters have changed and matured since their previous relationship",
            "Use past memories and experiences as both obstacles and connection points",
            "Include family or friends who remember the previous relationship and have opinions",
            "Show the difficulty of rebuilding trust and overcoming past hurt",
            "Balance nostalgia with the reality of creating something new together"
        ],
        "elements": [
            "Shared history", "Past hurt", "Personal growth", "Unresolved feelings",
            "Trust rebuilding", "Changed circumstances", "Mature perspectives", "Regret and forgiveness",
            "Family opinions", "Memory triggers", "Second chances", "Renewed connection"
        ],
        "tone": "Nostalgic, mature, emotionally complex, hopeful"
    },
    
    "Forbidden Romance": {
        "description": "Romance that faces significant social, professional, or personal barriers and taboos",
        "techniques": [
            "Create compelling reasons why the romance is forbidden or socially unacceptable",
            "Show the internal conflict between desire and duty, love and responsibility",
            "Use secrecy, stolen moments, and hidden meetings to build romantic tension",
            "Include the cost and consequences of pursuing forbidden love",
            "Show how external pressure and disapproval affect the romantic relationship",
            "Balance the thrill of forbidden love with realistic consequences and challenges",
            "Include moral dilemmas and difficult choices between love and other values"
        ],
        "elements": [
            "Social barriers", "Secret meetings", "Internal conflict", "Moral dilemmas",
            "External pressure", "Hidden relationships", "Consequential choices", "Duty vs desire",
            "Social disapproval", "Stolen moments", "Risk and sacrifice", "Forbidden attraction"
        ],
        "tone": "Intense, secretive, morally complex, passionately desperate"
    }
}

def build_romance_prompt(style_data, selected_techniques=None, word_count=None, additional_elements=None, heat_level="moderate"):
    """Build a comprehensive romance system prompt from style data"""
    
    # Base prompt structure
    base_prompt = f"""You are an expert romance writer specializing in {style_data['description']}.

CORE ROMANCE WRITING TECHNIQUES:
"""
    
    # Add techniques
    techniques = selected_techniques if selected_techniques else style_data['techniques']
    for i, technique in enumerate(techniques, 1):
        base_prompt += f"{i}. {technique}\n"
    
    base_prompt += f"\nROMANCE ELEMENTS TO INCLUDE:\n"
    
    # Add elements
    elements = style_data['elements']
    if additional_elements:
        elements.extend(additional_elements)
    
    elements_text = ", ".join(elements)
    base_prompt += f"{elements_text}\n"
    
    base_prompt += f"\nROMANCE AND INTIMACY LEVEL:\n"
    if heat_level == "sweet":
        base_prompt += "Focus on emotional intimacy, tender moments, and romantic gestures with minimal physical content.\n"
    elif heat_level == "steamy":
        base_prompt += "Include passionate physical attraction, sensual tension, and intimate romantic scenes.\n"
    else:
        base_prompt += "Balance emotional intimacy with moderate physical attraction and romantic chemistry.\n"
    
    base_prompt += f"Show genuine character attraction, emotional connection, and romantic development.\n"
    base_prompt += f"Include romantic tension, meaningful dialogue, and relationship-building moments.\n"
    
    base_prompt += f"\nTONE AND STYLE:\n"
    base_prompt += f"Maintain a {style_data['tone']} tone throughout the scene.\n"
    base_prompt += f"Balance romantic elements with realistic character development and authentic emotions.\n"
    
    if word_count:
        base_prompt += f"\nLENGTH REQUIREMENT:\n"
        base_prompt += f"Write approximately {word_count} words.\n"
    
    base_prompt += f"\nFOCUS:\n"
    base_prompt += f"Create emotionally satisfying romance scenes that develop authentic relationships while maintaining romantic tension and reader engagement."
    
    return base_prompt
