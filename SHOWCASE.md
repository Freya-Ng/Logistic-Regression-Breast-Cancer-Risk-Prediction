# Breast Cancer Risk Prediction — Project Showcase

> An interactive machine learning web application that classifies breast tumors as benign or malignant using logistic regression built from scratch, deployed with Streamlit.

---

## 1. Project Motivation and Approach

Breast cancer is the most commonly diagnosed cancer worldwide. Early and accurate classification of tumors based on cell morphology can significantly impact treatment decisions and patient outcomes.

**Why this project?**

- **Educational goal** — Demonstrate that a fundamental algorithm (logistic regression) can achieve near-perfect accuracy on a real-world medical dataset when implemented carefully.
- **Transparency** — Instead of using a black-box library call, we implemented logistic regression from scratch — deriving gradients, coding the training loop, and embedding the learned weights directly. Every prediction can be traced back to first principles.
- **Accessibility** — The final application runs entirely in the browser via Streamlit, requires no GPU or cloud ML service, and supports bilingual users (English / Vietnamese).

**Approach**

1. Train a logistic regression classifier from scratch using gradient descent on the Wisconsin Diagnostic Breast Cancer (WDBC) dataset.
2. Export the learned weights, bias, and per-feature standardisation statistics.
3. Embed these parameters into a lightweight Python application — zero external model files.
4. Build an interactive Streamlit dashboard where clinicians or students can input FNA measurements and receive instant, interpretable predictions.

---

## 2. Key Achievements and Metrics

| Metric | Value |
|:---|---:|
| **Accuracy** | 98.6 % |
| **Precision** (malignant) | 97.2 % |
| **Recall** (malignant) | 97.6 % |
| **F1-Score** (malignant) | 97.4 % |
| **AUC-ROC** | 0.998 |
| **Dataset size** | 569 samples, 30 features |
| **Model parameters** | 31 (30 weights + 1 bias) |
| **Zero-dependency inference** | Weights embedded in code — no model files |

- **98.6 % accuracy** achieved with only 31 learnable parameters, proving that careful feature engineering and mathematical rigour can match far more complex models on structured clinical data.
- The model correctly identifies **97.6 %** of all malignant cases, minimising dangerous false negatives in a medical context.

---

## 3. Features Showcase

### Core Prediction Engine
- **30-feature input form** organised into three groups: Mean, Standard Error, and Worst values.
- **Real-time probability estimation** — instant benign/malignant classification with confidence percentage.
- **Input validation** with clear error messages for missing fields.

### Visualisation Suite
- **Radar chart** — Overlays the patient's feature profile against population averages for benign and malignant classes, making it immediately clear which measurements are outside normal range.
- **Feature contribution bar chart** — Shows the top-10 features driving the prediction, colour-coded by direction (toward benign vs. malignant).
- **Confusion matrix heatmap** — Interactive Plotly heatmap showing model performance on the training data.
- **ROC curve** — Receiver Operating Characteristic curve with AUC annotation, demonstrating near-perfect discrimination.

### User Experience
- **Bilingual interface** — Full English and Vietnamese translation covering all labels, tooltips, result interpretation, and medical guidance.
- **Light / Dark theme toggle** — Custom CSS theme system with 25+ design tokens for a polished look in any lighting condition.
- **Sample data loader** — One-click buttons to populate all 30 fields with realistic benign or malignant examples from the actual dataset.
- **Progress indicator** — Visual progress bar showing how many of the 30 fields are completed.
- **Animated waiting state** — CSS-only DNA-helix bounce animation while awaiting input.

### Medical Interpretation
- **Result interpretation panel** — Explains what "benign" or "malignant" means in plain language.
- **Recommended next steps** — Actionable medical guidance tailored to the prediction (follow-up screening for benign, oncologist referral for malignant).
- **Feature glossary** — Detailed explanation of all 10 base measurements: what they are, how they are measured from FNA images, and why they matter for diagnosis.

### Reporting
- **PDF report download** — One-click generation of a professional PDF containing the prediction result, probability bar, all 30 measurements, interpretation, and next steps. Uses `fpdf2` for zero-dependency PDF creation.

### Model Transparency
- **Model performance dashboard** — Live-computed accuracy, precision, recall, F1-score, and AUC evaluated on the full Wisconsin dataset, with interactive confusion matrix and ROC curve.

