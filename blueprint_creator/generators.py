"""Blueprint generation logic using Ollama"""

import requests
from .config import get_time_estimate, check_ollama_connection

class BlueprintGenerator:
    def __init__(self):
        pass
    
    def generate_blueprint_with_ollama(self, blueprint_data):
        """Generate blueprint content using Ollama"""
        print("\n" + "="*60)
        print("GENERATING BLUEPRINT WITH OLLAMA")
        print("="*60)
        print(f"Using model: {blueprint_data['llm_model']}")
        
        # Check Ollama connection before generating
        if not check_ollama_connection():
            print("❌ Cannot connect to Ollama!")
            print("Please make sure Ollama is running with: ollama serve")
            return "Error: Ollama service not available"
        
        # Show generation settings info
        print(f"Max tokens: {blueprint_data['max_tokens']:,}")
        print(f"Complexity level: {blueprint_data.get('complexity', 'Not chosen')}")
        
        time_estimate = get_time_estimate(blueprint_data['max_tokens'])
        print(f"Estimated time: {time_estimate}")
        
        # Add warning for very high token counts
        if blueprint_data['max_tokens'] >= 65536:
            print("⚠️  This is a very detailed blueprint - generation may take significant time!")
            confirm = input("Continue? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Blueprint generation cancelled")
                return None
        
        # Create the prompt for Ollama
        prompt = self.create_blueprint_prompt(blueprint_data)
        
        print("\nSending request to Ollama...")
        print("This may take several minutes for detailed blueprints...")
        print("Please be patient - larger blueprints take more time to generate.\n")
        
        # Generate blueprint content
        blueprint_content = self.call_ollama_for_blueprint(prompt, blueprint_data['llm_model'], blueprint_data)
        
        if blueprint_content.startswith("Error:"):
            print(f"❌ Failed to generate blueprint: {blueprint_content}")
            input("Press Enter to continue...")
            return None
        
        # Show generation stats
        word_count = len(blueprint_content.split())
        char_count = len(blueprint_content)
        print(f"\n✅ Blueprint generated successfully!")
        print(f"   Words: {word_count:,}")
        print(f"   Characters: {char_count:,}")
        print(f"   Tokens used: ~{blueprint_data['max_tokens']:,}")
        
        # Display the generated blueprint
        print("\n" + "="*60)
        print("GENERATED BLUEPRINT")
        print("="*60)
        print(blueprint_content)
        print("="*60)
        
        return blueprint_content

    def create_blueprint_prompt(self, blueprint_data):
        """Create the prompt for Ollama to generate the blueprint"""
        prompt_parts = []
    
        prompt_parts.append("You are an expert story development consultant and blueprint creator. Create a comprehensive, detailed story blueprint that will guide writers to create LONG, DETAILED stories with extensive scenes.")
        prompt_parts.append("")
        prompt_parts.append("BLUEPRINT SPECIFICATIONS:")

        # Required fields
        prompt_parts.append(f"GENRE: {blueprint_data['genre']}")
        if blueprint_data['subgenre'] != 'Not chosen':
            prompt_parts.append(f"SUBGENRE: {blueprint_data['subgenre']}")
        
        if blueprint_data['target_length'] != 'Long (15-20 scenes)':
            prompt_parts.append(f"TARGET STORY LENGTH: {blueprint_data['target_length']}")

        prompt_parts.append("")
        prompt_parts.append("WRITER PREFERENCES (incorporate these if specified, otherwise choose genre-appropriate defaults):")

        # Optional fields with more context
        if blueprint_data['storytelling_style'] != 'Not chosen':
            prompt_parts.append(f"- Storytelling style: {blueprint_data['storytelling_style']}")

        if blueprint_data['perspective'] != 'Not chosen':
            prompt_parts.append(f"- Narrative perspective: {blueprint_data['perspective']}")

        if blueprint_data['setting_type'] != 'Not chosen':
            prompt_parts.append(f"- Setting type: {blueprint_data['setting_type']}")

        if blueprint_data['tone'] != 'Not chosen':
            prompt_parts.append(f"- Story tone: {blueprint_data['tone']}")

        if blueprint_data['complexity'] != 'Not chosen':
            prompt_parts.append(f"- Complexity level: {blueprint_data['complexity']}")

        if blueprint_data['special_elements']:
            prompt_parts.append(f"- Special elements to include: {', '.join(blueprint_data['special_elements'])}")

        if blueprint_data['custom_instructions'] != 'Not chosen':
            prompt_parts.append(f"- Custom requirements: {blueprint_data['custom_instructions']}")

        if blueprint_data.get('protagonist_gender') != 'Not chosen':
            prompt_parts.append(f"- Protagonist gender: {blueprint_data['protagonist_gender']}")
    
        if blueprint_data.get('counterpart_type') != 'Not chosen':
            counterpart_info = blueprint_data['counterpart_type']
            if blueprint_data.get('counterpart_gender') != 'Not chosen':
                counterpart_info += f" ({blueprint_data['counterpart_gender']})"
            prompt_parts.append(f"- Main counterpart character: {counterpart_info}")
        
        # Add the rest of the comprehensive prompt requirements
        prompt_parts.extend(self._get_detailed_requirements(blueprint_data))
        
        return "\n".join(prompt_parts)

    def _get_detailed_requirements(self, blueprint_data):
        """Get detailed requirements section of the prompt"""
        prompt_parts = []
        
        prompt_parts.append("")
        prompt_parts.append("CRITICAL REQUIREMENTS FOR LONG STORIES:")
        prompt_parts.append("This blueprint MUST guide the creation of LONG, DETAILED stories. Include these specific instructions:")
        prompt_parts.append("")
        prompt_parts.append("SCENE REQUIREMENTS:")
        prompt_parts.append("- Create 15-25 scenes (NOT 10 scenes)")
        prompt_parts.append("- Each scene should be 2000-4000 words long")
        prompt_parts.append("- Scenes should be richly detailed with extensive dialogue, description, and character development")
        prompt_parts.append("- Include transition scenes and character development moments between major plot points")
        prompt_parts.append("")
    
        prompt_parts.append("BLUEPRINT REQUIREMENTS:")
        prompt_parts.append("Create a COMPREHENSIVE blueprint that includes ALL of the following sections in EXTENSIVE DETAIL:")
        prompt_parts.append("")
    
        # Genre-specific requirements
        if blueprint_data['genre'] == 'Detective/Mystery':
            prompt_parts.extend(self._get_mystery_requirements())
        else:
            prompt_parts.extend(self._get_generic_requirements())
        
        prompt_parts.extend(self._get_final_requirements())
        
        return prompt_parts

    def _get_mystery_requirements(self):
        """Get mystery-specific requirements"""
        return [
            "1. **STORY FOUNDATION:**",
            "   - Detailed victim profile (background, relationships, secrets, full life history)",
            "   - Complete killer profile (identity, motive, method, psychology, backstory)",
            "   - Crime details (when, where, how, weapon, evidence left behind, crime scene layout)",
            "   - Extended timeline of events covering weeks/months leading to and following the crime",
            "   - Multiple subplots and secondary mysteries to extend the story",
            "",
            "2. **EXTENSIVE CHARACTER DEVELOPMENT:**",
            "   - Detective/protagonist (detailed background, skills, personal life, flaws, growth arc)",
            "   - 6-8 suspects with comprehensive profiles (motives, alibis, secrets, red herrings, full backstories)",
            "   - 4-6 supporting characters (witnesses, authorities, family, friends, informants)",
            "   - Character relationship web showing how everyone connects",
            "   - Character development arcs that span the entire story",
            "",
            "3. **DETAILED PLOT STRUCTURE (15-25 SCENES):**",
            "   - Opening scenes (2-3 scenes): Character introduction, world-building, setup",
            "   - Discovery phase (3-4 scenes): Crime discovery, initial investigation, first clues",
            "   - Investigation development (6-8 scenes): Interviews, clue gathering, false leads",
            "   - Complication phase (3-4 scenes): New developments, red herrings, plot twists",
            "   - Revelation phase (2-3 scenes): Key discoveries, narrowing suspects",
            "   - Climax and resolution (2-3 scenes): Confrontation, explanation, aftermath",
            "   - Each scene should advance plot, develop characters, AND provide rich details",
            "",
            "4. **COMPREHENSIVE CLUE DISTRIBUTION (EXTENDED MYSTERY):**",
            "   - 12-15 genuine clues distributed across all scenes",
            "   - 6-8 red herrings and false leads to extend the investigation",
            "   - Multiple layers of mystery (primary crime plus 2-3 subplots)",
            "   - Clue revelation timeline spanning the entire story length",
            "   - Complex connections between clues that require extensive investigation",
            "",
            "5. **DETAILED SCENE-BY-SCENE BREAKDOWN:**",
            "   - 15-25 comprehensive scenes with specific content, dialogue, and purpose",
            "   - Each scene description should be 200-300 words detailing what happens",
            "   - Include character interactions, clue discoveries, and emotional beats",
            "   - Specify pacing: slow character development scenes AND fast action scenes",
            "   - Include transitional scenes that build atmosphere and develop relationships",
            "",
            "6. **RICH DIALOGUE AND INTERACTION GUIDE:**",
            "   - Detailed interrogation scenes with specific questions and responses",
            "   - Character-building conversations that reveal backstory and personality",
            "   - Subtext and hidden meanings that add depth to every interaction",
            "   - Multiple questioning rounds as new evidence emerges",
            "   - Relationship development through extended dialogue sequences",
            "",
            "7. **RICH SETTING AND ATMOSPHERE:**",
            "   - Multiple detailed locations with full descriptions and significance",
            "   - How each setting contributes to mood, character, and plot",
            "   - Atmospheric elements that build and maintain tension throughout",
            "   - Crime scene details, forensic considerations, and physical evidence",
            "   - Environmental storytelling that adds depth to every scene",
            "",
            "8. **SUBPLOT DEVELOPMENT FOR STORY LENGTH:**",
            "   - 2-3 substantial subplots that weave through the main mystery",
            "   - Character personal stories that develop alongside the investigation",
            "   - Secondary mysteries or complications that extend the narrative",
            "   - Relationship dynamics that evolve throughout the story",
            "   - Background elements that add richness and depth to the world"
        ]

    def _get_generic_requirements(self):
        """Get generic requirements for non-mystery genres"""
        return [
            "1. **EXTENSIVE STORY FOUNDATION:**",
            "   - Complex, multi-layered premise with several interconnected conflicts",
            "   - Protagonist with detailed background, multiple goals, and complex character arc",
            "   - Antagonist/opposition with nuanced motivations and their own character development",
            "   - Multiple thematic elements that develop throughout the extended narrative",
            "   - 2-3 substantial subplots that enhance and extend the main story",
            "",
            "2. **COMPREHENSIVE CHARACTER DEVELOPMENT:**",
            "   - Detailed protagonist profile (background, personality, flaws, relationships, growth)",
            "   - 4-6 supporting characters with their own arcs and development",
            "   - Character relationships that evolve and deepen throughout the story",
            "   - Distinctive dialogue voices and personality traits for each character",
            "   - Character backstories that influence present-day actions and decisions",
            "",
            "3. **EXTENDED PLOT STRUCTURE (15-25 SCENES):**",
            "   - Opening act (4-5 scenes): World-building, character introduction, multiple setups",
            "   - Development act (8-12 scenes): Rising action, complications, character growth",
            "   - Climax act (3-4 scenes): Multiple conflicts resolve, character arcs complete",
            "   - Resolution (2-3 scenes): Aftermath, character reflection, new beginnings",
            "   - Include pacing variety: introspective scenes, action scenes, dialogue-heavy scenes",
            "",
            "4. **DETAILED SCENE BREAKDOWN:**",
            "   - 15-25 substantial scenes, each 2000-4000 words when written",
            "   - Specific scene purposes: plot advancement, character development, world-building",
            "   - Rich scene descriptions including setting, mood, character actions",
            "   - Dialogue snippets and emotional beats for each scene",
            "   - Transitions and connections between scenes",
            "",
            "5. **EXTENSIVE WORLD-BUILDING AND SETTING:**",
            "   - Multiple detailed locations that serve the story and characters",
            "   - World rules and logic that support extended narrative exploration",
            "   - Cultural, social, or historical elements that add depth",
            "   - Environmental details that enhance mood and theme throughout",
            "   - How settings change and evolve as the story progresses",
            "",
            "6. **DEEP THEME AND SUBTEXT DEVELOPMENT:**",
            "   - Multiple interconnected themes explored throughout the extended narrative",
            "   - How themes develop and evolve through character actions and plot events",
            "   - Symbolic elements and motifs that recur throughout the story",
            "   - Questions and messages that develop complexity over the full story length",
            "   - Subtext in dialogue and action that adds layers of meaning"
        ]

    def _get_final_requirements(self):
        """Get final requirements section"""
        return [
            "",
            "CRITICAL FORMATTING AND LENGTH REQUIREMENTS:",
            "- Use clear headings and detailed subheadings",
            "- Provide extensive, specific details - NOT general advice",
            "- Include concrete examples, character names, and plot specifics",
            "- Make each section comprehensive and substantial (minimum 500 words per major section)",
            "- Scene descriptions should be detailed enough to guide 2000-4000 word scenes",
            "- ENSURE THE BLUEPRINT GUIDES CREATION OF 15-25 SCENES, NOT 10",
            "",
            "ABSOLUTE REQUIREMENTS:",
            "- This blueprint MUST result in stories of 30,000-60,000+ words",
            "- Stories generated from this blueprint should have 15-25 detailed scenes",
            "- Each scene should be rich, detailed, and substantial (2000-4000 words)",
            "- Include instructions for extensive character development and world-building",
            "- Provide guidance for creating complex, multi-layered narratives",
            "",
            "IMPORTANT: This blueprint will be used to generate detailed story bibles and scene plans for LONG STORIES. Make it as comprehensive and detailed as possible. Do not summarize - provide full, extensive guidance that will result in substantial, book-length narratives."
        ]

    def call_ollama_for_blueprint(self, prompt, model, blueprint_data):
        """Call Ollama API to generate blueprint content with dynamic settings"""
        url = "http://localhost:11434/api/generate"
        
        # Get optimized settings based on blueprint requirements
        generation_options = self.configure_generation_settings(blueprint_data)
        
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": generation_options
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response generated")
        except Exception as e:
            return f"Error: {e}"

    def configure_generation_settings(self, blueprint_data):
        """Configure generation settings based on user preferences"""
        # Use the user-specified max_tokens directly
        base_tokens = blueprint_data.get('max_tokens', 8192)
        
        return {
            "num_predict": base_tokens,  # Use user's choice directly
            "temperature": 0.8,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.15,
            "stop": []
        }
