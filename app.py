"""
========================================================================
TEACHER PEHPEH — AI-Powered Classroom Assistant for Liberian Teachers
========================================================================
Multi-model (Claude + ChatGPT + Gemini) educational support platform
with Liberia Ministry of Education curriculum alignment.

Built by the Institute of Basic Technology (IBT)
Co-founded by Rodney Bollie & Dr. Sylvia Bollie

Drop your logo file in this folder as "logo.png" to brand the app.
Drop Ministry of Education curriculum JSON files into curriculum_data/
to enable curriculum-aligned content generation.
========================================================================
"""

import streamlit as st
import time
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# =====================================================================
# API KEYS — Paste your keys here
# =====================================================================
OPENAI_API_KEY    = ""   # sk-...
ANTHROPIC_API_KEY = ""   # sk-ant-...
GOOGLE_API_KEY    = ""   # AIzaSy...

# =====================================================================
# LOGO — Put your logo file in the same folder as this script
# =====================================================================
LOGO_FILENAME = "logo.png"

# =====================================================================
# CURRICULUM — Load Ministry of Education data
# =====================================================================
# Add the app directory to path so curriculum module can be found
APP_DIR = Path(__file__).parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

try:
    from curriculum import (
        load_all_curricula,
        get_grade_topics,
        get_topic_details,
        build_curriculum_context,
        get_curriculum_summary,
        get_available_subjects,
    )
    CURRICULUM_AVAILABLE = True
except ImportError:
    CURRICULUM_AVAILABLE = False

# Load curriculum data at startup
CURRICULA = {}
if CURRICULUM_AVAILABLE:
    CURRICULA = load_all_curricula()

# =====================================================================
# IMPORTS — AI Libraries
# =====================================================================
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


# =====================================================================
# DROPDOWN OPTIONS
# =====================================================================

REGIONS = {
    "Urban": "urban area with relatively better access to resources and infrastructure",
    "Peri-Urban": "peri-urban area with mixed access to resources",
    "Rural": "rural area with limited access to resources and technology",
    "Remote / Island": "remote or island community with very limited infrastructure",
}

COUNTRIES = [
    "Liberia", "Sierra Leone", "Ghana", "Nigeria", "Kenya",
    "Uganda", "Tanzania", "Ethiopia", "Senegal", "Cameroon",
    "Gambia", "Guinea", "Côte d'Ivoire", "Mali", "Burkina Faso",
    "Rwanda", "Malawi", "Zambia", "Zimbabwe", "Mozambique",
    "South Africa", "Botswana", "Namibia", "DRC", "Angola",
    "Togo", "Benin", "Niger", "Chad", "Somalia",
]

GRADE_LEVELS = {
    "Grade 7 (JHS 1)": 7,
    "Grade 8 (JHS 2)": 8,
    "Grade 9 (JHS 3 / BECE Level)": 9,
    "Grade 10 (SHS 1)": 10,
    "Grade 11 (SHS 2)": 11,
    "Grade 12 (SHS 3 / WASSCE Level)": 12,
}

SUBJECTS = [
    "Mathematics", "English Language", "Integrated Science",
    "Social Studies", "Physics", "Chemistry", "Biology",
    "Economics", "Government / Civics", "Literature in English",
    "History", "Geography", "Agriculture", "French",
    "Religious Studies", "Business Management", "Accounting",
    "Computer Studies / ICT", "Technical Drawing",
    "Home Economics", "Physical Education", "Art / Creative Arts", "Music",
]

