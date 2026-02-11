"""
Feature definitions, glossary data, and sample inputs.
"""

# ── Feature definitions ──────────────────────────────────────────────────────
# (key, en_label, vi_label, en_tooltip, vi_tooltip)

FEATURES_RAW = [
    ("mean_radius",            "Radius",       "Ban Kinh",      "Average distance from center to boundary",   "Khoang cach trung binh tu tam den ranh gioi"),
    ("mean_texture",           "Texture",      "Ket Cau",       "Std deviation of gray-scale values",         "Do lech chuan cua gia tri thang xam"),
    ("mean_perimeter",         "Perimeter",    "Chu Vi",        "Mean perimeter of the nucleus",              "Chu vi trung binh cua nhan te bao"),
    ("mean_area",              "Area",         "Dien Tich",     "Mean area of the nucleus",                   "Dien tich trung binh cua nhan te bao"),
    ("mean_smoothness",        "Smoothness",   "Do Min",        "Local variation in radius lengths",          "Bien dong cuc bo cua do dai ban kinh"),
    ("mean_compactness",       "Compactness",  "Do Chat",       "Perimeter\u00b2 / Area \u2212 1",           "Chu vi\u00b2 / Dien tich \u2212 1"),
    ("mean_concavity",         "Concavity",    "Do Lom",        "Severity of concave contour portions",       "Muc do lom cua duong vien"),
    ("mean_concave_points",    "Concave Pts",  "Diem Lom",      "Number of concave contour portions",         "So luong phan lom cua duong vien"),
    ("mean_symmetry",          "Symmetry",     "Doi Xung",      "Symmetry of the nucleus shape",              "Do doi xung cua hinh dang nhan"),
    ("mean_fractal_dimension", "Fractal Dim",  "Chieu Fractal", "Boundary complexity (coastline approx.)",    "Do phuc tap duong vien"),
    ("radius_error",            "Radius",      "Ban Kinh",      "Standard error of radius",                   "Sai so chuan cua ban kinh"),
    ("texture_error",           "Texture",     "Ket Cau",       "Standard error of texture",                  "Sai so chuan cua ket cau"),
    ("perimeter_error",         "Perimeter",   "Chu Vi",        "Standard error of perimeter",                "Sai so chuan cua chu vi"),
    ("area_error",              "Area",        "Dien Tich",     "Standard error of area",                     "Sai so chuan cua dien tich"),
    ("smoothness_error",        "Smoothness",  "Do Min",        "Standard error of smoothness",               "Sai so chuan cua do min"),
    ("compactness_error",       "Compactness", "Do Chat",       "Standard error of compactness",              "Sai so chuan cua do chat"),
    ("concavity_error",         "Concavity",   "Do Lom",        "Standard error of concavity",                "Sai so chuan cua do lom"),
    ("concave_points_error",    "Concave Pts", "Diem Lom",      "Standard error of concave points",           "Sai so chuan cua diem lom"),
    ("symmetry_error",          "Symmetry",    "Doi Xung",      "Standard error of symmetry",                 "Sai so chuan cua doi xung"),
    ("fractal_dimension_error", "Fractal Dim", "Chieu Fractal", "Standard error of fractal dimension",        "Sai so chuan cua chieu fractal"),
    ("worst_radius",            "Radius",      "Ban Kinh",      "Largest radius (mean of 3 largest)",         "Ban kinh lon nhat (TB 3 gia tri lon nhat)"),
    ("worst_texture",           "Texture",     "Ket Cau",       "Largest texture value",                      "Gia tri ket cau lon nhat"),
    ("worst_perimeter",         "Perimeter",   "Chu Vi",        "Largest perimeter value",                    "Gia tri chu vi lon nhat"),
    ("worst_area",              "Area",        "Dien Tich",     "Largest area value",                         "Gia tri dien tich lon nhat"),
    ("worst_smoothness",        "Smoothness",  "Do Min",        "Largest smoothness value",                   "Gia tri do min lon nhat"),
    ("worst_compactness",       "Compactness", "Do Chat",       "Largest compactness value",                  "Gia tri do chat lon nhat"),
    ("worst_concavity",         "Concavity",   "Do Lom",        "Largest concavity value",                    "Gia tri do lom lon nhat"),
    ("worst_concave_points",    "Concave Pts", "Diem Lom",      "Largest concave points value",               "Gia tri diem lom lon nhat"),
    ("worst_symmetry",          "Symmetry",    "Doi Xung",      "Largest symmetry value",                     "Gia tri doi xung lon nhat"),
    ("worst_fractal_dimension", "Fractal Dim", "Chieu Fractal", "Largest fractal dimension value",            "Gia tri chieu fractal lon nhat"),
]

