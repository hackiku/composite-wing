        # "Rosen": {
        #     "formula": lambda f, m, Vf, Vm: (m['Gm'] / (1 - Vf)),
        #     "latex": r"F_{1C} = \frac{G_m}{1 - V_f}",
        #     "math": lambda f, m, Vf, Vm: f"F_{{1C}} = \\frac{{{m['Gm']}}}{{1 - {Vf:.3f}}}"
        # },
        # "Budiansky-Fleck ($V_f > 0.3$)": {
        #     "formula": lambda f, m, Vf, Vm, vf_check: (
        #         m['tau_ry'] / (m['phi'] + m['gamma_ry']) if vf_check else None
        #     ),
        #     "latex": r"F_{1C} = \frac{\tau_{ry}}{\phi + \gamma_{ry}}",
        #     "math": lambda f, m, Vf, Vm, vf_check: (
        #         f"F_{{1C}} = \\frac{{{m['tau_ry']}}}{{{m['phi']} + {m['gamma_ry']}}}" if vf_check else "N/A"
        #     ),
        #     "coefficients": {
        #         "vf_check": {
        #             "formula": lambda Vf: Vf > 0.3,
        #             "latex": r"V_f > 0.3"
        #         }
        #     }
        # },
        # "Agarwal-Broutman": {
        #     "formula": lambda f, m, Vf, Vm: ((f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['epsilon_mT']) / (f['ni12f'] * Vf + m['nim'] * Vm),
        #     "latex": r"F_{1C} = \frac{(E_{1f} V_f + E_m V_m) (1 - V_f^{1/3}) \varepsilon_{mu}}{\nu_{12f} V_f + \nu_m V_m}",
        #     "math": lambda f, m, Vf, Vm: f"F_{{1C}} = \\frac{{({f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}) \cdot (1 - {Vf:.3f}^{{1/3}}) \cdot {m['epsilon_mT']}}}{{{f['ni12f']} \cdot {Vf:.3f} + {m['nim']} \cdot {Vm:.3f}}}"
        # },    
    # },















# material_math/math_ui.py

import streamlit as st
from material_math.properties import calculate_properties, plot_properties, display_theories, get_property_units

def compute_ni21(ni12, E2, E1):
    return ni12 * E2 / E1

def display_micromechanical_properties(fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math, show_individual_graphs):
    sigma = {'sigma1': 100, 'sigma2': 50, 'tau12': 30}  # Example values

    # Calculate micromechanical properties
    micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, micromechanics_theories = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)

    st.header("Micromechanical properties")
    st.write("The following properties are calculated using micromechanical models for the combination:")
    col1, col2 = st.columns([6, 4])
    with col1:
        st.code(f"{fiber_material_key} / {matrix_material_key}")
    with col2:
        st.code(f"Vf: {Vf} / Vm: {Vm} / Vvoid: {Vvoid}")
        
    properties = ["E1", "E2", "G12", "ni12", "ni21"]
    units = get_property_units(properties)

    col1, col2 = st.columns([6, 1])
    with col1:
        micromechanics_df = plot_properties(micromechanics_results, properties, units, micromechanics_theories)
    st.write(micromechanics_df)

    if st.button("Compare all material combos", type="primary"): 
        st.write("3D Graph")

    st.markdown("***")

    for property_name in properties:
        if property_name in micromech_properties:
            display_theories(property_name, micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, fiber_material_key, fibers[fiber_material_key], matrix_material_key, matrices[matrix_material_key], Vf, Vm, Vvoid, sigma, show_individual_graphs, show_math)
            st.markdown("***")
    
    # Allow users to select theories for ni12, E1, and E2
    selected_ni12_theory = st.selectbox("Select theory for ni12", micromechanics_theories['ni12'])
    selected_E1_theory = st.selectbox("Select theory for E1", micromechanics_theories['E1'])
    selected_E2_theory = st.selectbox("Select theory for E2", micromechanics_theories['E2'])

    # Get the index of the selected theories
    ni12_index = micromechanics_theories['ni12'].index(selected_ni12_theory)
    E1_index = micromechanics_theories['E1'].index(selected_E1_theory)
    E2_index = micromechanics_theories['E2'].index(selected_E2_theory)

    # Compute ni21 using the selected theory values
    ni12 = micromechanics_results['ni12'][ni12_index]
    E2 = micromechanics_results['E2'][E2_index]
    E1 = micromechanics_results['E1'][E1_index]
    computed_ni21 = compute_ni21(ni12, E2, E1)

    # Display the computed ni21
    st.write("Computed ni21:", computed_ni21)

    # Display LaTeX formatted results
    latex_formula = r"\nu_{21} = \nu_{12} \cdot \frac{E_{2}}{E_{1}}"
    latex_result = f"\\nu_{{21}} = {ni12:.3f} \\cdot \\frac{{{E2:.3f}}}{{{E1:.3f}}} = {computed_ni21:.3f}"

    st.latex(latex_formula)
    st.latex(latex_result)
    
    st.write("Computed ni21:", computed_ni21)

