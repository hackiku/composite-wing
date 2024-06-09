# material_math/formulas.py

import numpy as np

def calculate_density(rhof, rhom, Vf, Vm):
    rho = rhof * Vf + rhom * Vm
    return rho


micromech_properties = {
    "E1": {
        "name": "Young's longitudinal modulus",
        "help": "Measures the stiffness of the composite in the fiber direction",
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_1 = {f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}"
        },
        "Inverse ROM": {
            "formula": lambda f, m, Vf, Vm: 1 / (Vf / f['E1f'] + Vm / m['Em']),
            "latex": r"\frac{1}{E_1} = \frac{V_f}{E_{1f}} + \frac{V_m}{E_m}",
            "math": lambda f, m, Vf, Vm: f"E_1 = \\frac{{1}}{{\\frac{{{Vf:.3f}}}{f['E1f']} + \\frac{{{Vm:.3f}}}{m['Em']}}}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['E1f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E1f']),
            "latex": r"E_1 = \frac{E_{1f} \cdot E_m}{V_f \cdot E_m + V_m \cdot E_{1f}}",
            "math": lambda f, m, Vf, Vm: f"E_1 = {f['E1f']} \cdot {m['Em']} / {Vf:.3f} \cdot {m['Em']} + {Vm:.3f} \cdot {f['E1f']}"
        },
    "Hashin-Rosen": {
        "formula": lambda f, m, Vf, Vm, Kf, Km, Gm: (
            f['E1f'] * Vf + m['Em'] * Vm +
            (4 * Kf * Km * Gm * Vf * Vm * (m['nim'] - f['ni12f'])**2) /
            (Kf * Km + Gm * (Vf * Kf + Vm * Km))
        ),
        "latex": r"E_1 = E_{f1}V_f + E_mV_m + \frac{4K_f K_m G_m V_f V_m (\nu_m - \nu_{f12})^2}{K_f K_m + G_m (V_f K_f + V_m K_m)}",
        "math": lambda f, m, Vf, Vm, Kf, Km, Gm: f"E_1 = {f['E1f']} \\cdot {Vf:.3f} + {m['Em']} \\cdot {Vm:.3f} + \\frac{{4 \\cdot {Kf} \\cdot {Km:.3f} \\cdot {Gm} \\cdot {Vf:.3f} \\cdot {Vm:.3f} \\cdot ({m['nim']} - {f['ni12f']})^2}}{{{Kf:.3f} \\cdot {Km:.3f} + {Gm:.3f} \\cdot ({Vf:.3f} \\cdot {Kf:.3f} + {Vm:.3f} \\cdot {Km:.3f})}}",
        "coefficients": {
            "Kf": {
                "formula": lambda f, m, Vf, Vm: f['E1f'] / (2 * (1 - 2 * f['ni12f']) * (1 + f['ni12f'])),
                "latex": r"K_f = \frac{E_{f1}}{2(1 - 2\nu_{f12})(1 + \nu_{f12})}"
            },
            "Km": {
                "formula": lambda f, m, Vf, Vm: m['Em'] / (2 * (1 - 2 * m['nim']) * (1 + m['nim'])),
                "latex": r"K_m = \frac{E_m}{2(1 - 2\nu_m)(1 + \nu_m)}"
            },
            "Gm": {
                "formula": lambda f, m: m['Gm'],
                "latex": r"G_m = G_m"
            }
        }
    },

    },
    "E2": {
        "name": "Young's transverse modulus",
        "help": "Measures the stiffness of the composite perpendicular to the fiber direction",
        "unit": "GPa",
        "Inverse ROM": {
            "formula": lambda f, m, Vf, Vm: (f['E2f'] * m['Em']) / (Vf * m['Em'] + Vm * f['E2f']),
            "latex": r"E_2 = \frac{E_{2f} \cdot E_m}{V_f \cdot E_m + V_m \cdot E_{2f}}",
            "math": lambda f, m, Vf, Vm: f"E_2 = \\frac{{{f['E2f']} \\cdot {m['Em']}}}{{{Vf:.3f} \\cdot {m['Em']} + {Vm:.3f} \\cdot {f['E2f']}}}"
        },
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: m['Em'] / (1 - np.sqrt(Vf) * (1 - m['Em'] / f['E2f'])),
            "latex": r"E_2 = \frac{E_m}{1 - \sqrt{V_f} \left( 1 - \frac{E_m}{E_{2f}} \right)}",
            "math": lambda f, m, Vf, Vm: f"E_2 = \\frac{{{m['Em']}}}{{1 - \\sqrt{{{Vf:.3f}}} \\left( 1 - \\frac{{{m['Em']}}}{{{f['E2f']}}} \\right)}}"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: m['Em'] * ((1 + Vf) * f['E2f'] + Vm * m['Em']) / (Vm * f['E2f'] + (1 + Vf) * m['Em']),
            "latex": r"E_2 = E_m \left( \frac{(1 + V_f)E_{2f} + V_m E_m}{V_m E_{2f} + (1 + V_f)E_m} \right)",
            "math": lambda f, m, Vf, Vm: f"E_2 = {m['Em']} \\left( \\frac{{(1 + {Vf:.3f}){f['E2f']} + {Vm:.3f} {m['Em']}}}{{{Vm:.3f} {f['E2f']} + (1 + {Vf:.3f}) {m['Em']}}} \\right)"
        },
        "name": "Young's transverse modulus",
        "help": "Measures the stiffness of the composite perpendicular to the fiber direction",
        "unit": "GPa",
        "Modified IROM": {
            "formula": lambda f, m, Vf, Vm, eta_f, eta_m: 1 / (
                (eta_f * Vf / f['E2f']) + (eta_m * Vm / m['Em'])
            ),
            "latex": r"E_2 = \frac{1}{\frac{\eta_f V_f}{E_{2f}} + \frac{\eta_m V_m}{E_m}}",
            "math": lambda f, m, Vf, Vm, eta_f, eta_m: f"E_2 = \\frac{{1}}{{\\frac{{{eta_f} \\cdot {Vf:.3f}}}{{{f['E2f']}}} + \\frac{{{eta_m} \\cdot {Vm:.3f}}}{{{m['Em']}}}}}",
            "coefficients": {
                "eta_f": {
                    "formula": lambda f, m, Vf, Vm: (f['E1f'] * Vf + ((1 - f['ni12f'] * f['ni21f']) * m['Em'] + m['nim'] * f['ni21f'] * f['E1f']) * Vm) / (f['E1f'] * Vf + m['Em'] * Vm),
                    "latex": r"\eta_f = \frac{E_{f1} V_f + ((1 - \nu_{12f} \nu_{21f}) E_m + \nu_m \nu_{21f} E_{f1}) V_m}{E_{f1} V_f + E_m V_m}"
                },
                "eta_m": {
                    "formula": lambda f, m, Vf, Vm: ((1 - m['nim']**2) * f['E1f'] - (1 - m['nim'] * f['ni12f']) * m['Em'] * Vf + m['Em'] * Vm) / (f['E1f'] * Vf + m['Em'] * Vm),
                    "latex": r"\eta_m = \frac{(1 - \nu_m^2) E_{f1} - (1 - \nu_m \nu_{12f}) E_m V_f + E_m V_m}{E_{f1} V_f + E_m V_m}"
                }
            }
        }
    },


    "G12": {
        "name": "Shear modulus",
        "help": "Measures the shear stiffness of the composite",
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['G12f'] * Vf + m['Gm'] * Vm,
            "latex": r"G_{12} = G_{12f}V_f + G_mV_m"
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
            "formula": lambda f, m, Vf, Vm: 1 / ((Vf / f['G12f']) + (100 * Vm / m['Gm'])),
            "latex": r"\frac{1}{G_{12}} = \frac{V_f}{G_{12f}} + \frac{\eta' V_m}{G_m}"
        }
    },
    "nu12": {
        "name": "Poisson's ratio",
        "help": "Ratio of transverse strain to axial strain",
        "unit": "-",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['ni12f'] * Vf + m['nim'] * Vm,
            "latex": r"\nu_{12} = \nu_{12f}V_f + \nu_mV_m"
        },
        "Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: f['ni12f'] * Vf + m['nim'] * Vm,
            "latex": r"\nu_{12} = \nu_{12f}V_f + \nu_mV_m"
        },
        "Halpin-Tsai": {
            "formula": lambda f, m, Vf, Vm: (f['ni12f'] * m['nim']) / (Vf * m['nim'] + Vm * f['ni12f']),
            "latex": r"\nu_{12} = \frac{\nu_{12f} \cdot \nu_m}{V_f \cdot \nu_m + V_m \cdot \nu_{12f}}"
        }
    }
}

