class ContentConfigurator:
    def get_rating_display(self, content_rating):
        """Get display string for content rating"""
        if content_rating == "auto":
            return "Auto (from blueprint)"
        elif content_rating.startswith("custom:"):
            custom_text = content_rating[7:]  # Remove "custom:" prefix
            return f"Custom: {custom_text}"
        else:
            return content_rating.title()
    
    def configure_content_rating(self, current_rating):
        """Configure content rating for stories"""
        print("\n" + "="*60)
        print("CONTENT RATING CONFIGURATION")
        print("="*60)
        print("Control the content rating/age appropriateness of your stories:\n")
    
        print("CONTENT RATINGS:")
        print("┌────────┬─────────────────────────────────────────────────────┐")
        print("│ Rating │ Description                                         │")
        print("├────────┼─────────────────────────────────────────────────────┤")
        print("│ Family │ Family-friendly - All ages, no adult content       │")
        print("│ Teen   │ Teen appropriate - Mild themes, minimal violence   │")
        print("│ Adult  │ Adult themes - Strong content, mature situations   │")
        print("│ Custom │ Your own rating description                         │")
        print("│ Auto   │ Use blueprint's natural rating (default)           │")
        print("└────────┴─────────────────────────────────────────────────────┘")
    
        print(f"\nCurrent: {self.get_rating_display(current_rating)}")
    
        print("\nOptions:")
        print("1. Family - Family-friendly content")
        print("2. Teen - Teen-appropriate content")
        print("3. Adult - Mature themes and content")
        print("4. Custom - Enter your own rating description")
        print("5. Auto - Use blueprint's natural rating")
        print("6. Keep current setting")
    
        try:
            choice = input("Select (1-6): ").strip()
    
            if choice == "1":
                result = "family"
                print("✓ Set to Family - Family-friendly content")
            elif choice == "2":
                result = "teen"
                print("✓ Set to Teen - Teen-appropriate content")
            elif choice == "3":
                result = "adult"
                print("✓ Set to Adult - Mature themes and content")
            elif choice == "4":
                print("\nCUSTOM RATING:")
                print("Enter your own content rating description.")
                print("Examples: 'PG-13 equivalent', 'No violence', 'Historical accuracy focus'")
    
                custom_rating = input("Enter custom rating description: ").strip()
                if custom_rating:
                    result = f"custom:{custom_rating}"
                    print(f"✓ Set to Custom: {custom_rating}")
                else:
                    print("❌ No description entered. Keeping current setting.")
                    result = current_rating
            elif choice == "5":
                result = "auto"
                print("✓ Set to Auto - Use blueprint's natural rating")
            elif choice == "6":
                result = current_rating
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
                result = current_rating
    
            if choice in ["1", "2", "3", "4"] and choice != "5":
                print("  Note: This will override any rating implied in the blueprint")
    
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_rating
    
        input("\nPress Enter to continue...")
        return result
    
    def configure_story_tone(self, current_tone):
        """Configure story tone/genre"""
        print("\n" + "="*60)
        print("STORY TONE CONFIGURATION")
        print("="*60)
        print("Control the overall tone and style of your stories:\n")
        
        print("STORY TONE OPTIONS:")
        print("┌──────────────────┬────────────────────────────────────────────┐")
        print("│ Tone             │ Description                                │")
        print("├──────────────────┼────────────────────────────────────────────┤")
        print("│ Comedy           │ Lighthearted, funny, comedic situations   │")
        print("│ Light Comedy     │ Gentle humor, feel-good, upbeat           │")
        print("│ Romantic Comedy  │ Love story with humor, heartwarming        │")
        print("│ Dark Comedy      │ Black humor, satirical, edgy              │")
        print("│ Raunchy          │ Adult humor, crude jokes, provocative     │")
        print("│ Serious          │ Dramatic, realistic, no humor             │")
        print("│ Dark/Noir        │ Gritty, pessimistic, morally complex      │")
        print("│ Thriller         │ Suspenseful, intense, high tension        │")
        print("│ Horror           │ Scary, supernatural, frightening          │")
        print("│ Mystery          │ Puzzle-focused, investigative, cerebral   │")
        print("│ Action           │ Fast-paced, exciting, adventure-focused   │")
        print("│ Drama            │ Character-driven, emotional, realistic    │")
        print("│ Auto             │ Use blueprint's natural tone (default)    │")
        print("└──────────────────┴────────────────────────────────────────────┘")
        
        current_display = current_tone.replace('_', ' ').title() if current_tone != "auto" else "Auto (from blueprint)"
        print(f"\nCurrent: {current_display}")
        
        print("\nOptions:")
        print("1. Comedy - Lighthearted and funny")
        print("2. Light Comedy - Gentle humor")
        print("3. Romantic Comedy - Love with laughs")
        print("4. Dark Comedy - Black humor")
        print("5. Raunchy - Adult/crude humor")
        print("6. Serious - No humor, dramatic")
        print("7. Dark/Noir - Gritty and pessimistic")
        print("8. Thriller - Suspenseful")
        print("9. Horror - Scary/frightening")
        print("10. Mystery - Puzzle-focused")
        print("11. Action - Fast-paced adventure")
        print("12. Drama - Character-driven")
        print("13. Auto - Use blueprint's tone")
        print("14. Keep current setting")
        
        try:
            choice = input("Select (1-14): ").strip()
            
            tones = {
                "1": ("comedy", "Comedy"),
                "2": ("light_comedy", "Light Comedy"),
                "3": ("romantic_comedy", "Romantic Comedy"),
                "4": ("dark_comedy", "Dark Comedy"),
                "5": ("raunchy", "Raunchy"),
                "6": ("serious", "Serious"),
                "7": ("dark_noir", "Dark/Noir"),
                "8": ("thriller", "Thriller"),
                "9": ("horror", "Horror"),
                "10": ("mystery", "Mystery"),
                "11": ("action", "Action"),
                "12": ("drama", "Drama"),
                "13": ("auto", "Auto - Use blueprint's tone")
            }
            
            if choice in tones:
                result = tones[choice][0]
                print(f"✓ Set to {tones[choice][1]}")
                
                if choice != "13":
                    print("  Note: This will override any tone implied in the blueprint")
            elif choice == "14":
                result = current_tone
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
                result = current_tone
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_tone
        
        input("\nPress Enter to continue...")
        return result
    
    def configure_story_ending(self, current_ending):
        """Configure story ending type"""
        print("\n" + "="*60)
        print("STORY ENDING CONFIGURATION")
        print("="*60)
        print("Control how your stories conclude:\n")
        
        print("ENDING TYPES:")
        print("┌─────────────┬──────────────────────────────────────────────────┐")
        print("│ Ending      │ Description                                      │")
        print("├─────────────┼──────────────────────────────────────────────────┤")
        print("│ Happy       │ Positive resolution, everyone wins              │")
        print("│ Dark        │ Pessimistic, villain wins, tragedy              │")
        print("│ Bittersweet │ Mixed outcome, victory with cost                │")
        print("│ Open        │ Ambiguous, unresolved, reader decides           │")
        print("│ Tragic      │ Hero falls, devastating consequences            │")
        print("│ Twist       │ Surprise revelation changes everything          │")
        print("│ Redemption  │ Character growth, second chances                │")
        print("│ Justice     │ Right prevails, wrongdoers punished            │")
        print("│ Cliffhanger │ Unfinished, setup for continuation             │")
        print("│ Auto        │ Use blueprint's natural ending (default)       │")
        print("└─────────────┴──────────────────────────────────────────────────┘")
        
        current_display = current_ending.replace('_', ' ').title() if current_ending != "auto" else "Auto (from blueprint)"
        print(f"\nCurrent: {current_display}")
        
        print("\nOptions:")
        print("1. Happy - Positive resolution")
        print("2. Dark - Pessimistic outcome")
        print("3. Bittersweet - Mixed victory")
        print("4. Open - Ambiguous ending")
        print("5. Tragic - Hero falls")
        print("6. Twist - Surprise revelation")
        print("7. Redemption - Character growth")
        print("8. Justice - Right prevails")
        print("9. Cliffhanger - Unfinished")
        print("10. Auto - Use blueprint's ending")
        print("11. Keep current setting")
        
        try:
            choice = input("Select (1-11): ").strip()
            
            endings = {
                "1": ("happy", "Happy"),
                "2": ("dark", "Dark"),
                "3": ("bittersweet", "Bittersweet"),
                "4": ("open", "Open"),
                "5": ("tragic", "Tragic"),
                "6": ("twist", "Twist"),
                "7": ("redemption", "Redemption"),
                "8": ("justice", "Justice"),
                "9": ("cliffhanger", "Cliffhanger"),
                "10": ("auto", "Auto - Use blueprint's ending")
            }
            
            if choice in endings:
                result = endings[choice][0]
                print(f"✓ Set to {endings[choice][1]} ending")
                
                if choice != "10":
                    print("  Note: This will override any ending implied in the blueprint")
            elif choice == "11":
                result = current_ending
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
                result = current_ending
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_ending
        
        input("\nPress Enter to continue...")
        return result
    
    def configure_character_count(self, current_count):
        """Configure character count for stories - NEW FEATURE"""
        print("\n" + "="*60)
        print("CHARACTER COUNT CONFIGURATION")
        print("="*60)
        print("Control how many people appear in your stories:\n")
        
        print("CHARACTER COUNT OPTIONS:")
        print("┌─────────────┬────────────────────────────────────────────────┐")
        print("│ Count       │ Description & Examples                         │")
        print("├─────────────┼────────────────────────────────────────────────┤")
        print("│ Minimal     │ 2-3 people - Intimate, focused stories        │")
        print("│ (2-3 people)│ • Detective vs Killer cat-and-mouse           │")
        print("│             │ • Romantic drama between lovers               │")
        print("│             │ • Parent-child conflict                       │")
        print("├─────────────┼────────────────────────────────────────────────┤")
        print("│ Small Cast  │ 4-6 people - Small ensemble stories           │")
        print("│ (4-6 people)│ • Close friend group dynamics                 │")
        print("│             │ • Family drama with key members               │")
        print("│             │ • Detective team investigation                │")
        print("├─────────────┼────────────────────────────────────────────────┤")
        print("│ Large Cast  │ 7+ people - Epic, complex stories             │")
        print("│ (7+ people) │ • Multi-family sagas                          │")
        print("│             │ • Workplace ensemble                          │")
        print("│             │ • Community-wide mysteries                    │")
        print("├─────────────┼────────────────────────────────────────────────┤")
        print("│ Auto        │ AI decides based on story type (default)      │")
        print("└─────────────┴────────────────────────────────────────────────┘")
        
        current_display = current_count.replace('_', ' ').title() if current_count != "auto" else "Auto (from blueprint)"
        print(f"\nCurrent: {current_display}")
        
        print("\nDETECTIVE STORIES WITH MINIMAL CAST:")
        print("• Detective's internal monologue at crime scenes")
        print("• Cat-and-mouse phone calls/messages with killer") 
        print("• Flashbacks showing killer's perspective")
        print("• Final confrontation dialogue")
        print("• Maybe one victim who appears in flashbacks only")
        
        print("\nOptions:")
        print("1. Minimal (2-3 people) - Intimate, focused stories")
        print("2. Small Cast (4-6 people) - Small ensemble")
        print("3. Large Cast (7+ people) - Epic, complex stories")
        print("4. Auto - AI decides based on story type")
        print("5. Keep current setting")
        
        try:
            choice = input("Select (1-5): ").strip()
            
            if choice == "1":
                result = "minimal"
                print("✓ Set to Minimal (2-3 people)")
                print("  Focus on intimate character dynamics and deep relationships")
            elif choice == "2":
                result = "small_cast"
                print("✓ Set to Small Cast (4-6 people)")
                print("  Perfect for ensemble stories with manageable complexity")
            elif choice == "3":
                result = "large_cast"
                print("✓ Set to Large Cast (7+ people)")
                print("  Epic stories with multiple plotlines and characters")
            elif choice == "4":
                result = "auto"
                print("✓ Set to Auto - AI decides based on story type")
            elif choice == "5":
                result = current_count
                print("✓ Keeping current setting")
            else:
                print("❌ Invalid choice")
                result = current_count
        except Exception as e:
            print(f"❌ Error: {e}")
            result = current_count
        
        input("\nPress Enter to continue...")
        return result
