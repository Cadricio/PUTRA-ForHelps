import streamlit as st
import rasterio
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

st.set_page_config(page_title="PUTRA ForHelps Pro", layout="wide")
st.title("🌲 PUTRA Forest Health Predictor (Pro)")

uploaded_file = st.file_uploader("Upload PlanetScope Multispectral TIFF", type=["tif", "tiff"])

if uploaded_file:
    with rasterio.open(uploaded_file) as src:
        data = src.read() # Shape: (Bands, Height, Width)
        st.write(f"DEBUG: Data shape detected: {data.shape}") 
        
        # --- IMAGE DISPLAY LOGIC ---
        # Map first 3 bands to RGB, handle if < 3 bands exist
        num_bands = data.shape[0]
        display_bands = min(num_bands, 3)
        rgb_display = np.zeros((data.shape[1], data.shape[2], 3), dtype=np.uint8)
        
        for i in range(display_bands):
            band = data[i, :, :]
            p2, p98 = np.percentile(band, (2, 98))
            norm = np.clip((band - p2) / (p98 - p2 + 1e-8), 0, 1)
            rgb_display[:, :, i] = (norm * 255).astype(np.uint8)
        
        display_img = Image.fromarray(rgb_display)

    coordinates = streamlit_image_coordinates(display_img)

    if coordinates:
        x, y = coordinates["x"], coordinates["y"]
        st.write(f"**Coordinates:** x={x}, y={y}")
        
        # --- DYNAMIC CALCULATION ---
        # If your data has at least 5 bands (B, G, R, NIR, RE), this works:
        if num_bands >= 5:
            b_red = data[2, y, x]
            b_nir = data[3, y, x]
            b_rededge = data[4, y, x]
            
            ndvi = (b_nir - b_red) / (b_nir + b_red + 1e-8)
            st.metric("Calculated NDVI at point", round(ndvi, 3))
        else:
            st.error(f"Error: Your file only has {num_bands} bands. Need at least 5 for NIR/RE indices.")
