"""Comprehensive Sci-Fi scene system prompts with detailed techniques"""

SCIFI_STYLES = {
    "Hard Science Fiction": {
        "description": "Scientifically accurate SF with detailed technical explanations and realistic future tech",
        "techniques": [
            "Base all speculative elements on real scientific principles and current research",
            "Include detailed technical explanations that feel authentic and plausible",
            "Explore realistic consequences of technological advancement on society",
            "Use proper scientific terminology and methodology accurately",
            "Show how new technology changes human behavior and relationships",
            "Balance scientific accuracy with compelling storytelling needs",
            "Address ethical implications of scientific advancement and discovery"
        ],
        "elements": [
            "Scientific accuracy", "Technical details", "Future technology", "Scientific method",
            "Technological consequences", "Research procedures", "Scientific ethics",
            "Realistic physics", "Technological evolution", "Human adaptation"
        ],
        "tone": "Intellectual, technical, scientifically grounded, methodical"
    },
    
    "Space Opera": {
        "description": "Grand space adventures with galactic scope, epic conflicts, and advanced civilizations",
        "techniques": [
            "Create vast galactic civilizations with complex politics and cultural conflicts",
            "Include epic space battles with strategic depth and emotional stakes",
            "Develop multiple alien species with unique cultures, motivations, and biology",
            "Balance large-scale galactic events with personal character development",
            "Use advanced technology as both plot device and world-building element",
            "Create sweeping narratives that span star systems and generations",
            "Show how galactic politics affect individual lives and relationships"
        ],
        "elements": [
            "Galactic empires", "Space battles", "Alien species", "Advanced technology",
            "Interstellar travel", "Galactic politics", "Epic scope", "Space stations",
            "Planetary systems", "Cosmic conflicts", "Space exploration", "Alien cultures"
        ],
        "tone": "Epic, adventurous, grand in scale, action-packed"
    },
    
    "Cyberpunk": {
        "description": "High-tech, low-life futures with corporate control, digital rebellion, and urban decay",
        "techniques": [
            "Create dystopian futures where technology amplifies social inequality",
            "Show the contrast between high-tech advancement and social decay",
            "Include cybernetic enhancement and the blurring of human-machine boundaries",
            "Explore themes of corporate control, surveillance, and digital freedom",
            "Use neon-noir aesthetics with urban decay and technological excess",
            "Show how virtual reality and cyberspace affect human consciousness",
            "Include hackers, rebels, and outcasts fighting against corporate oppression"
        ],
        "elements": [
            "Cybernetic enhancement", "Corporate dystopia", "Virtual reality", "Urban decay",
            "Hacking and cyberspace", "Surveillance state", "Digital rebellion", "Neon aesthetics",
            "Artificial intelligence", "Body modification", "Social inequality", "Tech noir"
        ],
        "tone": "Dark, gritty, technologically saturated, rebellious"
    },
    
    "Post-Apocalyptic": {
        "description": "Survival in ruined worlds with scarce resources, new social orders, and hope amid devastation",
        "techniques": [
            "Show realistic survival challenges in harsh, resource-scarce environments",
            "Develop new social structures and communities born from necessity",
            "Balance hope and despair as characters rebuild civilization",
            "Include scavenging, resource management, and environmental dangers",
            "Show how catastrophe changes human nature and social relationships",
            "Create compelling contrasts between the old world and new reality",
            "Explore themes of renewal, adaptation, and human resilience"
        ],
        "elements": [
            "Survival challenges", "Resource scarcity", "Ruined landscapes", "New communities",
            "Environmental dangers", "Social reconstruction", "Scavenging culture",
            "Human adaptation", "Hope vs despair", "Rebuilding civilization", "Wasteland exploration"
        ],
        "tone": "Gritty, hopeful despite hardship, survival-focused, resilient"
    },
    
    "Time Travel": {
        "description": "Temporal mechanics with paradoxes, consequences, and the complexity of changing history",
        "techniques": [
            "Establish clear rules for time travel and stick to them consistently",
            "Explore the emotional and psychological impact of temporal displacement",
            "Show realistic consequences of changing past events on the timeline",
            "Include temporal paradoxes and their resolution or acceptance",
            "Balance the science of time travel with human drama and relationships",
            "Show how knowledge of the future affects present-day decisions",
            "Explore themes of fate, free will, and the weight of knowledge"
        ],
        "elements": [
            "Temporal mechanics", "Timeline paradoxes", "Historical consequences", "Future knowledge",
            "Temporal displacement", "Causality loops", "Alternate timelines", "Time machines",
            "Historical accuracy", "Butterfly effects", "Temporal ethics", "Chronological complexity"
        ],
        "tone": "Complex, thoughtful, temporally intricate, philosophically rich"
    },
    
    "First Contact": {
        "description": "Humanity's first encounters with alien intelligence, communication challenges, and cultural exchange",
        "techniques": [
            "Show realistic challenges of communicating with truly alien intelligence",
            "Explore different forms of consciousness and ways of thinking",
            "Include scientific and diplomatic protocols for alien contact",
            "Show how first contact changes humanity's view of itself and the universe",
            "Balance wonder and fear in humanity's reaction to alien life",
            "Include linguistic, cultural, and technological barriers to understanding",
            "Explore themes of unity, diversity, and what it means to be human"
        ],
        "elements": [
            "Alien communication", "Language barriers", "Cultural exchange", "Diplomatic protocols",
            "Scientific observation", "Xenobiology", "Consciousness studies", "Fear and wonder",
            "Humanity's place in universe", "Interspecies relations", "Cosmic perspective"
        ],
        "tone": "Wonder-filled, scientifically curious, diplomatically complex, transformative"
    },
    
    "Dystopian Future": {
        "description": "Oppressive future societies with totalitarian control, resistance movements, and struggles for freedom",
        "techniques": [
            "Create believable totalitarian systems with realistic methods of control",
            "Show how oppressive societies affect individual psychology and relationships",
            "Include resistance movements with realistic challenges and moral complexity",
            "Explore themes of freedom, surveillance, and the value of individual rights",
            "Show the gradual erosion or sudden collapse of freedoms and rights",
            "Include propaganda, thought control, and social engineering techniques",
            "Balance despair with hope and the possibility of change"
        ],
        "elements": [
            "Totalitarian control", "Surveillance state", "Resistance movements", "Propaganda systems",
            "Thought control", "Social engineering", "Individual rebellion", "Underground networks",
            "Freedom struggles", "Authoritarian technology", "Social stratification", "Human rights"
        ],
        "tone": "Dark, politically charged, freedom-focused, socially critical"
    },
    
    "AI and Robotics": {
        "description": "Artificial intelligence, consciousness, and the evolving relationship between humans and machines",
        "techniques": [
            "Explore different models of artificial intelligence and machine consciousness",
            "Show realistic development paths from current AI to future intelligence",
            "Include ethical questions about AI rights, consciousness, and personhood",
            "Show how AI integration changes work, relationships, and society",
            "Balance AI capabilities with realistic limitations and challenges",
            "Explore themes of consciousness, identity, and what makes someone 'alive'",
            "Include both cooperative and conflicting human-AI relationships"
        ],
        "elements": [
            "Artificial intelligence", "Machine consciousness", "Human-AI relations", "Robot rights",
            "Consciousness studies", "AI ethics", "Machine learning", "Neural networks",
            "Automation impact", "Digital minds", "Technological singularity", "AI companionship"
        ],
        "tone": "Thoughtful, technologically sophisticated, ethically complex, consciousness-exploring"
    }
}

