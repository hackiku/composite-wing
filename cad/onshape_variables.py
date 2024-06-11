# cad/onshape_variables.py

import requests
import os
import base64
from dotenv import load_dotenv
import re

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

def extract_and_convert_values(variables):
    variable_dict = {}
    for var_table in variables:
        for var in var_table['variables']:
            value = var['value']
            if value:
                match = re.match(r"(-?[0-9.]+)", value)
                if match:
                    value = float(match.group(1))
                    if var['type'] == 'LENGTH':
                        # Convert to millimeters if in meters
                        if 'meter' in var['value']:
                            value *= 1000
                    elif var['type'] == 'ANGLE':
                        # Convert to degrees if in radians
                        if 'radian' in var['value']:
                            value *= (180 / 3.141592653589793)
            variable_dict[var['name']] = {
                "type": var['type'],
                "value": value,
                "expression": var['expression'],
                "description": var['description']
            }
    return variable_dict

def fetch_onshape_variables(did, wv, wvid, eid):
    url = f"{ONSHAPE_BASE_URL}/api/variables/d/{did}/{wv}/{wvid}/e/{eid}/variables?includeValuesAndReferencedVariables=true"
    headers = get_basic_auth_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        variables = response.json()
        return extract_and_convert_values(variables)
    else:
        raise Exception(f"Failed to fetch custom variables: {response.status_code} {response.reason}")

def update_custom_variables(did, wv, wvid, eid, variables):
    url = f"{ONSHAPE_BASE_URL}/api/variables/d/{did}/{wv}/{wvid}/e/{eid}/variables"
    headers = get_basic_auth_headers()
    response = requests.post(url, headers=headers, json=variables)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to update custom variables: {response.status_code} {response.reason}")
