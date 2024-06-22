# material_math/properties.py

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
import inspect


def calculate_properties(category, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid=0, show_math=True):
    results = {}
    latex_results = {}
    math_results = {} if show_math else None
    coefficients_latex = {}
    theories_map = {}

    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    for property_name, theories in category.items():
        results[property_name] = []
        latex_results[property_name] = {}
        coefficients_latex[property_name] = {}
        theories_map[property_name] = [theory_name for theory_name in theories if theory_name not in ["unit", "name", "help"]]

        for theory_name, theory_details in theories.items():
            if theory_name in ["unit", "name", "help"]:
                continue

            formula = theory_details["formula"]
            latex_formula = theory_details["latex"]
            math_formula = theory_details.get("math", None)

            try:
                coefficients = {}
                if 'coefficients' in theory_details:
                    coefficients_latex[property_name][theory_name] = {}
                    for coeff_name, coeff_details in theory_details['coefficients'].items():
                        if 'formula' in coeff_details:
                            num_args = coeff_details['formula'].__code__.co_argcount
                            if num_args == 2:
                                coefficients[coeff_name] = coeff_details['formula'](fiber_material, matrix_material)
                            elif num_args == 4:
                                coefficients[coeff_name] = coeff_details['formula'](fiber_material, matrix_material, Vf, Vm)
                            coefficients_latex[property_name][theory_name][coeff_name] = f"{coeff_details['latex']} = {coefficients[coeff_name]:.3f}"
                        else:
                            coefficients[coeff_name] = coeff_details['default']
                            coefficients_latex[property_name][theory_name][coeff_name] = f"{coeff_details['latex']} = {coefficients[coeff_name]:.3f}"

                if "Vvoid" in formula.__code__.co_varnames:
                    result = formula(fiber_material, matrix_material, Vf, Vm, Vvoid, **coefficients)
                else:
                    result = formula(fiber_material, matrix_material, Vf, Vm, **coefficients)
                
                if math_formula:
                    if 'Vvoid' in math_formula.__code__.co_varnames:
                        interpolated_math = math_formula(fiber_material, matrix_material, Vf, Vm, Vvoid, **coefficients)
                    else:
                        interpolated_math = math_formula(fiber_material, matrix_material, Vf, Vm, **coefficients)
                else:
                    interpolated_math = None

            except TypeError as e:
                st.error(f"Error calculating {property_name} with {theory_name}: {e}")
                result = None
                interpolated_math = None

            results[property_name].append(result)
            latex_results[property_name][theory_name] = latex_formula

            if show_math:
                if property_name not in math_results:
                    math_results[property_name] = {}
                math_results[property_name][theory_name] = interpolated_math

    # Ensure all lists are the same length
    max_length = max(len(results[prop]) for prop in results)
    for prop in results:
        while len(results[prop]) < max_length:
            results[prop].append(None)

    return results, latex_results, math_results, coefficients_latex, theories_map



def plot_properties(results, properties, units, theories):
    # Initialize a dictionary to hold the structured data
    structured_data = {property_name: {} for property_name in properties}
    
    for property_name in properties:
        for idx, theory_name in enumerate(theories[property_name]):
            key = f"{property_name} [{units[properties.index(property_name)]}]"
            if theory_name not in structured_data[property_name]:
                structured_data[property_name][theory_name] = results[property_name][idx]

    # Create DataFrame from the structured data
    results_df = pd.DataFrame(structured_data).transpose()

    # Formatting the DataFrame
    results_df = results_df.applymap(lambda x: f"{x:.3f}" if x is not None else "0.000")

    # Plotting
    fig, ax1 = plt.subplots(figsize=(14, 10))
    ax2 = ax1.twiny()

    color_map = plt.get_cmap('tab10')
    color_idx = 0
    color_dict = {}

    for property_name in properties:
        color_dict[property_name] = color_map(color_idx)
        color_idx += 1

    for property_name in properties:
        unit = units[properties.index(property_name)]
        y_pos = properties.index(property_name)
        for theory_name in theories[property_name]:
            value = results[property_name][theories[property_name].index(theory_name)]
            ax1.plot([value], [y_pos], 'o', label=theory_name, color=color_dict[property_name])
            ax1.text(value, y_pos, f"{theory_name}", fontsize=9, ha='right' if value < 10 else 'left')

    ax1.set_yticks(range(len(properties)))
    ax1.set_yticklabels([f"{prop} [{unit}]" for prop, unit in zip(properties, units)])
    ax1.set_xlabel('MPa / GPa')
    ax1.set_title('Composite properties compared by theory')
    ax1.grid(True)
    
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(ax1.get_xticks())
    ax2.set_xticklabels([f"{x:.3f}" for x in ax1.get_xticks()])
    ax2.set_xlabel('Dimensionless')

    fig.legend(loc='upper right', bbox_to_anchor=(1.15, 1.0))
    st.pyplot(fig)

    return results_df