strength_properties = {
    "tensile_strength": {
        "name": "Tensile strength",
        "help": "Maximum stress the composite can withstand while being stretched",
        "unit": "MPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm, Vvoid: f['F1ft'] * Vf + m['FmT'] * Vm * (1 - Vvoid),
            "latex": r"F_{1T} = F_{1ft}V_f + F_mTV_m(1 - V_{void})"
        },
        "Modified ROM": {
            "formula": lambda f, m, Vf, Vm, Vvoid: f['F1ft'] * Vf * 0.9 + m['FmT'] * Vm * (1 - Vvoid),
            "latex": r"F_{1T} = 0.9 (F_{1ft}V_f + F_mTV_m(1 - V_{void}))"
        },
        "Nielsen": {
            "formula": lambda f, m, Vf, Vm, Vvoid: (1 - Vvoid**(1/3)) * f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = (1 - V_{void}^{1/3}) F_{1ft}V_f + F_mTV_m"
        }
    },
    "compressive_strength": {
        "name": "Compressive strength",
        "help": "Maximum stress the composite can withstand while being compressed",
        "unit": "MPa",
        "Timoshenko-Gere": {
            "formula": lambda f, m, Vf, Vm: 2 * Vf * np.sqrt((Vf * f['E1f'] * m['Em']) / (3 * (1 - Vf))),
            "latex": r"F_{1C} = 2V_f \sqrt{\frac{V_f E_{1f} E_m}{3(1 - V_f)}}"
        },
        "Agarwal-Broutman": {
            "formula": lambda f, m, Vf, Vm: ((f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['epsilon_mT']) / (f['ni12f'] * Vf + m['nim'] * Vm),
            "latex": r"F_{1C} = \frac{(E_{1f} V_f + E_m V_m) (1 - V_f^{1/3}) \varepsilon_{mu}}{\nu_{12f} V_f + \nu_m V_m}"
        },
        "Modified ROM": {
            "formula": lambda f, m, Vf, Vm, Vvoid: (f['F1ft'] * Vf + m['FmC'] * Vm) * (1 - Vvoid),
            "latex": r"F_{1C} = (F_{1ft}V_f + F_mCV_m)(1 - V_{void})"
        }
    },
    "transverse_tensile_strength": {
        "name": "Transverse tensile strength",
        "help": "Maximum stress the composite can withstand while being stretched perpendicular to the fiber direction",
        "unit": "MPa",
        "Nielsen": {
            "formula": lambda f, m, Vf, Vm, Vvoid: (1 - Vvoid**(1/3)) * (f['E2f'] * m['FmT']) / m['Em'],
            "latex": r"F_{2T} = \left( 1 - V_{void}^{1/3} \right) \frac{E_{2f} F_{mT}}{E_m}"
        },
        "Barbero": {
            "formula": lambda f, m, Vf, Vm, Vvoid: m['FmT'] * (1 - np.sqrt((4 * Vvoid) / (np.pi * Vm))) * (1 + (Vf - np.sqrt(Vf)) * (1 - m['Em'] / f['E2f'])),
            "latex": r"F_{2T} = F_{mT} \left( 1 - \sqrt{\frac{4 V_{void}}{\pi V_m}} \right) \left( 1 + \left( V_f - \sqrt{V_f} \right) \left( 1 - \frac{E_m}{E_{2f}} \right) \right)"
        },
        "Modified ROM": {
            "formula": lambda f, m, Vf, Vm, Vvoid: (f['F1ft'] * Vf + m['FmT'] * Vm) * (1 - Vvoid),
            "latex": r"F_{2T} = (F_{1ft}V_f + F_mTV_m)(1 - V_{void})"
        }
    }
}

