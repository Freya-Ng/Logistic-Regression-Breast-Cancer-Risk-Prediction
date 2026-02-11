"""
PDF report generator using fpdf2.

Produces a professional multi-page clinical report with:
  - Header & classification result
  - Clinical summary
  - Tumor characteristic analysis (size, shape, texture)
  - Measurements table
  - Result interpretation & next steps
  - Empathetic patient note
  - Lifestyle & wellness advice
  - Model methodology note
  - Disclaimer
"""

from datetime import date
from fpdf import FPDF
from .config import SECTIONS, FEATURES_RAW
from .model import FEAT_MEAN
from .translations import LANG, t


# ── Helpers ──────────────────────────────────────────────────────────────────

def _safe(text: str) -> str:
    """Strip HTML tags and replace Unicode chars unsupported by Helvetica."""
    return (text
            .replace("<strong>", "").replace("</strong>", "")
            .replace("\u2014", "--").replace("\u2013", "-")
            .replace("\u2018", "'").replace("\u2019", "'")
            .replace("\u201c", '"').replace("\u201d", '"'))


def _section_heading(pdf: FPDF, title: str) -> None:
    """Render a coloured section heading bar."""
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(240, 244, 248)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 9, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.ln(3)
    pdf.set_text_color(0, 0, 0)


def _body_text(pdf: FPDF, text: str, size: int = 10) -> None:
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(0, 5.5, _safe(text))
    pdf.ln(2)


def _sub_heading(pdf: FPDF, title: str) -> None:
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")


# ── Main generator ───────────────────────────────────────────────────────────

