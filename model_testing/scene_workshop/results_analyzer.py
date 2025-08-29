import os
import json
from datetime import datetime

class ResultsAnalyzer:
    def __init__(self, workshop):
        self.workshop = workshop
    
    def analyze_recent_results(self):
        """Analyze recent generation results"""
        print("\nRESULTS ANALYSIS")
        print("="*40)
        
        # Get recent test results
        results = self._get_recent_results()
        
        if not results:
            print("No recent results found")
            print("Generate some scenes first!")
            input("Press Enter to continue...")
            return
        
        # Display analysis menu
        while True:
            print(f"\nFound {len(results)} recent results")
            print("="*30)
            print("1. View generation statistics")
            print("2. Compare parameter effects")
            print("3. Analyze word patterns")
            print("4. View best/worst results")
            print("5. Export results summary")
            print("6. Back to workshop")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                self._show_generation_stats(results)
            elif choice == "2":
                self._compare_parameter_effects(results)
            elif choice == "3":
                self._analyze_word_patterns(results)
            elif choice == "4":
                self._show_best_worst_results(results)
            elif choice == "5":
                self._export_results_summary(results)
            elif choice == "6":
                break
            else:
                print("Invalid option")
                input("Press Enter to continue...")
    
    def _get_recent_results(self):
        """Get recent workshop results"""
        try:
            results_folder = os.path.join(self.workshop.model_tester.results_folder, "session_results")
            if not os.path.exists(results_folder):
                return []
            
            results = []
            
            # Look through recent session folders
            for folder_name in sorted(os.listdir(results_folder), reverse=True)[:10]:  # Last 10 sessions
                if folder_name.startswith("scene_workshop"):
                    session_path = os.path.join(results_folder, folder_name)
                    
                    # Look for result files in this session
                    for file_name in os.listdir(session_path):
                        if file_name.endswith('.json'):
                            file_path = os.path.join(session_path, file_name)
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    result_data = json.load(f)
                                    
                                # Add session info
                                result_data['session_folder'] = folder_name
                                result_data['file_name'] = file_name
                                results.append(result_data)
                                
                            except Exception:
                                continue
            
            return results[:50]  # Limit to 50 most recent
            
        except Exception as e:
            print(f"Error reading results: {e}")
            return []
    
    def _show_generation_stats(self, results):
        """Show generation statistics"""
        print("\nGENERATION STATISTICS")
        print("="*40)
        
        if not results:
            print("No results to analyze")
            input("Press Enter to continue...")
            return
        
        # Calculate stats
        word_counts = []
        gen_times = []
        wpm_rates = []
        models_used = {}
        prompt_types = {}
        improvements = 0
        
        for result in results:
            test_info = result.get('test_info', {})
            response_info = result.get('response_info', {})
            
            # Word counts
            word_count = response_info.get('word_count', 0)
            if word_count > 0:
                word_counts.append(word_count)
            
            # Generation times
            gen_time = response_info.get('generation_time', 0)
            if gen_time > 0:
                gen_times.append(gen_time)
                
                # WPM calculation
                if word_count > 0:
                    wpm = (word_count / gen_time) * 60
                    wpm_rates.append(wpm)
            
            # Models used
            model = test_info.get('model', 'Unknown')
            models_used[model] = models_used.get(model, 0) + 1
            
            # Prompt types
            test_type = test_info.get('test_type', 'Unknown')
            prompt_types[test_type] = prompt_types.get(test_type, 0) + 1
            
            # Improvements
            if test_info.get('improvement_applied'):
                improvements += 1
        
        # Display stats
        print(f"Total results analyzed: {len(results)}")
        print(f"Results with improvements: {improvements}")
        print()
        
        if word_counts:
            print("WORD COUNT STATISTICS:")
            print(f"  Average: {sum(word_counts)/len(word_counts):.1f} words")
            print(f"  Range: {min(word_counts)} - {max(word_counts)} words")
            print(f"  Median: {sorted(word_counts)[len(word_counts)//2]} words")
            print()
        
        if gen_times:
            print("GENERATION TIME STATISTICS:")
            print(f"  Average: {sum(gen_times)/len(gen_times):.1f} seconds")
            print(f"  Range: {min(gen_times):.1f} - {max(gen_times):.1f} seconds")
            print()
        
        if wpm_rates:
            print("WORDS PER MINUTE STATISTICS:")
            print(f"  Average: {sum(wpm_rates)/len(wpm_rates):.0f} WPM")
            print(f"  Range: {min(wpm_rates):.0f} - {max(wpm_rates):.0f} WPM")
            print()
        
        if models_used:
            print("MODELS USED:")
            for model, count in models_used.items():
                print(f"  {model}: {count} generations")
            print()
        
        if prompt_types:
            print("GENERATION TYPES:")
            for ptype, count in prompt_types.items():
                display_type = ptype.replace('scene_workshop_', '').replace('_', ' ').title()
                print(f"  {display_type}: {count} generations")
        
        input("\nPress Enter to continue...")
    
    def _compare_parameter_effects(self, results):
        """Compare effects of different parameters"""
        print("\nPARAMETER EFFECTS COMPARISON")
        print("="*50)
        
        # Group results by parameter ranges
        temp_groups = {'low': [], 'med': [], 'high': []}
        top_p_groups = {'low': [], 'med': [], 'high': []}
        
        for result in results:
            test_info = result.get('test_info', {})
            params = test_info.get('parameters_used', {})
            response_info = result.get('response_info', {})
            
            temp = params.get('temperature', 0.8)
            top_p = params.get('top_p', 0.9)
            word_count = response_info.get('word_count', 0)
            gen_time = response_info.get('generation_time', 1)
            
            if word_count > 0 and gen_time > 0:
                wpm = (word_count / gen_time) * 60
                data_point = {
                    'word_count': word_count,
                    'gen_time': gen_time,
                    'wpm': wpm,
                    'temp': temp,
                    'top_p': top_p
                }
                
                # Categorize by temperature
                if temp < 0.6:
                    temp_groups['low'].append(data_point)
                elif temp < 1.0:
                    temp_groups['med'].append(data_point)
                else:
                    temp_groups['high'].append(data_point)
                
                # Categorize by top_p
                if top_p < 0.8:
                    top_p_groups['low'].append(data_point)
                elif top_p < 0.95:
                    top_p_groups['med'].append(data_point)
                else:
                    top_p_groups['high'].append(data_point)
        
        # Display temperature effects
        print("TEMPERATURE EFFECTS:")
        for level, data in temp_groups.items():
            if data:
                avg_words = sum(d['word_count'] for d in data) / len(data)
                avg_wpm = sum(d['wpm'] for d in data) / len(data)
                temp_range = f"{min(d['temp'] for d in data):.1f}-{max(d['temp'] for d in data):.1f}"
                print(f"  {level.upper()} ({temp_range}): {len(data)} samples, {avg_words:.0f} words avg, {avg_wpm:.0f} WPM")
        print()
        
        # Display top_p effects
        print("TOP-P EFFECTS:")
        for level, data in top_p_groups.items():
            if data:
                avg_words = sum(d['word_count'] for d in data) / len(data)
                avg_wpm = sum(d['wpm'] for d in data) / len(data)
                top_p_range = f"{min(d['top_p'] for d in data):.2f}-{max(d['top_p'] for d in data):.2f}"
                print(f"  {level.upper()} ({top_p_range}): {len(data)} samples, {avg_words:.0f} words avg, {avg_wpm:.0f} WPM")
        
        print("\nOBSERVATIONS:")
        print("• Higher temperature typically increases creativity but may reduce coherence")
        print("• Higher top-p increases vocabulary diversity")
        print("• Lower parameters often generate faster but may be more repetitive")
        
        input("\nPress Enter to continue...")
    
    def _analyze_word_patterns(self, results):
        """Analyze word patterns in generated content"""
        print("\nWORD PATTERN ANALYSIS")
        print("="*40)
        
        all_text = []
        word_counts = []
        
        for result in results:
            response_info = result.get('response_info', {})
            response_text = response_info.get('response', '')
            
            if response_text:
                all_text.append(response_text.lower())
                word_counts.append(len(response_text.split()))
        
        if not all_text:
            print("No text content found in results")
            input("Press Enter to continue...")
            return
        
        # Combine all text
        combined_text = ' '.join(all_text)
        words = combined_text.split()
        
        # Most common words (excluding very common ones)
        common_words = ['the', 'and', 'a', 'to', 'of', 'in', 'i', 'you', 'it', 'that', 'was', 'is', 'he', 'she', 'his', 'her', 'with', 'as', 'at', 'on', 'for', 'had', 'have', 'but', 'not', 'they', 'this', 'from', 'or', 'by', 'be', 'are', 'an', 'my', 'me', 'we', 'our', 'up', 'out', 'if', 'no', 'so', 'what', 'all', 'were', 'when', 'would', 'there', 'been', 'their', 'said', 'could', 'him', 'her']
        
        word_freq = {}
        for word in words:
            clean_word = ''.join(c for c in word if c.isalpha())
            if len(clean_word) > 3 and clean_word not in common_words:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Sort by frequency
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        print(f"Analyzed {len(results)} generations ({len(words)} total words)")
        print(f"Average length: {sum(word_counts)/len(word_counts):.1f} words per generation")
        print()
        
        print("MOST FREQUENT CONTENT WORDS:")
        for word, freq in top_words[:10]:
            percentage = (freq / len(words)) * 100
            print(f"  {word}: {freq} times ({percentage:.2f}%)")
        print()
        
        # Check for perspective consistency
        first_person = combined_text.count(' i ') + combined_text.count(' my ') + combined_text.count(' me ')
        second_person = combined_text.count(' you ') + combined_text.count(' your ')
        third_person = combined_text.count(' he ') + combined_text.count(' she ') + combined_text.count(' his ') + combined_text.count(' her ')
        
        print("PERSPECTIVE ANALYSIS:")
        print(f"  First person indicators: {first_person}")
        print(f"  Second person indicators: {second_person}")
        print(f"  Third person indicators: {third_person}")
        
        if first_person > second_person and first_person > third_person:
            print("  Primary perspective: First Person")
        elif second_person > third_person:
            print("  Primary perspective: Second Person")
        else:
            print("  Primary perspective: Third Person")
        
        input("\nPress Enter to continue...")
    
    def _show_best_worst_results(self, results):
        """Show best and worst performing results"""
        print("\nBEST & WORST RESULTS")
        print("="*40)
        
        # Calculate performance metrics
        performance_data = []
        
        for result in results:
            response_info = result.get('response_info', {})
            test_info = result.get('test_info', {})
            
            word_count = response_info.get('word_count', 0)
            gen_time = response_info.get('generation_time', 1)
            
            if word_count > 0 and gen_time > 0:
                wpm = (word_count / gen_time) * 60
                
                performance_data.append({
                    'result': result,
                    'word_count': word_count,
                    'gen_time': gen_time,
                    'wpm': wpm,
                    'model': test_info.get('model', 'Unknown'),
                    'params': test_info.get('parameters_used', {}),
                    'session': result.get('session_folder', 'Unknown')
                })
        
        if not performance_data:
            print("No performance data available")
            input("Press Enter to continue...")
            return
        
        # Sort by different metrics
        by_wpm = sorted(performance_data, key=lambda x: x['wpm'], reverse=True)
        by_word_count = sorted(performance_data, key=lambda x: x['word_count'], reverse=True)
        by_speed = sorted(performance_data, key=lambda x: x['gen_time'])
        
        print("FASTEST GENERATION (WPM):")
        for i, data in enumerate(by_wpm[:3], 1):
            print(f"{i}. {data['wpm']:.0f} WPM - {data['word_count']} words in {data['gen_time']:.1f}s")
            print(f"   Model: {data['model']}, T={data['params'].get('temperature', '?')}")
            print()
        
        print("LONGEST STORIES:")
        for i, data in enumerate(by_word_count[:3], 1):
            print(f"{i}. {data['word_count']} words - {data['wpm']:.0f} WPM")
            print(f"   Model: {data['model']}, T={data['params'].get('temperature', '?')}")
            print()
        
        print("FASTEST COMPLETION:")
        for i, data in enumerate(by_speed[:3], 1):
            print(f"{i}. {data['gen_time']:.1f} seconds - {data['word_count']} words ({data['wpm']:.0f} WPM)")
            print(f"   Model: {data['model']}, T={data['params'].get('temperature', '?')}")
            print()
        
        input("Press Enter to continue...")
    
    def _export_results_summary(self, results):
        """Export results summary to file"""
        print("\nEXPORT RESULTS SUMMARY")
        print("="*40)
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"workshop_analysis_{timestamp}.txt"
            filepath = os.path.join(self.workshop.model_tester.results_folder, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("SCENE WORKSHOP RESULTS ANALYSIS\n")
                f.write("="*50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Results analyzed: {len(results)}\n\n")
                
                # Write statistics
                word_counts = []
                gen_times = []
                models_used = {}
                
                for result in results:
                    test_info = result.get('test_info', {})
                    response_info = result.get('response_info', {})
                    
                    word_count = response_info.get('word_count', 0)
                    if word_count > 0:
                        word_counts.append(word_count)
                    
                    gen_time = response_info.get('generation_time', 0)
                    if gen_time > 0:
                        gen_times.append(gen_time)
                    
                    model = test_info.get('model', 'Unknown')
                    models_used[model] = models_used.get(model, 0) + 1
                
                if word_counts:
                    f.write("WORD COUNT STATISTICS:\n")
                    f.write(f"  Average: {sum(word_counts)/len(word_counts):.1f} words\n")
                    f.write(f"  Range: {min(word_counts)} - {max(word_counts)} words\n")
                    f.write(f"  Median: {sorted(word_counts)[len(word_counts)//2]} words\n\n")
                
                if gen_times:
                    f.write("GENERATION TIME STATISTICS:\n")
                    f.write(f"  Average: {sum(gen_times)/len(gen_times):.1f} seconds\n")
                    f.write(f"  Range: {min(gen_times):.1f} - {max(gen_times):.1f} seconds\n\n")
                
                if models_used:
                    f.write("MODELS USED:\n")
                    for model, count in models_used.items():
                        f.write(f"  {model}: {count} generations\n")
            
            print(f"Analysis exported to: {filename}")
            print(f"Location: {filepath}")
            
        except Exception as e:
            print(f"Error exporting analysis: {e}")
        
        input("Press Enter to continue...")
