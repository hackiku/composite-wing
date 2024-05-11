import streamlit as st
import numpy as np
from materials import fibers, matrices

def spacer(height='2em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

def display_material_properties(fiber, matrix):
    """Displays selected fiber and matrix material properties."""
    st.write("Selected Fiber Material Properties:")
    st.json(fibers[fiber])
    st.write("Selected Matrix Material Properties:")
    st.json(matrices[matrix])

def calculate_youngs_modulus(f, m, Vf, Vm):
    # Calculate and display Young's Modulus
    E1 = f['E1f'] * Vf + m['Em'] * (1 - Vm)
    st.subheader('Young’s Modulus (E1)')
    st.write("Calculated as the weighted average of the modulus of the fiber and matrix.")
    st.latex(r"E1 = E_{f}V_{f} + E_{m}V_{m}")
    st.latex(f"E1 = {f['E1f']} \\times {Vf:.2f} + {m['Em']} \\times {Vm:.2f}")
    st.latex(f"E1 = {E1:.2f} \\, \\text{{GPa}}")

def calculate_shear_modulus(f, m, Vf, Vm):
    # Calculate and display Shear Modulus using a given model
    G12 = m['Gm'] / (1 - np.sqrt(Vf) * (1 - m['Gm']/f['G12f']))
    st.subheader('Shear Modulus `G12`')
    st.write("Calculated using Chamis model for shear modulus.")
    st.latex(r"G12 = \frac{G_m}{1 - \sqrt{V_f}(1 - \frac{G_m}{G_{12f}})}")
    st.latex(f"G12 = {m['Gm']:.2f} / (1 - \sqrt{{{Vf:.2f}}}(1 - {m['Gm']:.2f}/{f['G12f']:.2f}))")
    st.latex(f"G12 ={G12:.2f} \\, \\text{{GPa}}")

def main():
    st.title('Composite Materials Calculator')

    # Dropdown to select materials
    fiber_material = st.selectbox('Select Fiber Material', list(fibers.keys()))
    matrix_material = st.selectbox('Select Matrix Material', list(matrices.keys()))

    # Slider for fiber volume fraction
    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01)
    Vm = 1 - Vf

    # Display selected material properties
    display_material_properties(fiber_material, matrix_material)

    # Calculate and display mechanical properties
    calculate_youngs_modulus(fibers[fiber_material], matrices[matrix_material], Vf, Vm)
    st.markdown('***')
    calculate_shear_modulus(fibers[fiber_material], matrices[matrix_material], Vf, Vm)
    st.markdown('***')


if __name__ == "__main__":
    main()
