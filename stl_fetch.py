import streamlit as st
import os
import requests
import base64
from dotenv import load_dotenv
from utils import spacer
from show_model import load_stl, get_model_files
from io import BytesIO

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

def initiate_stl_export(did, wid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/partstudios/d/{did}/w/{wid}/e/{eid}/stl?mode=text&grouping=true&scale=1&units=inch"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 307:
        redirect_url = response.headers['Location']
        return redirect_url
    else:
        st.error(f"Failed to initiate export: {response.status_code} {response.reason}")
        st.write(response.text)
        return None

def download_stl_model(redirect_url):
    headers = get_basic_auth_headers()
    response = requests.get(redirect_url, headers=headers)
    if response.status_code == 200:
        st.write("STL model downloaded.")
        return response.content
    else:
        st.error(f"Failed to download STL model: {response.status_code} {response.reason}")
        st.write(response.text)
        return None

def main():
    st.header('Fetch Onshape STL')

    # Presets
    presets = {
        "composite_wing": {
            "did": "f6ac5c0b25ce21ecd85991db",
            "wid": "2f1903d2edb515536def7421",
            "eid": "1746a09d07c6f27e71172a7f",
            "url": "https://cad.onshape.com/documents/cae4cba9e2f625664baf1122/w/ba81e6382142c773cd7b78ba/e/640a7618098c9be6fe97b244?renderMode=0&uiState=6654e4567ce53e2d5ac81735"
        }
    }

    # Hardcoded to first preset for now
    preset = "composite_wing"
    st.write(f"Using preset: {preset}")

    did = presets[preset]['did']
    wid = presets[preset]['wid']
    eid = presets[preset]['eid']

    if st.button('Fetch and Visualize STL Model'):
        with st.spinner('Fetching STL model...'):
            redirect_url = initiate_stl_export(did, wid, eid)
            if redirect_url:
                stl_content = download_stl_model(redirect_url)
                if stl_content:
                    stl_path = f"/tmp/{preset}_model.stl"
                    with open(stl_path, 'wb') as f:
                        f.write(stl_content)
                    fig = load_stl(stl_path)
                    if fig:
                        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
