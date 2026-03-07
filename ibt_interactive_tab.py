"""
IBT Interactive Reports Tab
Self-contained — no external module dependencies.
Call: render_ibt_interactive_tab()
"""
import streamlit as st
import datetime

IBT_BENCH = {
    "Mathematics": 39.1, "Physics": 39.9, "Chemistry": 49.4, "Biology": 44.7,
    "English Grammar": 43.3, "Literature": 43.3, "Economics": 43.3, "French": 43.3,
}
IBT_ALL_SUBJ = list(IBT_BENCH.keys())
WASSCE  = 50.0
AT_RISK = 37.5
EXCELLENT = 62.5
IBT_OVERALL_AVG = 43.3
IBT_N = 183

RISK_FACTS = [
    ("School quality", "School is the #1 predictor (F=8.60, p<0.001). Best school avg: 51.2 vs worst: 35.4 — a 15.8-point gap."),
    ("Mother's education", "Students with HS-grad mothers avg 44.9 vs 41.8 for no-HS mothers (p=0.031). Physics gap is widest: 43.8 vs 36.3 (p=0.0075)."),
    ("Computer access", "58.5% of IBT students never used a computer. Computer access adds +4.1 pts on average."),
    ("Intervention impact", "Without intervention: gap widens +5.5 pts over 2 years. With IBT intervention: narrows to 2.4 pts."),
    ("WASSCE target", "IBT sets WASSCE pass at 50/100. Class avg of 43.3 means most students need targeted support to reach the threshold."),
    ("Gender parity", "No statistically significant gender gap in overall scores in IBT dataset — interventions affect boys and girls equally."),
]

C_NAVY = "#0F2247"; C_GOLD = "#D4A843"; C_RED = "#8B1A1A"
C_GREEN = "#1B5E20"; C_AMBER = "#E65100"

def _status(score, subj=None):
    bench = IBT_BENCH.get(subj, IBT_OVERALL_AVG) if subj else IBT_OVERALL_AVG
    if score >= EXCELLENT:  return "⭐ Excellent", "#1B5E20"
    if score >= WASSCE:     return "🟢 On Target", "#2E7D32"
    if score >= bench:      return "🔵 At IBT Avg", "#0D47A1"
    if score >= AT_RISK:    return "🟡 Monitor", "#E65100"
    return "🔴 Intervention", "#8B1A1A"

def _score_card(col, label, value, benchmark, unit=""):
    stat, bg = _status(value, label)
    delta = value - benchmark
    col.markdown(
        f'<div style="background:{bg}22;border:1px solid {bg};border-radius:10px;'
        f'padding:10px 14px;text-align:center">'
        f'<div style="color:#8899BB;font-size:.75rem;margin-bottom:2px">{label}</div>'
        f'<div style="color:{C_GOLD};font-size:1.3rem;font-weight:800">{value:.1f}{unit}</div>'
        f'<div style="color:#aaa;font-size:.72rem">IBT bench: {benchmark:.1f} '
        f'<span style="color:{"#4CAF50" if delta>=0 else "#EF5350"}">'
        f'({delta:+.1f})</span></div>'
        f'<div style="font-size:.75rem;margin-top:3px">{stat}</div>'
        f'</div>', unsafe_allow_html=True)

def _build_grade_map(grade_history):
    """Returns {student: {subject: [scores]}}"""
    gmap = {}
    for g in grade_history:
        s = g["student"]; sub = g["subject"]; sc = g["score"]
        gmap.setdefault(s, {}).setdefault(sub, []).append(sc)
    return gmap

def render_ibt_interactive_tab(best_all_fn=None, build_free_chat_fn=None):
    gh = st.session_state.get("grade_history", [])
    students_list = st.session_state.get("students", [])

    # ── Banner ────────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="background:linear-gradient(135deg,{C_NAVY},{C_RED});border-radius:14px;
padding:18px 24px 14px;margin-bottom:12px;border:1px solid {C_GOLD}44">
  <div style="color:{C_GOLD};font-size:1.1rem;font-weight:800;letter-spacing:.5px">
    📈 IBT INTERVENTION ANALYSIS ENGINE</div>
  <div style="color:#D0D8E8;font-size:.85rem;margin-top:4px">
    Compares your class data against IBT's 183-student, 6-school, 8-year Liberian research dataset
    · WASSCE target: 50 · At-risk threshold: 37.5 · Overall IBT avg: 43.3</div>
