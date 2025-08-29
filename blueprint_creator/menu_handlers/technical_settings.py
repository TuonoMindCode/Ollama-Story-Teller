"""Technical settings handlers"""
from ..config import *
import requests
import time

class TechnicalSettingsHandler:
    def __init__(self, blueprint_creator):
        self.bc = blueprint_creator

    def set_llm_model(self, blueprint_data):
        """Set LLM model for blueprint generation - Fast version"""
        print("\n" + "-"*40)
        print("LLM MODEL SELECTION")
        print("-"*40)
        print("Choose which Ollama model to use for blueprint generation.\n")

        # Fast model fetching - no extra details
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                available_models = [model['name'] for model in models_data.get('models', [])]
            else:
                available_models = ["mistral:latest", "llama2", "dolphin3:latest"]
        except:
            print("❌ Cannot connect to Ollama. Using fallback models.")
            available_models = ["mistral:latest", "llama2", "dolphin3:latest"]

        if not available_models:
            print("❌ No models found!")
            print("Please install models first with: ollama pull mistral")
            input("Press Enter to continue...")
            return

        print(f"Available models ({len(available_models)} found):")
        for i, model in enumerate(available_models, 1):
            print(f"{i:2d}. {model}")

        current_model = blueprint_data.get('llm_model', 'mistral:latest')
        print(f"\n{len(available_models)+1}. Keep current ({current_model})")

        try:
            choice = int(input(f"\nSelect model (1-{len(available_models)+1}): "))
            if 1 <= choice <= len(available_models):
                selected_model = available_models[choice-1]
                blueprint_data['llm_model'] = selected_model
                print(f"✅ Model set to: {selected_model}")
            else:
                print("✅ Model unchanged")
        except ValueError:
            print("❌ Invalid input, model unchanged")

        input("Press Enter to continue...")


    def set_max_tokens(self, blueprint_data):
        """Set maximum tokens for blueprint generation"""
        print("\n" + "-"*40)
        print("MAX TOKENS (BLUEPRINT LENGTH)")
        print("-"*40)
        print("Controls how long and detailed the generated blueprint will be.")
        print("More tokens = longer, more comprehensive blueprints.\n")

        print("RECOMMENDED SETTINGS:")
        print("┌────────────┬─────────────────┬──────────────────────────────┐")
        print("│ Tokens     │ Blueprint Size  │ Description                  │")
        print("├────────────┼─────────────────┼──────────────────────────────┤")
        print("│ 4,096      │ Basic          │ Essential elements only      │")
        print("│ 8,192      │ Standard       │ Good detail, most genres     │")
        print("│ 16,384     │ Comprehensive  │ Very detailed, complex plots │")
        print("│ 32,768     │ Exhaustive     │ Maximum detail, all elements │")
        print("│ 65,536     │ Ultra-detailed │ Extreme detail (very slow)   │")
        print("│ 131,072    │ Maximum        │ Absolute maximum (slowest)   │")
        print("└────────────┴─────────────────┴──────────────────────────────┘")

        print(f"\nCurrent setting: {blueprint_data['max_tokens']:,} tokens")

        print("\nCOMMON CHOICES:")
        print("1. 4,096    - Basic blueprint (quick generation)")
        print("2. 8,192    - Standard blueprint (recommended)")
        print("3. 16,384   - Comprehensive blueprint (detailed)")
        print("4. 32,768   - Exhaustive blueprint (very detailed)")
        print("5. 65,536   - Ultra-detailed blueprint (maximum)")
        print("6. 131,072  - Absolute maximum (slowest)")
        print("7. Custom   - Enter your own value (1,024-131,072)")
        print("8. Keep current setting")

        try:
            choice = input("Select option (1-8): ").strip()

            if choice in TOKEN_OPTIONS:
                blueprint_data['max_tokens'] = TOKEN_OPTIONS[choice]
                print(f"✓ Max tokens set to: {blueprint_data['max_tokens']:,}")

                time_estimate = self._get_time_estimate(blueprint_data['max_tokens'])
                print(f"  Estimated generation time: {time_estimate}")

                if blueprint_data['max_tokens'] >= 65536:
                    print("  ⚠️  WARNING: Very high token count may be slow and memory intensive!")
                    print("     Consider using a smaller value unless you need maximum detail.")

            elif choice == "7":
                custom_tokens = int(input("Enter custom token count (1,024-131,072): "))
                if 1024 <= custom_tokens <= 131072:
                    blueprint_data['max_tokens'] = custom_tokens
                    print(f"✓ Max tokens set to: {blueprint_data['max_tokens']:,}")

                    time_estimate = self._get_time_estimate(custom_tokens)
                    print(f"  Estimated generation time: {time_estimate}")

                    if custom_tokens >= 65536:
                        print("  ⚠️  WARNING: Very high token count may be slow and memory intensive!")
                else:
                    print("❌ Invalid token count. Must be between 1,024 and 131,072.")
            elif choice == "8":
                print(f"✓ Keeping current setting: {blueprint_data['max_tokens']:,} tokens")
            else:
                print("❌ Invalid choice.")

        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")

        input("Press Enter to continue...")

    def set_target_length(self, blueprint_data):
        """Set target story length"""
        print("\n" + "-"*40)
        print("TARGET STORY LENGTH")
        print("-"*40)
        print("Set how long you want stories generated from this blueprint to be.\n")

        print("Length options:")
        for num, (length, description) in LENGTH_OPTIONS.items():
            print(f"{num}. {length} - {description}")
        print(f"6. Keep current ({blueprint_data['target_length']})")

        try:
            choice = int(input("Select length (1-6): "))
            if 1 <= choice <= 4:
                blueprint_data['target_length'] = LENGTH_OPTIONS[choice][0]
                print(f"✓ Target length set to: {LENGTH_OPTIONS[choice][0]}")
                print(f"  Expected: {LENGTH_OPTIONS[choice][1]}")
            elif choice == 5:
                scenes = input("Enter target scene count (8-30): ").strip()
                words = input("Enter target word count (15000-100000): ").strip()
                if scenes and words:
                    blueprint_data['target_length'] = f"Custom ({scenes} scenes, {words} words)"
                    print(f"✓ Custom length set: {blueprint_data['target_length']}")
            elif choice == 6:
                print("✓ Length unchanged")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")

        input("Press Enter to continue...")

    # Helper methods
    def _check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def _get_available_ollama_models(self):
        """Get list of available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []


    def _get_time_estimate(self, tokens):
        """Get time estimate for token generation"""
        if tokens <= 4096:
            return "1-3 minutes"
        elif tokens <= 8192:
            return "2-5 minutes"
        elif tokens <= 16384:
            return "5-10 minutes"
        elif tokens <= 32768:
            return "10-20 minutes"
        elif tokens <= 65536:
            return "20-40 minutes"
        else:
            return "40+ minutes"
