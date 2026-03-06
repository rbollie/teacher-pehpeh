"""
ibt_whatif_tab.py
=================
IBT Trajectory Analysis & What-If Scenario Planner for Teacher Pehpeh

Features:
  - Per-student comparison against IBT's 8-year proprietary benchmarks
  - Interactive Chart.js component with:
      · Hover tooltips on all lines
      · Draggable "what-if" projection line (drag up/down to model interventions)
      · Live summary panel updating as you drag
  - IBT research context & risk factor analysis
  - Subject-level benchmark breakdown

Integration into app.py:
  At top of file, add alongside existing IBT imports:
      try:
          from ibt_whatif_tab import render_ibt_whatif_tab
          IBT_WHATIF_AVAILABLE = True
      except ImportError:
          IBT_WHATIF_AVAILABLE = False

  In Tab 6 block (IBT REPORTS), add BEFORE or AFTER the existing render_ibt_report_tab():
      if IBT_WHATIF_AVAILABLE:
          render_ibt_whatif_tab(
              roster=st.session_state.get("_ar_roster"),          # set by academic_report_excel_tab
              subject_data=st.session_state.get("_ar_subject_data")
          )

  OR call it standalone if ibt_reports_tab.py is unavailable.

Built by IBT | Teacher Pehpeh Project
"""

import streamlit as st
import json

# ── IBT Proprietary Benchmarks (183 students, 6 schools, 8 years) ─────────────
IBT_BENCH = {
    "Overall":         43.3,
    "Mathematics":     39.1,
    "Physics":         39.9,
    "Chemistry":       49.4,
    "Biology":         44.7,
    "English Grammar": 43.3,
    "Literature":      43.3,
    "Economics":       43.3,
    "French":          43.3,
}
# IBT trajectory constants
IBT_GAP_NO_INTERV  = 5.5   # pts gap widens per 2 yrs without intervention
IBT_GAP_INTERV     = 2.4   # pts gap with consistent intervention
IBT_WASSCE_TARGET  = 50.0  # minimum for WASSCE readiness (B-)
IBT_AT_RISK        = 37.5  # C- / intervention trigger
IBT_EXCELLENT      = 62.5  # B / distinction zone

SUBJECT_LIST = ["Overall"] + [k for k in IBT_BENCH if k != "Overall"]


# ── Entry Point ──────────────────────────────────────────────────────────────

def render_ibt_whatif_tab(roster=None, subject_data=None):
    """
    Main render function. Call inside Tab 6 (IBT Reports) of app.py.

    roster       : list of {name, grade, student_id, gender}  (from Excel or None)
    subject_data : {subject: {student_name: {s1_avg, s2_avg, overall_avg, ...}}}
    """

    # ── Banner ───────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#0D1B2A,#1A0D2E);border-radius:14px;
  padding:16px 22px 14px;margin-bottom:14px;border:1px solid #2A1E4A">
  <div style="color:#D4A843;font-size:1.05rem;font-weight:800;letter-spacing:.4px">
    📈 IBT TRAJECTORY ANALYSIS — WHAT-IF SCENARIO PLANNER</div>
  <div style="color:#8899BB;font-size:.83rem;margin-top:5px">
    Compare each student against IBT's 8-year proprietary dataset (183 students · 6 Liberian schools).
    <strong style="color:#D0D8E8">Drag the green projected line</strong> up or down to model
    intervention scenarios and see projected WASSCE readiness in real time.
  </div>
