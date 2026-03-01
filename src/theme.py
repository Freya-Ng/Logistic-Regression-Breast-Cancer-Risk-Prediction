"""
Light / dark theme system with CSS injection.
"""

import streamlit as st

THEMES = {
    "light": dict(
        bg="#fdf2f8", card="#ffffff", sidebar="#fdf2f8",
        text="#1e0a2e", text_sec="#6d28d9", text_muted="#71717a",
        border="#e9d5ff", input_border="#a78bfa", stat_bg="#f5f3ff",
        info_bg="#fdf4ff", info_border="#d8b4fe", info_text="#5b21b6",
        waiting_icon_bg="#f5f3ff",
        interpret_benign_bg="#ecfdf5", interpret_benign_border="#6ee7b7",
        interpret_benign_h="#065f46", interpret_benign_t="#064e3b",
        interpret_mal_bg="#fef2f2", interpret_mal_border="#fca5a5",
        interpret_mal_h="#991b1b", interpret_mal_t="#7f1d1d",
        glossary_label="#7c3aed", glossary_text="#4b5563",
        metric_accent="#9333ea",
    ),
    "dark": dict(
        bg="#0a0414", card="#150828", sidebar="#150828",
        text="#f5f3ff", text_sec="#ddd6fe", text_muted="#a78bfa",
        border="#3b1573", input_border="#5b21b6", stat_bg="#1e0d3a",
        info_bg="rgba(124,58,237,0.12)", info_border="#4c1d95", info_text="#c4b5fd",
        waiting_icon_bg="#150828",
        interpret_benign_bg="rgba(5,150,105,0.15)", interpret_benign_border="#059669",
        interpret_benign_h="#34d399", interpret_benign_t="#a7f3d0",
        interpret_mal_bg="rgba(220,38,38,0.15)", interpret_mal_border="#dc2626",
        interpret_mal_h="#f87171", interpret_mal_t="#fca5a5",
        glossary_label="#c084fc", glossary_text="#ddd6fe",
        metric_accent="#c084fc",
    ),
}


