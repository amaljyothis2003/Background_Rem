import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import base64

st.set_page_config(layout="wide", page_title="Image Background Remover & Editor")

st.write("## Remove background and Edit your Image")
st.write(":art: Upload your image to remove background and apply various filters. This app uses the [rembg](https://github.com/danielgatis/rembg) library.")
st.sidebar.write("## Upload, Edit, and Download :gear:")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Convert image to bytes for download
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Apply Image Filters
def apply_filters(image, brightness, contrast, grayscale, blur, edge_enhance):
    # Brightness
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    
    # Contrast
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)

    # Grayscale
    if grayscale:
        image = image.convert("L")

    # Blur
    if blur:
        image = image.filter(ImageFilter.GaussianBlur(2))

    # Edge Enhancement
    if edge_enhance:
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    
    return image

# Change Background
def change_background(image, background):
    background = background.resize(image.size)
    background.paste(image, (0, 0), image)
    return background

# Process Image
def fix_image(upload, bg_upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image, use_column_width=True)

    # Remove Background
    fixed = remove(image)
    col2.write("Background Removed Image :wrench:")
    col2.image(fixed, use_column_width=True)

    # Sidebar options for filters
    st.sidebar.write("### Image Editing Options")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    grayscale = st.sidebar.checkbox("Grayscale")
    blur = st.sidebar.checkbox("Blur")
    edge_enhance = st.sidebar.checkbox("Edge Enhance")

    edited_image = apply_filters(fixed, brightness, contrast, grayscale, blur, edge_enhance)
    
    # Background change
    if bg_upload is not None:
        background = Image.open(bg_upload)
        edited_image = change_background(edited_image, background)
        col2.write("Image with New Background :sparkles:")
    else:
        col2.write("Edited Image :sparkles:")
    
    col2.image(edited_image, use_column_width=True)

    st.sidebar.markdown("\n")
    st.sidebar.download_button("Download Edited Image", convert_image(edited_image), "edited_image.png", "image/png")

col1, col2 = st.columns(2)
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
background_upload = st.sidebar.file_uploader("Upload a background image (optional)", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
    else:
        fix_image(my_upload, background_upload)
else:
    st.info("Please upload an image to proceed.")