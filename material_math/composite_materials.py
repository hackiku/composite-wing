# material_math/composite_materials.py

import pandas as pd
import streamlit as st

def initialize_composite_materials():
    if 'composite_materials' not in st.session_state:
        st.session_state['composite_materials'] = pd.DataFrame(columns=['Fiber', 'Matrix', 'Vf', 'Vm', 'Vvoid', 'E1', 'E2', 'nu12', 'nu21'])

def add_composite_material(fiber, matrix, Vf, Vm, Vvoid, properties):
    new_material = {
        'Fiber': fiber,
        'Matrix': matrix,
        'Vf': Vf,
        'Vm': Vm,
        'Vvoid': Vvoid,
        'E1': properties['E1'][0],
        'E2': properties['E2'][0],
        'nu12': properties['ni12'][0],
        'nu21': properties['nu21'][0]
    }
    st.session_state['composite_materials'] = st.session_state['composite_materials'].append(new_material, ignore_index=True)

def display_composite_materials():
    st.sidebar.write("### Composite Materials")
    st.sidebar.dataframe(st.session_state['composite_materials'])

# composite_materials.py

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