def generate_pdf(lang: str, inputs_dict: dict, cls_name: str, mal_pct: float) -> bytes:
    """Build a comprehensive clinical PDF report and return raw bytes."""
    is_malignant = mal_pct >= 50
    ben_pct = 100 - mal_pct

    # Extract key values for tumour analysis
    vals = {row[0]: inputs_dict.get(row[0], 0) for row in FEATURES_RAW}
    mean_radius    = float(vals.get("mean_radius", 0) or 0)
    mean_area      = float(vals.get("mean_area", 0) or 0)
    mean_compact   = float(vals.get("mean_compactness", 0) or 0)
    mean_concavity = float(vals.get("mean_concavity", 0) or 0)
    mean_texture   = float(vals.get("mean_texture", 0) or 0)
    mean_symmetry  = float(vals.get("mean_symmetry", 0) or 0)

    # Population averages for comparison
    avg_radius    = float(FEAT_MEAN[0])
    avg_compact   = float(FEAT_MEAN[5])
    avg_concavity = float(FEAT_MEAN[6])
    avg_texture   = float(FEAT_MEAN[1])
    avg_symmetry  = float(FEAT_MEAN[8])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ═════════════════════════════════════════════════════════════════════════
    #  PAGE 1 — Header, Result, Clinical Summary
    # ═════════════════════════════════════════════════════════════════════════

    pdf.add_page()

    # Title block
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 12, t("pdf_clinical_report", lang),
             new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"{t('pdf_date', lang)}: {date.today().isoformat()}",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 6, f"{t('pdf_method', lang)}: {t('pdf_method_desc', lang)}",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)

    # Horizontal rule
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(6)

    # Classification result
    pdf.set_font("Helvetica", "B", 16)
    if is_malignant:
        pdf.set_text_color(220, 38, 38)
    else:
        pdf.set_text_color(5, 150, 105)
    pdf.cell(0, 11, f"{cls_name}  -  {mal_pct:.2f}% {t('prob_caption', lang)}",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Probability bar
    bar_x, bar_w, bar_h = 40, 130, 8
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(bar_x, pdf.get_y(), bar_w, bar_h)
    fill_w = bar_w * mal_pct / 100
    if is_malignant:
        pdf.set_fill_color(220, 38, 38)
    else:
        pdf.set_fill_color(5, 150, 105)
    pdf.rect(bar_x, pdf.get_y(), fill_w, bar_h, "F")
    pdf.ln(bar_h + 2)

    # Labels under bar
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(bar_w / 2, 5, f"{t('benign', lang)}: {ben_pct:.1f}%",
             align="L")
    pdf.cell(bar_w / 2 + 20, 5, f"{t('malignant', lang)}: {mal_pct:.1f}%",
             new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.ln(6)

    # Clinical summary
    _section_heading(pdf, t("pdf_summary_title", lang))
    summary_key = "pdf_summary_malignant" if is_malignant else "pdf_summary_benign"
    _body_text(pdf, t(summary_key, lang))

    # ═════════════════════════════════════════════════════════════════════════
    #  PAGE 2 — Tumor Characteristic Analysis
    # ═════════════════════════════════════════════════════════════════════════

    pdf.add_page()
    _section_heading(pdf, t("pdf_tumor_analysis", lang))

    # Size & Growth
    _sub_heading(pdf, t("pdf_size_title", lang))
    size_elevated = mean_radius > avg_radius * 1.15
    size_key = "pdf_size_elevated" if size_elevated else "pdf_size_normal"
    _body_text(pdf, t(size_key, lang, val=mean_radius, area=mean_area))

    # Shape & Regularity
    _sub_heading(pdf, t("pdf_shape_title", lang))
    shape_irregular = (mean_compact > avg_compact * 1.2
                       or mean_concavity > avg_concavity * 1.3)
    shape_key = "pdf_shape_irregular" if shape_irregular else "pdf_shape_normal"
    _body_text(pdf, t(shape_key, lang, compact=mean_compact,
                      concave=mean_concavity))

    # Texture & Symmetry
    _sub_heading(pdf, t("pdf_texture_title", lang))
    texture_abnormal = (mean_texture > avg_texture * 1.15
                        or mean_symmetry > avg_symmetry * 1.15)
    texture_key = "pdf_texture_abnormal" if texture_abnormal else "pdf_texture_normal"
    _body_text(pdf, t(texture_key, lang, texture=mean_texture,
                      symmetry=mean_symmetry))

    # ═════════════════════════════════════════════════════════════════════════
    #  Measurements Table
    # ═════════════════════════════════════════════════════════════════════════

    pdf.ln(2)
    _section_heading(pdf, t("sidebar_title", lang))

    for _sid, feat_list, sec_key, _ in SECTIONS:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_fill_color(230, 236, 242)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 6, f"  {t(sec_key, lang)}", new_x="LMARGIN",
                 new_y="NEXT", fill=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(55, 65, 81)
        for key, en_label, vi_label, *_ in feat_list:
            lbl = en_label if lang == "en" else vi_label
            val = inputs_dict.get(key, 0)
            pdf.cell(50, 5.5, f"    {lbl}")
            pdf.cell(40, 5.5, f"{val:.6f}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    # ═════════════════════════════════════════════════════════════════════════
    #  PAGE 3 — Interpretation, Next Steps, Patient Note
    # ═════════════════════════════════════════════════════════════════════════

    pdf.add_page()

    # Result interpretation
    _section_heading(pdf, t("interpret_title", lang))
    ikey = "interpret_malignant" if is_malignant else "interpret_benign"
    _body_text(pdf, t(ikey, lang))

    # Next steps
    _section_heading(pdf, t("next_steps_title", lang))
    skey = "next_steps_malignant" if is_malignant else "next_steps_benign"
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    for i, step in enumerate(LANG[skey][lang], 1):
        pdf.multi_cell(0, 5.5, _safe(f"  {i}. {step}"))
        pdf.ln(1)
    pdf.ln(3)

    # Empathetic patient note
    _section_heading(pdf, t("pdf_reassurance_title", lang))
    rkey = "pdf_reassurance_malignant" if is_malignant else "pdf_reassurance_benign"
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(55, 65, 81)
    pdf.multi_cell(0, 5.5, _safe(t(rkey, lang)))
    pdf.ln(4)

    # ═════════════════════════════════════════════════════════════════════════
    #  PAGE 4 — Lifestyle Advice, Model Note, Disclaimer
    # ═════════════════════════════════════════════════════════════════════════

    pdf.add_page()

    # Lifestyle advice
    _section_heading(pdf, t("pdf_lifestyle_title", lang))
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(55, 65, 81)
    for i, advice in enumerate(LANG["pdf_lifestyle"][lang], 1):
        pdf.multi_cell(0, 5.5, _safe(f"  {i}. {advice}"))
        pdf.ln(1.5)
    pdf.ln(4)

    # Model methodology note
    _section_heading(pdf, t("pdf_model_note_title", lang))
    _body_text(pdf, t("pdf_model_note", lang), size=9)
    pdf.ln(4)

    # Disclaimer
    pdf.set_draw_color(200, 200, 200)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 4.5, _safe(t("disclaimer", lang)))

    return bytes(pdf.output())