# Fallback topics when no curriculum data exists for a subject
FALLBACK_TOPICS = {
    "Physics": [
        "Measurement and Units", "Scalars and Vectors",
        "Motion (Kinematics)", "Newton's Laws of Motion",
        "Work, Energy and Power", "Simple Machines",
        "Thermal Physics", "Gas Laws",
        "Electrostatics", "Current Electricity",
        "Magnetism", "Electromagnetic Induction",
        "Waves and Sound", "Light and Optics",
        "Refraction and Lenses", "Nuclear Physics",
        "Electronics", "Quantum Physics",
    ],
    "Mathematics": [
        "Number and Numeration", "Fractions and Decimals", "Percentages",
        "Ratio and Proportion", "Algebraic Expressions", "Linear Equations",
        "Quadratic Equations", "Simultaneous Equations", "Inequalities",
        "Sets and Venn Diagrams", "Functions and Relations",
        "Sequences and Series", "Matrices", "Trigonometry",
        "Mensuration", "Statistics and Probability",
        "Geometry (Plane and Solid)", "Vectors", "Calculus (Introduction)",
    ],
    "English Language": [
        "Comprehension and Summary", "Essay Writing (Narrative)",
        "Essay Writing (Descriptive)", "Essay Writing (Argumentative)",
        "Essay Writing (Expository)", "Letter Writing (Formal)",
        "Letter Writing (Informal)", "Speech Writing", "Report Writing",
        "Grammar (Parts of Speech)", "Grammar (Tenses)",
        "Grammar (Sentence Structure)", "Vocabulary Development",
        "Oral English and Phonetics", "Literature Appreciation",
        "Reading Skills", "Listening and Note-Taking",
    ],
    "Chemistry": [
        "Introduction to Chemistry", "States of Matter",
        "Atomic Structure", "Periodic Table",
        "Chemical Bonding", "Chemical Equations",
        "Acids, Bases and Salts", "Redox Reactions",
        "Electrochemistry", "Energy Changes",
        "Rates of Reaction", "Chemical Equilibrium",
        "Carbon and Its Compounds", "Metals and Their Compounds",
        "Non-Metals", "Environmental Chemistry",
    ],
    "Biology": [
        "Cell Biology", "Classification of Living Things",
        "Nutrition", "Transport in Living Things",
        "Respiration", "Excretion",
        "Reproduction (Plants)", "Reproduction (Animals/Humans)",
        "Growth and Development", "Genetics and Heredity",
        "Evolution", "Ecology and Environment",
        "Microorganisms and Disease", "Biotechnology",
    ],
    "Integrated Science": [
        "Scientific Method", "Measurement", "Matter",
        "Energy", "Force and Motion", "Electricity",
        "Light and Sound", "Heat and Temperature",
        "Living Things", "Ecology", "Health and Disease",
        "Earth Science", "Space and the Solar System",
    ],
}

TASK_TYPES = {
    "📝 Lesson Plan": "a complete, detailed lesson plan",
    "📋 Scheme of Work (Weekly)": "a one-week scheme of work with daily breakdowns",
    "📋 Scheme of Work (Termly)": "a full-term scheme of work with weekly topics and objectives",
    "📊 Quiz (10 Questions)": "a 10-question quiz with answer key",
    "📊 Quiz (20 Questions)": "a 20-question quiz with answer key",
    "📝 WASSCE Paper 1 (Objectives)": "a WASSCE-style Paper 1 objective test with 50 multiple-choice questions and answer key",
    "📝 WASSCE Paper 2 (Theory/Essay)": "a WASSCE-style Paper 2 theory/essay paper with structured and essay questions plus marking scheme",
    "📝 BECE Exam Practice": "a BECE-style examination paper with objective and theory sections",
    "📚 Homework Assignment": "a homework assignment appropriate for the level",
    "👥 Group Activity": "a group activity or collaborative learning exercise",
    "🎯 Rubric / Marking Guide": "a detailed rubric or marking guide",
    "📬 Parent Communication Letter": "a professional letter to parents about student progress or classroom matters",
    "🔁 Remedial / Catch-Up Material": "remedial or catch-up material for struggling students",
    "🎮 Educational Game / Activity": "an educational game or interactive classroom activity",
    "📖 Reading Comprehension Exercise": "a reading comprehension passage with questions",
    "🧪 Lab / Practical Guide": "a laboratory or practical activity guide with procedure and questions",
    "📑 Student Progress Report Template": "a student progress report template with relevant criteria",
    "🧠 Differentiated Instruction Plan": "a differentiated instruction plan addressing multiple ability levels",
    "🌍 Real-World Application Worksheet": "a worksheet connecting the topic to real-world Liberian/African contexts",
    "📢 Class Presentation Guide": "a guide for student presentations on this topic",
}

