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

def calculate_properties(f, m, Vf, Vm, theory):
    """Calculates and displays mechanical properties based on the selected theory."""
    if theory == "Chamis":
        E1 = f['E1f'] * Vf + m['Em'] * Vm
        G12 = m['Gm'] / (1 - np.sqrt(Vf) * (1 - m['Gm']/f['G12f']))
    elif theory == "Theory 2":
        # Placeholder for Theory 2 calculations
        E1 = G12 = 0
    elif theory == "Theory 3":
        # Placeholder for Theory 3 calculations
        E1 = G12 = 0
    elif theory == "Theory 4":
        # Placeholder for Theory 4 calculations
        E1 = G12 = 0
    else:
        st.error("Unknown theory selected.")
        return
    
    st.subheader(f'Young’s Modulus (E1) using {theory}', help="Calculated as the weighted average of the modulus of the fiber and matrix.")
    st.latex(r"E_1 = E_{f}V_{f} + E_{m}V_{m}")
    st.latex(f"E_1 = {f['E1f']} \\times {Vf:.2f} + {m['Em']} \\times {Vm:.2f}")
    st.latex(f"E_1 = {E1:.2f} \\, \\text{{GPa}}")

    st.subheader(f'Shear Modulus (G12) using {theory}', help="Calculated using the selected theory model for shear modulus.")
    st.latex(r"G_{12} = \frac{G_m}{1 - \sqrt{V_f}(1 - \frac{G_m}{G_{12f}})}")
    st.latex(f"G_{{12}} = {m['Gm']:.2f} / (1 - \\sqrt{{{Vf:.2f}}}(1 - {m['Gm']:.2f}/{f['G12f']:.2f}))")
    st.latex(f"G_{{12}} ={G12:.2f} \\, \\text{{GPa}}")

def main():
    st.title('Composite Materials Calculator')

    # Dropdown to select materials
    fiber_material = st.selectbox('Select Fiber Material', list(fibers.keys()), help="Choose the type of fiber material")
    matrix_material = st.selectbox('Select Matrix Material', list(matrices.keys()), help="Choose the type of matrix material")

    # Slider for fiber volume fraction
    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf

    # Radio buttons for selecting the theory model
    theory = st.radio('Select Theory Model', ['Chamis', 'Theory 2', 'Theory 3', 'Theory 4'], horizontal=True, help="Select the theory model for calculations")

    # Display selected material properties as DataFrames
    materials_dataframe(fiber_material, matrix_material)

    # Calculate and display mechanical properties
    calculate_properties(fibers[fiber_material], matrices[matrix_material], Vf, Vm, theory)
    st.markdown('***')

if __name__ == "__main__":
    main()
