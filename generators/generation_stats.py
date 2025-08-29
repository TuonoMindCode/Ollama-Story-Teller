import time

class GenerationStats:
    def __init__(self):
        self.stats = {
            'total_scenes': 0,
            'completed_scenes': 0,
            'start_time': None,
            'scene_times': [],
            'total_words': 0,
            'total_characters': 0
        }
    
    def start_generation(self, total_scenes):
        """Initialize generation tracking"""
        self.stats['start_time'] = time.time()
        self.stats['total_scenes'] = total_scenes
        self.stats['completed_scenes'] = 0
        self.stats['scene_times'] = []
        self.stats['total_words'] = 0
        self.stats['total_characters'] = 0
    
    def complete_scene(self, scene_time, word_count, char_count):
        """Record completion of a scene"""
        self.stats['completed_scenes'] += 1
        self.stats['scene_times'].append(scene_time)
        self.stats['total_words'] += word_count
        self.stats['total_characters'] += char_count
    
    def show_progress(self):
        """Show current generation progress"""
        if self.stats['total_scenes'] == 0:
            return
            
        completed = self.stats['completed_scenes']
        total = self.stats['total_scenes']
        percentage = (completed / total) * 100
        
        # Create progress bar
        bar_length = 30
        filled_length = int(bar_length * completed // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Calculate time estimates
        if completed > 0 and self.stats['scene_times']:
            avg_time = sum(self.stats['scene_times']) / len(self.stats['scene_times'])
            remaining_scenes = total - completed
            estimated_time_left = avg_time * remaining_scenes
            
            elapsed_time = time.time() - self.stats['start_time']
            
            print(f"\n📊 Progress: [{bar}] {completed}/{total} ({percentage:.1f}%)")
            print(f"⏱️ Elapsed: {self._format_time(elapsed_time)} | Est. remaining: {self._format_time(estimated_time_left)}")
            print(f"📝 Total words so far: {self.stats['total_words']:,}")
        else:
            print(f"\n📊 Progress: [{bar}] {completed}/{total} ({percentage:.1f}%)")

    def show_scene_completion(self, scene_num, scene_time, word_count, char_count):
        """Show individual scene completion statistics"""
        print(f"   ✅ Scene {scene_num} completed:")
        print(f"      ⏱️ Time: {self._format_time(scene_time)}")
        print(f"      📝 Words: {word_count:,} | Characters: {char_count:,}")
        
        # Show speed stats
        if scene_time > 0:
            words_per_minute = (word_count / scene_time) * 60
            print(f"      🚀 Speed: {words_per_minute:.1f} words/minute")

    def show_final_stats(self, total_time):
        """Show final generation statistics"""
        print(f"\n🎉 STORY GENERATION COMPLETE!")
        print("="*50)
        print(f"⏱️ Total time: {self._format_time(total_time)}")
        print(f"📝 Total words: {self.stats['total_words']:,}")
        print(f"📄 Total characters: {self.stats['total_characters']:,}")
        print(f"🎬 Total scenes: {self.stats['total_scenes']}")
        
        if self.stats['scene_times']:
            avg_scene_time = sum(self.stats['scene_times']) / len(self.stats['scene_times'])
            fastest_scene = min(self.stats['scene_times'])
            slowest_scene = max(self.stats['scene_times'])
            
            print(f"⚡ Average scene time: {self._format_time(avg_scene_time)}")
            print(f"🏃 Fastest scene: {self._format_time(fastest_scene)}")
            print(f"🐌 Slowest scene: {self._format_time(slowest_scene)}")
            
            # Overall generation speed
            if total_time > 0:
                words_per_minute = (self.stats['total_words'] / total_time) * 60
                print(f"🚀 Overall speed: {words_per_minute:.1f} words/minute")

    def _format_time(self, seconds):
        """Format time in a readable way"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.1f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
