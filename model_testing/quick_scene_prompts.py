"""Quick Genre & Style prompts for scene generation"""

QUICK_SCENE_PROMPTS = {
    "Romance": {
        "Sweet & Tender": "Write romantic scenes with gentle emotions, meaningful glances, and tender moments between characters.",
        "Steamy & Passionate": "Create passionate romantic scenes with intense chemistry, desire, and intimate emotional connections.",
        "Slow Burn": "Build romantic tension gradually through subtle interactions, lingering touches, and unspoken feelings.",
        "Enemies to Lovers": "Transform conflict into attraction through heated exchanges that reveal hidden romantic tension.",
        "First Love": "Capture the innocence and wonder of first love with nervous excitement and heartfelt discoveries.",
        "Forbidden Romance": "Create tension through forbidden attraction with secret meetings and stolen moments of connection.",
        "Second Chance": "Write scenes of rekindled romance with past hurt, forgiveness, and renewed hope.",
        "Friends to Lovers": "Show the transition from friendship to romance through dawning realization and changing dynamics."
    },
    
    "Fantasy": {
        "Epic & Heroic": "Write fantasy scenes with grand adventures, noble heroes, and magical conflicts of good versus evil.",
        "Dark & Gritty": "Create gritty fantasy with moral ambiguity, dangerous magic, and harsh realistic consequences.",
        "Whimsical & Magical": "Focus on wonder and enchantment with playful magic, curious creatures, and delightful discoveries.",
        "Political Intrigue": "Weave fantasy scenes with court politics, magical schemes, and complex power struggles between factions.",
        "Urban Fantasy": "Blend modern world with hidden magic, supernatural creatures living among ordinary people.",
        "Medieval Fantasy": "Create traditional fantasy with knights, dragons, castles, and classic magical elements.",
        "Mythological": "Draw from ancient myths and legends with gods, heroes, and legendary creatures.",
        "Magical Academy": "Focus on learning magic in school settings with young wizards and magical education."
    },
    
    "Detective": {
        "Classic Mystery": "Write detective scenes with logical deduction, hidden clues, and methodical investigation techniques.",
        "Noir & Gritty": "Create dark detective scenes with moral ambiguity, urban decay, and cynical characters.",
        "Cozy Mystery": "Focus on gentle mysteries in small communities with amateur sleuths and minimal violence.",
        "Psychological Thriller": "Build tension through mind games, unreliable narrators, and psychological manipulation.",
        "Police Procedural": "Show realistic police work with forensics, interviews, and systematic investigation methods.",
        "Hard-boiled": "Write tough detective scenes with corruption, violence, and morally complex characters.",
        "Amateur Sleuth": "Feature ordinary people solving crimes through curiosity, intuition, and local knowledge.",
        "Cold Case": "Investigate old unsolved crimes with new evidence, fresh perspectives, and buried secrets."
    },
    
    "Sci-Fi": {
        "Space Opera": "Create grand space adventures with alien civilizations, starships, and galactic conflicts.",
        "Cyberpunk": "Write futuristic scenes with high tech, low life, corporate control, and digital rebellion.",
        "Hard Science": "Focus on realistic science with detailed technical explanations and plausible future technology.",
        "Dystopian": "Create oppressive future societies with resistance, control, and struggles for freedom.",
        "Time Travel": "Explore temporal mechanics with paradoxes, consequences, and changing timelines.",
        "First Contact": "Write scenes of humanity meeting alien species for the first time.",
        "Post-Apocalyptic": "Show survival in ruined worlds with scarce resources and new social orders.",
        "AI & Robots": "Explore artificial intelligence, consciousness, and human-machine relationships."
    },
    
    "Horror": {
        "Psychological Horror": "Build dread through mental deterioration, paranoia, and questioning reality.",
        "Supernatural": "Create fear with ghosts, demons, curses, and otherworldly threatening forces.",
        "Body Horror": "Focus on physical transformation, disease, and grotesque bodily changes.",
        "Cosmic Horror": "Invoke existential dread with incomprehensible entities and humanity's insignificance.",
        "Gothic Horror": "Use dark atmosphere with old mansions, family secrets, and romantic decay.",
        "Survival Horror": "Create tension through resource scarcity, isolation, and constant threat.",
        "Folk Horror": "Draw from rural traditions, ancient rituals, and community-based supernatural threats.",
        "Slasher": "Write scenes with stalking killers, final girls, and escalating violence."
    },
    
    "Adventure": {
        "Swashbuckling": "Create adventurous scenes with sword fights, daring escapes, and heroic bravado.",
        "Treasure Hunting": "Focus on quests for lost artifacts with maps, puzzles, and dangerous obstacles.",
        "Exploration": "Write scenes of discovery in unknown lands with natural dangers and wonders.",
        "Survival": "Show characters overcoming harsh environments with resourcefulness and determination.",
        "Heist & Caper": "Plan and execute elaborate schemes with clever tricks and narrow escapes.",
        "Military Action": "Write combat scenes with strategy, teamwork, and high-stakes missions.",
        "Espionage": "Create spy scenarios with secret identities, surveillance, and covert operations.",
        "Western": "Set adventures in the Old West with gunfights, frontier justice, and lawless towns."
    },
    
    "Drama": {
        "Family Drama": "Explore complex family relationships with generational conflicts and emotional revelations.",
        "Coming of Age": "Show character growth through challenges, self-discovery, and life-changing experiences.",
        "Social Issues": "Address contemporary problems with realistic characters facing societal challenges.",
        "Historical Drama": "Set dramatic scenes in past eras with period-accurate conflicts and customs.",
        "Medical Drama": "Create hospital scenes with life-and-death decisions and emotional medical situations.",
        "Legal Drama": "Write courtroom scenes with moral dilemmas, justice, and legal maneuvering.",
        "Workplace Drama": "Show professional conflicts with office politics, career struggles, and personal relationships.",
        "Small Town Drama": "Explore close-knit community dynamics with secrets, gossip, and interconnected lives."
    },
    
    "Comedy": {
        "Romantic Comedy": "Write humorous romantic situations with misunderstandings, cute meet-cutes, and happy endings.",
        "Slapstick": "Create physical comedy with exaggerated actions, mishaps, and visual humor.",
        "Satirical": "Use humor to critique society, politics, or human behavior with wit and irony.",
        "Situational Comedy": "Build humor from everyday situations with relatable characters and awkward moments.",
        "Dark Comedy": "Combine humor with serious subjects, finding comedy in inappropriate or tragic situations.",
        "Parody": "Mock and exaggerate other genres, tropes, or specific works for comedic effect.",
        "Buddy Comedy": "Focus on comedic partnerships with contrasting personalities and shared adventures.",
        "Fish Out of Water": "Create humor from characters in unfamiliar situations or environments."
    }
}

