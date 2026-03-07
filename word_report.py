"""
word_report.py — Teacher Pehpeh by IBT
Generates the Academic Performance Word (.docx) report.
Accessible typography: dark red / dark blue / black outside tables.
"""
import io, base64 as _b64wr
from datetime import datetime


def generate_academic_word_report(grade_history, students, school_label, grade_level, analysis_text=""):
    """Generate IBT Academic Performance Word report. Returns bytes."""
    try:
        from docx import Document
        from docx.shared import Pt, Inches, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.oxml.ns import qn as _qn
        from docx.oxml import OxmlElement as _OE

        # ── Import logo constants from app globals (injected at deploy time) ──
        try:
            from app import (_IBT_LOGO_MD_B64 as _IL, _PEHPEH_LOGO_MD_B64 as _PL,
                             _IBT_PHONE as _IP, _IBT_EMAIL as _IM, _IBT_URL as _IU)
        except Exception:
            _IL = _PL = ""; _IP = "(0777)-974-676"
            _IM = "support@institutebasictechnology.org"
            _IU = "https://www.institutebasictechnology.org/index.php"

        doc = Document()
        _style = doc.styles["Normal"]; _style.font.name = "Calibri"; _style.font.size = Pt(11)
        for sec in doc.sections:
            sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
            sec.left_margin = Inches(1.0); sec.right_margin = Inches(1.0)

        # ── Helper: remove table borders ──────────────────────────────────
        def _no_bdr(cell):
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            tcB = _OE("w:tcBorders")
            for s in ("top","left","bottom","right","insideH","insideV"):
                b = _OE(f"w:{s}"); b.set(_qn("w:val"), "none"); tcB.append(b)
            tcPr.append(tcB)

        # ── 3-col logo/contact header table ──────────────────────────────
        htbl = doc.add_table(rows=1, cols=3)
        htbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for hcell in list(htbl.columns[0].cells)+list(htbl.columns[1].cells)+list(htbl.columns[2].cells):
            _no_bdr(hcell)
        htbl.cell(0,0).width = Inches(1.2)
        htbl.cell(0,1).width = Inches(4.6)
        htbl.cell(0,2).width = Inches(1.2)
        # Left: IBT logo
        try:
            p0 = htbl.cell(0,0).paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p0.add_run().add_picture(io.BytesIO(_b64wr.b64decode(_IL)), height=Inches(0.75))
        except Exception: pass
        # Centre: contact info
        pc = htbl.cell(0,1).paragraphs[0]; pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc = pc.add_run("Institute of Basic Technology")
        rc.bold = True; rc.font.size = Pt(10); rc.font.color.rgb = RGBColor(0x8B,0x1A,0x1A)
        pc2 = htbl.cell(0,1).add_paragraph(f"{_IP}  |  {_IM}"); pc2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r2 in pc2.runs: r2.font.size = Pt(8.5); r2.font.color.rgb = RGBColor(0x00,0x33,0x99)
        pc3 = htbl.cell(0,1).add_paragraph("www.institutebasictechnology.org"); pc3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r3 in pc3.runs: r3.font.size = Pt(8); r3.font.color.rgb = RGBColor(0x00,0x33,0x99)
        # Right: Pehpeh logo
        try:
            p2 = htbl.cell(0,2).paragraphs[0]; p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p2.add_run().add_picture(io.BytesIO(_b64wr.b64decode(_PL)), height=Inches(0.75))
        except Exception: pass

        doc.add_paragraph()  # spacer

        # ── Title block (accessible dark red) ────────────────────────────
        tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        tr = tp.add_run("ACADEMIC PERFORMANCE REPORT")
        tr.bold = True; tr.font.size = Pt(18); tr.font.color.rgb = RGBColor(0x8B,0x1A,0x1A)

        sp = doc.add_paragraph(); sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sr = sp.add_run(f"{school_label}  |  Grade: {grade_level}  |  {datetime.now().strftime('%B %d, %Y')}")
        sr.font.size = Pt(10); sr.font.color.rgb = RGBColor(0x00,0x33,0x66)

        # ── Horizontal rule ───────────────────────────────────────────────
        from lxml import etree
        hr_p = doc.add_paragraph()
        hr_p.paragraph_format.space_after = Pt(10)
        pPr = hr_p._p.get_or_add_pPr()
        pBdr = etree.SubElement(pPr, _qn("w:pBdr"))
        bot = etree.SubElement(pBdr, _qn("w:bottom"))
        bot.set(_qn("w:val"), "single"); bot.set(_qn("w:sz"), "6")
        bot.set(_qn("w:color"), "8B1A1A"); bot.set(_qn("w:space"), "1")

        # ── Summary table ─────────────────────────────────────────────────
        if grade_history and students:
            import collections
            from math import sqrt

            def _cv(raw): return sqrt(max(0,raw)/100)*100

            by_stu = collections.defaultdict(list)
            for g in grade_history: by_stu[g["student"]].append(g)

            doc.add_paragraph()
            hp = doc.add_paragraph()
            for r in hp.runs: r.bold = True
            hrun = hp.add_run("Class Performance Summary")
            hrun.bold = True; hrun.font.size = Pt(13); hrun.font.color.rgb = RGBColor(0x8B,0x1A,0x1A)

            tbl = doc.add_table(rows=1, cols=4)
            tbl.style = "Table Grid"
            for hdr, cell in zip(["Student","Subjects Covered","Average Score","Curved Avg"],tbl.rows[0].cells):
                cell.text = hdr
                for run in cell.paragraphs[0].runs:
                    run.bold = True; run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
                from docx.oxml.ns import qn as _q2
                shading = _OE("w:shd")
                shading.set(_q2("w:val"),"clear"); shading.set(_q2("w:color"),"auto")
                shading.set(_q2("w:fill"),"1A3A6A")
                cell._tc.get_or_add_tcPr().append(shading)

            for sname, records in sorted(by_stu.items()):
                scores = [r["score"] for r in records]
                avg = sum(scores)/len(scores) if scores else 0
                cavg = sum(_cv(s) for s in scores)/len(scores) if scores else 0
                subjects = len({r.get("subject","") for r in records})
                row_cells = tbl.add_row().cells
                row_cells[0].text = sname
                row_cells[1].text = str(subjects)
                row_cells[2].text = f"{avg:.1f}/100"
                row_cells[3].text = f"{cavg:.1f}"
                for cell in row_cells:
                    for run in cell.paragraphs[0].runs:
                        run.font.size = Pt(10)

        # ── AI Analysis text ──────────────────────────────────────────────
        if analysis_text:
            doc.add_paragraph()
            ap = doc.add_paragraph()
            ar = ap.add_run("AI Performance Analysis")
            ar.bold = True; ar.font.size = Pt(13); ar.font.color.rgb = RGBColor(0x0D,0x3B,0x8C)
            for para_text in analysis_text.split("\n"):
                stripped = para_text.strip()
                if not stripped: doc.add_paragraph(); continue
                if stripped.startswith(("#","**","##")):
                    lvl = 2 if stripped.startswith("##") else 1
                    clean = stripped.lstrip("#").strip().strip("*")
                    ph = doc.add_heading(clean, level=lvl)
                    for run in ph.runs:
                        run.font.color.rgb = RGBColor(0x0D,0x3B,0x8C) if lvl==2 else RGBColor(0x8B,0x1A,0x1A)
                else:
                    pp = doc.add_paragraph(stripped)
                    for run in pp.runs: run.font.size = Pt(10.5); run.font.color.rgb = RGBColor(0,0,0)

        # ── Footer ────────────────────────────────────────────────────────
        doc.add_paragraph()
        fp = doc.add_paragraph(); fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        from lxml import etree as et2
        hr2 = fp._p.get_or_add_pPr()
        pBdr2 = et2.SubElement(hr2, _qn("w:pBdr"))
        bt2 = et2.SubElement(pBdr2, _qn("w:top"))
        bt2.set(_qn("w:val"),"single"); bt2.set(_qn("w:sz"),"4")
        bt2.set(_qn("w:color"),"8B1A1A"); bt2.set(_qn("w:space"),"1")
        fp2 = doc.add_paragraph(); fp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fr = fp2.add_run(f"Teacher Pehpeh by IBT  |  {_IP}  |  {_IM}  |  www.institutebasictechnology.org")
        fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(0x00,0x33,0x66); fr.italic = True

        buf = io.BytesIO(); doc.save(buf); buf.seek(0); return buf.getvalue()
    except Exception as e:
        raise RuntimeError(f"word_report error: {e}") from e
