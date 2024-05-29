import streamlit as st
import pandas as pd
import os
import requests
import base64
from dotenv import load_dotenv
from PIL import Image
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

def fetch_custom_variables(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/variables/d/{did}/{wv}/{wvid}/e/{eid}/variables"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch custom variables: {response.status_code} {response.reason}")
        st.write(response.text)
        return None

def get_thumbnail_url(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/thumbnails/d/{did}/{wv}/{wvid}/e/{eid}/s/300x300/"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Failed to fetch thumbnail: {response.status_code} {response.reason}")
        st.write(response.text)
        return None

def display_thumbnail(thumbnail_content):
    try:
        image = Image.open(BytesIO(thumbnail_content))
        st.image(image, caption='Model Thumbnail', use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying thumbnail: {str(e)}")

def main():
    st.title('Onshape Custom Variables and Thumbnail Viewer')

    # Presets
    presets = {
        "COMPOSITE": {
            "did": "cae4cba9e2f625664baf1122",
            "wv": "w",
            "wvid": "ba81e6382142c773cd7b78ba",
            "eid": "640a7618098c9be6fe97b244",
            "url": "https://cad.onshape.com/documents/cae4cba9e2f625664baf1122/w/ba81e6382142c773cd7b78ba/e/640a7618098c9be6fe97b244"
        },
        "Parametric Wing": {
            "did": "308d36ae2431fbf4b9b96a48",
            "wv": "w",
            "wvid": "4dfbfac17da94e7168ec10cd",
            "eid": "1c23a328748cc03fde2f37f5",
            "url": "https://cad.onshape.com/documents/cae4cba9e2f625664baf1122/w/ba81e6382142c773cd7b78ba/e/640a7618098c9be6fe97b244?renderMode=0&uiState=6654e4567ce53e2d5ac81735"
        }
    }

    # Selector for presets
    preset = st.selectbox('Select Preset', list(presets.keys()), index=0)

    # Default placeholders
    col1, col2 = st.columns(2)
    with col1:
        did = st.text_input('Document ID', presets[preset]['did'])
        col3, col4 = st.columns([2,1])
        with col3:
            wv = st.selectbox('WVM', ['w', 'v', 'm'], index=0)
        with col4:
            spacer()
            st.write("[onshape](%s)" % presets[preset]['url'])
    with col2:
        wvid = st.text_input('WVMID', presets[preset]['wvid'])
        eid = st.text_input('Element ID', presets[preset]['eid'])
        
    if st.button('Fetch and Display Custom Variables'):
        if did and wvid and eid:
            variables = fetch_custom_variables(did, wv, wvid, eid)
            if variables:
                st.json(variables, expanded=False)  # Debug statement
                data = []
                if isinstance(variables, list):
                    for variable_table in variables:
                        if 'variables' in variable_table:
                            for var in variable_table['variables']:
                                value = var['value']
                                if value is None:
                                    value = var.get('expression', 'N/A')
                                data.append({
                                    'Name': var['name'],
                                    'Type': var['type'],
                                    'Value': value,
                                    'Description': var.get('description', '')
                                })
                    df = pd.DataFrame(data)
                    st.table(df)
                else:
                    st.error("Unexpected data format received from API.")

    if st.button('Display Thumbnail'):
        if did and wvid and eid:
            with st.spinner('Loading thumbnail...'):
                thumbnail_content = get_thumbnail_url(did, wv, wvid, eid)
                if thumbnail_content:
                    display_thumbnail(thumbnail_content)
        else:
            st.warning('Please fill in all the required fields.')

if __name__ == "__main__":
    main()
