"""Comprehensive Fantasy scene system prompts with detailed techniques"""

FANTASY_STYLES = {
    "High Fantasy": {
        "description": "Epic fantasy worlds with complex magic systems and grand quests",
        "techniques": [
            "Build consistent, detailed magic systems with clear rules and limitations",
            "Create rich worldbuilding with unique cultures, histories, and geographies", 
            "Develop epic conflicts between good and evil with world-changing stakes",
            "Show character growth through heroic journeys and magical challenges",
            "Balance magical wonder with realistic character emotions and motivations",
            "Use prophecies, ancient lore, and mystical elements to drive plot forward",
            "Create memorable fantasy races and creatures with distinct characteristics"
        ],
        "elements": [
            "Magic systems", "Epic quests", "Mythical creatures", "Ancient prophecies",
            "Fantasy races", "Magical artifacts", "Heroic journeys", "Good vs evil",
            "World-changing stakes", "Magical landscapes", "Divine intervention"
        ],
        "tone": "Epic, heroic, magical, grand in scope"
    },
    
    "Dark Fantasy": {
        "description": "Fantasy with horror elements, moral ambiguity, and mature themes",
        "techniques": [
            "Blend fantasy elements with horror, dread, and psychological darkness",
            "Create morally ambiguous characters where good and evil are blurred",
            "Use gothic atmosphere with decaying kingdoms and corrupted magic",
            "Show the terrible cost of magic and power on users and society",
            "Include body horror, transformation, and supernatural corruption",
            "Balance fantasy wonder with genuine fear and unsettling imagery",
            "Explore themes of sacrifice, corruption, and the price of power"
        ],
        "elements": [
            "Corrupted magic", "Moral ambiguity", "Gothic atmosphere", "Supernatural horror",
            "Decaying realms", "Cursed artifacts", "Demonic entities", "Forbidden knowledge",
            "Blood magic", "Undead creatures", "Psychological darkness", "Cosmic horror"
        ],
        "tone": "Dark, unsettling, morally complex, atmospheric"
    },
    
    "Urban Fantasy": {
        "description": "Fantasy elements hidden within modern urban settings",
        "techniques": [
            "Seamlessly blend supernatural elements with contemporary urban life",
            "Create hidden magical societies operating alongside the normal world",
            "Show the contrast and conflict between mundane and magical reality",
            "Use modern technology in creative interaction with ancient magic",
            "Develop supernatural politics and conflicts within city environments",
            "Include modern problems solved through magical or supernatural means",
            "Balance urban realism with fantastical elements and wonder"
        ],
        "elements": [
            "Hidden magic", "Modern settings", "Secret societies", "Urban mythology",
            "Supernatural politics", "Magic-technology blend", "City supernatural",
            "Contemporary problems", "Masquerade elements", "Modern mythology"
        ],
        "tone": "Modern, mysterious, edgy, urban cool"
    },
    
    "Medieval Fantasy": {
        "description": "Traditional fantasy with knights, dragons, and medieval-inspired settings",
        "techniques": [
            "Create authentic medieval-inspired societies with appropriate social structures",
            "Include classic fantasy elements like dragons, knights, and magical kingdoms",
            "Show feudal politics, court intrigue, and medieval warfare accurately",
            "Balance traditional fantasy tropes with fresh, original storytelling",
            "Use period-appropriate dialogue and cultural elements convincingly",
            "Include chivalric codes, honor systems, and medieval values",
            "Create compelling castle, village, and wilderness settings"
        ],
        "elements": [
            "Medieval kingdoms", "Knights and chivalry", "Dragons", "Castles",
            "Court intrigue", "Feudal systems", "Medieval warfare", "Honor codes",
            "Village life", "Guilds and crafts", "Religious orders", "Noble houses"
        ],
        "tone": "Traditional, chivalric, adventurous, honor-bound"
    },
    
    "Magical Realism": {
        "description": "Subtle magic woven into realistic, everyday settings",
        "techniques": [
            "Integrate magical elements naturally into realistic, everyday situations",
            "Treat supernatural occurrences as normal parts of the world",
            "Focus on character emotions and relationships over magical spectacle",
            "Use magic to illuminate deeper truths about human nature and society",
            "Maintain ambiguity about whether magic is real or metaphorical",
            "Ground fantastical elements in cultural traditions and folklore",
            "Create dreamlike, poetic prose that blurs reality and fantasy"
        ],
        "elements": [
            "Subtle magic", "Everyday settings", "Cultural folklore", "Dreamlike atmosphere",
            "Symbolic elements", "Emotional truth", "Blurred reality", "Poetic prose",
            "Human relationships", "Cultural traditions", "Metaphorical magic"
        ],
        "tone": "Subtle, poetic, emotionally rich, culturally grounded"
    },
    
    "Sword and Sorcery": {
        "description": "Action-focused fantasy with warriors, magic, and adventure",
        "techniques": [
            "Focus on action, adventure, and physical conflict over complex plotting",
            "Create powerful warrior protagonists with martial prowess and courage",
            "Include exciting combat scenes with detailed fight choreography",
            "Use magic as a tool for conflict and adventure rather than world-building",
            "Maintain fast pacing with constant danger and excitement",
            "Show personal struggles and individual heroism over epic world-saving",
            "Include exotic locations, dangerous quests, and treasure hunting"
        ],
        "elements": [
            "Warrior heroes", "Combat scenes", "Adventure quests", "Exotic locations",
            "Martial prowess", "Personal conflicts", "Treasure hunting", "Dangerous magic",
            "Individual heroism", "Fast pacing", "Physical challenges", "Survival"
        ],
        "tone": "Action-packed, adventurous, fast-paced, personally heroic"
    },
    
    "Steampunk Fantasy": {
        "description": "Victorian-era inspired fantasy with magical technology and industrial magic",
        "techniques": [
            "Blend Victorian-era aesthetics with magical and mechanical innovations",
            "Create magical technology powered by arcane forces and steam power",
            "Show the social tensions between traditional magic and new technology",
            "Include airships, clockwork mechanisms, and magical industrial processes",
            "Develop class conflicts between magical aristocracy and industrial workers",
            "Use Victorian social customs and mannerisms authentically",
            "Balance steampunk technology with traditional fantasy elements"
        ],
        "elements": [
            "Steam-powered magic", "Victorian aesthetics", "Airships", "Clockwork devices",
            "Industrial magic", "Class conflicts", "Magical technology", "Social tensions",
            "Arcane engineering", "Mechanical familiars", "Steam and sorcery"
        ],
        "tone": "Victorian, innovative, socially conscious, technologically magical"
    },
    
    "Portal Fantasy": {
        "description": "Characters from our world transported to magical realms",
        "techniques": [
            "Show realistic reactions to discovering magical worlds and abilities",
            "Contrast modern world knowledge with fantasy world requirements",
            "Develop character growth through adaptation to magical circumstances",
            "Use the outsider perspective to explore and explain the fantasy world",
            "Show culture shock and adjustment to different social systems",
            "Include the tension between wanting to return home and embracing new world",
            "Balance fish-out-of-water humor with genuine adventure and growth"
        ],
        "elements": [
            "World transition", "Culture shock", "Adaptation challenges", "Outsider perspective",
            "Modern vs magical", "Personal growth", "Home vs adventure", "Fish-out-of-water",
            "Portal mechanics", "Two-world contrast", "Identity transformation"
        ],
        "tone": "Wonder-filled, transformative, adventurous, personally challenging"
    }
}

