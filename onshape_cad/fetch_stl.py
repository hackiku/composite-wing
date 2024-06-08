import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ONSHAPE_ACCESS_KEY = os.getenv("ONSHAPE_ACCESS_KEY")
ONSHAPE_SECRET_KEY = os.getenv("ONSHAPE_SECRET_KEY")
ONSHAPE_BASE_URL = os.getenv("ONSHAPE_BASE_URL")

PRESETS = {
    "Torsion box": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wv": "w",
        "wvid": "2f1903d2edb515536def7421",
        "eid": "1746a09d07c6f27e71172a7f",
        "url": "https://cad.onshape.com/documents/cae4cba9e2f625664baf1122/w/ba81e6382142c773cd7b78ba/e/640a7618098c9be6fe97b244?renderMode=0&uiState=6654e4567ce53e2d5ac81735"
    },
    "Full wing (old)": {
        "did": "f6ac5c0b25ce21ecd85991db",
        "wvid": "2f1903d2edb515536def7421",
        "wv": "w",
        "eid": "b879915fba35863ee60116c6",
        "url": ""
    },
    "Parametric Wing": {
        "did": "308d36ae2431fbf4b9b96a48",
        "wvid": "4dfbfac17da94e7168ec10cd",
        "wv": "w",
        "eid": "1c23a328748cc03fde2f37f5",
        "url": "https://cad.onshape.com/documents/308d36ae2431fbf4b9b96a48/w/4dfbfac17da94e7168ec10cd/e/1c23a328748cc03fde2f37f5"
    },
}

def get_basic_auth_headers():
    credentials = f"{ONSHAPE_ACCESS_KEY}:{ONSHAPE_SECRET_KEY}"
    basic_auth = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        'Authorization': f'Basic {basic_auth}',
        'Content-Type': 'application/json'
    }
    return headers

def initiate_stl_export(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/partstudios/d/{did}/{wv}/{wvid}/e/{eid}/stl?mode=text&grouping=true&scale=1&units=inch"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 307:
        redirect_url = response.headers['Location']
        return redirect_url
    else:
        raise Exception(f"Failed to initiate export: {response.status_code} {response.reason}")

def download_stl_model(redirect_url):
    headers = get_basic_auth_headers()
    response = requests.get(redirect_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download STL model: {response.status_code} {response.reason}")

def fetch_stl(preset_name):
    preset = PRESETS[preset_name]
    redirect_url = initiate_stl_export(preset['did'], preset['wv'], preset['wvid'], preset['eid'])
    stl_content = download_stl_model(redirect_url)
    return stl_content
