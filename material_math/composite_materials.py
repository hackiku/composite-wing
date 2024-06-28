# material_math/composite_materials.py

import pandas as pd
import streamlit as st

def initialize_composite_materials():
    if 'composite_materials_df' not in st.session_state:
        st.session_state['composite_materials_df'] = pd.DataFrame(columns=[
            'Fiber', 'Matrix', 'Vf', 'Vm', 'Vvoid', 'E1', 'E2', 'G12', 'nu12', 'nu21'
        ])

def add_composite_material(fiber, matrix, Vf, Vm, Vvoid, properties):
    new_material = {
        'Fiber': fiber,
        'Matrix': matrix,
        'Vf': Vf,
        'Vm': Vm,
        'Vvoid': Vvoid,
        'E1': properties['E1'][-1],
        'E2': properties['E2'][-1],
        'G12': properties['G12'][-1],
        'nu12': properties['nu12'][-1],
        'nu21': properties['nu21'][-1]
    }
    st.session_state['composite_materials_df'] = st.session_state['composite_materials_df'].append(new_material, ignore_index=True)

def get_composite_properties(material_name):
    df = st.session_state['composite_materials_df']
    material = df[df['Fiber'] == material_name].iloc[-1]
    return material

def display_composite_materials():
    if 'composite_materials_df' in st.session_state:
        st.sidebar.write("### Composite Materials")
        st.sidebar.dataframe(st.session_state['composite_materials_df'])
