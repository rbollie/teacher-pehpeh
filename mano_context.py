"""
========================================================================
MANO LANGUAGE MODULE - Bilingual support for Mano-speaking communities
========================================================================
Provides Mano vocabulary, phrases, grammar patterns, and cultural context
for Teacher Pehpeh lessons targeting Nimba County and other Mano-speaking
areas in Liberia.

The Mano language (Maa) is spoken by ~300,000+ people, primarily in
Nimba County, Liberia, and parts of Guinea.
========================================================================
"""

# Flag for app.py to check
MANO_AVAILABLE = True

# ── Core Mano Vocabulary Dictionary ───────────────────────────────────
# Structure: English -> {"mano": Mano word, "pronunciation": guide, "category": grouping}

MANO_DICT = {
    # ── Numbers ──
    "one":    {"mano": "dɔ́",     "pronunciation": "doh",      "category": "numbers"},
    "two":    {"mano": "fèlè",   "pronunciation": "feh-leh",  "category": "numbers"},
    "three":  {"mano": "sáwá",   "pronunciation": "sah-wah",  "category": "numbers"},
    "four":   {"mano": "náání",  "pronunciation": "nah-nee",  "category": "numbers"},
    "five":   {"mano": "sɔ́ɔ́lú","pronunciation": "soh-loo",  "category": "numbers"},
    "six":    {"mano": "sɔ́ɔ́ldɔ́","pronunciation": "sohl-doh","category": "numbers"},
    "seven":  {"mano": "sɔ́ɔ́lfèlè","pronunciation": "sohl-feh-leh","category": "numbers"},
    "eight":  {"mano": "sɔ́ɔ́lsáwá","pronunciation": "sohl-sah-wah","category": "numbers"},
    "nine":   {"mano": "sɔ́ɔ́lnáání","pronunciation": "sohl-nah-nee","category": "numbers"},
    "ten":    {"mano": "vù",     "pronunciation": "voo",      "category": "numbers"},
    "twenty": {"mano": "mɔ̀ɔ̀ dɔ́","pronunciation": "moh doh","category": "numbers"},
    "hundred":{"mano": "kɛ̀mɛ̀", "pronunciation": "keh-meh",  "category": "numbers"},

    # ── School & Education ──
    "school":    {"mano": "sùkúù",    "pronunciation": "soo-koo",    "category": "education"},
    "teacher":   {"mano": "kàlàmàsɛ̀","pronunciation": "kah-lah-mah-seh","category": "education"},
    "student":   {"mano": "sùkúùnù", "pronunciation": "soo-koo-noo","category": "education"},
    "book":      {"mano": "bɛ́ì",     "pronunciation": "beh-ee",     "category": "education"},
    "pen":       {"mano": "kàlàmà",  "pronunciation": "kah-lah-mah","category": "education"},
    "paper":     {"mano": "kàlá",    "pronunciation": "kah-lah",    "category": "education"},
    "learn":     {"mano": "kàlà",    "pronunciation": "kah-lah",    "category": "education"},
    "read":      {"mano": "kàlà",    "pronunciation": "kah-lah",    "category": "education"},
    "write":     {"mano": "sɛ̀bɛ̀",   "pronunciation": "seh-beh",    "category": "education"},
    "question":  {"mano": "màlèní",  "pronunciation": "mah-leh-nee","category": "education"},
    "answer":    {"mano": "jàbí",    "pronunciation": "jah-bee",    "category": "education"},
    "know":      {"mano": "lɔ́n",     "pronunciation": "lawn",       "category": "education"},
    "understand":{"mano": "mɛ́nì",   "pronunciation": "meh-nee",    "category": "education"},
    "think":     {"mano": "lààlú",   "pronunciation": "lah-loo",    "category": "education"},
    "count":     {"mano": "yálá",    "pronunciation": "yah-lah",    "category": "education"},

    # ── Science & Nature ──
    "water":   {"mano": "ní",       "pronunciation": "nee",        "category": "science"},
    "fire":    {"mano": "tɛ́",      "pronunciation": "teh",        "category": "science"},
    "earth":   {"mano": "lɔ́ɔ̀",     "pronunciation": "law",        "category": "science"},
    "air":     {"mano": "fɛ̀fɛ́",    "pronunciation": "feh-feh",    "category": "science"},
    "sun":     {"mano": "là",       "pronunciation": "lah",        "category": "science"},
    "moon":    {"mano": "kálá",     "pronunciation": "kah-lah",    "category": "science"},
    "star":    {"mano": "sàlá",     "pronunciation": "sah-lah",    "category": "science"},
    "rain":    {"mano": "ní-sà",    "pronunciation": "nee-sah",    "category": "science"},
    "tree":    {"mano": "wúlú",     "pronunciation": "woo-loo",    "category": "science"},
    "stone":   {"mano": "kúlú",     "pronunciation": "koo-loo",    "category": "science"},
    "iron":    {"mano": "nɛ̀ɛ́",     "pronunciation": "neh",        "category": "science"},
    "gold":    {"mano": "sáná",     "pronunciation": "sah-nah",    "category": "science"},
    "mountain":{"mano": "kpɔ́ŋ",    "pronunciation": "kpong",      "category": "science"},
    "river":   {"mano": "ní-wɛ̀lɛ́", "pronunciation": "nee-weh-leh","category": "science"},
    "animal":  {"mano": "nɛ́ná",    "pronunciation": "neh-nah",    "category": "science"},
    "bird":    {"mano": "wɔ̀nì",    "pronunciation": "woh-nee",    "category": "science"},
    "fish":    {"mano": "kpɔ̀lɔ̀",   "pronunciation": "kpoh-loh",   "category": "science"},
    "seed":    {"mano": "ɓìí",     "pronunciation": "bee",        "category": "science"},
    "leaf":    {"mano": "yíí",     "pronunciation": "yee",        "category": "science"},

    # ── Body & Health ──
    "body":    {"mano": "kɔ́",      "pronunciation": "koh",        "category": "health"},
    "head":    {"mano": "wúŋ",     "pronunciation": "woong",      "category": "health"},
    "hand":    {"mano": "kɛ́",      "pronunciation": "keh",        "category": "health"},
    "eye":     {"mano": "yá",      "pronunciation": "yah",        "category": "health"},
    "ear":     {"mano": "tóó",     "pronunciation": "toh",        "category": "health"},
    "mouth":   {"mano": "dá",      "pronunciation": "dah",        "category": "health"},
    "heart":   {"mano": "nìì",     "pronunciation": "nee",        "category": "health"},
    "blood":   {"mano": "yà",      "pronunciation": "yah",        "category": "health"},
    "bone":    {"mano": "kɔ̀lɔ̀",    "pronunciation": "koh-loh",    "category": "health"},
    "medicine":{"mano": "wàlé",    "pronunciation": "wah-leh",    "category": "health"},
    "sick":    {"mano": "kpànà",   "pronunciation": "kpah-nah",   "category": "health"},

    # ── Food & Agriculture ──
    "rice":    {"mano": "mɔ̀ní",    "pronunciation": "moh-nee",    "category": "food"},
    "cassava": {"mano": "yáká",    "pronunciation": "yah-kah",    "category": "food"},
    "palm oil":{"mano": "mɛ́ní",   "pronunciation": "meh-nee",    "category": "food"},
    "pepper":  {"mano": "pèpè",   "pronunciation": "peh-peh",    "category": "food"},
    "food":    {"mano": "mɔ́ɔ̀",     "pronunciation": "moh",        "category": "food"},
    "eat":     {"mano": "mɔ́ɔ̀ mɛ̀", "pronunciation": "moh meh",    "category": "food"},
    "farm":    {"mano": "kpɛ́",     "pronunciation": "kpeh",       "category": "food"},
    "harvest": {"mano": "wɔ́lɔ̀",   "pronunciation": "woh-loh",    "category": "food"},
    "plant":   {"mano": "dú",      "pronunciation": "doo",        "category": "food"},
    "banana":  {"mano": "bàná",    "pronunciation": "bah-nah",    "category": "food"},
    "corn":    {"mano": "kàá",     "pronunciation": "kah",        "category": "food"},

    # ── Family & Community ──
    "mother":  {"mano": "nàá",     "pronunciation": "nah",        "category": "family"},
    "father":  {"mano": "ɓàá",     "pronunciation": "bah",        "category": "family"},
    "child":   {"mano": "lóŋ",     "pronunciation": "long",       "category": "family"},
    "elder":   {"mano": "nùú-kpà", "pronunciation": "noo-kpah",   "category": "family"},
    "person":  {"mano": "nùú",     "pronunciation": "noo",        "category": "family"},
    "people":  {"mano": "nùú-sù",  "pronunciation": "noo-soo",    "category": "family"},
    "friend":  {"mano": "dɔ̀ɔ̀mɛ̀nù","pronunciation": "doh-meh-noo","category": "family"},
    "village": {"mano": "tàá",     "pronunciation": "tah",        "category": "family"},
    "house":   {"mano": "pɛ́lɛ́",   "pronunciation": "peh-leh",    "category": "family"},
    "woman":   {"mano": "lɔ́kɔ́",   "pronunciation": "loh-koh",    "category": "family"},
    "man":     {"mano": "kùnùú",   "pronunciation": "koo-noo",    "category": "family"},
    "brother": {"mano": "díé",     "pronunciation": "dee-eh",     "category": "family"},
    "sister":  {"mano": "díé-lɔ́kɔ́","pronunciation": "dee-eh loh-koh","category": "family"},

    # ── Actions & Verbs ──
    "go":      {"mano": "wà",      "pronunciation": "wah",        "category": "verbs"},
    "come":    {"mano": "pà",      "pronunciation": "pah",        "category": "verbs"},
    "see":     {"mano": "ké",      "pronunciation": "keh",        "category": "verbs"},
    "hear":    {"mano": "mɛ̀ní",    "pronunciation": "meh-nee",    "category": "verbs"},
    "say":     {"mano": "fò",      "pronunciation": "foh",        "category": "verbs"},
    "do":      {"mano": "kɛ́",      "pronunciation": "keh",        "category": "verbs"},
    "make":    {"mano": "kɛ́",      "pronunciation": "keh",        "category": "verbs"},
    "give":    {"mano": "ɓó",      "pronunciation": "boh",        "category": "verbs"},
    "take":    {"mano": "mɔ̀",      "pronunciation": "moh",        "category": "verbs"},
    "work":    {"mano": "wálá",    "pronunciation": "wah-lah",    "category": "verbs"},
    "help":    {"mano": "dɛ̀ɛ́",     "pronunciation": "deh",        "category": "verbs"},
    "sit":     {"mano": "sìgí",    "pronunciation": "see-gee",    "category": "verbs"},
    "stand":   {"mano": "lɔ̀",      "pronunciation": "loh",        "category": "verbs"},
    "walk":    {"mano": "táámà",   "pronunciation": "tah-mah",    "category": "verbs"},
    "run":     {"mano": "fé",      "pronunciation": "feh",        "category": "verbs"},

    # ── Descriptors ──
    "big":     {"mano": "gbɛ̀lɛ̀",  "pronunciation": "gbeh-leh",   "category": "descriptors"},
    "small":   {"mano": "wɛ́lɛ́",   "pronunciation": "weh-leh",    "category": "descriptors"},
    "good":    {"mano": "ɲɛ̀",     "pronunciation": "nyeh",       "category": "descriptors"},
    "bad":     {"mano": "yúgúlú",  "pronunciation": "yoo-goo-loo","category": "descriptors"},
    "hot":     {"mano": "gbàndá",  "pronunciation": "gbahn-dah",  "category": "descriptors"},
    "cold":    {"mano": "wìsí",    "pronunciation": "wee-see",    "category": "descriptors"},
    "long":    {"mano": "gbù",     "pronunciation": "gboo",       "category": "descriptors"},
    "short":   {"mano": "kútú",    "pronunciation": "koo-too",    "category": "descriptors"},
    "heavy":   {"mano": "gblé",    "pronunciation": "gbleh",      "category": "descriptors"},
    "light":   {"mano": "fɛ́fɛ́",   "pronunciation": "feh-feh",    "category": "descriptors"},
    "new":     {"mano": "kúlá",    "pronunciation": "koo-lah",    "category": "descriptors"},
    "old":     {"mano": "kɔ̀lɔ̀",    "pronunciation": "koh-loh",    "category": "descriptors"},
    "many":    {"mano": "wáá",     "pronunciation": "wah",        "category": "descriptors"},
    "few":     {"mano": "wɛ́lɛ́-wɛ́lɛ́","pronunciation": "weh-leh weh-leh","category": "descriptors"},
    "true":    {"mano": "tɔ́ɔ̀ná",  "pronunciation": "toh-nah",    "category": "descriptors"},
    "fast":    {"mano": "kpáná",   "pronunciation": "kpah-nah",   "category": "descriptors"},
    "slow":    {"mano": "mɔ̀lɔ̀-mɔ̀lɔ̀","pronunciation": "moh-loh moh-loh","category": "descriptors"},

    # ── Greetings & Expressions ──
    "hello":      {"mano": "ǎ ní gbɛ́",  "pronunciation": "ah nee gbeh",  "category": "greetings"},
    "thank you":  {"mano": "ǎ ní ɲɛ̀",   "pronunciation": "ah nee nyeh",  "category": "greetings"},
    "welcome":    {"mano": "ǎ pà ɲɛ̀",   "pronunciation": "ah pah nyeh",  "category": "greetings"},
    "goodbye":    {"mano": "ǎ nì tà",   "pronunciation": "ah nee tah",   "category": "greetings"},
    "good morning":{"mano":"ɓá kɔ̀ ɲɛ̀",  "pronunciation": "bah koh nyeh", "category": "greetings"},
    "how are you":{"mano": "ǎ kɛ́ dí",   "pronunciation": "ah keh dee",   "category": "greetings"},
    "I am fine":  {"mano": "ń kɛ́ ɲɛ̀",   "pronunciation": "n keh nyeh",   "category": "greetings"},
    "please":     {"mano": "yàá",       "pronunciation": "yah",          "category": "greetings"},
    "yes":        {"mano": "ɔ̃́ɔ̃̀",       "pronunciation": "ohn",          "category": "greetings"},
    "no":         {"mano": "ǎ-à",       "pronunciation": "ah-ah",        "category": "greetings"},

    # ── Time & Calendar ──
    "today":     {"mano": "bì",       "pronunciation": "bee",        "category": "time"},
    "tomorrow":  {"mano": "sínì",     "pronunciation": "see-nee",    "category": "time"},
    "yesterday": {"mano": "kúnɛ̀",    "pronunciation": "koo-neh",    "category": "time"},
    "morning":   {"mano": "ɓɛ́ɛ́lɛ̀",   "pronunciation": "beh-leh",    "category": "time"},
    "evening":   {"mano": "kpɛ̀ní",   "pronunciation": "kpeh-nee",   "category": "time"},
    "night":     {"mano": "kpɛ̀",     "pronunciation": "kpeh",       "category": "time"},
    "day":       {"mano": "là-ɲáná", "pronunciation": "lah-nyah-nah","category": "time"},
    "year":      {"mano": "sàn",     "pronunciation": "sahn",       "category": "time"},
}

