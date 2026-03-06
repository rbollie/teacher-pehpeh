"""
Student Import Patch — Roster Sheet Support
=============================================
Drop this into your app.py (or grade_tracker.py) to replace the existing
student upload logic. It handles THREE upload scenarios automatically:

  1. Full IBT Grade Tracker workbook (.xlsx) with a "Roster" sheet
     → reads names from row 3 onward (header in row 3, data from row 4)
  2. Any .xlsx without a Roster sheet but with a "name" column anywhere
     → falls back to the existing first-sheet behaviour
  3. Plain .csv with a "name" column
     → unchanged existing behaviour

HOW TO INTEGRATE
----------------
Find the block in your Students tab that looks like:

    uf = st.file_uploader("Upload student list", type=["csv","xlsx"], ...)
    if uf:
        df = pd.read_csv(uf) / pd.read_excel(uf)
        ...

Replace the entire if-uf block with a call to:

    load_students_from_upload(uf)

which returns a list of student dicts ready to extend st.session_state.students.
"""

import pandas as pd
import streamlit as st


# ── Column aliases the Roster sheet (or any sheet) might use ────────────────
_NAME_ALIASES = ["name", "student name", "student_name", "full name",
                 "full_name", "pupil", "pupil name"]


def _find_name_col(df: pd.DataFrame) -> str | None:
    """Return the actual column label that contains student names, or None."""
    for col in df.columns:
        if str(col).strip().lower() in _NAME_ALIASES:
            return col
    return None


def _parse_roster_sheet(xf: pd.ExcelFile) -> list[dict] | None:
    """
    Try to read the 'Roster' sheet from an ExcelFile.
    Returns a list of student dicts, or None if the sheet isn't present / usable.

    Roster sheet layout (from IBT Grade Tracker template):
        Row 1  — decorative header (merged)
        Row 2  — column headers: Student Name | Grade Level | Class Section | Notes | Subjects Tracked
        Row 3+ — one student per row
    """
    if "Roster" not in xf.sheet_names:
        return None

    # Read with header at row index 1 (0-based) → row 2 in the spreadsheet
    df = pd.read_excel(xf, sheet_name="Roster", header=1)
    df.dropna(how="all", inplace=True)   # remove blank rows

    name_col = _find_name_col(df)
    if name_col is None:
        return None

    students = []
    for _, row in df.iterrows():
        raw_name = str(row[name_col]).strip()
        if not raw_name or raw_name.lower() in ("nan", "none", ""):
            continue

        # Pull optional metadata if the columns exist
        grade_level = ""
        section = ""
        subjects = []

        if "Grade Level" in df.columns:
            gl = str(row.get("Grade Level", "")).strip()
            grade_level = "" if gl.lower() in ("nan", "") else gl

        if "Class Section" in df.columns:
            sc = str(row.get("Class Section", "")).strip()
            section = "" if sc.lower() in ("nan", "") else sc

        if "Subjects Tracked" in df.columns:
            sv = str(row.get("Subjects Tracked", "")).strip()
            if sv and sv.lower() not in ("nan", ""):
                subjects = [s.strip() for s in sv.split(",") if s.strip()]

        students.append({
            "name": raw_name,
            "grade": grade_level,
            "section": section,
            "subjects": subjects,
            # risk / IBT fields default to neutral until grades come in
            "risk_score": 50,
            "grades": {},
        })

    return students if students else None


def _parse_generic_sheet(xf: pd.ExcelFile) -> list[dict] | None:
    """
    Fallback: read the first sheet of an xlsx looking for any 'name'-like column.
    """
    df = pd.read_excel(xf, sheet_name=xf.sheet_names[0])
    df.dropna(how="all", inplace=True)

    name_col = _find_name_col(df)
    if name_col is None:
        return None

    students = []
    for _, row in df.iterrows():
        raw_name = str(row[name_col]).strip()
        if not raw_name or raw_name.lower() in ("nan", "none", ""):
            continue
        students.append({
            "name": raw_name,
            "risk_score": 50,
            "grades": {},
        })
    return students if students else None


def _parse_csv(file) -> list[dict] | None:
    """Read a CSV file with a 'name' column."""
    df = pd.read_csv(file)
    df.dropna(how="all", inplace=True)

    name_col = _find_name_col(df)
    if name_col is None:
        return None

    students = []
    for _, row in df.iterrows():
        raw_name = str(row[name_col]).strip()
        if not raw_name or raw_name.lower() in ("nan", "none", ""):
            continue
        students.append({
            "name": raw_name,
            "risk_score": 50,
            "grades": {},
        })
    return students if students else None


# ── PUBLIC FUNCTION — call this from your Students tab ──────────────────────

def load_students_from_upload(uploaded_file) -> list[dict]:
    """
    Parse an uploaded file (CSV or XLSX) and return a clean list of student dicts.
    Emits Streamlit success/warning/error messages automatically.

    Usage in Students tab:
        uf = st.file_uploader("Upload student list", type=["csv","xlsx"],
                              key="student_upload")
        if uf:
            new_students = load_students_from_upload(uf)
            if new_students:
                # Merge — avoid duplicates by name
                existing = {s["name"] for s in st.session_state.students}
                added = [s for s in new_students if s["name"] not in existing]
                st.session_state.students.extend(added)
                if added:
                    st.success(f"✅ Imported {len(added)} student(s).")
                else:
                    st.info("All students in this file are already in your list.")
    """
    fname = uploaded_file.name.lower()
    students = None
    source_note = ""

    if fname.endswith(".xlsx") or fname.endswith(".xls"):
        xf = pd.ExcelFile(uploaded_file)

        # Priority 1 — Roster sheet (IBT Grade Tracker workbook)
        students = _parse_roster_sheet(xf)
        if students is not None:
            source_note = "📋 Read from **Roster** sheet"
        else:
            # Priority 2 — any sheet with a name column
            students = _parse_generic_sheet(xf)
            if students is not None:
                source_note = f"📄 Read from sheet: *{xf.sheet_names[0]}*"

    elif fname.endswith(".csv"):
        students = _parse_csv(uploaded_file)
        if students is not None:
            source_note = "📄 Read from CSV"

    if students is None:
        st.error(
            "❌ Could not find a student name column in this file.\n\n"
            "Expected a **Roster** sheet (IBT Grade Tracker workbook), "
            "or any sheet/CSV with a column named **`name`** (lowercase)."
        )
        return []

    if source_note:
        st.caption(source_note)

    return students


# ── COPY-PASTE SNIPPET for Students tab ─────────────────────────────────────
STUDENTS_TAB_SNIPPET = """
# ── Student Import (paste inside your Students tab block) ───────────────────
from student_import_patch import load_students_from_upload

with st.expander("📥 Import Students from File", expanded=False):
    uf = st.file_uploader(
        "Upload the IBT Grade Tracker workbook (.xlsx) or any CSV with a 'name' column",
        type=["csv", "xlsx"],
        key="student_roster_upload"
    )
    if uf:
        new_students = load_students_from_upload(uf)
        if new_students:
            existing = {s["name"] for s in st.session_state.students}
            added = [s for s in new_students if s["name"] not in existing]
            skipped = len(new_students) - len(added)
            st.session_state.students.extend(added)
            if added:
                st.success(f"✅ Imported {len(added)} student(s).")
            if skipped:
                st.info(f"ℹ️ {skipped} student(s) already in list — skipped.")
            st.rerun()
"""
