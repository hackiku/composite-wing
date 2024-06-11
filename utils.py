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
def crop_image(image_path, crop_params, dark_graphs=False):

    start_x, start_y, width, height = crop_params
    with Image.open(image_path) as img:
        box = (start_x, start_y, start_x + width, start_y + height)
        cropped_image = img.crop(box)
        
        edited_image = invert_colors(cropped_image) if dark_graphs==False else cropped_image
            # edited_image = invert_colors(cropped_image)
    return edited_image

# Example usage
# cropped_img = crop_image("path/to/image.png", 100, 100, 200, 200)
# cropped_img.show()  # Display the cropped image

def invert_colors(image):
    # with Image.open(image_path) as img:
    inverted_image = ImageOps.invert(image.convert("RGB"))
        # inverted_image = ImageOps.invert(img.convert('RGB'))
    return inverted_image
