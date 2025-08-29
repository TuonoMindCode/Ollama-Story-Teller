import os
import time
import requests

class StoryAnalyzer:
    def __init__(self, stories_folder, blueprint_folder, llm_settings):
        self.stories_folder = stories_folder
        self.blueprint_folder = blueprint_folder  # Store blueprint folder
     
        self.llm_settings = llm_settings
        self.analysis_folder = "analysis"
        os.makedirs(self.analysis_folder, exist_ok=True)
    
    def get_available_stories(self):
        """Get list of generated stories"""
        import glob
        story_files = glob.glob(os.path.join(self.stories_folder, "*.txt"))
        return [os.path.basename(f) for f in story_files]
    
    def analyze_story(self):
        """Browse and analyze existing stories"""
        stories = self.get_available_stories()
        
        if not stories:
            print(f"\nNo stories found in {self.stories_folder}/ folder.")
            print("Generate some stories first using option 12.")
            input("Press Enter to continue...")
            return
        
        print(f"\nAvailable stories ({len(stories)} found):")
        print("-" * 50)
        
        # Display stories with size and date info
        for i, story_file in enumerate(stories, 1):
            story_path = os.path.join(self.stories_folder, story_file)
            try:
                file_size = os.path.getsize(story_path)
                size_kb = file_size / 1024
                mod_time = os.path.getmtime(story_path)
                date_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(mod_time))
                print(f"{i:2d}. {story_file:<40} ({size_kb:.1f}KB - {date_str})")
            except:
                print(f"{i:2d}. {story_file}")
        
        try:
            choice = int(input(f"\nSelect story to analyze (1-{len(stories)}): "))
            if 1 <= choice <= len(stories):
                selected_story = stories[choice - 1]
                self.perform_story_analysis(selected_story)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")

    def call_ollama_direct(self, system_prompt, user_prompt, use_analysis_system=False):
        """Direct call to Ollama for story analysis with optional analysis system prompt"""
        url = "http://localhost:11434/api/generate"
        
        # Get base analysis system prompt and combine it
        if use_analysis_system:
            base_system = self.get_analysis_system_prompt()
            combined_system = f"{base_system}\n\n{system_prompt}"
        else:
            combined_system = system_prompt
        
        full_prompt = f"System: {combined_system}\n\nUser: {user_prompt}\n\nAssistant:"
        
        options = {
            "num_predict": self.llm_settings['max_tokens'],
            "temperature": self.llm_settings['temperature'],
            "top_p": self.llm_settings['top_p'],
            "top_k": self.llm_settings['top_k'],
            "repeat_penalty": self.llm_settings['repeat_penalty']
        }
        
        if self.llm_settings['seed'] is not None:
            options["seed"] = self.llm_settings['seed']
        
        data = {
            "model": self.llm_settings['model'],
            "prompt": full_prompt,
            "stream": False,
            "options": options
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response generated")
        except Exception as e:
            return f"Error: {e}"

    def get_analysis_system_prompt(self):
        """Get base system prompt for story analysis if it exists"""
        system_file = "analyze.system.txt"
        system_path = os.path.join(self.blueprint_folder, system_file) # Assuming blueprints folder
        
        try:
            with open(system_path, 'r', encoding='utf-8') as file:
                base_system = file.read().strip()
                print(f"  ✓ Found analysis system prompt: {system_file}")
                return base_system
        except FileNotFoundError:
            # Fallback to generic analysis system prompt
            return "You are a professional literary analyst with expertise in story analysis, narrative structure, and creative writing assessment."
        except Exception as e:
            print(f"Error reading analysis system prompt: {e}")
            return "You are a professional literary analyst with expertise in story analysis, narrative structure, and creative writing assessment."

    def perform_story_analysis(self, story_filename):
        """Perform detailed analysis of selected story"""
        story_path = os.path.join(self.stories_folder, story_filename)
        
        try:
            with open(story_path, 'r', encoding='utf-8') as file:
                story_content = file.read()
        except Exception as e:
            print(f"❌ Error reading story: {e}")
            return
        
        print(f"\n{'='*60}")
        print(f"ANALYZING: {story_filename}")
        print("="*60)
        
        # Show analysis options
        print("\nAnalysis Options:")
        print("1. Story Summary")
        print("2. Character Analysis")
        print("3. Plot Structure Breakdown")
        print("4. Writing Quality Assessment")
        print("5. Missing Elements Check")
        print("6. Genre Adherence Analysis")
        print("7. Improvement Suggestions")
        print("8. Complete Analysis (All above)")
        print("9. Custom Analysis Question")
        print("10. Back to main menu")
        
        try:
            analysis_choice = int(input("\nSelect analysis type (1-10): "))
            
            if analysis_choice == 10:
                return
            elif analysis_choice == 9:
                custom_question = input("Enter your analysis question: ")
                self.run_custom_analysis(story_content, story_filename, custom_question)
            elif 1 <= analysis_choice <= 8:
                self.run_predefined_analysis(story_content, story_filename, analysis_choice)
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

    def run_predefined_analysis(self, story_content, story_filename, analysis_type):
        """Run predefined analysis types with analysis system prompt"""
        
        analysis_prompts = {
            1: {
                "name": "Story Summary",
                "system": "You are a literary analyst specializing in story summarization. Provide clear, concise summaries that capture the essence of narratives.",
                "user": f"Provide a comprehensive summary of this story, including main plot points, key characters, and the resolution:\n\n{story_content}"
            },
            2: {
                "name": "Character Analysis", 
                "system": "You are a character development expert. Analyze characters for depth, motivation, consistency, and development arcs.",
                "user": f"Analyze all characters in this story. For each character, discuss their role, personality, motivations, development arc, and how well they're portrayed:\n\n{story_content}"
            },
            3: {
                "name": "Plot Structure Breakdown",
                "system": "You are a narrative structure analyst. Break down stories into their structural components and evaluate pacing and flow.",
                "user": f"Analyze the plot structure of this story. Identify the setup, inciting incident, rising action, climax, falling action, and resolution. Comment on pacing and structural effectiveness:\n\n{story_content}"
            },
            4: {
                "name": "Writing Quality Assessment",
                "system": "You are a writing quality assessor. Evaluate prose style, dialogue quality, descriptions, and overall writing craft.",
                "user": f"Assess the writing quality of this story. Evaluate prose style, dialogue naturalness, descriptive writing, consistency, and overall readability:\n\n{story_content}"
            },
            5: {
                "name": "Missing Elements Check",
                "system": "You are a story completeness checker. Identify gaps, inconsistencies, and missing elements that could improve the narrative.",
                "user": f"Identify what's missing from this story. Look for plot holes, underdeveloped elements, missing character motivations, unresolved threads, or areas that need more development:\n\n{story_content}"
            },
            6: {
                "name": "Genre Adherence Analysis",
                "system": "You are a genre expert. Analyze how well stories conform to genre expectations and conventions.",
                "user": f"Analyze how well this story adheres to its apparent genre conventions. Identify genre elements present, missing genre expectations, and how effectively it delivers on genre promises:\n\n{story_content}"
            },
            7: {
                "name": "Improvement Suggestions",
                "system": "You are a story development consultant. Provide constructive suggestions for improving narratives.",
                "user": f"Provide specific, actionable suggestions for improving this story. Focus on areas like character development, plot enhancement, pacing, dialogue, and overall narrative effectiveness:\n\n{story_content}"
            },
            8: {
                "name": "Complete Analysis",
                "system": "You are a comprehensive literary analyst. Provide thorough analysis covering all aspects of storytelling.",
                "user": f"Provide a complete analysis of this story covering: plot summary, character analysis, structure breakdown, writing quality, missing elements, genre adherence, and improvement suggestions:\n\n{story_content}"
            }
        }
        
        if analysis_type not in analysis_prompts:
            print("❌ Invalid analysis type.")
            return
        
        prompt_data = analysis_prompts[analysis_type]
        
        print(f"\n🔍 Running {prompt_data['name']}...")
        print("⏳ This may take a moment for longer stories...\n")
        
        # Use analysis system prompt
        result = self.call_ollama_direct(prompt_data['system'], prompt_data['user'], use_analysis_system=True)
        
        if result.startswith("Error:"):
            print(f"❌ Analysis failed: {result}")
            return
        
        print(f"📋 {prompt_data['name'].upper()} RESULTS:")
        print("="*60)
        print(result)
        print("="*60)
        
        # Offer to save analysis
        save_choice = input("\nSave this analysis to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            self.save_analysis(story_filename, prompt_data['name'], result)

    def run_custom_analysis(self, story_content, story_filename, custom_question):
        """Run custom analysis with user-provided question"""
        
        # Detect if this is a direct factual question vs analysis request
        direct_question_keywords = [
            'who is', 'who was', 'who did', 'what is', 'what was', 'what did',
            'where is', 'where was', 'when did', 'how did', 'why did',
            'who killed', 'who murdered', 'what happened', 'how was',
            'who is the killer', 'who is the murderer', 'what is the weapon',
            'where did', 'when was'
        ]
        
        is_direct_question = any(keyword in custom_question.lower() for keyword in direct_question_keywords)
        
        if is_direct_question:
            # Use direct answer system prompt
            system_prompt = "You are a story content expert. Answer direct questions about story content with factual, specific answers based solely on what is explicitly stated or clearly implied in the text. Do not provide literary analysis - just answer the question directly and concisely."
            
            user_prompt = f"Based on this story, answer this question directly and factually: {custom_question}\n\nStory content:\n{story_content}"
            
            print(f"\n🔍 Answering Direct Question...")
            print(f"❓ Question: {custom_question}")
            print("⏳ Getting direct answer...\n")
            
            # Don't use analysis system prompt for direct questions
            result = self.call_ollama_direct(system_prompt, user_prompt, use_analysis_system=False)
            
        else:
            # Use analysis system prompt for analytical questions
            system_prompt = "You are a comprehensive story analyst. Answer the user's specific question about the story with detailed, insightful analysis."
            
            user_prompt = f"Question about this story: {custom_question}\n\nStory content:\n{story_content}"
            
            print(f"\n🔍 Running Custom Analysis...")
            print(f"❓ Question: {custom_question}")
            print("⏳ This may take a moment...\n")
            
            # Use analysis system prompt for analytical questions
            result = self.call_ollama_direct(system_prompt, user_prompt, use_analysis_system=True)
        
        if result.startswith("Error:"):
            print(f"❌ Analysis failed: {result}")
            return
        
        if is_direct_question:
            print(f"📋 DIRECT ANSWER:")
        else:
            print(f"📋 CUSTOM ANALYSIS RESULTS:")
        print("="*60)
        print(result)
        print("="*60)
        
        # Offer to save analysis
        save_choice = input("\nSave this answer to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            analysis_type = "Direct Answer" if is_direct_question else "Custom Analysis"
            self.save_analysis(story_filename, analysis_type, result)

    def save_analysis(self, story_filename, analysis_type, analysis_result):
        """Save analysis results to file"""
        try:
            # Generate filename
            story_base = story_filename.replace('.txt', '')
            analysis_type_clean = analysis_type.replace(' ', '_').lower()
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            analysis_filename = f"{story_base}_{analysis_type_clean}_{timestamp}.txt"
            analysis_path = os.path.join(self.analysis_folder, analysis_filename)
            
            # Save analysis
            with open(analysis_path, 'w', encoding='utf-8') as file:
                file.write(f"STORY ANALYSIS REPORT\n")
                file.write(f"="*50 + "\n")
                file.write(f"Story File: {story_filename}\n")
                file.write(f"Analysis Type: {analysis_type}\n")
                file.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Model Used: {self.llm_settings['model']}\n")
                file.write(f"="*50 + "\n\n")
                file.write(analysis_result)
            
            print(f"✅ Analysis saved to: {analysis_path}")
            
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")