# ── Common Phrases for Classroom Use ──────────────────────────────────
MANO_PHRASES = [
    {"english": "Open your books", "mano": "Á bɛ́ì-nù kàà", "context": "Classroom instruction"},
    {"english": "Listen carefully", "mano": "Á tóó dò", "context": "Getting attention"},
    {"english": "Do you understand?", "mano": "Á mɛ́nì à?", "context": "Checking comprehension"},
    {"english": "Let us learn", "mano": "Kà kàlà", "context": "Starting a lesson"},
    {"english": "Very good!", "mano": "Ɲɛ̀ gbɛ̀lɛ̀!", "context": "Praise/encouragement"},
    {"english": "Try again", "mano": "Á kɛ́ dóó", "context": "Encouragement after mistake"},
    {"english": "Write it down", "mano": "Á sɛ̀bɛ̀ à", "context": "Note-taking instruction"},
    {"english": "Raise your hand", "mano": "Á kɛ́ sàngá", "context": "Classroom management"},
    {"english": "Work together", "mano": "Kà wálá kɔ̃̀", "context": "Group work instruction"},
    {"english": "Well done!", "mano": "Á wálá ɲɛ̀!", "context": "Praise after task completion"},
    {"english": "Be quiet", "mano": "Á tɔ́ŋ", "context": "Classroom management"},
    {"english": "Come to the board", "mano": "Á pà bɔ́ɔ́dù yà", "context": "Student participation"},
    {"english": "Who knows the answer?", "mano": "Wàá lɔ́n jàbí?", "context": "Questioning technique"},
    {"english": "Let us count together", "mano": "Kà yálá kɔ̃̀", "context": "Math engagement"},
    {"english": "Read aloud", "mano": "Á kàlà gbɛ̀lɛ̀", "context": "Reading instruction"},
]

