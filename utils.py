import pandas as pd
import matplotlib.style as mplstyle
import streamlit as st
from PIL import Image, ImageOps

def spacer(height='2em'):
    st.markdown(f'<div style="margin: {height};"></div>', unsafe_allow_html=True)

def set_mpl_style(theme_mode):
    if theme_mode == "dark":
        mplstyle.use('dark_background')
    else:
        mplstyle.use('default')
        
# def crop_image(image_path, crop_params, invert_color, dark_graphs):
def crop_image(image_path, crop_params):

    start_x, start_y, width, height = crop_params
    with Image.open(image_path) as img:
        box = (start_x, start_y, start_x + width, start_y + height)
        cropped_image = img.crop(box)
    return cropped_image

def invert_colors(image):
    inverted_image = ImageOps.invert(image.convert("RGB"))
    return inverted_image
