import streamlit as st
import rasterio
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

st.set_page_config(page_title="PUTRA ForHelps Pro", layout="wide")
st.title("🌲 PUTRA Forest Health Predictor (Pro)")

uploaded_file = st.file_uploader("Upload PlanetScope TIFF", type=["tif", "tiff"])

if uploaded_file:
    with rasterio.open(uploaded_file) as src:
        data = src.read() # Shape: (Bands, Height, Width)
        num_bands = data.shape[0]
        st.write(f"Detected: {num_bands} bands in your TIFF.")

        # --- DYNAMIC IMAGE DISPLAY ---
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
        
        # --- DYNAMIC CALCULATION LOGIC ---
        if num_bands >= 5:
            st.success("Multispectral Data Detected (NIR & Red-Edge available).")
            # Assuming PlanetScope order: B, G, R, NIR, RE (indices 0, 1, 2, 3, 4)
            b_red = data[2, y, x]
            b_nir = data[3, y, x]
            b_rededge = data[4, y, x]
            
            # Allow user to pick between NDVI and NDRE
            index_choice = st.selectbox("Choose Index", ["NDVI", "NDRE"])
            if index_choice == "NDVI":
                vi = (b_nir - b_red) / (b_nir + b_red + 1e-8)
            else:
                vi = (b_nir - b_rededge) / (b_nir + b_rededge + 1e-8)
            st.metric(f"{index_choice} Value", round(vi, 3))
            
        else:
            st.warning("RGB Data Detected. Using Visible Index (VARI).")
            # VARI uses only R, G, B bands (Indices 0=B, 1=G, 2=R)
            b_blue = data[0, y, x]
            b_green = data[1, y, x]
            b_red = data[2, y, x]
            
            # VARI formula: (G - R) / (G + R - B)
            vi = (b_green - b_red) / (b_green + b_red - b_blue + 1e-8)
            st.metric("Calculated VARI Value", round(vi, 3))

# Define regression coefficients (m, c) for the four indices
# Structure: {IndexName: {VI_Name: {"m": value, "c": value}}}
# Replace these placeholder values with the exact constants from your thesis data
fungal_models = {
    "Shannon": {"VARI": {"m": 0.0611, "c": 0.252}, "NDRE": {"m": 0.0632, "c": 0.584}},
    "Richness": {"VARI": {"m": 0.05, "c": 0.2}, "NDRE": {"m": 0.04, "c": 0.1}}, # Update with real thesis values
    "Simpson": {"VARI": {"m": 0.07, "c": 0.3}, "NDRE": {"m": 0.06, "c": 0.4}},  # Update with real thesis values
    "Evenness": {"VARI": {"m": 0.03, "c": 0.1}, "NDRE": {"m": 0.02, "c": 0.05}}  # Update with real thesis values
}

# In your coordinates block:
if coordinates:
    # ... (calculate 'vi' value as you did before) ...
    
    selected_vi = "VARI" if num_bands < 5 else "NDRE" # Or based on user selection
    
    st.subheader("Predicted Fungal Diversity Indices")
    
    # Calculate and display all 4 indices
    cols = st.columns(4)
    for i, (name, models) in enumerate(fungal_models.items()):
        if selected_vi in models:
            m = models[selected_vi]["m"]
            c = models[selected_vi]["c"]
            prediction = (vi - c) / m
            cols[i].metric(name, round(prediction, 3))