# Failure theories
failure_criteria = {
    "Maximum Stress": {
        "formula": lambda f, m, sigma, F: max(abs(sigma['sigma1']) / F['F1'], abs(sigma['sigma2']) / F['F2'], abs(sigma['tau12']) / F['F6']),
        "latex": r"\max\left( \frac{|\sigma_1|}{F_1}, \frac{|\sigma_2|}{F_2}, \frac{|\tau_{12}|}{F_6} \right)"
    },
    "Tsai-Wu": {
        "formula": lambda f, m, sigma, F: (F['F1'] * sigma['sigma1'] + F['F2'] * sigma['sigma2'] + 
                                      F['F11'] * sigma['sigma1']**2 + F['F22'] * sigma['sigma2']**2 + 
                                      2 * F['F12'] * sigma['sigma1'] * sigma['sigma2'] + 
                                      F['F66'] * sigma['tau12']**2),
        "latex": r"F_1 \sigma_1 + F_2 \sigma_2 + F_{11} \sigma_1^2 + F_{22} \sigma_2^2 + 2 F_{12} \sigma_1 \sigma_2 + F_{66} \tau_{12}^2 = 1"
    },
    "Tsai-Hill": {
        "formula": lambda f, m, sigma, F: ((sigma['sigma1'] / F['F1t'])**2 - sigma['sigma1'] * sigma['sigma2'] / F['F1t']**2 + (sigma['sigma2'] / F['F2t'])**2 + (sigma['tau12'] / F['F6'])**2),
        "latex": r"\left( \frac{\sigma_1}{F_{1t}} \right)^2 - \frac{\sigma_1 \sigma_2}{F_{1t}^2} + \left( \frac{\sigma_2}{F_{2t}} \right)^2 + \left( \frac{\tau_{12}}{F_6} \right)^2 = 1"
    }
}
