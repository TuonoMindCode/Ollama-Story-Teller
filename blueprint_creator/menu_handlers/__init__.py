"""Menu handlers package for blueprint creation"""
from .basic_settings import BasicSettingsHandler
from .story_elements import StoryElementsHandler
from .character_settings import CharacterSettingsHandler
from .technical_settings import TechnicalSettingsHandler

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
