import streamlit as st
import numpy as np
import pandas as pd
from materials import fibers, matrices

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
    }
}

# --------------------------------------

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
        fiber_material = st.selectbox('Fiber Material', list(fibers.keys()), index=default_fiber_index, help="Choose the type of fiber material")
    with col2:
        matrix_material = st.selectbox('Matrix Material', list(matrices.keys()), index=default_matrix_index, help="Choose the type of matrix material")

    Vf = st.slider('Fiber Volume Fraction (Vf)', 0.0, 1.0, 0.6, 0.01, help="Adjust the fiber volume fraction (between 0 and 1)")
    Vm = 1 - Vf

    materials_dataframe(fiber_material, matrix_material)

    st.markdown('***')
    
    f = fibers[fiber_material]
    m = matrices[matrix_material]
    
    # Calculate Young's Modulus (E1) --------------------------------
    E1 = f['E1f'] * Vf + m['Em'] * Vm
    st.subheader('Young’s Modulus `E1`', help="Calculated as the weighted average of the modulus of the fiber and matrix.")
    st.latex(r"E_1 = E_{f}V_{f} + E_{m}V_{m}")
    st.latex(f"E_1 = {f['E1f']} \\times {Vf:.2f} + {m['Em']} \\times {Vm:.2f}")
    st.latex(f"E_1 = {E1:.2f} \\, \\text{{GPa}}")

    st.markdown('***')

    # Shear Modulus (G12) --------------------------------
    st.subheader(f'Shear Modulus `G12`', help="Calculated using the selected theory model for shear modulus.")
    theory = st.radio('Theory model for shear modulus', list(theories.keys()), horizontal=True, help="Select the theory model for shear modulus calculations")

    G12 = theories[theory]["shear_modulus"](f, m, Vf, Vm)
    st.latex(r"G_{12} = \frac{G_m}{1 - \sqrt{V_f}(1 - \frac{G_m}{G_{12f}})}")
    st.latex(f"G_{{12}} = {m['Gm']:.2f} / (1 - \\sqrt{{{Vf:.2f}}}(1 - {m['Gm']:.2f}/{f['G12f']:.2f}))")
    st.latex(f"G_{{12}} ={G12:.2f} \\, \\text{{GPa}}")

    st.markdown('***')

    # Poisson's Ratio (ν12) --------------------------------
    st.subheader('Poisson’s Ratio `ν12`', help="Calculated using the selected theory model for Poisson's ratio.")
    theory_poisson = st.radio('Theory model for Poisson’s Ratio', list(theories.keys()), horizontal=True, help="Select the theory model for Poisson’s Ratio calculations")

    v12 = theories[theory_poisson]["poisson_ratio"](f, m, Vf, Vm)
    st.latex(r"\nu_{12} = \nu_{f}V_{f} + \nu_{m}V_{m}")
    st.latex(f"\\nu_{{12}} = {f['v12f']} \\times {Vf:.2f} + {m['vm']} \\times {Vm:.2f}")
    st.latex(f"\\nu_{{12}} = {v12:.2f}")

    st.markdown('***')

    # Tensile Strength (F1T) --------------------------------
    st.subheader('Tensile Strength `F1T`', help="Calculated using the selected theory model for tensile strength.")
    theory_tensile = st.radio('Theory model for Tensile Strength', list(theories.keys()), horizontal=True, help="Select the theory model for tensile strength calculations")

    F1T = theories[theory_tensile]["tensile_strength"](f, m, Vf, Vm)
    st.latex(r"F_{1T} = F_{fT}V_{f} + F_{mT}V_{m}")
    st.latex(f"F_{{1T}} = {f['F1ft']} \\times {Vf:.2f} + {m['FmT']} \\times {Vm:.2f}")
    st.latex(f"F_{{1T}} = {F1T:.2f} \\, \\text{{MPa}}")

    st.markdown('***')

    # Compressive Strength (F1C) --------------------------------
    st.subheader('Compressive Strength `F1C`', help="Calculated using empirical formula for compressive strength.")
    F1C = (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm)
    st.latex(r"F_{1C} = \frac{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3})\varepsilon_{m}}{\nu_{f}V_{f} + \nu_{m}V_{m}}")
    st.latex(f"F_{{1C}} = \\frac{{({f['E1f']} \\times {Vf:.2f} + {m['Em']} \\times {Vm:.2f})(1 - {Vf:.2f}^{1/3}) \\times {m['FmC']} }}{{ {f['v12f']} \\times {Vf:.2f} + {m['vm']} \\times {Vm:.2f} }}")
    st.latex(f"F_{{1C}} = {F1C:.2f} \\, \\text{{MPa}}")

    st.markdown('***')

    # Transverse Tensile Strength (F2T) --------------------------------
    st.subheader('Transverse Tensile Strength `F2T`', help="Calculated using Nielsen empirical formula for transverse tensile strength.")
    F2T = (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3)))
    st.latex(r"F_{2T} = \frac{E_{2f} \cdot F_{mT}}{E_{m} \cdot (1 - V_{f}^{1/3})}")
    st.latex(f"F_{{2T}} = \\frac{{{f['E2f']} \\times {m['FmT']}}}{{{m['Em']} \\times (1 - {Vf:.2f}^{1/3})}}")
    st.latex(f"F_{{2T}} = {F2T:.2f} \\, \\text{{MPa}}")

    st.markdown('***')

    # Transverse Compressive Strength (F2C) --------------------------------
    st.subheader('Transverse Compressive Strength `F2C`', help="Calculated using empirical formula for transverse compressive strength.")
    F2C = m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f']))
    st.latex(r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]")
    st.latex(f"F_{{2C}} = {m['FmC']} \\times \\left[1 + ({Vf:.2f} - {Vf:.2f}^{{1/2}}) \\times \\left(1 - \\frac{{{m['Em']}}}{{{f['E2f']}}}\\right)\\right]")
    st.latex(f"F_{{2C}} = {F2C:.2f} \\, \\text{{MPa}}")

    st.markdown('***')

    # Transverse Tensile Strength (F2T) --------------------------------
    st.subheader('Transverse Tensile Strength `F2T`', help="Calculated using Nielsen empirical formula for transverse tensile strength.")
    F2T = (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3)))
    st.latex(r"F_{2T} = \frac{E_{2f} \cdot F_{mT}}{E_{m} \cdot (1 - V_{f}^{1/3})}")
    st.latex(f"F_{{2T}} = \\frac{{{f['E2f']} \\times {m['FmT']}}}{{{m['Em']} \\times (1 - {Vf:.2f}^{1/3})}}")
    st.latex(f"F_{{2T}} = {F2T:.2f} \\, \\text{{MPa}}")

    st.markdown('***')

    # Transverse Compressive Strength (F2C) --------------------------------
    st.subheader('Transverse Compressive Strength `F2C`', help="Calculated using empirical formula for transverse compressive strength.")
    F2C = m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f']))
    st.latex(r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]")
    st.latex(f"F_{{2C}} = {m['FmC']} \\times \\left[1 + ({Vf:.2f} - {Vf:.2f}^{{1/2}}) \\times \\left(1 - \\frac{{{m['Em']}}}{{{f['E2f']}}}\\right)\\right]")
    st.latex(f"F_{{2C}} = {F2C:.2f} \\, \\text{{MPa}}")

    st.markdown('***')

    # In-plane Shear Strength (F6) --------------------------------
    st.subheader('In-plane Shear Strength `F6`', help="Calculated using empirical formula for in-plane shear strength.")
    
    # Ensure that 'Fms' key exists in the matrix properties
    if 'Fms' in m and 'Gm' in m and 'G12f' in f:
        F6 = m['Fms'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f']))
        st.latex(r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]")
        st.latex(f"F_{{6}} = {m['Fms']} \\times \\left[1 + ({Vf:.2f} - {Vf:.2f}^{{1/2}}) \\times \\left(1 - \\frac{{{m['Gm']}}}{{{f['G12f']}}}\\right)\\right]")
        st.latex(f"F_{{6}} = {F6:.2f} \\, \\text{{MPa}}")
    else:
        st.error("The required material properties for calculating `F6` are not available in the provided data.")

    st.markdown('***')

if __name__ == "__main__":
    main()
