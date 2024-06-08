# material_math/theories.py

import numpy as np

micromechanics_properties = {
    "E1_modulus": {
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m"
        },
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m"
        },
        "Inverse Rule of Mixtures": {
            "formula": lambda f, m, Vf, Vm: 1 / (Vf / f['E1f'] + Vm / m['Em']),
            "latex": r"\frac{1}{E_1} = \frac{V_f}{E_{1f}} + \frac{V_m}{E_m}"
        }
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
        }
    },
    "shear_modulus": {
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
            "formula": lambda f, m, Vf, Vm: (f['G12f'] * m['Gm']) / (Vf * m['Gm'] + Vm * f['G12f']),
            "latex": r"G_{12} = \frac{G_{12f} \cdot G_m}{V_f \cdot G_m + V_m \cdot G_{12f}}"
        }
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

# Strength theories
strength_properties = {
    "tensile_strength": {
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
        "unit": "MPa",
        "Timoshenko-Gere": {
            "formula": lambda f, m, Vf, Vm: 2 * Vf * np.sqrt((Vf * f['E1f'] * m['Em']) / (3 * (1 - Vf))),
            "latex": r"F_{1C} = 2V_f \sqrt{\frac{V_f E_{1f} E_m}{3(1 - V_f)}}"
        },
        "Agarwal-Broutman": {
            "formula": lambda f, m, Vf, Vm: ((f['E1f'] * Vf + m['Em'] * Vm) * (1 - Vf**(1/3)) * m['epsilon_mT']) / (f['v12f'] * Vf + m['vm'] * Vm),
            "latex": r"F_{1C} = \frac{(E_{1f} V_f + E_m V_m) (1 - V_f^{1/3}) \varepsilon_{mu}}{\nu_{12f} V_f + \nu_m V_m}"
        },
        "Modified ROM": {
            "formula": lambda f, m, Vf, Vm, Vvoid: (f['F1ft'] * Vf + m['FmC'] * Vm) * (1 - Vvoid),
            "latex": r"F_{1C} = (F_{1ft}V_f + F_mCV_m)(1 - V_{void})"
        }
    },
    "transverse_tensile_strength": {
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
