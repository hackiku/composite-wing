import streamlit as st
import numpy as np
from materials import fibers, matrices

def main():
    st.title('Composite Materials Calculator')

    # Dropdown to select materials
    fiber_material = st.selectbox('Select Fiber Material', list(fibers.keys()))
    matrix_material = st.selectbox('Select Matrix Material', list(matrices.keys()))

    # Slider for fiber volume fraction
    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01)
    Vm = 1 - Vf



    # Function to calculate properties
    def calculate_properties(fiber, matrix, Vf):
        f = fibers[fiber]
        m = matrices[matrix]

        # Calculations using formulas
        E1 = f['E1f'] * Vf + m['Em'] * (1 - Vf)
        E2 = m['Em'] / (1 - np.sqrt(Vf) * (1 - m['Em']/f['E2f']))
        G12 = m['Gm'] / (1 - np.sqrt(Vf) * (1 - m['Gm']/f['G12f']))
        v12 = f['v12f'] * Vf + m['vm'] * (1 - Vf)
        F1T = f['F1ft'] * Vf + 0.01086 * m['Em'] * (1 - Vf)

        # Displaying results with LaTeX
        st.subheader('Calculated Properties:')
        st.latex(f"E1 (Longitudinal Modulus) = {E1:.2f} \\, \\text{{GPa}}")
        st.latex(f"E2 (Transverse Modulus) = {E2:.2f} \\, \\text{{GPa}}")
        st.latex(f"G12 (Shear Modulus) = {G12:.2f} \\, \\text{{GPa}}")
        st.latex(f"v12 (Poisson Ratio) = {v12:.2f}")
        st.latex(f"F1T (Tensile Strength along fibers) = {F1T:.2f} \\, \\text{{MPa}}")

    # Automatic update when selections change
    calculate_properties(fiber_material, matrix_material, Vf)

if __name__ == "__main__":
    main()
