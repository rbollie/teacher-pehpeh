# 🌶️ Teacher Pehpeh — AI-Powered Teaching Assistant

## What's New: Ministry of Education Curriculum Integration

Teacher Pehpeh now loads **official Liberia Ministry of Education curriculum data** and injects it directly into AI prompts. When a teacher selects Physics → Grade 10 → "Velocity and Acceleration", the AI receives the exact learning objectives, content outline, suggested activities, and Liberian contextualization notes from the MOE syllabus.

### How It Works

1. Teacher selects grade, subject, and topic from dropdowns
2. If MOE curriculum data exists for that combination, a green badge appears: **✅ MOE Curriculum-Aligned Topics**
3. The teacher can expand "View Ministry of Education Requirements" to see exactly what the MOE expects
4. When they click Generate, the AI receives all curriculum details and produces content that aligns with official standards

### What's Included

```
teacher_pehpeh/
├── app.py                          ← Main application
├── curriculum.py                   ← Curriculum loader module
├── curriculum_data/
│   └── physics.json                ← Physics Grades 10-12 (18 topics)
├── requirements.txt                ← Python packages
├── logo.png                        ← Your logo (add this yourself)
└── README.md                       ← This file
```

---

## 🚀 Setup

### Step 1: Install packages
```bash
pip install -r requirements.txt
```

### Step 2: Add your API keys
Open `app.py` and paste your keys near the top (line ~25):
```python
OPENAI_API_KEY    = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."
GOOGLE_API_KEY    = "AIzaSy..."
```

### Step 3: Add your logo
Put your logo file in this folder as `logo.png`.

### Step 4: Run it
```bash
streamlit run app.py
```

---

## 📘 Adding More Subjects

This is designed so you can keep adding curriculum data as you get more MOE syllabi.

### Step 1: Get the curriculum document (PDF or paper)

### Step 2: Create a JSON file following this structure

Create a new file in `curriculum_data/` — for example `chemistry.json`:

```json
{
  "subject": "Chemistry",
  "country": "Liberia",
  "authority": "Ministry of Education - Republic of Liberia",
  "description": "Brief description of the syllabus...",
  "general_objectives": [
    "Objective 1",
    "Objective 2"
  ],
  "expected_competencies": [
    "Effective Communication Skills",
    "Research and Problem Solving"
  ],
  "assessment_strategies": [
    "Presentations", "Quizzes", "Lab Reports", "Tests"
  ],
  "primary_texts": [
    "Textbook 1 (Author, Year)",
    "Textbook 2 (Author, Year)"
  ],
  "grades": {
    "10": {
      "grade_label": "Grade 10 (SHS 1)",
      "semesters": {
        "1": {
          "periods": [
            {
              "period": "I",
              "topic": "Topic Name Here",
              "specific_objectives": [
                "Students will be able to...",
                "Students will be able to..."
              ],
              "content_outline": [
                "Content area 1",
                "Content area 2"
              ],
              "suggested_activities": [
                "Activity 1",
                "Activity 2"
              ],
              "lab_materials": [
                "Material 1", "Material 2"
              ],
              "local_contextualization_notes": "How to connect this topic to Liberian daily life..."
            }
          ]
        }
      }
    }
  }
}
```

### Step 3: Restart the app

The new subject will automatically appear. The app discovers all `.json` files in `curriculum_data/`.

---

## 🌶️ About

Built by the **Institute of Basic Technology (IBT)**
Co-founded by Rodney Bollie & Dr. Sylvia Bollie

Teacher Pehpeh is named after the Liberian concept of "Pehpeh" (pepper) — the strict, passionate teacher driven by deep belief in their students' potential. 

*For the teacher who stays late. For the student who keeps showing up.*
