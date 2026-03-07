"""
word_report.py — Teacher Pehpeh by IBT
Generates the Academic Performance Word (.docx) report.
Accessible typography: dark red / dark blue / black outside tables.
"""
import io, base64 as _b64wr
from datetime import datetime
from math import sqrt


def generate_academic_word_report(
    grade_history, students, school_label, grade_level,
    analysis_text="", subject_data=None
):
    """
    Generate IBT Academic Performance Word report. Returns bytes.

    subject_data : dict  {subject -> {student -> {"s1_avg": float|None, "s2_avg": float|None}}}
                  If provided, adds Subject Breakdown and Individual-by-Subject-Semester tables.
    """
    try:
        from docx import Document
        from docx.shared import Pt, Inches, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.oxml.ns import qn as _qn
        from docx.oxml import OxmlElement as _OE
        from lxml import etree
        import pandas as _pd, collections

        try:
            from app import (_IBT_LOGO_MD_B64 as _IL, _PEHPEH_LOGO_MD_B64 as _PL,
                             _IBT_PHONE as _IP, _IBT_EMAIL as _IM)
        except Exception:
            _IL = _PL = ""; _IP = "(0777)-974-676"
            _IM = "support@institutebasictechnology.org"

        doc = Document()

        # ── Global tight spacing ───────────────────────────────────────────
        _sty = doc.styles["Normal"]
        _sty.font.name = "Calibri"; _sty.font.size = Pt(10.5)
        _sty.paragraph_format.space_before = Pt(0)
        _sty.paragraph_format.space_after  = Pt(3)

        for sec in doc.sections:
            sec.top_margin    = Inches(0.75); sec.bottom_margin = Inches(0.75)
            sec.left_margin   = Inches(0.9);  sec.right_margin  = Inches(0.9)

        # ── Helpers ────────────────────────────────────────────────────────
        def _no_bdr(cell):
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            tcB = _OE("w:tcBorders")
            for s in ("top","left","bottom","right","insideH","insideV"):
                b = _OE(f"w:{s}"); b.set(_qn("w:val"), "none"); tcB.append(b)
            tcPr.append(tcB)

        def _micro():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(2)

        def _heading(text, level=1, color=(139, 26, 26)):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8 if level == 1 else 6)
            p.paragraph_format.space_after  = Pt(3)
            run = p.add_run(text)
            run.bold = True
            run.font.size = Pt(13 if level == 1 else 11)
            run.font.color.rgb = RGBColor(*color)
            return p

        def _hr():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(5)
            pPr = p._p.get_or_add_pPr()
            pBdr = etree.SubElement(pPr, _qn("w:pBdr"))
            bot  = etree.SubElement(pBdr, _qn("w:bottom"))
            bot.set(_qn("w:val"),   "single"); bot.set(_qn("w:sz"), "6")
            bot.set(_qn("w:color"), "8B1A1A"); bot.set(_qn("w:space"), "1")

        def _tbl_hdr(tbl, headers, fill="1A3A6A"):
            hrow = tbl.rows[0]
            for cell, txt in zip(hrow.cells, headers):
                cell.text = txt
                for run in cell.paragraphs[0].runs:
                    run.bold = True; run.font.size = Pt(9); run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
                shd = _OE("w:shd"); shd.set(_qn("w:val"), "clear")
                shd.set(_qn("w:color"), "auto"); shd.set(_qn("w:fill"), fill)
                cell._tc.get_or_add_tcPr().append(shd)

        def _tbl_row(tbl, values, alt=False):
            fill = "EEF2F8" if alt else "FFFFFF"
            row = tbl.add_row()
            for cell, val in zip(row.cells, values):
                cell.text = str(val) if val is not None else "—"
                for run in cell.paragraphs[0].runs:
                    run.font.size = Pt(9.5)
                shd = _OE("w:shd"); shd.set(_qn("w:val"), "clear")
                shd.set(_qn("w:color"), "auto"); shd.set(_qn("w:fill"), fill)
                cell._tc.get_or_add_tcPr().append(shd)

        def _curved(raw):
            return round(sqrt(max(0.0, float(raw)) / 100.0) * 100.0, 1)

        def _status(avg):
            if avg is None: return "—"
            return "Intervention" if avg < 50 else ("Monitor" if avg < 65 else "On Track")

        def _fmt(v):
            return f"{v:.1f}/100" if v is not None else "—"

        # ── 3-col Logo Header ──────────────────────────────────────────────
        htbl = doc.add_table(rows=1, cols=3)
        htbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for hcell in (list(htbl.columns[0].cells) + list(htbl.columns[1].cells)
                      + list(htbl.columns[2].cells)):
            _no_bdr(hcell)
        htbl.cell(0,0).width = Inches(1.2)
        htbl.cell(0,1).width = Inches(4.6)
        htbl.cell(0,2).width = Inches(1.2)
        try:
            p0 = htbl.cell(0,0).paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p0.add_run().add_picture(io.BytesIO(_b64wr.b64decode(_IL)), height=Inches(0.75))
        except Exception: pass
        pc  = htbl.cell(0,1).paragraphs[0]; pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pc.paragraph_format.space_after = Pt(1)
        rc  = pc.add_run("Institute of Basic Technology")
        rc.bold = True; rc.font.size = Pt(10); rc.font.color.rgb = RGBColor(0x8B,0x1A,0x1A)
        pc2 = htbl.cell(0,1).add_paragraph(f"{_IP}  |  {_IM}")
        pc2.alignment = WD_ALIGN_PARAGRAPH.CENTER; pc2.paragraph_format.space_after = Pt(1)
        for r2 in pc2.runs: r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(0x00,0x33,0x99)
        pc3 = htbl.cell(0,1).add_paragraph("www.institutebasictechnology.org")
        pc3.alignment = WD_ALIGN_PARAGRAPH.CENTER; pc3.paragraph_format.space_after = Pt(0)
        for r3 in pc3.runs: r3.font.size = Pt(8); r3.font.color.rgb = RGBColor(0x00,0x33,0x99)
        try:
            p2 = htbl.cell(0,2).paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p2.add_run().add_picture(io.BytesIO(_b64wr.b64decode(_PL)), height=Inches(0.75))
        except Exception: pass

        # ── Title ──────────────────────────────────────────────────────────
        tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        tp.paragraph_format.space_before = Pt(6); tp.paragraph_format.space_after = Pt(2)
        tr = tp.add_run("ACADEMIC PERFORMANCE REPORT")
        tr.bold = True; tr.font.size = Pt(16); tr.font.color.rgb = RGBColor(0x8B,0x1A,0x1A)
        sp = doc.add_paragraph(); sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_after = Pt(4)
        sr = sp.add_run(f"{school_label}  |  Grade: {grade_level}  |  {datetime.now().strftime('%B %d, %Y')}")
        sr.font.size = Pt(9.5); sr.font.color.rgb = RGBColor(0x00,0x33,0x66)
        _hr()

        # ── Build shared DataFrame ─────────────────────────────────────────
        n_subjs = 0
        _df = None
        if grade_history:
            _df = _pd.DataFrame(grade_history)
            _df["score"] = _pd.to_numeric(_df["score"], errors="coerce")
            n_subjs = _df["subject"].dropna().nunique()

        # ── SECTION 1: Class Performance Summary ──────────────────────────
        if grade_history and _df is not None:
            by_stu = collections.defaultdict(list)
            for g in grade_history:
                by_stu[g["student"]].append(g)

            _heading("1. Class Performance Summary")
            tbl1 = doc.add_table(rows=1, cols=5); tbl1.style = "Table Grid"
            _tbl_hdr(tbl1, ["Student", "Subjects", "Overall Avg", "IBT Curved Avg", "Status"])
            for idx, (sname, records) in enumerate(sorted(by_stu.items())):
                scores = [r["score"] for r in records]
                avg    = sum(scores) / len(scores) if scores else 0
                cavg   = sum(_curved(s) for s in scores) / len(scores) if scores else 0
                subjs  = len({r.get("subject","") for r in records})
                _tbl_row(tbl1, [sname, subjs, _fmt(avg), _fmt(cavg), _status(avg)],
                         alt=(idx % 2 == 1))

        # ── SECTION 2: Subject Breakdown — Class Averages ─────────────────
        if _df is not None and n_subjs > 1:
            _micro()
            _heading("2. Subject Breakdown — Class Averages")

            _sd = subject_data or {}
            _has_sem = any(
                v.get("s1_avg") is not None or v.get("s2_avg") is not None
                for sd in _sd.values() for v in sd.values()
            )

            if _has_sem:
                hdrs2 = ["Subject", "Class Avg", "Sem 1 Cls Avg", "Sem 2 Cls Avg",
                         "Top Student", "Lowest Score"]
            else:
                hdrs2 = ["Subject", "Class Avg", "# Records", "Top Student", "Lowest Score"]

            tbl2 = doc.add_table(rows=1, cols=len(hdrs2)); tbl2.style = "Table Grid"
            _tbl_hdr(tbl2, hdrs2)

            for idx, subj in enumerate(sorted(_df["subject"].dropna().unique())):
                _sdf = _df[_df["subject"] == subj]
                cls_avg = _sdf["score"].mean() if not _sdf.empty else None
                top_stu = (_sdf.loc[_sdf["score"].idxmax(), "student"]
                           if not _sdf.empty else "—")
                low_sc  = _sdf["score"].min() if not _sdf.empty else None

                if _has_sem:
                    s1_vals = [v["s1_avg"] for v in _sd.get(subj, {}).values()
                               if v.get("s1_avg") is not None]
                    s2_vals = [v["s2_avg"] for v in _sd.get(subj, {}).values()
                               if v.get("s2_avg") is not None]
                    s1_cls = sum(s1_vals)/len(s1_vals) if s1_vals else None
                    s2_cls = sum(s2_vals)/len(s2_vals) if s2_vals else None
                    row_vals = [subj, _fmt(cls_avg), _fmt(s1_cls), _fmt(s2_cls),
                                top_stu, _fmt(low_sc)]
                else:
                    row_vals = [subj, _fmt(cls_avg), len(_sdf), top_stu, _fmt(low_sc)]

                _tbl_row(tbl2, row_vals, alt=(idx % 2 == 1))

        # ── SECTION 3: Individual Averages by Subject & Semester ──────────
        _sd = subject_data or {}
        _has_sem_ind = any(
            v.get("s1_avg") is not None or v.get("s2_avg") is not None
            for sd in _sd.values() for v in sd.values()
        )

        if _has_sem_ind:
            _micro()
            _heading("3. Individual Averages by Subject & Semester")
            tbl3 = doc.add_table(rows=1, cols=6); tbl3.style = "Table Grid"
            _tbl_hdr(tbl3, ["Student", "Subject", "Semester 1", "Semester 2",
                            "Overall Avg", "Status"])
            _all_stus  = sorted({stu for sd in _sd.values() for stu in sd})
            _all_subjs = sorted(_sd.keys())
            _row_idx   = 0
            for stu in _all_stus:
                for subj in _all_subjs:
                    entry = _sd.get(subj, {}).get(stu, {})
                    s1 = entry.get("s1_avg"); s2 = entry.get("s2_avg")
                    if s1 is None and s2 is None:
                        continue
                    vals    = [v for v in [s1, s2] if v is not None]
                    overall = round(sum(vals)/len(vals), 1)
                    _tbl_row(tbl3,
                        [stu, subj, _fmt(s1), _fmt(s2), _fmt(overall), _status(overall)],
                        alt=(_row_idx % 2 == 1))
                    _row_idx += 1

        elif _df is not None and n_subjs > 1:
            # Fallback: no semester split available
            _micro()
            _heading("3. Individual Averages by Subject")
            tbl3b = doc.add_table(rows=1, cols=4); tbl3b.style = "Table Grid"
            _tbl_hdr(tbl3b, ["Student", "Subject", "Avg Score", "Status"])
            _row_idx = 0
            for stu in sorted(_df["student"].dropna().unique()):
                for subj in sorted(_df["subject"].dropna().unique()):
                    _sdf2 = _df[(_df["student"]==stu) & (_df["subject"]==subj)]
                    if _sdf2.empty: continue
                    avg2 = _sdf2["score"].mean()
                    _tbl_row(tbl3b, [stu, subj, _fmt(avg2), _status(avg2)],
                             alt=(_row_idx % 2 == 1))
                    _row_idx += 1

        # ── SECTION 4: AI Analysis ────────────────────────────────────────
        if analysis_text:
            _sec_n = 4 if (_df is not None and n_subjs > 1) else (3 if grade_history else 2)
            _micro()
            _heading(f"{_sec_n}. AI Performance Analysis", level=1, color=(13,59,140))
            lines = analysis_text.split("\n")
            prev_blank = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    if not prev_blank: _micro()
                    prev_blank = True; continue
                prev_blank = False
                clean = stripped.replace("**","").replace("__","")

                if stripped.startswith("## ") or stripped.startswith("### "):
                    _heading(stripped.lstrip("#").strip(), level=2, color=(13,59,140))
                elif stripped.startswith("# "):
                    _heading(stripped.lstrip("#").strip(), level=1, color=(139,26,26))
                elif (len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ".):") or \
                     (len(stripped) > 3 and stripped[:2].isdigit() and stripped[2] in ".):"):
                    ph = doc.add_paragraph()
                    ph.paragraph_format.space_before = Pt(7); ph.paragraph_format.space_after = Pt(2)
                    pr = ph.add_run(clean)
                    pr.bold = True; pr.font.size = Pt(11); pr.font.color.rgb = RGBColor(139,26,26)
                elif stripped[:2] in ("- ","* ","• "):
                    bp = doc.add_paragraph(clean[2:], style="List Bullet")
                    bp.paragraph_format.space_before = Pt(1); bp.paragraph_format.space_after = Pt(1)
                    for run in bp.runs: run.font.size = Pt(10)
                elif clean == clean.upper() and len(clean) > 4:
                    ph = doc.add_paragraph()
                    ph.paragraph_format.space_before = Pt(7); ph.paragraph_format.space_after = Pt(2)
                    pr = ph.add_run(clean.rstrip(":"))
                    pr.bold = True; pr.font.size = Pt(11); pr.font.color.rgb = RGBColor(139,26,26)
                else:
                    pp = doc.add_paragraph(clean)
                    pp.paragraph_format.space_before = Pt(1); pp.paragraph_format.space_after = Pt(3)
                    for run in pp.runs:
                        run.font.size = Pt(10.5); run.font.color.rgb = RGBColor(0,0,0)

        # ── Footer ────────────────────────────────────────────────────────
        _micro()
        fp = doc.add_paragraph(); fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.paragraph_format.space_before = Pt(4); fp.paragraph_format.space_after = Pt(0)
        fr = fp.add_run(
            f"Teacher Pehpeh by IBT  |  {_IP}  |  {_IM}  |  www.institutebasictechnology.org"
        )
        fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(0x00,0x33,0x66); fr.italic = True

        buf = io.BytesIO(); doc.save(buf); buf.seek(0); return buf.getvalue()

    except Exception as e:
        raise RuntimeError(f"word_report error: {e}") from e
