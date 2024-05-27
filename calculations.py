# calculations.py
import numpy as np

theories = {
    "youngs_modulus": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (f['E1f'] - np.sqrt(Vf) * (f['E1f'] - m['Em'])),
            "latex": r"E_1 = \frac{{E_{1f} \cdot E_m}}{{E_{1f} - \sqrt{V_f} \cdot (E_{1f} - E_m)}}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = {E1f}V_f + {Em}V_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
            "latex": r"E_1 = \frac{{E1f \cdot Em}}{{V_f \cdot Em + V_m \cdot E1f}}"
        }
    },
    "shear_modulus": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['G12f'] * m['Gm']) / (f['G12f'] - np.sqrt(Vf) * (f['G12f'] - m['Gm'])),
            "latex": r"G_{12} = \frac{{G_{12f} \cdot G_m}}{{G_{12f} - \sqrt{V_f} \cdot (G_{12f} - G_m)}}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['G12f'] * Vf + m['Gm'] * Vm,
            "latex": r"G_{12} = {G12f}V_f + {G_m}V_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['G12f'] * m['Gm']) / (Vf * m['Gm'] + Vm * f['G12f']),
            "latex": r"G_{12} = \frac{{G12f \cdot Gm}}{{V_f \cdot Gm + V_m \cdot G12f}}"
        }
    },
    "poisson_ratio": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = {v12f}V_f + {vm}V_m"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = {v12f}V_f + {vm}V_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['v12f'] * m['vm']) / (Vf * m['vm'] + Vm * f['v12f']),
            "latex": r"\nu_{12} = \frac{{v12f \cdot vm}}{{V_f \cdot vm + V_m \cdot v12f}}"
        }
    },
    "tensile_strength": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = {F1ft}V_f + {FmT}V_m"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = {F1ft}V_f + {FmT}V_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['F1ft'] * m['FmT']) / (Vf * m['FmT'] + Vm * f['F1ft']),
            "latex": r"F_{1T} = \frac{{F1ft \cdot FmT}}{{V_f \cdot FmT + V_m \cdot F1ft}}"
        }
    },
    "compressive_strength": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3}) \epsilon_{m}}}{{\nu_{f}V_{f} + \nu_{m}V_{m}}}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3}) \epsilon_{m}}}{{\nu_{f}V_{f} + \ну_{m}V_{m}}}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{{(E_{f}V_{f} + E_{m}V_{m})(1 - V_{f}^{1/3}) \epsilon_{m}}}{{\nu_{f}V_{f} + \ну_{m}V_{m}}}"
        }
    },
    "transverse_tensile_strength": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{{E_{2f} \cdot F_{mT}}}{{E_{m} \cdot (1 - V_{f}^{1/3})}}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{{E_{2f} \cdot F_{mT}}}{{E_{m} \cdot (1 - V_{f}^{1/3})}}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{{E_{2f} \cdot F_{mT}}}{{E_{m} \cdot (1 - V_{f}^{1/3})}}"
        }
    },
    "transverse_compressive_strength": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{E_{m}}{E_{2f}}\right)\right]"
        }
    },
    "in_plane_shear_strength": {
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_{f} - V_{f}^{1/2}\right) \cdot \left(1 - \frac{G_{m}}{G_{12f}}\right)\right]"
        }
    },
    "failure_criterion": {
        "Tsai-Wu": {
            "formula": lambda sigma, F: (F['F1'] * sigma['sigma1'] + F['F2'] * sigma['sigma2'] + F['F11'] * sigma['sigma1']**2 + F['F22'] * sigma['sigma2']**2 + 2 * F['F12'] * sigma['sigma1'] * sigma['sigma2'] + F['F66'] * sigma['tau12']**2),
            "latex": r"F_1 \sigma_1 + F_2 \sigma_2 + F_{11} \sigma_1^2 + F_{22} \sigma_2^2 + 2 F_{12} \sigma_1 \sigma_2 + F_{66} \tau_{12}^2 = 1"
        },
        "Tsai-Hill": {
            "formula": lambda sigma, F: ((sigma['sigma1'] / F['F1t'])**2 - sigma['sigma1'] * sigma['sigma2'] / F['F1t']**2 + (sigma['sigma2'] / F['F2t'])**2 + (sigma['tau12'] / F['F6'])**2),
            "latex": r"\left( \frac{\sigma_1}{F_{1t}} \right)^2 - \frac{\sigma_1 \sigma_2}{F_{1t}^2} + \left( \frac{\sigma_2}{F_{2t}} \right)^2 + \left( \frac{\tau_{12}}{F_6} \right)^2 = 1"
        }
    }
}

def calculate_properties(fiber_material, matrix_material, Vf, Vm):
    properties = ["youngs_modulus", "shear_modulus", "poisson_ratio", 
                  "tensile_strength", "compressive_strength", 
                  "transverse_tensile_strength", "transverse_compressive_strength",
                  "in_plane_shear_strength"]
    results = {"Property": properties}

    for property_name in properties:
        for theory_name, theory_details in theories[property_name].items():
            if theory_name not in results:
                results[theory_name] = []
            formula = theory_details["formula"]
            result = formula(fiber_material, matrix_material, Vf, Vm)
            results[theory_name].append(result)
    
    return results
