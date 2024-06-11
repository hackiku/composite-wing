# app.py

import streamlit as st
import pandas as pd
from materials import fibers, matrices
from utils import spacer, set_mpl_style, crop_image
from wing_load_calculator import calculate_wing_load
from material_math.properties import calculate_properties, plot_properties, display_theories, get_property_units
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
# cad
from cad.presets import aircraft_presets, onshape_projects
from cad.export_step import export_step_from_preset
from cad.onshape_presets import PRESETS
from cad.cad_ui import cad_ui
# from onshape_cad.model_ui import model_ui


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

def materials_dataframe(fiber_key, matrix_key, fibers, matrices):
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber_key], orient='index', columns=[fiber_key]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix_key], orient='index', columns=[matrix_key]).transpose()
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

def compose_onshape_url(presets, selected_preset, part_type, eid):
    did = presets[selected_preset]['did']
    wv = presets[selected_preset]['wv']
    wvid = presets[selected_preset]['wvid']
    return f"https://cad.onshape.com/documents/{did}/{wv}/{wvid}/e/{eid}"

# Sidebar configuration
fiber_material_key = st.sidebar.selectbox('Fiber material $$(f)$$', list(fibers.keys()), index=0, help="Choose the type of fiber material")
matrix_material_key = st.sidebar.selectbox('Matrix material $$(m)$$', list(matrices.keys()), index=0, help="Choose the type of matrix material")
Vf = st.sidebar.slider('Fiber volume fraction $$(V_{{f}})$$ `Vf`', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
Vm = 1 - Vf
Vvoid = st.sidebar.slider('Void space $$(V_{{void}})$$ `Vvoid`', 0.0, 1.0, 0.3, 0.01, help="Adjust void ratio in the composite (between 0 and 1)")

selected_preset = st.sidebar.selectbox("Select Preset", options=["None"] + list(onshape_projects.keys()))
if selected_preset != "None":
    part_type = st.sidebar.selectbox("Select Part Type", options=list(onshape_projects[selected_preset]['eid'].keys()))
    eid = onshape_projects[selected_preset]['eid'][part_type]

    if st.sidebar.button(f"💾 {part_type} STEP"):
        try:
            output_directory = 'femap/'
            did = onshape_projects[selected_preset]['did']
            wv = onshape_projects[selected_preset]['wv']
            wvid = onshape_projects[selected_preset]['wvid']
            exported_file = export_step_from_preset(did, wv, wvid, eid, output_directory)
            st.sidebar.success(f"Exported STEP file: {exported_file}")
        except Exception as e:
            st.sidebar.error(f"Failed to export STEP file: {e}")

    # Display the Onshape URL for the selected part
    part_url = compose_onshape_url(onshape_projects, selected_preset, part_type, eid)
    st.sidebar.markdown(f"[Onshape URL →]({part_url})")

st.sidebar.markdown('---')

theme_mode = set_mpl_style(st.sidebar.selectbox("Graph theme", options=["Dark", "Light"], index=0).lower())
show_individual_graphs = st.sidebar.checkbox("Show graphs", value=False)
show_math = st.sidebar.checkbox("Full math", value=False)

# Main Function
def main():
    st.title("Composite Wingy 🪃")
    st.write("Prototype an aircraft wing in composite materials. Live CAD model, juicy materials math, export to Femap.")

    st.markdown("***")

    # ========== AIRCRAFT ==========
    st.header('Aircraft & Wing Specifications')

    col1, col2 = st.columns(2)
    with col1:
        selected_aircraft = st.selectbox('Select Aircraft', options=list(aircraft_presets.keys()), index=0)
    with col2:
        st.selectbox('Select Wing Type', options=["Box", "Wing"], index=0)
        st.select_slider('Max Mach Number', options=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], value=0.8, key='mmax', help="The maximum Mach number the aircraft can reach")   
    if selected_aircraft:
        aircraft = aircraft_presets[selected_aircraft]
        specs_df = pd.DataFrame([aircraft["specs"]])
        wing_df = pd.DataFrame([aircraft["wing"]])
        
        st.color_picker('Select Color', value='#ff0000', key='color')
        
        st.write(f"### Aircraft: {selected_aircraft}")
        st.write("**Specifications**")
        st.dataframe(specs_df)
        st.write("**Wing Geometry**")
        st.dataframe(wing_df)

        image_path = aircraft['specs']['3_view']
        three_view = crop_image(image_path, aircraft['specs']['crop_params'])
        st.image(three_view, caption=f"{selected_aircraft} 3-view")
    else:
        mmax = 999.0

    # =============== CAD MODEL ===============
    cad_ui()

    spacer()

    # =============== WING LOAD ===============
    st.markdown("***")
    st.header("Wing Load Calculation")
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_mass = st.number_input('Mass of aircraft (kg)', value=aircraft['specs']['mass'], step=100.0)
        load_factor = st.number_input('Load Factor', value=aircraft['specs']['load_factor'], help="The load factor represents the ratio of the maximum load the wing can support to the aircraft's weight. A higher load factor indicates greater structural stress.")
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15)
        num_ribs = st.number_input('Number of Ribs', value=12)
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=aircraft['wing']['span_wet'] * 1000)
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20)
    
    calculate_wing_load(selected_mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)

    st.markdown("***")
    st.header('Composite Materials Selection')
    st.write('Now it\'s time to choose the fiber and matrix materials. For faster processing, deselect the Show Graphs option.')
    st.info('Choose materials & options in the sidebar', icon="👈")

    if st.button("Show all material properties", type="secondary"):
        display_all_materials()

    materials_dataframe(fiber_material_key, matrix_material_key, fibers, matrices)

    sigma = {'sigma1': 100, 'sigma2': 50, 'tau12': 30}  # Example values, adjust as needed

    micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, micromechanics_theories = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)
    strength_results, strength_latex, strength_math, strength_coefficients, strength_theories = calculate_properties(strength_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)

    # ------ MICROMECH ------
    st.header("Micromechanical Properties")
    properties = ["E1", "E2", "G12", "nu12"]
    units = get_property_units(properties)

    col1, col2 = st.columns([3, 2])
    with col1:
        micromechanics_df = plot_properties(micromechanics_results, properties, units, micromechanics_theories)
    with col2:
        st.write(micromechanics_df)

    st.markdown("***")

    for property_name in properties:
        if property_name in micromech_properties:
            display_theories(property_name, micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, fiber_material_key, fibers[fiber_material_key], matrix_material_key, matrices[matrix_material_key], Vf, Vm, Vvoid, sigma, show_individual_graphs, show_math)
            st.markdown("***")

    # ------ STRENGTH ------
    st.header("Strength Properties")
    properties = ["F1T", "F1C", "F2T", "F2C", "F6"]
    units = get_property_units(properties)

    col1, col2 = st.columns([3, 2])
    with col1:
        strength_df = plot_properties(strength_results, properties, units, strength_theories)
    with col2:
        st.dataframe(strength_df)

    st.markdown("***")

    for property_name in properties:
        if property_name in strength_properties:
            display_theories(property_name, strength_results, strength_latex, strength_math, strength_coefficients, fiber_material_key, fibers[fiber_material_key], matrix_material_key, matrices[matrix_material_key], Vf, Vm, Vvoid, sigma, show_individual_graphs, show_math)

    st.header("Failure Criteria")
    st.markdown('***')

if __name__ == "__main__":
    main()