# ════════════════════════════════════════════════════════════════════════════
# INTEGRATION GUIDE — Teacher Pehpeh Academic Report & IBT What-If Upgrade
# ════════════════════════════════════════════════════════════════════════════
#
# FILES TO ADD (place in same folder as app.py):
#   • academic_report_excel_tab.py   — Excel-based student-by-student report
#   • ibt_whatif_tab.py              — IBT benchmark + draggable what-if chart
#
# ════════════════════════════════════════════════════════════════════════════

# ── STEP 1: Add imports near the top of app.py ──────────────────────────────
# Find the existing block:
#     try:
#         from ibt_reports_tab import render_ibt_report_tab
#         IBT_REPORTS_AVAILABLE = True
#     except ImportError:
#         IBT_REPORTS_AVAILABLE = False
#
# ADD IMMEDIATELY AFTER IT:

try:
    from academic_report_excel_tab import render_academic_report_from_excel
    EXCEL_REPORT_AVAILABLE = True
except ImportError:
    EXCEL_REPORT_AVAILABLE = False

try:
    from ibt_whatif_tab import render_ibt_whatif_tab
    IBT_WHATIF_AVAILABLE = True
except ImportError:
    IBT_WHATIF_AVAILABLE = False


# ── STEP 2: Replace Tab 5 (Academic Report) content ─────────────────────────
#
# Find the block that starts with:
#     # TAB 5: ACADEMIC REPORT
#     if t5:
#      with t5:
#         import datetime as _ardt
#         _school_label = ...
#
# REPLACE the entire "with t5:" block body (everything up to "# TAB 3: CHAT")
# with this:

    # TAB 5: ACADEMIC REPORT
    if t5:
     with t5:
        if EXCEL_REPORT_AVAILABLE:
            render_academic_report_from_excel()
        else:
            # ── ORIGINAL FALLBACK (keep your existing Tab 5 code here) ────────
            import datetime as _ardt
            _school_label = st.session_state.get("_classroom_label", school_name or "My School")
            st.markdown("Academic Report — install academic_report_excel_tab.py for full version.")


# ── STEP 3: Enhance Tab 6 (IBT Reports) ─────────────────────────────────────
#
# Find the block:
#     # TAB 6: IBT REPORTS
#     if t6:
#      with t6:
#         if IBT_REPORTS_AVAILABLE:
#             render_ibt_report_tab()
#
# REPLACE the "with t6:" block body with:

    # TAB 6: IBT REPORTS
    if t6:
     with t6:
        # ── IBT What-If Analysis (new interactive chart) ──────────────────────
        if IBT_WHATIF_AVAILABLE:
            # Pass roster/subject_data from Excel upload (set by academic_report_excel_tab)
            render_ibt_whatif_tab(
                roster=st.session_state.get("_ar_roster"),
                subject_data=st.session_state.get("_ar_subject_data"),
            )
            st.markdown("---")

        # ── Original IBT Report Tab (keep if available) ───────────────────────
        if IBT_REPORTS_AVAILABLE:
            render_ibt_report_tab()
        elif not IBT_WHATIF_AVAILABLE:
            st.markdown(
                '<div style="background:rgba(212,168,67,.08);border:1px solid #D4A84344;'
                'border-radius:12px;padding:24px;text-align:center;margin:1rem 0">'
                '<p style="color:#D4A843;font-size:1.1rem;font-weight:700;margin-bottom:.5rem">'
                '📈 IBT Student Analysis Engine</p>'
                '<p style="color:#8899BB;font-size:.9rem">Add ibt_whatif_tab.py and/or '
                'ibt_reports_tab.py to activate this tab.</p>'
                '</div>',
                unsafe_allow_html=True
            )


# ── STEP 4 (Optional): Pass Excel data between tabs via session_state ────────
#
# In academic_report_excel_tab.py, inside load_excel_data() success path,
# the roster and subject_data are already cached. To share them with the
# IBT tab automatically, add these two lines inside _render_excel_path()
# AFTER the successful load_excel_data() call:
#
#     st.session_state["_ar_roster"]       = roster
#     st.session_state["_ar_subject_data"] = subject_data
#
# (These lines are already present in academic_report_excel_tab.py v1.1+)


# ════════════════════════════════════════════════════════════════════════════
# WHAT YOU GET
# ════════════════════════════════════════════════════════════════════════════
#
# ACADEMIC REPORT TAB (Tab 5):
#   • Upload IBT Grade Tracker Excel → auto-reads Roster + all subject sheets
#   • Class summary: avg score, IBT gap, # needing intervention
#   • Class Overview: summary table + bar chart (Class Avg vs IBT Benchmark,
#     per subject, with hover tooltips)
#   • Student Deep-Dive: select any student → subject score cards,
#     semester progression line chart (hover shows score + IBT gap),
#     HW / Quiz / Test category breakdown table
#   • Fallback: if no Excel, uses manually-entered grade_history
#
# IBT REPORT TAB (Tab 6):
#   • Interactive Chart.js component (no server round-trips):
#       - Gold line: student's actual semester scores
#       - Green dashed line: what-if projection (DRAG UP/DOWN!)
#       - Blue dashed: IBT 8-yr average benchmark
#       - Green thin: WASSCE target (50)
#       - Red thin:   At-risk threshold (37.5)
#       - Orange dashed: no-intervention trajectory (toggle)
#   • Hover tooltips on every point (score + IBT gap + status label)
#   • Live summary panel: Current · Projected End · IBT Bench · Gap · Status
#   • Subject benchmark grid: per-subject score vs IBT avg
#   • Risk factor panel: flags No-HS mom, single parent, siblings, work, etc.
#   • IBT research context: 6 key findings from the 8-year dataset
#
# ════════════════════════════════════════════════════════════════════════════
