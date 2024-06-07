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
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"_{{voigt}} \ E_1 = {f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}"
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
            "latex": r"E_2 = E_{2f}V_f + E_mV_m",
        },
        # Add other theories here
    },
    # Add more micromechanics theories...
}

# Define strength theories
strength_theories = {
    "tensile_strength": {
        "unit": "MPa",
        "Chamis": {
            "formula": lambda f, m, Vf, Vm: f['F1ft'] * Vf + m['FmT'] * Vm,
            "latex": r"F_{1T} = F_{1ft}V_f + F_mTV_m"
        },
        # Add other theories here
    },
    "compressive_strength": {
        "unit": "MPa",
        "Timoshenko-Gere": {
            "formula": lambda f, m, Vf, Vm: ((1 - Vf**0.5) * f['F1ft'] + Vf**0.5 * m['FmC']),
            "latex": r"F_{1C} = (1 - V_f^{1/2}) F_{1ft} + V_f^{1/2} F_{mC}"
        },
        # Add other theories here
    },
    # Add more strength theories...
}

# Define failure theories
failure_theories = {
    "Tsai-Wu": {
        "formula": lambda sigma, F: (F['F1'] * sigma['sigma1'] + F['F2'] * sigma['sigma2'] + 
                                      F['F11'] * sigma['sigma1']**2 + F['F22'] * sigma['sigma2']**2 + 
                                      2 * F['F12'] * sigma['sigma1'] * sigma['sigma2'] + 
                                      F['F66'] * sigma['tau12']**2),
        "latex": r"F_1 \sigma_1 + F_2 \sigma_2 + F_{11} \sigma_1^2 + F_{22} \sigma_2^2 + 2 F_{12} \sigma_1 \sigma_2 + F_{66} \tau_{12}^2 = 1",
        "math" : f"math"
    },
    "Tsai-Hill": {
        "formula": lambda sigma, F: ((sigma['sigma1'] / F['F1t'])**2 - sigma['sigma1'] * sigma['sigma2'] / F['F1t']**2 + (sigma['sigma2'] / F['F2t'])**2 + (sigma['tau12'] / F['F6'])**2),
        "latex": r"\left( \frac{\sigma_1}{F_{1t}} \right)^2 - \frac{\sigma_1 \sigma_2}{F_{1t}^2} + \left( \frac{\sigma_2}{F_{2t}} \right)^2 + \left( \frac{\tau_{12}}{F_6} \right)^2 = 1",
        "math" : f"math"
    },
    # Add more failure theories...
}
