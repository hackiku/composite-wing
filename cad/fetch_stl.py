# cad/fetch_stl.py

import os
import requests
import base64
from dotenv import load_dotenv

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

def initiate_stl_export(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v5/partstudios/d/{did}/{wv}/{wvid}/e/{eid}/stl?mode=text&scale=1"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 307:
        return response.headers['Location']
    else:
        raise Exception(f"Failed to initiate export: {response.status_code} {response.reason}")

def download_stl_model(redirect_url):
    headers = get_basic_auth_headers()
    response = requests.get(redirect_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download STL model: {response.status_code} {response.reason}")

def fetch_stl(did, wv, wvid, eid):
    redirect_url = initiate_stl_export(did, wv, wvid, eid)
    return download_stl_model(redirect_url)
