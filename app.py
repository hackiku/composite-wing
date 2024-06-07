import streamlit as st
import pandas as pd
from materials import fibers, matrices
from utils import spacer
from composite_math.calculations import calculate_properties, plot_properties, display_theories
from composite_math.theories import micromechanics_theories, strength_theories, failure_theories, theory_categories
from stl_fetch import fetch_stl, PRESETS 
from stl_show import load_stl, get_model_files
import onshape_variables
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
fiber_material_key = st.sidebar.selectbox('Fiber Material', list(fibers.keys()), index=3, help="Choose the type of fiber material")
matrix_material_key = st.sidebar.selectbox('Matrix Material', list(matrices.keys()), index=7, help="Choose the type of matrix material")
Vf = st.sidebar.slider('Fiber Volume Fraction `Vf`', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
Vm = 1 - Vf
Vvoid = st.sidebar.slider('Volume of void space `Vvoid`', 0.0, 1.0, 0.3, 0.01, help="Adjust void ratio in the composite (between 0 and 1)")

theme_mode = st.sidebar.selectbox("Graphs", options=["Dark", "Light"], index=0).lower()
show_individual_graphs = st.sidebar.checkbox("Show Graphs", value=False)
show_math = st.sidebar.checkbox("Show Math", value=False)


# ------------------------------------

def main():
    
    if 'stl_model' not in st.session_state:
        st.session_state.stl_model = None
        st.session_state.selected_preset = "None"
        st.session_state.variables = {}

    st.title("Composite Wingy 🪃")
    st.write("Design a wing with composite materials. You can build a parametric wing in Onshap API, calculate composite material properties, and then export STEP to FEMAP for finite elements analysis.")

    st.markdown("***")

    # Wing design and STL model section
    col1, col2 = st.columns([3, 2])
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
        rib_num_total = int(st.session_state.variables.get('rib_num_total', {}).get('value', 12))
        st.write(f"Number of ribs = `{rib_num_total}`")

        if st.button("Update STL model", type="primary"):
            if st.session_state.selected_preset != "None":
                preset = PRESETS[selected_preset]
                updated_variables = {
                    "span": span,
                    "root": root,
                    "tip": tip,
                    "front_sweep": front_sweep,
                    "rib_inc": rib_inc,
                    "rib_num_total": rib_num_total,
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

    # Wing load section
    st.markdown("***")
    st.header("Wing load")
    col1, col2, col3 = st.columns(3)
    with col1:
        mass = st.number_input('Mass of aircraft (kg)', value=11300, step=100)
        load_factor = st.number_input('Load Factor', value=6, help="The load factor represents the ratio of the maximum load the wing can support to the aircraft's weight. A higher load factor indicates greater structural stress.")
        
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15)
        num_ribs = st.number_input('Number of Ribs', value=rib_num_total)
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=span)
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20)
    
    # if st.button('Calculate Load Forces'):
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

    # Failure inputs
    sigma = {"sigma1": 0, "sigma2": 0, "tau12": 0}
    F = {"F1": 0, "F2": 0, "F11": 0, "F22": 0, "F12": 0, "F66": 0}

    # Define properties to calculate
    micromechanics_properties = ["E1_modulus", "E2_modulus", "shear_modulus", "poisson_ratio"]
    strength_properties = ["tensile_strength", "compressive_strength", "transverse_tensile_strength", "transverse_compressive_strength", "in_plane_shear_strength"]
    failure_properties = ["Tsai-Wu", "Tsai-Hill"]

    # Calculate properties for each category
    results_micromechanics, latex_micromechanics, math_micromechanics = calculate_properties(micromechanics_theories, micromechanics_properties, fiber_material, matrix_material, Vf, Vm, show_math)
    results_strength, latex_strength, math_strength = calculate_properties(strength_theories, strength_properties, fiber_material, matrix_material, Vf, Vm, show_math)
    results_failure, latex_failure, math_failure = calculate_properties(failure_theories, failure_properties, fiber_material, matrix_material, Vf, Vm, show_math)


    # Combine results
    results_combined = {
        "Micromechanics": results_micromechanics,
        "Strength": results_strength,
        "Failure Theories": results_failure
    }
    latex_combined = {
        "Micromechanics": latex_micromechanics,
        "Strength": latex_strength,
        "Failure Theories": latex_failure
    }
    math_combined = {
        "Micromechanics": math_micromechanics,
        "Strength": math_strength,
        "Failure Theories": math_failure
    }

    # Display results and plots for each category
    for category, properties in [("Micromechanics", micromechanics_properties), ("Strength", strength_properties), ("Failure Theories", failure_properties)]:
        st.subheader(f"Calculated Properties by {category}")
        results_df = pd.DataFrame(results_combined[category])
        st.dataframe(results_df)
        plot_properties(results_df, theme_mode)
        st.markdown('***')
        
        for property_name in properties:
            display_theories(property_name, micromechanics_theories if category == "Micromechanics" else strength_theories if category == "Strength" else failure_theories, results_combined[category], latex_combined[category], math_combined[category], fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid, show_individual_graphs, theme_mode, show_math)
            st.markdown('***')

if __name__ == "__main__":
    main()