SECTIONS = [
    ("Mean",      FEATURES_RAW[0:10],  "sec_mean",  "sec_mean_desc"),
    ("Std Error", FEATURES_RAW[10:20], "sec_se",    "sec_se_desc"),
    ("Worst",     FEATURES_RAW[20:30], "sec_worst", "sec_worst_desc"),
]

FEATURE_ORDER = [row[0] for row in FEATURES_RAW]

MEAN_LABELS = {
    "en": ["Radius", "Texture", "Perimeter", "Area", "Smoothness",
            "Compactness", "Concavity", "Concave Pts", "Symmetry", "Fractal Dim"],
    "vi": ["Ban Kinh", "Ket Cau", "Chu Vi", "Dien Tich", "Do Min",
            "Do Chat", "Do Lom", "Diem Lom", "Doi Xung", "Chieu Fractal"],
}

FULL_LABELS = {
    "en": [f"Mean {n}" for n in MEAN_LABELS["en"]]
         + [f"{n} SE" for n in MEAN_LABELS["en"]]
         + [f"Worst {n}" for n in MEAN_LABELS["en"]],
    "vi": [f"TB {n}" for n in MEAN_LABELS["vi"]]
         + [f"SC {n}" for n in MEAN_LABELS["vi"]]
         + [f"LN {n}" for n in MEAN_LABELS["vi"]],
}

# ── Glossary ─────────────────────────────────────────────────────────────────

