"""Log analyzer for examining Ollama prompt exchanges and effectiveness"""
import os
import glob
import re
import json
from datetime import datetime

class StoryLogAnalyzer:
    def __init__(self, stories_folder, llm_settings):
        self.stories_folder = stories_folder
        self.llm_settings = llm_settings
        self.logs_folder = os.path.join(os.path.dirname(stories_folder), 'logs')
        
    def get_available_log_files(self):
        """Get list of available log files"""
        if not os.path.exists(self.logs_folder):
            return []
        
        log_files = glob.glob(os.path.join(self.logs_folder, 'prompt_log_*.txt'))
        return sorted(log_files, key=lambda x: os.path.getmtime(x), reverse=True)
    
    def analyze_logs(self):
        """Main log analysis menu"""
        log_files = self.get_available_log_files()
        
        if not log_files:
            print(f"\n❌ No log files found in {self.logs_folder}")
            print("Enable prompt logging in Advanced Settings and generate some stories first.")
            input("Press Enter to continue...")
            return
        
        print(f"\n📊 LOG ANALYZER")
        print("="*60)
        print("Analyze Ollama prompt exchanges to improve story generation")
        print("="*60)
        
        print(f"\nAvailable log files ({len(log_files)} found):")
        print("-" * 80)
        
        # Display log files with info
        for i, log_file in enumerate(log_files, 1):
            try:
                filename = os.path.basename(log_file)
                size = os.path.getsize(log_file)
                size_mb = size / (1024 * 1024)
                mod_time = os.path.getmtime(log_file)
                date_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                
                # Extract story name from filename if possible
                story_match = re.search(r'prompt_log_(.+?)_\d{8}_\d{6}\.txt', filename)
                story_name = story_match.group(1) if story_match else "unknown"
                
                print(f"{i:2d}. {filename}")
                print(f"    Story: {story_name:<20} | Size: {size_mb:.1f}MB | Created: {date_str}")
                
            except Exception as e:
                print(f"{i:2d}. {os.path.basename(log_file)} (Error reading info: {e}")
        
        try:
            choice = int(input(f"\nSelect log file to analyze (1-{len(log_files)}): "))
            if 1 <= choice <= len(log_files):
                selected_log = log_files[choice - 1]
                self.analyze_selected_log(selected_log)
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def analyze_selected_log(self, log_file_path):
        """Analyze a specific log file"""
        try:
            with open(log_file_path, 'r', encoding='utf-8') as file:
                log_content = file.read()
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
            return
    
        # Parse the log file to extract exchanges
        exchanges = self.parse_log_exchanges(log_content)
    
        if not exchanges:
            print("❌ No valid exchanges found in log file")
            return
    
        filename = os.path.basename(log_file_path)
        print(f"\n📋 ANALYZING LOG: {filename}")
        print("="*80)
        print(f"Found {len(exchanges)} prompt exchanges in this log file")
        print()
        print("💡 TIP: Each exchange represents one conversation with Ollama")
        print("   (e.g., Story Bible generation, Scene Plan creation, Scene 1, Scene 2, etc.)")
    
        # Show exchange types/names
        print(f"\n🎯 SELECT WHICH EXCHANGE TO ANALYZE:")
        print("-" * 80)
        for i, exchange in enumerate(exchanges, 1):
            exchange_type = exchange.get('type', 'Unknown')
            model = exchange.get('model', 'Unknown')
            tokens = exchange.get('tokens', 'Unknown')
        
            # Add helpful descriptions for common exchange types
            description = self.get_exchange_description(exchange_type)
        
            print(f"{i:2d}. {exchange_type:<25} | Model: {model} | Tokens: {tokens}")
            if description:
                print(f"    └─ {description}")
    
        print(f"\n{len(exchanges) + 1}. 📊 Analyze All Exchanges at Once")
        print(f"    └─ Get a summary analysis of all exchanges in this log")
        print(f"{len(exchanges) + 2}. ⬅️  Back to Log File Selection")
    
        try:
            choice = int(input(f"\nSelect exchange to analyze (1-{len(exchanges) + 2}): "))
        
            if choice == len(exchanges) + 2:
                return
            elif choice == len(exchanges) + 1:
                self.analyze_all_exchanges(exchanges, filename)
            elif 1 <= choice <= len(exchanges):
                selected_exchange = exchanges[choice - 1]
                self.analyze_single_exchange(selected_exchange, choice, filename)
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def get_exchange_description(self, exchange_type):
        """Get helpful description for exchange types"""
        descriptions = {
            'Story Bible': 'Character profiles, world-building, and story foundation',
            'Scene Plan': 'Detailed outline of all scenes in the story',
            'Scene 1': 'First scene generation',
            'Scene 2': 'Second scene generation',
            'Scene 3': 'Third scene generation',
            'Scene 4': 'Fourth scene generation',
            'Scene 5': 'Fifth scene generation',
            'Final Scene': 'Story conclusion and ending',
            'Blueprint Generation': 'Creating the initial story blueprint',
            'Character Development': 'Developing character details and arcs',
            'Dialogue Generation': 'Creating character conversations',
            'Setting Description': 'Building the story world and locations'
        }
    
        # Try exact match first
        if exchange_type in descriptions:
            return descriptions[exchange_type]
    
        # Try partial matches
        for key, desc in descriptions.items():
            if key.lower() in exchange_type.lower():
                return desc
    
        # Check for scene numbers
        if 'scene' in exchange_type.lower():
            return 'Individual scene generation'
    
        return None
    
    def parse_log_exchanges(self, log_content):
        """Parse log content to extract individual exchanges"""
        exchanges = []
        
        # Split on exchange markers
        exchange_pattern = r'═{50,}.*?EXCHANGE.*?═{50,}'
        parts = re.split(exchange_pattern, log_content)
        
        if len(parts) < 2:
            # Try alternative parsing method
            return self.parse_log_exchanges_alternative(log_content)
        
        for i, part in enumerate(parts[1:], 1):  # Skip first empty part
            try:
                exchange = self.parse_single_exchange(part, i)
                if exchange:
                    exchanges.append(exchange)
            except Exception as e:
                print(f"Warning: Error parsing exchange {i}: {e}")
                continue
        
        return exchanges
    
    def parse_log_exchanges_alternative(self, log_content):
        """Alternative parsing method for different log formats"""
        exchanges = []
        
        # Look for system prompt markers
        system_pattern = r'SYSTEM PROMPT.*?(?=USER PROMPT|$)'
        user_pattern = r'USER PROMPT.*?(?=OLLAMA RESPONSE|$)'
        response_pattern = r'OLLAMA RESPONSE.*?(?=SYSTEM PROMPT|═{50,}|$)'
        
        system_matches = re.findall(system_pattern, log_content, re.DOTALL)
        user_matches = re.findall(user_pattern, log_content, re.DOTALL)
        response_matches = re.findall(response_pattern, log_content, re.DOTALL)
        
        min_matches = min(len(system_matches), len(user_matches), len(response_matches))
        
        for i in range(min_matches):
            exchange = {
                'number': i + 1,
                'type': f'Exchange {i + 1}',
                'system_prompt': self.clean_prompt_text(system_matches[i]),
                'user_prompt': self.clean_prompt_text(user_matches[i]),
                'response': self.clean_prompt_text(response_matches[i]),
                'model': 'Unknown',
                'tokens': 'Unknown'
            }
            exchanges.append(exchange)
        
        return exchanges
    
    def parse_single_exchange(self, exchange_text, exchange_num):
        """Parse a single exchange from log text"""
        exchange = {
            'number': exchange_num,
            'type': f'Exchange {exchange_num}',
            'system_prompt': '',
            'user_prompt': '',
            'response': '',
            'model': 'Unknown',
            'tokens': 'Unknown'
        }
        
        # Extract exchange type/name
        type_match = re.search(r'Type: (.+)', exchange_text)
        if type_match:
            exchange['type'] = type_match.group(1).strip()
        
        # Extract model
        model_match = re.search(r'Model: (.+)', exchange_text)
        if model_match:
            exchange['model'] = model_match.group(1).strip()
        
        # Extract tokens
        tokens_match = re.search(r'Tokens: (.+)', exchange_text)
        if tokens_match:
            exchange['tokens'] = tokens_match.group(1).strip()
        
        # Extract system prompt
        system_match = re.search(r'SYSTEM PROMPT.*?─{20,}(.*?)(?=USER PROMPT|$)', exchange_text, re.DOTALL)
        if system_match:
            exchange['system_prompt'] = self.clean_prompt_text(system_match.group(1))
        
        # Extract user prompt
        user_match = re.search(r'USER PROMPT.*?─{20,}(.*?)(?=OLLAMA RESPONSE|$)', exchange_text, re.DOTALL)
        if user_match:
            exchange['user_prompt'] = self.clean_prompt_text(user_match.group(1))
        
        # Extract response
        response_match = re.search(r'OLLAMA RESPONSE.*?─{20,}(.*?)(?=═{50,}|$)', exchange_text, re.DOTALL)
        if response_match:
            exchange['response'] = self.clean_prompt_text(response_match.group(1))
        
        return exchange
    
    def clean_prompt_text(self, text):
        """Clean and format prompt text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text
    
    def analyze_single_exchange(self, exchange, exchange_num, log_filename):
        """Analyze a single prompt exchange"""
        print(f"\n🔍 ANALYZING EXCHANGE {exchange_num}")
        print("="*80)
        print(f"Log File: {log_filename}")
        print(f"Exchange Type: {exchange['type']}")
        print(f"Model: {exchange['model']}")
        print(f"Tokens: {exchange['tokens']}")
        print("="*80)
        
        # Show the exchange details
        print(f"\n📋 SYSTEM PROMPT:")
        print("-" * 40)
        system_preview = exchange['system_prompt'][:500] + "..." if len(exchange['system_prompt']) > 500 else exchange['system_prompt']
        print(system_preview)
        
        print(f"\n📝 USER PROMPT:")
        print("-" * 40)
        user_preview = exchange['user_prompt'][:500] + "..." if len(exchange['user_prompt']) > 500 else exchange['user_prompt']
        print(user_preview)
        
        print(f"\n🤖 OLLAMA RESPONSE:")
        print("-" * 40)
        response_preview = exchange['response'][:500] + "..." if len(exchange['response']) > 500 else exchange['response']
        print(response_preview)
        
        print("\n" + "="*80)
        print("WHAT WOULD YOU LIKE TO DO?")
        print("="*80)
        print("1. 📖 Read Complete Exchange")
        print("   └─ View the full system prompt, user prompt, and response")
        print()
        print("2. 🤖 AI-Powered Analysis")
        print("   └─ Let AI analyze prompt effectiveness and suggest improvements")
        print()
        print("3. ✍️  Manual Analysis (Answer Key Questions)")
        print("   └─ Answer guided questions about prompt effectiveness yourself")
        print("   └─ Includes: Does response follow system prompt? What improvements needed?")
        print()
        print("4. 💾 Export Exchange to Text File")
        print("   └─ Save this exchange (prompts + response) for external analysis")
        print()
        print("5. ⬅️  Back to Exchange List")
        print("   └─ Return to choose a different exchange")
        
        try:
            analysis_choice = int(input("\nSelect option (1-5): "))
            
            if analysis_choice == 1:
                self.show_full_exchange(exchange)
            elif analysis_choice == 2:
                self.run_ai_prompt_analysis(exchange)
            elif analysis_choice == 3:
                self.run_manual_analysis_questions(exchange)
            elif analysis_choice == 4:
                self.save_exchange_to_file(exchange, log_filename)
            elif analysis_choice == 5:
                return
            else:
                print("❌ Invalid choice.")
                
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_full_exchange(self, exchange):
        """Show the complete exchange details"""
        print(f"\n📋 FULL EXCHANGE DETAILS")
        print("="*80)
        
        print(f"🔧 SYSTEM PROMPT ({len(exchange['system_prompt'])} characters):")
        print("─" * 80)
        print(exchange['system_prompt'])
        
        print(f"\n📝 USER PROMPT ({len(exchange['user_prompt'])} characters):")
        print("─" * 80)
        print(exchange['user_prompt'])
        
        print(f"\n🤖 OLLAMA RESPONSE ({len(exchange['response'])} characters):")
        print("─" * 80)
        print(exchange['response'])
        
        print("\n" + "="*80)
        input("Press Enter to continue...")
    
    def run_ai_prompt_analysis(self, exchange):
        """Use AI to analyze the prompt effectiveness"""
        print(f"\n🤖 AI ANALYSIS OF PROMPT EFFECTIVENESS")
        print("="*60)
        print("Using AI to analyze this prompt exchange...")
        print("⏳ This may take a moment...\n")
        
        # Create analysis prompt
        analysis_prompt = f"""Analyze this Ollama prompt exchange for effectiveness:

