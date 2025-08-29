"""Configuration and constants for blueprint creation"""

import requests
import json

GENRES = [
    "Detective/Mystery", "Horror", "Science Fiction", "Fantasy", 
    "Thriller", "Romance", "Drama", "Adventure", "Western", 
    "Historical Fiction", "Comedy", "Literary Fiction"
]

SUBGENRES = {
    "Detective/Mystery": ["Cozy Mystery", "Police Procedural", "Noir", "Hardboiled", "Amateur Sleuth"],
    "Horror": ["Gothic", "Psychological Horror", "Supernatural", "Slasher", "Cosmic Horror"],
    "Science Fiction": ["Space Opera", "Cyberpunk", "Dystopian", "Time Travel", "Hard Sci-Fi"],
    "Fantasy": ["High Fantasy", "Urban Fantasy", "Dark Fantasy", "Epic Fantasy", "Magical Realism"],
    "Thriller": ["Psychological Thriller", "Action Thriller", "Espionage", "Legal Thriller", "Medical Thriller"],
    "Romance": ["Historical Romance", "Contemporary Romance", "Paranormal Romance", "Romantic Suspense"],
    "Drama": ["Family Drama", "Coming of Age", "Historical Drama", "Social Drama"],
    "Adventure": ["Action Adventure", "Survival", "Quest", "Exploration"],
    "Western": ["Traditional Western", "Space Western", "Weird Western"],
    "Historical Fiction": ["Medieval", "Victorian", "World War Era", "Ancient Times"]
}

STORYTELLING_STYLES = [
    "Monologue-driven", "Dialogue-heavy", "Action-oriented", 
    "Descriptive/Atmospheric", "Minimalist", "Stream of consciousness",
    "Epistolary", "Multiple timelines", "Unreliable narrator", "Documentary style"
]

PERSPECTIVES = [
    "First person singular", "First person plural", "Second person",
    "Third person limited", "Third person omniscient", "Third person multiple", "Mixed perspectives"
]

NARRATIVE_STYLES = [
    "Descriptive Literary",
    "Fast-paced Action", 
    "Romantic Intimate First Person",
    "Mysterious Atmospheric",
    "Conversational Casual",
    "Dramatic Emotional",
    "Humorous Light-hearted",
    "Philosophical Contemplative"
]

SETTING_TYPES = [
    "Urban", "Small town", "Isolated location", "Institution",
    "Historical period", "Futuristic", "Fantasy realm", "Multiple locations",
    "Confined space", "Natural environment"
]

TONES = [
    "Dark and gritty", "Light and humorous", "Suspenseful", "Melancholic",
    "Optimistic", "Cynical", "Romantic", "Cerebral", "Visceral", "Whimsical"
]

COMPLEXITIES = ["Simple", "Moderate", "Complex", "Highly complex"]

SPECIAL_ELEMENTS = [
    "Red herrings", "Unreliable witnesses", "Locked room mystery", "Multiple suspects",
    "Time pressure", "Romantic subplot", "Family secrets", "Corporate intrigue",
    "Historical elements", "Supernatural hints", "Technology focus", "Social commentary"
]

LENGTH_OPTIONS = {
    1: ("Short (8-12 scenes)", "Quick stories, 15,000-25,000 words"),
    2: ("Medium (12-15 scenes)", "Standard stories, 25,000-40,000 words"),
    3: ("Long (15-20 scenes)", "Extended stories, 40,000-60,000 words"),
    4: ("Epic (20-25 scenes)", "Book-length stories, 60,000-80,000+ words"),
    5: ("Custom", "Specify your own scene count and word target")
}

TOKEN_OPTIONS = {
    "1": 4096,
    "2": 8192,
    "3": 16384,
    "4": 32768,
    "5": 65536,
    "6": 131072
}

GENDERS = ["Male", "Female", "Non-binary", "Not specified"]

PROTAGONIST_COUNTERPARTS = {
    "Detective/Mystery": ["Criminal/Perpetrator", "Victim", "Partner/Colleague", "Love Interest"],
    "Romance": ["Love Interest", "Romantic Rival", "Ex-partner", "Best Friend"],
    "Thriller": ["Antagonist/Villain", "Accomplice", "Victim", "Ally"],
    "Horror": ["Monster/Entity", "Cult Leader", "Possessed Person", "Survivor"],
    "Science Fiction": ["Alien/AI", "Corporate Antagonist", "Rebel Leader", "Scientist"],
    "Fantasy": ["Dark Lord/Sorcerer", "Dragon/Beast", "Rival Mage", "Princess/Prince"],
    "Drama": ["Family Member", "Rival", "Mentor", "Love Interest"],
    "Adventure": ["Villain", "Rival Explorer", "Guide", "Love Interest"],
    "Western": ["Outlaw", "Sheriff", "Rancher", "Saloon Owner"],
    "Historical Fiction": ["Historical Figure", "War Enemy", "Political Rival", "Love Interest"],
    "Comedy": ["Straight Man", "Rival", "Love Interest", "Sidekick"],
    "Literary Fiction": ["Foil Character", "Family Member", "Mentor", "Love Interest"]
}

def get_time_estimate(max_tokens):
    """Get time estimate for blueprint generation based on token count"""
    if max_tokens <= 8192:
        return "1-3 minutes"
    elif max_tokens <= 16384:
        return "3-6 minutes"
    elif max_tokens <= 32768:
        return "6-12 minutes"
    elif max_tokens <= 65536:
        return "12-20 minutes"
    else:
        return "20+ minutes"

def get_model_description(model):
    """Get description for common models"""
    model_lower = model.lower()
    if "llama2" in model_lower:
        return " (Balanced, reliable)"
    elif "dolphin" in model_lower:
        return " (Creative, uncensored)"
    elif "mistral" in model_lower:
        return " (Fast, efficient)"
    elif "codellama" in model_lower:
        return " (Code-focused)"
    elif "vicuna" in model_lower:
        return " (Conversational)"
    return ""

def get_available_ollama_models():
    """Get list of locally installed Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            models = []
            for model in data.get('models', []):
                model_name = model.get('name', '')
                if model_name:
                    models.append(model_name)
            return sorted(models) if models else get_default_models()
        else:
            print("⚠️ Could not connect to Ollama API, using default model list")
            return get_default_models()
    except Exception as e:
        print(f"⚠️ Error fetching Ollama models: {e}")
        print("Using default model list")
        return get_default_models()

def get_default_models():
    """Fallback model list if Ollama API is not available"""
    return ["llama2", "dolphin3:latest", "mistral", "codellama", "vicuna"]

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False