CLASS_SIZES = [
    "Small (under 25)", "Medium (25-40)", "Large (40-60)",
    "Very Large (60-100)", "Overcrowded (100+)",
]

RESOURCES = [
    "Textbooks only", "Textbooks + chalkboard",
    "Basic supplies (paper, pens, ruler)",
    "Some lab equipment", "Full lab access",
    "Computer / tablet access", "Internet access",
    "No materials (teacher knowledge only)",
]

LANGUAGES = [
    "English only", "English + Liberian English (Koloqua)",
    "English + local language support", "Bilingual instruction",
]

ABILITY_LEVELS = [
    "Mixed abilities", "Below grade level",
    "At grade level", "Above grade level",
    "Wide range (remedial to advanced)",
]

TIME_OPTIONS = [
    "30 minutes", "45 minutes", "1 hour",
    "1.5 hours", "2 hours", "Double period",
]


# =====================================================================
# SYSTEM PROMPT — The heart of Teacher Pehpeh
# =====================================================================

def build_system_prompt(country, region_desc, grade, subject, class_size,
                        resources, language, ability, time_avail,
                        curriculum_context=""):
    """Build the system prompt with optional curriculum injection."""

    curriculum_block = ""
    if curriculum_context:
        curriculum_block = f"""

CRITICAL — MINISTRY OF EDUCATION CURRICULUM DATA:
The following is the OFFICIAL curriculum from Liberia's Ministry of Education
for this exact topic. You MUST align your response with these objectives,
content requirements, and suggested activities. This is not optional — 
teachers are evaluated against these standards.

{curriculum_context}

When generating content, you MUST:
1. Address ALL specific learning objectives listed above
2. Follow the content outline structure
3. Incorporate the suggested activities where appropriate
4. Use the local contextualization examples to make content relevant
5. Reference recommended textbooks when suggesting further reading
6. Ensure assessment aligns with the approved assessment strategies
7. Build toward the expected competencies listed
"""

    return f"""You are Teacher Pehpeh — a culturally contextualized AI teaching assistant 
built by the Institute of Basic Technology (IBT) for teachers in Liberia and 
across West Africa.

You are named after the Liberian concept of "Pehpeh" (pepper) — the strict, 
passionate, demanding teacher who believes deeply in their students' potential.

CONTEXT FOR THIS REQUEST:
- Country: {country}
- Setting: {region_desc}
- Grade Level: {grade}
- Subject: {subject}
- Class Size: {class_size}
- Available Resources: {resources}
- Language Context: {language}
- Student Ability Level: {ability}
- Time Available: {time_avail}
{curriculum_block}

YOUR CORE PRINCIPLES:
1. LIBERIAN CONTEXT FIRST: Use examples, references, and scenarios from 
   Liberian daily life. Reference local places (Monrovia, Buchanan, Nimba, 
   Bong, Lofa, Grand Bassa), local foods (cassava, palm butter, pepper soup, 
   dumboy), local currency (Liberian dollars), local transportation (kekeh, 
   penpens, public buses), and local culture.

2. RESOURCE-AWARE: Design everything to work with the stated available 
   resources. If the teacher has no lab equipment, suggest locally available 
   alternatives (bottles, sticks, rubber bands, stones, water, cooking pots).
   Never assume access to technology unless stated.

3. WASSCE/BECE ALIGNED: All academic content should prepare students for 
   the West African Senior School Certificate Examination (WASSCE) or Basic 
   Education Certificate Examination (BECE) as appropriate for the grade.

4. CULTURALLY RESPECTFUL: Be aware of Liberian sociocultural norms. 
   Use Liberian English (Koloqua) examples where appropriate to connect 
   with students, while teaching standard English.

5. PRACTICAL AND ACTIONABLE: Every output should be immediately usable 
   by a teacher. No theoretical abstractions — give concrete steps, exact 
   questions, specific examples, and clear instructions.

6. INCLUSIVE EDUCATION: Design activities for mixed-gender groups, 
   accommodate different learning styles, and be sensitive to students 
   from different socioeconomic backgrounds.

7. LARGE CLASS STRATEGIES: When class sizes are large, include specific 
   strategies for managing and engaging all students (group work rotation, 
   peer teaching, call-and-response, etc.).

FORMAT: Use clear headings, numbered steps, and organized sections.
Make everything copy-paste ready for the teacher to use immediately.
"""


