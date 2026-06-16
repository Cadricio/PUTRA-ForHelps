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
        data = src.read()  # Reads [Bands, Height, Width]
        
        # 1. Select first 3 bands (or fewer if fewer exist)
        num_bands = min(data.shape[0], 3)
        rgb = data[:num_bands, :, :]
        
        # 2. Initialize a blank (H, W, 3) array
        height, width = rgb.shape[1], rgb.shape[2]
        rgb_display = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 3. Normalize each band individually for contrast
        for i in range(num_bands):
            band = rgb[i, :, :]
            # Use 2nd and 98th percentile to ignore extreme outliers (hot pixels)
            p2, p98 = np.percentile(band, (2, 98))
            
            # Clip values to the percentile range and scale to 0-255
            norm_band = np.clip((band - p2) / (p98 - p2 + 1e-8), 0, 1)
            rgb_display[:, :, i] = (norm_band * 255).astype(np.uint8)
            
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
        
       # Extract the reflectance values at the clicked (x, y) coordinate
        # Assuming data order is: [Band1, Band2, Band3, NIR, RedEdge]
        # Adjust these indices [0, 1, 2, 3, 4] to match your specific TIFF band order!
        b_red = data[2, y, x]
        b_nir = data[3, y, x]
        b_rededge = data[4, y, x]
        
        # Calculate the Vegetation Index based on user selection
        if selected_vi == "NDVI":
            vi_val = (b_nir - b_red) / (b_nir + b_red + 1e-8)
        elif selected_vi == "NDRE":
            vi_val = (b_nir - b_rededge) / (b_nir + b_rededge + 1e-8)
        else:
            # Fallback/Placeholder for other indices
            vi_val = 0.5 

        # Calculate prediction using the formula from your thesis
        m = models[selected_vi]["m"]
        c = models[selected_vi]["c"]
        prediction = (vi_val - c) / m
        
        st.metric(f"Predicted Shannon Diversity (H') using {selected_vi}", round(prediction, 3))