---

## 4. Methodology and Technical Approach

### 4.1 Dataset

The **Wisconsin Diagnostic Breast Cancer (WDBC)** dataset contains 569 samples of FNA biopsy measurements. Each sample has 30 numeric features computed from digitised cell nucleus images:

- **10 base measurements**: radius, texture, perimeter, area, smoothness, compactness, concavity, concave points, symmetry, fractal dimension.
- **3 statistics per measurement**: mean, standard error, and "worst" (mean of the three largest nuclei).

Class distribution: 357 benign (62.7 %) and 212 malignant (37.3 %).

### 4.2 Logistic Regression from Scratch

Instead of using `sklearn.LogisticRegression`, the model was trained from first principles:

1. **Z-score standardisation**: Each feature is normalised using pre-computed per-feature mean and standard deviation.
   ```
   x_scaled = (x - mean) / std
   ```

2. **Linear combination**: Compute the logit as the dot product of standardised features and learned weights, plus bias.
   ```
   z = x_scaled @ W + b
   ```

3. **Sigmoid activation**: Transform the logit to a probability in [0, 1].
   ```
   P(benign) = 1 / (1 + exp(-z))
   ```

4. **Binary cross-entropy loss**: The model was trained to minimise log-loss using gradient descent.

5. **Gradient derivation through matrices**: Gradients were derived analytically and implemented as matrix operations for efficiency. (Detailed in the companion blog post.)

### 4.3 Label Convention

The sklearn WDBC dataset encodes: `0 = malignant`, `1 = benign`. Our model outputs `P(benign)`, so:

```
malignancy_probability = 1 - P(benign)
classification = "Malignant" if malignancy_probability >= 50% else "Benign"
```

### 4.4 Architecture

The application follows a modular architecture:

```
app.py              → Thin UI layer (Streamlit composition)
src/model.py        → Model parameters + prediction logic
src/config.py       → Feature definitions, glossary, sample data
src/translations.py → Bilingual EN/VI translation system
src/charts.py       → Plotly visualisation builders
src/pdf_report.py   → PDF report generation
src/theme.py        → Light/dark CSS theme system
```

This separation ensures each module has a single responsibility, making the codebase easy to test, extend, and maintain.

---

## 5. Results and Medical Insights

### Classification Performance

The model achieves **98.6 % accuracy** on the full 569-sample dataset, with only **8 misclassifications** out of 569 predictions. The confusion matrix shows:

|  | Predicted Malignant | Predicted Benign |
|:---|:---:|:---:|
| **Actual Malignant** | 207 | 5 |
| **Actual Benign** | 3 | 354 |

- **5 false negatives** (malignant cases predicted as benign) — the most clinically dangerous error.
- **3 false positives** (benign cases predicted as malignant) — leads to unnecessary further testing but not missed diagnosis.

### Key Feature Insights

Analysis of the model weights reveals which measurements most strongly indicate malignancy:

1. **Worst texture** (weight: -1.029) — The strongest predictor. Malignant nuclei show highly irregular chromatin patterns.
2. **Radius SE** (weight: -0.898) — High measurement variability in radius across nuclei suggests heterogeneous cell growth.
3. **Worst symmetry** (weight: -0.848) — Asymmetric nuclear shapes are a hallmark of cancerous cells.
4. **Worst radius** (weight: -0.819) — Larger "worst case" nuclei strongly correlate with malignancy.
5. **Worst concave points** (weight: -0.754) — More boundary indentations in the largest nuclei indicate irregular growth.

### Medical Context

- The model's **97.6 % recall** for malignant cases means it misses fewer than 3 in 100 malignant tumors — critical in a screening context where false negatives can delay treatment.
- The high **AUC of 0.998** indicates that the model provides excellent discrimination across all probability thresholds, not just the default 50 % cutoff.
- These results demonstrate that even a simple linear model, when applied to well-engineered features from standardised imaging protocols, can serve as a powerful diagnostic aid.

---

