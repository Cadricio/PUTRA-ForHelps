import streamlit as st

# 1. Page Setup
st.set_page_config(page_title="Multi-Index Forest Health", page_icon="🍄", layout="wide")

# 2. Header
st.title("🌲 Advanced Forest Health & Fungal Diversity Predictor")
st.markdown("##### Research-Based Decision Support System | UPM")
st.divider()

# 3. Step-by-Step Selection
c1, c2, c3 = st.columns(3)

with c1:
    f_index = st.selectbox(
        "1. Select Fungal Target", 
        ["Shannon Index (H')", "Simpson Index (1-D)", "Pielou's Evenness (J')", "Species Richness (S)"]
    )

with c2:
    v_index = st.selectbox(
        "2. Select Vegetation Index (VI)", 
        ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"]
    )

with c3:
    val = st.number_input(f"3. Enter observed {v_index} Value", value=0.750, min_value=-100.0, max_value=100.0, step=0.001, format="%.3f")

# 4. Regression Engine (Constants from your PDF)
# Note: All your models use the same m/c coefficients relative to the VI
models = {
    "NDRE": {"m": 0.0632, "c": 0.584, "r2": "99.0%"},
    "CIRE": {"m": 1.1500, "c": 2.820, "r2": "91.8%"},
    "NDVI": {"m": 0.0347, "c": 0.818, "r2": "86.2%"},
    "VARI": {"m": 0.0611, "c": 0.252, "r2": "84.7%"},
    "MSAVI": {"m": 0.0181, "c": 0.900, "r2": "67.4%"},
    "SAVI": {"m": 0.0440, "c": 1.230, "r2": "61.6%"},
    "GNDVI": {"m": -0.0242, "c": 0.770, "r2": "33.3%"}
}

m, c, r2 = models[v_index]["m"], models[v_index]["c"], models[v_index]["r2"]
prediction = (val - c) / m

# 5. Results Dashboard
st.divider()
st.write(f"### 📊 Prediction for {f_index}")
res1, res2, res3 = st.columns(3)

with res1:
    st.metric(f"Predicted {f_index}", f"{prediction:.3f}")

with res2:
    st.metric("Model Confidence (R²)", r2)

with res3:
    # Classification Logic (Thresholds adjusted per Index from your data)
    if f_index == "Shannon Index (H')":
        if prediction >= 3.45: status, site, color = "PRISTINE", "Taman Negara Pahang (TNP)", "green"
        elif 3.25 <= prediction < 3.45: status, site, color = "STABLE", "Sungai Tekala Recreational Forest (STF)", "orange"
        else: status, site, color = "DISTURBED", "Taman Rimba Alam (TRA)", "red"
    elif f_index == "Species Richness (S)":
        if prediction >= 65: status, site, color = "PRISTINE", "Taman Negara Pahang (TNP)", "green"
        elif 50 <= prediction < 65: status, site, color = "STABLE", "Sungai Tekala Recreational Forest (STF)", "orange"
        else: status, site, color = "DISTURBED", "Taman Rimba Alam (TRA)", "red"
    else:
        status, site, color = "DATA ANALYSIS", "Multiple reference sites", "blue"
    
    st.write("**Ecosystem Class:**")
    st.subheader(f":{color}[{status}]")

# 6. Site Context Info
st.info(f"**Baseline Match:** This result is characteristic of the ecological profile found at **{site}**.")

# 7. Comparison Table (Reference data from your PDF)
st.markdown("### 📍 Research Reference Baselines")
st.markdown(f"""
| Study Site Name | Shannon (H') | Simpson (1-D) | Evenness (J') | Richness (S) |
| :--- | :---: | :---: | :---: | :---: |
| **Taman Negara Pahang (TNP)** | 3.483 | 0.955 | 0.804 | 76.0 |
| **Sungai Tekala (STF)** | 3.389 | 0.952 | 0.849 | 54.0 |
| **Taman Rimba Alam (TRA)** | 3.123 | 0.936 | 0.820 | 45.0 |
""", unsafe_allow_html=True)