SYSTEM PROMPT:
{exchange['system_prompt']}

USER PROMPT: 
{exchange['user_prompt']}

OLLAMA RESPONSE:
{exchange['response']}

Please analyze and provide insights on:

1. **Prompt Effectiveness**: Does the response follow the system prompt instructions?

2. **System Prompt Quality**: Is the system prompt clear, specific, and well-structured?

3. **User Prompt Quality**: Is the user prompt clear and does it provide necessary context?

4. **Response Quality**: Does the response meet the apparent goals of the prompts?

5. **Improvement Suggestions**: What specific improvements could be made to either prompt?

6. **Adherence Analysis**: Point out any places where Ollama ignored or misinterpreted instructions.

Provide specific, actionable feedback for improving these prompts."""
        
        # Call Ollama for analysis
        result = self.call_ollama_for_analysis(analysis_prompt)
        
        if result.startswith("Error:"):
            print(f"❌ Analysis failed: {result}")
            return
        
        print(f"📊 AI ANALYSIS RESULTS:")
        print("="*60)
        print(result)
        print("="*60)
        
        # Offer to save
        save_choice = input("\nSave this analysis to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            self.save_analysis_to_file(exchange, result, "AI_Analysis")
        
        input("\nPress Enter to continue...")
    
    def run_manual_analysis_questions(self, exchange):
        """Run manual analysis with guided questions"""
        print(f"\n✍️  MANUAL PROMPT ANALYSIS")
        print("="*70)
        print("You'll be asked to evaluate this prompt exchange by answering")
        print("key questions about its effectiveness.")
        print()
        print("🎯 FOCUS AREAS:")
        print("• Does Ollama follow the system prompt instructions?")
        print("• How effective are the prompts?")
        print("• What improvements could be made?")
        print("="*70)
        
        # Your specific priority questions
        priority_questions = [
            {
                "question": "Add your observations about prompt effectiveness:",
                "help": "What do you notice about how well this exchange worked overall?"
            },
            {
                "question": "Does the response follow the system prompt?",
                "help": "Did Ollama do what the system prompt asked it to do? Explain why or why not."
            },
            {
                "question": "What improvements are needed to the system prompt or user prompt?",
                "help": "What specific changes would make these prompts work better?"
            }
        ]
        
        # Additional questions
        additional_questions = [
            {
                "question": "Rate the overall effectiveness (1-10) and explain your reasoning:",
                "help": "1=Completely ineffective, 10=Perfect. What's your rating and why?"
            },
            {
                "question": "What worked best in this exchange?",
                "help": "What aspects of the prompts or response were most successful?"
            },
            {
                "question": "What could be improved for better results?",
                "help": "What specific changes would you make for next time?"
            }
        ]
        
        answers = {}
        
        print(f"\n🔍 PRIORITY QUESTIONS (Most Important):")
        print("-" * 50)
        
        for i, q_data in enumerate(priority_questions, 1):
            print(f"\n⭐ QUESTION {i}:")
            print(f"   {q_data['question']}")
            print(f"   💡 Hint: {q_data['help']}")
            answer = input("\n   Your answer: ").strip()
            answers[f"priority_{i}"] = answer
        
        print(f"\n📋 ADDITIONAL QUESTIONS (Optional but helpful):")
        print("-" * 50)
        
        for i, q_data in enumerate(additional_questions, 1):
            print(f"\n{i + 3}. {q_data['question']}")
            print(f"   💡 Hint: {q_data['help']}")
            answer = input("\n   Your answer: ").strip()
            answers[f"additional_{i}"] = answer
        
        # Format the analysis with clearer sections
        manual_analysis = f"""MANUAL PROMPT ANALYSIS REPORT
