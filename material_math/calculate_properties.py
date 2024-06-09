import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from composite_math.theories import micromechanics_theories, strength_theories, failure_theories
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
from utils import set_mpl_style


theories = {
    "E1_modulus": micromech_properties["E1_modulus"],
    "E2_modulus": micromech_properties["E2_modulus"],
    "shear_modulus": micromech_properties["shear_modulus"],
    "poisson_ratio": micromech_properties["poisson_ratio"],
    "tensile_strength": strength_properties["tensile_strength"],
    "compressive_strength": strength_properties["compressive_strength"],
    "transverse_tensile_strength": strength_properties["transverse_tensile_strength"],
}

def calculate_properties(theory_dict, properties, fiber_material, matrix_material, Vf, Vm, Vvoid=0, show_math=True):
    results = {property_name: [] for property_name in properties}
    latex_results = {property_name: {} for property_name in properties}
    math_results = {property_name: {} for property_name in properties} if show_math else None

    for property_name in properties:
        if property_name in theory_dict:
            for theory_name, theory_details in theory_dict[property_name].items():
                if theory_name == "unit":
                    continue

                formula = theory_details["formula"]
                latex_formula = theory_details["latex"]

                try:
                    if "Vvoid" in formula.__code__.co_varnames:
                        result = formula(fiber_material, matrix_material, Vf, Vm, Vvoid)
                    else:
                        result = formula(fiber_material, matrix_material, Vf, Vm)
                except TypeError as e:
                    st.error(f"Error calculating {property_name} with {theory_name}: {e}")
                    continue

                results[property_name].append(result)
                latex_results[property_name][theory_name] = latex_formula
                if math_results is not None:
                    math_results[property_name][theory_name] = result

    return results, latex_results, math_results


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

# material_math/calculate_properties.py

def display_theories(property_name, theory_dict, results, latex_results, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, show_individual_graphs=False, theme_mode='default', show_math=False):
    set_mpl_style(theme_mode)
    theory_names = [name for name in theory_dict[property_name].keys() if name != "unit"]

    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        st.subheader(property_name.replace('_', ' ').title())
    with col2:
        st.write(f'{fiber_material_key}')
        st.json(fiber_material, expanded=False)
    with col3:
        st.write(f'{matrix_material_key}')
        st.json(matrix_material, expanded=False)

    if len(theory_names) > 1:
        selected_theory = st.radio(f'Select theory for {property_name.replace("_", " ").title()}', theory_names, horizontal=True, label_visibility="collapsed")
    else:
        selected_theory = theory_names[0]

    theory_details = theory_dict[property_name][selected_theory]
    latex = latex_results[property_name][selected_theory]
    unit = theory_dict[property_name].get('unit', '')

    st.write("Results structure:", results)  # Debug statement

    if show_math:
        st.latex(f"{latex}")
        result = results[property_name][theory_names.index(selected_theory)]
        st.latex(f"{result:.3f} \\ [{unit}]")
    else:
        st.latex(f"{latex} = {results[property_name][theory_names.index(selected_theory)]:.3f} \\ [{unit}]")

    if show_individual_graphs:
        vfs = np.linspace(0, 1, 100)
        all_values = {theory: [] for theory in theory_names}

        for vf in vfs:
            vm = 1 - vf
            for theory in theory_names:
                coeffs = {}
                if 'coefficients' in theory_dict[property_name][theory]:
                    coeffs = {coeff_name: coeff_details['formula'](fiber_material, matrix_material) if 'formula' in coeff_details else coeff_details['default']
                              for coeff_name, coeff_details in theory_dict[property_name][theory]['coefficients'].items()}
                value = theory_dict[property_name][theory]['formula'](fiber_material, matrix_material, vf, vm, **coeffs) if coeffs else theory_dict[property_name][theory]['formula'](fiber_material, matrix_material, vf, vm)
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
