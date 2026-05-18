import streamlit as st
import pandas as pd

# App Title and Description
st.set_page_config(page_title="Forest Health Fungal Predictor", layout="wide")
st.title("🌲 Forest Health & Fungal Diversity Predictor")
st.markdown("""
This decision support system uses **PlanetScope Multispectral Indices** to predict subterranean fungal diversity 
based on the research findings of **Luqman Nur Haqeem (UPM)**.
""")

# Sidebar for Input
st.sidebar.header("Input Parameters")
selected_index = st.sidebar.selectbox(
    "Choose a Vegetation Index (VI)", 
    ["NDRE", "CIRE", "NDVI", "VARI", "MSAVI", "SAVI", "GNDVI"]
)

# Use number input for the index value
x_input = st.sidebar.number_input(f"Enter {selected_index} Value", value=0.5, step=0.01)

# Logic Dictionary based on Table 4.1 from Thesis
# y = mx + c (where x is fungal diversity index and y is VI)
# To predict Fungal Diversity (x) from VI (y), we use: x = (y - c) / m
models = {
    "NDRE": {"m": 0.0632, "c": 0.584, "r2": 0.990, "desc": "High Sensitivity Red-Edge Index"},
    "CIRE": {"m": 1.1500, "c": 2.820, "r2": 0.918, "desc": "Chlorophyll Index - Red Edge"},
    "NDVI": {"m": 0.0347, "c": 0.818, "r2": 0.862, "desc": "Standard Greenness Index"},
    "VARI": {"m": 0.0611, "c": 0.252, "r2": 0.847, "desc": "Visible Resistant Index"},
    "MSAVI": {"m": 0.0181, "c": 0.900, "r2": 0.674, "desc": "Modified Soil-Adjusted Index"},
    "SAVI": {"m": -0.0440, "c": 1.230, "r2": 0.616, "desc": "Soil-Adjusted Index"},
    "GNDVI": {"m": -0.0242, "c": 0.770, "r2": 0.333, "desc": "Green-band Index"}
}

# Calculate Prediction
m = models[selected_index]["m"]
c = models[selected_index]["c"]
r2 = models[selected_index]["r2"]

# Solving for x (Fungal Diversity Index)
prediction = (x_input - c) / m

# Display Results
col1, col2 = st.columns(2)

with col1:
    st.subheader("Results")
    st.metric(label="Predicted Shannon Diversity Index (H')", value=round(prediction, 3))
    st.info(f"**Model Accuracy (R²):** {r2}")
    st.caption(f"Note: This uses the equation y = {m}x + {c}")

with col2:
    st.subheader("Ecosystem Interpretation")
    if prediction >= 3.4:
        st.success("Status: Primary Forest (High Health)")
        st.write("The spectral signature suggests a stable, high-diversity ecosystem similar to TNP.")
    elif 3.1 <= prediction < 3.4:
        st.warning("Status: Recreational Forest (Moderate Health)")
        st.write("Moderate diversity levels with potential anthropogenic disturbance.")
    else:
        st.error("Status: Urban Forest (Disturbed/Low Health)")
        st.write("Lower fungal diversity often associated with fragmented urban environments like TRA.")

st.divider()
st.write("Agricultural and Biosystems Engineering - UPM")