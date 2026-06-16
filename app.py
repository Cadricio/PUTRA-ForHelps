import streamlit as st
import rasterio
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="PUTRA Forest Health Prediction System Pro", layout="wide")
st.title("🌲 PUTRA Forest Health & Fungal Diversity Predictor (Pro)")
st.markdown("Automated Forest Health monitoring using multispectral satellite data.")

# 2. Regression Models based on Table 4.15
# x = (y - c) / m 
models = {
    "NDRE": {"m": 0.0632, "c": 0.584},
    "CIRE": {"m": 1.1500, "c": 2.820},
    "NDVI": {"m": 0.0347, "c": 0.818},
    "VARI": {"m": 0.0611, "c": 0.252},
    "MSAVI": {"m": 0.0181, "c": 0.900},
    "SAVI": {"m": -0.0440, "c": 1.230},
    "GNDVI": {"m": -0.0242, "c": 0.770}
}

# 3. TIFF Input
uploaded_file = st.file_uploader("Upload PlanetScope Multispectral TIFF", type=["tif", "tiff"])

if uploaded_file:
    with rasterio.open(uploaded_file) as src:
        data = src.read()  # Reads [Bands, Height, Width]
        # Create a displayable image (using first 3 bands as RGB)
        display_img = Image.fromarray(np.moveaxis(data[:3, :, :], 0, -1).astype(np.uint8))
    
    st.write("### Select a pixel on the forest to analyze:")
    coordinates = streamlit_image_coordinates(display_img)

    if coordinates:
        x, y = coordinates["x"], coordinates["y"]
        st.write(f"**Coordinates:** x={x}, y={y}")
        
        # Extract reflectance values at (x, y)
        pixel_data = data[:, y, x]
        
        # 4. Calculation Logic
        # NOTE: Ensure the index of bands matches your TIFF configuration
        # Band order: Blue, Green, Red, NIR, Red-Edge [cite: 266]
        # Example for NDRE Calculation[cite: 226]:
        # NIR = data[3], RedEdge = data[4] (adjust based on your actual TIFF)
        
        st.subheader("Predicted Fungal Diversity Indices")
        
        # Example for one model
        selected_vi = "NDRE" 
        vi_val = 0.750 # This would be calculated from pixel_data
        
        m = models[selected_vi]["m"]
        c = models[selected_vi]["c"]
        shannon = (vi_val - c) / m
        
        col1, col2 = st.columns(2)
        col1.metric("Shannon Diversity (H')", round(shannon, 3))
        col2.info("Based on research findings from UPM [cite: 3]")