</div>""", unsafe_allow_html=True)

    # ── Build student list from all available sources ─────────────────────────
    students = _build_student_list(roster, subject_data)

    if not students:
        st.info("📭 No student data available. Add students in the Students tab "
                "or upload the IBT Grade Tracker Excel in the Academic Report tab.")
        return

    # ── Controls row ─────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        sel_name = st.selectbox("Student:", [s["name"] for s in students],
                                key="wi_student_sel")
    with c2:
        sel_subj = st.selectbox("Subject:", SUBJECT_LIST, key="wi_subj_sel")
    with c3:
        show_nointerv = st.checkbox("Show no-intervention trajectory",
                                    value=True, key="wi_show_noint")

    sel_student = next((s for s in students if s["name"] == sel_name), None)
    if not sel_student:
        return

    # ── Resolve actual scores ─────────────────────────────────────────────────
    actual_scores, s1_avg, s2_avg = _resolve_scores(sel_student, sel_subj)
    bench = IBT_BENCH.get(sel_subj, IBT_BENCH["Overall"])

    # ── Render interactive chart ──────────────────────────────────────────────
    _render_chart(sel_name, sel_subj, actual_scores, bench, show_nointerv)

    # ── Subject benchmark grid ────────────────────────────────────────────────
    st.markdown("---")
    _render_subject_benchmarks(sel_student, subject_data, sel_name)

    # ── Risk factor & IBT context panel ──────────────────────────────────────
    _render_ibt_context(sel_student)


# ── Student List Builder ──────────────────────────────────────────────────────

def _build_student_list(roster, subject_data):
    """
    Combine roster/subject_data from Excel with session_state.students.
    Returns list of {name, info, scores} where scores = {subj: {s1_avg, s2_avg, overall_avg}}.
    """
    result = {}

    # From Excel
    if roster:
        for s in roster:
            name = s["name"]
            scores = {}
            if subject_data:
                for subj, sdata in subject_data.items():
                    if name in sdata:
                        scores[subj] = sdata[name]
            result[name] = {"name": name, "info": s, "scores": scores,
                             "source": "excel"}

    # From session state (manual entry)
    for stu in st.session_state.get("students", []):
        name = stu["name"]
        if name not in result:
            result[name] = {"name": name, "info": stu, "scores": {},
                            "source": "session"}

    return list(result.values())


# ── Score Resolver ─────────────────────────────────────────────────────────────

def _resolve_scores(student, subj):
    """
    Return (actual_scores_list, s1_avg, s2_avg) for the selected subject.
    actual_scores = [s1_avg, s2_avg] with Nones removed.
    """
    scores_dict = student.get("scores", {})

    if subj == "Overall":
        all_s1 = [d["s1_avg"] for d in scores_dict.values()
                  if d.get("s1_avg") is not None]
        all_s2 = [d["s2_avg"] for d in scores_dict.values()
                  if d.get("s2_avg") is not None]
        s1 = round(sum(all_s1)/len(all_s1), 1) if all_s1 else None
        s2 = round(sum(all_s2)/len(all_s2), 1) if all_s2 else None
    else:
        sdata = scores_dict.get(subj, {})
        s1 = sdata.get("s1_avg")
        s2 = sdata.get("s2_avg")

    actual = [v for v in [s1, s2] if v is not None]
    return actual, s1, s2


# ── Chart Renderer ─────────────────────────────────────────────────────────────

def _render_chart(student_name, subject, actual_scores, bench, show_nointerv):
    """
    Render the Chart.js interactive what-if component via streamlit.components.v1.html.
    """
    import streamlit.components.v1 as components

    n_actual = len(actual_scores)
    labels_actual = [f"Sem {i+1}" for i in range(n_actual)]
    labels_proj   = ["Sem 3 (Proj)", "Sem 4 (Proj)", "Year End"]
    all_labels    = labels_actual + labels_proj

    last = actual_scores[-1] if actual_scores else bench

    # Default what-if projection: modest improvement
    default_proj = [
        round(min(100, last + 4),  1),
        round(min(100, last + 8),  1),
        round(min(100, last + 12), 1),
    ]

    # No-intervention trajectory: gap widens ~2.75 pts per semester
    no_interv_proj = [
        round(max(0, last - 2.75), 1),
        round(max(0, last - 5.5),  1),
        round(max(0, last - 8.25), 1),
    ] if show_nointerv else []

    cfg = {
        "allLabels":      all_labels,
        "nActual":        n_actual,
        "actualScores":   actual_scores,
        "defaultProj":    default_proj,
        "noIntervProj":   no_interv_proj,
        "bench":          bench,
        "wassceTarget":   IBT_WASSCE_TARGET,
        "atRisk":         IBT_AT_RISK,
        "excellent":      IBT_EXCELLENT,
        "studentName":    student_name,
        "subject":        subject,
        "showNoInterv":   show_nointerv,
    }
    cfg_json = json.dumps(cfg)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-dragdata@2.2.5/dist/chartjs-plugin-dragdata.min.js"></script>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0a0e1a;font-family:system-ui,-apple-system,sans-serif;padding:14px 14px 8px}}
  .chart-wrap{{position:relative;width:100%;height:300px}}
  .panel{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:10px}}
  .card{{background:#0D1B2A;border:1px solid #1E3A6A;border-radius:9px;padding:10px 12px;text-align:center}}
  .card-label{{color:#8899BB;font-size:10px;font-weight:600;letter-spacing:.5px;text-transform:uppercase;margin-bottom:3px}}
  .card-value{{font-size:19px;font-weight:800;line-height:1}}
  .card-sub{{color:#556;font-size:9.5px;margin-top:3px}}
  .hint{{color:#445;font-size:10.5px;text-align:center;margin-top:7px;padding-bottom:2px}}
  .hint strong{{color:#66BB6A}}
  @media(max-width:500px){{.panel{{grid-template-columns:repeat(3,1fr)}}}}
</style>
</head>
<body>

<div class="chart-wrap">
  <canvas id="c"></canvas>
</div>

<div class="panel">
  <div class="card">
    <div class="card-label">Current</div>
    <div class="card-value" id="vCur" style="color:#D4A843">—</div>
    <div class="card-sub">Latest actual</div>
  </div>
  <div class="card">
    <div class="card-label">Projected End</div>
    <div class="card-value" id="vProj" style="color:#66BB6A">—</div>
    <div class="card-sub">Year-end what-if</div>
  </div>
  <div class="card">
    <div class="card-label">IBT Benchmark</div>
    <div class="card-value" id="vBench" style="color:#2B7DE9">—</div>
    <div class="card-sub">8-yr class avg</div>
  </div>
  <div class="card">
    <div class="card-label">Gap to IBT</div>
    <div class="card-value" id="vGap">—</div>
    <div class="card-sub">vs benchmark</div>
  </div>
  <div class="card">
    <div class="card-label">Status</div>
    <div class="card-value" id="vStatus" style="font-size:13px;line-height:1.3">—</div>
    <div class="card-sub" id="vStatusSub"></div>
  </div>
</div>

<div class="hint">
  💡 Drag the <strong>green projected line</strong> up or down to simulate intervention outcomes
</div>

<script>
const C = {cfg_json};

// ── Status logic ────────────────────────────────────────────────────────────
function status(v) {{
  if (v >= C.excellent)    return {{text:"🏆 Excellent",   sub:"Distinction zone",  col:"#81C784"}};
  if (v >= C.wassceTarget) return {{text:"✅ On Target",   sub:"WASSCE-ready",      col:"#66BB6A"}};
  if (v >= C.bench)        return {{text:"📊 At IBT Avg",  sub:"Meeting benchmark", col:"#FFA726"}};
  if (v >= C.atRisk)       return {{text:"⚠️ Monitor",     sub:"Below IBT avg",     col:"#FF9800"}};
  return                          {{text:"🔴 Intervention",sub:"Urgent support",    col:"#EF5350"}};
}}

// ── Update summary panel ────────────────────────────────────────────────────
function updatePanel(projArr) {{
  const cur  = C.actualScores.length ? C.actualScores[C.actualScores.length - 1] : null;
  const proj = projArr[projArr.length - 1];
  const gap  = proj !== null ? proj - C.bench : null;
  const st   = proj !== null ? status(proj) : null;

  document.getElementById('vCur').textContent  = cur  !== null ? cur.toFixed(1)  : '—';
  document.getElementById('vProj').textContent = proj !== null ? proj.toFixed(1) : '—';
  document.getElementById('vBench').textContent = C.bench.toFixed(1);

  if (gap !== null) {{
    const gEl = document.getElementById('vGap');
    gEl.textContent  = (gap >= 0 ? '+' : '') + gap.toFixed(1);
    gEl.style.color  = gap >= 0 ? '#66BB6A' : '#EF5350';
  }}
  if (st) {{
    const sEl = document.getElementById('vStatus');
    sEl.textContent  = st.text;
    sEl.style.color  = st.col;
    document.getElementById('vStatusSub').textContent = st.sub;
  }}
}}

// ── Build dataset arrays ─────────────────────────────────────────────────────
const nL = C.allLabels.length;
const nA = C.nActual;

// Actual: fill first nA positions
const dActual = Array(nL).fill(null);
C.actualScores.forEach((v, i) => {{ dActual[i] = v; }});

// Projection: bridge from last actual, then 3 future points
const dProj = Array(nL).fill(null);
if (nA > 0) dProj[nA - 1] = C.actualScores[nA - 1]; // bridge
C.defaultProj.forEach((v, i) => {{ dProj[nA + i] = v; }});

// Benchmark (flat)
const dBench = Array(nL).fill(C.bench);

// WASSCE target (flat)
const dTarget = Array(nL).fill(C.wassceTarget);

// At-risk threshold (flat)
const dAtRisk = Array(nL).fill(C.atRisk);

// No-intervention trajectory (future only, bridge from last actual)
const dNoInterv = Array(nL).fill(null);
if (C.showNoInterv && nA > 0) {{
  dNoInterv[nA - 1] = C.actualScores[nA - 1]; // bridge
  C.noIntervProj.forEach((v, i) => {{ dNoInterv[nA + i] = v; }});
}}

// ── Chart datasets ────────────────────────────────────────────────────────────
const datasets = [
  {{
    label: C.studentName + ' (Actual)',
    data: dActual,
    borderColor: '#D4A843',
    backgroundColor: 'rgba(212,168,67,.12)',
    borderWidth: 3,
    pointRadius: 7, pointHoverRadius: 10,
    pointBackgroundColor: '#D4A843',
    fill: false, tension: 0.3, spanGaps: false,
    dragData: false,
  }},
  {{
    label: '✏️ What-If Projection (drag!)',
    data: dProj,
    borderColor: '#66BB6A',
    backgroundColor: 'rgba(102,187,106,.08)',
    borderWidth: 2.5,
    borderDash: [7, 3],
    pointRadius: 9, pointHoverRadius: 13,
    pointBackgroundColor: '#66BB6A',
    pointBorderColor: '#ffffff',
    pointBorderWidth: 2,
    fill: false, tension: 0.3, spanGaps: false,
    dragData: true,
  }},
  {{
    label: 'IBT 8-yr Avg Benchmark',
    data: dBench,
    borderColor: '#2B7DE9',
    borderWidth: 2,
    borderDash: [10, 5],
    pointRadius: 0, fill: false,
    dragData: false,
  }},
  {{
    label: 'WASSCE Target (' + C.wassceTarget + ')',
    data: dTarget,
    borderColor: '#81C784',
    borderWidth: 1.5,
    borderDash: [4, 4],
    pointRadius: 0, fill: false,
    dragData: false,
  }},
  {{
    label: 'At-Risk Line (' + C.atRisk + ')',
    data: dAtRisk,
    borderColor: '#EF5350',
    backgroundColor: 'rgba(239,83,80,.04)',
    borderWidth: 1.5,
    borderDash: [3, 3],
    pointRadius: 0,
    fill: true,
    dragData: false,
  }},
];

if (C.showNoInterv) {{
  datasets.push({{
    label: '📉 No-Intervention Trajectory',
    data: dNoInterv,
    borderColor: '#FF7043',
    borderWidth: 1.8,
    borderDash: [5, 5],
    pointRadius: 5, pointHoverRadius: 8,
    pointBackgroundColor: '#FF7043',
    fill: false, tension: 0.3, spanGaps: false,
    dragData: false,
  }});
}}

// ── Chart init ────────────────────────────────────────────────────────────────
const ctx = document.getElementById('c').getContext('2d');
const myChart = new Chart(ctx, {{
  type: 'line',
  data: {{ labels: C.allLabels, datasets }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    animation: {{ duration: 200 }},
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{
        position: 'top',
        labels: {{
          color: '#D0D8E8', font: {{ size: 10.5 }},
          boxWidth: 14, padding: 10,
          filter: item => item.text !== undefined,
        }}
      }},
      tooltip: {{
        backgroundColor: 'rgba(10,14,26,.96)',
        titleColor: '#D4A843',
        bodyColor:  '#D0D8E8',
        borderColor: '#1E3A6A',
        borderWidth: 1,
        padding: 10,
        callbacks: {{
          title: (items) => `${{C.allLabels[items[0].dataIndex]}}`,
          label: (item) => {{
            if (item.raw === null || item.raw === undefined) return null;
            const v   = item.raw.toFixed(1);
            const diff = (item.raw - C.bench).toFixed(1);
            const pfx  = diff >= 0 ? '+' : '';
            let extra  = ` (${{pfx}}${{diff}} vs IBT)`;
            if (item.dataset.dragData) {{
              const st = status(item.raw);
              extra += `  →  ${{st.text}}`;
            }}
            return `${{item.dataset.label.split('(')[0].trim()}}: ${{v}}${{extra}}`;
          }}
        }}
      }},
      dragData: {{
        round: 1,
        showTooltip: true,
        magnet: {{ to: v => Math.min(100, Math.max(0, Math.round(v * 2) / 2)) }},
        onDragStart: (e, datasetIndex) => datasetIndex === 1,
        onDrag: (e, datasetIndex, index, value) => {{
          if (datasetIndex !== 1) return false;
          if (index < nA - 1)    return false;   // cannot drag before bridge point
        }},
        onDragEnd: (e, datasetIndex, index, value) => {{
          const pts = myChart.data.datasets[1].data
            .slice(nA > 0 ? nA - 1 : 0)
            .filter(v => v !== null && v !== undefined);
          updatePanel(pts);
        }},
      }}
    }},
    scales: {{
      x: {{
        grid:  {{ color: 'rgba(255,255,255,.05)' }},
        ticks: {{ color: '#8899BB', font: {{ size: 10 }} }},
      }},
      y: {{
        min: 0, max: 100,
        grid:  {{ color: 'rgba(255,255,255,.05)' }},
        ticks: {{ color: '#8899BB', font: {{ size: 10 }}, stepSize: 10 }},
        title: {{ display: true, text: 'Score / 100', color: '#8899BB',
                  font: {{ size: 10 }} }},
      }}
    }}
  }}
}});

// Initial panel
const initPts = dProj.slice(nA > 0 ? nA - 1 : 0).filter(v => v !== null);
updatePanel(initPts.length ? initPts : [C.bench]);
</script>
</body>
</html>"""

    components.html(html, height=530, scrolling=False)


