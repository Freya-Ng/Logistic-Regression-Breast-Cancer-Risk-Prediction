/***********************
 * MODEL PARAMETERS
 ***********************/

// ⚠️ Replace these with YOUR trained values from Python
// w shape: (30,)
const W = [
  -0.5389699731743985, -0.6434330617896211, -0.5174582015672622, -0.5770918729105026, -0.2008837293724098, 0.1789416511927587, -0.6330460231705183, -0.7811099571940602, 0.030956916449250783, 0.29941691085377464, -0.8980222254853673, 0.0585137030636357, -0.6163295474882419, -0.6953746065699656, -0.17861237266070726, 0.5966244425141785, 0.07464162683808573, -0.1349711696127181, 0.3070665545532483, 0.5311932217459552, -0.8192697259096365, -1.0289293339678638, -0.7069306940664978, -0.7941580589413779, -0.6927809984196284, -0.13324953592635932, -0.7214969938484923, -0.7540139817698556, -0.8482017996838813, -0.13518883825108646
];

// bias
const B = 0.5602710363570669;

// StandardScaler parameters
const MEAN = [
  14.117635164835171, 19.18503296703298, 91.88224175824185, 654.3775824175825, 0.09574402197802204, 0.10361931868131863, 0.08889814505494498, 0.04827987032967031, 0.18109868131868148, 0.06275676923076925, 0.40201582417582393, 1.2026868131868136, 2.858253406593405, 40.0712989010989, 0.00698907472527473, 0.025635448351648396, 0.0328236723076923, 0.011893940659340657, 0.020573512087912114, 0.003820455604395603, 16.23510329670329, 25.535692307692308, 107.10312087912091, 876.9870329670341, 0.13153213186813184, 0.2527418021978023, 0.27459456923076936, 0.11418222197802197, 0.29050219780219777, 0.0838678461538462
];

const STD = [
  3.5319276091287684, 4.261314035201523, 24.29528446596607, 354.5529252060648, 0.013907698124434402, 0.052412805496132024, 0.07938050908411763, 0.038018354057687886, 0.027457084964442154, 0.0072017850581413915, 0.2828495575198162, 0.5411516758817481, 2.068931392290445, 47.18438200914984, 0.003053473706769491, 0.01858629695791424, 0.032110245434099904, 0.006287187209688091, 0.008162966415892984, 0.0027840687418581585, 4.805977154451531, 6.058439641882756, 33.33796863783808, 567.0486811155924, 0.02305712569565531, 0.15484384737160206, 0.20916786137677873, 0.06525425828147159, 0.06308179580673515, 0.017828276003334045
];

// Feature order MUST match training
const FEATURE_NAMES = [
  "mean_radius", "mean_texture", "mean_perimeter", "mean_area",
  "mean_smoothness", "mean_compactness", "mean_concavity",
  "mean_concave_points", "mean_symmetry", "mean_fractal_dimension",
  "radius_error", "texture_error", "perimeter_error", "area_error",
  "smoothness_error", "compactness_error", "concavity_error",
  "concave_points_error", "symmetry_error", "fractal_dimension_error",
  "worst_radius", "worst_texture", "worst_perimeter", "worst_area",
  "worst_smoothness", "worst_compactness", "worst_concavity",
  "worst_concave_points", "worst_symmetry", "worst_fractal_dimension"
];

/***********************
 * MATH
 ***********************/
function sigmoid(z) {
  return 1 / (1 + Math.exp(-z));
}

function dot(a, b) {
  return a.reduce((sum, ai, i) => sum + ai * b[i], 0);
}

function standardize(x) {
  return x.map((xi, i) => (xi - MEAN[i]) / STD[i]);
}

/***********************
 * UI HANDLER
 ***********************/
document.getElementById("predict-form").addEventListener("submit", (e) => {
  e.preventDefault();

  const x = FEATURE_NAMES.map(name => {
    const el = document.querySelector(`[name="${name}"]`);
    return Number(el.value);
  });

  const xScaled = standardize(x);
  const z = dot(xScaled, W) + B;
  const p = sigmoid(z);

  document.getElementById("result").innerHTML = `
    <div class="card">
      <h2>${p >= 0.5 ? "⚠️ Malignant" : "✅ Benign"}</h2>
      <p><b>Probability (Cancer):</b> ${(p * 100).toFixed(2)}%</p>
    </div>
  `;
});
