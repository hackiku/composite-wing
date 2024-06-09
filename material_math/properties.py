import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import inspect
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
from utils import set_mpl_style

def calculate_properties(category, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid=0, show_math=True):
    results = {}
    latex_results = {}
    math_results = {} if show_math else None

    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    for property_name, theories in category.items():
        results[property_name] = []
        latex_results[property_name] = {}

        for theory_name, theory_details in theories.items():
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
            if show_math:
                math_results[property_name] = {theory_name: result}

    return results, latex_results, math_results

def calculate_failure(fibers, matrices, fiber_material_key, matrix_material_key, sigma, show_math=True):
    results = {}
    latex_results = {}
    math_results = {} if show_math else None

    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    for property_name, theories in failure_criteria.items():
        results[property_name] = []
        latex_results[property_name] = {}

        for theory_name, theory_details in theories.items():
            if theory_name == "unit":
                continue

            formula = theory_details["formula"]
            latex_formula = theory_details["latex"]

            F = {
                'F1': fiber_material.get('F1ft', 0),
                'F2': matrix_material.get('FmT', 0),
                'F6': matrix_material.get('FmS', 0),
                'F1t': fiber_material.get('F1ft', 0),
                'F2t': matrix_material.get('FmT', 0),
                'F1c': fiber_material.get('F1fc', 0),
                'F2c': matrix_material.get('FmC', 0),
                'F11': 1,  # Example value
                'F22': 1,  # Example value
                'F12': 1,  # Example value
                'F66': 1,  # Example value
            }

            try:
                # Debugging output
                st.write(f"Calculating {property_name} with {theory_name}")
                st.write(f"Fiber Material: {fiber_material}")
                st.write(f"Matrix Material: {matrix_material}")
                st.write(f"Sigma: {sigma}")

                result = formula(fiber_material, matrix_material, sigma, F)

                # More debugging output
                st.write(f"Result: {result}")

            except TypeError as e:
                st.error(f"Error calculating {property_name} with {theory_name}: {e}")
                continue

            results[property_name].append(result)
            latex_results[property_name][theory_name] = latex_formula
            if show_math:
                math_results[property_name] = {theory_name: result}

    return results, latex_results, math_results

def plot_properties(results, theme_mode):
    set_mpl_style(theme_mode)
    results_df = pd.DataFrame(results).transpose()
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

def display_theories(property_name, results, latex_results, math_results, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid, sigma, show_individual_graphs=False, theme_mode='default', show_math=False):
    set_mpl_style(theme_mode)
    theory_dict = micromech_properties if property_name in micromech_properties else strength_properties if property_name in strength_properties else failure_criteria
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
    formula = theory_details["formula"]
    latex = latex_results[property_name][selected_theory]
    unit = theory_dict[property_name].get('unit', '')

    if show_math:
        st.latex(f"{latex}")
        result = results[property_name][theory_names.index(selected_theory)]
        st.latex(f"{result:.3f} \\ [{unit}]")
    else:
        st.latex(f"{latex} = {results[property_name][theory_names.index(selected_theory)]:.3f} \\ [{unit}]")

    formula_code = inspect.getsource(theory_details["formula"])
    st.code(formula_code, language='python')

    if show_individual_graphs:
        vfs = np.linspace(0, 1, 100)
        all_values = {theory: [] for theory in theory_names}

        for vf in vfs:
            vm = 1 - vf
            for theory in theory_names:
                formula = theory_dict[property_name][theory]["formula"]
                coeffs = {}
                if 'coefficients' in theory_dict[property_name][theory]:
                    coeffs = {coeff_name: coeff_details['formula'](fiber_material, matrix_material) if 'formula' in coeff_details else coeff_details['default']
                              for coeff_name, coeff_details in theory_dict[property_name][theory]['coefficients'].items()}
                if "Vvoid" in formula.__code__.co_varnames:
                    value = formula(fiber_material, matrix_material, vf, vm, Vvoid, **coeffs)
                else:
                    value = formula(fiber_material, matrix_material, vf, vm)
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
