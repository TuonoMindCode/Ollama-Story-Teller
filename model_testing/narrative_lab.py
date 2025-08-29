import os
import datetime
from typing import Dict, List
from .model_tester import ModelTester

class NarrativeLab:
    def __init__(self, model_tester: ModelTester):
        self.model_tester = model_tester
        
        # Just a few key styles for now
        self.styles = {
            'literary': {
                'name': 'Literary Fiction',
                'system_addit ision': 'Write in a literary fiction style with rich prose and deep character insight.',
                'description': 'Rich, sophisticated prose'
            },
            'dialogue_heavy': {
                'name': 'Dialogue-Heavy',
                'system_addition': 'Focus heavily on dialogue with minimal description. Let characters reveal themselves through speech.',
                'description': 'Character-driven dialogue focus'
            },
            'minimalist': {
                'name': 'Minimalist',
                'system_addition': 'Write in a minimalist style like Hemingway. Use simple, direct language.',
                'description': 'Simple, direct, understated'
            }
        }
        
        # Just a few scene templates
        self.scenes = [
            "Write a scene where two characters have an important conversation in a busy coffee shop.",
            "Write a scene where two close friends have a heated argument about a betrayal.",
            "Write a scene where the protagonist discovers something that changes everything."
        ]
    
    def run_lab_menu(self):
        """Simple narrative lab menu"""
        while True:
            print("\n" + "="*60)
            print("🎭 NARRATIVE STYLE LABORATORY")
            print("="*60)
            
            if not self.model_tester.test_config.get('model'):
                print("❌ No model selected")
                if not self._select_model():
                    return
            
            print(f"Using model: {self.model_tester.test_config['model']}")
            print("\n1. Single scene with streaming")
            print("2. Compare multiple styles")
            print("3. Back to testing menu")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == "1":
                self._single_scene_streaming()
            elif choice == "2":
                self._compare_styles()
            elif choice == "3":
                break
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def _single_scene_streaming(self):
        """Single scene with full streaming output"""
        print("\n📝 SINGLE SCENE WITH STREAMING")
        print("="*50)
        
        # Select scene
        print("Select a scene:")
        for i, scene in enumerate(self.scenes, 1):
            preview = scene[:50] + "..." if len(scene) > 50 else scene
            print(f"{i}. {preview}")
        
        print(f"{len(self.scenes) + 1}. Enter custom scene")
        
        try:
            choice = int(input(f"Select (1-{len(self.scenes) + 1}): "))
            if 1 <= choice <= len(self.scenes):
                scene_prompt = self.scenes[choice - 1]
            elif choice == len(self.scenes) + 1:
                scene_prompt = input("Enter scene prompt: ").strip()
                if not scene_prompt:
                    return
            else:
                return
        except ValueError:
            return
        
        # Select style
        print("\nSelect writing style:")
        styles = list(self.styles.items())
        for i, (key, style) in enumerate(styles, 1):
            print(f"{i}. {style['name']} - {style['description']}")
        
        try:
            choice = int(input(f"Select style (1-{len(styles)}): "))
            if 1 <= choice <= len(styles):
                style_key, style = styles[choice - 1]
            else:
                return
        except ValueError:
            return
        
        # Run with streaming
        self._run_streaming_generation(scene_prompt, style, f"Single_{style['name']}")
    
    def _compare_styles(self):
        """Compare multiple styles with the same scene"""
        print("\n⚡ COMPARE WRITING STYLES")
        print("="*40)
        
        # Use first scene for simplicity
        scene_prompt = self.scenes[0]
        print(f"Using scene: {scene_prompt[:60]}...")
        
        print(f"\nTesting {len(self.styles)} different writing styles:")
        for style in self.styles.values():
            print(f"  • {style['name']}")
        
        print("\nStreaming mode:")
        print("1. Full streaming (see text as generated)")
        print("2. Results only (faster)")
        
        try:
            stream_choice = int(input("Select mode (1-2): "))
            full_streaming = (stream_choice == 1)
        except ValueError:
            full_streaming = True
        
        confirm = input("\nRun style comparison? (y/n): ").strip().lower()
        if confirm != 'y':
            return
        
        # Run comparison
        session_folder = self.model_tester.create_session_folder("style_comparison")
        
        for i, (style_key, style) in enumerate(self.styles.items(), 1):
            print(f"\n🎭 Style {i}/{len(self.styles)}: {style['name']}")
            print("="*50)
            
            if full_streaming:
                print("🤖 STREAMING OUTPUT:")
                print("-" * 30)
                
                def stream_callback(content, full_response):
                    print(content, end='', flush=True)
            else:
                print("🔄 Generating...", end='', flush=True)
                stream_callback = None
            
            # Build system prompt
            system_prompt = f"You are a skilled creative writer. {style['system_addition']}"
            
            # Run generation
            result = self.model_tester.stream_ollama_request(
                system_prompt,
                scene_prompt,
                self.model_tester.test_config,
                stream_callback
            )
            
            if full_streaming:
                print("\n" + "-" * 30)
            else:
                print(" Done!")
            
            # Show result
            if result['success']:
                word_count = len(result['response'].split())
                wpm = (word_count / result['generation_time']) * 60 if result['generation_time'] > 0 else 0
                print(f"✅ {style['name']}: {result['generation_time']:.2f}s, {word_count} words, {wpm:.0f} WPM")
            else:
                print(f"❌ {style['name']}: Failed")
            
            # Save result
            test_info = {
                'model': self.model_tester.test_config['model'],
                'test_type': 'style_comparison',
                'template_name': f"Compare_{style['name']}",
                'system_prompt': system_prompt,
                'user_prompt': scene_prompt,
                'style': style_key
            }
            
            self.model_tester.save_test_result(result, test_info, session_folder)
        
        print(f"\n📁 Comparison saved to: {os.path.basename(session_folder)}")
        input("Press Enter to continue...")
    
    def _run_streaming_generation(self, scene_prompt: str, style: Dict, name: str):
        """Run generation with full streaming output and stats"""
        print(f"\n🎬 GENERATING: {style['name']}")
        print("="*60)
        print(f"Style: {style['description']}")
        print(f"Scene: {scene_prompt[:60]}{'...' if len(scene_prompt) > 60 else ''}")
        
        print(f"\n🤖 STREAMING OUTPUT FROM OLLAMA:")
        print("="*60)
        
        # Track performance during streaming
        start_time = datetime.datetime.now()
        word_count = 0
        last_update = start_time
        
        def stream_callback(content, full_response):
            nonlocal word_count, last_update
            
            # Print content as it comes
            print(content, end='', flush=True)
            
            # Show progress every 3 seconds
            now = datetime.datetime.now()
            if (now - last_update).total_seconds() >= 3:
                word_count = len(full_response.split())
                elapsed = (now - start_time).total_seconds()
                wpm = (word_count / elapsed) * 60 if elapsed > 0 else 0
                print(f"\n[📊 {word_count} words, {wpm:.0f} WPM, {elapsed:.0f}s]", end='', flush=True)
                last_update = now
        
        # Build system prompt
        system_prompt = f"You are a skilled creative writer. {style['system_addition']}"
        
        # Create session folder
        session_folder = self.model_tester.create_session_folder("single_streaming")
        
        # Run generation
        result = self.model_tester.stream_ollama_request(
            system_prompt,
            scene_prompt,
            self.model_tester.test_config,
            stream_callback
        )
        
        print("\n" + "="*60)
        
        # Show final stats
        if result['success']:
            final_words = result['word_count']
            final_tokens = result['token_count']
            estimated_tokens = result.get('estimated_tokens', 0)
            elapsed = result['generation_time']
            wpm = (final_words / elapsed) * 60 if elapsed > 0 else 0
            tpm = (final_tokens / elapsed) * 60 if elapsed > 0 else 0
            
            print(f"✅ GENERATION COMPLETED!")
            print(f"📊 Style: {style['name']}")
            print(f"⏱️  Total Time: {elapsed:.2f} seconds")
            print(f"📝 Words: {final_words:,} ({wpm:.0f} WPM)")
            
            # Show token info with estimation note if needed
            if final_tokens == estimated_tokens:
                print(f"� Tokens: ~{final_tokens:,} (estimated, {tpm:.0f} TPM)")
            else:
                print(f"🔢 Tokens: {final_tokens:,} ({tpm:.0f} TPM)")
        else:
            print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        
        # Save result
        test_info = {
            'model': self.model_tester.test_config['model'],
            'test_type': 'single_streaming',
            'template_name': name,
            'system_prompt': system_prompt,
            'user_prompt': scene_prompt,
            'style': style['name']
        }
        
        filepath = self.model_tester.save_test_result(result, test_info, session_folder)
        print(f"💾 Saved to: {os.path.basename(filepath)}")
        
        input("\nPress Enter to continue...")
    
    def _select_model(self):
        """Select model"""
        models = self.model_tester.get_available_models()
        if not models:
            print("❌ No models found")
            return False
        
        print("\n🤖 SELECT MODEL:")
        for i, model in enumerate(models, 1):
            print(f"{i}. {model}")
        
        try:
            choice = int(input(f"Select (1-{len(models)}): "))
            if 1 <= choice <= len(models):
                self.model_tester.test_config['model'] = models[choice - 1]
                return True
        except ValueError:
            pass
        return False