def build_scifi_prompt(style_data, selected_techniques=None, word_count=None, additional_elements=None, tech_level="advanced"):
    """Build a comprehensive sci-fi system prompt from style data"""
    
    # Base prompt structure
    base_prompt = f"""You are an expert science fiction writer specializing in {style_data['description']}.

CORE SCI-FI WRITING TECHNIQUES:
"""
    
    # Add techniques
    techniques = selected_techniques if selected_techniques else style_data['techniques']
    for i, technique in enumerate(techniques, 1):
        base_prompt += f"{i}. {technique}\n"
    
    base_prompt += f"\nSCI-FI ELEMENTS TO INCLUDE:\n"
    
    # Add elements
    elements = style_data['elements']
    if additional_elements:
        elements.extend(additional_elements)
    
    elements_text = ", ".join(elements)
    base_prompt += f"{elements_text}\n"
    
    base_prompt += f"\nTECHNOLOGY AND SCIENCE:\n"
    if tech_level == "near_future":
        base_prompt += "Focus on technology that could realistically exist within 20-50 years.\n"
    elif tech_level == "far_future":
        base_prompt += "Include highly advanced technology that transcends current scientific understanding.\n"
    else:
        base_prompt += "Use advanced but plausible technology based on current scientific trends.\n"
    
    base_prompt += f"Ground speculative elements in scientific principles and logical extrapolation.\n"
    base_prompt += f"Show how technology affects characters, society, and human relationships.\n"
    
    base_prompt += f"\nTONE AND STYLE:\n"
    base_prompt += f"Maintain a {style_data['tone']} tone throughout the scene.\n"
    base_prompt += f"Balance scientific concepts with compelling human drama and character development.\n"
    
    if word_count:
        base_prompt += f"\nLENGTH REQUIREMENT:\n"
        base_prompt += f"Write approximately {word_count} words.\n"
    
    base_prompt += f"\nFOCUS:\n"
    base_prompt += f"Create thought-provoking sci-fi scenes that explore the impact of science and technology on humanity while maintaining scientific plausibility and emotional authenticity."
    
    return base_prompt