</div>""", unsafe_allow_html=True)

    if not gh:
        st.info("📭 No grade data loaded yet. Upload the IBT Grade Tracker Excel or enter grades in the Students tab first.")
        return

    try:
        import pandas as pd
        PD = True
    except ImportError:
        PD = False

    gmap = _build_grade_map(gh)
    all_students = sorted(gmap.keys())
    all_subjects = sorted({g["subject"] for g in gh})

    # ── SECTION 1: Class vs IBT Benchmark ────────────────────────────────────
    st.markdown(f'<div style="color:{C_GOLD};font-weight:700;font-size:1rem;margin:8px 0 6px">📊 Class vs IBT Benchmarks</div>', unsafe_allow_html=True)

    bench_rows = []
    for subj in IBT_ALL_SUBJ:
        subj_scores = [sc for s in all_students for sc in gmap.get(s,{}).get(subj,[]) ]
        class_avg = sum(subj_scores)/len(subj_scores) if subj_scores else None
        bench = IBT_BENCH[subj]
        bench_rows.append((subj, class_avg, bench))

    # Render as compact cards
    n_subj_with_data = sum(1 for _, ca, _ in bench_rows if ca is not None)
    if n_subj_with_data:
        cols = st.columns(min(4, n_subj_with_data))
        ci = 0
        for subj, ca, bench in bench_rows:
            if ca is None: continue
            with cols[ci % len(cols)]:
                _score_card(cols[ci % len(cols)], subj[:10], ca, bench)
            ci += 1
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Summary comparison table
    if PD:
        import pandas as pd
        tbl_rows = []
        for subj, ca, bench in bench_rows:
            if ca is None: continue
            gap = ca - bench
            stat, _ = _status(ca, subj)
            tbl_rows.append({
                "Subject": subj,
                "Class Avg": f"{ca:.1f}",
                "IBT Bench": f"{bench:.1f}",
                "Gap": f"{gap:+.1f}",
                "WASSCE Target": "50.0",
                "Gap to WASSCE": f"{ca-50:+.1f}",
                "Status": stat,
            })
        if tbl_rows:
            st.dataframe(pd.DataFrame(tbl_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # ── SECTION 2: Student Deep-Dive ─────────────────────────────────────────
    st.markdown(f'<div style="color:{C_GOLD};font-weight:700;font-size:1rem;margin:4px 0 6px">🎓 Student Deep-Dive</div>', unsafe_allow_html=True)

    sel_student = st.selectbox("Select student:", all_students, key="ibt_stu_sel")
    stu_data = gmap.get(sel_student, {})
    stu_profile = next((s for s in students_list if s.get("name") == sel_student), {})

    # Student profile risk factors
    if stu_profile:
        risk_items = []
        if stu_profile.get("mom") == "No HS":   risk_items.append(("🔴", "No HS mother"))
        if stu_profile.get("sm") == "Yes":       risk_items.append(("🔴", "Single mother"))
        if stu_profile.get("sib") == "8+":       risk_items.append(("🟠", "8+ siblings"))
        if stu_profile.get("wk") == "Yes":       risk_items.append(("🟠", "Works after school"))
        if stu_profile.get("cp") == "Never":     risk_items.append(("🟡", "No computer access"))
        if stu_profile.get("cp") == "Rarely":    risk_items.append(("🟡", "Rare computer access"))
        n_risk = len(risk_items)
        risk_html = " · ".join(f'{ico} {lbl}' for ico, lbl in risk_items) or "🟢 Lower risk profile"
        risk_color = "#8B1A1A" if n_risk >= 3 else ("#E65100" if n_risk >= 1 else "#1B5E20")
        st.markdown(
            f'<div style="background:{risk_color}22;border:1px solid {risk_color}55;'
            f'border-radius:8px;padding:8px 14px;margin-bottom:8px;font-size:.83rem">'
            f'<strong style="color:{C_GOLD}">Risk Factors ({n_risk}):</strong> '
            f'<span style="color:#D0D8E8">{risk_html}</span></div>', unsafe_allow_html=True)

    # Score cards per subject
    stu_subjs = [s for s in IBT_ALL_SUBJ if s in stu_data]
    if stu_subjs:
        cols2 = st.columns(min(4, len(stu_subjs)))
        for ci, subj in enumerate(stu_subjs):
            scores = stu_data[subj]
            avg = sum(scores)/len(scores)
            with cols2[ci % len(cols2)]:
                _score_card(cols2[ci % len(cols2)], subj[:10], avg, IBT_BENCH.get(subj, IBT_OVERALL_AVG))

    # ── SECTION 3: What-If Scenario ───────────────────────────────────────────
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(f'<div style="color:{C_GOLD};font-weight:700;font-size:.95rem;margin:4px 0 4px">🔮 What-If Scenario</div>', unsafe_allow_html=True)
    st.caption("Adjust target scores to see IBT benchmark status and WASSCE probability")

    wi_subj = st.selectbox("Subject for what-if:", stu_subjs or IBT_ALL_SUBJ[:1], key="ibt_wi_subj")
    current_scores = stu_data.get(wi_subj, [])
    current_avg = sum(current_scores)/len(current_scores) if current_scores else 0

    wc1, wc2 = st.columns([2, 3])
    with wc1:
        wi_target = st.slider(
            "Target score for next assessment:",
            min_value=0, max_value=100,
            value=min(100, int(current_avg) + 8),
            step=1, key="ibt_wi_slider"
        )
    with wc2:
        proj_avg = (current_avg * max(1, len(current_scores)) + wi_target) / (max(1, len(current_scores)) + 1)
        bench_wi = IBT_BENCH.get(wi_subj, IBT_OVERALL_AVG)
        stat_curr, sc_bg = _status(current_avg, wi_subj)
        stat_proj, sp_bg = _status(proj_avg, wi_subj)
        wassce_prob = min(100, max(0, (proj_avg - AT_RISK) / (WASSCE - AT_RISK) * 100)) if proj_avg > AT_RISK else 0

        st.markdown(
            f'<div style="background:#0D1B2A;border:1px solid #1E3A6A;border-radius:10px;padding:12px 16px">'
            f'<div style="display:flex;gap:24px;flex-wrap:wrap">'
            f'<div><span style="color:#8899BB;font-size:.78rem">Current avg</span><br>'
            f'<span style="color:{C_GOLD};font-weight:700;font-size:1.1rem">{current_avg:.1f}</span> '
            f'<span style="font-size:.78rem">{stat_curr}</span></div>'
            f'<div><span style="color:#8899BB;font-size:.78rem">→ Projected avg</span><br>'
            f'<span style="color:#4CAF50;font-weight:700;font-size:1.1rem">{proj_avg:.1f}</span> '
            f'<span style="font-size:.78rem">{stat_proj}</span></div>'
            f'<div><span style="color:#8899BB;font-size:.78rem">IBT benchmark</span><br>'
            f'<span style="color:#3B6DC4;font-weight:700;font-size:1.1rem">{bench_wi:.1f}</span></div>'
            f'<div><span style="color:#8899BB;font-size:.78rem">WASSCE readiness</span><br>'
            f'<span style="color:{"#4CAF50" if wassce_prob>=70 else "#FFA726" if wassce_prob>=40 else "#EF5350"};'
            f'font-weight:700;font-size:1.1rem">{wassce_prob:.0f}%</span></div>'
            f'</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── SECTION 4: IBT Research Context ──────────────────────────────────────
    st.markdown(f'<div style="color:{C_GOLD};font-weight:700;font-size:.95rem;margin:4px 0 6px">📚 IBT Research Context</div>', unsafe_allow_html=True)

    rf_cols = st.columns(2)
    for ri, (title, text) in enumerate(RISK_FACTS):
        with rf_cols[ri % 2]:
            st.markdown(
                f'<div style="background:#0D1B2A;border-left:3px solid {C_GOLD};border-radius:6px;'
                f'padding:8px 12px;margin-bottom:8px">'
                f'<div style="color:{C_GOLD};font-weight:700;font-size:.8rem;margin-bottom:2px">{title}</div>'
                f'<div style="color:#C0C8D8;font-size:.78rem;line-height:1.5">{text}</div>'
                f'</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── SECTION 5: AI Intervention Plan ──────────────────────────────────────
    st.markdown(f'<div style="color:{C_GOLD};font-weight:700;font-size:.95rem;margin:4px 0 6px">🤖 AI Intervention Plan</div>', unsafe_allow_html=True)

    ibt_ai_key = f"ibt_ai_{sel_student}"
    gen_cols = st.columns([2, 3])
    with gen_cols[0]:
        if st.button("⚡ Generate IBT Intervention Plan", key="ibt_gen_ai", type="primary", use_container_width=True):
            # Build context for AI
            stu_summary = []
            for subj in stu_subjs:
                scores = stu_data[subj]
                avg = sum(scores)/len(scores)
                bench = IBT_BENCH.get(subj, IBT_OVERALL_AVG)
                gap = avg - bench
                stu_summary.append(f"  {subj}: avg {avg:.1f} (IBT bench {bench:.1f}, gap {gap:+.1f})")

            risk_ctx = ""
            if stu_profile:
                rf = []
                if stu_profile.get("mom")=="No HS": rf.append("mother has no HS education (IBT data: -3.1 pts avg, Physics gap -7.5 pts)")
                if stu_profile.get("sm")=="Yes": rf.append("single-mother household")
                if stu_profile.get("wk")=="Yes": rf.append("works after school (limited study time)")
                if stu_profile.get("cp")=="Never": rf.append("no computer access (-4.1 pts IBT avg)")
                if stu_profile.get("sib")in["5-8","8+"]: rf.append(f"{stu_profile['sib']} siblings (caregiving burden)")
                if rf: risk_ctx = "RISK FACTORS: "+"; ".join(rf)

            prompt = f"""You are an expert Liberian education analyst using IBT's 183-student, 8-year research dataset.

