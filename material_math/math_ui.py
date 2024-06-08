# material_math/math_ui.py

import streamlit as st
import pandas as pd
from utils import materials_dataframe, set_mpl_style
from materials import fibers, matrices
from material_math.calculate_properties import calculate_properties, plot_properties, display_theories
from material_math.formulas import micromech_properties

def materials_ui(fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math, theme_mode):
    set_mpl_style(theme_mode)

    materials_dataframe(fiber_material_key, matrix_material_key, fibers, matrices)

    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    properties_to_calculate = ["E1_modulus", "E2_modulus", "shear_modulus", "poisson_ratio"]

    results_micromechanics, latex_micromechanics, math_micromechanics = calculate_properties(
        micromech_properties, properties_to_calculate, fiber_material, matrix_material, Vf, Vm, Vvoid, show_math
    )

    # Ensure all arrays in results_micromechanics have the same length
    min_length = min(len(arr) for arr in results_micromechanics.values())
    results_micromechanics = {key: value[:min_length] for key, value in results_micromechanics.items()}

    st.header("👉 Micromechanics properties")

    # Ensure properties_to_calculate matches the length of results_micromechanics
    properties_to_calculate = properties_to_calculate[:min_length]
    
    results_df = pd.DataFrame(results_micromechanics)
    
    # Check lengths before inserting
    st.write("Properties to calculate:", properties_to_calculate)
    st.write("Results DataFrame shape:", results_df.shape)
    
    if len(properties_to_calculate) == results_df.shape[0]:
        results_df.insert(0, 'Property', properties_to_calculate)
    else:
        st.error("Length mismatch between properties_to_calculate and results DataFrame")

    st.dataframe(results_df)
    plot_properties(results_df, theme_mode)
    st.markdown('***')

    for property_name in properties_to_calculate:
        display_theories(property_name, micromech_properties, results_micromechanics, latex_micromechanics, math_micromechanics, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid)
        st.markdown('***')
