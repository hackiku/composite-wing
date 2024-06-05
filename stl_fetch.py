import streamlit as st
import os
import requests
import base64
from dotenv import load_dotenv
from io import BytesIO
from utils import spacer

# Load environment variables
load_dotenv()

ONSHAPE_ACCESS_KEY = os.getenv("ONSHAPE_ACCESS_KEY")
ONSHAPE_SECRET_KEY = os.getenv("ONSHAPE_SECRET_KEY")
ONSHAPE_BASE_URL = os.getenv("ONSHAPE_BASE_URL")

def get_basic_auth_headers():
    credentials = f"{ONSHAPE_ACCESS_KEY}:{ONSHAPE_SECRET_KEY}"
    basic_auth = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {basic_auth}',
        'Content-Type': 'application/json'
    }
    return headers

def fetch_stl_model(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/partstudios/d/{did}/{wv}/{wvid}/e/{eid}/stl"
    headers = get_basic_auth_headers()
    st.write(f"Fetching STL model from URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        st.write("STL model fetched successfully.")
        return response.content
    else:
        st.error(f"Failed to fetch STL model: {response.status_code} {response.reason}")
        st.write(response.text)
        return None

def main():
    st.title('Onshape STL Model Fetcher and Downloader')

    # Presets
    presets = {
        "composite_wing": {
            "did": "f6ac5c0b25ce21ecd85991db",
            "wv": "w",
            "wvid": "2f1903d2edb515536def7421",
            "eid": "1746a09d07c6f27e71172a7f",
            "url": "https://cad.onshape.com/documents/cae4cba9e2f625664baf1122/w/ba81e6382142c773cd7b78ba/e/640a7618098c9be6fe97b244?renderMode=0&uiState=6654e4567ce53e2d5ac81735"
        }
    }

    # Hardcoded to first preset for now
    preset = "composite_wing"
    st.write(f"Using preset: {preset}")

    did = presets[preset]['did']
    wv = presets[preset]['wv']
    wvid = presets[preset]['wvid']
    eid = presets[preset]['eid']
    
    if st.button('Fetch and Download STL Model'):
        with st.spinner('Fetching STL model...'):
            stl_content = fetch_stl_model(did, wv, wvid, eid)
            if stl_content:
                st.write("Preparing download link...")
                st.download_button(
                    label="Download STL Model",
                    data=stl_content,
                    file_name=f"{preset}_model.stl",
                    mime="application/octet-stream"
                )
                st.write("Download link ready.")

if __name__ == "__main__":
    main()
