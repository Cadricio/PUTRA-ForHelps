import streamlit as st
import rasterio
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="PUTRA Forest Health Prediction System Pro", layout="wide")
st.title("🌲 PUTRA Forest Health & Fungal Diversity Predictor (Pro)")

# 2. Regression Models (x = (y - c) / m)
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
        data = src.read()
        
        # Robust band handling (ensures we get 3 bands for RGB display)
        num_bands = min(data.shape[0], 3)
        rgb = data[:num_bands, :, :]
        rgb_display = np.zeros((rgb.shape[1], rgb.shape[2], 3), dtype=np.uint8)
        
        for i in range(num_bands):
            band = rgb[i, :, :]
            if band.max() - band.min() > 0:
                norm_band = 255 * (band - band.min()) / (band.max() - band.min())
            else:
                norm_band = band
            rgb_display[:, :, i] = norm_band.astype(np.uint8)
        
        display_img = Image.fromarray(rgb_display)

    st.write("### Select a pixel on the forest to analyze:")
    coordinates = streamlit_image_coordinates(display_img)

    if coordinates:
        x, y = coordinates["x"], coordinates["y"]
        st.write(f"**Coordinates:** x={x}, y={y}")
        
        # Placeholder for your VI calculation logic
        # In a real scenario, you would calculate specific VI based on pixel_data
        st.subheader("Predicted Fungal Diversity Indices")
        
        selected_vi = st.selectbox("Select VI for prediction", list(models.keys()))
        
        # Example calculation (replace 0.750 with your actual pixel-based formula)
        vi_val = 0.750 
        m = models[selected_vi]["m"]
        c = models[selected_vi]["c"]
        shannon = (vi_val - c) / m
        
        st.metric("Predicted Shannon Diversity (H')", round(shannon, 3))
