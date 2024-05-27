# onshape_model.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

ONSHAPE_API_KEY = os.getenv("ONSHAPE_API_KEY")
ONSHAPE_BASE_URL = os.getenv("ONSHAPE_BASE_URL")

def get_headers():
    return {
        'Authorization': f'Bearer {ONSHAPE_API_KEY}',
        'Content-Type': 'application/json'
    }

def load_step_model(document_id, workspace_id, element_id):
    url = f"{ONSHAPE_BASE_URL}/api/documents/d/{document_id}/w/{workspace_id}/e/{element_id}/parasolid"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.content
    else:
        response.raise_for_status()

def change_parameter(document_id, workspace_id, element_id, parameter_id, new_value):
    url = f"{ONSHAPE_BASE_URL}/api/partstudios/d/{document_id}/w/{workspace_id}/e/{element_id}/features/partstudio/parameter/{parameter_id}"
    data = {
        "parameter": {
            "value": new_value
        }
    }
    response = requests.post(url, headers=get_headers(), json=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

