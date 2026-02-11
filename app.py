"""
Breast Cancer Risk Prediction — Streamlit application entry point.

All heavy logic lives in the `src/` package.  This file composes the UI:
  - Sidebar: language, theme, sample loader, 30 feature inputs, predict button
  - Main area: header, prediction results / waiting state, model performance, glossary
"""

import numpy as np
import streamlit as st

from src import (
    predict_prob, compute_model_metrics,
    SECTIONS, FEATURE_ORDER, SAMPLE_BENIGN, SAMPLE_MALIGNANT, GLOSSARY,
    LANG, t,
    make_radar, make_contribution, make_confusion, make_roc,
    generate_pdf,
    THEMES, inject_css,
)

# ─── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Breast Cancer Risk Prediction",
    page_icon="\U0001f52c",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Language + theme selectors
    lc, tc = st.columns(2)
    with lc:
        lang = st.selectbox(
            "\U0001f310 Language", ["en", "vi"],
            format_func=lambda x: "English" if x == "en" else "Tieng Viet",
            key="lang",
        )
    with tc:
        theme_name = st.selectbox(
            "\U0001f3a8 " + ("Theme" if lang == "en" else "Giao Dien"),
            ["light", "dark"],
            format_func=lambda x: x.capitalize(),
            key="theme_sel",
        )

    th = THEMES[theme_name]
    inject_css(th)

    st.markdown(
        f'<div class="sidebar-header"><h3>{t("sidebar_title", lang)}</h3>'
        f'<p>{t("sidebar_subtitle", lang)}</p></div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # Sample data loader
    st.caption(t("sample_title", lang))
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button(t("sample_benign", lang), use_container_width=True):
            for key, val in zip(FEATURE_ORDER, SAMPLE_BENIGN):
                st.session_state[key] = val
            st.rerun()
    with sc2:
        if st.button(t("sample_malignant", lang), use_container_width=True):
            for key, val in zip(FEATURE_ORDER, SAMPLE_MALIGNANT):
                st.session_state[key] = val
            st.rerun()
    st.divider()

    # Feature inputs (3 sections x 10 features)
    inputs: dict[str, float] = {}
    for _sid, feat_list, sec_key, sec_desc_key in SECTIONS:
        with st.expander(f"**{t(sec_key, lang)}**  ({len(feat_list)})",
                         expanded=(_sid == "Mean")):
            st.caption(t(sec_desc_key, lang))
            c1, c2 = st.columns(2)
            for idx, (key, en_lbl, vi_lbl, en_tip, vi_tip) in enumerate(feat_list):
                lbl = en_lbl if lang == "en" else vi_lbl
                tip = en_tip if lang == "en" else vi_tip
                with c1 if idx % 2 == 0 else c2:
                    inputs[key] = st.number_input(
                        lbl, value=None, format="%.6f",
                        help=tip, key=key, placeholder="0.000000",
                    )

    # Progress indicator
    filled = sum(1 for v in inputs.values() if v is not None)
    st.progress(filled / 30, text=t("progress_text", lang, n=filled))

    st.divider()
    predict_clicked = st.button(
        t("btn_predict", lang), use_container_width=True, type="primary",
    )

# ═════════════════════════════════════════════════════════════════════════════
#  MAIN AREA
# ═════════════════════════════════════════════════════════════════════════════

# Header
st.markdown(
    '<div class="app-header"><div class="icon">'
    '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 '
    '0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2'
    'c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg></div>'
    f'<h1>{t("app_title", lang)}</h1><p>{t("app_subtitle", lang)}</p></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="info-banner"><svg class="info-icon" viewBox="0 0 20 20" fill="currentColor">'
    '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 '
    '0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 '
    '0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clip-rule="evenodd"/></svg>'
    f'<p>{t("info_banner", lang)}</p></div>',
    unsafe_allow_html=True,
)

# ─── Prediction / Waiting ────────────────────────────────────────────────────

metrics = compute_model_metrics()

if predict_clicked:
    # Validate all fields are filled
    missing = []
    for _sid, fl, _sk, _sdk in SECTIONS:
        for key, en_lbl, vi_lbl, *_ in fl:
            if inputs.get(key) is None:
                missing.append(en_lbl if lang == "en" else vi_lbl)
    if missing:
        msg = t("error_missing", lang, n=len(missing))
        fields = ", ".join(missing[:6])
        detail = t("error_missing_list", lang, fields=fields)
        if len(missing) > 6:
            detail += t("error_and_more", lang, n=len(missing) - 6)
        st.error(f"**{msg}** {detail}")
    else:
        values = [float(inputs[key]) for key in FEATURE_ORDER]
        p_benign = predict_prob(values)
        mal_pct = (1 - p_benign) * 100
        is_malignant = mal_pct >= 50

        cls_name = t("malignant", lang) if is_malignant else t("benign", lang)
        cls_css = "malignant" if is_malignant else "benign"

        # Result panel
        st.markdown(
            f'<div class="result-panel"><div class="result-label">{t("result_title", lang)}</div>'
            f'<div class="result-class class-{cls_css}">{"&#9888;&#65039;" if is_malignant else "&#10004;&#65039;"} {cls_name}</div>'
            f'<div class="prob-container"><div class="prob-label-row"><span>{t("benign", lang)}</span><span>{t("malignant", lang)}</span></div>'
            f'<div class="prob-track"><div class="prob-fill fill-{cls_css}" style="width:{mal_pct:.1f}%"></div></div></div>'
            f'<div class="prob-value prob-value-{cls_css}">{mal_pct:.2f}%</div>'
            f'<div class="prob-caption">{t("prob_caption", lang)}</div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("")

        # Stat boxes
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f'<div class="stat-box"><div class="stat-label">{t("stat_classification", lang)}</div>'
                f'<div class="stat-value">{cls_name}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div class="stat-box"><div class="stat-label">{t("stat_malignancy", lang)}</div>'
                f'<div class="stat-value">{mal_pct:.2f}%</div></div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div class="stat-box"><div class="stat-label">{t("stat_benign", lang)}</div>'
                f'<div class="stat-value">{100 - mal_pct:.2f}%</div></div>',
                unsafe_allow_html=True,
            )

        # Charts
        st.markdown("")
        ch1, ch2 = st.columns(2)
        with ch1:
            st.subheader(t("radar_title", lang))
            fig_radar = make_radar(
                np.array(values), metrics["benign_avg"],
                metrics["malignant_avg"], lang, th,
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        with ch2:
            st.subheader(t("contribution_title", lang))
            fig_contrib = make_contribution(values, lang, th)
            st.plotly_chart(fig_contrib, use_container_width=True)

        # Interpretation
        ikey = "interpret_malignant" if is_malignant else "interpret_benign"
        skey = "next_steps_malignant" if is_malignant else "next_steps_benign"
        steps_html = "".join(f"<li>{s}</li>" for s in LANG[skey][lang])
        st.markdown(
            f'<div class="interpret-card interpret-{cls_css}">'
            f'<h4>{t("interpret_title", lang)}</h4><p>{t(ikey, lang)}</p>'
            f'<h4>{t("next_steps_title", lang)}</h4><ul>{steps_html}</ul></div>',
            unsafe_allow_html=True,
        )

        # PDF download
        st.markdown("")
        pdf_bytes = generate_pdf(lang, inputs, cls_name, mal_pct)
        st.download_button(
            label=f"\U0001f4c4 {t('pdf_download', lang)}",
            data=pdf_bytes,
            file_name="breast_cancer_prediction_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

else:
    # Animated waiting state
    st.markdown(
        '<div class="waiting-state">'
        '<div class="dna-wave">'
        '<div class="dna-dot"></div><div class="dna-dot"></div><div class="dna-dot"></div>'
        '<div class="dna-dot"></div><div class="dna-dot"></div><div class="dna-dot"></div>'
        '<div class="dna-dot"></div></div>'
        f'<h3>{t("waiting_title", lang)}</h3>'
        f'<p>{t("waiting_text", lang)}</p></div>',
        unsafe_allow_html=True,
    )

# ═════════════════════════════════════════════════════════════════════════════
#  MODEL PERFORMANCE SECTION
# ═════════════════════════════════════════════════════════════════════════════

st.divider()
with st.expander(
    f"\U0001f4ca {t('model_perf_title', lang)} \u2014 {t('model_perf_desc', lang)}"
):
    m1, m2, m3, m4, m5 = st.columns(5)
    for col, label, val in [
        (m1, "Accuracy",  metrics["accuracy"]),
        (m2, "Precision", metrics["precision"]),
        (m3, "Recall",    metrics["recall"]),
        (m4, "F1-Score",  metrics["f1"]),
        (m5, "AUC",       metrics["roc_auc"]),
    ]:
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="mc-label">{label}</div>'
                f'<div class="mc-value">{val:.3f}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("")
    cm1, cm2 = st.columns(2)
    with cm1:
        st.subheader(t("confusion_matrix", lang))
        st.plotly_chart(make_confusion(metrics["cm"], lang, th),
                        use_container_width=True)
    with cm2:
        st.subheader(t("roc_curve", lang))
        st.plotly_chart(
            make_roc(metrics["fpr"], metrics["tpr"], metrics["roc_auc"], th),
            use_container_width=True,
        )

# ═════════════════════════════════════════════════════════════════════════════
#  FEATURE GLOSSARY
# ═════════════════════════════════════════════════════════════════════════════

st.divider()
with st.expander(
    f"\U0001f4d6 {t('glossary_title', lang)} \u2014 {t('glossary_subtitle', lang)}"
):
    st.markdown(t("glossary_variants_text", lang))
    st.markdown("")
    for item in GLOSSARY:
        st.markdown(
            f'<div class="glossary-item"><h5>{item["name"][lang]}</h5>'
            f'<p class="g-desc">{item["desc"][lang]}</p>'
            f'<div class="g-label">{t("glossary_how", lang)}</div>'
            f'<p class="g-text">{item["how"][lang]}</p>'
            f'<div class="g-label">{t("glossary_why", lang)}</div>'
            f'<p class="g-text">{item["why"][lang]}</p></div>',
            unsafe_allow_html=True,
        )

# Footer
st.markdown(
    f'<div class="app-footer">{t("disclaimer", lang)}</div>',
    unsafe_allow_html=True,
)
