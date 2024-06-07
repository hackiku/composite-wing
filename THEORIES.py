# micromechanics.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np
import inspect
from calculations import theories

def set_mpl_style(theme_mode):
    if theme_mode == "dark":
        mplstyle.use('dark_background')
    else:
        mplstyle.use('default')

def display_theories(property_name, fiber_key, fiber_material, matrix_key, matrix_material, Vf, Vm, Vvoid, show_individual_graphs, theme_mode, latex_results, math_results, show_math):
    set_mpl_style(theme_mode)
    theory_names = [name for name in theories[property_name].keys() if name != "unit"]

    coefficients = {}

    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.subheader(property_name.replace('_', ' ').title())
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