# cad/export_step.py

import os
import requests
import base64
import time
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

def validate_step_format():
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/translationformats"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    formats = response.json()
    for format in formats:
        if format["translatorName"].lower() == "step" and format["validDestinationFormat"]:
            return True
    return False

def initiate_step_export(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/partstudios/d/{did}/{wv}/{wvid}/e/{eid}/translations"
    headers = get_basic_auth_headers()
    data = {
        "formatName": "STEP",
        "flattenAssemblies": True,
        "yAxisIsUp": True,
        "includeExportIds": True,
        "storeInDocument": False,
        "resolution": "fine",
        "stepParasolidPreprocessingOption": "NO_PRE_PROCESSING",
        "stepVersionString": "AP203",
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()['id']

def check_translation_status(translation_id):
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/{translation_id}"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_step_model(document_id, result_external_data_id):
    url = f"{ONSHAPE_BASE_URL}/documents/d/{document_id}/externaldata/{result_external_data_id}"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers, allow_redirects=True)
    
    if response.headers.get('Content-Type') == 'text/html':
        raise Exception("Received HTML instead of the STEP file. Check the URL or authentication.")
    
    response.raise_for_status()
    print(response)
    return response.content

def export_step_from_preset(did, wv, wvid, eid, output_directory='femap/'):
    if not validate_step_format():
        raise Exception("STEP format not supported.")
    
    translation_id = initiate_step_export(did, wv, wvid, eid)

    # Poll for the translation status
    while True:
        status = check_translation_status(translation_id)
        if status['requestState'] == 'DONE':
            if 'resultExternalDataIds' in status and status['resultExternalDataIds']:
                result_external_data_id = status['resultExternalDataIds'][0]
                break
            else:
                raise Exception("Translation completed but no external data URL found.")
        elif status['requestState'] == 'FAILED':
            raise Exception("STEP export failed.")
        time.sleep(5)  # Wait for 5 seconds before checking again

    step_content = download_step_model(did, result_external_data_id)
    
    step_file_path = os.path.join(output_directory, f"{eid}.step")
    with open(step_file_path, 'wb') as file:
        file.write(step_content)
    return step_file_path

if __name__ == "__main__":
    # Example preset details
    did = "f6ac5c0b25ce21ecd85991db"
    wv = "w"
    wvid = "2f1903d2edb515536def7421"
    eid = "0f38721b826a5669e2acf9d0"
    
    output_directory = "femap/"
    try:
        exported_file = export_step_from_preset(did, wv, wvid, eid, output_directory)
        print(f"Exported STEP file: {exported_file}")
    except Exception as e:
        print(f"Failed to export STEP file: {e}")
