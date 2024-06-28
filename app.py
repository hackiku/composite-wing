# app.py
import streamlit as st
import pandas as pd
from materials import fibers, matrices
from utils import spacer, set_mpl_style, crop_image, invert_colors
from wing_load_calculator import calculate_wing_load

from material_math.properties import calculate_properties, plot_properties, display_theories, get_property_units
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
from material_math.hooke_law import display_hooke_law_matrices
from material_math.composite_materials import initialize_composite_materials, add_composite_material, display_composite_materials, get_composite_properties


from cad.presets import aircraft_presets, onshape_projects
from cad.cad_ui import cad_ui
# from cad.step_dl import export_step
# from cad.assembly_step import export_step_from_assembly

from femap.wing_load import calc_wing_load

initialize_composite_materials()


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

def initialize_session_state():
    if "current_preset" not in st.session_state:
        st.session_state.current_preset = "P-51"
    if "aircraft_df" not in st.session_state:
        st.session_state.aircraft_df = pd.DataFrame([aircraft_presets[st.session_state.current_preset]])
    if "custom_preset" not in st.session_state:
        st.session_state.custom_preset = False
    if "selected_wing_model" not in st.session_state:
        st.session_state.selected_wing_model = [key for key in aircraft_presets["P-51"]['model'].keys() if key != "project"][0]
    initialize_composite_materials()

initialize_session_state()

def materials_dataframe(fiber_key, matrix_key, fibers, matrices):
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber_key], orient='index', columns=[fiber_key]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix_key], orient='index', columns=[matrix_key]).transpose()
    st.write("##### Fiber + Matrix:")
    st.dataframe(fiber_properties)
    st.dataframe(matrix_properties)


def display_all_materials():
    all_fibers = pd.DataFrame(fibers).transpose()
    all_matrices = pd.DataFrame(matrices).transpose()
    st.write("All Fiber Materials:")
    st.dataframe(all_fibers)
    st.write("All Matrix Materials:")
    st.dataframe(all_matrices)

def on_change_aircraft():
    st.session_state.current_preset = st.session_state.selected_aircraft
    st.session_state.aircraft_df = pd.DataFrame([aircraft_presets[st.session_state.current_preset]])
    st.session_state.custom_preset = False

def on_change_custom():
    st.session_state.custom_preset = True

# Sidebar configuration
st.sidebar.selectbox('Aircraft', options=list(aircraft_presets.keys()), index=0, key='selected_aircraft', on_change=on_change_aircraft)
st.sidebar.write('')
fiber_material_key = st.sidebar.selectbox('Fiber material $$(f)$$', list(fibers.keys()), index=aircraft_presets[st.session_state.current_preset]["materials"]["fiber"], help="Choose the type of fiber material")
matrix_material_key = st.sidebar.selectbox('Matrix material $$(m)$$', list(matrices.keys()), index=aircraft_presets[st.session_state.current_preset]["materials"]["matrix"], help="Choose the type of matrix material")
Vf = st.sidebar.slider('Fiber volume fraction $$(V_{{f}})$$ `Vf`', 0.0, 1.0, aircraft_presets[st.session_state.current_preset]["materials"]["Vf"], 0.01, help="Adjust the fiber volume fraction (between 0 and 1)", on_change=on_change_custom)
Vm = 1 - Vf
Vvoid = st.sidebar.slider('Void space $$(V_{{void}})$$ `Vvoid`', 0.0, 1.0, aircraft_presets[st.session_state.current_preset]["materials"]["Vvoid"], 0.01, help="Adjust void ratio in the composite (between 0 and 1)", on_change=on_change_custom)

if st.sidebar.button("💾 Save material", type="primary"):
    properties = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=False)[0]
    add_composite_material(fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, properties)
    st.sidebar.success(f"Material {fiber_material_key}/{matrix_material_key} added.")

display_composite_materials()

# composite_material dataframe logic. NOTE: we can put st.sidebar bits anywhere in the script, not only beginning.

st.sidebar.button("⤵️ Download Femap Script", type="secondary")

