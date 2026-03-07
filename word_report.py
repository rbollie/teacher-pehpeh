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

        try:
            from app import (_IBT_LOGO_MD_B64 as _IL, _PEHPEH_LOGO_MD_B64 as _PL,
                             _IBT_PHONE as _IP, _IBT_EMAIL as _IM)
        except Exception:
            _IL = _PL = ""; _IP = "(0777)-974-676"
            _IM = "support@institutebasictechnology.org"

        doc = Document()

        # Tight global spacing
        _sty = doc.styles["Normal"]
        _sty.font.name = "Calibri"; _sty.font.size = Pt(10.5)
        _sty.paragraph_format.space_before = Pt(0)
        _sty.paragraph_format.space_after  = Pt(3)

        for sec in doc.sections:
            sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.8)
            sec.left_margin = Inches(1.0); sec.right_margin  = Inches(1.0)

        def _no_bdr(cell):
            tc = cell._tc; tcPr = tc.get_or_add_tcPr()
            tcB = _OE("w:tcBorders")
            for s in ("top","left","bottom","right","insideH","insideV"):
                b = _OE(f"w:{s}"); b.set(_qn("w:val"), "none"); tcB.append(b)
            tcPr.append(tcB)

        def _micro():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(2)

        def _heading(text, level=1, color=(139,26,26)):
            # Use plain paragraph with explicit formatting to avoid
            # Word heading-style spacing overrides
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8 if level == 1 else 6)
            p.paragraph_format.space_after  = Pt(3)
            sz = Pt(13) if level == 1 else Pt(11)
            run = p.add_run(text)
            run.bold = True; run.font.size = sz
            run.font.color.rgb = RGBColor(*color)
            return p

        # 3-col logo header
        htbl = doc.add_table(rows=1, cols=3); htbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for hcell in list(htbl.columns[0].cells)+list(htbl.columns[1].cells)+list(htbl.columns[2].cells):
            _no_bdr(hcell)
        htbl.cell(0,0).width = Inches(1.2); htbl.cell(0,1).width = Inches(4.6); htbl.cell(0,2).width = Inches(1.2)
        try:
            p0 = htbl.cell(0,0).paragraphs[0]; p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p0.add_run().add_picture(io.BytesIO(_b64wr.b64decode(_IL)), height=Inches(0.75))
        except Exception: pass
        pc = htbl.cell(0,1).paragraphs[0]; pc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pc.paragraph_format.space_after = Pt(1)
        rc = pc.add_run("Institute of Basic Technology")
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

        # Title
        tp = doc.add_paragraph(); tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        tp.paragraph_format.space_before = Pt(6); tp.paragraph_format.space_after = Pt(2)
        tr = tp.add_run("ACADEMIC PERFORMANCE REPORT")
        tr.bold = True; tr.font.size = Pt(16); tr.font.color.rgb = RGBColor(0x8B,0x1A,0x1A)
        sp = doc.add_paragraph(); sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.space_after = Pt(4)
        sr = sp.add_run(f"{school_label}  |  Grade: {grade_level}  |  {datetime.now().strftime('%B %d, %Y')}")
        sr.font.size = Pt(9.5); sr.font.color.rgb = RGBColor(0x00,0x33,0x66)

        # Thin rule
        from lxml import etree
        hr_p = doc.add_paragraph()
        hr_p.paragraph_format.space_before = Pt(0); hr_p.paragraph_format.space_after = Pt(5)
        pPr = hr_p._p.get_or_add_pPr()
        pBdr = etree.SubElement(pPr, _qn("w:pBdr"))
        bot = etree.SubElement(pBdr, _qn("w:bottom"))
        bot.set(_qn("w:val"), "single"); bot.set(_qn("w:sz"), "6")
        bot.set(_qn("w:color"), "8B1A1A"); bot.set(_qn("w:space"), "1")

        # Class summary table
        if grade_history and students:
            import collections
            from math import sqrt
            def _cv(raw): return sqrt(max(0, raw) / 100) * 100
            by_stu = collections.defaultdict(list)
            for g in grade_history: by_stu[g["student"]].append(g)
            _heading("Class Performance Summary")
            tbl = doc.add_table(rows=1, cols=4); tbl.style = "Table Grid"
            for hdr, cell in zip(["Student","Subjects","Avg Score","Curved Avg"], tbl.rows[0].cells):
                cell.text = hdr
                for run in cell.paragraphs[0].runs:
                    run.bold = True; run.font.size = Pt(9.5); run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
                shading = _OE("w:shd"); shading.set(_qn("w:val"),"clear"); shading.set(_qn("w:color"),"auto"); shading.set(_qn("w:fill"),"1A3A6A")
                cell._tc.get_or_add_tcPr().append(shading)
            for sname, records in sorted(by_stu.items()):
                scores = [r["score"] for r in records]
                avg  = sum(scores)/len(scores) if scores else 0
                cavg = sum(_cv(s) for s in scores)/len(scores) if scores else 0
                row_cells = tbl.add_row().cells
                for cell, val in zip(row_cells, [sname, str(len({r.get("subject","") for r in records})), f"{avg:.1f}/100", f"{cavg:.1f}"]):
                    cell.text = val
                    for run in cell.paragraphs[0].runs: run.font.size = Pt(9.5)

        # AI Analysis — tight line-by-line rendering
        if analysis_text:
            _micro()
            _heading("AI Performance Analysis", level=1, color=(13,59,140))
            lines = analysis_text.split("\n")
            prev_blank = False
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    if not prev_blank:
                        _micro()
                    prev_blank = True
                    continue
                prev_blank = False
                clean = stripped.replace("**","").replace("__","")

                # Markdown heading
                if stripped.startswith("## ") or stripped.startswith("### "):
                    _heading(stripped.lstrip("#").strip(), level=2, color=(13,59,140))
                elif stripped.startswith("# "):
                    _heading(stripped.lstrip("#").strip(), level=1, color=(139,26,26))

                # Numbered section header e.g. "1. TITLE" or "1) ..."
                elif (len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in ".):" and stripped[2:].strip()) or \
                     (len(stripped) > 3 and stripped[:2].isdigit() and stripped[2] in ".):"):
                    # Use plain bold paragraph — NOT doc.add_heading() which inherits
                    # unpredictable Word style spacing that overrides our settings
                    ph = doc.add_paragraph()
                    ph.paragraph_format.space_before = Pt(7)
                    ph.paragraph_format.space_after  = Pt(2)
                    pr = ph.add_run(clean)
                    pr.bold = True; pr.font.size = Pt(11)
                    pr.font.color.rgb = RGBColor(139,26,26)

                # Bullet
                elif stripped[:2] in ("- ","* ","• "):
                    bp = doc.add_paragraph(clean[2:], style="List Bullet")
                    bp.paragraph_format.space_before = Pt(1); bp.paragraph_format.space_after = Pt(1)
                    for run in bp.runs: run.font.size = Pt(10)

                # ALL-CAPS label (e.g. "RISK PROFILE SUMMARY:")
                elif clean == clean.upper() and len(clean) > 4:
                    ph = doc.add_paragraph()
                    ph.paragraph_format.space_before = Pt(7)
                    ph.paragraph_format.space_after  = Pt(2)
                    pr = ph.add_run(clean.rstrip(":"))
                    pr.bold = True; pr.font.size = Pt(11)
                    pr.font.color.rgb = RGBColor(139,26,26)

                # Body
                else:
                    pp = doc.add_paragraph(clean)
                    pp.paragraph_format.space_before = Pt(1); pp.paragraph_format.space_after = Pt(3)
                    for run in pp.runs: run.font.size = Pt(10.5); run.font.color.rgb = RGBColor(0,0,0)

        # Footer
        _micro()
        fp = doc.add_paragraph(); fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.paragraph_format.space_before = Pt(4); fp.paragraph_format.space_after = Pt(0)
        fr = fp.add_run(f"Teacher Pehpeh by IBT  |  {_IP}  |  {_IM}  |  www.institutebasictechnology.org")
        fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(0x00,0x33,0x66); fr.italic = True

        buf = io.BytesIO(); doc.save(buf); buf.seek(0); return buf.getvalue()
    except Exception as e:
        raise RuntimeError(f"word_report error: {e}") from e
