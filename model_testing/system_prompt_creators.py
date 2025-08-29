from .comprehensive_detective_prompts import DETECTIVE_STYLES, build_comprehensive_prompt
from .comprehensive_fantasy_prompts import FANTASY_STYLES, build_fantasy_prompt
from .comprehensive_scifi_prompts import SCIFI_STYLES, build_scifi_prompt
from .comprehensive_romance_prompts import ROMANCE_STYLES, build_romance_prompt
from .ai_scene_prompt_creator import AIScenePromptCreator

class SystemPromptCreators:
    def __init__(self, template_manager):
        self.template_manager = template_manager
        # Initialize the AI creator
        self.ai_creator = AIScenePromptCreator(template_manager)
        self.content_type = "scene"
    
    def create_ai_generated_prompt(self):
        """Use AI to create comprehensive system prompts"""
        self.ai_creator.create_ai_generated_comprehensive_prompt()
        
    def create_comprehensive_scifi_prompt(self):
        """Create comprehensive sci-fi scene system prompts"""
        print(f"\n{'='*70}")
        print("COMPREHENSIVE SCI-FI SCENE TECHNIQUES")
        print(f"{'='*70}")
        print("Create detailed sci-fi system prompts with futuristic technology techniques.")
        print("Choose your sci-fi style and customize the technological elements to include.")
        print()
    
        print("🚀 SCI-FI STYLES AVAILABLE:")
        print("-" * 60)
        styles = list(SCIFI_STYLES.keys())
        for i, style in enumerate(styles, 1):
            info = SCIFI_STYLES[style]
            print(f"{i}. {style}")
            print(f"   └─ {info['description']}")
            print()
    
        try:
            style_choice = int(input(f"Select sci-fi style (1-{len(styles)}): "))
            if not (1 <= style_choice <= len(styles)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
        
            selected_style = styles[style_choice - 1]
            style_data = SCIFI_STYLES[selected_style]
        
            print(f"\n🎯 SELECTED: {selected_style.upper()}")
            print("=" * 60)
            print(style_data['description'])
            print(f"Tone: {style_data['tone']}")
            print()
        
            # Show techniques
            print("📚 AVAILABLE SCI-FI TECHNIQUES:")
            print("-" * 40)
            for i, technique in enumerate(style_data['techniques'], 1):
                print(f"{i}. {technique}")
        
            print(f"\n🔬 SCI-FI ELEMENTS INCLUDED:")
            print(f"{', '.join(style_data['elements'])}")
        
            # Technology level customization
            print(f"\n🛸 TECHNOLOGY LEVEL:")
            print("1. Near Future (20-50 years from now)")
            print("2. Advanced (plausible but advanced technology)")
            print("3. Far Future (highly advanced, speculative technology)")
        
            tech_choice = int(input("Select technology level (1-3): "))
            tech_levels = ["near_future", "advanced", "far_future"]
            tech_level = tech_levels[tech_choice - 1] if 1 <= tech_choice <= 3 else "advanced"
        
            # Additional customization options
            print(f"\n⚙️  PROMPT CUSTOMIZATION:")
            print("1. Use all techniques (full comprehensive prompt)")
            print("2. Select specific techniques to include")
            print("3. Add word count requirement")
            print("4. Add custom sci-fi elements")
        
            custom_choice = int(input("Select customization option (1-4): "))
        
            selected_techniques = style_data['techniques']
            word_count = None
            additional_elements = []
        
            if custom_choice == 2:
                print("\nSelect techniques to include (enter numbers separated by commas):")
                technique_input = input(f"Techniques 1-{len(style_data['techniques'])}: ").strip()
                try:
                    technique_indices = [int(x.strip()) - 1 for x in technique_input.split(',')]
                    selected_techniques = [style_data['techniques'][i] for i in technique_indices 
                                     if 0 <= i < len(style_data['techniques'])]
                except:
                    print("Invalid input, using all techniques")
        
            if custom_choice >= 3:
                word_input = input("Target word count (or press Enter to skip): ").strip()
                if word_input.isdigit():
                    word_count = int(word_input)
        
            if custom_choice == 4:
                custom_elements = input("Additional sci-fi elements (comma-separated): ").strip()
                if custom_elements:
                    additional_elements = [elem.strip() for elem in custom_elements.split(',')]
        
            # Build the comprehensive sci-fi prompt
            comprehensive_prompt = build_scifi_prompt(
                style_data, 
                selected_techniques, 
                word_count, 
                additional_elements,
                tech_level
            )
        
            # Show preview
            print(f"\n📋 COMPREHENSIVE SCI-FI PROMPT PREVIEW:")
            print("=" * 60)
            preview = comprehensive_prompt[:400] + "..." if len(comprehensive_prompt) > 400 else comprehensive_prompt
            print(preview)
            print("=" * 60)
            print(f"Full prompt: {len(comprehensive_prompt.split())} words")
            print(f"Technology Level: {tech_level.replace('_', ' ').title()}")
        
            # Save option
            save_choice = input("\nSave this comprehensive sci-fi prompt? (y/n): ").strip().lower()
            if save_choice == 'y':
                safe_style = selected_style.replace(" ", "_").replace("&", "and").lower()
                template_name = f"scifi_{safe_style}_{tech_level}"
            
                if self.template_manager.save_system_prompt_template(template_name, comprehensive_prompt):
                    print(f"\n✅ Comprehensive sci-fi prompt saved!")
                    print(f"📁 Filename: system_prompt_{self.template_manager.content_type}_{template_name}.txt")
                    print(f"🎯 Style: {selected_style}")
                    print(f"🛸 Tech Level: {tech_level.replace('_', ' ').title()}")
                    print(f"📝 Techniques: {len(selected_techniques)} included")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")


    def create_custom_system_prompt(self):
        """Create custom system prompt and save as template"""
        content_label = self.content_type.capitalize() if self.content_type else "System"
        
        print(f"\n{'='*60}")
        print(f"CREATE CUSTOM {content_label.upper()} SYSTEM PROMPT")
        print(f"{'='*60}")
        print("Enter your system prompt content (press Enter on empty line to finish):")
        print("This defines the AI's role, behavior, and writing style.")
        print()
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        if not lines:
            print("No content entered.")
            input("Press Enter to continue...")
            return
        
        content = '\n'.join(lines)
        
        # Get template name
        print(f"\nPreview ({len(content.split())} words):")
        print("-" * 40)
        print(content[:200] + "..." if len(content) > 200 else content)
        print("-" * 40)
        
        name = input("\nEnter template name (e.g., 'creative_writer', 'detective_noir'): ").strip()
        if not name:
            print("No name provided. Template not saved.")
            input("Press Enter to continue...")
            return
        
        # Save template
        if self.template_manager.save_system_prompt_template(name, content):
            print(f"Template can now be used in Scene Workshop!")
        
        input("Press Enter to continue...")


    def create_comprehensive_romance_prompt(self):
        """Create comprehensive romance scene system prompts"""
        print(f"\n{'='*70}")
        print("COMPREHENSIVE ROMANCE SCENE TECHNIQUES")
        print(f"{'='*70}")
        print("Create detailed romance system prompts with relationship development techniques.")
        print("Choose your romance style and customize the romantic elements to include.")
        print()
    
        print("💖 ROMANCE STYLES AVAILABLE:")
        print("-" * 60)
        styles = list(ROMANCE_STYLES.keys())
        for i, style in enumerate(styles, 1):
            info = ROMANCE_STYLES[style]
            print(f"{i}. {style}")
            print(f"   └─ {info['description']}")
            print()
    
        try:
            style_choice = int(input(f"Select romance style (1-{len(styles)}): "))
            if not (1 <= style_choice <= len(styles)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
        
            selected_style = styles[style_choice - 1]
            style_data = ROMANCE_STYLES[selected_style]
            
            print(f"\n🎯 SELECTED: {selected_style.upper()}")
            print("=" * 60)
            print(style_data['description'])
            print(f"Tone: {style_data['tone']}")
            print()
            
            # Show techniques
            print("📚 AVAILABLE ROMANCE TECHNIQUES:")
            print("-" * 40)
            for i, technique in enumerate(style_data['techniques'], 1):
                print(f"{i}. {technique}")
        
            print(f"\n💕 ROMANCE ELEMENTS INCLUDED:")
            print(f"{', '.join(style_data['elements'])}")
        
            # Heat level customization
            print(f"\n🔥 ROMANCE INTENSITY LEVEL:")
            print("1. Sweet (emotional intimacy, tender moments, minimal physical)")
            print("2. Moderate (balanced emotional and physical attraction)")
            print("3. Steamy (passionate attraction, sensual tension, intimate scenes)")
        
            heat_choice = int(input("Select romance intensity (1-3): "))
            heat_levels = ["sweet", "moderate", "steamy"]
            heat_level = heat_levels[heat_choice - 1] if 1 <= heat_choice <= 3 else "moderate"
        
            # Additional customization options
            print(f"\n⚙️  PROMPT CUSTOMIZATION:")
            print("1. Use all techniques (full comprehensive prompt)")
            print("2. Select specific techniques to include")
            print("3. Add word count requirement")
            print("4. Add custom romance elements")
        
            custom_choice = int(input("Select customization option (1-4): "))
        
            selected_techniques = style_data['techniques']
            word_count = None
            additional_elements = []
        
            if custom_choice == 2:
                print("\nSelect techniques to include (enter numbers separated by commas):")
                technique_input = input(f"Techniques 1-{len(style_data['techniques'])}: ").strip()
                try:
                    technique_indices = [int(x.strip()) - 1 for x in technique_input.split(',')]
                    selected_techniques = [style_data['techniques'][i] for i in technique_indices 
                                     if 0 <= i < len(style_data['techniques'])]
                except:
                    print("Invalid input, using all techniques")
        
            if custom_choice >= 3:
                word_input = input("Target word count (or press Enter to skip): ").strip()
                if word_input.isdigit():
                    word_count = int(word_input)
        
            if custom_choice == 4:
                custom_elements = input("Additional romance elements (comma-separated): ").strip()
                if custom_elements:
                    additional_elements = [elem.strip() for elem in custom_elements.split(',')]
        
            # Build the comprehensive romance prompt
            comprehensive_prompt = build_romance_prompt(
                style_data, 
                selected_techniques, 
                word_count, 
                additional_elements,
                heat_level
            )
        
            # Show preview
            print(f"\n📋 COMPREHENSIVE ROMANCE PROMPT PREVIEW:")
            print("=" * 60)
            preview = comprehensive_prompt[:400] + "..." if len(comprehensive_prompt) > 400 else comprehensive_prompt
            print(preview)
            print("=" * 60)
            print(f"Full prompt: {len(comprehensive_prompt.split())} words")
            print(f"Romance Level: {heat_level.title()}")
        
            # Save option
            save_choice = input("\nSave this comprehensive romance prompt? (y/n): ").strip().lower()
            if save_choice == 'y':
                safe_style = selected_style.replace(" ", "_").replace("&", "and").lower()
                template_name = f"romance_{safe_style}_{heat_level}"
            
                if self.template_manager.save_system_prompt_template(template_name, comprehensive_prompt):
                    print(f"\n✅ Comprehensive romance prompt saved!")
                    print(f"📁 Filename: system_prompt_{self.template_manager.content_type}_{template_name}.txt")
                    print(f"🎯 Style: {selected_style}")
                    print(f"💕 Romance Level: {heat_level.title()}")
                    print(f"📝 Techniques: {len(selected_techniques)} included")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")


    def create_comprehensive_detective_prompt(self):
        """Create comprehensive detective scene system prompts"""
        print(f"\n{'='*70}")
        print("COMPREHENSIVE DETECTIVE SCENE TECHNIQUES")
        print(f"{'='*70}")
        print("Create detailed detective system prompts with professional techniques.")
        print("Choose your detective style and customize the techniques to include.")
        print()
        
        print("🔍 DETECTIVE STYLES AVAILABLE:")
        print("-" * 60)
        styles = list(DETECTIVE_STYLES.keys())
        for i, style in enumerate(styles, 1):
            info = DETECTIVE_STYLES[style]
            print(f"{i}. {style}")
            print(f"   └─ {info['description']}")
            print()
        
        try:
            style_choice = int(input(f"Select detective style (1-{len(styles)}): "))
            if not (1 <= style_choice <= len(styles)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
            
            selected_style = styles[style_choice - 1]
            style_data = DETECTIVE_STYLES[selected_style]
            
            print(f"\n🎯 SELECTED: {selected_style.upper()}")
            print("=" * 60)
            print(style_data['description'])
            print(f"Tone: {style_data['tone']}")
            print()
            
            # Show techniques
            print("📚 AVAILABLE TECHNIQUES:")
            print("-" * 40)
            for i, technique in enumerate(style_data['techniques'], 1):
                print(f"{i}. {technique}")
            
            print(f"\n🔧 KEY ELEMENTS INCLUDED:")
            print(f"{', '.join(style_data['elements'])}")
            
            # Customization options
            print(f"\n⚙️  PROMPT CUSTOMIZATION:")
            print("1. Use all techniques (full comprehensive prompt)")
            print("2. Select specific techniques to include")
            print("3. Add word count requirement")
            print("4. Add custom elements")
            
            custom_choice = int(input("Select customization option (1-4): "))
            
            selected_techniques = style_data['techniques']
            word_count = None
            additional_elements = []
            
            if custom_choice == 2:
                print("\nSelect techniques to include (enter numbers separated by commas):")
                technique_input = input(f"Techniques 1-{len(style_data['techniques'])}: ").strip()
                try:
                    technique_indices = [int(x.strip()) - 1 for x in technique_input.split(',')]
                    selected_techniques = [style_data['techniques'][i] for i in technique_indices 
                                           if 0 <= i < len(style_data['techniques'])]
                except:
                    print("Invalid input, using all techniques")
            
            if custom_choice >= 3:
                word_input = input("Target word count (or press Enter to skip): ").strip()
                if word_input.isdigit():
                    word_count = int(word_input)
            
            if custom_choice == 4:
                custom_elements = input("Additional elements (comma-separated): ").strip()
                if custom_elements:
                    additional_elements = [elem.strip() for elem in custom_elements.split(',')]
            
            # Build the comprehensive prompt
            comprehensive_prompt = build_comprehensive_prompt(
                style_data, 
                selected_techniques, 
                word_count, 
                additional_elements
            )
            
            # Show preview
            print(f"\n📋 COMPREHENSIVE PROMPT PREVIEW:")
            print("=" * 60)
            preview = comprehensive_prompt[:400] + "..." if len(comprehensive_prompt) > 400 else comprehensive_prompt
            print(preview)
            print("=" * 60)
            print(f"Full prompt: {len(comprehensive_prompt.split())} words")
            
            # Save option
            save_choice = input("\nSave this comprehensive detective prompt? (y/n): ").strip().lower()
            if save_choice == 'y':
                safe_style = selected_style.replace(" ", "_").replace("&", "and").lower()
                template_name = f"detective_{safe_style}_comprehensive"
                
                if self.template_manager.save_system_prompt_template(template_name, comprehensive_prompt):
                    print(f"\n✅ Comprehensive detective prompt saved!")
                    print(f"📁 Filename: system_prompt_{self.content_type}_{template_name}.txt")
                    print(f"🎯 Style: {selected_style}")
                    print(f"📝 Techniques: {len(selected_techniques)} included")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    

    def create_comprehensive_fantasy_prompt(self):
        """Create comprehensive fantasy scene system prompts"""
        print(f"\n{'='*70}")
        print("COMPREHENSIVE FANTASY SCENE TECHNIQUES")
        print(f"{'='*70}")
        print("Create detailed fantasy system prompts with professional techniques.")
        print("Choose your fantasy style and customize the techniques to include.")
        print()
        
        print("✨ FANTASY STYLES AVAILABLE:")
        print("-" * 60)
        styles = list(FANTASY_STYLES.keys())
        for i, style in enumerate(styles, 1):
            info = FANTASY_STYLES[style]
            print(f"{i}. {style}")
            print(f"   └─ {info['description']}")
            print()
        
        try:
            style_choice = int(input(f"Select fantasy style (1-{len(styles)}): "))
            if not (1 <= style_choice <= len(styles)):
                print("❌ Invalid choice.")
                input("Press Enter to continue...")
                return
            
            selected_style = styles[style_choice - 1]
            style_data = FANTASY_STYLES[selected_style]
            
            print(f"\n🎯 SELECTED: {selected_style.upper()}")
            print("=" * 60)
            print(style_data['description'])
            print(f"Tone: {style_data['tone']}")
            print()
            
            # Show techniques
            print("📚 AVAILABLE TECHNIQUES:")
            print("-" * 40)
            for i, technique in enumerate(style_data['techniques'], 1):
                print(f"{i}. {technique}")
            
            print(f"\n🔧 KEY ELEMENTS INCLUDED:")
            print(f"{', '.join(style_data['elements'])}")
            
            # Customization options
            print(f"\n⚙️  PROMPT CUSTOMIZATION:")
            print("1. Use all techniques (full comprehensive prompt)")
            print("2. Select specific techniques to include")
            print("3. Add word count requirement")
            print("4. Add custom elements")
            
            custom_choice = int(input("Select customization option (1-4): "))
            
            selected_techniques = style_data['techniques']
            word_count = None
            additional_elements = []
            
            if custom_choice == 2:
                print("\nSelect techniques to include (enter numbers separated by commas):")
                technique_input = input(f"Techniques 1-{len(style_data['techniques'])}: ").strip()
                try:
                    technique_indices = [int(x.strip()) - 1 for x in technique_input.split(',')]
                    selected_techniques = [style_data['techniques'][i] for i in technique_indices 
                                           if 0 <= i < len(style_data['techniques'])]
                except:
                    print("Invalid input, using all techniques")
            
            if custom_choice >= 3:
                word_input = input("Target word count (or press Enter to skip): ").strip()
                if word_input.isdigit():
                    word_count = int(word_input)
            
            if custom_choice == 4:
                custom_elements = input("Additional elements (comma-separated): ").strip()
                if custom_elements:
                    additional_elements = [elem.strip() for elem in custom_elements.split(',')]
            
            # Build the comprehensive prompt
            comprehensive_prompt = build_fantasy_prompt(
                style_data, 
                selected_techniques, 
                word_count, 
                additional_elements
            )
            
            # Show preview
            print(f"\n📋 COMPREHENSIVE PROMPT PREVIEW:")
            print("=" * 60)
            preview = comprehensive_prompt[:400] + "..." if len(comprehensive_prompt) > 400 else comprehensive_prompt
            print(preview)
            print("=" * 60)
            print(f"Full prompt: {len(comprehensive_prompt.split())} words")
            
            # Save option
            save_choice = input("\nSave this comprehensive fantasy prompt? (y/n): ").strip().lower()
            if save_choice == 'y':
                safe_style = selected_style.replace(" ", "_").replace("&", "and").lower()
                template_name = f"fantasy_{safe_style}_comprehensive"
                
                if self.template_manager.save_system_prompt_template(template_name, comprehensive_prompt):
                    print(f"\n✅ Comprehensive fantasy prompt saved!")
                    print(f"📁 Filename: system_prompt_{self.content_type}_{template_name}.txt")
                    print(f"🎯 Style: {selected_style}")
                    print(f"📝 Techniques: {len(selected_techniques)} included")
        
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")