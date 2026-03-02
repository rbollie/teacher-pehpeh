"""
========================================================================
CURRICULUM MODULE - Loads and serves Ministry of Education curriculum data
========================================================================
Drop new subject JSON files into the curriculum_data/ folder.
Each file follows the same structure as physics.json.

This module automatically discovers all available curricula and provides
grade-specific topics, objectives, and activities for AI prompt injection.
========================================================================
"""

import json
import os
from pathlib import Path

# ── Location of curriculum JSON files ──────────────────────────────────
CURRICULUM_DIR = Path(__file__).parent / "curriculum_data"


def load_all_curricula():
    """
    Scan the curriculum_data/ folder and load every JSON file.
    Returns a dict keyed by subject name (lowercase).
    Example: {"physics": {…}, "chemistry": {…}}
    """
    curricula = {}
    if not CURRICULUM_DIR.exists():
        return curricula

    for filepath in sorted(CURRICULUM_DIR.glob("*.json")):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            subject_key = data.get("subject", filepath.stem).strip().lower()
            curricula[subject_key] = data
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[Curriculum] Warning: Could not load {filepath.name}: {e}")
    return curricula


def get_available_subjects(curricula):
    """Return a sorted list of subject names that have curriculum data."""
    return sorted(
        [c["subject"] for c in curricula.values()],
        key=str.lower,
    )


def get_grade_topics(curricula, subject, grade_number):
    """
    Given a subject name and grade number (10, 11, or 12),
    return a list of topic strings for that grade, in semester order.
    """
    subject_key = subject.strip().lower()
    if subject_key not in curricula:
        return []

    grade_data = curricula[subject_key].get("grades", {}).get(str(grade_number))
    if not grade_data:
        return []

    topics = []
    for sem_key in sorted(grade_data.get("semesters", {}).keys()):
        semester = grade_data["semesters"][sem_key]
        for period in semester.get("periods", []):
            topic = period.get("topic", "")
            if topic and topic not in topics:
                topics.append(topic)
    return topics


def get_topic_details(curricula, subject, grade_number, topic_name):
    """
    Return the full curriculum detail block for a specific topic.
    Returns a dict with objectives, content_outline, activities, 
    lab_materials, and local_contextualization_notes.
    Returns None if not found.
    """
    subject_key = subject.strip().lower()
    if subject_key not in curricula:
        return None

    grade_data = curricula[subject_key].get("grades", {}).get(str(grade_number))
    if not grade_data:
        return None

    for sem_key in sorted(grade_data.get("semesters", {}).keys()):
        semester = grade_data["semesters"][sem_key]
        for period in semester.get("periods", []):
            if period.get("topic", "").strip().lower() == topic_name.strip().lower():
                return period
    return None


def get_semester_for_topic(curricula, subject, grade_number, topic_name):
    """Return which semester a topic belongs to (1 or 2)."""
    subject_key = subject.strip().lower()
    if subject_key not in curricula:
        return None

    grade_data = curricula[subject_key].get("grades", {}).get(str(grade_number))
    if not grade_data:
        return None

    for sem_key in sorted(grade_data.get("semesters", {}).keys()):
        semester = grade_data["semesters"][sem_key]
        for period in semester.get("periods", []):
            if period.get("topic", "").strip().lower() == topic_name.strip().lower():
                return int(sem_key)
    return None


