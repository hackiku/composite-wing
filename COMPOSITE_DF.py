# material_math/composite_materials.py

import pandas as pd
import streamlit as st

def initialize_composite_materials():
    if 'composite_materials' not in st.session_state:
        st.session_state.composite_materials = {}

def add_composite_material(name, fiber, matrix, Vf, Vm, Vvoid, properties):
    new_material = {
        "fiber": fiber,
        "matrix": matrix,
        "Vf": Vf,
        "Vm": Vm,
        "Vvoid": Vvoid,
        "micromechanics": {
            "E1": {
                "ROM": properties["E1"]["ROM"],
                "Inverse ROM": properties["E1"]["Inverse ROM"],
                "Halpin-Tsai": properties["E1"]["Halpin-Tsai"],
                "Hashin-Rosen": properties["E1"]["Hashin-Rosen"],
                "chosen": "ROM",
            },
            "E2": {
                "ROM": properties["E2"]["ROM"],
                "Inverse ROM": properties["E2"]["Inverse ROM"],
                "Chamis": properties["E2"]["Chamis"],
                "Halpin-Tsai": properties["E2"]["Halpin-Tsai"],
                "Modified IROM": properties["E2"]["Modified IROM"],
                "chosen": "Chamis",
            },
            "G12": {
                "ROM": properties["G12"]["ROM"],
                "MROM": properties["G12"]["MROM"],
                "Chamis": properties["G12"]["Chamis"],
                "Halpin-Tsai": properties["G12"]["Halpin-Tsai"],
                "Hashin-Rosen": properties["G12"]["Hashin-Rosen"],
                "Elasticity": properties["G12"]["Elasticity"],
                "chosen": "ROM",
            },
            "nu12": {
                "ROM": properties["nu12"]["ROM"],
                "Chamis": properties["nu12"]["Chamis"],
                "Halpin-Tsai": properties["nu12"]["Halpin-Tsai"],
                "chosen": "ROM",
            },
            "nu21": {
                "Stiffness matrix symmetry": properties["nu21"]["Stiffness matrix symmetry"],
                "chosen": "Stiffness matrix symmetry",
            }
        },
        "strength": {
            "F1T": {
                "Standard": properties["F1T"]["Standard"],
            },
            "F1C": {
                "Timoshenko-Gere": properties["F1C"]["Timoshenko-Gere"],
                "Rosen": properties["F1C"]["Rosen"],
                "Agarwal-Broutman": properties["F1C"]["Agarwal-Broutman"],
                "chosen": "Timoshenko-Gere",
            },
            "F2T": {
                "Nielsen": properties["F2T"]["Nielsen"],
                "Modified ROM": properties["F2T"]["Modified ROM"],
                "chosen": "Nielsen",
            },
            "F2C": {
                "Weeton": properties["F2C"]["Weeton"],
                "chosen": "Weeton",
            },
            "F6": {
                "Stellbrink": properties["F6"]["Stellbrink"],
                "chosen": "Stellbrink",
            },
        }
    }
    st.session_state.composite_materials[name] = new_material

def display_composite_materials():
    st.sidebar.write("### Composite Materials")
    for name, material in st.session_state.composite_materials.items():
        st.sidebar.write(f"**{name}**")
        st.sidebar.write(material)

def get_composite_properties(material_name):
    if material_name not in st.session_state.composite_materials:
        st.error(f"No composite material found for: {material_name}")
        return None
    return st.session_state.composite_materials[material_name]
