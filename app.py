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
        
        # Determine how many bands we can actually use (up to 3)
        num_bands = min(data.shape[0], 3)
        rgb = data[:num_bands, :, :]
        
        # Create a blank canvas (H, W, 3) to ensure we always have 3 channels for RGB
        rgb_display = np.zeros((rgb.shape[1], rgb.shape[2], 3), dtype=np.uint8)
        
        for i in range(num_bands):
            band = rgb[i, :, :]
            # Normalize to 0-255
            if band.max() - band.min() > 0:
                norm_band = 255 * (band - band.min()) / (band.max() - band.min())
            else:
                norm_band = band
            rgb_display[:, :, i] = norm_band.astype(np.uint8)
        
        display_img = Image.fromarray(rgb_display)
        for i in range(3):
            band = rgb[i, :, :]
            # Normalize each band based on its min/max values
            if band.max() - band.min() > 0:
                rgb_norm[i, :, :] = 255 * (band - band.min()) / (band.max() - band.min())
            else:
                rgb_norm[i, :, :] = band
        
        # 3. Transpose to [Height, Width, Bands] for PIL and convert
        display_img = Image.fromarray(np.moveaxis(rgb_norm, 0, -1))
    
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