def build_curriculum_context(curricula, subject, grade_number, topic_name):
    """
    Build a rich text block that gets injected into the AI prompt,
    giving the model full knowledge of the Ministry of Education's
    requirements for this specific topic.

    Returns a formatted string, or empty string if no curriculum data exists.
    """
    details = get_topic_details(curricula, subject, grade_number, topic_name)
    if not details:
        return ""

    subject_data = curricula.get(subject.strip().lower(), {})
    semester = get_semester_for_topic(curricula, subject, grade_number, topic_name)

    lines = []
    lines.append("=" * 60)
    lines.append("LIBERIA MINISTRY OF EDUCATION — OFFICIAL CURRICULUM ALIGNMENT")
    lines.append("=" * 60)
    lines.append(f"Subject: {subject}")
    lines.append(f"Grade: {grade_number} | Semester: {semester or 'N/A'} | Period: {details.get('period', 'N/A')}")
    lines.append(f"Topic: {details.get('topic', topic_name)}")
    lines.append("")

    # General objectives
    gen_obj = subject_data.get("general_objectives", [])
    if gen_obj:
        lines.append("GENERAL SUBJECT OBJECTIVES:")
        for obj in gen_obj:
            lines.append(f"  • {obj}")
        lines.append("")

    # Specific objectives for this topic
    spec_obj = details.get("specific_objectives", [])
    if spec_obj:
        lines.append("SPECIFIC LEARNING OBJECTIVES FOR THIS TOPIC:")
        lines.append("(These are what the Ministry of Education requires students to achieve)")
        for i, obj in enumerate(spec_obj, 1):
            lines.append(f"  {i}. {obj}")
        lines.append("")

    # Content outline
    content = details.get("content_outline", [])
    if content:
        lines.append("REQUIRED CONTENT OUTLINE:")
        for item in content:
            lines.append(f"  • {item}")
        lines.append("")

    # Suggested activities
    activities = details.get("suggested_activities", [])
    if activities:
        lines.append("MINISTRY-SUGGESTED TEACHING ACTIVITIES:")
        for act in activities:
            lines.append(f"  • {act}")
        lines.append("")

    # Lab materials
    materials = details.get("lab_materials", [])
    if materials:
        lines.append("RECOMMENDED LAB MATERIALS:")
        lines.append(f"  {', '.join(materials)}")
        lines.append("")

    # Local contextualization
    local_notes = details.get("local_contextualization_notes", "")
    if local_notes:
        lines.append("LIBERIAN CONTEXTUALIZATION GUIDANCE:")
        lines.append(f"  {local_notes}")
        lines.append("")

    # Assessment strategies
    assess = subject_data.get("assessment_strategies", [])
    if assess:
        lines.append("APPROVED ASSESSMENT STRATEGIES:")
        lines.append(f"  {', '.join(assess)}")
        lines.append("")

    # Expected competencies
    comp = subject_data.get("expected_competencies", [])
    if comp:
        lines.append("EXPECTED COMPETENCIES TO DEVELOP:")
        lines.append(f"  {', '.join(comp)}")
        lines.append("")

    # Recommended texts
    texts = subject_data.get("primary_texts", [])
    if texts:
        lines.append("MINISTRY-RECOMMENDED TEXTBOOKS:")
        for t in texts:
            lines.append(f"  - {t}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("Use the above curriculum data to ensure your response is FULLY")
    lines.append("aligned with Liberia's Ministry of Education requirements.")
    lines.append("=" * 60)

    return "\n".join(lines)


def get_curriculum_summary(curricula):
    """
    Return a human-readable summary of all loaded curricula.
    Useful for displaying in the app sidebar.
    """
    if not curricula:
        return "No curriculum data loaded."

    lines = []
    for subject_key, data in sorted(curricula.items()):
        subject_name = data.get("subject", subject_key.title())
        grades = sorted(data.get("grades", {}).keys())
        topic_count = sum(
            len(get_grade_topics(curricula, subject_name, int(g)))
            for g in grades
        )
        lines.append(f"📘 {subject_name}: Grades {', '.join(grades)} ({topic_count} topics)")
    return "\n".join(lines)


# ── Quick self-test ────────────────────────────────────────────────────
if __name__ == "__main__":
    curricula = load_all_curricula()
    print(f"Loaded {len(curricula)} subject(s):")
    print(get_curriculum_summary(curricula))
    print()

    # Test Physics Grade 10
    if "physics" in curricula:
        topics = get_grade_topics(curricula, "Physics", 10)
        print(f"Physics Grade 10 topics: {topics}")
        print()

        if topics:
            ctx = build_curriculum_context(curricula, "Physics", 10, topics[0])
            print("Sample curriculum context block:")
            print(ctx[:500] + "...")
