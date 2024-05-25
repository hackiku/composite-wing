import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
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
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (f['E1f'] - np.sqrt(Vf) * (f['E1f'] - m['Em'])),
            "latex": r"E_1 = \frac{{E_{1f} \cdot E_m}}{{E_{1f} - \sqrt{V_f} \cdot (E_{1f} - E_m)}}"
        },
        "shear_modulus": {
            "formula": lambda f, m, Vf, Vm: (f['G12f'] * m['Gm']) / (f['G12f'] - np.sqrt(Vf) * (f['G12f'] - m['Gm'])),
            "latex": r"G_{12} = \frac{{G_{12f} \cdot G_m}}{{G_{12f} - \sqrt{V_f} \cdot (G_{12f} - G_m)}}"
        },
        "poisson_ratio": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = {v12f}V_f + {vm}V_m"
        },
        "tensile_strength": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = {F1ft}V_f + {FmT}V_m"
        },
        "compressive_strength": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3}) \epsilon_{m}}}{{\nu_{f}V_{f} + \nu_{m}V_{m}}}"
        },
        "transverse_tensile_strength": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{{E_{2f} \cdot F_{mT}}}{{E_{m} \cdot (1 - V_{f}^{1/3})}}"
        },
        "transverse_compressive_strength": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]"
        },
        "in_plane_shear_strength": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]"
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
        },
        "poisson_ratio": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = {v12f}V_f + {vm}V_m"
        },
        "tensile_strength": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = {F1ft}V_f + {FmT}V_m"
        },
        "compressive_strength": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3}) \epsilon_{m}}}{{\nu_{f}V_{f} + \ну_{m}V_{m}}}"
        },
        "transverse_tensile_strength": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{{E_{2f} \cdot F_{mT}}}{{E_{m} \cdot (1 - V_{f}^{1/3})}}"
        },
        "transverse_compressive_strength": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]"
        },
        "in_plane_shear_strength": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]"
        }
    },
    "Halpin-Tsai": {
        "youngs_modulus": {
            "formula": lambda f, m, Vf, Vm: ((f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f'])),
            "latex": r"E_1 = \frac{{E1f \cdot Em}}{{V_f \cdot Em + V_m \cdot E1f}}"
        },
        "shear_modulus": {
            "formula": lambda f, m, Vf, Vm: ((f['G12f'] * m['Gm']) / (Vf * m['Gm'] + Vm * f['G12f'])),
            "latex": r"G_{12} = \frac{{G12f \cdot Gm}}{{V_f \cdot Gm + V_m \cdot G12f}}"
        },
        "poisson_ratio": {
            "formula": lambda f, m, Vf, Vm: ((f['v12f'] * m['vm']) / (Vf * m['vm'] + Vm * f['v12f'])),
            "latex": r"\nu_{12} = \frac{{v12f \cdot vm}}{{V_f \cdot vm + V_m \cdot v12f}}"
        },
        "tensile_strength": {
            "formula": lambda f, m, Vf, Vm: ((f['F1ft'] * m['FmT']) / (Vf * m['FmT'] + Vm * f['F1ft'])),
            "latex": r"F_{1T} = \frac{{F1ft \cdot FmT}}{{V_f \cdot FmT + V_m \cdot F1ft}}"
        },
        "compressive_strength": {
            "formula": lambda f, m, Vf, Vm: ((f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm)),
            "latex": r"F_{1C} = \frac{{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3}) \epsilon_{m}}}{{\nu_{f}V_{f} + \ну_{m}V_{m}}}"
        },
        "transverse_tensile_strength": {
            "formula": lambda f, m, Vf, Vm: ((f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3)))),
            "latex": r"F_{2T} = \frac{{E_{2f} \cdot F_{mT}}}{{E_{m} \cdot (1 - V_{f}^{1/3})}}"
        },
        "transverse_compressive_strength": {
            "formula": lambda f, m, Vf, Vm: (m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f']))),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]"
        },
        "in_plane_shear_strength": {
            "formula": lambda f, m, Vf, Vm: ((m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])))),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]"
        }
    },
    "Tsai-Wu": {
        "failure_criterion": {
            "formula": lambda sigma, F: (F['F1'] * sigma['sigma1'] + F['F2'] * sigma['sigma2'] + F['F11'] * sigma['sigma1']**2 + F['F22'] * sigma['sigma2']**2 + 2 * F['F12'] * sigma['sigma1'] * sigma['sigma2'] + F['F66'] * sigma['tau12']**2),
            "latex": r"F_1 \sigma_1 + F_2 \sigma_2 + F_{11} \sigma_1^2 + F_{22} \sigma_2^2 + 2 F_{12} \sigma_1 \sigma_2 + F_{66} \tau_{12}^2 = 1"
        }
    },
    "Tsai-Hill": {
        "failure_criterion": {
            "formula": lambda sigma, F: ((sigma['sigma1'] / F['F1t'])**2 - sigma['sigma1'] * sigma['sigma2'] / F['F1t']**2 + (sigma['sigma2'] / F['F2t'])**2 + (sigma['tau12'] / F['F6'])**2),
            "latex": r"\left( \frac{\sigma_1}{F_{1t}} \right)^2 - \frac{\sigma_1 \sigma_2}{F_{1t}^2} + \left( \frac{\sigma_2}{F_{2t}} \right)^2 + \left( \frac{\tau_{12}}{F_6} \right)^2 = 1"
        }
    }
}

