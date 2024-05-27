import streamlit as st
import os
import requests
import hashlib
import hmac
import base64
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

ONSHAPE_ACCESS_KEY = os.getenv("ONSHAPE_ACCESS_KEY")
ONSHAPE_SECRET_KEY = os.getenv("ONSHAPE_SECRET_KEY")
ONSHAPE_BASE_URL = os.getenv("ONSHAPE_BASE_URL")

def get_headers(method, url, content_type='application/json'):
    nonce = os.urandom(16).hex()
    auth_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query

    string_to_sign = f"{method}\n{nonce}\n{auth_date}\n{content_type}\n{path}\n{query}".lower()
    signature = hmac.new(
        ONSHAPE_SECRET_KEY.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()

    signature_b64 = base64.b64encode(signature).decode('utf-8')
    authorization = f"On {ONSHAPE_ACCESS_KEY}:HmacSHA256:{signature_b64}"

    return {
        'Authorization': authorization,
        'Date': auth_date,
        'Content-Type': content_type,
        'On-Nonce': nonce
    }

def get_document(document_id):
    url = f"{ONSHAPE_BASE_URL}/api/documents/{document_id}"
    headers = get_headers("GET", url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def display_document_info(document):
    st.write("Document Name:", document['name'])
    st.write("Created At:", document['createdAt'])
    st.write("Modified At:", document['modifiedAt'])
    st.write("Owner:", document['owner']['name'])
    st.write("Thumbnails:")
    for thumbnail in document['thumbnail']['sizes']:
        st.image(thumbnail['href'], caption=f"Size: {thumbnail['size']}")

def main():
    st.header('Onshape Model Integration')
    col1, col2 = st.columns(2)
    with col1:
        document_id = st.text_input('Document ID', '308d36ae2431fbf4b9b96a48')
        workspace_id = st.text_input('Workspace ID', '4dfbfac17da94e7168ec10cd')
        element_id = st.text_input('Element ID', '1c23a328748cc03fde2f37f5')
    with col2:
        parameter_id = st.text_input('Parameter ID', '')
        new_value = st.text_input('New Value', '')

    if st.button('Load Document'):
        try:
            document = get_document(document_id)
            st.write('Document Loaded Successfully')
            display_document_info(document)
        except Exception as e:
            st.error(f"Error loading document: {e}")

if __name__ == "__main__":
    main()
