# calculations.py
import numpy as np

def calculate_xi(G12f, Gm):
    return (G12f / Gm - 1) / (G12f / Gm + 2)

theories = {
    "youngs_modulus": {
        "unit": "GPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (f['E1f'] - np.sqrt(Vf) * (f['E1f'] - m['Em'])),
            "latex": r"E_1 = \frac{{E_{1f} \cdot E_m}}{{E_{1f} - \sqrt{V_f} \cdot (E_{1f} - E_m)}}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
            "latex": r"E_1 = \frac{{E_{1f} \cdot E_m}}{{V_f \cdot E_m + V_m \cdot E_{1f}}}"
        }
    },
    "shear_modulus": {
        "unit": "GPa",
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['G12f'] * Vf + m['Gm'] * Vm,
            "latex": r"G_{12} = G_{12f}V_f + G_mV_m"
        },
        "Hashin-Rosen": {
            "formula": lambda f, m, Vf, Vm: (m['Gm'] * (f['G12f'] * (1 + Vf) + m['Gm'] * Vm)) / (f['G12f'] * Vm + m['Gm'] * (1 + Vf)),
            "latex": r"G_{12} = G_m \frac{G_{12f} (1 + V_f) + G_m V_m}{G_{12f} V_m + G_m (1 + V_f)}"
        },
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: m['Gm'] / (1 - np.sqrt(Vf) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"G_{12} = \frac{G_m}{1 - \sqrt{V_f} \left( 1 - \frac{G_m}{G_{12f}} \right)}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm, xi: m['Gm'] * ((1 + 2 * xi * Vf) / (1 - xi * Vf)),
            "latex": r"G_{12} = G_m \left( \frac{1 + 2 \cdot \xi \cdot V_f}{1 - \xi \cdot V_f} \right)",
            "coefficients": {
                "xi": {
                    "formula": lambda f, m: (f['G12f'] / m['Gm'] - 1) / (f['G12f'] / m['Gm'] + 2),
                    "latex": r"\xi = \frac{\frac{G_{12f}}{G_m} - 1}{\frac{G_{12f}}{G_m} + 2}",
                    "default": 0.5
                }
            }
        },
        "Modified Rule of Mixtures (MROM)": {
            "formula": lambda f, m, Vf, Vm, eta: 1 / ((Vf / f['G12f']) + (eta * Vm / m['Gm'])),
            "latex": r"\frac{1}{G_{12}} = \frac{V_f}{G_{12f}} + \frac{\eta' V_m}{G_m}",
            "coefficients": {
                "eta": {
                    "default": 0.6,
                    "latex": r"\eta"
                }
            }
        }
    },
    "poisson_ratio": {
        "unit": "dimensionless",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = \nu_{12f}V_f + \nu_mV_m"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = \nu_{12f}V_f + \nu_mV_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['v12f'] * m['vm']) / (Vf * m['vm'] + Vm * f['v12f']),
            "latex": r"\nu_{12} = \frac{\nu_{12f} \cdot \nu_m}{V_f \cdot \nu_m + V_m \cdot \nu_{12f}}"
        }
    },
    "tensile_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = F_{1ft}V_f + F_mTV_m"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = F_{1ft}V_f + F_mTV_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['F1ft'] * m['FmT']) / (Vf * m['FmT'] + Vm * f['F1ft']),
            "latex": r"F_{1T} = \frac{F_{1ft} \cdot F_{mT}}{V_f \cdot F_{mT} + V_m \cdot F_{1ft}}"
        }
    },
    "compressive_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{(E_fV_f + E_mV_m)(1 - V_f^{1/3}) \epsilon_m}{\nu_fV_f + \nu_mV_m}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{(E_fV_f + E_mV_m)(1 - V_f^{1/3}) \epsilon_m}{\nu_fV_f + \nu_mV_m}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['FmC'] / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{(E_fV_f + E_mV_m)(1 - V_f^{1/3}) \epsilon_m}{\nu_fV_f + \nu_mV_m}"
        }
    },
    "transverse_tensile_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{E_{2f} \cdot F_{mT}}{E_m \cdot (1 - V_f^{1/3})}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{E_{2f} \cdot F_{mT}}{E_m \cdot (1 - V_f^{1/3})}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['FmT']) / (m['Em'] * (1 - Vf**(1/3))),
            "latex": r"F_{2T} = \frac{E_{2f} \cdot F_{mT}}{E_m \cdot (1 - V_f^{1/3})}"
        }
    },
    "transverse_compressive_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_f - V_f^{1/2}\right) \cdot \left(1 - \frac{E_m}{E_{2f}}\right)\right]"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_f - V_f^{1/2}\right) \cdot \left(1 - \frac{E_m}{E_{2f}}\right)\right]"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: m['FmC'] * (1 + (Vf - Vf**(1/2)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \cdot \left[1 + \left(V_f - V_f^{1/2}\right) \cdot \left(1 - \frac{E_m}{E_{2f}}\right)\right]"
        }
    },
    "in_plane_shear_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_f - V_f^{1/2}\right) \cdot \left(1 - \frac{G_m}{G_{12f}}\right)\right]"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_f - V_f^{1/2}\right) \cdot \left(1 - \frac{G_m}{G_{12f}}\right)\right]"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: m['FmS'] * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{ms} \cdot \left[1 + \left(V_f - V_f^{1/2}\right) \cdot \left(1 - \frac{G_m}{G_{12f}}\right)\right]"
        }
    },
    "failure_criterion": {
        "unit": "dimensionless",
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
        unit = theories[property_name]["unit"]
        for theory_name, theory_details in theories[property_name].items():
            if theory_name == "unit":
                continue
            if theory_name not in results:
                results[theory_name] = []
            
            formula = theory_details["formula"]

            # Handle coefficients if they exist
            if 'coefficients' in theory_details:
                coefficients = {}
                for coeff_name, coeff_details in theory_details['coefficients'].items():
                    if 'formula' in coeff_details:
                        coefficients[coeff_name] = coeff_details['formula'](fiber_material, matrix_material)
                    else:
                        coefficients[coeff_name] = coeff_details['default']
                result = formula(fiber_material, matrix_material, Vf, Vm, **coefficients)
            else:
                result = formula(fiber_material, matrix_material, Vf, Vm)
            
            results[theory_name].append(result)
    
    return results
