import streamlit as st

# 1. Page Setup
st.set_page_config(page_title="PUTRA Forest Health", page_icon="🌳", layout="wide")
st.title("🌲 PUTRA Forest Health Prediction System")
st.markdown("##### Agricultural and Biosystems Engineering (UPM)")
st.divider()

# 2. Inputs
c1, c2, c3 = st.columns(3)
with c1:
    f_target = st.selectbox("1. Select Fungal Target", 
                            ["Shannon Index (H')", "Species Richness (S)", "Simpson Index (1-D)", "Pielou's Evenness (J')"])
with c2:
    v_index = st.selectbox("2. Select Vegetation Index (VI)", ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"])
with c3:
    val = st.number_input(f"3. Enter observed {v_index} Value", value=0.750, format="%.3f")

# 3. Engineering Data (Standardized coefficients from your PDF)
models = {
    "NDRE": [0.0632, 0.584], "CIRE": [1.15, 2.82], "NDVI": [0.0347, 0.818],
    "VARI": [0.0611, 0.252], "MSAVI": [0.0181, 0.9], "SAVI": [0.044, 1.23], "GNDVI": [0.0242, 0.77]
}

# Reference Baselines for Classification Logic
thresholds = {
    "Shannon Index (H')": {"Pristine": 3.483, "Stable": 3.389, "Disturbed": 3.123},
    "Species Richness (S)": {"Pristine": 76.0, "Stable": 54.0, "Disturbed": 45.0},
    "Simpson Index (1-D)": {"Pristine": 0.955, "Stable": 0.952, "Disturbed": 0.936},
    "Pielou's Evenness (J')": {"Pristine": 0.804, "Stable": 0.849, "Disturbed": 0.820}
}

# 4. Calculation
m, c = models[v_index]
# Algebra: y = mx + c  =>  x = (y - c) / m
prediction = (val - c) / m

# 5. Dashboard Results
st.divider()
st.write(f"### 📊 Prediction Results")

# Display Dynamic Regression Equation
st.info(f"**Current Regression Model:** $y = {m}x + {c}$  \n*(where $y$ = {v_index} and $x$ = {f_target})*")

res1, res2, res3 = st.columns(3)

with res1:
    st.metric(f"Predicted {f_target}", f"{prediction:.3f}")

with res2:
    r2_map = {"NDRE": "99.0%", "CIRE": "91.8%", "NDVI": "86.2%", "VARI": "84.7%", "MSAVI": "67.4%", "SAVI": "61.6%", "GNDVI": "33.3%"}
    st.metric("Model Confidence (R²)", r2_map[v_index])

with res3:
    # Nearest Neighbor Logic for Health Classification
    t = thresholds[f_target]
    diffs = {
        "PRISTINE (TNP)": abs(prediction - t["Pristine"]),
        "STABLE (STF)": abs(prediction - t["Stable"]),
        "DISTURBED (TRA)": abs(prediction - t["Disturbed"])
    }
    status = min(diffs, key=diffs.get)
    color = "
