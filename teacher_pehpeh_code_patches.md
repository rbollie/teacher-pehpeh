# Teacher Pehpeh — Code Patches
Three targeted fixes + one new feature for your Streamlit app.

---

## FIX 1 — Drop `nan` / empty rows when loading the CSV/XLSX

Find wherever you read the uploaded student file (likely `pd.read_csv(...)` or `pd.read_excel(...)`) and add `.dropna(how="all")` immediately after:

```python
# BEFORE (causes nan rows)
df = pd.read_csv(uploaded_file)

# AFTER — add one line
df = pd.read_csv(uploaded_file)
df = df.dropna(subset=["Name"])          # drop rows where Name is blank
df = df[df["Name"].str.strip() != ""]   # also drop whitespace-only names
df = df.reset_index(drop=True)
```

If you use `pd.read_excel` instead, same pattern applies.

---

## FIX 2 — Add `Grade` column to template download + display

### 2a. Template download button
Update your template-generation code to include `Grade`:

```python
TEMPLATE_COLS = [
    "Name", "Grade", "Siblings", "Mom_Edu",
    "Single_Mom", "Works", "Computer", "Avg_Score", "Notes"
]

def get_template_csv():
    return pd.DataFrame(columns=TEMPLATE_COLS).to_csv(index=False)

st.download_button(
    label="📥 Download Student Template",
    data=get_template_csv(),
    file_name="student_template.csv",
    mime="text/csv"
)
```

### 2b. Student card display — show Grade
In your student card rendering loop, add Grade next to the name:

```python
grade = row.get("Grade", "")
grade_str = f" · Grade {grade}" if pd.notna(grade) and str(grade).strip() else ""
st.markdown(f"**{row['Name']}**{grade_str} — ...")
```

### 2c. Manual grade editing in the app
Add a text_input inside each student's expander (using the key-swap pattern you already use):

```python
# Inside the per-student expander / edit section
new_grade = st.text_input(
    "Grade",
    value=str(row.get("Grade", "")),
    key=f"grade_{student_idx}_{st.session_state.input_key}"
)
if new_grade != str(row.get("Grade", "")):
    st.session_state.students.at[student_idx, "Grade"] = new_grade
```

---

## FIX 3 — AI Agent Selection Button

Add this **above** the Analysis section in your UI. It lets users choose which report(s) to run before clicking any analysis button.

```python
# ── AI Agent Selector ──────────────────────────────────────────────────────
st.markdown("### 🤖 Select AI Analysis")

agent_options = {
    "📊 Academic Report":   "academic",
    "🏫 IBT Risk Report":   "ibt",
    "📝 Assignment Help":   "assignment",
}

if "selected_agents" not in st.session_state:
    st.session_state.selected_agents = ["academic", "ibt"]   # default both on

cols = st.columns(len(agent_options))
for col, (label, key) in zip(cols, agent_options.items()):
    active = key in st.session_state.selected_agents
    btn_type = "primary" if active else "secondary"
    if col.button(label, type=btn_type, key=f"agent_toggle_{key}"):
        if active:
            st.session_state.selected_agents.remove(key)
        else:
            st.session_state.selected_agents.append(key)
        st.rerun()

# ── Run Analysis button ────────────────────────────────────────────────────
if st.button("⚡ Run Selected Analysis", type="primary"):
    if not st.session_state.selected_agents:
        st.warning("Please select at least one analysis type above.")
    else:
        for agent_key in st.session_state.selected_agents:
            if agent_key == "academic":
                run_academic_report(selected_student)   # your existing function
            elif agent_key == "ibt":
                run_ibt_report(selected_student)        # your existing function
            elif agent_key == "assignment":
                run_assignment_help(selected_student)   # your existing function
```

> **Tip:** Replace `run_academic_report`, `run_ibt_report`, `run_assignment_help` with whatever your actual function names are. The toggle buttons visually switch between primary (active) and secondary (inactive) so the teacher can clearly see what's armed.

---

## Column Reference — Updated CSV Schema

| Column      | Type    | Example Values                  |
|-------------|---------|----------------------------------|
| Name        | text    | Blessing Varney                 |
| Grade       | text    | 10A, 7B, 9C                     |
| Siblings    | select  | 0-4, 5-8, 8+                    |
| Mom_Edu     | select  | No HS, HS Grad, College, Unknown|
| Single_Mom  | select  | Yes, No                         |
| Works       | select  | Yes, No                         |
| Computer    | select  | Never, Sometimes, Often         |
| Avg_Score   | number  | 0–100                           |
| Notes       | text    | Free text                       |

---

*Patches authored for Teacher Pehpeh v2 · IBT · March 2026*
