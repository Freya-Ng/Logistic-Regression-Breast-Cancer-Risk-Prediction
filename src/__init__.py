"""
src package — modular components for the Breast Cancer Risk Prediction app.
"""

from .model import predict_prob, compute_model_metrics, W, FEAT_MEAN, FEAT_STD
from .config import (
    FEATURES_RAW, SECTIONS, FEATURE_ORDER, MEAN_LABELS, FULL_LABELS,
    GLOSSARY, SAMPLE_BENIGN, SAMPLE_MALIGNANT,
)
from .translations import LANG, t
from .charts import make_radar, make_contribution, make_confusion, make_roc
from .pdf_report import generate_pdf
from .theme import THEMES, inject_css

__all__ = [
    "predict_prob", "compute_model_metrics", "W", "FEAT_MEAN", "FEAT_STD",
    "FEATURES_RAW", "SECTIONS", "FEATURE_ORDER", "MEAN_LABELS", "FULL_LABELS",
    "GLOSSARY", "SAMPLE_BENIGN", "SAMPLE_MALIGNANT",
    "LANG", "t",
    "make_radar", "make_contribution", "make_confusion", "make_roc",
    "generate_pdf",
    "THEMES", "inject_css",
]
