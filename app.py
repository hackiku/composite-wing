import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from materials import fibers, matrices
from calculations import calculate_properties, theories
import inspect
from onshape_model import load_step_model, change_parameter

mplstyle.use('dark_background')

def spacer(height='2em'):
    st.markdown(f'<div style="margin: {height};"></div>', unsafe_allow_html=True)

def materials_dataframe(fiber, matrix):
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber], orient='index', columns=[fiber]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix], orient='index', columns=[matrix]).transpose()
    st.write("Selected Fiber Material Properties:")
    st.dataframe(fiber_properties)
    st.write("Selected Matrix Material Properties:")
    st.dataframe(matrix_properties)

def plot_properties(results_df):
    results_df = results_df.set_index("Property").transpose()
    fig, ax = plt.subplots(figsize=(12, 8))
    for property_name in results_df.columns:
        ax.plot(results_df.index, results_df[property_name], marker='o', label=property_name)
    ax.set_title('Comparison of Composite Properties by Theory', color='white')
    ax.set_xlabel('Theory', color='white')
    ax.set_ylabel('Value', color='white')
    ax.legend()
    ax.grid(True, color='gray')
    ax.tick_params(colors='white')
    st.pyplot(fig)

def display_theories(property_name, fiber_key, fiber_material, matrix_key, matrix_material, Vf, Vm):
    theory_names = list(theories[property_name].keys())

    col1, col2, col3 = st.columns([3,1,1])
    with col1:
        st.subheader(property_name.replace('_', ' ').title())
    with col2:
        # st.write(f'{fiber_key}')
        st.json(fiber_material, expanded=False)
    with col3:
        # st.write(f'{matrix_key}')
        st.json(matrix_material, expanded=False)

    if len(theory_names) > 1:
        selected_theory = st.radio(f'', theory_names, horizontal=True, key=f"{property_name}_theory_selector", label_visibility='collapsed')
    else:
        selected_theory = theory_names[0]

    theory_details = theories[property_name][selected_theory]
    formula = theory_details['formula']
    latex = theory_details['latex']

    result = formula(fiber_material, matrix_material, Vf, Vm)
    
    st.latex(latex + f" = {result:.3f}")

    st.write(f"Result: {result:.2f}")
    
    # Display the raw code of the formula
    formula_code = inspect.getsource(formula)
    st.code(formula_code, language='python')

def main():
    
    # Onshape Integration
    st.header('Onshape Model Integration')
    document_id = st.text_input('Document ID', '')
    workspace_id = st.text_input('Workspace ID', '')
    element_id = st.text_input('Element ID', '')
    parameter_id = st.text_input('Parameter ID', '')
    new_value = st.text_input('New Value', '')

    if st.button('Load Model'):
        try:
            model = load_step_model(document_id, workspace_id, element_id)
            st.write('Model Loaded Successfully')
            # Display or handle the model content as needed
        except Exception as e:
            st.error(f"Error loading model: {e}")

    if st.button('Change Parameter'):
        try:
            response = change_parameter(document_id, workspace_id, element_id, parameter_id, new_value)
            st.write('Parameter Changed Successfully')
            st.json(response)
        except Exception as e:
            st.error(f"Error changing parameter: {e}")

    
    st.title('Composite Materials Calculator')

    if st.button('Show All Material Data'):
        fiber_df = pd.DataFrame(fibers).transpose()
        matrix_df = pd.DataFrame(matrices).transpose()
        st.write("Fiber Materials Data")
        st.dataframe(fiber_df)
        st.write("Matrix Materials Data")
        st.dataframe(matrix_df)

    col1, col2 = st.columns(2)
    default_fiber_index = 3  
    default_matrix_index = 7 

    with col1:
        fiber_material_key = st.selectbox('Fiber Material', list(fibers.keys()), index=default_fiber_index, help="Choose the type of fiber material")
    with col2:
        matrix_material_key = st.selectbox('Matrix Material', list(matrices.keys()), index=default_matrix_index, help="Choose the type of matrix material")

    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf

    materials_dataframe(fiber_material_key, matrix_material_key)
    st.markdown('***')

    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    results = calculate_properties(fiber_material, matrix_material, Vf, Vm)

    results_df = pd.DataFrame(results)
    st.subheader("Calculated Properties by Theory")
    st.dataframe(results_df)

    plot_properties(results_df)

    st.header('📐 Math')
    st.markdown('***')

    properties = ["youngs_modulus", "shear_modulus", "poisson_ratio", 
                  "tensile_strength", "compressive_strength", 
                  "transverse_tensile_strength", "transverse_compressive_strength",
                  "in_plane_shear_strength"]

    for property_name in properties:
        display_theories(property_name, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm)
        st.markdown('***')

if __name__ == "__main__":
    main()