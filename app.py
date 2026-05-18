import streamlit as st

# 1. Page Setup
st.set_page_config(page_title="Forest Fungal Predictor", page_icon="🍄", layout="wide")

# 2. Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #2e7d32; }
    </style>
    """, unsafe_allow_index=True)

# 3. Header
st.title("🌳 Forest Health & Fungal Diversity Predictor")
st.markdown("##### Decision Support System based on Research by Luqman Nur Haqeem")
st.divider()

# 4. Inputs (Top Row)
col_a, col_b = st.columns(2)

with col_a:
    selected_index = st.selectbox(
        "Select Vegetation Index (VI)", 
        ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"]
    )

with col_b:
    # Wider range as requested
    val = st.number_input(f"Enter {selected_index} Value", value=0.750, min_value=-100.0, max_value=100.0, step=0.001, format="%.3f")

st.divider()

# 5. Engineering Logic
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
r2 = models[selected_index]["r2"]

# The Prediction Calculation: x = (y - c) / m
prediction = (val - c) / m

# 6. Results Row
res1, res2, res3 = st.columns(3)

with res1:
    st.metric("Predicted Shannon Index (H')", f"{prediction:.3f}")
with res2:
    st.metric("Model Confidence (R²)", r2)
with res3:
    if prediction >= 3.45:
        label, site, color = "PRISTINE", "Taman Negara Pahang (TNP)", "green"
    elif 3.25 <= prediction < 3.45:
        label, site, color = "STABLE", "Sungai Tekala Recreational Forest (STF)", "orange"
    else:
        label, site, color = "DISTURBED", "Taman Rimba Alam (TRA)", "red"
    
    st.write("**Ecosystem Status:**")
    st.subheader(f":{color}[{label}]")

# 7. Site Interpretation Box
st.markdown("---")
if color == "green":
    st.success(f"**Condition Assessment:** High health levels detected. Profile matches **{site}**.")
elif color == "orange":
    st.warning(f"**Condition Assessment:** Moderate health levels detected. Profile matches **{site}**.")
else:
    st.error(f"**Condition Assessment:** Low health/High stress detected. Profile matches **{site}**.")

# 8. Comparison Table (Manual HTML to avoid Pandas errors)
st.markdown("### 📍 Study Site Baselines")
st.markdown(f"""
| Site Name | Category | Average H' Value |
| :--- | :--- | :--- |
| **Taman Negara Pahang (TNP)** | Primary Forest | 3.483 |
| **Sungai Tekala Recreational Forest (STF)** | Recreational Forest | 3.389 |
| **Taman Rimba Alam (TRA)** | Urban Forest | 3.123 |
""", unsafe_allow_html=True)

st.divider()
st.caption(f"Logic: Linear Regression | Calculation: ({val} - {c}) / {m}")