# ── Subject Benchmark Grid ─────────────────────────────────────────────────────

def _render_subject_benchmarks(student, subject_data, student_name):
    """Show per-subject score cards vs IBT benchmarks for this student."""
    st.markdown(
        f'<div style="color:#D4A843;font-weight:700;font-size:.9rem;margin-bottom:8px">'
        '🔬 Subject-by-Subject vs IBT Benchmarks</div>', unsafe_allow_html=True)

    scores_dict = student.get("scores", {})
    if not scores_dict:
        st.caption("No per-subject grade data available for this student.")
        return

    subj_keys = [k for k in IBT_BENCH if k != "Overall" and k in scores_dict]
    if not subj_keys:
        st.caption("No matching subjects found.")
        return

    cols_per_row = 4
    for batch_start in range(0, len(subj_keys), cols_per_row):
        batch = subj_keys[batch_start:batch_start + cols_per_row]
        cols  = st.columns(len(batch))
        for col, subj in zip(cols, batch):
            d    = scores_dict[subj]
            ov   = d.get("overall_avg")
            b    = IBT_BENCH[subj]
            diff = round(ov - b, 1) if ov is not None else None
            color = ("#66BB6A" if diff is not None and diff >= 0
                     else ("#FFA726" if diff is not None and diff >= -8
                           else "#EF5350"))
            diff_str = (f"{diff:+.1f}" if diff is not None else "—")
            col.markdown(f"""
<div style="background:#0F1E38;border:1px solid #1E3A6A;border-radius:9px;
  padding:10px 12px;text-align:center;margin-bottom:6px">
  <div style="color:#D4A843;font-weight:700;font-size:.78rem">{subj[:12]}</div>
  <div style="font-size:1.4rem;font-weight:800;color:#fff;line-height:1.1;margin:3px 0">
    {f"{ov:.0f}" if ov else "—"}</div>
  <div style="color:#556;font-size:.7rem">IBT avg: {b}</div>
  <div style="color:{color};font-size:.73rem;font-weight:700">{diff_str} vs IBT</div>
</div>""", unsafe_allow_html=True)


