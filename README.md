# Breast Cancer Risk Prediction

A machine learning web application that predicts breast cancer risk from tumor cell measurements using **logistic regression implemented from scratch**. Built with Streamlit and achieving **98.6% accuracy** on the Wisconsin Diagnostic Breast Cancer dataset.

Part of the **AI Conquer** program by **AI Vietnam**.

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser. Use the **"Benign Example"** / **"Malignant Example"** buttons to quickly test with realistic data.

---

## Features

- **30-feature prediction** — Input FNA biopsy measurements, get instant benign/malignant classification
- **Interactive charts** — Radar chart, feature contribution bar chart, confusion matrix, ROC curve
- **Bilingual** — Full English and Vietnamese support
- **Light / Dark theme** — Toggle between themes
- **PDF report** — Download a printable prediction report
- **Model transparency** — View accuracy, precision, recall, F1, AUC with live-computed metrics
- **Feature glossary** — Detailed explanation of each measurement
- **Sample data loader** — One-click auto-fill with realistic examples

---

## Model Performance

| Metric | Value |
|:---|---:|
| Accuracy | 98.6% |
| Precision | 97.2% |
| Recall | 97.6% |
| F1-Score | 97.4% |
| AUC | 0.998 |

Trained from scratch using gradient descent — no `sklearn.LogisticRegression`. Weights and standardisation parameters are embedded directly in the code (31 parameters total).

---

## Project Structure

```
├── app.py                  # Streamlit entry point
├── requirements.txt        # Dependencies
├── SHOWCASE.md             # Detailed project showcase
├── src/                    # Application modules
│   ├── model.py            # Weights, prediction, metrics
│   ├── config.py           # Feature definitions, glossary
│   ├── translations.py     # EN/VI translations
│   ├── charts.py           # Plotly chart builders
│   ├── pdf_report.py       # PDF generation
│   └── theme.py            # CSS theme system
├── legacy/                 # Original HTML/JS/CSS version
│   ├── index.html
│   ├── script.js
│   └── style.css
└── docs/                   # Slides and images
    ├── ProjectSlide.pptx
    └── images/
```

---

## How It Works

1. **Input** — Enter 30 tumor measurements from FNA biopsy (mean, std error, worst for 10 base features)
2. **Standardise** — Z-score normalisation with pre-computed mean and standard deviation
3. **Predict** — Linear combination with trained weights, sigmoid activation
4. **Classify** — `P(malignant) >= 50%` = malignant, otherwise benign

---

## Technology Stack

| | |
|:---|:---|
| Python | Core language |
| Streamlit | Web framework |
| NumPy | Numerical computation |
| Plotly | Interactive charts |
| scikit-learn | Model evaluation metrics |
| fpdf2 | PDF report generation |

---

## Links

- **Detailed Showcase**: [SHOWCASE.md](SHOWCASE.md)
- **Live Demo (legacy)**: [blmppes.github.io/AICONQUER007](https://blmppes.github.io/AICONQUER007/)
- **Blog (VN)**: [Logistic Regression from Scratch](https://aioconquer.aivietnam.edu.vn/posts/logistic-regression-from-scratch-hieu-gradient-thong-qua-ma-tran)
- **Blog (EN)**: [Understanding the Gradient Through Matrices](https://aioconquer.aivietnam.edu.vn/posts/logistic-regression-from-the-start-understanding-the-gradient-through-matrices)

## Team

- [Nguyen An Phuong Linh](https://github.com/Freya-Ng) · Do Cam Nhung · Nguyen Hoai Nam · Vu Minh Hieu · [Do Trung Hieu](https://github.com/Blmppes)

---

*Educational project — not a substitute for professional medical diagnosis.*