def inject_css(th: dict) -> None:
    """Inject full-page CSS based on the active theme dictionary."""
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp {{ background:{th["bg"]}; font-family:'Inter',sans-serif; }}
section[data-testid="stSidebar"] {{ background:{th["sidebar"]}; border-right:1px solid {th["border"]}; }}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span {{ color:{th["text"]}; }}
.app-header {{ text-align:center; padding:2.5rem 1rem 1rem; }}
.app-header .icon {{ display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;background:linear-gradient(135deg,#ec4899,#7c3aed);border-radius:16px;margin-bottom:1rem; }}
.app-header .icon svg {{ width:32px;height:32px;fill:#fff; }}
.app-header h1 {{ color:{th["text"]};font-size:1.85rem;font-weight:700;margin:0 0 .35rem;letter-spacing:-.02em; }}
.app-header p {{ color:{th["text_sec"]};font-size:.95rem;margin:0; }}
section[data-testid="stSidebar"] .stNumberInput label p {{ font-size:.82rem!important;font-weight:500!important;color:{th["text"]}!important; }}
section[data-testid="stSidebar"] .stNumberInput>div>div>input {{ border-radius:8px;border:1.5px solid {th["input_border"]};font-size:.85rem;padding:.45rem .6rem;background:{th["card"]};color:{th["text"]}; }}
section[data-testid="stSidebar"] .stNumberInput>div>div>input:focus {{ border-color:#7c3aed;box-shadow:0 0 0 3px rgba(124,58,237,.2); }}
section[data-testid="stSidebar"] hr {{ border-color:{th["border"]};margin:.75rem 0; }}
.stButton>button[kind="primary"] {{ background:linear-gradient(135deg,#db2777,#7c3aed)!important;border:none!important;font-weight:600!important;font-size:.95rem!important;padding:.65rem 1.5rem!important;border-radius:10px!important;transition:transform .1s,box-shadow .15s; }}
.stButton>button[kind="primary"]:hover {{ transform:translateY(-1px);box-shadow:0 4px 16px rgba(219,39,119,.45)!important; }}
.result-panel {{ background:{th["card"]};border:1px solid {th["border"]};border-radius:16px;padding:2rem 2.5rem;text-align:center; }}
.result-label {{ font-size:.75rem;text-transform:uppercase;letter-spacing:.1em;font-weight:600;color:{th["text_muted"]};margin-bottom:.5rem; }}
.result-class {{ font-size:2rem;font-weight:700;margin:.25rem 0 1.25rem; }}
.class-benign {{ color:#059669; }} .class-malignant {{ color:#dc2626; }}
.prob-container {{ margin:1.5rem auto;max-width:380px; }}
.prob-label-row {{ display:flex;justify-content:space-between;font-size:.75rem;color:{th["text_muted"]};font-weight:500;margin-bottom:6px; }}
.prob-track {{ width:100%;height:12px;background:{th["border"]};border-radius:999px;overflow:hidden; }}
.prob-fill {{ height:100%;border-radius:999px;transition:width .6s ease; }}
.fill-benign {{ background:linear-gradient(90deg,#34d399,#059669); }}
.fill-malignant {{ background:linear-gradient(90deg,#f87171,#dc2626); }}
.prob-value {{ font-size:2.5rem;font-weight:700;margin:1rem 0 .25rem; }}
.prob-value-benign {{ color:#059669; }} .prob-value-malignant {{ color:#dc2626; }}
.prob-caption {{ font-size:.85rem;color:{th["text_sec"]}; }}
.stat-box {{ background:{th["stat_bg"]};border:1px solid {th["border"]};border-radius:10px;padding:1rem 1.25rem;text-align:center; }}
.stat-box .stat-label {{ font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:{th["text_muted"]};font-weight:600;margin-bottom:.3rem; }}
.stat-box .stat-value {{ font-size:1.35rem;font-weight:700;color:{th["text"]}; }}
.info-banner {{ background:{th["info_bg"]};border:1px solid {th["info_border"]};border-radius:10px;padding:1rem 1.25rem;display:flex;gap:.75rem;align-items:flex-start;margin-bottom:1.5rem; }}
.info-banner .info-icon {{ flex-shrink:0;width:20px;height:20px;color:#7c3aed;margin-top:1px; }}
.info-banner p {{ color:{th["info_text"]};font-size:.85rem;line-height:1.5;margin:0; }}
.interpret-card {{ border-radius:12px;padding:1.5rem 1.75rem;margin-top:1.25rem;line-height:1.6; }}
.interpret-benign {{ background:{th["interpret_benign_bg"]};border:1px solid {th["interpret_benign_border"]}; }}
.interpret-malignant {{ background:{th["interpret_mal_bg"]};border:1px solid {th["interpret_mal_border"]}; }}
.interpret-card h4 {{ margin:0 0 .5rem;font-size:1rem;font-weight:700; }}
.interpret-benign h4 {{ color:{th["interpret_benign_h"]}; }} .interpret-malignant h4 {{ color:{th["interpret_mal_h"]}; }}
.interpret-card p {{ margin:0 0 .75rem;font-size:.88rem; }}
.interpret-benign p {{ color:{th["interpret_benign_t"]}; }} .interpret-malignant p {{ color:{th["interpret_mal_t"]}; }}
.interpret-card ul {{ margin:0;padding-left:1.25rem; }}
.interpret-card li {{ font-size:.86rem;margin-bottom:.35rem; }}
.interpret-benign li {{ color:{th["interpret_benign_t"]}; }} .interpret-malignant li {{ color:{th["interpret_mal_t"]}; }}
.waiting-state {{ text-align:center;padding:3rem 2rem; }}
.waiting-state h3 {{ color:{th["text"]};font-size:1.1rem;font-weight:600;margin:0 0 .4rem; }}
.waiting-state p {{ color:{th["text_muted"]};font-size:.88rem;margin:0; }}
.dna-wave {{ display:flex;justify-content:center;gap:6px;margin-bottom:1.5rem; }}
.dna-dot {{ width:10px;height:10px;border-radius:50%;background:#db2777;animation:dna-bounce 1.4s ease-in-out infinite; }}
.dna-dot:nth-child(2){{animation-delay:.15s}} .dna-dot:nth-child(3){{animation-delay:.3s}}
.dna-dot:nth-child(4){{animation-delay:.45s}} .dna-dot:nth-child(5){{animation-delay:.6s}}
.dna-dot:nth-child(6){{animation-delay:.75s}} .dna-dot:nth-child(7){{animation-delay:.9s}}
@keyframes dna-bounce {{
  0%,100% {{ transform:translateY(0);opacity:.3; }}
  50% {{ transform:translateY(-22px);opacity:1;background:#7c3aed; }}
}}
.glossary-item {{ background:{th["card"]};border:1px solid {th["border"]};border-radius:10px;padding:1.25rem 1.5rem;margin-bottom:.75rem; }}
.glossary-item h5 {{ color:{th["text"]};font-size:.95rem;font-weight:700;margin:0 0 .4rem; }}
.glossary-item .g-desc {{ color:{th["text_sec"]};font-size:.85rem;margin:0 0 .6rem;line-height:1.5; }}
.glossary-item .g-label {{ font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{th["glossary_label"]};margin:.5rem 0 .2rem; }}
.glossary-item .g-text {{ color:{th["glossary_text"]};font-size:.83rem;margin:0;line-height:1.5; }}
.app-footer {{ text-align:center;color:{th["text_muted"]};font-size:.78rem;padding:1.5rem 1rem 1rem;line-height:1.5; }}
.sidebar-header {{ padding-bottom:.25rem; }}
.sidebar-header h3 {{ color:{th["text"]};font-size:1rem;font-weight:700;margin:0 0 .15rem; }}
.sidebar-header p {{ color:{th["text_muted"]};font-size:.8rem;margin:0; }}
.metric-card {{ background:{th["card"]};border:1px solid {th["border"]};border-radius:10px;padding:1rem;text-align:center; }}
.metric-card .mc-label {{ font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;color:{th["text_muted"]};font-weight:600; }}
.metric-card .mc-value {{ font-size:1.6rem;font-weight:700;color:{th["metric_accent"]};margin-top:.2rem; }}
#MainMenu, footer, header {{ visibility:hidden; }}
[data-testid="stMetric"] {{ display:none; }}
</style>""", unsafe_allow_html=True)
