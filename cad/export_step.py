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
    print(f"Auth Headers: {headers}")  # Debug print
    return headers

def validate_step_format():
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/translationformats"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    formats = response.json()
    print(f"Translation Formats: {formats}")  # Debug print
    for format in formats:
        if format["translatorName"].lower() == "step" and format["validDestinationFormat"]:
            return True
    return False

def initiate_step_export(did, wid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/assemblies/d/{did}/w/{wid}/e/{eid}/translations"

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
    print(f"Initiate Export Response: {response.json()}")  # Debug print
    return response.json()['id']

def check_translation_status(tid):
    url = f"{ONSHAPE_BASE_URL}/api/v6/translations/{tid}"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    status = response.json()
    print(f"Translation Status: {status}")  # Debug print
    return status

def download_step_model(document_id, result_external_data_id):
    url = f"{ONSHAPE_BASE_URL}/documents/d/{document_id}/externaldata/{result_external_data_id}"
    headers = get_basic_auth_headers()
    print(f"Download URL: {url}")  # Debug print

    # First request to get the redirect URL
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 307:
        redirect_url = response.headers['Location']
        print(f"Redirect URL: {redirect_url}")  # Debug print
        
        # Follow the redirect URL
        response = requests.get(redirect_url, headers=headers)

    if response.headers.get('Content-Type') == 'text/html':
        print(f"HTML Response Content: {response.text}")  # Debug print
        raise Exception("Received HTML instead of the STEP file. Check the URL or authentication.")
    
    response.raise_for_status()
    print(f"Downloaded Content Type: {response.headers.get('Content-Type')}")  # Debug print
    return response.content

def export_step_from_preset(did, wv, wvid, eid, output_directory='cad/step/'):
    if not validate_step_format():
        raise Exception("STEP format not supported.")
    
    tid = initiate_step_export(did, wv, wvid, eid)
    print(f"Translation ID: {tid}")  # Debug print

    # Poll for the translation status
    while True:
        status = check_translation_status(tid)
        if status['requestState'] == 'DONE':
            if 'resultExternalDataIds' in status and status['resultExternalDataIds']:
                result_external_data_id = status['resultExternalDataIds'][0]
                break
            else:
                raise Exception("Translation completed but no external data URL found.")
        elif status['requestState'] == 'FAILED':
            raise Exception(f"STEP export failed. Reason: {status.get('failureReason', 'Unknown')}")
        print("Translation in progress...")  # Debug print
        time.sleep(5)  # Wait for 5 seconds before checking again

    step_content = download_step_model(did, result_external_data_id)
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    step_file_path = os.path.join(output_directory, f"{eid}.step")
    print(f"Saving STEP file to: {step_file_path}")  # Debug print

    # Write the content to the file
    try:
        with open(step_file_path, 'wb') as file:
            file.write(step_content)
        print(f"STEP file saved: {step_file_path}")  # Debug print
    except IOError as e:
        print(f"Failed to write STEP file: {e}")  # Debug print
        raise e

    return step_file_path

if __name__ == "__main__":
    # Example preset details
    did = "f6ac5c0b25ce21ecd85991db"
    wv = "w"
    wvid = "2f1903d2edb515536def7421"
    eid = "0f38721b826a5669e2acf9d0"
    
    output_directory = "cad/step/"
    try:
        exported_file = export_step_from_preset(did, wv, wvid, eid, output_directory)
        print(f"Exported STEP file: {exported_file}")
    except Exception as e:
        print(f"Failed to export STEP file: {e}")
