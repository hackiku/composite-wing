# material_math/composite_materials.py

import pandas as pd
import streamlit as st

def initialize_composite_materials():
    if 'composite_materials' not in st.session_state:
        default_material = {
            'Fiber': 'Default Fiber',
            'Matrix': 'Default Matrix',
            'Vf': 0.5,
            'Vm': 0.5,
            'Vvoid': 0.0,
            'E1': 100.0,
            'E2': 50.0,
            'nu12': 0.3,
            'nu21': 0.15,
            'G12': 25.0
        }
        st.session_state['composite_materials'] = pd.DataFrame([default_material])

def add_composite_material(fiber, matrix, Vf, Vm, Vvoid, properties):
    new_material = {
        'Fiber': fiber,
        'Matrix': matrix,
        'Vf': Vf,
        'Vm': Vm,
        'Vvoid': Vvoid,
        'E1': properties['E1'][0],
        'E2': properties['E2'][0],
        'nu12': properties['nu12'][0],
        'nu21': properties['nu21'][0],
        'G12': properties['G12'][0]
    }
    new_material_df = pd.DataFrame([new_material])
    st.session_state['composite_materials'] = pd.concat([st.session_state['composite_materials'], new_material_df], ignore_index=True)

def display_composite_materials():
    st.sidebar.write("### Composite Materials")
    st.sidebar.dataframe(st.session_state['composite_materials'])

def get_composite_properties(material_name):
    df = st.session_state['composite_materials']
    if df.empty:
        st.error("Composite materials DataFrame is empty. Please add a material first.")
        return None
    material = df[df['Fiber'] == material_name]
    if material.empty:
        st.error(f"No composite material found for Fiber: {material_name}")
        return None
    return material.iloc[-1].to_dict()