def build_fantasy_prompt(style_data, selected_techniques=None, word_count=None, additional_elements=None, magic_level="moderate"):
    """Build a comprehensive fantasy system prompt from style data"""
    
    # Base prompt structure
    base_prompt = f"""You are an expert fantasy writer specializing in {style_data['description']}.

CORE FANTASY WRITING TECHNIQUES:
"""
    
    # Add techniques
    techniques = selected_techniques if selected_techniques else style_data['techniques']
    for i, technique in enumerate(techniques, 1):
        base_prompt += f"{i}. {technique}\n"
    
    base_prompt += f"\nFANTASY ELEMENTS TO INCLUDE:\n"
    
    # Add elements
    elements = style_data['elements']
    if additional_elements:
        elements.extend(additional_elements)
    
    elements_text = ", ".join(elements)
    base_prompt += f"{elements_text}\n"
    
    base_prompt += f"\nMAGIC AND WORLDBUILDING:\n"
    if magic_level == "high":
        base_prompt += "Magic should be prominent, powerful, and central to the scene.\n"
    elif magic_level == "low":
        base_prompt += "Magic should be subtle, rare, or have significant costs and limitations.\n"
    else:
        base_prompt += "Magic should be present but balanced with non-magical elements.\n"
    
    base_prompt += f"Create vivid, immersive fantasy settings with rich sensory details.\n"
    base_prompt += f"Develop authentic fantasy cultures with their own customs and beliefs.\n"
    
    base_prompt += f"\nTONE AND STYLE:\n"
    base_prompt += f"Maintain a {style_data['tone']} tone throughout the scene.\n"
    base_prompt += f"Balance fantasy wonder with believable character emotions and motivations.\n"
    
    if word_count:
        base_prompt += f"\nLENGTH REQUIREMENT:\n"
        base_prompt += f"Write approximately {word_count} words.\n"
    
    base_prompt += f"\nFOCUS:\n"
    base_prompt += f"Create immersive fantasy scenes that transport readers to magical worlds while maintaining emotional authenticity and engaging storytelling."
    
    return base_prompt
