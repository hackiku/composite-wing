import streamlit as st
import pandas as pd
import numpy as np
from materials import fibers, matrices
from latex_utils import render_latex
from calculations import calculate_youngs_modulus, calculate_shear_modulus

def spacer(height='2em'):
    st.markdown(f'<div style="margin: {height};"></div>', unsafe_allow_html=True)

def materials_dataframe(fiber, matrix):
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber], orient='index', columns=[fiber]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix], orient='index', columns=[matrix]).transpose()
    st.write("Selected Fiber Material Properties:")
    st.dataframe(fiber_properties)
    st.write("Selected Matrix Material Properties:")
    st.dataframe(matrix_properties)

theories = {
    "Chamis": {
        "youngs_modulus": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = {E1f}V_f + {Em}V_m"
        },
        "shear_modulus": {
            "formula": lambda f, m, Vf, Vm: m['Gm'] / (1 - np.sqrt(Vf) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"G_{12} = \frac{{G_m}}{{1 - \sqrt{{V_f}}(1 - \frac{{G_m}}{{G_{12f}}})}}"
        }
    },
    "Rule of Mixtures": {
        "youngs_modulus": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = {E1f}V_f + {Em}V_m"
        },
        "shear_modulus": {
            "formula": lambda f, m, Vf, Vm: f['G12f'] * Vf + m['Gm'] * Vm,
            "latex": r"G_{12} = {G12f}V_f + {G_m}V_m"
        }
    },
    "Halpin-Tsai": {
        "youngs_modulus": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
            "latex": r"E_1 = \frac{{E1f \cdot Em}}{{V_f \cdot Em + V_m \cdot E1f}}"
        },
        "shear_modulus": {
            "formula": lambda f, m, Vf, Vm: f['G12f'] * (1 + 0.6 * Vf) / (1 - 0.6 * Vf),
            "latex": r"G_{12} = \frac{{G12f(1 + 0.6V_f)}}{{1 - 0.6V_f}}"
        }
    }
}

def main():
    st.title('Composite Materials Calculator')

    if st.button('Show All Material Data'):
        fiber_df = pd.DataFrame(fibers).transpose()
        matrix_df = pd.DataFrame(matrices).transpose()
        st.write("Fiber Materials Data")
        st.dataframe(fiber_df)
        st.write("Matrix Materials Data")
        st.dataframe(matrix_df)

    col1, col2 = st.columns(2)
    
    default_fiber_index = 3  
    default_matrix_index = 7 

    with col1:
        fiber_material_key = st.selectbox('Fiber Material', list(fibers.keys()), index=default_fiber_index, help="Choose the type of fiber material")
    with col2:
        matrix_material_key = st.selectbox('Matrix Material', list(matrices.keys()), index=default_matrix_index, help="Choose the type of matrix material")

    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf

    materials_dataframe(fiber_material_key, matrix_material_key)

    st.markdown('***')
    
    fiber_material = fibers[fiber_material_key]
    matrix_material = matrices[matrix_material_key]

    # --------------------- ALL CALCS ---------------------

    # Calculate values for each theory
    results = {
        "Property": ["Young's Modulus `E1`", "Shear Modulus `G12`"],
    }

    for theory_name, theory_details in theories.items():
        E1 = theory_details['youngs_modulus']['formula'](fiber_material, matrix_material, Vf, Vm)
        G12 = theory_details['shear_modulus']['formula'](fiber_material, matrix_material, Vf, Vm)
        results[theory_name] = [E1, G12]

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Display the DataFrame
    st.subheader("Calculated Properties by Theory")
    st.dataframe(results_df)


    # --------------------- LATEX ---------------------

    st.markdown('***')

    # Select theory
    theory = st.radio('Select theory for calculations', list(theories.keys()), horizontal=True)

    # Calculate Young's Modulus (E1) --------------------------------
    youngs_modulus = theories[theory]['youngs_modulus']
    E1 = youngs_modulus['formula'](fiber_material, matrix_material, Vf, Vm)
    st.subheader('Young’s Modulus `E1`', help="Calculated as the weighted average of the modulus of the fiber and matrix.")
    values = {"E1f": fiber_material['E1f'], "V_f": Vf, "Em": matrix_material['Em'], "V_m": Vm}
    st.latex(render_latex('', youngs_modulus['latex'], values))
    st.latex(f"E_1 = {E1:.2f} \\, \\text{{GPa}}")

    st.markdown('***')

    # Shear Modulus (G12) --------------------------------
    shear_modulus = theories[theory]['shear_modulus']
    G12 = shear_modulus['formula'](fiber_material, matrix_material, Vf, Vm)
    st.subheader(f'Shear Modulus `G12`', help="Calculated using the selected theory model for shear modulus.")
    values = {"G_m": matrix_material['Gm'], "V_f": Vf, "G_{12f}": fiber_material['G12f']}
    st.latex(render_latex('Shear Modulus `G12`', shear_modulus['latex'], values))
    st.latex(f"G_{{12}} ={G12:.2f} \\, \\text{{GPa}}")

    st.markdown('***')

if __name__ == "__main__":
    main()