def get_property_units(properties):
    unit_map = {**micromech_properties, **strength_properties, **failure_criteria}
    return [unit_map[prop].get("unit", '') for prop in properties]



def display_theories(property_name, results, latex_results, math_results, coefficients_latex, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid, sigma=None, show_individual_graphs=False, show_math=False):
    theory_dict = micromech_properties if property_name in micromech_properties else strength_properties if property_name in strength_properties else failure_criteria
    theory_names = [name for name in theory_dict[property_name].keys() if name not in ["unit", "name", "help"]]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"`{property_name.title()}` {theory_dict[property_name]['name']}", help=theory_dict[property_name]['help'])
    with col2:
        st.caption(f"""{fiber_material_key}
                   \n {matrix_material_key}""")

    unit = theory_dict[property_name].get('unit', '')

    if len(theory_names) > 1:
        selected_theory = st.radio(f'Select theory for {property_name} ', theory_names, horizontal=True, label_visibility="collapsed")
    else:
        selected_theory = theory_names[0]

    theory_details = theory_dict[property_name][selected_theory]
    formula = theory_details["formula"]
    latex = latex_results[property_name][selected_theory]
    result = results[property_name][theory_names.index(selected_theory)]
    
    if selected_theory in coefficients_latex[property_name]:
        for coeff, coeff_latex in coefficients_latex[property_name][selected_theory].items():
            st.latex(coeff_latex)
            
    if show_math and math_results[property_name][selected_theory]:
        st.latex(f"{latex}")
        st.latex(f"{math_results[property_name][selected_theory]} = {result:.3f} \\ [{unit}]")
        formula_code = inspect.getsource(theory_details["formula"])
        st.code(formula_code, language='python')
    else:
        st.latex(f"{latex} = {result:.3f} \\ [{unit}]")


    if show_individual_graphs:
        vfs = np.linspace(0, 1, 100)
        all_values = {theory: [] for theory in theory_names}

        for vf in vfs:
            vm = 1 - vf
            for theory in theory_names:
                formula = theory_dict[property_name][theory]["formula"]
                coeffs = {}
                if 'coefficients' in theory_dict[property_name][theory]:
                    for coeff_name, coeff_details in theory_dict[property_name][theory]['coefficients'].items():
                        num_args = coeff_details['formula'].__code__.co_argcount
                        if num_args == 2:
                            coeffs[coeff_name] = coeff_details['formula'](fiber_material, matrix_material)
                        elif num_args == 4:
                            coeffs[coeff_name] = coeff_details['formula'](fiber_material, matrix_material, vf, vm)
                        else:
                            coeffs[coeff_name] = coeff_details['default']
                if "Vvoid" in formula.__code__.co_varnames:
                    value = formula(fiber_material, matrix_material, vf, vm, Vvoid, **coeffs)
                else:
                    value = formula(fiber_material, matrix_material, vf, vm, **coeffs)
                all_values[theory].append(value)

        fig, ax = plt.subplots(figsize=(12, 6))
        for theory, values in all_values.items():
            ax.plot(vfs, values, label=theory)
        ax.axvline(Vf, color='red', linestyle='--', alpha=0.5, label=f'Current Vf = {Vf}')
        ax.set_title(f'{property_name.replace("_", " ").title()} vs. Fiber Volume Fraction', color='white')
        ax.set_xlabel('Fiber Volume Fraction (Vf)', color='white')
        ax.set_ylabel(f'{property_name.replace("_", " ").title()} ({unit})', color='white')
        ax.legend()
        ax.grid(True, color='gray')
        ax.tick_params(colors='white')
        st.pyplot(fig)
