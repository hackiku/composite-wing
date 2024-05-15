import streamlit as st
import numpy as np
import pandas as pd
from materials import fibers, matrices

def spacer(height='2em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

def materials_dataframe(fiber, matrix):
    """Displays selected fiber and matrix material properties as an inverted DataFrame."""
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber], orient='index', columns=[fiber]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix], orient='index', columns=[matrix]).transpose()
    st.write("Selected Fiber Material Properties:")
    st.dataframe(fiber_properties)
    st.write("Selected Matrix Material Properties:")
    st.dataframe(matrix_properties)

# Define the calculation theories as a dictionary
theories = {
    "Chamis": {
        "youngs_modulus": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
        "shear_modulus": lambda f, m, Vf, Vm: m['Gm'] / (1 - np.sqrt(Vf) * (1 - m['Gm'] / f['G12f'])),
        "poisson_ratio": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
        "tensile_strength": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
    },
    "Rule of Mixtures": {
        "youngs_modulus": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
        "shear_modulus": lambda f, m, Vf, Vm: f['G12f'] * Vf + m['Gm'] * Vm,
        "poisson_ratio": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
        "tensile_strength": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
    },
    "Halpin-Tsai": {
        "youngs_modulus": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
        "shear_modulus": lambda f, m, Vf, Vm: f['G12f'] * (1 + 0.6 * Vf) / (1 - 0.6 * Vf),
        "poisson_ratio": lambda f, m, Vf, Vm: ((f['v12f'] * m['vm']) / (Vf * m['vm'] + Vm * f['v12f'])),
        "tensile_strength": lambda f, m, Vf, Vm: (f['F1ft'] * m['FmT']) / (Vf * m['FmT'] + Vm * f['F1ft']),
    },
    "Theory 4": {
        "youngs_modulus": lambda f, m, Vf, Vm: 0,  # Placeholder for Theory 4
        "shear_modulus": lambda f, m, Vf, Vm: 0,  # Placeholder for Theory 4
        "poisson_ratio": lambda f, m, Vf, Vm: 0,  # Placeholder for Theory 4
        "tensile_strength": lambda f, m, Vf, Vm: 0,  # Placeholder for Theory 4
    }
}

def main():
    st.title('Composite Materials Calculator')

    # Button to display the whole DataFrame
    if st.button('Show All Material Data'):
        fiber_df = pd.DataFrame(fibers).transpose()
        matrix_df = pd.DataFrame(matrices).transpose()
        st.write("Fiber Materials Data")
        st.dataframe(fiber_df)
        st.write("Matrix Materials Data")
        st.dataframe(matrix_df)

    # Dropdown to select materials
    col1, col2 = st.columns(2)
    with col1:
        fiber_material = st.selectbox('Fiber Material', list(fibers.keys()), help="Choose the type of fiber material")
    with col2:
        matrix_material = st.selectbox('Matrix Material', list(matrices.keys()), help="Choose the type of matrix material")

    # Slider for fiber volume fraction
    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf

    # Display selected material properties as DataFrames
    materials_dataframe(fiber_material, matrix_material)

    st.markdown('***')
    
    f = fibers[fiber_material]
    m = matrices[matrix_material]
    
    # Calculate Young's Modulus (E1)
    E1 = f['E1f'] * Vf + m['Em'] * Vm
    st.subheader('Young’s Modulus `E1`', help="Calculated as the weighted average of the modulus of the fiber and matrix.")
    st.latex(r"E_1 = E_{f}V_{f} + E_{m}V_{m}")
    st.latex(f"E_1 = {f['E1f']} \\times {Vf:.2f} + {m['Em']} \\times {Vm:.2f}")
    st.latex(f"E_1 = {E1:.2f} \\, \\text{{GPa}}")

    st.markdown('***')

    # Shear Modulus (G12)
    st.subheader(f'Shear Modulus `G12`', help="Calculated using the selected theory model for shear modulus.")
    theory = st.radio('Theory model for shear modulus', list(theories.keys()), horizontal=True, help="Select the theory model for shear modulus calculations")

    G12 = theories[theory]["shear_modulus"](f, m, Vf, Vm)
    st.latex(r"G_{12} = \frac{G_m}{1 - \sqrt{V_f}(1 - \frac{G_m}{G_{12f}})}")
    st.latex(f"G_{{12}} = {m['Gm']:.2f} / (1 - \\sqrt{{{Vf:.2f}}}(1 - {m['Gm']:.2f}/{f['G12f']:.2f}))")
    st.latex(f"G_{{12}} ={G12:.2f} \\, \\text{{GPa}}")

    st.markdown('***')

if __name__ == "__main__":
    main()
