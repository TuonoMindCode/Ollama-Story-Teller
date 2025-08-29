import os
from typing import Optional
from .model_tester import ModelTester

class SingleSceneGenerator:
    def __init__(self, model_tester: ModelTester):
        self.model_tester = model_tester
    
    def run_single_scene_menu(self):
        """Single scene generation menu"""
        while True:
            print("\n" + "="*60)
            print("📝 SINGLE SCENE GENERATION")
            print("="*60)
            
            # Check model selection
            current_model = self.model_tester.test_config['model']
            if current_model:
                print(f"Using model: {current_model}")
                self._display_current_settings()
            else:
                print("❌ No model selected")
            
            print("\n1. Generate from template")
            print("2. Generate from custom prompt")
            print("3. Generate from file")
            print("4. Quick creative prompt")
            print("5. Select different model")
            print("6. Adjust generation settings")
            print("7. Back to testing menu")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                if current_model:
                    self.generate_from_template()
                else:
                    self._prompt_select_model()
            elif choice == "2":
                if current_model:
                    self.generate_from_custom()
                else:
                    self._prompt_select_model()
            elif choice == "3":
                if current_model:
                    self.generate_from_file()
                else:
                    self._prompt_select_model()
            elif choice == "4":
                if current_model:
                    self.quick_creative_prompt()
                else:
                    self._prompt_select_model()
            elif choice == "5":
                self.select_model()
            elif choice == "6":
                self.adjust_settings()
            elif choice == "7":
                break
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def _display_current_settings(self):
        """Display current generation settings"""
        config = self.model_tester.test_config
        print(f"Settings: Temp={config['temperature']}, Top-p={config['top_p']}, "
              f"Top-k={config['top_k']}, Tokens={config['max_tokens']}")
    
    def _prompt_select_model(self):
        """Prompt user to select a model"""
        print("\n❌ No model selected. Please select a model first.")
        self.select_model()
    
    def select_model(self):
        """Select model for testing"""
        models = self.model_tester.get_available_models()
        
        if not models:
            print("\n❌ No Ollama models found")
            input("Press Enter to continue...")
            return
        
        print("\n🤖 SELECT MODEL:")
        for i, model in enumerate(models, 1):
            current = " (current)" if model == self.model_tester.test_config['model'] else ""
            print(f"{i:2d}. {model}{current}")
        
        try:
            choice = int(input(f"\nSelect model (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                self.model_tester.test_config['model'] = models[choice - 1]
                print(f"✅ Model set to: {models[choice - 1]}")
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
        
        input("Press Enter to continue...")
    
    def adjust_settings(self):
        """Adjust generation settings"""
        config = self.model_tester.test_config
        
        print("\n⚙️  ADJUST GENERATION SETTINGS")
        print("="*40)
        print("(Press Enter to keep current value)")
        
        try:
            # Temperature
            temp = input(f"Temperature [{config['temperature']}]: ").strip()
            if temp:
                new_temp = float(temp)
                if 0.0 <= new_temp <= 2.0:
                    config['temperature'] = new_temp
                else:
                    print("⚠️  Temperature should be between 0.0 and 2.0")
            
            # Top-p
            top_p = input(f"Top-p [{config['top_p']}]: ").strip()
            if top_p:
                new_top_p = float(top_p)
                if 0.0 <= new_top_p <= 1.0:
                    config['top_p'] = new_top_p
                else:
                    print("⚠️  Top-p should be between 0.0 and 1.0")
            
            # Top-k
            top_k = input(f"Top-k [{config['top_k']}]: ").strip()
            if top_k:
                new_top_k = int(top_k)
                if new_top_k > 0:
                    config['top_k'] = new_top_k
                else:
                    print("⚠️  Top-k should be positive")
            
            # Max tokens
            tokens = input(f"Max tokens [{config['max_tokens']}]: ").strip()
            if tokens:
                new_tokens = int(tokens)
                if new_tokens > 0:
                    config['max_tokens'] = new_tokens
                else:
                    print("⚠️  Max tokens should be positive")
            
            print("✅ Settings updated")
            
        except ValueError:
            print("❌ Invalid input format")
        
        input("Press Enter to continue...")
    
    def generate_from_template(self):
        """Generate using a template"""
        templates = self.model_tester.get_templates()
        
        if not templates:
            print("\n❌ No templates found")
            input("Press Enter to continue...")
            return
        
        # Simple template selection
        all_templates = []
        print("\n📋 SELECT TEMPLATE:")
        template_num = 1
        
        for category, category_templates in templates.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for template in category_templates:
                print(f"{template_num:2d}. {template['name']}")
                all_templates.append(template)
                template_num += 1
        
        try:
            choice = int(input(f"\nSelect template (1-{len(all_templates)}): "))
            if 1 <= choice <= len(all_templates):
                template = all_templates[choice - 1]
                self._run_generation(
                    template['system_prompt'],
                    template['user_prompt'],
                    template['name']
                )
            else:
                print("❌ Invalid choice")
                input("Press Enter to continue...")
        except ValueError:
            print("❌ Invalid input")
            input("Press Enter to continue...")
    
    def generate_from_custom(self):
        """Generate using custom prompts"""
        print("\n📝 CUSTOM PROMPT GENERATION")
        print("-" * 40)
        
        system_prompt = input("System prompt (optional): ").strip()
        if not system_prompt:
            system_prompt = "You are a skilled creative writer. Write engaging, detailed scenes with good character development."
        
        user_prompt = input("Scene prompt: ").strip()
        if not user_prompt:
            print("❌ Scene prompt is required")
            input("Press Enter to continue...")
            return
        
        self._run_generation(system_prompt, user_prompt, "Custom_Scene")
    
    def generate_from_file(self):
        """Generate using prompts from file"""
        file_path = input("Enter file path: ").strip()
        
        if not os.path.exists(file_path):
            print("❌ File not found")
            input("Press Enter to continue...")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Parse file content
            if "SYSTEM:" in content and "USER:" in content:
                parts = content.split("USER:", 1)
                system_prompt = parts[0].replace("SYSTEM:", "").strip()
                user_prompt = parts[1].strip()
            else:
                system_prompt = "You are a skilled creative writer."
                user_prompt = content
            
            filename = os.path.basename(file_path)
            self._run_generation(system_prompt, user_prompt, f"File_{filename}")
            
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            input("Press Enter to continue...")
    
    def quick_creative_prompt(self):
        """Quick creative writing prompts"""
        prompts = [
            "Write a scene where someone discovers a hidden door in their house",
            "Write a dialogue between two strangers stuck in an elevator",
            "Write a scene at a coffee shop where someone overhears something they shouldn't",
            "Write about a character who can hear other people's thoughts for one day",
            "Write a scene where someone finds an old letter that changes everything",
            "Write about a mysterious package delivered to the wrong address",
            "Write a scene where two childhood friends meet after 20 years",
            "Write about someone who discovers they can pause time"
        ]
        
        print("\n⚡ QUICK CREATIVE PROMPTS:")
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt}")
        
        print(f"{len(prompts) + 1}. Random selection")
        
        try:
            choice = int(input(f"Select prompt (1-{len(prompts) + 1}): "))
            
            if choice == len(prompts) + 1:
                import random
                selected_prompt = random.choice(prompts)
            elif 1 <= choice <= len(prompts):
                selected_prompt = prompts[choice - 1]
            else:
                print("❌ Invalid choice")
                input("Press Enter to continue...")
                return
            
            system_prompt = "You are a creative writer. Write an engaging scene with vivid details, good dialogue, and interesting characters."
            self._run_generation(system_prompt, selected_prompt, "Quick_Creative")
            
        except ValueError:
            print("❌ Invalid input")
            input("Press Enter to continue...")
    
    def _run_generation(self, system_prompt: str, user_prompt: str, name: str):
        """Run the actual generation with streaming output"""
        print(f"\n🚀 GENERATING: {name}")
        print("="*60)
        print("📝 Prompt Preview:")
        print(f"System: {system_prompt[:100]}{'...' if len(system_prompt) > 100 else ''}")
        print(f"User: {user_prompt[:100]}{'...' if len(user_prompt) > 100 else ''}")
        print("\n" + "="*60)
        print("🤖 OLLAMA OUTPUT:")
        print("-" * 60)
        
        # Create session folder
        session_folder = self.model_tester.create_session_folder("single_scene")
        
        def stream_callback(content, full_response):
            print(content, end='', flush=True)
        
        # Run generation
        result = self.model_tester.stream_ollama_request(
            system_prompt,
            user_prompt,
            self.model_tester.test_config,
            stream_callback
        )
        
        print("\n" + "-" * 60)
        
        if result['success']:
            word_count = len(result['response'].split())
            print(f"✅ Generation completed!")
            print(f"⏱️  Time: {result['generation_time']:.2f}s")
            print(f"📊 Words: {word_count:,}")
            print(f"📊 Tokens: {result['token_count']:,}")
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        
        # Save result
        test_info = {
            'model': self.model_tester.test_config['model'],
            'test_type': 'single_scene',
            'template_name': name,
            'system_prompt': system_prompt,
            'user_prompt': user_prompt
        }
        
        filepath = self.model_tester.save_test_result(result, test_info, session_folder)
        print(f"💾 Saved to: {os.path.basename(filepath)}")
        
        input("\nPress Enter to continue...")
