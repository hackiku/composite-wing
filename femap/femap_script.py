# femap+
import pythoncom
from pyfemap import constants as feConstants
import sys
import win32com.client as win32
import pandas as pd
import numpy as np

# Initialize Femap API connection
try:
    win32.gencache.is_readonly = False
    existObj = pythoncom.connect(feConstants.model.CLSID)
    App = feConstants.model(existObj)
except:
    sys.exit("Femap is not open")

# Function to import CFD data from a CSV file
def impt_cfd_data(f_name):
    df = pd.read_csv(f_name)
    return df

# Example usage of the function
if __name__ == "__main__":
    rc = App.feAppMessage("Python API Started")
    slc_file = r'C:\Users\bzrub\Documents\Python\CFD_results_to_datasurf\PressureData.csv'
    print(slc_file)

    cfd_data = impt_cfd_data(slc_file)
    locs = cfd_data[['X', 'Y', 'Z']]

    num_rows = cfd_data.shape[0]
    p_vals = np.array(cfd_data['Pressure'])
    p_vals = np.stack((p_vals, np.zeros(num_rows), np.zeros(num_rows)))

    pressure_vals = np.array(p_vals).flatten('F')
    xyz_locs = np.array(locs).flatten()

    # Additional processing and applying data to Femap model
    # This part will vary depending on your specific requirements and setup
