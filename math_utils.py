# math_utils.py
import streamlit as st
import pandas as pd

# def materials_dataframe(fiber_key, matrix_key, fibers, matrices):
#     fiber_properties = pd.DataFrame.from_dict(fibers[fiber_key], orient='index', columns=[fiber_key]).transpose()
#     matrix_properties = pd.DataFrame.from_dict(matrices[matrix_key], orient='index', columns=[matrix_key]).transpose()
#     st.write("Selected Fiber Material Properties:")
#     st.dataframe(fiber_properties)
#     st.write("Selected Matrix Material Properties:")
#     st.dataframe(matrix_properties)

def calculate_property(formula, fiber_material, matrix_material, Vf, Vm, Vvoid=0):
    if "Vvoid" in formula.__code__.co_varnames:
        return formula(fiber_material, matrix_material, Vf, Vm, Vvoid)
    else:
        return formula(fiber_material, matrix_material, Vf, Vm)

def compute_results(theory_dict, properties, fiber_material, matrix_material, Vf, Vm, Vvoid=0, show_math=True):
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
                    result = calculate_property(formula, fiber_material, matrix_material, Vf, Vm, Vvoid)
                except TypeError as e:
                    st.error(f"Error calculating {property_name} with {theory_name}: {e}")
                    continue

                results[property_name].append(result)
                latex_results[property_name][theory_name] = latex_formula
                if math_results is not None:
                    math_results[property_name][theory_name] = result

    return results, latex_results, math_results