# =====================================================================
# AI MODEL CALLS
# =====================================================================

def call_chatgpt(prompt, system_prompt):
    """Call OpenAI ChatGPT."""
    if not OPENAI_AVAILABLE or not OPENAI_API_KEY:
        return None
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ ChatGPT error: {str(e)}"


def call_claude(prompt, system_prompt):
    """Call Anthropic Claude."""
    if not ANTHROPIC_AVAILABLE or not ANTHROPIC_API_KEY:
        return None
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except Exception as e:
        return f"⚠️ Claude error: {str(e)}"


def call_gemini(prompt, system_prompt):
    """Call Google Gemini."""
    if not GEMINI_AVAILABLE or not GOOGLE_API_KEY:
        return None
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=system_prompt,
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"


def query_all_models(prompt, system_prompt):
    """Query all available models in parallel."""
    responses = {}
    tasks = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        if OPENAI_AVAILABLE and OPENAI_API_KEY:
            tasks["chatgpt"] = executor.submit(call_chatgpt, prompt, system_prompt)
        if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
            tasks["claude"] = executor.submit(call_claude, prompt, system_prompt)
        if GEMINI_AVAILABLE and GOOGLE_API_KEY:
            tasks["gemini"] = executor.submit(call_gemini, prompt, system_prompt)

        for name, future in tasks.items():
            try:
                responses[name] = future.result(timeout=60)
            except Exception as e:
                responses[name] = f"⚠️ {name} timed out: {str(e)}"

    return responses


def synthesize_responses(responses, task_label, topic, grade):
    """Pick the best response or synthesize from multiple."""
    valid = {k: v for k, v in responses.items()
             if v and not str(v).startswith("⚠️")}

    if not valid:
        return "⚠️ No AI models returned a response. Please check your API keys."

    if len(valid) == 1:
        return list(valid.values())[0]

    # Use the longest substantive response as primary
    primary_name = max(valid, key=lambda k: len(str(valid[k])))
    return valid[primary_name]


# =====================================================================
# HELPER: Get topics for current grade + subject
# =====================================================================

def get_topics_for_selection(subject, grade_number):
    """
    Return topics for the dropdown. If curriculum data exists for this
    subject + grade, use it. Otherwise fall back to generic topics.
    """
    # Try curriculum data first
    if CURRICULA and CURRICULUM_AVAILABLE:
        subject_key = subject.strip().lower()
        if subject_key in CURRICULA:
            topics = get_grade_topics(CURRICULA, subject, grade_number)
            if topics:
                return topics, True  # True = curriculum-aligned

    # Fall back to generic topics
    fallback = FALLBACK_TOPICS.get(subject, [
        "Introduction / Fundamentals",
        "Core Concepts",
        "Applications and Problem Solving",
        "Review and Exam Preparation",
    ])
    return fallback, False


# =====================================================================
# BUILD THE TASK PROMPT
# =====================================================================

