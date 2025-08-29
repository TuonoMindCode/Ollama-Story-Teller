"""Menu handling methods for blueprint creation"""

from .config import *
import requests
from generators.narrative_style_examples import NARRATIVE_STYLE_EXAMPLES, show_all_style_examples

from .menu_handlers.basic_settings import BasicSettingsHandler
from .menu_handlers.story_elements import StoryElementsHandler
from .menu_handlers.character_settings import CharacterSettingsHandler
from .menu_handlers.technical_settings import TechnicalSettingsHandler


class MenuHandlers:
    def __init__(self, blueprint_creator):
        self.bc = blueprint_creator
        
        # Initialize sub-handlers
        self.basic = BasicSettingsHandler(blueprint_creator)
        self.story = StoryElementsHandler(blueprint_creator)
        self.character = CharacterSettingsHandler(blueprint_creator)
        self.technical = TechnicalSettingsHandler(blueprint_creator)
    
    # Delegate methods to appropriate handlers
    def set_blueprint_name(self, blueprint_data):
        return self.basic.set_blueprint_name(blueprint_data)
    
    def set_genre(self, blueprint_data):
        return self.basic.set_genre(blueprint_data)
    
    def set_subgenre(self, blueprint_data):
        return self.basic.set_subgenre(blueprint_data)
    
    def set_target_audience(self, blueprint_data):
        return self.basic.set_target_audience(blueprint_data)
    
    def set_storytelling_style(self, blueprint_data):
        return self.story.set_storytelling_style(blueprint_data)
    
    def set_perspective(self, blueprint_data):
        return self.story.set_perspective(blueprint_data)
    
    def set_narrative_style(self, blueprint_data):
        return self.story.set_narrative_style(blueprint_data)
    
    def set_language_style(self, blueprint_data):
        return self.story.set_language_style(blueprint_data)
    
    def set_setting_type(self, blueprint_data):
        return self.story.set_setting_type(blueprint_data)
    
    def set_tone(self, blueprint_data):
        return self.story.set_tone(blueprint_data)
    
    def set_complexity(self, blueprint_data):
        return self.story.set_complexity(blueprint_data)
    
    def set_special_elements(self, blueprint_data):
        return self.story.set_special_elements(blueprint_data)
    
    def set_custom_instructions(self, blueprint_data):
        return self.story.set_custom_instructions(blueprint_data)
    
    def set_protagonist_gender(self, blueprint_data):
        return self.character.set_protagonist_gender(blueprint_data)
    
    def set_counterpart_character(self, blueprint_data):
        return self.character.set_counterpart_character(blueprint_data)
    
    def set_counterpart_gender(self, blueprint_data):
        return self.character.set_counterpart_gender(blueprint_data)
    
    def set_llm_model(self, blueprint_data):
        return self.technical.set_llm_model(blueprint_data)
    
    def set_max_tokens(self, blueprint_data):
        return self.technical.set_max_tokens(blueprint_data)
    
    def set_target_length(self, blueprint_data):
        return self.technical.set_target_length(blueprint_data)


def _get_genre_specific_example(self, perspective, genre):
    """Get genre-specific examples for perspectives"""
    examples = {
        "Romance": {
            "First person singular": "I couldn't stop thinking about the way he looked at me across the coffee shop. Did he feel it too, this electric connection?",
            "Third person limited": "Emma's heart raced as David approached. She tried to appear casual, but her hands were trembling.",
            "Third person omniscient": "Neither Emma nor David realized they were both thinking the same thing: this could be the beginning of something beautiful.",
            "Third person multiple": "Emma's POV: 'He's gorgeous but probably taken.' David's POV: 'She seems out of my league, but maybe I should try.'"
        },
        "Mystery": {
            "First person singular": "I studied the crime scene photos again, knowing I was missing something crucial. The killer had left a clue, I was sure of it.",
            "Third person limited": "Detective Sarah Martinez stared at the evidence board, her instincts telling her the obvious suspect was too obvious.",
            "Third person omniscient": "While Sarah focused on the fingerprints, she didn't notice the real clue hidden in plain sight on the victim's desk.",
            "Third person multiple": "Detective's POV: 'The husband is lying.' Killer's POV: 'The detective is getting too close to the truth.'"
        },
        "Fantasy": {
            "First person singular": "I felt the magic surge through my veins as I raised my staff. The dragon's eyes locked onto mine, and I knew this was my moment.",
            "Third person limited": "Kira gripped her enchanted blade, feeling its power pulse in response to the approaching dark magic.",
            "Third person omniscient": "As Kira prepared for battle, the ancient spirits watched from the ethereal realm, knowing her destiny hung in the balance.",
            "Third person multiple": "Hero's POV: 'I must save the kingdom.' Villain's POV: 'Today, the old world ends and my reign begins.'"
        },
        "Horror": {
            "First person singular": "I could hear the scratching in the walls getting louder. Something was definitely living inside my house, and it wasn't human.",
            "Second person": "You hear the floorboard creak behind you. You turn slowly, your flashlight shaking in your grip, but see nothing there.",
            "Third person limited": "David felt the temperature drop as he entered the basement. Every instinct screamed at him to leave, but he pressed on.",
            "Third person omniscient": "David descended into the basement, unaware that the malevolent presence had been waiting decades for someone to disturb its rest."
        },
        "Science Fiction": {
            "First person singular": "I activated my neural implant and watched the data stream directly into my consciousness. The conspiracy was deeper than I'd imagined.",
            "Third person limited": "Captain Rivera studied the alien artifact, her scientific mind racing to understand its impossible geometry.",
            "Third person omniscient": "While the crew debated the artifact's origin, the AI quietly calculated that humanity had exactly 72 hours left.",
            "Third person multiple": "Human POV: 'This could revolutionize everything.' Alien POV: 'The primitive species has found our beacon.'"
        },
        "Thriller": {
            "First person singular": "I knew someone was watching me. Every shadow seemed to move, every sound made me jump. I had to get out of the city tonight.",
            "Third person limited": "Lisa checked her rearview mirror for the tenth time. The black sedan was still there, three cars back.",
            "Third person omniscient": "Lisa drove frantically through the city, unaware that her pursuer was actually trying to protect her from the real threat.",
            "Third person multiple": "Victim's POV: 'I'm being hunted.' Hunter's POV: 'She's making this too easy.' Protector's POV: 'I have to reach her first.'"
        }
    }

    genre_examples = examples.get(genre, {})
    return genre_examples.get(perspective, None)
