import os
import glob
import time
import shutil
from datetime import datetime

# Move the imports inside a try-catch block
try:
    from gradio_client import Client, handle_file
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False
    Client = None
    handle_file = None

class F5TTSHandler:
    def __init__(self, audio_folder="multiscene/audio"):  # Updated parameter name for clarity
        if not GRADIO_AVAILABLE:
            raise ImportError("F5-TTS requires: pip install gradio-client==1.11.0 huggingface-hub==0.34.2")
            
        # Fix: Set up proper folder paths
        self.audio_folder = audio_folder  # Where audio files will be saved
        self.story_search_folders = [      # Where to search for story files
            "multiscene/stories",
            "laboratory/scenes"
        ]
        
        # F5-TTS settings
        self.f5tts_server_url = "http://127.0.0.1:7860"
        self.f5tts_selected_ref = None
        self.f5tts_ref_text = ""
        self.f5tts_remove_silence = False
        self.f5tts_cross_fade = 0.15
        self.f5tts_nfe = 16
        self.f5tts_speed = 1.0
        self.selected_story_file = None
        self.selected_story_path = None  # Track full path of selected file
        
        # Timing data for estimation
        self.tts_timing_data = []
        self.tts_processed_count = 0
        
        # Create audio folder
        os.makedirs(self.audio_folder, exist_ok=True)
    
    def get_available_stories(self):
        """Get list of available story files from multiple folders"""
        all_stories = []
        
        for folder in self.story_search_folders:
            if os.path.exists(folder):
                story_files = glob.glob(os.path.join(folder, "*.txt"))
                for story_file in story_files:
                    # Create entry with both display name and full path
                    display_name = os.path.basename(story_file)
                    folder_name = os.path.basename(folder)
                    
                    all_stories.append({
                        'display_name': f"{display_name} ({folder_name})",
                        'file_path': story_file,
                        'folder': folder_name,
                        'basename': display_name
                    })
        
        # Sort by folder then by filename
        all_stories.sort(key=lambda x: (x['folder'], x['basename']))
        return all_stories
    
    def get_available_reference_audio(self):
        """Get list of available reference audio files with paired .txt files"""
        # Search in current directory and common audio folders
        search_paths = [".", "references", "audio", "voice_refs", "samples"]
    
        valid_pairs = []
        missing_txt_files = []
    
        for path in search_paths:
            if os.path.exists(path):
                # Find all .wav files
                wav_files = glob.glob(os.path.join(path, "*.wav"))
                
                for wav_file in wav_files:
                    # Check if corresponding .txt file exists
                    wav_basename = os.path.splitext(wav_file)[0]
                    txt_file = wav_basename + ".txt"
                    
                    if os.path.exists(txt_file):
                        # Valid pair found
                        valid_pairs.append({
                            'wav': os.path.relpath(wav_file),
                            'txt': os.path.relpath(txt_file),
                            'basename': os.path.basename(wav_basename)
                        })
                    else:
                        # .wav file without corresponding .txt
                        missing_txt_files.append(os.path.relpath(wav_file))
    
        return valid_pairs, missing_txt_files
    
    def display_f5tts_menu(self):
        """Display F5-TTS configuration menu"""
        print("\n" + "="*60)
        print("F5-TTS AUDIO GENERATION")
        print("="*60)
        
        # Show current settings
        print(f"1. Server URL: {self.f5tts_server_url}")
        print(f"2. F5-TTS reference audio: {self.f5tts_selected_ref or 'None selected'}")
        print(f"3. Remove silence: {self.f5tts_remove_silence}")
        print(f"4. Cross-fade: {self.f5tts_cross_fade}")
        print(f"5. NFE value: {self.f5tts_nfe}")
        print(f"6. Speed: {self.f5tts_speed}")
        print(f"7. Chosen text file: {self.selected_story_file or 'None selected'}")
        print("8. Generate Audio File")
        print("9. Back to main menu")
        
        print("\nSelect option (1-9): ", end="")
    
    def set_server_url(self):
        """Set F5-TTS server URL"""
        print(f"\nCurrent server URL: {self.f5tts_server_url}")
        new_url = input("Enter new server URL (or press Enter to keep current): ").strip()
        
        if new_url:
            # Ensure URL format is correct
            if not new_url.startswith("http"):
                new_url = "http://" + new_url
            self.f5tts_server_url = new_url
            print(f"✓ Server URL set to: {self.f5tts_server_url}")
        else:
            print("✓ Keeping current server URL")
        
        input("Press Enter to continue...")
    
    def select_reference_audio(self):
        """Select reference audio file with automatic .txt pairing"""
        try:
            valid_pairs, missing_txt_files = self.get_available_reference_audio()
            
            # Show missing .txt files if any
            if missing_txt_files:
                print("\n⚠️  WARNING: Found .wav files without corresponding .txt files:")
                for wav_file in missing_txt_files:
                    txt_file = os.path.splitext(wav_file)[0] + ".txt"
                    print(f"   - {wav_file} (missing {txt_file})")
                print()
            
            if not valid_pairs:
                print("\n❌ No valid reference audio files found!")
                print("\nTo use F5-TTS, you need paired files:")
                print("- audio_name.wav (the reference audio)")
                print("- audio_name.txt (transcription of the audio)")
                print("\nPlace these files in one of these locations:")
                print("- Current directory")
                print("- ./references/")
                print("- ./audio/")
                print("- ./voice_refs/")
                print("- ./samples/")
                
                if missing_txt_files:
                    print(f"\n💡 Found {len(missing_txt_files)} .wav files that need .txt transcriptions")
                
                input("Press Enter to continue...")
                return
            
            print(f"\nAvailable reference audio pairs ({len(valid_pairs)} found):")
            print("-" * 70)
            print("   Audio File                    Text File                    Size")
            print("-" * 70)
            
            for i, pair in enumerate(valid_pairs, 1):
                try:
                    # Get file sizes
                    wav_size = os.path.getsize(pair['wav']) / (1024 * 1024)  # MB
                    txt_size = os.path.getsize(pair['txt'])  # bytes
                    
                    wav_name = os.path.basename(pair['wav'])
                    txt_name = os.path.basename(pair['txt'])
                    
                    print(f"{i:2d}. {wav_name:<25} {txt_name:<25} ({wav_size:.1f}MB)")
                    
                    # Show a preview of the text content
                    try:
                        with open(pair['txt'], 'r', encoding='utf-8') as f:
                            text_preview = f.read().strip()[:60]
                            if len(text_preview) > 0:
                                print(f"    Text preview: {text_preview}{'...' if len(text_preview) == 60 else ''}")
                            else:
                                print(f"    ⚠️  Text file is empty!")
                    except Exception as e:
                        print(f"    ❌ Error reading text file: {e}")
                    
                except Exception as e:
                    print(f"{i:2d}. {pair['basename']} (Error reading file info)")
            
            try:
                choice = int(input(f"\nSelect reference audio pair (1-{len(valid_pairs)}): "))
                if 1 <= choice <= len(valid_pairs):
                    selected_pair = valid_pairs[choice - 1]
                    self.f5tts_selected_ref = selected_pair['wav']
                    
                    # Load the reference text automatically
                    try:
                        with open(selected_pair['txt'], 'r', encoding='utf-8') as f:
                            self.f5tts_ref_text = f.read().strip()
                        
                        print(f"✓ Selected audio: {self.f5tts_selected_ref}")
                        print(f"✓ Loaded reference text ({len(self.f5tts_ref_text)} characters)")
                        
                        if len(self.f5tts_ref_text) > 200:
                            print(f"   Preview: {self.f5tts_ref_text[:200]}...")
                        else:
                            print(f"   Text: {self.f5tts_ref_text}")
                            
                        if not self.f5tts_ref_text:
                            print("⚠️  Warning: Reference text file is empty!")
                            
                    except Exception as e:
                        print(f"❌ Error loading reference text: {e}")
                        self.f5tts_ref_text = ""
                        
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Invalid input.")
        
        except Exception as e:
            print(f"❌ Error in reference audio selection: {e}")
    
        input("Press Enter to continue...")
    
    def set_remove_silence(self):
        """Toggle remove silence setting"""
        print(f"\nCurrent setting: {self.f5tts_remove_silence}")
        print("1. Enable remove silence")
        print("2. Disable remove silence")
        print("3. Keep current setting")
        
        try:
            choice = input("Select (1-3): ").strip()
            if choice == "1":
                self.f5tts_remove_silence = True
                print("✓ Remove silence enabled")
            elif choice == "2":
                self.f5tts_remove_silence = False
                print("✓ Remove silence disabled")
            elif choice == "3":
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def set_cross_fade(self):
        """Set cross-fade value"""
        print(f"\nCurrent cross-fade: {self.f5tts_cross_fade}")
        print("Cross-fade controls smooth transitions between audio segments.")
        print("Range: 0.0 (no cross-fade) to 1.0 (maximum cross-fade)")
        print("Recommended: 0.15 for natural speech")
        
        try:
            value = input("Enter cross-fade value (0.0-1.0, or press Enter to keep current): ").strip()
            if value:
                fade_value = float(value)
                if 0.0 <= fade_value <= 1.0:
                    self.f5tts_cross_fade = fade_value
                    print(f"✓ Cross-fade set to: {self.f5tts_cross_fade}")
                else:
                    print("❌ Cross-fade must be between 0.0 and 1.0")
            else:
                print("✓ Keeping current cross-fade")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def set_nfe_value(self):
        """Set NFE (Neural Flow Estimation) value"""
        print(f"\nCurrent NFE value: {self.f5tts_nfe}")
        print("NFE controls generation quality vs speed trade-off.")
        print("Lower values = faster generation, potentially lower quality")
        print("Higher values = slower generation, potentially higher quality")
        print("Recommended range: 8-32, default: 16")
        
        try:
            value = input("Enter NFE value (1-64, or press Enter to keep current): ").strip()
            if value:
                nfe_value = int(value)
                if 1 <= nfe_value <= 64:
                    self.f5tts_nfe = nfe_value
                    print(f"✓ NFE value set to: {self.f5tts_nfe}")
                else:
                    print("❌ NFE value must be between 1 and 64")
            else:
                print("✓ Keeping current NFE value")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def set_speed(self):
        """Set playback speed"""
        print(f"\nCurrent speed: {self.f5tts_speed}")
        print("Speed controls how fast the generated speech will be.")
        print("1.0 = normal speed")
        print("0.5 = half speed (slower)")
        print("2.0 = double speed (faster)")
        print("Recommended range: 0.5-2.0")
        
        try:
            value = input("Enter speed value (0.1-3.0, or press Enter to keep current): ").strip()
            if value:
                speed_value = float(value)
                if 0.1 <= speed_value <= 3.0:
                    self.f5tts_speed = speed_value
                    print(f"✓ Speed set to: {self.f5tts_speed}")
                else:
                    print("❌ Speed must be between 0.1 and 3.0")
            else:
                print("✓ Keeping current speed")
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def select_story_file(self):
        """Select a story file to convert to audio from multiple folders"""
        stories = self.get_available_stories()
        
        if not stories:
            print(f"\nNo stories found in any of these folders:")
            for folder in self.story_search_folders:
                print(f"  - {folder}/")
            print("Generate some stories first before creating audio files.")
            input("Press Enter to continue...")
            return
        
        print(f"\nAvailable stories ({len(stories)} found):")
        print("-" * 80)
        print("   Story File                                    Folder        Size      Date")
        print("-" * 80)
        
        # Display stories with size and date info
        for i, story_info in enumerate(stories, 1):
            story_path = story_info['file_path']
            try:
                file_size = os.path.getsize(story_path)
                size_kb = file_size / 1024
                mod_time = os.path.getmtime(story_path)
                date_str = time.strftime('%Y-%m-%d %H:%M', time.localtime(mod_time))
                
                # Format display with proper spacing
                filename = story_info['basename'][:40]  # Limit filename length
                folder = story_info['folder'][:12]       # Limit folder length
                
                print(f"{i:2d}. {filename:<40} {folder:<12} {size_kb:>6.1f}KB {date_str}")
            except Exception as e:
                print(f"{i:2d}. {story_info['display_name']:<40} (Error reading file info)")
        
        try:
            choice = int(input(f"\nSelect story file (1-{len(stories)}): "))
            if 1 <= choice <= len(stories):
                selected_story = stories[choice - 1]
                self.selected_story_file = selected_story['basename']  # Just the filename
                self.selected_story_path = selected_story['file_path']  # Full path
                print(f"✓ Selected: {selected_story['display_name']}")
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Invalid input.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("Press Enter to continue...")
    
    def generate_audio_file(self):
        """Generate audio file from selected story"""
        # Validate requirements
        if not self.selected_story_file or not self.selected_story_path:
            print("❌ Please select a story file first.")
            input("Press Enter to continue...")
            return
        
        if not self.f5tts_selected_ref:
            print("❌ Please select a reference audio file first.")
            input("Press Enter to continue...")
            return
        
        if not self.f5tts_ref_text:
            print("❌ No reference text loaded. Please select a valid reference audio pair.")
            input("Press Enter to continue...")
            return
        
        # Read story content using the full path
        try:
            with open(self.selected_story_path, 'r', encoding='utf-8') as file:
                story_content = file.read().strip()
        except Exception as e:
            print(f"❌ Error reading story file: {e}")
            input("Press Enter to continue...")
            return
        
        if not story_content:
            print("❌ Story file is empty.")
            input("Press Enter to continue...")
            return
        
        print(f"\n🎵 Generating audio for: {self.selected_story_file}")
        print(f"📁 Story location: {self.selected_story_path}")
        print(f"📁 Reference audio: {self.f5tts_selected_ref}")
        print(f"📝 Reference text loaded: {len(self.f5tts_ref_text)} characters")
        print(f"🌐 Server: {self.f5tts_server_url}")
        print("-" * 50)
        
        # Generate output filename with new naming convention
        story_name = os.path.splitext(self.selected_story_file)[0]  # Remove .txt extension
        
        # Limit story name to 30 characters
        if len(story_name) > 30:
            story_name = story_name[:30]
        
        # Get reference audio basename (without path and extension)
        ref_audio_basename = os.path.splitext(os.path.basename(self.f5tts_selected_ref))[0]
        
        # Create base filename: storyname.referencename.wav
        base_filename = f"{story_name}.{ref_audio_basename}.wav"
        output_path = os.path.join(self.audio_folder, base_filename)
        
        # Check if file exists and add .01, .02, etc. if needed
        counter = 1
        while os.path.exists(output_path):
            numbered_filename = f"{story_name}.{ref_audio_basename}.{counter:02d}.wav"
            output_path = os.path.join(self.audio_folder, numbered_filename)
            counter += 1
            
            # Safety check to prevent infinite loop
            if counter > 99:
                print("❌ Too many existing audio files with similar names!")
                input("Press Enter to continue...")
                return
        
        final_filename = os.path.basename(output_path)
        print(f"🎧 Output filename: {final_filename}")
        print(f"🎧 Full path: {output_path}")
        print("⏳ This may take several minutes for long stories...")
        
        # Call F5-TTS API
        success = self._call_f5tts_api(story_content, output_path)
        
        if success:
            print(f"✅ Audio generation completed successfully!")
            print(f"📁 Saved to: {output_path}")
        else:
            print(f"❌ Audio generation failed.")
        
        input("Press Enter to continue...")
    
    def _call_f5tts_api(self, text_content, output_path):
        """
        Call F5-TTS API to generate audio using gradio client
        """
        try:
            # Count words and characters for timing info
            number_of_words = len(text_content.split())
            char_count = len(text_content)
            
            # Calculate estimated processing time based on historical data
            estimated_time = None
            if self.tts_timing_data:
                if len(self.tts_timing_data) >= 3:
                    # Calculate average time per character
                    total_chars = sum(item[0] for item in self.tts_timing_data)
                    total_time = sum(item[1] for item in self.tts_timing_data)
                    avg_time_per_char = total_time / total_chars
                    estimated_time = avg_time_per_char * char_count
                    print(f"📊 Estimated processing time: {estimated_time:.1f} seconds")
                else:
                    # Simple estimation based on most recent processing
                    recent_time_per_char = self.tts_timing_data[-1][1] / self.tts_timing_data[-1][0]
                    estimated_time = recent_time_per_char * char_count
                    print(f"📊 Estimated processing time: {estimated_time:.1f} seconds")
            else:
                print("📊 First time processing - will establish timing baseline")
            
            # Determine if we should recalibrate timing
            should_recalibrate = (char_count >= 3000 and char_count <= 4000) or not self.tts_timing_data
            if should_recalibrate:
                print("🔧 Character count in calibration range - will update timing model")
            
            print(f"📝 Processing {number_of_words} words ({char_count:,} characters)")
            
            start_time = time.time()
            
            # Create Gradio client
            client = Client(self.f5tts_server_url)
            
            # Call F5-TTS API
            result = client.predict(
                ref_audio_input=handle_file(self.f5tts_selected_ref),
                ref_text_input=self.f5tts_ref_text,
                gen_text_input=text_content,
                remove_silence=self.f5tts_remove_silence,
                cross_fade_duration_slider=float(self.f5tts_cross_fade),
                nfe_slider=int(self.f5tts_nfe),
                speed_slider=float(self.f5tts_speed),
                api_name="/basic_tts",
            )
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Update timing data
            if should_recalibrate:
                self.tts_timing_data.append((char_count, elapsed_time))
                # Keep only the last 5 timing data points
                if len(self.tts_timing_data) > 5:
                    self.tts_timing_data.pop(0)
            
            self.tts_processed_count += 1
            
            print(f"⏱️  Processing completed in {elapsed_time:.1f} seconds")
            
            if estimated_time is not None:
                error_percentage = abs(estimated_time - elapsed_time) / elapsed_time * 100
                print(f"📊 Estimation accuracy: {100 - error_percentage:.1f}%")
            
            # Get the generated audio file path
            source_audio_path = result[0]
            
            if not os.path.exists(source_audio_path):
                print(f"❌ Generated audio file not found: {source_audio_path}")
                return False
            
            # Copy the file to our desired location
            try:
                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Copy the generated audio file
                shutil.copy2(source_audio_path, output_path)
                
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                    print(f"💾 Audio file saved successfully ({file_size:.1f}MB)")
                    return True
                else:
                    print(f"❌ Failed to save audio file to: {output_path}")
                    return False
                    
            except Exception as copy_error:
                print(f"❌ Error copying audio file: {copy_error}")
                return False
            
        except Exception as e:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"❌ F5-TTS processing failed after {elapsed_time:.1f} seconds")
            print(f"❌ Error: {e}")
            print("❌ Make sure F5-TTS is installed and running on the specified server URL")
            return False
    
    def run_f5tts_menu(self):
        """Run the F5-TTS menu loop"""
        while True:
            self.display_f5tts_menu()
            
            try:
                choice = input().strip()
                
                if choice == "1":
                    self.set_server_url()
                elif choice == "2":
                    self.select_reference_audio()
                elif choice == "3":
                    self.set_remove_silence()
                elif choice == "4":
                    self.set_cross_fade()
                elif choice == "5":
                    self.set_nfe_value()
                elif choice == "6":
                    self.set_speed()
                elif choice == "7":
                    self.select_story_file()
                elif choice == "8":
                    self.generate_audio_file()
                elif choice == "9":
                    break
                else:
                    print("❌ Invalid option. Please select 1-9.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")