def build_task_prompt(task_label, task_desc, subject, topic, grade,
                      class_size, time_avail, curriculum_details=None):
    """Build the user prompt for the AI models."""

    prompt = f"""Generate {task_desc} for the following:

Subject: {subject}
Topic: {topic}
Grade: {grade}
Class Size: {class_size}
Time Available: {time_avail}
"""

    # If we have curriculum details, add specific guidance
    if curriculum_details:
        objectives = curriculum_details.get("specific_objectives", [])
        if objectives:
            prompt += "\nThis lesson must address these specific learning objectives:\n"
            for i, obj in enumerate(objectives, 1):
                prompt += f"  {i}. {obj}\n"

        local_notes = curriculum_details.get("local_contextualization_notes", "")
        if local_notes:
            prompt += f"\nContextualization guidance: {local_notes}\n"

        materials = curriculum_details.get("lab_materials", [])
        if materials:
            prompt += f"\nAvailable lab materials: {', '.join(materials)}\n"

    prompt += """
Make it immediately usable — a teacher should be able to take this output
straight into their classroom. Include all necessary details, examples, 
questions, and answers where applicable.

Use Liberian context throughout: local examples, familiar scenarios, 
culturally relevant references, and language appropriate for Liberian students.
"""
    return prompt


# =====================================================================
# STREAMLIT APP
# =====================================================================

