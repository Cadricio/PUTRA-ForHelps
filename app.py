import streamlit as st
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Forest Health Predictor", page_icon="🌳", layout="wide")

# 2. Sidebar for Inputs
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/b/bd/Universiti_Putra_Malaysia_logo.png", width=100) # Optional UPM Logo link
st.sidebar.title("System Controls")
st.sidebar.markdown("---")

selected_index = st.sidebar.selectbox(
    "Choose Vegetation Index (VI)", 
    ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"]
)

# Dynamic slider range based on typical VI values
val = st.sidebar.slider(f"Input {selected_index} Value", 0.0, 1.0, 0.75, step=0.01)

st.sidebar.markdown("---")
st.sidebar.write("**Researcher:** Luqman Nur Haqeem")
st.sidebar.write("**Faculty:** Engineering, UPM")

# 3. Main Dashboard Area
st.title("🌲 Forest Health & Fungal Diversity Analysis")
st.markdown(f"### Current Model: {selected_index} Regression Analysis")

# 4. Logic (y = mx + c) -> x = (y - c) / m
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

# 5. Display Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Predicted Shannon Index (H')", value=f"{prediction:.3f}")

with col2:
    st.metric(label="Model Reliability (R²)", value=f"{r2:.1%}")

with col3:
    # Classification Logic based on your Site Results
    if prediction >= 3.45:
        status = "High Diversity"
        site = "Taman Negara Pahang (TNP)"
        color = "inverse" # Green
    elif 3.25 <= prediction < 3.45:
        status = "Moderate Diversity"
        site = "Sungai Tekala Recreational Forest (STF)"
        color = "normal" # Orange
    else:
        status = "Low Diversity"
        site = "Taman Rimba Alam (TRA)"
        color = "off" # Red
    st.metric(label="Ecosystem Class", value=status)

# 6. Detailed Interpretation Box
st.markdown("---")
if status == "High Diversity":
    st.success(f"✅ **Primary Forest Condition:** The spectral signature matches the profile of **{site}**. High biological stability detected.")
elif status == "Moderate Diversity":
    st.warning(f"⚠️ **Secondary/Recreational Condition:** Matches the profile of **{site}**. Minor anthropogenic stress likely.")
else:
    st.error(f"🚨 **Urban/Disturbed Condition:** Matches the profile of **{site}**. Low fungal biodiversity and high fragmentation detected.")

# 7. Model Equation display
st.info(f"**Engineering Logic:** Used {full_name} to solve for fungal diversity where $H' = ({val} - {c}) / {m}$")