mplstyle.use('dark_background')

def plot_properties(results_df):
    # Transpose the DataFrame for easier plotting
    results_df = results_df.set_index("Property").transpose()

    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot each property
    for property_name in results_df.columns:
        ax.plot(results_df.index, results_df[property_name], marker='o', label=property_name)

    ax.set_title('Comparison of Composite Properties by Theory', color='white')
    ax.set_xlabel('Theory', color='white')
    ax.set_ylabel('Value', color='white')
    ax.legend()
    ax.grid(True, color='gray')

    # Set the color of the tick labels
    ax.tick_params(colors='white')

    st.pyplot(fig)



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
    properties = ["Young's Modulus `E1`", "Shear Modulus `G12`", "Poisson's Ratio `ν12`", "Tensile Strength `F1T`", 
                  "Compressive Strength `F1C`", "Transverse Tensile Strength `F2T`", "Transverse Compressive Strength `F2C`",
                  "In-plane Shear Strength `F6`"]
    results = {"Property": properties}

    for theory_name, theory_details in theories.items():
        E1 = theory_details['youngs_modulus']['formula'](fiber_material, matrix_material, Vf, Vm) if "youngs_modulus" in theory_details else None
        G12 = theory_details['shear_modulus']['formula'](fiber_material, matrix_material, Vf, Vm) if "shear_modulus" in theory_details else None
        v12 = theory_details['poisson_ratio']['formula'](fiber_material, matrix_material, Vf, Vm) if "poisson_ratio" in theory_details else None
        F1T = theory_details['tensile_strength']['formula'](fiber_material, matrix_material, Vf, Vm) if "tensile_strength" in theory_details else None
        F1C = theory_details['compressive_strength']['formula'](fiber_material, matrix_material, Vf, Vm) if "compressive_strength" in theory_details else None
        F2T = theory_details['transverse_tensile_strength']['formula'](fiber_material, matrix_material, Vf, Vm) if "transverse_tensile_strength" in theory_details else None
        F2C = theory_details['transverse_compressive_strength']['formula'](fiber_material, matrix_material, Vf, Vm) if "transverse_compressive_strength" in theory_details else None
        F6 = theory_details['in_plane_shear_strength']['formula'](fiber_material, matrix_material, Vf, Vm) if "in_plane_shear_strength" in theory_details else None
        
        results[theory_name] = [E1, G12, v12, F1T, F1C, F2T, F2C, F6]

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Display the DataFrame
    st.subheader("Calculated Properties by Theory")
    st.dataframe(results_df)
    
    plot_properties(results_df)


    # --------------------- LATEX ---------------------

    st.markdown('***')

    # Select theory
    theory = st.radio('Select theory for calculations', list(theories.keys()), horizontal=True)

    # The rest of the app continues...

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