GLOSSARY = [
    {"name": {"en": "Radius", "vi": "Ban Kinh"},
     "desc": {"en": "Mean distance from the center of the cell nucleus to its perimeter.", "vi": "Khoang cach trung binh tu tam nhan te bao den chu vi."},
     "how":  {"en": "Software identifies each nucleus boundary in the FNA image and averages distances from centroid to boundary points.", "vi": "Phan mem xac dinh ranh gioi nhan te bao trong hinh FNA va tinh trung binh khoang cach tu tam den cac diem tren ranh gioi."},
     "why":  {"en": "Malignant cells tend to be larger -- higher radius may indicate malignancy.", "vi": "Te bao ac tinh thuong lon hon -- ban kinh lon hon co the chi ra tinh ac tinh."}},
    {"name": {"en": "Texture", "vi": "Ket Cau"},
     "desc": {"en": "Standard deviation of gray-scale pixel values within the nucleus.", "vi": "Do lech chuan cua gia tri pixel thang xam trong nhan te bao."},
     "how":  {"en": "Gray-scale values of all pixels inside the nucleus boundary are collected; their standard deviation measures texture variation.", "vi": "Thu thap gia tri thang xam cua tat ca diem anh trong ranh gioi nhan; do lech chuan do luong bien dong ket cau."},
     "why":  {"en": "Malignant nuclei often have irregular chromatin patterns producing higher texture.", "vi": "Nhan ac tinh thuong co cau truc chromatin khong deu, tao gia tri ket cau cao hon."}},
    {"name": {"en": "Perimeter", "vi": "Chu Vi"},
     "desc": {"en": "Total length of the nucleus boundary.", "vi": "Tong chieu dai duong vien nhan te bao."},
     "how":  {"en": "The software traces the detected boundary and sums pixel distances.", "vi": "Phan mem truy vet duong vien va cong cac khoang cach pixel."},
     "why":  {"en": "Larger and more irregular nuclei have longer perimeters.", "vi": "Nhan lon hon va bat thuong hon co chu vi dai hon."}},
    {"name": {"en": "Area", "vi": "Dien Tich"},
     "desc": {"en": "Total area enclosed within the nucleus boundary.", "vi": "Tong dien tich nam trong ranh gioi nhan te bao."},
     "how":  {"en": "Count of all pixels inside the detected boundary.", "vi": "Dem tat ca diem anh nam trong ranh gioi phat hien duoc."},
     "why":  {"en": "Cancer cells typically have larger nuclei -- increased area is a strong malignancy indicator.", "vi": "Te bao ung thu thuong co nhan lon hon -- dien tich tang la chi bao manh cua tinh ac tinh."}},
    {"name": {"en": "Smoothness", "vi": "Do Min"},
     "desc": {"en": "Local variation in radius lengths of the boundary.", "vi": "Bien dong cuc bo cua do dai ban kinh tren duong vien."},
     "how":  {"en": "Difference between local radius and mean radius of neighbors, averaged across the boundary.", "vi": "Chenh lech giua ban kinh cuc bo va ban kinh trung binh cac diem lan can, lay trung binh tren duong vien."},
     "why":  {"en": "Rough, irregular boundaries are more common in malignant tumors.", "vi": "Duong vien gho ghe, khong deu pho bien hon o khoi u ac tinh."}},
    {"name": {"en": "Compactness", "vi": "Do Chat"},
     "desc": {"en": "Calculated as (perimeter\u00b2 / area) \u2212 1. Measures shape regularity.", "vi": "Tinh bang (chu vi\u00b2 / dien tich) \u2212 1. Do luong do deu cua hinh dang."},
     "how":  {"en": "Derived from perimeter and area. A perfect circle has the lowest value.", "vi": "Tinh tu chu vi va dien tich. Hinh tron hoan hao co gia tri thap nhat."},
     "why":  {"en": "Malignant nuclei are more irregularly shaped, producing higher compactness.", "vi": "Nhan ac tinh co hinh dang bat thuong hon, tao gia tri do chat cao hon."}},
    {"name": {"en": "Concavity", "vi": "Do Lom"},
     "desc": {"en": "Severity (depth) of concave portions of the boundary.", "vi": "Muc do (do sau) cua cac phan lom tren duong vien."},
     "how":  {"en": "Boundary analyzed for concave segments; depth of each indentation is measured and averaged.", "vi": "Duong vien duoc phan tich de tim cac doan lom; do sau moi cho lom duoc do va lay trung binh."},
     "why":  {"en": "Deep indentations are a hallmark of irregular, malignant cell growth.", "vi": "Cac cho lom sau la dau hieu dac trung cua su phat trien te bao ac tinh."}},
    {"name": {"en": "Concave Points", "vi": "Diem Lom"},
     "desc": {"en": "Number of concave (indentation) points on the boundary.", "vi": "So luong diem lom tren duong vien."},
     "how":  {"en": "Each point where the contour curves inward is counted.", "vi": "Moi diem noi duong vien cong vao trong duoc dem."},
     "why":  {"en": "More concave points = more irregular boundary. One of the model's most important features.", "vi": "Nhieu diem lom hon = duong vien bat thuong hon. Mot trong nhung chi so quan trong nhat."}},
    {"name": {"en": "Symmetry", "vi": "Doi Xung"},
     "desc": {"en": "Symmetry of the nucleus along its longest axis.", "vi": "Do doi xung cua nhan theo truc dai nhat."},
     "how":  {"en": "Nucleus is reflected along its major axis; difference between opposite sides is averaged.", "vi": "Nhan duoc phan chieu doc truc chinh; chenh lech giua hai ben duoc lay trung binh."},
     "why":  {"en": "Malignant cells tend to grow asymmetrically.", "vi": "Te bao ac tinh co xu huong phat trien khong doi xung."}},
    {"name": {"en": "Fractal Dimension", "vi": "Chieu Fractal"},
     "desc": {"en": "Boundary complexity via the \"coastline approximation\" method.", "vi": "Do phuc tap duong vien bang phuong phap \"xap xi duong bo bien\"."},
     "how":  {"en": "Boundary measured at progressively finer scales; the rate of length increase gives the fractal dimension.", "vi": "Duong vien do o cac ty le nho dan; ty le tang chieu dai cho ra chieu fractal."},
     "why":  {"en": "Higher fractal dimension = more complex boundary, typical of malignant nuclei.", "vi": "Chieu fractal cao hon = duong vien phuc tap hon, dac trung cua nhan ac tinh."}},
]

# ── Sample data (realistic values from the Wisconsin dataset) ────────────────

SAMPLE_BENIGN = [
    12.25, 17.94, 78.27, 462.0, 0.0869, 0.0678, 0.029, 0.0149, 0.172, 0.0596,
    0.236, 0.866, 1.68, 19.54, 0.0054, 0.0137, 0.0186, 0.0072, 0.0163, 0.0025,
    13.5, 22.46, 86.92, 562.1, 0.119, 0.142, 0.093, 0.044, 0.247, 0.071,
]

SAMPLE_MALIGNANT = [
    19.81, 22.15, 130.0, 1260.0, 0.0984, 0.159, 0.1974, 0.1049, 0.19, 0.061,
    0.746, 1.153, 5.439, 94.44, 0.0061, 0.0349, 0.056, 0.0179, 0.0225, 0.0043,
    25.67, 29.33, 170.1, 2027.0, 0.145, 0.4504, 0.5187, 0.2154, 0.369, 0.1048,
]