STUDENT: {sel_student}
{risk_ctx}

SUBJECT PERFORMANCE vs IBT BENCHMARKS:
{chr(10).join(stu_summary)}

IBT RESEARCH FACTS:
- Overall IBT avg: 43.3/100
- WASSCE pass target: 50/100
- At-risk threshold: 37.5/100
- School quality is #1 predictor (F=8.60)
- Computer access adds +4.1 pts
- No-HS mother gap: -3.1 pts overall, -7.5 pts in Physics
- Without intervention: gap widens +5.5 pts/2yrs
- With IBT intervention: narrows to 2.4 pts

Write a structured IBT INTERVENTION REPORT for this student. Include:

1. RISK PROFILE SUMMARY: Assess this student's risk level based on their scores AND home factors using IBT data. Be specific.
2. SUBJECT-BY-SUBJECT ANALYSIS: For each subject, state score vs IBT benchmark and what the gap means practically for WASSCE readiness.
3. PRIORITY INTERVENTIONS (ranked 1-3): The 3 most impactful actions for this specific student. Each must:
   - Be doable without internet or special materials
   - Reference IBT research to justify why it will help
   - Include a specific measurable goal (e.g., "Raise Physics to 45 within 6 weeks")
4. TEACHER ACTION THIS WEEK: 2-3 concrete things the teacher can do Monday morning.
5. PROGNOSIS: If interventions are applied consistently, what does IBT data suggest the student can realistically achieve by end of term?

