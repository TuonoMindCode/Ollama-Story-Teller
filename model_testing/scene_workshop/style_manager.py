class StyleManager:
    def __init__(self, workshop):
        self.workshop = workshop
        
        # Narrative styles
        self.narrative_styles = {
            'first_inner': {
                'name': 'First Person - Inner Thoughts',
                'addition': 'Write in first person focusing on internal thoughts.',
                'desc': 'I thought... I felt... (introspective)'
            },
            'second_romance': {
                'name': 'Second Person Romance',
                'addition': 'Write in second person romantic style.',
                'desc': 'You walked in... I saw you... (intimate)'
            },
            'third_limited': {
                'name': 'Third Person Limited',
                'addition': 'Write in third person limited.',
                'desc': 'She noticed... He thought... (single focus)'
            },
            'stream': {
                'name': 'Stream of Consciousness',
                'addition': 'Write in stream of consciousness.',
                'desc': 'Thoughts flowing... memories mixing...'
            }
        }
        
        # Writing styles
        self.writing_styles = {
            'literary': {
                'name': 'Literary Fiction',
                'addition': 'Use rich prose with metaphors.',
                'desc': 'Rich prose, metaphors, deep meaning'
            },
            'minimalist': {
                'name': 'Minimalist',
                'addition': 'Write in simple, direct language.',
                'desc': 'Simple, direct, understated'
            },
            'dialogue': {
                'name': 'Dialogue-Heavy',
                'addition': 'Focus on dialogue.',
                'desc': 'Conversation-focused'
            },
            'descriptive': {
                'name': 'Descriptive',
                'addition': 'Use rich sensory details.',
                'desc': 'Rich sensory details, atmosphere'
            }
        }
    
    def select_narrative_style(self):
        """Select narrative style reinforcement for user prompt"""
        print("\nSELECT NARRATIVE STYLE REINFORCEMENT")
        print("="*50)
        print("This adds perspective guidance to your USER PROMPT to reinforce")
        print("the narrative style that should already be in your system prompt.")
        print()
        
        styles = list(self.narrative_styles.items())
        for i, (key, style) in enumerate(styles, 1):
            print(f"{i}. {style['name']}")
            print(f"   Adds to user prompt: {style['desc']}")
        
        try:
            choice = int(input(f"\nSelect reinforcement (1-{len(styles)}): "))
            if 1 <= choice <= len(styles):
                key, style = styles[choice - 1]
                self.workshop.current_settings['narrative_style'] = key
                self.workshop.current_settings['narrative_style_name'] = style['name']
                print(f"Will add narrative reinforcement to user prompt: {style['name']}")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
    
    def select_writing_style(self):
        """Select writing style reinforcement for user prompt"""
        print("\nSELECT WRITING STYLE REINFORCEMENT")
        print("="*45)
        print("This adds style guidance to your USER PROMPT to reinforce")
        print("the writing style that should already be in your system prompt.")
        print()
        
        styles = list(self.writing_styles.items())
        for i, (key, style) in enumerate(styles, 1):
            print(f"{i}. {style['name']}")
            print(f"   Adds to user prompt: {style['desc']}")
        
        try:
            choice = int(input(f"\nSelect reinforcement (1-{len(styles)}): "))
            if 1 <= choice <= len(styles):
                key, style = styles[choice - 1]
                self.workshop.current_settings['writing_style'] = key
                self.workshop.current_settings['writing_style_name'] = style['name']
                print(f"Will add writing reinforcement to user prompt: {style['name']}")
        except ValueError:
            print("Invalid input")
        
        input("Press Enter to continue...")