QUICK_STORY_PROMPTS = {
    "Romance": {
        "Epic Romance": "Write complete romantic stories with character development, relationship arcs, and satisfying emotional resolution.",
        "Contemporary Romance": "Create modern love stories with realistic relationships, current settings, and relatable conflicts.",
        "Historical Romance": "Set romantic stories in past eras with period-accurate courtship and historical conflicts.",
        "Paranormal Romance": "Blend romance with supernatural elements, magical creatures, and otherworldly settings.",
    },
    
    "Fantasy": {
        "High Fantasy": "Create complete fantasy worlds with magic systems, quests, and epic conflicts between good and evil.",
        "Low Fantasy": "Write fantasy with minimal magic in realistic settings, focusing on character over world-building.",
        "Dark Fantasy": "Combine fantasy elements with horror, moral ambiguity, and mature themes throughout the story.",
        "Urban Fantasy": "Set fantasy stories in modern cities with hidden magical worlds and supernatural conflicts.",
    },
    
    "Detective": {
        "Mystery Novel": "Structure complete detective stories with clues, red herrings, investigation, and satisfying resolution.",
        "Crime Thriller": "Write fast-paced crime stories with suspense, danger, and complex criminal plots.",
        "Detective Series": "Create ongoing detective characters with recurring elements and evolving relationships.",
        "True Crime Style": "Write realistic crime stories with documentary-style investigation and authentic details.",
    },
    
    "Sci-Fi": {
        "Space Epic": "Create grand science fiction stories spanning galaxies with alien species and advanced technology.",
        "Near Future": "Write science fiction set in the near future with emerging technology and social changes.",
        "Alternate History": "Explore how history might have changed with different technological or social developments.",
        "Generation Ship": "Focus on long space voyages with multi-generational crews and evolving societies.",
    },
    
    "Adventure": {
        "Quest Adventure": "Structure adventure stories around specific goals with obstacles, allies, and character growth.",
        "Survival Story": "Write adventures focused on overcoming harsh environments and life-threatening situations.",
        "Action Adventure": "Create fast-paced adventure stories with constant movement, danger, and heroic action.",
        "Historical Adventure": "Set adventures in specific historical periods with accurate details and period conflicts.",
    }
}
