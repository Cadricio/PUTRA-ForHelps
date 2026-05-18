import streamlit as st

# 1. Basic Page Setup
st.set_page_config(page_title="Forest Health Predictor", page_icon="🌳", layout="wide")

# 2. Clean Header
st.title("🌳 Forest Health & Fungal Diversity Predictor")
st.write("### Agricultural & Biosystems Engineering Decision Support System")
st.markdown("---")

# 3. Input Section
col_left, col_right = st.columns(2)

with col_left:
    selected_index = st.selectbox(
        "1. Select Vegetation Index (VI)", 
        ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"]
    )

with col_right:
    # Wide range from -100 to 100 as you requested
    val = st.number_input(f"2. Enter {selected_index} Value", value=0.750, min_value=-100.0, max_value=100.0, step=0.001, format="%.3f")

st.markdown("---")

# 4. Regression Logic Engine (Based on Thesis Table 4.1)
models = {
    "NDRE": {"m": 0.0632, "c": 0.584, "r2": "99.0%"},
    "CIRE": {"m": 1.1500, "c": 2.820, "r2": "91.8%"},
    "NDVI": {"m": 0.0347, "c": 0.818, "r2": "86.2%"},
    "VARI": {"m": 0.0611, "c": 0.252, "r2": "84.7%"},
    "MSAVI": {"m": 0.0181, "c": 0.900, "r2": "67.4%"},
    "SAVI": {"m": -0.0440, "c": 1.230, "r2": "61.6%"},
    "GNDVI": {"m": -0.0242, "c": 0.770, "r2": "33.3%"}
}

m = models[selected_index]["m"]
c = models[selected_index]["c"]
r2_val = models[selected_index]["r2"]

# Calculate H' Prediction
prediction = (val - c) / m

# 5. Dashboard Display
st.write("### 📊 Analysis Results")
metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric("Shannon Index (H')", f"{prediction:.3f}")

with metric_2:
    st.metric("Model R² Accuracy", r2_val)

with metric_3:
    if prediction >= 3.45:
        status, site = "🟢 PRISTINE", "Taman Negara Pahang (TNP)"
    elif 3.25 <= prediction < 3.45:
        status, site = "🟠 STABLE", "Sungai Tekala Recreational Forest (STF)"
    else:
        status, site = "🔴 DISTURBED", "Taman Rimba Alam (TRA)"
    st.write("**Ecosystem Class:**")
    st.subheader(status)

# 6. Site Context
st.info(f"**Condition Assessment:** This reading most closely matches the profile of **{site}**.")

# 7. Comparison Data
st.markdown("### 📍 Research Baseline Comparison")
# Manual table to avoid library errors
st.markdown("""
| Study Site Name | Forest Category | Avg Shannon Index (H') |
| :--- | :--- | :--- |
| **Taman Negara Pahang (TNP)** | Primary Forest | 3.483 |
| **Sungai Tekala Recreational Forest (STF)** | Recreational Forest | 3.389 |
| **Taman Rimba Alam (TRA)** | Urban Forest | 3.123 |
""")

st.markdown("---")
st.caption(f"Researcher: Luqman Nur Haqeem | Formula: H' = ({val} - {c}) / {m}")
