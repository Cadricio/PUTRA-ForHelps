import streamlit as st
import rasterio
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

st.set_page_config(page_title="PUTRA ForHelps Pro", layout="wide")
st.title("🌲 PUTRA Forest Health & Fungal Diversity Predictor")

# Thesis Regression Constants (y = mx + c)
# Inverse formula to predict diversity (x): x = (y - c) / m
fungal_models = {
    "Shannon": {"m": 0.0632, "c": 0.584},
    "Richness": {"m": 0.0510, "c": 0.320},
    "Simpson": {"m": 0.0712, "c": 0.410},
    "Evenness": {"m": 0.0425, "c": 0.150}
}

uploaded_file = st.file_uploader("Upload PlanetScope TIFF", type=["tif", "tiff"])

if uploaded_file:
    with rasterio.open(uploaded_file) as src:
        data = src.read()
        num_bands = data.shape[0]

        # Robust contrast-stretched display logic
        rgb_display = np.zeros((data.shape[1], data.shape[2], 3), dtype=np.uint8)
        display_bands = min(num_bands, 3)
        for i in range(display_bands):
            band = data[i, :, :]
            p2, p98 = np.percentile(band[band > 0], (2, 98)) if band[band > 0].size > 0 else (0, 1)
            norm = np.clip((band - p2) / (p98 - p2 + 1e-8), 0, 1)
            rgb_display[:, :, i] = (norm * 255).astype(np.uint8)
        display_img = Image.fromarray(rgb_display)

    # Split-screen UI
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Analysis Area")
        coords = streamlit_image_coordinates(display_img, use_column_width=True)

    with col2:
        st.subheader("Analysis Results")
        if coords:
            x, y = coords["x"], coords["y"]
            
            # Auto-select index logic
            if num_bands >= 5:
                # Assuming PlanetScope: B, G, R, NIR, RE (indices 0, 1, 2, 3, 4)
                vi = (data[3, y, x] - data[2, y, x]) / (data[3, y, x] + data[2, y, x] + 1e-8)
                st.info(f"Multispectral mode (NDVI): {round(float(vi), 3)}")
            else:
                # Fallback to VARI for 3-band RGB
                vi = (data[1, y, x] - data[2, y, x]) / (data[1, y, x] + data[2, y, x] - data[0, y, x] + 1e-8)
                st.info(f"RGB mode (VARI): {round(float(vi), 3)}")

            # Calculate and display metrics
            metrics = st.columns(2)
            for i, (name, coeffs) in enumerate(fungal_models.items()):
                pred = (vi - coeffs["c"]) / coeffs["m"]
                metrics[i % 2].metric(name, round(float(pred), 3))
        else:
            st.info("Click on a forest point to generate metrics.")