Be specific, data-driven, and compassionate. Acknowledge home barriers."""

            try:
                _baf = best_all_fn or st.session_state.get("_best_all_fn")
                _bcf = build_free_chat_fn or st.session_state.get("_build_free_chat_fn")
                if not _baf or not _bcf:
                    st.warning("AI functions not available. Please ensure the app is running correctly.")
                else:
                    with st.spinner("Generating IBT intervention analysis..."):
                        r, m, _ = _baf(_bcf(), prompt, [])
                    st.session_state[ibt_ai_key] = r
            except Exception as e:
                st.error(f"Could not generate analysis: {e}")

    if st.session_state.get(ibt_ai_key):
        st.markdown(
            f'<div style="background:#0D1B2A;border:1px solid #1E3A6A;border-radius:10px;'
            f'padding:18px 22px;color:#D0D8E8;font-size:.87rem;line-height:1.8;white-space:pre-wrap;margin-top:8px">'
            f'{st.session_state[ibt_ai_key]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── SECTION 6: Download IBT Word Report ──────────────────────────────────
    st.markdown(f'<div style="color:{C_GOLD};font-weight:700;font-size:.95rem;margin:4px 0 6px">📥 Download Reports</div>', unsafe_allow_html=True)
    dl1, dl2 = st.columns(2)
    with dl1:
        try:
            from word_report import generate_academic_word_report
            docx_bytes = generate_academic_word_report(
                gh,
                students_list,
                st.session_state.get("_classroom_label", "IBT School"),
                st.session_state.get("grade_en", "Grade 10"),
                st.session_state.get("ar_analysis_text", "")
            )
            fname = f"IBT_Academic_Report_{datetime.datetime.now().strftime('%Y%m%d')}.docx"
            st.download_button(
                "📄 Download Academic Report (Word)",
                data=docx_bytes,
                file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="ibt_dl_word", type="primary", use_container_width=True
            )
        except Exception as e:
            st.warning(f"Word report: {e}")
    with dl2:
        if PD and gh:
            import pandas as pd
            csv = pd.DataFrame(gh).to_csv(index=False)
            st.download_button(
                "📊 Download Grade Data (CSV)",
                data=csv,
                file_name=f"IBT_Grades_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="ibt_dl_csv", use_container_width=True
            )