dark_graphs = st.sidebar.checkbox(f"Dark mode", value=True, key='dark_graphs')
graph_style = "dark" if dark_graphs else "light"

theme_mode = set_mpl_style(graph_style)
show_individual_graphs = st.sidebar.checkbox(f"Show graphs", value=False)
show_math = st.sidebar.checkbox("Full math", value=False)

# math_ui()

# Main function
def main():
    # st.write("Prototype an aircraft wing in composite materials. Live CAD model, juicy materials math, export to Femap.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Composite Wingy 🪃")
        st.markdown("""
            Prototype an aircraft wing in composite materials. Will it snap or nope?
            - Live CAD model in Onshape
            - Juicy materials math
            - Export STEP to Simcenter Femap and parse results
            """)
    with col2:
        # st.image("data/logoUniMas.png", use_column_width=True)    
        st.image("data/vaz100.png", use_column_width=False, clamp=False, width=120)
        # st.image("data/mas30.png", use_column_width=True)    
    st.markdown("***")
    # ========== AIRCRAFT ==========
    st.header('1️⃣ Aircraft & Wing')

    aircraft_df = st.session_state.aircraft_df
    
    mass = aircraft_df['specs'][0]['mass']
    wingspan = aircraft_df['specs'][0]['wingspan']
    
    spacer()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"#### **{aircraft_df['specs'][0]['name']}**")
        st.markdown(f"###### {aircraft_df['specs'][0]['manufacturer']}")
        st.metric(label="Mass [kg]", value=mass)
        st.metric(label="Span [m]", value=wingspan)
    with col2:
        image_path = aircraft_df['specs'][0]['3_view']
        three_view = crop_image(image_path, aircraft_df['specs'][0]['crop_params'])
        if dark_graphs:
            three_view = invert_colors(three_view)
        st.image(three_view, caption=f"{aircraft_df['specs'][0]['name']} 3-view", use_column_width=True)

    # CAD Model UI
    cad_ui()

    spacer()

    # =============== WING LOAD ===============
    st.markdown("***")
    st.header("Wing Load Calculation")
    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_mass = st.number_input('Mass of aircraft (kg)', value=aircraft_df['specs'][0]['mass'], step=100.0, on_change=on_change_custom)
        load_factor = st.number_input('Load Factor', value=aircraft_df['specs'][0]['load_factor'], help="The load factor represents the ratio of the maximum load the wing can support to the aircraft's weight. A higher load factor indicates greater structural stress.", on_change=on_change_custom)
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15, on_change=on_change_custom)
        num_ribs = st.number_input('Number of Ribs', value=12, on_change=on_change_custom)
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=aircraft_df['wing'].get('span_wet', 1) * 1000, on_change=on_change_custom)
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20, on_change=on_change_custom)


    calc_wing_load(selected_mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)
    # calculate_wing_load(selected_mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)

    st.markdown("***")
    st.header('2️⃣ Bake composite materials')
    st.write('Now it\'s time to choose the fiber and matrix materials. For faster processing, deselect the Show Graphs option.')
    col1, col2 = st.columns([3, 4])
    with col1:
        st.info('Choose materials & options in the sidebar', icon="👈")

    if st.button("Show all material properties", type="secondary"):
        display_all_materials()

    spacer()
    
    # HOOKE LAW
    
    with st.expander("Hooke's Law"):
        display_hooke_law_matrices()
    
    
    materials_dataframe(fiber_material_key, matrix_material_key, fibers, matrices)

    sigma = {'sigma1': 100, 'sigma2': 50, 'tau12': 30}  # Example values

    micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, micromechanics_theories = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)
    strength_results, strength_latex, strength_math, strength_coefficients, strength_theories = calculate_properties(strength_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)

    st.markdown("***")

    # ------------------ MICROMECH ------------------
    
    st.header("Micromechanical properties")
    st.write("The following properties are calculated using micromechanical models for the combination:")
    col1, col2 = st.columns([6, 4])
    with col1:
        st.code(f"{fiber_material_key} / {matrix_material_key}")
    with col2:
        st.code(f"Vf: {Vf} / Vm: {Vm} / Vvoid: {Vvoid}")
        
    properties = ["E1", "E2", "G12", "ni12", "nu21"]
    units = get_property_units(properties)

    col1, col2 = st.columns([6, 1])
    with col1:
        micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, micromechanics_theories = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)
        micromechanics_df = plot_properties(micromechanics_results, properties, units, micromechanics_theories)

    # with col2:
    st.write(micromechanics_df)

    if st.button("Compare all material combos", type="primary"): 
        # fancy 3D Graph
        st.write("3D Graph")

    st.markdown("***")

    for property_name in properties:
        if property_name in micromech_properties:
            display_theories(property_name, micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, fiber_material_key, fibers[fiber_material_key], matrix_material_key, matrices[matrix_material_key], Vf, Vm, Vvoid, sigma, show_individual_graphs, show_math)
            st.markdown("***")
    
    # def compute_ni21(ni12, E2, E1):
    #     return ni12 * E2 / E1

    # Allow users to select theories for ni12, E1, and E2
    # selected_ni12_theory = st.selectbox("Select theory for ni12", micromechanics_theories['ni12'])
    # selected_E1_theory = st.selectbox("Select theory for E1", micromechanics_theories['E1'])
    # selected_E2_theory = st.selectbox("Select theory for E2", micromechanics_theories['E2'])

    # Get the index of the selected theories
    # ni12_index = micromechanics_theories['ni12'].index(selected_ni12_theory)
    # E1_index = micromechanics_theories['E1'].index(selected_E1_theory)
    # E2_index = micromechanics_theories['E2'].index(selected_E2_theory)

    # Compute ni21 using the selected theory values
    # ni12 = micromechanics_results['ni12'][ni12_index]
    # E2 = micromechanics_results['E2'][E2_index]
    # E1 = micromechanics_results['E1'][E1_index]
    # computed_ni21 = compute_ni21(ni12, E2, E1)

    # Display the computed ni21
    # st.write("Computed ni21:", computed_ni21)

    # Display LaTeX formatted results
    # latex_formula = r"\nu_{21} = \nu_{12} \cdot \frac{E_{2}}{E_{1}}"
    # latex_result = f"\\nu_{{21}} = {ni12:.3f} \\cdot \\frac{{{E2:.3f}}}{{{E1:.3f}}} = {computed_ni21:.3f}"

    # st.latex(latex_formula)
    # st.latex(latex_result)
        
    # st.write(f"{micromechanics_results['E1']} {micromechanics_results['E2']} {micromechanics_results['G12']} {micromechanics_results['ni12']} {micromechanics_results['ni21']}")
    # ------ STRENGTH ------
    st.header("Strength Properties")
    st.write("The following properties are calculated using micromechanical models for the combination:")
    col1, col2 = st.columns([6, 4])
    with col1:
        st.code(f"{fiber_material_key} / {matrix_material_key}")
    with col2:
        st.code(f"Vf: {Vf} / Vm: {Vm} / Vvoid: {Vvoid}")

    properties = ["F1T", "F1C", "F2T", "F2C", "F6"]
    units = get_property_units(properties)

    col1, col2 = st.columns([6, 1])
    with col1:
        strength_df = plot_properties(strength_results, properties, units, strength_theories)
    st.dataframe(strength_df)

    st.markdown("***")

    for property_name in properties:
        if property_name in strength_properties:
            display_theories(property_name, strength_results, strength_latex, strength_math, strength_coefficients, fiber_material_key, fibers[fiber_material_key], matrix_material_key, matrices[matrix_material_key], Vf, Vm, Vvoid, sigma, show_individual_graphs, show_math)


    st.markdown('***')
    st.markdown('***')

    st.header("Failure Criteria")

    st.code(f"Failure Criteria for {fiber_material_key} / {matrix_material_key}")

    # SEE HERE CHATGPT
    # list materials created by user
    st.sidebar.write("AS-4/3501-6 Vf=0.63") 

if __name__ == "__main__":
    main()
