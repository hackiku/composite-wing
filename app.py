import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from materials import fibers, matrices
from calculations import calculate_properties
from utils import spacer
from stl_fetch import fetch_stl, PRESETS 
from stl_show import load_stl, get_model_files
import onshape_variables  # Updated import
import micromechanics
from wing_load_calculator import calculate_wing_load
import inspect
import os

st.set_page_config(
    page_title="Composite Wing",
    page_icon="🪃",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Keep it *wingy*",
        'Get Help': 'https://jzro.co'
    }
)

def set_mpl_style(theme_mode):
    if theme_mode == "dark":
        mplstyle.use('dark_background')
    else:
        mplstyle.use('default')

def materials_dataframe(fiber, matrix):
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber], orient='index', columns=[fiber]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix], orient='index', columns=[matrix]).transpose()
    st.write("Selected Fiber Material Properties:")
    st.dataframe(fiber_properties)
    st.write("Selected Matrix Material Properties:")
    st.dataframe(matrix_properties)

def display_all_materials():
    all_fibers = pd.DataFrame(fibers).transpose()
    all_matrices = pd.DataFrame(matrices).transpose()
    st.write("All Fiber Materials:")
    st.dataframe(all_fibers)
    st.write("All Matrix Materials:")
    st.dataframe(all_matrices)

def plot_properties(results_df, theme_mode):
    set_mpl_style(theme_mode)
    results_df = results_df.set_index("Property").transpose()
    fig, ax = plt.subplots(figsize=(12, 8))
    for property_name in results_df.columns:
        ax.scatter(results_df.index, results_df[property_name], label=property_name)
    ax.set_title('Comparison of Composite Properties by Theory', color='white' if theme_mode == 'dark' else 'black')
    ax.set_xlabel('Theory', color='white' if theme_mode == 'dark' else 'black')
    ax.set_ylabel('Value', color='white' if theme_mode == 'dark' else 'black')
    ax.legend()
    ax.grid(True, color='gray')
    ax.tick_params(colors='white' if theme_mode == 'dark' else 'black')
    st.pyplot(fig)

# ===============================================================

def main():
    if 'stl_model' not in st.session_state:
        st.session_state.stl_model = None
        st.session_state.selected_preset = "None"
        st.session_state.variables = {}

    st.sidebar.markdown('### Choose wing material')
    fiber_material_key = st.sidebar.selectbox('Fiber Material', list(fibers.keys()), index=3, help="Choose the type of fiber material")
    matrix_material_key = st.sidebar.selectbox('Matrix Material', list(matrices.keys()), index=7, help="Choose the type of matrix material")
    Vf = st.sidebar.slider('Fiber Volume Fraction `Vf`', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf
    theme_mode = st.sidebar.selectbox("Graphs", options=["Dark", "Light"], index=0).lower()
    show_individual_graphs = st.sidebar.checkbox("Show Graphs", value=False)
    show_math = st.sidebar.checkbox("Show Math", value=False)

    st.title("Wingy Business 0.01")
    st.write("Design a composite wing. You can build a parametric wing in Onshap API, calculate composite material properties, and then export STEP to FEMAP for finite elements analysis.")
    st.info('Choose materials in the sidebar', icon="👈")

    st.markdown("***")


    col1, col2 = st.columns([3,2])
    with col1:
        st.header('1️⃣ Wing design')

    with col2:
        selected_preset = st.selectbox("Onshape Presets", ["None"] + list(PRESETS.keys()))
        if selected_preset != "None" and st.session_state.selected_preset != selected_preset:
            st.session_state.selected_preset = selected_preset
            with st.spinner('Fetching STL model and variables...'):
                try:
                    stl_content = fetch_stl(selected_preset)
                    stl_path = f"/tmp/{selected_preset}_model.stl"
                    with open(stl_path, 'wb') as f:
                        f.write(stl_content)
                    st.session_state.stl_model = load_stl(stl_path)
                    preset = PRESETS[selected_preset]
                    st.session_state.variables = onshape_variables.fetch_custom_variables(preset["did"], preset["wv"], preset["wvid"], preset["eid"])
                except Exception as e:
                    st.error(f"Error: {e}")



    col1, col2 = st.columns([1, 4])
    with col1:
        spacer('2em')
        span = st.number_input('Span (mm)', value=st.session_state.variables.get('span', {}).get('value', 1200))
        root = st.number_input('Root (mm)', value=st.session_state.variables.get('root', {}).get('value', 400))
        tip = st.number_input('Tip (mm)', value=st.session_state.variables.get('tip', {}).get('value', 100))
        front_sweep = st.number_input('Front Sweep (deg)', value=st.session_state.variables.get('wing_sweep', {}).get('value', 20))
        rib_inc = st.number_input('Rib Increment (mm)', value=st.session_state.variables.get('rib_inc', {}).get('value', 20))

        if st.button("Apply Parameters"):
            if st.session_state.selected_preset != "None":
                preset = PRESETS[selected_preset]
                updated_variables = {
                    "span": span,
                    "root": root,
                    "tip": tip,
                    "front_sweep": front_sweep,
                    "rib_inc": rib_inc
                }
                try:
                    onshape_variables.update_custom_variables(preset["did"], preset["wv"], preset["wvid"], preset["eid"], updated_variables)
                    st.success("Parameters applied and model updated.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("No Onshape preset selected.")

    with col2:
        if st.session_state.stl_model:
            st.plotly_chart(st.session_state.stl_model)

    st.json(st.session_state.variables, expanded=False)

    spacer()

    st.header("Wing load")
    st.markdown("***")
    col1, col2, col3 = st.columns(3)
    with col1:
        mass = st.number_input('Mass of aircraft (kg)', value=11300)
        load_factor = st.number_input('Load Factor', value=6)
        st.button("Update Onshape Model")
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15)
        num_ribs = st.number_input('Number of Ribs', value=12)
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=3821.4)
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20)
    st.markdown('***')
    
    if st.button('Calculate Load Forces'):
        calculate_wing_load(mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)

    st.markdown("***")
    st.subheader('2️⃣ Choose composite materials')
    if st.button("Show all materials", type="secondary"):
        display_all_materials()
    materials_dataframe(fiber_material_key, matrix_material_key)
    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]
    results, latex_results, math_results = calculate_properties(fiber_material, matrix_material, Vf, Vm, show_math)
    max_len = max(len(results[theory]) for theory in results if theory != "Property")
    for theory in results:
        if theory != "Property" and len(results[theory]) < max_len:
            results[theory].extend([None] * (max_len - len(results[theory])))
    results_df = pd.DataFrame(results)
    st.subheader("Calculated Properties by Theory")
    st.dataframe(results_df)
    plot_properties(results_df, theme_mode)
    st.markdown('***')

    properties = ["E1_modulus", "E2_modulus", "shear_modulus", "poisson_ratio", 
                  "tensile_strength", "compressive_strength", 
                  "transverse_tensile_strength", "transverse_compressive_strength",
                  "in_plane_shear_strength"]
    for property_name in properties:
        micromechanics.display_theories(property_name, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, show_individual_graphs, theme_mode, latex_results, math_results, show_math)
        st.markdown('***')

if __name__ == "__main__":
    main()
