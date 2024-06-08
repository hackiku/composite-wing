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
            "formula": lambda f, m, Vf, Vm, **kwargs: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_{{1}} = {f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}"
        },
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_{{1}} = {f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}"
        },
        "Inverse Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: 1 / (Vf / f['E1f'] + Vm / m['Em']),
            "latex": r"\frac{1}{E_1} = \frac{V_f}{E_{1f}} + \frac{V_m}{E_m}",
            "math": lambda f, m, Vf, Vm: f"\frac{{1}}{{E_{{1}}}} = \frac{{{Vf:.3f}}}{{{f['E1f']}}} + \frac{{{Vm:.3f}}}{{{m['Em']}}}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
            "latex": r"E_1 = \frac{E_{1f} \cdot E_m}{V_f \cdot E_m + V_m \cdot E_{1f}}",
            "math": lambda f, m, Vf, Vm: f"E_{{1}} = \frac{{{f['E1f']} \cdot {m['Em']}}}{{{Vf:.3f} \cdot {m['Em']} + {Vm:.3f} \cdot {f['E1f']}}}"
        },
    },
    "E2_modulus": {
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E2f'] * Vf + m['Em'] * Vm,
            "latex": r"E_2 = E_{2f}V_f + E_mV_m",
        },
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E2f'] * Vf + m['Em'] * Vm,
            "latex": r"E_2 = E_{2f}V_f + E_mV_m",
        },
        "Inverse Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: 1 / (Vf / f['E2f'] + Vm / m['Em']),
            "latex": r"\frac{1}{E_2} = \frac{V_f}{E_{2f}} + \frac{V_m}{E_m}",
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E2f']),
            "latex": r"E_2 = \frac{E_{2f} \cdot E_m}{V_f \cdot E_m + V_m \cdot E_{2f}}",
        },
    },
    "shear_modulus": {
        "unit": "GPa",
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['G12f'] * Vf + m['Gm'] * Vm,
            "latex": r"G_{12} = G_{12f}V_f + G_mV_m",
            "math": lambda f, m, Vf, Vm: f"G_{{12}} = {f['G12f']} \cdot {Vf:.3f} + {m['Gm']} \cdot {Vm:.3f}"
        },
        "Hashin-Rosen": {
            "formula": lambda f, m, Vf, Vm: (m['Gm'] * (f['G12f'] * (1 + Vf) + m['Gm'] * Vm)) / (f['G12f'] * Vm + m['Gm'] * (1 + Vf)),
            "latex": r"G_{12} = G_m \frac{G_{12f} (1 + V_f) + G_m V_m}{G_{12f} V_m + G_m (1 + V_f)}",
            "math": lambda f, m, Vf, Vm: f"G_{{12}} = {m['Gm']} \cdot \frac{{{f['G12f']} \cdot (1 + {Vf:.3f}) + {m['Gm']} \cdot {Vm:.3f}}}{{{f['G12f']} \cdot {Vm:.3f} + {m['Gm']} \cdot (1 + {Vf:.3f})}}"
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
            "latex": r"\nu_{12} = \nu_{12f}V_f + \nu_mV_m",
            "math": lambda f, m, Vf, Vm: f"\nu_{{12}} = {f['v12f']} \cdot {Vf:.3f} + {m['vm']} \cdot {Vm:.3f}"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['v12f'] * Vf + m['vm'] * Vm,
            "latex": r"\nu_{12} = \nu_{12f}V_f + \nu_mV_m",
            "math": lambda f, m, Vf, Vm: f"\nu_{{12}} = {f['v12f']} \cdot {Vf:.3f} + {m['vm']} \cdot {Vm:.3f}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['v12f'] * m['vm']) / (Vf * m['vm'] + Vm * f['v12f']),
            "latex": r"\nu_{12} = \frac{\nu_{12f} \cdot \nu_m}{V_f \cdot \nu_m + V_m \cdot \nu_{12f}}",
            "math": lambda f, m, Vf, Vm: f"\nu_{{12}} = \frac{{{f['v12f']} \cdot {m['vm']}}}{{{Vf:.3f} \cdot {m['vm']} + {Vm:.3f} \cdot {f['v12f']}}}"
        }
    }
}



# Define strength theories
strength_theories = {
    "tensile_strength": {
        "unit": "MPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = F_{1ft}V_f + F_mTV_m",
        },
        "Tensile Strength Composite Model": {
            "formula": lambda f, m, Vf, Vm, eps_f, eps_m: f['F1ft'] * (Vf + (Vm * m['Em'] / f['E1f'])) if eps_f <= eps_m else m['FmT'] * ((f['E1f'] / m['Em']) * Vf + Vm),
            "latex": r"F_{1T}"
        }
    },
    "compressive_strength": {
        "unit": "MPa",
        "Timoshenko-Gere": {
            "formula": lambda f, m, Vf, Vm: 2 * Vf * np.sqrt((Vf * f['E1f'] * m['Em']) / (3 * (1 - Vf))),
            "latex": r"F_{1C} = 2V_f \sqrt{\frac{V_f E_{1f} E_m}{3(1 - V_f)}}",
        },
        "Agarwal-Broutman": {
            "formula": lambda f, m, Vf, Vm, eps_m: ((f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * eps_m) / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{(E_{1f} V_f + E_m V_m) (1 - V_f^{1/3}) \varepsilon_{mu}}{\nu_{12f} V_f + \nu_m V_m}",
        }
    },
    "transverse_tensile_strength": {
        "unit": "MPa",
        "Nielsen": {
            "formula": lambda f, m, Vf, Vm: (1 - Vf**(1/3)) * (f['E2f'] * m['FmT']) / m['Em'],
            "latex": r"F_{2T} = \left( 1 - V_f^{1/3} \right) \frac{E_{2f} F_{mT}}{E_m}"
        },
        # "Barbero": {
        #     "formula": lambda f, m, Vf, Vm, Vvoid: m['FmT'] * (1 - np.sqrt((4 * Vvoid) / (np.pi * Vm))) * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Em'] / f['E2f'])),
        #     "latex": r"F_{2T} = F_{mT} \left( 1 - \sqrt{\frac{4 V_{void}}{\pi V_m}} \right) \left( 1 + \left( V_f - \sqrt{V_f} \right) \left( 1 - \frac{E_m}{E_{2f}} \right) \right)",
        # }
    },
    "transverse_compressive_strength": {
        "unit": "MPa",
        "Weeton": {
            "formula": lambda f, m, Vf, Vm, Vvoid: m['FmC'] * (1 - np.sqrt((4 * Vvoid) / (np.pi * Vm))) * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2C} = F_{mC} \left( 1 - \sqrt{\frac{4 V_{void}}{\pi V_m}} \right) \left( 1 + \left( V_f - \sqrt{V_f} \right) \left( 1 - \frac{E_m}{E_{2f}} \right) \right)",
        }
    },
    "in_plane_shear_strength": {
        "unit": "MPa",
        "Stellbrink": {
            "formula": lambda f, m, Vf, Vm, Vvoid: m['FmS'] * (1 - np.sqrt((4 * Vvoid) / (np.pi * Vm))) * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Gm'] / f['G12f'])),
            "latex": r"F_{6} = F_{mS} \left( 1 - \sqrt{\frac{4 V_{void}}{\pi V_m}} \right) \left( 1 + \left( V_f - \sqrt{V_f} \right) \left( 1 - \frac{G_m}{G_{12f}} \right) \right)",
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
