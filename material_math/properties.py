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
    # results_df = pd.DataFrame(structured_data)

    # Formatting the DataFrame and adding the average column
    def format_values(x):
        return f"{x:.3f}" if pd.notnull(x) else ""

    def calculate_average(row):
        valid_numbers = [float(x) for x in row if pd.notnull(x)]
        return sum(valid_numbers) / len(valid_numbers) if valid_numbers else None

    results_df = results_df.applymap(lambda x: float(x) if pd.notnull(x) else None)
    results_df['Average'] = results_df.apply(lambda row: calculate_average(row), axis=1)
    results_df = results_df.applymap(format_values)

    # Move Average column to the first position
    cols = results_df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Average')))
    results_df = results_df[cols]

    # Plotting horizontal bars
    fig, ax = plt.subplots(figsize=(14, 10))

    color_map = plt.get_cmap('tab10')
    color_dict = {theory: color_map(i) for i, theory in enumerate(set(theory for sublist in theories.values() for theory in sublist))}

    y_tick_positions = []
    y_labels = []

    y_pos = 0
    bar_height = 0.4  # Reduced bar height for narrower columns

    for property_name in properties:
        unit = units[properties.index(property_name)]
        y_labels.append(f"{property_name} [{unit}]")
        y_tick_positions.append(y_pos + len(theories[property_name]) / 2.0)
        
        for idx, theory_name in enumerate(theories[property_name]):
            value = results[property_name][theories[property_name].index(theory_name)]
            if pd.notnull(value):
                bar_position = y_pos + idx
                ax.barh(bar_position, float(value), color=color_dict[theory_name], edgecolor='black', height=bar_height)
                ax.text(float(value), bar_position, f" {theory_name}", va='center', ha='left', color='white', fontsize=12)  # Increased fontsize
                ax.text(float(value), bar_position, f" {float(value):.2f}", va='center', ha='right', color='white', fontsize=14, fontweight='bold')  # Larger font for values
        y_pos += len(theories[property_name]) + 1  # Add space between properties

    ax.set_yticks(y_tick_positions)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('MPa / GPa')
    ax.set_title('Composite properties compared by theory')
    ax.grid(True)
    st.pyplot(fig)

    # styled_df = results_df.style.applymap(lambda x: 'background-color: lightgray' if x == results_df['Average'].name else '', subset=['Average'])

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
        st.caption(f"""{fiber_material_key}\n {matrix_material_key}""")

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

        color_map = plt.get_cmap('tab10')
        color_dict = {theory: color_map(i) for i, theory in enumerate(theory_names)}

        # Initialize max_value as -infinity to find the actual maximum value
        # max_value = -np.inf
        max_value = -400
        max_theory = None
        max_value_at_Vf = None

        for theory, values in all_values.items():
            ax.plot(vfs, values, label=theory)
            current_value = values[np.abs(vfs - Vf).argmin()]
            if current_value > max_value:  # Correct comparison to find the maximum value
                max_value = current_value
                max_theory = theory
                max_value_at_Vf = current_value

        # Add the dot and text box at the intersection
        ax.scatter(Vf, max_value_at_Vf, color=color_dict[max_theory], zorder=5)
        ax.text(Vf, max_value_at_Vf, f'{max_value_at_Vf:.3f} [{unit}]\n{max_theory}', fontsize=14, color=color_dict[max_theory],
                ha='right', va='bottom', bbox=dict(facecolor='white', alpha=0.8, edgecolor=color_dict[max_theory]))

        ax.axvline(Vf, color='red', linestyle='--', alpha=0.5, label=f'Current Vf = {Vf}')
        ax.set_title(f'{property_name.replace("_", " ").title()} vs. Fiber Volume Fraction')
        ax.set_xlabel('Fiber Volume Fraction (Vf)')
        ax.set_ylabel(f'{property_name.replace("_", " ").title()} ({unit})')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
