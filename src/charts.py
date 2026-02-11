"""
Plotly chart builders for prediction visualisation.
"""

import numpy as np
import plotly.graph_objects as go

from .config import MEAN_LABELS, FULL_LABELS
from .model import W, FEAT_MEAN, FEAT_STD
from .translations import t


def _chart_layout(fig: go.Figure, th: dict) -> go.Figure:
    """Apply shared theme to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor=th["card"], plot_bgcolor=th["card"],
        font_color=th["text"], font_family="Inter, sans-serif",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="center", x=0.5),
    )
    return fig


def make_radar(patient_vals, benign_avg, malignant_avg, lang: str, th: dict):
    """Radar chart comparing patient measurements to class averages."""
    labels = MEAN_LABELS[lang]
    p = patient_vals[:10]
    b = benign_avg[:10]
    m = malignant_avg[:10]
    stk = np.vstack([p, b, m])
    lo, hi = stk.min(axis=0), stk.max(axis=0)
    rng = np.where(hi - lo == 0, 1, hi - lo)
    norm = lambda v: list((v - lo) / rng) + [float((v[0] - lo[0]) / rng[0])]
    theta = labels + [labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=norm(b), theta=theta, name=t("avg_benign", lang),
        fill="toself", fillcolor="rgba(52,211,153,0.10)",
        line=dict(color="#059669", width=2)))
    fig.add_trace(go.Scatterpolar(
        r=norm(m), theta=theta, name=t("avg_malignant", lang),
        fill="toself", fillcolor="rgba(248,113,113,0.10)",
        line=dict(color="#dc2626", width=2)))
    fig.add_trace(go.Scatterpolar(
        r=norm(p), theta=theta, name=t("patient", lang),
        fill="toself", fillcolor="rgba(99,102,241,0.15)",
        line=dict(color="#6366f1", width=3)))
    fig.update_layout(polar=dict(
        bgcolor=th["card"],
        radialaxis=dict(visible=True, range=[0, 1], showticklabels=False,
                        gridcolor=th["border"]),
        angularaxis=dict(gridcolor=th["border"]),
    ))
    return _chart_layout(fig, th)


def make_contribution(values, lang: str, th: dict):
    """Horizontal bar chart of top-10 feature contributions."""
    x = np.array(values)
    scaled = (x - FEAT_MEAN) / FEAT_STD
    contribs = scaled * W
    mal_contribs = -contribs  # positive = pushes toward malignant

    labels = FULL_LABELS[lang]
    idx = np.argsort(np.abs(mal_contribs))[::-1][:10]
    names = [labels[i] for i in idx][::-1]
    vals = [float(mal_contribs[i]) for i in idx][::-1]
    colors = ["#dc2626" if v > 0 else "#059669" for v in vals]

    fig = go.Figure(go.Bar(
        y=names, x=vals, orientation="h", marker_color=colors,
        hovertemplate="%{y}: %{x:.3f}<extra></extra>"))
    fig.update_layout(
        xaxis_title=(f"\u2190 {t('contribution_ben', lang)}    |    "
                     f"{t('contribution_mal', lang)} \u2192"),
        yaxis=dict(tickfont=dict(size=11)),
        xaxis=dict(gridcolor=th["border"], zeroline=True,
                   zerolinecolor=th["text_muted"], zerolinewidth=1),
        height=370,
    )
    return _chart_layout(fig, th)


def make_confusion(cm, lang: str, th: dict):
    """Heatmap confusion matrix."""
    labels = [t("malignant", lang), t("benign", lang)]
    fig = go.Figure(go.Heatmap(
        z=cm, x=labels, y=labels,
        text=cm, texttemplate="%{text}",
        colorscale=[[0, th["card"]], [1, "#6366f1"]],
        showscale=False, hoverinfo="skip",
    ))
    fig.update_layout(
        xaxis_title=t("predicted", lang), yaxis_title=t("actual", lang),
        yaxis=dict(autorange="reversed"),
        height=340, width=340,
    )
    return _chart_layout(fig, th)


def make_roc(fpr, tpr, roc_auc: float, th: dict):
    """ROC curve with AUC annotation."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        name=f"AUC = {roc_auc:.3f}",
        line=dict(color="#6366f1", width=2.5)))
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        name="Random",
        line=dict(color=th["text_muted"], dash="dash", width=1)))
    fig.update_layout(
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        xaxis=dict(gridcolor=th["border"]),
        yaxis=dict(gridcolor=th["border"]),
        height=340,
    )
    return _chart_layout(fig, th)
