"""
generate_academic_word_report(grade_history, students, school_label, grade_en, ai_text)
Returns bytes of a .docx file.
"""
import io, datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── IBT brand colours ──────────────────────────────────────────────────────────
NAVY   = RGBColor(0x0F, 0x22, 0x47)
GOLD   = RGBColor(0xD4, 0xA8, 0x43)
RED    = RGBColor(0x8B, 0x1A, 0x1A)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT  = RGBColor(0xE8, 0xED, 0xF5)
GREEN  = RGBColor(0x0D, 0x3B, 0x14)
AMBER  = RGBColor(0x8B, 0x5E, 0x00)

IBT_BENCH = {
    "Mathematics": 39.1, "Physics": 39.9, "Chemistry": 49.4, "Biology": 44.7,
    "English Grammar": 43.3, "Literature": 43.3, "Economics": 43.3, "French": 43.3,
}
WASSCE = 50.0
AT_RISK = 37.5

def _hex(rgb):
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def _cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def _set_cell_text(cell, text, bold=False, color=WHITE, size=9, align="left"):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == "center" else WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(str(text))
    run.bold = bold
    run.font.color.rgb = color
    run.font.size = Pt(size)
    run.font.name = "Arial"

def _add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Arial"
    run.font.size = Pt(16 if level == 1 else 12)
    run.font.color.rgb = GOLD if level == 1 else NAVY
    # bottom border on H1
    if level == 1:
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), "D4A843")
        pBdr.append(bottom)
        pPr.append(pBdr)
    return p

def _chart_bytes_bar(labels, values, benchmarks, title, figsize=(7, 2.8)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#0F2247")
    ax.set_facecolor("#0D1B2A")
    x = np.arange(len(labels))
    w = 0.35
    bars1 = ax.bar(x - w/2, values, w, color="#D4A843", label="Student Avg", zorder=3)
    bars2 = ax.bar(x + w/2, benchmarks, w, color="#3B6DC4", alpha=0.8, label="IBT Bench", zorder=3)
    ax.axhline(WASSCE, color="#4CAF50", linestyle="--", linewidth=1, label=f"WASSCE target ({WASSCE})", zorder=4)
    ax.axhline(AT_RISK, color="#EF5350", linestyle=":", linewidth=1, label=f"At-risk ({AT_RISK})", zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right", color="white", fontsize=7)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score", color="white", fontsize=8)
    ax.set_title(title, color="#D4A843", fontsize=9, pad=6)
    ax.tick_params(colors="white")
    ax.yaxis.set_tick_params(labelcolor="white")
    for spine in ax.spines.values():
        spine.set_color("#1E3A6A")
    ax.legend(fontsize=6, facecolor="#0D1B2A", labelcolor="white", loc="upper right")
    ax.grid(axis="y", color="#1E3A6A", linewidth=0.5, zorder=0)
    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x()+bar.get_width()/2, h+0.8, f"{h:.0f}", ha="center", va="bottom", color="white", fontsize=6)
    plt.tight_layout(pad=0.4)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf

