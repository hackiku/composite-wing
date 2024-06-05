import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from materials import fibers, matrices
from calculations import calculate_properties, theories
from utils import spacer
import model_playground
import stl_fetch
from stl_show import load_stl, get_model_files
from wing_load_calculator import calculate_wing_load
import inspect
import os

st.set_page_config(
    page_title="Composite Wing",
    page_icon="🪃",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Yay keep it *wingy*",
        'Get Help': 'https://jzro.co'
    }
)

# graph styling
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


# for button
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


def display_theories(property_name, fiber_key, fiber_material, matrix_key, matrix_material, Vf, Vm, show_individual_graphs, theme_mode, latex_results, math_results, show_math):
    set_mpl_style(theme_mode)
    theory_names = [name for name in theories[property_name].keys() if name != "unit"]

    coefficients = {}

    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.header(property_name.replace('_', ' ').title())
    with col2:
        st.write(f'{fiber_key}')
        st.json(fiber_material, expanded=False)
    with col3:
        st.write(f'{matrix_key}')
        st.json(matrix_material, expanded=False)

    if len(theory_names) > 1:
        selected_theory = st.radio(f'Select theory for {property_name.replace("_", " ").title()}', theory_names, horizontal=True, label_visibility="collapsed")
    else:
        selected_theory = theory_names[0]

    theory_details = theories[property_name][selected_theory]
    formula = theory_details['formula']
    latex = latex_results[property_name][selected_theory]
    unit = theories[property_name]['unit']

    if 'coefficients' in theory_details:
        for coeff_name, coeff_details in theory_details['coefficients'].items():
            if 'formula' in coeff_details:
                coeff_value = coeff_details['formula'](fiber_material, matrix_material)
            else:
                coeff_value = coeff_details['default']
            coefficients[coeff_name] = st.number_input(f'{coeff_name} for {selected_theory}', value=coeff_value)
            st.latex(f"{coeff_details['latex']} = {coeff_value}")

    if selected_theory in ["Halpin-Tsai", "Modified Rule of Mixtures (MROM)"]:
        result = formula(fiber_material, matrix_material, Vf, Vm, **coefficients)
    else:
        result = formula(fiber_material, matrix_material, Vf, Vm)

    if show_math:
        st.latex(f"{latex}")
        math = math_results[property_name][selected_theory]
        st.latex(f"{math} = {result:.3f} \\ [{unit}]")
    else:
        st.latex(f"{latex} = {result:.3f} \\ [{unit}]")
    
    formula_code = inspect.getsource(formula)
    st.code(formula_code, language='python')

    if show_individual_graphs:
        vfs = np.linspace(0, 1, 100)
        all_values = {theory: [] for theory in theory_names}
        
        for vf in vfs:
            vm = 1 - vf
            for theory in theory_names:
                coeffs = {}
                if 'coefficients' in theories[property_name][theory]:
                    for coeff_name, coeff_details in theories[property_name][theory]['coefficients'].items():
                        if 'formula' in coeff_details:
                            coeffs[coeff_name] = coeff_details['formula'](fiber_material, matrix_material)
                        else:
                            coeffs[coeff_name] = coeff_details['default']
                if theory in ["Halpin-Tsai", "Modified Rule of Mixtures (MROM)"]:
                    value = theories[property_name][theory]['formula'](fiber_material, matrix_material, vf, vm, **coeffs)
                else:
                    value = theories[property_name][theory]['formula'](fiber_material, matrix_material, vf, vm)
                all_values[theory].append(value)

        fig, ax = plt.subplots(figsize=(12, 6))
        for theory, values in all_values.items():
            ax.plot(vfs, values, label=theory)
        ax.axvline(Vf, color='red', linestyle='--', alpha=0.5, label=f'Current Vf = {Vf}')
        ax.set_title(f'{property_name.replace("_", " ").title()} vs. Fiber Volume Fraction', color='white' if theme_mode == 'dark' else 'black')
        ax.set_xlabel('Fiber Volume Fraction (Vf)', color='white' if theme_mode == 'dark' else 'black')
        ax.set_ylabel(f'{property_name.replace("_", " ").title()} ({unit})', color='white' if theme_mode == 'dark' else 'black')
        ax.legend()
        ax.grid(True, color='gray')
        ax.tick_params(colors='white' if theme_mode == 'dark' else 'black')
        st.pyplot(fig)


# ===============================================================

def main():
    # Sidebar
    
    stl_fetch.main()
    
    
    
    
    
    
    
    
    st.markdown("***")
    
    
    
    st.sidebar.markdown('### Choose wing material')
    
    fiber_material_key = st.sidebar.selectbox('Fiber Material', list(fibers.keys()), index=3, help="Choose the type of fiber material")
    matrix_material_key = st.sidebar.selectbox('Matrix Material', list(matrices.keys()), index=7, help="Choose the type of matrix material")
    
    Vf = st.sidebar.slider('Fiber Volume Fraction `Vf`', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf

    theme_mode = st.sidebar.selectbox("Graphs", options=["Dark", "Light"], index=0).lower()
    show_individual_graphs = st.sidebar.checkbox("Show Graphs", value=False)
    show_math = st.sidebar.checkbox("Show Math", value=False)

    # ----------- end sidebar
    
    st.title("Wingy Business 0.01")
    st.write("Design a composite wing. You can build a parametric wing in Onashape API, calculate composite material properties, and then export STEP to FEMAP for finite elements analysis.")
    st.info('Choose materials in the sidebar', icon="👈")

    st.markdown("***")
    
    # --------------------
    
    st.header('1️⃣ Wing design')
    
    models_path = './models/'
    model_files = get_model_files(models_path)
    
    
    selected_model = st.selectbox("Default STL file", model_files)
    spacer()
    
    
    # =============== MODEL ===============
    col1, col2 = st.columns([1, 4])

    with col1:
        span = st.number_input('Span (mm)', value=1200)
        root = st.number_input('Root (mm)', value=400)
        tip = st.number_input('Tip (mm)', value=100)
        front_sweep = st.number_input('Front Sweep (deg)', value=20)
        rib_inc = st.number_input('Rib Increment (mm)', value=20)

        # Model selection dropdown

    with col2:

        model_path = os.path.join(models_path, selected_model)
        if selected_model:
            fig = load_stl(model_path)
            if fig:
                st.plotly_chart(fig)
    
        st.button("Apply Onshape Parameters")
    
    spacer()
    
    
    with st.expander(label="Onshape stuff", expanded=False):
        model_playground.main()

    st.header("Wing load")

    st.markdown("***") # -------------------
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

    st.markdown("***")  # -------------------

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
        display_theories(property_name, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, show_individual_graphs, theme_mode, latex_results, math_results, show_math)
        st.markdown('***')

if __name__ == "__main__":
    main()
