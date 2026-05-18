import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="PUTRA Forest Health", page_icon="🌳", layout="wide")

# 2. Updated Title
st.title("🌲 PUTRA Forest Health Prediction System")
st.markdown("##### Decision Support System | Agricultural and Biosystems Engineering")
st.divider()

# 3. Input Section
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
    val = st.number_input(f"3. Enter {v_index} Value", value=0.750, min_value=-100.0, max_value=100.0, step=0.001)

# 4. Regression Engine (Using your thesis coefficients)
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

# 5. Prediction Dashboard
st.write(f"### 📊 Prediction for {f_index}")
res1, res2, res3 = st.columns(3)

with res1:
    st.metric(f"Predicted {f_index}", f"{prediction:.3f}")

with res2:
    st.metric("Model Confidence (R²)", r2)

with res3:
    # 1. Logic for Shannon Index
    if f_index == "Shannon Index (H')":
        if prediction >= 3.45: status, site, color = "PRISTINE", "TNP", "green"
        elif 3.25 <= prediction < 3.45: status, site, color = "STABLE", "STF", "orange"
        else: status, site, color = "DISTURBED", "TRA", "red"
        
    # 2. Logic for Species Richness
    elif f_index == "Species Richness (S)":
        if prediction >= 65: status, site, color = "PRISTINE", "TNP", "green"
        elif 50 <= prediction < 65: status, site, color = "STABLE", "STF", "orange"
        else: status, site, color = "DISTURBED", "TRA", "red"

    # 3. Logic for Simpson Index (1-D)
    elif f_index == "Simpson Index (1-D)":
        if prediction >= 0.954: status, site, color = "PRISTINE", "TNP", "green"
        elif 0.945 <= prediction < 0.954: status, site, color = "STABLE", "STF", "orange"
        else: status, site, color = "DISTURBED", "TRA", "red"

    # 4. Logic for Pielou's Evenness (J')
    elif f_index == "Pielou's Evenness (J')":
        # Note: In your data, TNP (0.804) is actually lower than STF (0.849)
        # We classify based on your site profiles
        if 0.800 <= prediction < 0.810: status, site, color = "PRISTINE", "TNP", "green"
        elif prediction >= 0.840: status, site, color = "STABLE", "STF", "orange"
        else: status, site, color = "DISTURBED", "TRA", "red"
    
    st.write("**Ecosystem Class:**")
    st.subheader(f":{color}[{status}]")

# 6. Research Baselines
st.markdown("### 📍 Research Site Reference Values")
st.markdown("""
| Study Site Name | Shannon (H') | Simpson (1-D) | Evenness (J') | Richness (S) |
| :--- | :---: | :---: | :---: | :---: |
| **Taman Negara Pahang (TNP)** | 3.483 | 0.955 | 0.804 | 76.0 |
| **Sungai Tekala (STF)** | 3.389 | 0.952 | 0.849 | 54.0 |
| **Taman Rimba Alam (TRA)** | 3.123 | 0.936 | 0.820 | 45.0 |
""", unsafe_allow_html=True)

st.divider()

# 7. Professional Remarks (Added at bottom)
st.write("**Made by:**")
st.write("Luqman Nur Haqeem bin Noor Azuan (215506)")
st.write("Agricultural and Biosystem Engineering (UPM)")