def _chart_bytes_class_bar(students, avg_scores, figsize=(7, 2.6)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#0F2247")
    ax.set_facecolor("#0D1B2A")
    colors = ["#EF5350" if s < 50 else "#FFA726" if s < 65 else "#4CAF50" for s in avg_scores]
    bars = ax.bar(students, avg_scores, color=colors, zorder=3)
    ax.axhline(WASSCE, color="#4CAF50", linestyle="--", linewidth=1, label=f"WASSCE ({WASSCE})", zorder=4)
    ax.axhline(AT_RISK, color="#EF5350", linestyle=":", linewidth=1, label=f"At-risk ({AT_RISK})", zorder=4)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Avg Score", color="white", fontsize=8)
    ax.set_title("Class Performance Overview", color="#D4A843", fontsize=9)
    ax.tick_params(colors="white")
    ax.set_xticklabels(students, rotation=25, ha="right", fontsize=7, color="white")
    for spine in ax.spines.values():
        spine.set_color("#1E3A6A")
    ax.legend(fontsize=7, facecolor="#0D1B2A", labelcolor="white")
    ax.grid(axis="y", color="#1E3A6A", linewidth=0.5, zorder=0)
    for bar, val in zip(bars, avg_scores):
        ax.text(bar.get_x()+bar.get_width()/2, val+0.8, f"{val:.0f}", ha="center", va="bottom", color="white", fontsize=7)
    plt.tight_layout(pad=0.4)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_academic_word_report(grade_history, students, school_label, grade_en, ai_text=""):
    import pandas as pd
    df = pd.DataFrame(grade_history)
    df["date"] = pd.to_datetime(df["date"])
    df_sorted = df.sort_values("date")

    doc = Document()

    # ── Page setup ─────────────────────────────────────────────────────────────
    section = doc.sections[0]
    section.page_width  = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = section.right_margin = Cm(2)
    section.top_margin  = section.bottom_margin = Cm(2)

    # Default font
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10)

    # ── Cover banner ────────────────────────────────────────────────────────────
    banner = doc.add_table(rows=1, cols=1)
    banner.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner.style = "Table Grid"
    bc = banner.rows[0].cells[0]
    _cell_bg(bc, "0F2247")
    bc.width = Cm(17)
    bc.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p_logo = bc.paragraphs[0]
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_logo.add_run("🎓  INSTITUTE OF BASIC TECHNOLOGY")
    r1.bold = True; r1.font.size = Pt(16); r1.font.color.rgb = GOLD; r1.font.name = "Arial"
    p2 = bc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("Teacher Pehpeh — Academic Performance Report")
    r2.font.size = Pt(11); r2.font.color.rgb = WHITE; r2.font.name = "Arial"
    p3 = bc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run(f"{school_label}  |  {grade_en}  |  Generated {datetime.datetime.now().strftime('%B %d, %Y')}")
    r3.font.size = Pt(9); r3.font.color.rgb = LIGHT; r3.font.name = "Arial"
    bc.paragraphs[0].paragraph_format.space_before = Pt(6)
    bc.paragraphs[-1].paragraph_format.space_after = Pt(6)
    doc.add_paragraph()

    # ── Class summary metrics ───────────────────────────────────────────────────
    _add_heading(doc, "1. Class Summary", 1)
    avg_all    = df["score"].mean()
    n_students = df["student"].nunique()
    n_subjs    = df["subject"].nunique()
    n_records  = len(df)
    df_s       = df_sorted
    t3         = df_s.tail(max(1, len(df)//3))["score"].mean()
    e3         = df_s.head(max(1, len(df)//3))["score"].mean()
    trend_d    = t3 - e3
    below50    = df[df["score"] < 50]["student"].nunique()

    met_table = doc.add_table(rows=2, cols=4)
    met_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    met_table.style = "Table Grid"
    met_hdrs = ["Class Average", "Grade Trend", "Students Tracked", "Need Intervention"]
    met_vals = [
        f"{avg_all:.1f} / 100",
        f"{'↑' if trend_d > 2 else ('↓' if trend_d < -2 else '→')} {abs(trend_d):.1f} pts",
        f"{n_students} students · {n_records} records",
        f"{below50} of {n_students} ({(below50/max(1,n_students))*100:.0f}%)",
    ]
    hdr_bg = ["0D3B8C", "0D3B8C", "0D3B8C", "5C1010" if below50 > 0 else "0D3B14"]
    for ci, (h, v, bg) in enumerate(zip(met_hdrs, met_vals, hdr_bg)):
        _set_cell_text(met_table.rows[0].cells[ci], h, bold=True, color=WHITE, size=8, align="center")
        _cell_bg(met_table.rows[0].cells[ci], bg)
        _set_cell_text(met_table.rows[1].cells[ci], v, bold=True, color=GOLD, size=10, align="center")
        _cell_bg(met_table.rows[1].cells[ci], "131F30")
    doc.add_paragraph()

    # ── Class performance chart ─────────────────────────────────────────────────
    stu_names  = sorted(df["student"].unique())
    stu_avgs   = [df[df["student"]==s]["score"].mean() for s in stu_names]
    chart1_buf = _chart_bytes_class_bar([s.split()[0] for s in stu_names], stu_avgs)
    doc.add_picture(chart1_buf, width=Inches(6.5))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    # ── Student performance table ───────────────────────────────────────────────
    _add_heading(doc, "2. Student Performance Summary", 1)
    subj_list = sorted(df["subject"].unique())
    col_widths_dxa = [2200] + [1000]*len(subj_list) + [1100, 1100, 1200]
    col_headers    = ["Student"] + subj_list + ["Overall Avg", "Trend", "Status"]
    n_cols = len(col_headers)

    stu_tbl = doc.add_table(rows=1 + len(stu_names), cols=n_cols)
    stu_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    stu_tbl.style = "Table Grid"
    for ci, h in enumerate(col_headers):
        c = stu_tbl.rows[0].cells[ci]
        _set_cell_text(c, h, bold=True, color=WHITE, size=8, align="center")
        _cell_bg(c, "0D3B8C")

    for ri, sname in enumerate(stu_names, 1):
        sd = df[df["student"]==sname].sort_values("date")
        savg = sd["score"].mean()
        trend_val = sd["score"].iloc[-1] - sd["score"].iloc[0] if len(sd) > 1 else 0
        trend_str = "↑" if trend_val > 2 else ("↓" if trend_val < -2 else "→")
        status = "🔴 Intervention" if savg < 50 else ("🟡 Monitor" if savg < 65 else "🟢 On Track")
        row_bg  = "2A0A0A" if savg < 50 else ("2A1F00" if savg < 65 else "0A2A0A")
        row = stu_tbl.rows[ri]
        _set_cell_text(row.cells[0], sname, bold=True, color=GOLD, size=8)
        _cell_bg(row.cells[0], row_bg)
        for ci, subj in enumerate(subj_list, 1):
            subj_scores = sd[sd["subject"]==subj]["score"]
            val = f"{subj_scores.mean():.0f}" if len(subj_scores) > 0 else "—"
            avg_f = subj_scores.mean() if len(subj_scores) > 0 else None
            bench = IBT_BENCH.get(subj, 43.3)
            cell_bg = ("5C0A0A" if avg_f is not None and avg_f < bench else
                       "0D3B14" if avg_f is not None and avg_f >= WASSCE else "1A1A2E")
            _set_cell_text(row.cells[ci], val, color=WHITE, size=8, align="center")
            _cell_bg(row.cells[ci], cell_bg)
        _set_cell_text(row.cells[-3], f"{savg:.1f}", bold=True, color=GOLD, size=9, align="center")
        _cell_bg(row.cells[-3], row_bg)
        _set_cell_text(row.cells[-2], trend_str, color=WHITE, size=9, align="center")
        _cell_bg(row.cells[-2], row_bg)
        _set_cell_text(row.cells[-1], status, color=WHITE, size=8, align="center")
        _cell_bg(row.cells[-1], row_bg)
    doc.add_paragraph()

    # ── Per-subject charts (2 per row) ─────────────────────────────────────────
    _add_heading(doc, "3. Subject vs IBT Benchmark Analysis", 1)
    note = doc.add_paragraph()
    note.paragraph_format.space_after = Pt(4)
    nr = note.add_run("Red bars = below IBT benchmark  |  Blue bars = IBT historical average  |  Green dashed = WASSCE target (50)")
    nr.font.size = Pt(8); nr.font.color.rgb = LIGHT; nr.font.italic = True

    for si in range(0, len(subj_list), 2):
        img_pair = doc.add_table(rows=1, cols=2)
        img_pair.alignment = WD_TABLE_ALIGNMENT.CENTER
        img_pair.style = "Table Grid"
        for offset in range(2):
            if si + offset >= len(subj_list):
                break
            subj = subj_list[si + offset]
            subj_df = df[df["subject"] == subj]
            student_avgs = [subj_df[subj_df["student"]==s]["score"].mean() if len(subj_df[subj_df["student"]==s]) > 0 else 0 for s in stu_names]
            benches      = [IBT_BENCH.get(subj, 43.3)] * len(stu_names)
            chart_buf = _chart_bytes_bar(
                [s.split()[0] for s in stu_names], student_avgs, benches,
                f"{subj}", figsize=(3.8, 2.4)
            )
            cell = img_pair.rows[0].cells[offset]
            _cell_bg(cell, "0D1B2A")
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = cell.paragraphs[0].add_run()
            run.add_picture(chart_buf, width=Inches(3.1))
        doc.add_paragraph()

    # ── IBT Benchmark comparison table ────────────────────────────────────────
    _add_heading(doc, "4. IBT Benchmark Gap Analysis", 1)
    gap_tbl = doc.add_table(rows=1+len(subj_list), cols=5)
    gap_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    gap_tbl.style = "Table Grid"
    for ci, h in enumerate(["Subject", "Class Avg", "IBT Benchmark", "Gap", "Status"]):
        _set_cell_text(gap_tbl.rows[0].cells[ci], h, bold=True, color=WHITE, size=9, align="center")
        _cell_bg(gap_tbl.rows[0].cells[ci], "0F2247")
    for ri, subj in enumerate(subj_list, 1):
        subj_df = df[df["subject"]==subj]
        cavg    = subj_df["score"].mean() if len(subj_df) > 0 else None
        bench   = IBT_BENCH.get(subj, 43.3)
        gap     = (cavg - bench) if cavg is not None else None
        status  = ("🔴 Below IBT" if gap is not None and gap < 0 else "🟢 Above IBT")
        row_bg  = "2A0A0A" if (gap is not None and gap < 0) else "0A2A0A"
        row = gap_tbl.rows[ri]
        vals = [subj, f"{cavg:.1f}" if cavg else "—", f"{bench:.1f}", f"{gap:+.1f}" if gap is not None else "—", status]
        for ci, v in enumerate(vals):
            _set_cell_text(row.cells[ci], v, color=GOLD if ci == 0 else WHITE, size=9, align="center" if ci > 0 else "left")
            _cell_bg(row.cells[ci], row_bg)
    doc.add_paragraph()

    # ── AI analysis ────────────────────────────────────────────────────────────
    if ai_text:
        _add_heading(doc, "5. AI-Generated Academic Analysis", 1)
        for line in ai_text.split("\n"):
            line = line.strip()
            if not line:
                continue
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after  = Pt(2)
            is_section = line[0].isdigit() and ("." in line[:3] or ":" in line[:25])
            r = p.add_run(line)
            r.font.name = "Arial"
            if is_section:
                r.bold = True; r.font.size = Pt(10); r.font.color.rgb = GOLD
            else:
                r.font.size = Pt(9); r.font.color.rgb = RGBColor(0xCC, 0xD4, 0xE0)
        doc.add_paragraph()

    # ── Footer note ────────────────────────────────────────────────────────────
    footer_p = doc.add_paragraph()
    footer_p.paragraph_format.space_before = Pt(12)
    pPr = footer_p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    top = OxmlElement("w:top")
    top.set(qn("w:val"), "single"); top.set(qn("w:sz"), "4")
    top.set(qn("w:space"), "1"); top.set(qn("w:color"), "D4A843")
    pBdr.append(top); pPr.append(pBdr)
    fr = footer_p.add_run(f"Generated by Teacher Pehpeh — IBT Educational AI  |  {school_label}  |  Confidential")
    fr.font.size = Pt(8); fr.font.color.rgb = LIGHT; fr.italic = True; fr.font.name = "Arial"
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out.getvalue()
