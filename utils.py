import pandas as pd
import matplotlib.style as mplstyle
import streamlit as st
from PIL import Image

def spacer(height='2em'):
    st.markdown(f'<div style="margin: {height};"></div>', unsafe_allow_html=True)

def set_mpl_style(theme_mode):
    if theme_mode == "dark":
        mplstyle.use('dark_background')
    else:
        mplstyle.use('default')
        


def crop_image(image_path, crop_params):
    """
    Crop an image to a specified size from a given starting coordinate.
    
    Parameters:
    - image_path (str): The path to the image file.
    - crop_params (list or tuple of float): The cropping parameters [start_x, start_y, width, height].
    
    Returns:
    - cropped_image (Image): The cropped PIL Image object.
    """
    start_x, start_y, width, height = crop_params
    with Image.open(image_path) as img:
        box = (start_x, start_y, start_x + width, start_y + height)
        cropped_image = img.crop(box)
    return cropped_image

# Example usage
# cropped_img = crop_image("path/to/image.png", 100, 100, 200, 200)
# cropped_img.show()  # Display the cropped image

def reverse_colors(image_path):
    with Image.open(image_path) as img:
        reversed_image = ImageOps.invert(img.convert('RGB'))
    return reversed_image