═══════════════════════════════════════════════════════════
Exchange: {exchange['type']}
Model: {exchange['model']}
Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════════════════════════════════════

🎯 PRIORITY ANALYSIS (Key Questions):

1. PROMPT EFFECTIVENESS OBSERVATIONS:
{answers['priority_1']}

2. DOES RESPONSE FOLLOW SYSTEM PROMPT?
{answers['priority_2']}

3. IMPROVEMENTS NEEDED TO PROMPTS:
{answers['priority_3']}

📊 ADDITIONAL ANALYSIS:

4. Overall Effectiveness Rating & Reasoning:
{answers['additional_1']}

5. What Worked Best:
{answers['additional_2']}

6. Areas for Improvement:
{answers['additional_3']}

═══════════════════════════════════════════════════════════
End of Analysis Report
═══════════════════════════════════════════════════════════
"""
        
        print(f"\n📋 YOUR COMPLETED ANALYSIS:")
        print("="*70)
        print(manual_analysis)
        print("="*70)
        
        # Offer to save
        save_choice = input("\nSave this analysis to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            self.save_analysis_to_file(exchange, manual_analysis, "Manual_Analysis")
        
        input("\nPress Enter to continue...")
    
    def save_exchange_to_file(self, exchange, log_filename):
        """Save exchange details to a file"""
        try:
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            exchange_type = exchange['type'].replace(' ', '_').replace('/', '_')
            filename = f"exchange_{exchange_type}_{timestamp}.txt"
            
            # Create analysis folder if it doesn't exist
            analysis_folder = "analysis"
            os.makedirs(analysis_folder, exist_ok=True)
            
            filepath = os.path.join(analysis_folder, filename)
            
            # Write exchange
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"PROMPT EXCHANGE EXPORT\n")
                f.write(f"="*50 + "\n")
                f.write(f"Source Log: {log_filename}\n")
                f.write(f"Exchange Type: {exchange['type']}\n")
                f.write(f"Model: {exchange['model']}\n")
                f.write(f"Tokens: {exchange['tokens']}\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"="*50 + "\n\n")
                
                f.write(f"SYSTEM PROMPT ({len(exchange['system_prompt'])} characters):\n")
                f.write("-" * 50 + "\n")
                f.write(exchange['system_prompt'])
                f.write("\n\n")
                
                f.write(f"USER PROMPT ({len(exchange['user_prompt'])} characters):\n")
                f.write("-" * 50 + "\n")
                f.write(exchange['user_prompt'])
                f.write("\n\n")
                
                f.write(f"OLLAMA RESPONSE ({len(exchange['response'])} characters):\n")
                f.write("-" * 50 + "\n")
                f.write(exchange['response'])
            
            print(f"✅ Exchange saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error saving exchange: {e}")
        
        input("Press Enter to continue...")
    
    def save_analysis_to_file(self, exchange, analysis_content, analysis_type):
        """Save analysis results to file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            exchange_type = exchange['type'].replace(' ', '_').replace('/', '_')
            filename = f"analysis_{exchange_type}_{analysis_type}_{timestamp}.txt"
            
            # Create analysis folder if it doesn't exist
            analysis_folder = "analysis"
            os.makedirs(analysis_folder, exist_ok=True)
            
            filepath = os.path.join(analysis_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"PROMPT ANALYSIS REPORT\n")
                f.write(f"="*50 + "\n")
                f.write(f"Exchange Type: {exchange['type']}\n")
                f.write(f"Model: {exchange['model']}\n")
                f.write(f"Analysis Type: {analysis_type}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"="*50 + "\n\n")
                f.write(analysis_content)
            
            print(f"✅ Analysis saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
    
    def analyze_all_exchanges(self, exchanges, log_filename):
        """Analyze all exchanges in the log file"""
        print(f"\n🔍 ANALYZING ALL EXCHANGES")
        print("="*60)
        print(f"Processing {len(exchanges)} exchanges...")
        print("⏳ This may take several minutes...\n")
        
        summary_analysis = f"""COMPLETE LOG ANALYSIS SUMMARY
Log File: {log_filename}
Total Exchanges: {len(exchanges)}
Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXCHANGE SUMMARY:
"""
        
        for i, exchange in enumerate(exchanges, 1):
            print(f"Analyzing exchange {i}/{len(exchanges)}: {exchange['type']}")
            
            # Quick analysis of each exchange
            system_len = len(exchange['system_prompt'])
            user_len = len(exchange['user_prompt'])
            response_len = len(exchange['response'])
            
            summary_analysis += f"""
Exchange {i}: {exchange['type']}
  Model: {exchange['model']} | Tokens: {exchange['tokens']}
  System Prompt: {system_len} chars
  User Prompt: {user_len} chars
  Response: {response_len} chars
  System Preview: {exchange['system_prompt'][:100]}...
  Response Preview: {exchange['response'][:100]}...
"""
        
        print(f"\n📊 COMPLETE LOG ANALYSIS:")
        print("="*60)
        print(summary_analysis)
        print("="*60)
        
        # Offer to save
        save_choice = input("\nSave complete analysis to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"complete_log_analysis_{timestamp}.txt"
                
                analysis_folder = "analysis"
                os.makedirs(analysis_folder, exist_ok=True)
                
                filepath = os.path.join(analysis_folder, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(summary_analysis)
                
                print(f"✅ Complete analysis saved to: {filepath}")
                
            except Exception as e:
                print(f"❌ Error saving analysis: {e}")
        
        input("\nPress Enter to continue...")
    
    def call_ollama_for_analysis(self, prompt):
        """Call Ollama to analyze prompts"""
        import requests
        
        url = "http://localhost:11434/api/generate"
        
        system_prompt = "You are an expert prompt engineer and AI interaction analyst. You specialize in evaluating the effectiveness of AI prompts and responses, identifying areas for improvement, and providing actionable feedback for better AI interactions."
        
        full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        
        options = {
            "num_predict": 4096,  # Use reasonable token limit for analysis
            "temperature": 0.3,   # Lower temperature for more analytical response
            "top_p": 0.9,
        }
        
        data = {
            "model": self.llm_settings['model'],
            "prompt": full_prompt,
            "stream": False,
            "options": options
        }
        
        try:
            response = requests.post(url, json=data, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response generated")
        except Exception as e:
            return f"Error: {e}"