def main():
    st.set_page_config(
        page_title="Teacher Pehpeh",
        page_icon="🌶️",
        layout="wide",
    )

    # ── Styling ──────────────────────────────────────────────────────
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:wght@600;700&display=swap');

        .stApp { font-family: 'DM Sans', sans-serif; }

        .app-header {
            text-align: center;
            padding: 0.5rem 0 1rem 0;
        }
        .app-header h1 {
            font-family: 'Fraunces', serif;
            color: #1B5E20;
            font-size: 2.2rem;
            margin: 0;
        }
        .app-header p {
            color: #555;
            font-size: 1rem;
            margin: 0.3rem 0 0 0;
        }

        .status-bar {
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
            border-left: 4px solid #2E7D32;
            padding: 0.7rem 1rem;
            border-radius: 6px;
            margin: 0.5rem 0 1rem 0;
            font-size: 0.88rem;
            color: #1B5E20;
        }

        .curriculum-badge {
            display: inline-block;
            background: linear-gradient(135deg, #1B5E20, #388E3C);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            margin: 4px 0;
        }
        .curriculum-badge-none {
            display: inline-block;
            background: #FF8F00;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            margin: 4px 0;
        }

        .result-header {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px 10px 0 0;
            margin-top: 1.5rem;
        }
        .result-header h3 { margin: 0; color: white; font-family: 'Fraunces', serif; }
        .result-header p { margin: 0.3rem 0 0 0; opacity: 0.85; font-size: 0.85rem; }

        .result-body {
            border: 1px solid #C8E6C9;
            border-top: none;
            border-radius: 0 0 10px 10px;
            padding: 1.5rem;
            background: #FAFAFA;
        }

        .app-footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            color: #888;
            font-size: 0.85rem;
            border-top: 1px solid #eee;
            margin-top: 2rem;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stRadio label {
            font-weight: 500;
        }

        .curriculum-info {
            background: #F1F8E9;
            border: 1px solid #C5E1A5;
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.5rem 0;
            font-size: 0.82rem;
            color: #33691E;
        }
    </style>
    """, unsafe_allow_html=True)

    # ── Logo / Header ────────────────────────────────────────────────
    logo_path = APP_DIR / LOGO_FILENAME
    if logo_path.exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(logo_path), use_container_width=True)
        st.markdown('<p style="text-align:center; color:#555; margin-top:-10px;">'
                    'AI-Powered Teaching Assistant · Aligned to Liberia MOE Curriculum</p>',
                    unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="app-header">
            <h1>🌶️ Teacher Pehpeh</h1>
            <p>AI-Powered Teaching Assistant · Aligned to Liberia Ministry of Education Curriculum</p>
        </div>
        """, unsafe_allow_html=True)

    # ── API key check ────────────────────────────────────────────────
    active_models = []
    if OPENAI_AVAILABLE and OPENAI_API_KEY:
        active_models.append("ChatGPT")
    if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
        active_models.append("Claude")
    if GEMINI_AVAILABLE and GOOGLE_API_KEY:
        active_models.append("Gemini")

    if not active_models:
        st.error("⚠️ **No API keys configured.** Open `app.py` and paste your API keys near the top.")
        return

    # ── Status bar ───────────────────────────────────────────────────
    curriculum_subjects = get_available_subjects(CURRICULA) if CURRICULA else []
    curriculum_note = ""
    if curriculum_subjects:
        curriculum_note = f" · 📘 Curriculum loaded: {', '.join(curriculum_subjects)}"

    st.markdown(f"""
    <div class="status-bar">
        ✅ <strong>{len(active_models)} AI model(s) active:</strong> {', '.join(active_models)}
        {curriculum_note}
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar: Classroom Context ───────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Classroom Context")
        st.markdown("*Set once — these shape every response.*")

        country = st.selectbox("🌍 Country", COUNTRIES, index=0)
        region = st.selectbox("📍 Setting", list(REGIONS.keys()), index=0)
        grade_label = st.selectbox("🎓 Grade Level", list(GRADE_LEVELS.keys()), index=3)
        grade_number = GRADE_LEVELS[grade_label]

        subject = st.selectbox("📚 Subject", SUBJECTS, index=4)  # Default: Physics
        class_size = st.selectbox("👥 Class Size", CLASS_SIZES, index=2)
        resources = st.selectbox("🔧 Available Resources", RESOURCES, index=1)
        language = st.selectbox("🗣️ Language Context", LANGUAGES, index=1)
        ability = st.selectbox("📊 Student Ability Level", ABILITY_LEVELS, index=0)
        time_avail = st.selectbox("⏱️ Time Available", TIME_OPTIONS, index=2)

        # Curriculum info in sidebar
        if CURRICULA and CURRICULUM_AVAILABLE:
            st.markdown("---")
            st.markdown("### 📘 Loaded Curricula")
            st.markdown(f'<div class="curriculum-info">{get_curriculum_summary(CURRICULA)}</div>',
                        unsafe_allow_html=True)
            st.markdown("*Drop more subject JSONs into `curriculum_data/` to expand.*")

    # ── Main Area: Task Selection ────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        task_key = st.selectbox("🎯 What do you need?", list(TASK_TYPES.keys()))
        task_label = task_key.split(" ", 1)[1] if " " in task_key else task_key
        task_desc = TASK_TYPES[task_key]

    with col2:
        # Dynamic topics based on grade + subject + curriculum
        topics, is_curriculum_aligned = get_topics_for_selection(subject, grade_number)

        if is_curriculum_aligned:
            st.markdown('<span class="curriculum-badge">✅ MOE Curriculum-Aligned Topics</span>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<span class="curriculum-badge-none">⚡ General Topics (No MOE data yet)</span>',
                        unsafe_allow_html=True)

        topic = st.selectbox("📖 Topic", topics)

    # ── Curriculum preview (expandable) ──────────────────────────────
    curriculum_details = None
    curriculum_context = ""
    if is_curriculum_aligned and CURRICULA:
        curriculum_details = get_topic_details(CURRICULA, subject, grade_number, topic)
        curriculum_context = build_curriculum_context(CURRICULA, subject, grade_number, topic)

        if curriculum_details:
            with st.expander("📋 View Ministry of Education Requirements for This Topic"):
                objectives = curriculum_details.get("specific_objectives", [])
                if objectives:
                    st.markdown("**Learning Objectives (students will be able to):**")
                    for obj in objectives:
                        st.markdown(f"- {obj}")

                content = curriculum_details.get("content_outline", [])
                if content:
                    st.markdown("**Content Outline:**")
                    for item in content:
                        st.markdown(f"- {item}")

                activities = curriculum_details.get("suggested_activities", [])
                if activities:
                    st.markdown("**Suggested Activities:**")
                    for act in activities:
                        st.markdown(f"- {act}")

                local_notes = curriculum_details.get("local_contextualization_notes", "")
                if local_notes:
                    st.markdown(f"**Liberian Contextualization:** {local_notes}")

                materials = curriculum_details.get("lab_materials", [])
                if materials:
                    st.markdown(f"**Lab Materials:** {', '.join(materials)}")

    # ── Advanced options ─────────────────────────────────────────────
    with st.expander("⚙️ Advanced Options"):
        col_a, col_b = st.columns(2)
        with col_a:
            include_diff = st.checkbox("Include differentiation strategies", value=True)
            include_wassce = st.checkbox("Align to WASSCE standards", value=True)
        with col_b:
            include_local = st.checkbox("Maximize Liberian context", value=True)
            include_assessment = st.checkbox("Include assessment criteria", value=True)

    # ── Generate Button ──────────────────────────────────────────────
    st.markdown("")
    generate = st.button("🌶️ Generate with Teacher Pehpeh", use_container_width=True, type="primary")

    if generate:
        # Build prompts
        region_desc = REGIONS[region]
        system = build_system_prompt(
            country, region_desc, grade_label, subject, class_size,
            resources, language, ability, time_avail, curriculum_context
        )
        prompt = build_task_prompt(
            task_label, task_desc, subject, topic, grade_label,
            class_size, time_avail, curriculum_details
        )

        # Add advanced options to prompt
        extras = []
        if include_diff:
            extras.append("Include differentiation strategies for multiple ability levels.")
        if include_wassce and grade_number >= 10:
            extras.append("Ensure alignment with WASSCE examination standards and question formats.")
        if include_local:
            extras.append("Maximize use of Liberian/West African real-world examples and cultural context.")
        if include_assessment:
            extras.append("Include clear assessment criteria or a marking guide.")
        if extras:
            prompt += "\n\nAdditional requirements:\n" + "\n".join(f"- {e}" for e in extras)

        # Progress indicator
        progress = st.empty()
        with progress.container():
            st.info(f"🌶️ Teacher Pehpeh is working... querying {len(active_models)} AI model(s)")
            bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                bar.progress(i + 1)

        # Query models
        responses = query_all_models(prompt, system)
        result = synthesize_responses(responses, task_label, topic, grade_label)
        progress.empty()

        # ── Display Result ───────────────────────────────────────────
        context_line = f"{grade_label} · {subject} · {topic} · {task_label}"
        alignment_tag = " · ✅ MOE Aligned" if is_curriculum_aligned else ""

        st.markdown(f"""
        <div class="result-header">
            <h3>🌶️ {task_label} — {topic}</h3>
            <p>{context_line}{alignment_tag} · {region} · {country}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="result-body">', unsafe_allow_html=True)
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download
        safe_name = f"{task_label}_{subject}_{topic}".replace(" ", "_").replace("/", "-")
        safe_name = "".join(c for c in safe_name if c.isalnum() or c in "_-").lower()
        st.download_button(
            label="📥 Download as Text File",
            data=result,
            file_name=f"teacher_pehpeh_{safe_name}.txt",
            mime="text/plain",
        )

        # Show individual model responses
        valid = {k: v for k, v in responses.items() if v and not str(v).startswith("⚠️")}
        if len(valid) > 1:
            with st.expander("🔍 View individual AI model responses"):
                for model_name, resp in valid.items():
                    st.markdown(f"**{model_name.upper()}**")
                    st.markdown(resp)
                    st.markdown("---")

    # ── Footer ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="app-footer">
        Built with 🌶️ by the <strong>Institute of Basic Technology (IBT)</strong><br>
        Teacher Pehpeh — For the teacher who stays late. For the student who keeps showing up.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
