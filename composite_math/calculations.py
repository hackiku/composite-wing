# composite_math/calculations.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import streamlit as st
from composite_math.theories import micromechanics_theories, strength_theories, failure_theories, failure_wrapper, strength_wrapper, micromechanics_wrapper


def set_mpl_style(theme_mode):
    if theme_mode == "dark":
        mplstyle.use('dark_background')
    else:
        mplstyle.use('default')


def calculate_properties(theory_dict, properties, fiber_material, matrix_material, Vf, Vm, Vvoid=0, sigma=None, F=None, show_math=True):
    results = {"Property": properties}
    latex_results = {property_name: {} for property_name in properties}
    math_results = {property_name: {} for property_name in properties} if show_math else None

    param_dict = {
        'f': fiber_material,
        'm': matrix_material,
        'Vf': Vf,
        'Vm': Vm,
        'Vvoid': Vvoid,
        'sigma': sigma,
        'F': F
    }

    for property_name in properties:
        if property_name in theory_dict:
            for theory_name, theory_details in theory_dict[property_name].items():
                if theory_name == "unit":
                    continue

                formula = theory_details["formula"]
                latex_formula = theory_details["latex"]
                math_formula = theory_details.get("math", None)

                if "sigma" in formula.__code__.co_varnames:
                    result = failure_wrapper(formula, param_dict)
                elif "Vvoid" in formula.__code__.co_varnames:
                    result = strength_wrapper(formula, param_dict)
                else:
                    result = micromechanics_wrapper(formula, param_dict)

                results.setdefault(theory_name, []).append(result)

                if show_math and math_formula:
                    math_results[property_name][theory_name] = result

                latex_results[property_name][theory_name] = latex_formula

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

def display_theories(property_name, theory_dict, results, latex_results, math_results, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, **kwargs):
    
    set_mpl_style(kwargs.get('theme_mode', 'default'))
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
    formula = theory_details['formula']
    latex = latex_results[property_name][selected_theory]
    unit = theory_dict[property_name].get('unit', '')

    # Extract the variables used in the formula
    used_variables = {'Vf': Vf, 'Vm': Vm}
    used_variables.update(fiber_material)
    used_variables.update(matrix_material)
    
    if 'coefficients' in theory_details:
        coefficients = {coeff_name: coeff_details['formula'](fiber_material, matrix_material) if 'formula' in coeff_details else coeff_details['default']
                        for coeff_name, coeff_details in theory_details['coefficients'].items()}
        result = formula(fiber_material, matrix_material, Vf, Vm, **coefficients)
    else:
        result = formula(fiber_material, matrix_material, Vf, Vm)

    if kwargs.get('show_math', False):
        st.latex(f"{latex}")
        math = math_results[property_name][selected_theory]
        st.latex(f"{math} = {result:.3f} \\ [{unit}]")
    else:
        st.latex(f"{latex} = {result:.3f} \\ [{unit}]")

    if kwargs.get('show_individual_graphs', False):
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
        ax.set_title(f'{property_name.replace("_", " ").title()} vs. Fiber Volume Fraction', color='white' if kwargs.get('theme_mode', 'default') == 'dark' else 'black')
        ax.set_xlabel('Fiber Volume Fraction (Vf)', color='white' if kwargs.get('theme_mode', 'default') == 'dark' else 'black')
        ax.set_ylabel(f'{property_name.replace("_", " ").title()} ({unit})', color='white' if kwargs.get('theme_mode', 'default') == 'dark' else 'black')
        ax.legend()
        ax.grid(True, color='gray')
        ax.tick_params(colors='white' if kwargs.get('theme_mode', 'default') == 'dark' else 'black')
        st.pyplot(fig)
