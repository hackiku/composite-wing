# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from materials import fibers, matrices
from utils import spacer
from composite_math.calculations import calculate_properties, plot_properties, display_theories
from composite_math.theories import micromechanics_theories, strength_theories, failure_theories
from onshape_cad.model_ui import model_ui
from wing_load_calculator import calculate_wing_load

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

# ================ SIDEBAR =================    
st.sidebar.markdown('### Choose wing material')
fiber_material_key = st.sidebar.selectbox('Fiber Material', list(fibers.keys()), index=0, help="Choose the type of fiber material")
matrix_material_key = st.sidebar.selectbox('Matrix Material', list(matrices.keys()), index=0, help="Choose the type of matrix material")
Vf = st.sidebar.slider('Fiber Volume Fraction `Vf`', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
Vm = 1 - Vf
Vvoid = st.sidebar.slider('Volume of void space `Vvoid`', 0.0, 1.0, 0.3, 0.01, help="Adjust void ratio in the composite (between 0 and 1)")

theme_mode = st.sidebar.selectbox("Graphs", options=["Dark", "Light"], index=0).lower()
show_individual_graphs = st.sidebar.checkbox("Show Graphs", value=False)
show_math = st.sidebar.checkbox("Show Math", value=False)

def main():
    st.title("Composite Wingy 🪃")
    st.write("Design a wing with composite materials")
    st.write("Visualize and edit a live CAD in Onshape, combine fibers and matrices, export config to Femap with NASTRAN solver.")

    st.markdown("***")

    model_ui()

    spacer()

    # Wing load section
    st.markdown("***")
    st.header("Wing load")
    col1, col2, col3 = st.columns(3)
    with col1:
        mass = st.number_input('Mass of aircraft (kg)', value=11300, step=100)
        load_factor = st.number_input('Load Factor', value=6, help="The load factor represents the ratio of the maximum load the wing can support to the aircraft's weight. A higher load factor indicates greater structural stress.")
        
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15)
        num_ribs = st.number_input('Number of Ribs', value=st.session_state.variables.get('rib_num_total', {}).get('value', 12))
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=st.session_state.variables.get('span', {}).get('value', 1200))
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20)
    
    calculate_wing_load(mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)

    # =================== MATERIALS ===================
    st.markdown("***")
    st.header('2️⃣ Composite materials')
    st.write('Now it\'s time to choose the fiber and matrix materials. For faster processing, deselect the Show Graphs option.')
    st.info('Choose materials & options in the sidebar', icon="👈")

    if st.button("Show all material properties", type="secondary"):
        display_all_materials()

    materials_dataframe(fiber_material_key, matrix_material_key)
    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    # Define properties to calculate
    micromechanics_properties = ["E1_modulus", "E2_modulus", "shear_modulus", "poisson_ratio"]

    # Calculate micromechanics properties
    results_micromechanics, latex_micromechanics, math_micromechanics = calculate_properties(
        micromechanics_theories, micromechanics_properties, fiber_material, matrix_material, Vf, Vm, show_math=show_math
    )

    # Check lengths of arrays in results_micromechanics
    lengths = {key: len(value) for key, value in results_micromechanics.items()}
    st.write("Lengths of arrays in results_micromechanics:", lengths)

    # Ensure all arrays are of the same length
    min_length = min(lengths.values())
    for key in results_micromechanics:
        results_micromechanics[key] = results_micromechanics[key][:min_length]

    # Display micromechanics results and plots
    st.header("👉 Micromechanics properties")
    results_df = pd.DataFrame(results_micromechanics)
    st.dataframe(results_df)
    plot_properties(results_df, theme_mode)
    st.markdown('***')

    for property_name in micromechanics_properties:
        display_theories(property_name, micromechanics_theories, results_micromechanics, latex_micromechanics, math_micromechanics, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid)
        st.markdown('***')

if __name__ == "__main__":
    main()
