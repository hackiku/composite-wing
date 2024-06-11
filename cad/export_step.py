# cad/export_step.py

import os
import requests
import base64
import time
from dotenv import load_dotenv
from cad.onshape_presets import PRESETS

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

def initiate_step_export(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/partstudios/d/{did}/{wv}/{wvid}/e/{eid}/translations"
    headers = get_basic_auth_headers()
    data = {
        "formatName": "STEP",
        "flattenAssemblies": True,
        "yAxisIsUp": True,
        "includeExportIds": True
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception(f"Failed to initiate STEP export: {response.status_code} {response.reason}")

def check_translation_status(translation_id):
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/{translation_id}"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to check translation status: {response.status_code} {response.reason}")

def download_step_model(redirect_url):
    headers = get_basic_auth_headers()
    response = requests.get(redirect_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download STEP model: {response.status_code} {response.reason}")

def export_step_from_preset(preset_name, part_type, output_directory='femap/'):
    preset = PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Preset {preset_name} not found.")
    
    document_id = preset['did']
    workspace_id = preset['wv']
    version_id = preset['wvid']
    element_id = preset['eid'].get(part_type)
    if not element_id:
        raise ValueError(f"Part type {part_type} not found in preset {preset_name}.")
    
    translation_id = initiate_step_export(document_id, workspace_id, version_id, element_id)

    # Poll for the translation status
    while True:
        status = check_translation_status(translation_id)
        if status['requestState'] == 'DONE':
            if 'resultExternalDataIds' in status and status['resultExternalDataIds']:
                redirect_url = status['resultExternalDataIds'][0]['href']
                break
            else:
                raise Exception("Translation completed but no external data URL found.")
        elif status['requestState'] == 'FAILED':
            raise Exception("STEP export failed.")
        time.sleep(5)  # Wait for 5 seconds before checking again

    step_content = download_step_model(redirect_url)
    
    step_file_path = os.path.join(output_directory, f"{element_id}.step")
    with open(step_file_path, 'wb') as file:
        file.write(step_content)
    return step_file_path

if __name__ == "__main__":
    preset_name = "composite_wing"  # Example preset name
    part_type = "Torsion box"  # Example part type
    output_directory = "femap/"
    exported_file = export_step_from_preset(preset_name, part_type, output_directory)
    print(f"Exported STEP file: {exported_file}")
