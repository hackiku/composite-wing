import streamlit as st
import numpy as np
from materials import fibers, matrices

def spacer(height='2em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)


def main():
    st.title('Composite Materials Calculator')

    # Dropdown to select materials
    fiber_material = st.selectbox('Select Fiber Material', list(fibers.keys()))
    matrix_material = st.selectbox('Select Matrix Material', list(matrices.keys()))

    # Slider for fiber volume fraction
    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01)
    Vm = 1 - Vf

    # Display selected material properties in a DataFrame or table format
    st.write("Selected Fiber Material Properties:")
    st.json(fibers[fiber_material])

    st.write("Selected Matrix Material Properties:")
    st.json(matrices[matrix_material])

    # Function to calculate properties
    def calculate_properties(fiber, matrix, Vf):
        f = fibers[fiber]
        m = matrices[matrix]
        
        # Calculations using formulas
        E1 = f['E1f'] * Vf + m['Em'] * (1 - Vf)
        # Display calculation steps
        st.subheader('Young’s Modulus (E1)')
        st.write("Calculated as the weighted average of the modulus of the fiber and matrix.")
        st.latex(r"E1 = E_{f}V_{f} + E_{m}V_{m}")
        st.latex(f"E1 = {f['E1f']} \\times {Vf:.2f} + {m['Em']} \\times {Vm:.2f}")
        st.latex(f"E1 = {E1:.2f} \\, \\text{{GPa}}")

    # Run calculations
    calculate_properties(fiber_material, matrix_material, Vf)

    st.markdown('***')


if __name__ == "__main__":
    main()