# ── Cultural Context Notes ────────────────────────────────────────────
MANO_CULTURAL = {
    "proverbs": [
        {"mano": "Nùú dɔ́ kɛ́ sè tàá gblàá", "english": "One person's hand cannot build a village", "lesson": "Cooperation/teamwork"},
        {"mano": "Wúlú gbɛ̀lɛ̀ ɓìí wɛ́lɛ́ kɛ̀ pà", "english": "A big tree comes from a small seed", "lesson": "Growth/patience in learning"},
        {"mano": "Ní sè kɔ́ sè fé", "english": "Water does not flow uphill", "lesson": "Natural laws/physics"},
        {"mano": "Yá fèlè ké gbɛ̀lɛ̀ dɔ́ yá dɔ́ kà", "english": "Two eyes see more than one", "lesson": "Perspective/collaboration"},
        {"mano": "Kɛ́ lɔ́n kɛ́ kɛ́, kɛ́ sè lɔ́n kɛ́ kàlà", "english": "What the hand knows, it does; what it doesn't know, it must learn", "lesson": "Value of education"},
    ],
    "counting_system": "Mano uses a base-5/base-20 counting system. Numbers 6-9 are built from 5+1, 5+2, etc. This is a rich entry point for teaching number systems and mathematical patterns.",
    "learning_tradition": "In Mano culture, knowledge passes through storytelling, proverbs, and hands-on apprenticeship. Effective teaching connects new concepts to familiar stories and practical skills like farming, weaving, or blacksmithing.",
    "respect_customs": "Address elders and teachers with respect prefixes. In Mano classroom culture, students stand to answer questions and show respect through attentive listening before speaking.",
}


