# app.py

import streamlit as st
import pandas as pd
from materials import fibers, matrices
from utils import spacer, materials_dataframe, set_mpl_style
from onshape_cad.model_ui import model_ui
from wing_load_calculator import calculate_wing_load # root
from material_math.math_ui import materials_ui
from material_math.calculate_properties import calculate_properties, plot_properties, display_theories
from material_math.formulas import micromech_properties

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

# set_mpl_style(theme_mode)

# =========================================================

def main():
    st.title("Composite Wingy 🪃")
    st.write("Design a wing with composite materials")
    st.write("Visualize and edit a live CAD in Onshape, combine fibers and matrices, export config to Femap with NASTRAN solver.")

    st.markdown("***")

    # ------------------ CAD MODEL -------------------
    model_ui()

    spacer()

    # -------  Wing load section
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

    materials_ui(fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math, theme_mode)


if __name__ == "__main__":
    main()