# ── IBT Research Context Panel ────────────────────────────────────────────────

def _render_ibt_context(student):
    """Render IBT research findings and risk factor analysis for the student."""
    st.markdown(
        f'<div style="color:#D4A843;font-weight:700;font-size:.9rem;margin-bottom:8px">'
        '📚 IBT Research Context</div>', unsafe_allow_html=True)

    facts = [
        ("📊", "IBT Dataset",
         "183 students · 6 Liberian schools · 8 years · 4 STEM subjects"),
        ("🏫", "School Effect",
         "Strongest predictor (F=8.60, p<0.001). Best school avg 51.2, worst 35.4 — "
         "16× the effect of parent education."),
        ("📚", "Subject Performance",
         "Chemistry leads (49.4) · Physics lowest (39.9) · "
         "Biology 44.7 · Mathematics 39.1"),
        ("👩‍👧", "Mother's Education",
         "HS-grad students avg 44.9 vs No-HS 41.8 (p=0.031). "
         "Physics gap: HS 43.8 vs NoHS 36.3 (p=0.0075)."),
        ("💻", "Digital Access",
         "58.5% of IBT students never used a computer. "
         "Computer access adds +4.1 pts on average."),
        ("🔄", "Intervention Impact",
         "Without support: gap widens +5.5 pts per 2 yrs. "
         "With support: gap narrows to 2.4 pts."),
    ]

    cols = st.columns(2)
    for i, (icon, title, body) in enumerate(facts):
        with cols[i % 2]:
            st.markdown(f"""
<div style="background:rgba(13,27,42,.8);border:1px solid #1E3A6A;border-radius:8px;
  padding:10px 13px;margin-bottom:7px">
  <div style="color:#D4A843;font-weight:700;font-size:.82rem">{icon} {title}</div>
  <div style="color:#8899BB;font-size:.78rem;margin-top:3px;line-height:1.5">{body}</div>
</div>""", unsafe_allow_html=True)

    # ── Risk Factors ──────────────────────────────────────────────────────────
    stu_info = student.get("info", {})
    risk_factors = []

    # Try session state students for risk detail
    ss_stu = next((s for s in st.session_state.get("students", [])
                   if s.get("name") == student["name"]), None)
    if ss_stu:
        if ss_stu.get("mom") == "No HS":        risk_factors.append(("Mother: No HS diploma", "#FFA726"))
        if ss_stu.get("sm")  == "Yes":          risk_factors.append(("Single-parent household", "#FFA726"))
        if ss_stu.get("sib") in ("5-8", "8+"): risk_factors.append((f"Many siblings ({ss_stu.get('sib')})", "#FFA726"))
        if ss_stu.get("wk")  == "Yes":          risk_factors.append(("Works after school", "#FF7043"))
        if ss_stu.get("cp")  in ("Never", "Rarely"):
                                                risk_factors.append(("Limited computer access", "#FF9800"))

    if risk_factors:
        items_html = "".join(
            f'<span style="background:rgba(255,160,0,.12);border:1px solid rgba(255,160,0,.25);'
            f'border-radius:5px;padding:2px 8px;font-size:.78rem;color:{c};margin:2px 3px;'
            f'display:inline-block">{t}</span>'
            for t, c in risk_factors
        )
        n = len(risk_factors)
        sev_color = "#EF5350" if n >= 3 else ("#FFA726" if n >= 2 else "#FF9800")
        st.markdown(f"""
<div style="background:rgba(139,26,26,.12);border:1px solid rgba(239,83,80,.3);
  border-radius:9px;padding:12px 15px;margin-top:6px">
  <div style="color:{sev_color};font-weight:700;font-size:.84rem;margin-bottom:6px">
    ⚠️ Risk Factors Detected — {student['name']} ({n} factor{'s' if n > 1 else ''})</div>
  <div style="line-height:2">{items_html}</div>
  <div style="color:#8899BB;font-size:.77rem;margin-top:7px;line-height:1.6">
    IBT research: students with 2+ risk factors average 10–15 pts below class mean
    (especially in Physics). Consistent targeted intervention can reduce this gap by
    up to 60% within one academic year.
  </div>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div style="color:#8899BB;font-size:.82rem;margin-top:4px">'
            f'No risk factors recorded for {student["name"]}. '
            f'Add student profile details in the Students tab for risk analysis.</div>',
            unsafe_allow_html=True)
