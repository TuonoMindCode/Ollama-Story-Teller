class AgeSpecificOptions:
    """Age-specific writing options for different audiences"""
    
    @staticmethod
    def get_options(age_group: str) -> dict:
        """Get age-specific writing options"""
        
        options = {
            'Middle Grade': {
                'techniques': [
                    ("Simple Internal Thoughts", "Age-appropriate internal monologue focusing on immediate feelings and simple motivations"),
                    ("Action-Adventure Focus", "Fast-paced scenes with clear cause-and-effect, emphasizing physical adventure"),
                    ("Friendship Dynamics", "Character relationships through dialogue and shared activities"),
                    ("Problem-Solving Journey", "Characters working through challenges with clear steps and growth"),
                    ("Sensory Discovery", "Rich descriptions that help young readers experience the world through senses")
                ],
                'perspectives': [
                    ("Third Person Limited", "Close to one character but maintains some distance, perfect for MG readers"),
                    ("First Person Present", "Immediate and engaging 'I am doing' style that draws young readers in"),
                    ("Third Person Multiple", "Switching between 2-3 main characters with clear chapter/section breaks"),
                    ("Omniscient Narrator", "Friendly, knowledgeable voice that can explain things young readers might not know")
                ],
                'styles': [
                    ("Clear and Direct", "Simple sentence structure with vivid, concrete language"),
                    ("Playful and Energetic", "Fun word choices, humor, and dynamic pacing that keeps young readers engaged"),
                    ("Warm and Encouraging", "Positive tone that builds confidence while addressing real challenges"),
                    ("Adventure-Driven", "Action-oriented with clear stakes and exciting moments"),
                    ("Gentle Emotional", "Handles feelings with care, teaching emotional literacy without overwhelming")
                ]
            },
            
            'Young Adult': {
                'techniques': [
                    ("Deep Internal Voice", "Rich internal monologue exploring identity, belonging, and complex emotions"),
                    ("Authentic Dialogue", "Realistic teen speech patterns with subtext about relationships and social dynamics"),
                    ("Coming-of-Age Moments", "Pivotal scenes that show character growth and self-discovery"),
                    ("Emotional Intensity", "High-stakes emotions appropriate for teens discovering who they are"),
                    ("Social Dynamics", "Complex peer relationships, family tensions, and romantic developments")
                ],
                'perspectives': [
                    ("First Person Present", "Immediate, intimate 'I am feeling' style that connects with teen readers"),
                    ("Dual POV", "Alternating between two main characters, often in romantic or friendship stories"),
                    ("Third Person Deep", "Close third person that feels almost first person in emotional intimacy"),
                    ("Multiple POV", "3-4 perspectives showing different sides of teen social situations")
                ],
                'styles': [
                    ("Emotionally Raw", "Honest, sometimes intense emotional expression that validates teen experiences"),
                    ("Contemporary Voice", "Current language and references that feel authentic to teen readers"),
                    ("Romantic Tension", "Building chemistry and emotional connection appropriate for teen relationships"),
                    ("Identity Exploration", "Questioning, searching tone that mirrors teen self-discovery"),
                    ("Dramatic Intensity", "Higher emotional stakes with passionate, sometimes angsty expression")
                ]
            },
            
            'Adult': {
                'techniques': [
                    ("Psychological Depth", "Complex internal landscapes exploring mature themes and motivations"),
                    ("Layered Characterization", "Multi-dimensional characters with contradictions and hidden depths"),
                    ("Sophisticated Conflict", "Internal and external conflicts with moral ambiguity"),
                    ("Relationship Complexity", "Mature romantic, family, and professional relationship dynamics"),
                    ("Life Experience Integration", "Drawing on accumulated wisdom and experience in storytelling")
                ],
                'perspectives': [
                    ("Third Person Limited", "Intimate access to one character's complex inner world"),
                    ("Multiple POV", "Several characters' perspectives creating a rich, layered narrative"),
                    ("Omniscient Narrator", "Sophisticated narrative voice with broad perspective on human nature"),
                    ("First Person Mature", "Reflective, experienced voice sharing hard-won insights")
                ],
                'styles': [
                    ("Emotionally Nuanced", "Subtle, complex emotional expression with sophisticated understanding"),
                    ("Literary Contemporary", "Beautiful prose that serves story without overwhelming it"),
                    ("Psychologically Realistic", "Authentic human behavior and motivation in complex situations"),
                    ("Relationship-Rich", "Deep exploration of how people connect and disconnect over time"),
                    ("Thematically Layered", "Multiple themes woven naturally through compelling storytelling")
                ]
            },
            
            'General Audience': {
                'techniques': [
                    ("Universal Themes", "Stories that resonate across different backgrounds and experiences"),
                    ("Accessible Complexity", "Sophisticated ideas presented in engaging, understandable ways"),
                    ("Emotional Connection", "Stories that create genuine feeling and empathy in diverse readers"),
                    ("Clear Storytelling", "Well-crafted narratives that serve story above stylistic flourishes"),
                    ("Character-Driven Plot", "Compelling people facing relatable challenges and growth")
                ],
                'perspectives': [
                    ("Third Person Accessible", "Close character connection without overwhelming intimacy"),
                    ("First Person Relatable", "Personal voice that many different readers can connect with"),
                    ("Multiple POV Balanced", "Different perspectives that enhance rather than complicate story"),
                    ("Omniscient Gentle", "Wise narrative voice that guides without overwhelming")
                ],
                'styles': [
                    ("Engaging Clarity", "Clear, beautiful prose that serves story and reaches broad audiences"),
                    ("Emotionally Honest", "Authentic feeling without pretension or excessive complexity"),
                    ("Accessible Literary", "Quality writing that doesn't require specialized knowledge to appreciate"),
                    ("Universal Voice", "Storytelling that transcends demographic boundaries"),
                    ("Balanced Approach", "Neither too simple nor too complex, hitting the sweet spot for general readers")
                ]
            }
        }
        
        return options.get(age_group, options['General Audience'])
