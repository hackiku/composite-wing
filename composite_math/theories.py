# composite_math/theories.py

import numpy as np

# Dictionary to hold the categories and their respective theories
theory_categories = {
    "Micromechanics": [
        "E1_modulus",
        "E2_modulus",
        "shear_modulus",
        "poisson_ratio"
    ],
    "Strength": [
        "tensile_strength",
        "compressive_strength",
        "transverse_tensile_strength",
        "transverse_compressive_strength",
        "in_plane_shear_strength"
    ],
    "Failure": [
        "Tsai-Wu",
        "Tsai-Hill"
    ]
}

# Define micromechanics theories
micromechanics_theories = {
    "E1_modulus": {
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_1 = {f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}"
        },
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m"
        },
        "Inverse Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: 1 / (Vf / f['E1f'] + Vm / m['Em']),
            "latex": r"\frac{1}{E_1} = \frac{V_f}{E_{1f}} + \frac{V_m}{E_m}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
            "latex": r"E_1 = \frac{E_{1f} \cdot E_m}{V_f \cdot E_m + V_m \cdot E_{1f}}"
        },
    },
    "E2_modulus": {
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E2f'] * Vf + m['Em'] * Vm,
            "latex": r"E_2 = E_{2f}V_f + E_mV_m"
        },
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E2f'] * Vf + m['Em'] * Vm,
            "latex": r"E_2 = E_{2f}V_f + E_mV_m"
        },
        "Inverse Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: 1 / (Vf / f['E2f'] + Vm / m['Em']),
            "latex": r"\frac{1}{E_2} = \frac{V_f}{E_{2f}} + \frac{V_m}{E_m}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E2f']),
            "latex": r"E_2 = \frac{E_{2f} \cdot E_m}{V_f \cdot E_m + V_m \cdot E_{2f}}"
        },
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
                    "latex": r"\xi = \frac{\frac{G_{12f}}{G_m} - 1}{\frac{G_{12f}}{G_m} + 2}"
                }
            }
        },
    },
    "poisson_ratio": {
        "unit": "-",
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
    }
}

# Define strength theories
strength_theories = {
    "tensile_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = F_{1ft}V_f + F_mTV_m",
            "math": lambda f, m, Vf, Vm: f"F_{{1T}} = {f['F1ft']} \cdot {Vf:.3f} + {m['FmT']} \cdot {Vm:.3f}"
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
        "Timoshenko-Gere": {
            "formula": lambda f, m, Vf, Vm: ((1 - Vf**0.5) * f['F1ft'] + Vf**0.5 * m['FmC']),
            "latex": r"F_{1C} = (1 - V_f^{1/2}) F_{1ft} + V_f^{1/2} F_{mC}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmC'] * Vm,
            "latex": r"F_{1C} = F_{1ft}V_f + F_mCV_m"
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
        }
    }
}

# Define failure theories
failure_theories = {
    "Tsai-Wu": {
        "formula": lambda sigma, F: (F['F1'] * sigma['sigma1'] + F['F2'] * sigma['sigma2'] + 
                                      F['F11'] * sigma['sigma1']**2 + F['F22'] * sigma['sigma2']**2 + 
                                      2 * F['F12'] * sigma['sigma1'] * sigma['sigma2'] + 
                                      F['F66'] * sigma['tau12']**2),
        "latex": r"F_1 \sigma_1 + F_2 \sigma_2 + F_{11} \sigma_1^2 + F_{22} \sigma_2^2 + 2 F_{12} \sigma_1 \sigma_2 + F_{66} \tau_{12}^2 = 1"
    },
    "Tsai-Hill": {
        "formula": lambda sigma, F: ((sigma['sigma1'] / F['F1t'])**2 - sigma['sigma1'] * sigma['sigma2'] / F['F1t']**2 + (sigma['sigma2'] / F['F2t'])**2 + (sigma['tau12'] / F['F6'])**2),
        "latex": r"\left( \frac{\sigma_1}{F_{1t}} \right)^2 - \frac{\sigma_1 \sigma_2}{F_{1t}^2} + \left( \frac{\sigma_2}{F_{2t}} \right)^2 + \left( \frac{\tau_{12}}{F_6} \right)^2 = 1"
    }
}
