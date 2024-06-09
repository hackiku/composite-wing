# material_math/properties.py

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from material_math.formulas import micromech_properties, strength_properties, failure_criteria
from utils import spacer, set_mpl_style
import inspect

def calculate_properties(category, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid=0, show_math=True):
    results = {}
    latex_results = {}
    math_results = {} if show_math else None
    theories_map = {}

    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    for property_name, theories in category.items():
        results[property_name] = []
        latex_results[property_name] = {}
        theories_map[property_name] = [theory_name for theory_name in theories if theory_name != "unit"]

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
                if property_name not in math_results:
                    math_results[property_name] = {}
                math_results[property_name][theory_name] = result

    return results, latex_results, math_results, theories_map


def plot_properties(results, properties, units, theories):
    flattened_data = {}
    for property_name in properties:
        if property_name in theories:
            for idx, theory_name in enumerate(theories[property_name]):
                flattened_data[f"{property_name} ({theory_name}, {units[properties.index(property_name)]})"] = results[property_name][idx]

    results_df = pd.DataFrame([flattened_data])
    
    if results_df.empty:
        st.write("No data to display.")
        return results_df
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    color_map = plt.get_cmap("tab10")
    color_idx = 0
    
    for property_name in properties:
        if property_name in theories:
            for idx, theory_name in enumerate(theories[property_name]):
                label = f"{property_name} ({theory_name}, {units[properties.index(property_name)]})"
                if "GPa" in label or "MPa" in label:
                    ax1.plot(results_df.index, results_df[label], marker='o', linestyle='-', color=color_map(color_idx), label=label)
                elif "-" in label:  # Assuming dimensionless values for poisson_ratio
                    ax2 = ax1.twinx()
                    ax2.plot(results_df.index, results_df[label], marker='x', linestyle='--', color=color_map(color_idx), label=label)
                    ax2.set_ylabel('Dimensionless', color='white')
                color_idx += 1

    ax1.set_title('Composite properties compared by theory', color='white')
    ax1.set_xlabel('Property', color='white')
    ax1.set_ylabel('MPa / GPa', color='white')
    ax1.grid(True, color='gray')
    ax1.tick_params(colors='white')

    fig.legend()
    st.pyplot(fig)
    
    return results_df

def get_property_units(properties):
    unit_map = {**micromech_properties, **strength_properties, **failure_criteria}
    return [unit_map[prop].get("unit", '') for prop in properties]

def display_theories(property_name, results, latex_results, math_results, fiber_material_key, fiber_material, matrix_material_key, matrix_material, Vf, Vm, Vvoid, sigma, show_individual_graphs=False, show_math=False):
    theory_dict = micromech_properties if property_name in micromech_properties else strength_properties if property_name in strength_properties else failure_criteria
    theory_names = [name for name in theory_dict[property_name].keys() if name != "unit"]

    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        st.subheader(property_name.replace('_', ' ').title())
    with col2:
        spacer()
    with col3:
        spacer()

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
        ax.set_title(f'{property_name.replace("_", " ").title()} vs. Fiber Volume Fraction', color='white')
        ax.set_xlabel('Fiber Volume Fraction (Vf)', color='white')
        ax.set_ylabel(f'{property_name.replace("_", " ").title()} ({unit})', color='white')
        ax.legend()
        ax.grid(True, color='gray')
        ax.tick_params(colors='white')
        st.pyplot(fig)
    return theory_names
