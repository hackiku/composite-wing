# cad/assembly_step.py

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
        'Content-Type': 'application/json',
        'accept': 'application/json;charset=UTF-8; qs=0.09'
    }
    return headers

def validate_step_format():
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/translationformats"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    formats = response.json()
    for format in formats:
        if format["translatorName"].lower() == "step" and format["validDestinationFormat"] and format["couldBeAssembly"]:
            return True
    return False

def initiate_step_export(did, wid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/assemblies/d/{did}/w/{wid}/e/{eid}/translations"
    headers = get_basic_auth_headers()
    data = {
        "allowFaultyParts": True,
        "angularTolerance": 0.001,
        "formatName": "STEP",
        "storeInDocument": False
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()['id']

def check_translation_status(tid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/{tid}"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_step_model(did, wid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/blobelements/d/{did}/w/{wid}/e/{eid}"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    
    if response.headers.get('Content-Type') == 'text/html':
        print(f"HTML Response Content: {response.text}")
        raise Exception("Received HTML instead of the STEP file. Check the URL or authentication.")
    
    response.raise_for_status()
    return response.content

def export_step_from_assembly(did, wid, eid, output_directory='cad/step/'):
    if not validate_step_format():
        raise Exception("STEP format not supported.")

    tid = initiate_step_export(did, wid, eid)
    print(f"Translation ID: {tid}")

    # Poll for the translation status
    while True:
        status = check_translation_status(tid)
        if status['requestState'] == 'DONE':
            if 'resultElementIds' in status and status['resultElementIds']:
                result_element_id = status['resultElementIds'][0]
                break
            else:
                raise Exception("Translation completed but no result element ID found.")
        elif status['requestState'] == 'FAILED':
            raise Exception("STEP export failed.")
        print("Translation in progress...")
        time.sleep(5)  # Wait for 5 seconds before checking again

    step_content = download_step_model(did, wid, result_element_id)
    
    os.makedirs(output_directory, exist_ok=True)
    
    step_file_path = os.path.join(output_directory, f"{eid}.step")
    with open(step_file_path, 'wb') as file:
        file.write(step_content)
    
    return step_file_path

if __name__ == "__main__":
    # Example assembly details
    did = "f6ac5c0b25ce21ecd85991db"
    wid = "2f1903d2edb515536def7421"
    eid = "00d134be28febc6d8fb0e925"

    output_directory = "cad/step/"
    try:
        exported_file = export_step_from_assembly(did, wid, eid, output_directory)
        print(f"Exported STEP file: {exported_file}")
    except Exception as e:
        print(f"Failed to export STEP file: {e}")
