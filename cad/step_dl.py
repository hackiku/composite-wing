# cad/step_dl.py

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

def get_element_type(did, wv, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/documents/d/{did}/{wv}/e/{eid}"
    headers = get_basic_auth_headers()
    print(f"GET Element Type URL: {url}")  # Debugging statement
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get element type. Response: {response.text}")  # Debugging statement
    response.raise_for_status()
    element = response.json()
    return element['type']

def initiate_export(did, wv, eid, element_type, format_name="STEP"):
    if element_type == 'ASSEMBLY':
        url = f"{ONSHAPE_BASE_URL}/api/v6/assemblies/d/{did}/w/{wv}/e/{eid}/translations"
    else:
        url = f"{ONSHAPE_BASE_URL}/api/v6/partstudios/d/{did}/w/{wv}/e/{eid}/translations"
        
    headers = get_basic_auth_headers()
    data = {
        "formatName": format_name,
        "allowFaultyParts": True,
        "angularTolerance": 0.001,
        "storeInDocument": False
    }
    print(f"Initiating export with URL: {url}, Data: {data}")  # Debugging statement
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f"Failed to initiate export. Response: {response.text}")  # Debugging statement
    response.raise_for_status()
    return response.json()['id']

def check_translation_status(tid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/{tid}"
    headers = get_basic_auth_headers()
    print(f"Checking translation status with URL: {url}")  # Debugging statement
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to check translation status. Response: {response.text}")  # Debugging statement
    response.raise_for_status()
    return response.json()

def download_step_model(did, result_external_data_id):
    url = f"{ONSHAPE_BASE_URL}/documents/d/{did}/externaldata/{result_external_data_id}"
    headers = get_basic_auth_headers()
    print(f"Downloading STEP model with URL: {url}")  # Debugging statement
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 307:
        redirect_url = response.headers['Location']
        response = requests.get(redirect_url, headers=headers)
    if response.headers.get('Content-Type') == 'text/html':
        print(f"HTML Response Content: {response.text}")  # Debugging statement
        raise Exception("Received HTML instead of the STEP file. Check the URL or authentication.")
    response.raise_for_status()
    return response.content

def export_step(did, wv, eid, output_directory='cad/step/'):
    element_type = get_element_type(did, wv, eid)
    tid = initiate_export(did, wv, eid, element_type)
    print(f"Translation ID: {tid}")  # Debugging statement
    while True:
        status = check_translation_status(tid)
        if status['requestState'] == 'DONE':
            if 'resultExternalDataIds' in status and status['resultExternalDataIds']:
                result_external_data_id = status['resultExternalDataIds'][0]
                break
            else:
                raise Exception("Translation completed but no external data URL found.")
        elif status['requestState'] == 'FAILED':
            raise Exception("STEP export failed.")
        print("Translation in progress...")  # Debugging statement
        time.sleep(5)

    step_content = download_step_model(did, result_external_data_id)
    os.makedirs(output_directory, exist_ok=True)
    step_file_path = os.path.join(output_directory, f"{eid}.step")
    with open(step_file_path, 'wb') as file:
        file.write(step_content)
    return step_file_path

if __name__ == "__main__":
    # Example document details
    did = "f6ac5c0b25ce21ecd85991db"
    wv = "w"
    eid = "0f38721b826a5669e2acf9d0"

    output_directory = "cad/step/"
    try:
        exported_file = export_step(did, wv, eid, output_directory)
        print(f"Exported STEP file: {exported_file}")
    except Exception as e:
        print(f"Failed to export STEP file: {e}")
