"""
Narrative Style Examples
Shows how different narrative perspectives would handle the same scene
"""

SCENE_PREMISE = "Character arrives at a coffee shop and sees their ex with someone new"

NARRATIVE_STYLE_EXAMPLES = {
    "first_person_inner_thoughts": {
        "name": "First Person - Inner Thoughts Focus",
        "example": '''I pushed open the glass door, the familiar chime of Morrison's Coffee filling my ears. *Just grab your usual and get out,* I told myself, already rehearsing my order. But then I saw them.

Sarah sat at our old table by the window, laughing at something the guy across from her was saying. *Of course she's here,* I thought, my stomach dropping. *Of course she looks happy.* 

I should leave. I should turn around right now and pretend I never saw this. But my feet wouldn't move. The guy was tall, clean-shaven, probably had his life together. Everything I wasn't when we were together.

*Stop staring,* I commanded myself, but it was too late. Sarah's eyes met mine across the crowded café, and her smile faltered.'''
    },
    
    "second_person_romance": {
        "name": "Second Person Romance",
        "example": '''I pushed open the coffee shop door, hoping you'd gotten my text. We'd agreed to meet here, to finally talk things through after that argument last week.

But as I scanned the room, I saw you weren't alone. You were sitting at a corner table, leaning forward as some woman I'd never seen before touched your arm and laughed.

*Who is she?* I thought, my heart sinking. You looked so relaxed with her, so at ease. The way you used to look with me.

I started to back toward the door, but you glanced up and saw me. Your expression changed instantly—surprise, then something that might have been guilt.

"I can explain," you said, standing quickly as I approached your table. But I wasn't sure I wanted you to.'''
    },
    
    "third_person_limited": {
        "name": "Third Person Limited",
        "example": '''David pushed open the coffee shop door, the familiar bell announcing his arrival. He'd been coming here for months, but today felt different somehow.

His eyes swept the familiar space until they landed on a table by the window. Sarah. His Sarah—or rather, his ex-Sarah—sat across from a man he'd never seen before. She was laughing, genuinely laughing, in a way she hadn't with him in months before their breakup.

The rational part of his mind told him to leave, to give her space. But he found himself rooted to the spot, watching as the stranger leaned closer to say something that made her eyes light up. David's chest tightened with an emotion he didn't want to name.

When Sarah's gaze found his across the crowded café, her smile faded, replaced by something unreadable.'''
    },
    
    "third_person_omniscient": {
        "name": "Third Person Omniscient",
        "example": '''The coffee shop buzzed with its usual afternoon energy as David entered, unaware that his world was about to shift. At a window table, Sarah was experiencing the first genuine joy she'd felt in months, finally allowing herself to believe that maybe, just maybe, she could move forward.

Her companion, David, had been carefully building up the courage to ask her out for weeks, not knowing about the complicated history that had brought her to this emotional crossroads.

As David spotted them, his mind raced through a catalog of regrets and what-ifs, while Sarah felt the familiar flutter of anxiety that always accompanied unexpected encounters with her past. David, oblivious to the undercurrents, continued his story about his disastrous camping trip, wondering why Sarah had suddenly gone quiet.

Three hearts, three different hopes and fears, converging in one moment of recognition.'''
    },
    
    "stream_of_consciousness": {
        "name": "Stream of Consciousness",
        "example": '''Door opens bell rings why did I come here stupid stupid I could have gone anywhere else but no Morrison's like always like we always did and there she is there she fucking is with him with someone else laughing god she's laughing when did she ever laugh like that with me never not like that not that free happy sound and he's what handsome sure confident probably has a real job real car real life not like me not like pathetic me standing here staring like some creep she sees me oh god she sees me and her face changes and I should run should definitely run but I can't move can't breathe can't think straight just standing here like an idiot...'''
    },
    
    "noir_first_person": {
        "name": "Noir First Person",
        "example": '''I'd walked into that coffee shop a hundred times before, but this time felt like stepping into a trap. The kind where you know you're screwed, but you walk in anyway because that's just the kind of fool you are.

She was there, of course. Sarah. Looking like a million bucks and twice as dangerous, sitting across from some clean-cut type who probably drove a sedan and filed his taxes early. The kind of man I'd never be.

I should have turned around. Should have walked back out into the rain and kept walking until I hit the ocean. But I've never been smart about these things. Never been smart about her.

The moment she looked up and saw me, I knew I was in trouble. The same kind of trouble that had landed me here in the first place.'''
    },
    
    "present_tense_immediate": {
        "name": "Present Tense First Person",
        "example": '''I push open the door and the coffee shop's warmth hits me. The usual crowd fills the tables, laptops open, conversations flowing. I'm scanning for an empty spot when I see her.

Sarah sits by the window, and she's not alone. There's a guy across from her, leaning in close, making her laugh. My stomach drops.

I freeze in the doorway. People are trying to get past me, but I can't move. She looks happy. Really happy. Happier than she ever looked with me.

She glances up and our eyes meet. Her laughter dies. The guy follows her gaze and turns to look at me. I feel like I'm intruding on something private, something that was never meant for me to see.'''
    },
    
    "romantic_intimate": {
        "name": "Romantic Intimate First Person",
        "example": '''My heart was already racing as I stepped into Morrison's, not from the cold October air, but from the possibility of seeing you again. We'd texted, carefully navigating around the hurt, around the things we'd said. Maybe today we could finally talk.

But you were already there, and you weren't alone. She was beautiful in that effortless way that made my chest ache with comparison. The way she made you laugh—God, when was the last time I'd seen you laugh like that? Open, unguarded, free.

I felt something break inside me, some fragile hope I'd been nursing since your last message. You looked up then, as if you could feel my gaze, and the guilt in your eyes told me everything I needed to know about what this meant.'''
    }
}

def show_all_style_examples():
    """Display all narrative style examples"""
    print("\n" + "="*80)
    print("NARRATIVE STYLE EXAMPLES")
    print("="*80)
    print(f"Scene: {SCENE_PREMISE}")
    print("="*80)
    
    for style_key, style_data in NARRATIVE_STYLE_EXAMPLES.items():
        print(f"\n{'='*20} {style_data['name'].upper()} {'='*20}")
        print(style_data['example'])
        print("\n" + "-"*60)
        input("Press Enter to see next example...")

def get_style_example(style_name):
    """Get example for a specific style"""
    for style_key, style_data in NARRATIVE_STYLE_EXAMPLES.items():
        if style_name.lower() in style_key.lower():
            return style_data['example']
    return None

if __name__ == "__main__":
    show_all_style_examples()
