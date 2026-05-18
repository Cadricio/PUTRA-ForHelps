import streamlit as st

# 1. Page Config
st.set_page_config(page_title="Forest Health Dashboard", page_icon="🌳", layout="wide")

# 2. UI Styling to remove clutter
st.markdown("""
    <style>
    .reportview-container { background: #f5f7f9; }
    .stNumberInput, .stSelectbox { border-radius: 10px; }
    div.stButton > button:first-child { background-color: #2e7d32; color:white; }
    </style>
    """, unsafe_allow_index=True)

# 3. Header
st.title("🌲 Forest Health & Fungal Diversity Analyzer")
st.markdown("### Biosystems Engineering Decision Support System")
st.divider()

# 4. Input Zone (Organized in 2 columns)
col_input1, col_input2 = st.columns(2)

with col_input1:
    st.write("#### 1. Parameter Selection")
    selected_index = st.selectbox(
        "Choose Vegetation Index (VI)", 
        ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"]
    )

with col_input2:
    st.write("#### 2. Spectral Data Input")
    # Using number_input instead of slider for unlimited range and precision
    val = st.number_input(f"Enter {selected_index} value observed from Satellite/UAV", value=0.750, step=0.001, format="%.3f")

st.divider()

# 5. Logic Engine
models = {
    "NDRE": {"m": 0.0632, "c": 0.584, "r2": 0.990, "full": "Normalized Difference Red Edge"},
    "CIRE": {"m": 1.1500, "c": 2.820, "r2": 0.918, "full": "Chlorophyll Index - Red Edge"},
    "NDVI": {"m": 0.0347, "c": 0.818, "r2": 0.862, "full": "Normalized Difference Vegetation Index"},
    "VARI": {"m": 0.0611, "c": 0.252, "r2": 0.847, "full": "Visible Resistant Index"},
    "MSAVI": {"m": 0.0181, "c": 0.900, "r2": 0.674, "full": "Modified Soil-Adjusted Index"},
    "SAVI": {"m": -0.0440, "c": 1.230, "r2": 0.616, "full": "Soil-Adjusted Index"},
    "GNDVI": {"m": -0.0242, "c": 0.770, "r2": 0.333, "full": "Green-band Index"}
}

m, c, r2, full_name = models[selected_index]["m"], models[selected_index]["c"], models[selected_index]["r2"], models[selected_index]["full"]
prediction = (val - c) / m

# 6. Results Zone (Three clean cards)
res1, res2, res3 = st.columns(3)

with res1:
    st.metric(label="Predicted Shannon Index (H')", value=f"{prediction:.3f}")
    st.caption(f"Calculated via {selected_index} Regression")

with res2:
    st.metric(label="Model Reliability (R²)", value=f"{r2:.1%}")
    st.caption("Statistical Confidence")

with res3:
    if prediction >= 3.45:
        status, color = "High Diversity", "green"
        site = "Taman Negara Pahang (TNP)"
    elif 3.25 <= prediction < 3.45:
        status, color = "Moderate Diversity", "orange"
        site = "Sungai Tekala Recreational Forest (STF)"
    else:
        status, color = "Low Diversity", "red"
        site = "Taman Rimba Alam (TRA)"
    
    st.markdown(f"**Ecosystem Class:**")
    st.subheader(f":{color}[{status}]")

# 7. Interpretation & Study Sites
st.markdown("---")
st.write("#### 3. Ecological Interpretation")
if color == "green":
    st.success(f"**Primary Forest Condition:** The result aligns with **{site}**. Suggests a stable climax community with high fungal richness.")
elif color == "orange":
    st.warning(f"**Recreational/Secondary Forest:** Matches **{site}**. Indicators suggest moderate ecological health with some human interference.")
else:
    st.error(f"**Urban/Disturbed Condition:** Result aligns with **{site}**. Spectral markers indicate fragmentation and reduced microbial biodiversity.")

# 8. Footer
st.divider()
st.caption(f"Researcher: Luqman Nur Haqeem | Thesis Reference: UAV Multispectral Biodiversity Assessment | Logic: H' = (VI - {c}) / {m}")