def get_mano_stats():
    """Return summary statistics about the Mano dictionary."""
    categories = {}
    for word, info in MANO_DICT.items():
        cat = info.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "total": len(MANO_DICT),
        "categories": sorted(categories.keys()),
        "category_counts": categories,
        "phrases": len(MANO_PHRASES),
        "proverbs": len(MANO_CULTURAL.get("proverbs", [])),
    }


def match_vocabulary(text, limit=10):
    """
    Find Mano vocabulary words that match English words in the given text.
    Returns a list of (english_word, mano_info) tuples.
    """
    text_lower = text.lower()
    matches = []
    for eng, info in MANO_DICT.items():
        if eng.lower() in text_lower:
            matches.append((eng, info))
    # Sort by relevance (longer matches first, then alphabetical)
    matches.sort(key=lambda x: (-len(x[0]), x[0]))
    return matches[:limit]


def get_mano_preview(topic=""):
    """
    Return a formatted preview string showing relevant Mano vocabulary
    for a given topic, for display in the sidebar.
    """
    if topic:
        matches = match_vocabulary(topic, limit=5)
        if matches:
            lines = []
            for eng, info in matches:
                lines.append(f"  {eng} → {info['mano']} ({info['pronunciation']})")
            return "\n".join(lines)
    # Default: show some common school words
    school_words = [(e, i) for e, i in MANO_DICT.items() if i["category"] == "education"][:5]
    return "\n".join(f"  {e} → {i['mano']} ({i['pronunciation']})" for e, i in school_words)