# material_math/math_ui.py

import streamlit as st
from material_math.properties import calculate_properties, plot_properties, display_theories, get_property_units

def compute_ni21(ni12, E2, E1):
    return ni12 * E2 / E1

def display_micromechanical_properties(fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math, show_individual_graphs):
    sigma = {'sigma1': 100, 'sigma2': 50, 'tau12': 30}  # Example values

    # Calculate micromechanical properties
    micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, micromechanics_theories = calculate_properties(micromech_properties, fibers, matrices, fiber_material_key, matrix_material_key, Vf, Vm, Vvoid, show_math=show_math)

    st.header("Micromechanical properties")
    st.write("The following properties are calculated using micromechanical models for the combination:")
    col1, col2 = st.columns([6, 4])
    with col1:
        st.code(f"{fiber_material_key} / {matrix_material_key}")
    with col2:
        st.code(f"Vf: {Vf} / Vm: {Vm} / Vvoid: {Vvoid}")
        
    properties = ["E1", "E2", "G12", "ni12", "ni21"]
    units = get_property_units(properties)

    col1, col2 = st.columns([6, 1])
    with col1:
        micromechanics_df = plot_properties(micromechanics_results, properties, units, micromechanics_theories)
    st.write(micromechanics_df)

    if st.button("Compare all material combos", type="primary"): 
        st.write("3D Graph")

    st.markdown("***")

    for property_name in properties:
        if property_name in micromech_properties:
            display_theories(property_name, micromechanics_results, micromechanics_latex, micromechanics_math, micromechanics_coefficients, fiber_material_key, fibers[fiber_material_key], matrix_material_key, matrices[matrix_material_key], Vf, Vm, Vvoid, sigma, show_individual_graphs, show_math)
            st.markdown("***")
    
    # Allow users to select theories for ni12, E1, and E2
    selected_ni12_theory = st.selectbox("Select theory for ni12", micromechanics_theories['ni12'])
    selected_E1_theory = st.selectbox("Select theory for E1", micromechanics_theories['E1'])
    selected_E2_theory = st.selectbox("Select theory for E2", micromechanics_theories['E2'])

    # Get the index of the selected theories
    ni12_index = micromechanics_theories['ni12'].index(selected_ni12_theory)
    E1_index = micromechanics_theories['E1'].index(selected_E1_theory)
    E2_index = micromechanics_theories['E2'].index(selected_E2_theory)

    # Compute ni21 using the selected theory values
    ni12 = micromechanics_results['ni12'][ni12_index]
    E2 = micromechanics_results['E2'][E2_index]
    E1 = micromechanics_results['E1'][E1_index]
    computed_ni21 = compute_ni21(ni12, E2, E1)

    # Display the computed ni21
    st.write("Computed ni21:", computed_ni21)

    # Display LaTeX formatted results
    latex_formula = r"\nu_{21} = \nu_{12} \cdot \frac{E_{2}}{E_{1}}"
    latex_result = f"\\nu_{{21}} = {ni12:.3f} \\cdot \\frac{{{E2:.3f}}}{{{E1:.3f}}} = {computed_ni21:.3f}"

    st.latex(latex_formula)
    st.latex(latex_result)
    
    st.write("Computed ni21:", computed_ni21)

