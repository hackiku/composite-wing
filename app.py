# app.py

import streamlit as st
import pandas as pd
from materials import fibers, matrices
from utils import spacer, set_mpl_style, crop_image
from onshape_cad.model_ui import model_ui
from wing_load_calculator import calculate_wing_load
from material_math.properties import calculate_properties, plot_properties, display_theories, get_property_units
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
from cad.export_step import export_step_from_preset
from cad.onshape_presets import PRESETS


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
# data/North_American_P-51B_Mustang_3-view_line_drawing.png

aircraft_presets = {
    "P-51 Mustang": {
        "mass": 5489.00,
        "wingspan": 5.643, # 11.286 / 2 [m]
        "tip": 1.297,
        "root": 2.752,
        "sweep_angle": 10.388,
        "3_view": "data/North_American_P-51B_Mustang_3-view_line_drawing.png",
        "crop_params": [100, 200, 200, 200],
        "load_factor": 10
    },
    "J-22 Orao": {
        "mass": 11300.00,
        "wingspan": 9.262,
        "tip": 1.297,
        "root": 2.752,
        "sweep_angle": 12.0,
        "3_view": "",
        "crop_params": [400, 200, 200, 200],
        "load_factor": 10
    }
}


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

# ================= SIDEBAR ====================
selected_aircraft = st.sidebar.selectbox('$$Aircraft$$', options=["P-51 Mustang", "Coming soon..."], index=0)
st.sidebar.markdown('')

fiber_material_key = st.sidebar.selectbox('Fiber material $$(f)$$', list(fibers.keys()), index=0, help="Choose the type of fiber material")
matrix_material_key = st.sidebar.selectbox('Matrix material $$(m)$$', list(matrices.keys()), index=0, help="Choose the type of matrix material")
# matrix_material_key = st.sidebar.selectbox('$$m$$ Matrix material', list(matrices.keys()), index=0, help="Choose the type of matrix material")
Vf = st.sidebar.slider('Fiber volume fraction $$(V_{{f}})$$ `Vf`', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
Vm = 1 - Vf
Vvoid = st.sidebar.slider('Void space $$(V_{{void}})$$ `Vvoid`', 0.0, 1.0, 0.3, 0.01, help="Adjust void ratio in the composite (between 0 and 1)")

preset_name = "composite_wing"
part_type = st.sidebar.selectbox("Select Part Type", options=list(PRESETS[preset_name]['eid'].keys()))

if st.sidebar.button(f"Download {part_type} STEP 💾"):
    try:
        output_directory = 'femap/'
        exported_file = export_step_from_preset(preset_name, part_type, output_directory)
        st.sidebar.success(f"Exported STEP file: {exported_file}")
    except Exception as e:
        st.sidebar.error(f"Failed to export STEP file: {e}")

st.sidebar.markdown('---')
# st.sidebar.markdown(r'$$_{Options}$$')

theme_mode = set_mpl_style(st.sidebar.selectbox("Graph theme", options=["Dark", "Light"], index=0).lower())
show_individual_graphs = st.sidebar.checkbox("Show Graphs", value=False)
show_math = st.sidebar.checkbox("Show Math", value=False)



# ---------------------------------
def main():
    st.title("Composite Wingy 🪃")
    st.write("Design a wing with composite materials")
    st.write("Visualize and edit a live CAD in Onshape, combine fibers and matrices, export config to Femap with NASTRAN solver.")

    st.markdown("***")


    # TODO convert to dataframe
    if selected_aircraft:
        aircraft = aircraft_presets[selected_aircraft]
        mmax = aircraft['mass']
        wingspan = aircraft['wingspan']
        sweep_angle = aircraft['sweep_angle']
        image_path = aircraft['3_view']

        # Display the selected aircraft's details
        st.write(f"### Aircraft: {selected_aircraft}")
        st.write(f"**Mass**: {mmax} kg")
        st.write(f"**Wingspan**: {wingspan} m")
        st.write(f"**Sweep Angle**: {sweep_angle} degrees")

        three_view = crop_image(image_path, aircraft['crop_params'])
        st.image(three_view, caption=f"{selected_aircraft} 3-view")
    else:
        mmax = 999.0

    # =============== CAD MODEL ===============
    model_ui()

    spacer()

    # =============== WING LOAD ===============

    st.markdown("***")
    st.header("Wing load")
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        # mass = st.slider(f'Aircraft mass $$(m_{{max}})$$ [Kg]', 0.0, 10000.0, 5579.18, 0.01, format="%d", help="Adjust void ratio in the composite (between 0 and 1)")
        selected_mass = st.number_input('Mass of aircraft (kg)', value=mmax, step=100.0)
        mass = selected_mass
        load_factor = st.number_input('Load Factor', value=6, help="The load factor represents the ratio of the maximum load the wing can support to the aircraft's weight. A higher load factor indicates greater structural stress.")
        
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15)
        num_ribs = st.number_input('Number of Ribs', value=st.session_state.variables.get('rib_num_total', {}).get('value', 12.0))
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=st.session_state.variables.get('span', {}).get('value', 1200))
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20)
    
    calculate_wing_load(mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)

    st.markdown("***")
    st.header('2️⃣ Composite materials')
    st.write('Now it\'s time to choose the fiber and matrix materials. For faster processing, deselect the Show Graphs option.')
    st.info('Choose materials & options in the sidebar', icon="👈")

    if st.button("Show all material properties", type="secondary"):
        display_all_materials()

    materials_dataframe(fiber_material_key, matrix_material_key, fibers, matrices)

    sigma = {'sigma1': 100, 'sigma2': 50, 'tau12': 30}  # Example values, adjust as needed

    # Update the unpacking to handle the additional returned value
    
    micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, micromechanics_theories = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)
    strength_results, strength_latex, strength_math, strength_coefficients, strength_theories = calculate_properties(strength_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)
    # failure_results, failure_latex, failure_math = calculate_failure(fibers, matrices, fiber_material_key, matrix_material_key, sigma, show_math=show_math)
        
    # ------ MICROMECH ------
    st.header("Micromechanical properties")

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
    st.header("Strength properties")
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

    # for property_name in properties:
    #     micromechanics.display_theories(property_name, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, show_individual_graphs, theme_mode, latex_results, math_results, show_math)
    #     st.markdown('***')


    st.header("Failure criteria")

    st.markdown('***')
    
    
if __name__ == "__main__":
    main()