def build_mano_prompt_context(topic="", subject=""):
    """
    Build a prompt context block that instructs the AI to include
    Mano language vocabulary and cultural references in its response.
    """
    lines = []
    lines.append("=" * 50)
    lines.append("MANO LANGUAGE (MAA) — BILINGUAL LESSON SUPPORT")
    lines.append("=" * 50)
    lines.append("The students speak Mano (Maa) as their first language.")
    lines.append("Include Mano vocabulary throughout your response to build bilingual literacy.")
    lines.append("")

    # Match topic-relevant vocabulary
    search_text = f"{topic} {subject}"
    matches = match_vocabulary(search_text, limit=8)
    if matches:
        lines.append("RELEVANT MANO VOCABULARY:")
        for eng, info in matches:
            lines.append(f"  • {eng} = {info['mano']} (say: {info['pronunciation']})")
        lines.append("")

    # Add classroom phrases
    lines.append("USEFUL MANO CLASSROOM PHRASES:")
    for phrase in MANO_PHRASES[:6]:
        lines.append(f"  • \"{phrase['english']}\" = \"{phrase['mano']}\" ({phrase['context']})")
    lines.append("")

    # Add a relevant proverb
    proverbs = MANO_CULTURAL.get("proverbs", [])
    if proverbs:
        # Pick a contextually relevant proverb if possible
        import random
        proverb = random.choice(proverbs)
        lines.append("MANO PROVERB TO WEAVE INTO THE LESSON:")
        lines.append(f"  \"{proverb['mano']}\"")
        lines.append(f"  Meaning: \"{proverb['english']}\"")
        lines.append(f"  Teaching connection: {proverb['lesson']}")
        lines.append("")

    # Cultural teaching notes
    lines.append("CULTURAL TEACHING NOTES:")
    lines.append(f"  • {MANO_CULTURAL['counting_system']}")
    lines.append(f"  • {MANO_CULTURAL['learning_tradition']}")
    lines.append("")

    lines.append("INSTRUCTIONS: Naturally weave Mano words into your lesson.")
    lines.append("Format: English word (Mano: mano_word, say: pronunciation)")
    lines.append("Start or end with a relevant Mano greeting or proverb.")
    lines.append("=" * 50)

    return "\n".join(lines)


# ── Quick self-test ────────────────────────────────────────────────────
if __name__ == "__main__":
    stats = get_mano_stats()
    print(f"Mano Dictionary: {stats['total']} words across {len(stats['categories'])} categories")
    print(f"Categories: {', '.join(stats['categories'])}")
    print(f"Phrases: {stats['phrases']}")
    print(f"Proverbs: {stats['proverbs']}")
    print()
    print("Sample context block for 'force and motion':")
    print(build_mano_prompt_context("force and motion", "Physics"))
