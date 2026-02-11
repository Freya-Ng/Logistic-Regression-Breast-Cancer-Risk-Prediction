"""
Logistic regression model parameters and prediction logic.

The model was trained from scratch on the Wisconsin Diagnostic Breast Cancer
dataset (569 samples, 30 features).  Weights, bias, and standardisation
statistics are embedded so the app has zero external model files.
"""

import math
import numpy as np
import streamlit as st
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc,
)

# ── Trained weights (30 features) ────────────────────────────────────────────

W = np.array([
    -0.5389699731743985, -0.6434330617896211, -0.5174582015672622,
    -0.5770918729105026, -0.2008837293724098,  0.1789416511927587,
    -0.6330460231705183, -0.7811099571940602,  0.030956916449250783,
     0.29941691085377464, -0.8980222254853673,  0.0585137030636357,
    -0.6163295474882419, -0.6953746065699656, -0.17861237266070726,
     0.5966244425141785,  0.07464162683808573, -0.1349711696127181,
     0.3070665545532483,  0.5311932217459552, -0.8192697259096365,
    -1.0289293339678638, -0.7069306940664978, -0.7941580589413779,
    -0.6927809984196284, -0.13324953592635932, -0.7214969938484923,
    -0.7540139817698556, -0.8482017996838813, -0.13518883825108646,
])

BIAS = 0.5602710363570669

# ── Standardisation parameters (per-feature mean & std from training) ────────

FEAT_MEAN = np.array([
    14.117635164835171, 19.18503296703298, 91.88224175824185,
    654.3775824175825, 0.09574402197802204, 0.10361931868131863,
    0.08889814505494498, 0.04827987032967031, 0.18109868131868148,
    0.06275676923076925, 0.40201582417582393, 1.2026868131868136,
    2.858253406593405, 40.0712989010989, 0.00698907472527473,
    0.025635448351648396, 0.0328236723076923, 0.011893940659340657,
    0.020573512087912114, 0.003820455604395603, 16.23510329670329,
    25.535692307692308, 107.10312087912091, 876.9870329670341,
    0.13153213186813184, 0.2527418021978023, 0.27459456923076936,
    0.11418222197802197, 0.29050219780219777, 0.0838678461538462,
])

FEAT_STD = np.array([
    3.5319276091287684, 4.261314035201523, 24.29528446596607,
    354.5529252060648, 0.013907698124434402, 0.052412805496132024,
    0.07938050908411763, 0.038018354057687886, 0.027457084964442154,
    0.0072017850581413915, 0.2828495575198162, 0.5411516758817481,
    2.068931392290445, 47.18438200914984, 0.003053473706769491,
    0.01858629695791424, 0.032110245434099904, 0.006287187209688091,
    0.008162966415892984, 0.0027840687418581585, 4.805977154451531,
    6.058439641882756, 33.33796863783808, 567.0486811155924,
    0.02305712569565531, 0.15484384737160206, 0.20916786137677873,
    0.06525425828147159, 0.06308179580673515, 0.017828276003334045,
])


# ── Prediction ───────────────────────────────────────────────────────────────

def predict_prob(values: list[float]) -> float:
    """Return P(benign).  The model outputs high probability for the benign class."""
    x = np.array(values)
    z = float(((x - FEAT_MEAN) / FEAT_STD) @ W + BIAS)
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    ez = math.exp(z)
    return ez / (1.0 + ez)


# ── Cached evaluation on the full dataset ────────────────────────────────────

@st.cache_data
def compute_model_metrics() -> dict:
    """Compute accuracy, precision, recall, F1, AUC, confusion matrix, ROC
    curve, and per-class average feature profiles."""
    data = load_breast_cancer()
    X, y = data.data, data.target          # y: 0=malignant, 1=benign

    X_scaled = (X - FEAT_MEAN) / FEAT_STD
    z = X_scaled @ W + BIAS
    probs = 1 / (1 + np.exp(-z))            # P(benign)
    y_pred = (probs >= 0.5).astype(int)

    acc  = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred, pos_label=0, zero_division=0)
    rec  = recall_score(y, y_pred, pos_label=0, zero_division=0)
    f1   = f1_score(y, y_pred, pos_label=0, zero_division=0)
    cm   = confusion_matrix(y, y_pred, labels=[0, 1])

    mal_prob = 1 - probs
    fpr, tpr, _ = roc_curve(y, mal_prob, pos_label=0)
    roc_auc = auc(fpr, tpr)

    benign_avg    = X[y == 1].mean(axis=0)
    malignant_avg = X[y == 0].mean(axis=0)

    return dict(
        accuracy=acc, precision=prec, recall=rec, f1=f1, cm=cm,
        fpr=fpr, tpr=tpr, roc_auc=roc_auc,
        benign_avg=benign_avg, malignant_avg=malignant_avg,
    )
