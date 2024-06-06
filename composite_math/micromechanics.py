# composite_math/micromechanics.py
import numpy as np

micromechanics_theories = {
    "E1_modulus": {
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_1 = {f['E1f']} \cdot {Vf:.3f} + {m['Em']} \cdot {Vm:.3f}"
        },
        # Additional models...
    },
    # Additional properties...
}

def calculate_micromechanics_properties(fiber, matrix, Vf, Vm, show_math):
    results = {"Property": [], "ROM": [], "Voigt Model": [], "Inverse Rule of Mixtures": [], "Halpin-Tsai": []}
    latex_results = {"E1_modulus": {}, "E2_modulus": {}, "shear_modulus": {}, "poisson_ratio": {}}
    math_results = {"E1_modulus": {}, "E2_modulus": {}, "shear_modulus": {}, "poisson_ratio": {}}

    for property_name, theory_data in micromechanics_theories.items():
        results["Property"].append(property_name)
        for theory, details in theory_data.items():
            if theory == "unit":
                continue
            formula = details["formula"]
            result = formula(fiber, matrix, Vf, Vm)
            results[theory].append(result)
            latex_results[property_name][theory] = details["latex"]
            math_results[property_name][theory] = f"{details['latex']} = {result:.3f} [{details['unit']}]"

    return results, latex_results, math_results
