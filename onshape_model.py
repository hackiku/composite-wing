# onshape_model.py

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
