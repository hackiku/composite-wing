# material_math/math_ui.py

import streamlit as st
import pandas as pd
import matplotlib.style as mplstyle
from materials import fibers, matrices
from material_math.calculate_properties import calculate_properties, plot_properties, display_theories
from material_math.formulas import micromechanics_properties

def set_mpl_style(theme_mode):
    if theme_mode == "dark":
        mplstyle.use('dark_background')
    else:
        mplstyle.use('default')


def materials_ui(fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math, theme_mode):

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

    # Ensure all arrays are of the same length
    min_length = min(len(arr) for arr in results_micromechanics.values())
    results_micromechanics = {key: value[:min_length] for key, value in results_micromechanics.items()}

    # Display micromechanics results and plots
    st.header("👉 Micromechanics properties")
    results_df = pd.DataFrame(results_micromechanics)
    st.dataframe(results_df)
    plot_properties(results_df, theme_mode)
    st.markdown('***')

    for property_name in micromechanics_properties:
        display_theories(property_name, micromechanics_theories, results_micromechanics, latex_micromechanics, math_micromechanics, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid)
        st.markdown('***')
