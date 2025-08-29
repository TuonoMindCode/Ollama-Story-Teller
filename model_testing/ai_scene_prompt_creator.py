"""AI-powered comprehensive scene system prompt creator with guided options"""

import requests
import json

class AIScenePromptCreator:
    def __init__(self, template_manager):
        self.template_manager = template_manager
    
    def create_ai_generated_comprehensive_prompt(self):
        """Use AI to create comprehensive scene system prompts with guided options"""
        content_label = self.template_manager.content_type.capitalize()
        total_questions = 7
        
        print(f"\n{'='*70}")
        print(f"AI-GENERATED COMPREHENSIVE {content_label.upper()} SYSTEM PROMPT")
        print(f"{'='*70}")
        print("Let AI create a professional system prompt based on your specific requirements.")
        print(f"You'll answer {total_questions} questions to customize your prompt.")
        print()
        
        # Question 1: Genre Selection
        print(f"📋 QUESTION 1/{total_questions}: PRIMARY GENRE")
        print("="*50)
        genres = [
            ("Romance", "Love stories, relationships, emotional connections"),
            ("Fantasy", "Magic, mythical creatures, otherworldly settings"),
            ("Detective/Mystery", "Crime solving, investigation, logical deduction"),
            ("Sci-Fi", "Future technology, space, scientific advancement"),
            ("Horror", "Fear, suspense, supernatural or psychological terror"),
            ("Thriller", "Suspense, danger, high-stakes situations"),
            ("Drama", "Emotional conflicts, character development, realistic situations"),
            ("Adventure", "Action, exploration, heroic journeys"),
            ("Historical", "Past time periods with accurate historical details"),
            ("Contemporary", "Modern settings and current social issues"),
            ("Custom", "Specify your own genre or combination")
        ]
        
        for i, (genre, description) in enumerate(genres, 1):
            print(f"{i:2d}. {genre:<15} - {description}")
        
        try:
            genre_choice = int(input(f"\nSelect primary genre (1-{len(genres)}): "))
            if not (1 <= genre_choice <= len(genres)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
            
            selected_genre = genres[genre_choice - 1][0]
            if selected_genre == "Custom":
                custom_genre = input("Enter your genre or genre combination: ").strip()
                selected_genre = custom_genre if custom_genre else "General Fiction"
                
        except ValueError:
            print("❌ Invalid input.")
            input("Press Enter to continue...")
            return
        
        # Question 2: Tone/Mood
        print(f"\n📋 QUESTION 2/{total_questions}: TONE/MOOD")
        print("="*50)
        print("What tone/mood should the scenes have?")
        
        tone_options = [
            "Dark and gritty",
            "Light and humorous", 
            "Intense and dramatic",
            "Melancholic and reflective",
            "Upbeat and optimistic",
            "Mysterious and atmospheric",
            "Emotional and heartfelt",
            "Suspenseful and tense",
            "Whimsical and playful",
            "Serious and thoughtful",
            "Custom tone"
        ]
        
        for i, tone in enumerate(tone_options, 1):
            print(f"{i:2d}. {tone}")
        
        try:
            tone_choice = int(input(f"\nSelect tone/mood (1-{len(tone_options)}): "))
            if 1 <= tone_choice <= len(tone_options):
                selected_tone = tone_options[tone_choice - 1]
                if selected_tone == "Custom tone":
                    custom_tone = input("Describe your desired tone/mood: ").strip()
                    selected_tone = custom_tone if custom_tone else "Balanced and engaging"
            else:
                selected_tone = "Balanced and engaging"
        except ValueError:
            selected_tone = "Balanced and engaging"
        
        # Question 3: Target Audience
        print(f"\n📋 QUESTION 3/{total_questions}: TARGET AUDIENCE")
        print("="*50)
        audiences = ["Young Adult (13-17)", "Adult (18+)", "General Audience", "Mature Adult (25+)"]
        for i, audience in enumerate(audiences, 1):
            print(f"{i}. {audience}")
        
        try:
            aud_choice = int(input(f"\nSelect audience (1-{len(audiences)}): "))
            target_audience = audiences[aud_choice - 1] if 1 <= aud_choice <= len(audiences) else "General Audience"
        except ValueError:
            target_audience = "General Audience"
        
        # Question 4: Specific Techniques
        print(f"\n QUESTION 4/{total_questions}: WRITING TECHNIQUES TO EMPHASIZE")
        print("="*50)
        print("What specific writing techniques should be emphasized?")
        
        technique_options = [
            "Detailed character psychology",
            "Fast-paced action sequences",
            "Atmospheric description",
            "Realistic dialogue",
            "Plot twists and surprises",
            "Emotional depth and complexity",
            "World-building and setting",
            "Internal monologue and thoughts",
            "Sensory details and imagery",
            "Tension and conflict building",
            "Multiple techniques",
            "Custom techniques"
        ]
        
        for i, technique in enumerate(technique_options, 1):
            print(f"{i:2d}. {technique}")
        
        try:
            tech_choice = int(input(f"\nSelect primary technique emphasis (1-{len(technique_options)}): "))
            if 1 <= tech_choice <= len(technique_options):
                if tech_choice == len(technique_options) - 1:  # Multiple techniques
                    print("Enter numbers separated by commas (e.g., 1,3,5):")
                    multi_choice = input("Techniques: ").strip()
                    try:
                        indices = [int(x.strip()) - 1 for x in multi_choice.split(',')]
                        selected_techniques = [technique_options[i] for i in indices if 0 <= i < len(technique_options) - 2]
                    except:
                        selected_techniques = ["Balanced writing approach"]
                elif tech_choice == len(technique_options):  # Custom
                    custom_tech = input("Describe your desired techniques: ").strip()
                    selected_techniques = [custom_tech] if custom_tech else ["Professional writing techniques"]
                else:
                    selected_techniques = [technique_options[tech_choice - 1]]
            else:
                selected_techniques = ["Professional writing techniques"]
        except ValueError:
            selected_techniques = ["Professional writing techniques"]
        
        # Question 5: Writing Style Preferences
        print(f"\n📋 QUESTION 5/{total_questions}: WRITING STYLE PREFERENCES")
        print("="*50)
        print("What narrative style should be used?")
        
        style_options = [
            "Show don't tell approach",
            "First person POV",
            "Third person limited POV", 
            "Third person omniscient POV",
            "Present tense narration",
            "Past tense narration",
            "Stream of consciousness",
            "Minimalist style",
            "Descriptive and detailed style",
            "Dialogue-heavy scenes",
            "Action-focused writing",
            "Custom style preferences"
        ]
        
        for i, style in enumerate(style_options, 1):
            print(f"{i:2d}. {style}")
        
        try:
            style_choice = int(input(f"\nSelect writing style (1-{len(style_options)}): "))
            if 1 <= style_choice <= len(style_options):
                if style_choice == len(style_options):  # Custom
                    custom_style = input("Describe your style preferences: ").strip()
                    selected_style = custom_style if custom_style else "Professional, engaging style"
                else:
                    selected_style = style_options[style_choice - 1]
            else:
                selected_style = "Professional, engaging style"
        except ValueError:
            selected_style = "Professional, engaging style"
        
        # Question 6: Length and Structure
        print(f"\n QUESTION 6/{total_questions}: SCENE LENGTH PREFERENCE")
        print("="*50)
        
        length_options = [
            ("Short scenes (200-500 words)", 350),
            ("Medium scenes (500-1000 words)", 750),
            ("Long scenes (1000-2000 words)", 1500),
            ("Very long scenes (2000+ words)", 2500),
            ("Flexible length based on content", None),
            ("Custom word count", "custom")
        ]
        
        for i, (description, _) in enumerate(length_options, 1):
            print(f"{i}. {description}")
        
        try:
            length_choice = int(input(f"\nSelect scene length preference (1-{len(length_options)}): "))
            if 1 <= length_choice <= len(length_options):
                if length_options[length_choice - 1][1] == "custom":
                    custom_length = input("Enter target word count: ").strip()
                    word_count = int(custom_length) if custom_length.isdigit() else None
                    length_description = f"Approximately {word_count} words" if word_count else "Flexible length"
                else:
                    word_count = length_options[length_choice - 1][1]
                    length_description = length_options[length_choice - 1][0]
            else:
                word_count = None
                length_description = "Flexible length based on content"
        except ValueError:
            word_count = None
            length_description = "Flexible length based on content"
        
        # Question 7: Special Requirements
        print(f"\n📋 QUESTION 7/{total_questions}: SPECIAL REQUIREMENTS (OPTIONAL)")
        print("="*50)
        print("Any special requirements or constraints?")
        
        special_options = [
            "No special requirements",
            "Must be family-friendly content",
            "Include diversity and representation",
            "Focus on mental health themes sensitively",
            "Avoid graphic violence or content",
            "Include educational elements",
            "Focus on character relationships",
            "Emphasize cultural authenticity",
            "Include accessibility considerations",
            "Custom requirements"
        ]
        
        for i, special in enumerate(special_options, 1):
            print(f"{i:2d}. {special}")
        
        try:
            special_choice = int(input(f"\nSelect special requirements (1-{len(special_options)}): "))
            if 1 <= special_choice <= len(special_options):
                if special_choice == len(special_options):  # Custom
                    custom_special = input("Describe your special requirements: ").strip()
                    special_req = custom_special if custom_special else ""
                elif special_choice == 1:  # No requirements
                    special_req = ""
                else:
                    special_req = special_options[special_choice - 1]
            else:
                special_req = ""
        except ValueError:
            special_req = ""
        
        # Summary and Generation
        print(f"\n🎯 SUMMARY OF YOUR REQUIREMENTS:")
        print("="*50)
        print(f"📚 Genre: {selected_genre}")
        print(f"🎭 Tone: {selected_tone}")
        print(f"👥 Audience: {target_audience}")
        print(f"⚡ Techniques: {', '.join(selected_techniques)}")
        print(f"✍️  Style: {selected_style}")
        print(f"📏 Length: {length_description}")
        if special_req:
            print(f"⭐ Special: {special_req}")
        
        proceed = input(f"\nProceed with AI generation? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Generation cancelled.")
            input("Press Enter to continue...")
            return
        
        print(f"\n🤖 GENERATING COMPREHENSIVE SYSTEM PROMPT...")
        print("This may take a few moments...")
        
        # Call AI to generate the system prompt
        generated_prompt = self._call_ai_for_system_prompt(
            selected_genre, selected_tone, target_audience, selected_techniques, 
            selected_style, word_count, special_req, content_label
        )
        
        if generated_prompt:
            print(f"\n📋 AI-GENERATED {content_label.upper()} SYSTEM PROMPT:")
            print("=" * 70)
            print(generated_prompt)
            print("=" * 70)
            print(f"Word count: {len(generated_prompt.split())} words")
            
            # Save option
            save_choice = input(f"\nSave this AI-generated system prompt? (y/n): ").strip().lower()
            if save_choice == 'y':
                # Create descriptive filename
                safe_genre = selected_genre.replace(" ", "_").replace("/", "_").lower()
                safe_tone = selected_tone.replace(" ", "_").lower()[:15]  # Truncate long tones
                template_name = f"ai_{safe_genre}_{safe_tone}"
                
                if self.template_manager.save_system_prompt_template(template_name, generated_prompt):
                    print(f"\n✅ AI-generated system prompt saved!")
                    print(f"📁 Filename: system_prompt_{self.template_manager.content_type}_{template_name}.txt")
                    print(f"🎯 Genre: {selected_genre}")
                    print(f"🎭 Tone: {selected_tone}")
                    print(f"🤖 Generated by: AI based on your {total_questions}-question specification")
            else:
                print("Prompt not saved.")
        else:
            print("❌ Failed to generate system prompt.")
        
        input("\nPress Enter to continue...")
    
    def _call_ai_for_system_prompt(self, genre, tone, audience, techniques, style, word_count, special_req, content_type):
        """Call Ollama AI to generate the system prompt using the configured model"""
        
        # Get the configured model from ModelTester
        if not hasattr(self.template_manager, 'model_tester') or not self.template_manager.model_tester:
            print("❌ No model tester available.")
            return None
        
        # Get the configured model from test_config
        configured_model = self.template_manager.model_tester.test_config.get('model')
        if not configured_model:
            print("❌ No model configured in testing settings.")
            print("Please configure a model first in Testing Configuration (option 6).")
            return None
        
        print(f"🤖 Using configured model: {configured_model}")
        
        # Create comprehensive AI instruction
        ai_system_prompt = f"""You are an expert writing instructor and system prompt engineer who creates comprehensive system prompts for AI creative writers. 

Your system prompts should be professional, detailed, and actionable. They should tell an AI writer exactly HOW to write in a specific style and genre, covering:
- Writing philosophy and approach for the genre
- Narrative techniques and methods  
- Character development strategies
- Dialogue and voice guidelines
- Pacing and structure principles
- Language and tone direction
- Genre-specific conventions and techniques

Create system prompts that are 200-400 words long and give clear, specific direction."""
        
        # Build the user prompt with all requirements
        techniques_text = ', '.join(techniques) if isinstance(techniques, list) else str(techniques)
        
        ai_user_prompt = f"""Create a comprehensive system prompt for an AI that will write {genre} {content_type.lower()}s with these specifications:

GENRE: {genre}
TONE/MOOD: {tone}
TARGET AUDIENCE: {audience}
CONTENT TYPE: {content_type}s (focused scenes/moments)

TECHNIQUES TO EMPHASIZE: {techniques_text}

WRITING STYLE: {style}

{'LENGTH GUIDANCE: Target approximately ' + str(word_count) + ' words per scene' if word_count else 'LENGTH: Flexible based on scene needs'}

{f'SPECIAL REQUIREMENTS: {special_req}' if special_req else ''}

The system prompt should:
- Start with "You are an expert {genre.lower()} writer who specializes in..."
- Be comprehensive but concise (200-400 words)  
- Focus specifically on writing {content_type.lower()}s in the {genre} genre
- Include specific techniques for {tone} tone
- Be appropriate for {audience} readers
- Give actionable writing guidance
- Cover the key elements that make great {genre} {content_type.lower()}s
- Include the specified techniques and style preferences

Return ONLY the system prompt, no additional commentary."""
        
        try:
            # Use the ModelTester's configuration for the API call
            import requests
            import json
            
            # Get full configuration from ModelTester
            test_config = self.template_manager.model_tester.test_config
            
            url = "http://localhost:11434/api/generate"
            
            data = {
                "model": configured_model,
                "prompt": f"System: {ai_system_prompt}\n\nUser: {ai_user_prompt}\n\nAssistant:",
                "stream": False,
                "options": {
                    "num_predict": test_config.get('max_tokens', 1024),
                    "temperature": test_config.get('temperature', 0.3),
                    "top_p": test_config.get('top_p', 0.9),
                    "top_k": test_config.get('top_k', 40)
                }
            }
            
            print("🔄 Connecting to Ollama...")
            timeout = test_config.get('timeout_seconds', 120)
            if timeout == 0:  # Unlimited timeout
                timeout = None
            
            response = requests.post(url, json=data, timeout=timeout)
            response.raise_for_status()
            result = response.json()
            
            generated_text = result.get("response", "").strip()
            if generated_text:
                print("✅ System prompt generated successfully!")
                return generated_text
            else:
                print("❌ Empty response from AI")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Ollama. Is Ollama running on http://localhost:11434?")
            return None
        except requests.exceptions.Timeout:
            print("❌ Request timed out. The model may be taking too long to respond.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to Ollama: {e}")
            return None
        except json.JSONDecodeError:
            print("❌ Invalid response format from Ollama")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