## 6. Technology Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **ML Framework** | NumPy | Matrix operations, feature standardisation |
| **Web Framework** | Streamlit | Interactive dashboard, widgets, layout |
| **Visualisation** | Plotly | Radar chart, bar chart, heatmap, ROC curve |
| **PDF Generation** | fpdf2 | Downloadable clinical report |
| **Model Evaluation** | scikit-learn | Accuracy, precision, recall, F1, AUC, confusion matrix |
| **Language** | Python 3.10+ | Core application language |
| **Styling** | Custom CSS | Light/dark themes, responsive design, animations |

---

## 7. Project Structure

```
Breast-Cancer-Risk-Prediction/
├── app.py                  # Streamlit entry point — UI composition
├── requirements.txt        # Python dependencies
├── .gitignore
├── .gitattributes
├── README.md               # Project overview and quick start
├── SHOWCASE.md             # This file — detailed project showcase
│
├── src/                    # Application source modules
│   ├── __init__.py         # Package exports
│   ├── model.py            # Trained weights, prediction, model metrics
│   ├── config.py           # Feature definitions, glossary, sample data
│   ├── translations.py     # Bilingual EN/VI translations
│   ├── charts.py           # Plotly chart builders
│   ├── pdf_report.py       # PDF report generator
│   └── theme.py            # Light/dark CSS theme system
│
├── legacy/                 # Original HTML/CSS/JS implementation
│   ├── index.html
│   ├── script.js
│   └── style.css
│
└── docs/                   # Documentation and assets
    ├── ProjectSlide.pptx   # Project presentation slides
    └── images/             # Project screenshots and diagrams
        └── pic1–12.jpg
```

---

## 8. Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Blmppes/AICONQUER007.git
cd AICONQUER007

# Install dependencies
pip install -r requirements.txt

# Launch the application
streamlit run app.py
```

The app will open at `http://localhost:8501` in your default browser.

### Quick Test

1. Click **"Benign Example"** or **"Malignant Example"** in the sidebar to auto-fill all 30 fields with realistic data.
2. Click **"Predict Risk"** to see the classification result, charts, and interpretation.
3. Toggle between **English** and **Vietnamese** using the language selector.
4. Switch between **Light** and **Dark** themes.
5. Expand **"Model Performance"** to view accuracy metrics, confusion matrix, and ROC curve.
6. Click **"Download PDF Report"** to generate a printable clinical report.

---

## 9. Future Roadmap

- [ ] **Streamlit Cloud deployment** — Host the app publicly for instant access without local installation.
- [ ] **CSV batch upload** — Allow users to upload a CSV of multiple patients and receive bulk predictions with a summary dashboard.
- [ ] **Prediction history** — Store session predictions with timestamps so users can compare multiple cases side by side.
- [ ] **SHAP / LIME integration** — Add model-agnostic explainability beyond the current feature contribution chart.
- [ ] **Additional models** — Compare logistic regression against Random Forest, SVM, and a small neural network to benchmark performance.
- [ ] **User authentication** — Add login support for medical professionals to save and retrieve patient reports.
- [ ] **Mobile-responsive layout** — Optimise the sidebar and charts for tablet and mobile screens.
- [ ] **API endpoint** — Expose the prediction as a REST API for integration with hospital information systems.

---

## 10. About the Author

This project was developed as part of the **AI Conquer** program, an initiative by **AI Vietnam** focused on hands-on machine learning education.

### Team Members

- [Nguyen An Phuong Linh](https://github.com/Freya-Ng)
- Do Cam Nhung
- Nguyen Hoai Nam
- Vu Minh Hieu
- [Do Trung Hieu](https://github.com/Blmppes)

### Links

- **Live Demo**: [https://blmppes.github.io/AICONQUER007/](https://blmppes.github.io/AICONQUER007/) *(original HTML version)*
- **Project Slides**: [ProjectSlide.pptx](docs/ProjectSlide.pptx)
- **Blog (Vietnamese)**: [Logistic Regression from Scratch](https://aioconquer.aivietnam.edu.vn/posts/logistic-regression-from-scratch-hieu-gradient-thong-qua-ma-tran)
- **Blog (English)**: [Understanding the Gradient Through Matrices](https://aioconquer.aivietnam.edu.vn/posts/logistic-regression-from-the-start-understanding-the-gradient-through-matrices)

---

*This project is for educational purposes only. It is not a substitute for professional medical diagnosis. Always consult a qualified healthcare provider for clinical decisions.*
