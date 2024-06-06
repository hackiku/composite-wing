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
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E1f'] * Vf + m['Em'] * Vm,
            "latex": r"E_1 = E_{1f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_1 = {f['E1f']} \cdot {Vf} + {m['Em']} \cdot {Vm}"
        }
    },
    "E2_modulus": {
        "unit": "GPa",
        "ROM": {
            "formula": lambda f, m, Vf, Vm: f['E2f'] * Vf + m['Em'] * Vm,
            "latex": r"E_2 = E_{2f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_2 = {f['E2f']} \cdot {Vf} + {m['Em']} \cdot {Vm}"
        },
        "Voigt Model": {
            "formula": lambda f, m, Vf, Vm: f['E2f'] * Vf + m['Em'] * Vm,
            "latex": r"E_2 = E_{2f}V_f + E_mV_m",
            "math": lambda f, m, Vf, Vm: f"E_2 = {f['E2f']} \cdot {Vf} + {m['Em']} \cdot {Vm}"
        }
    }
}

def calculate_micromechanics_properties(fiber, matrix, Vf, Vm, show_math):
    properties = list(micromechanics_theories.keys())
    results = {"Property": properties}
    latex_results = {property_name: {} for property_name in properties}
    math_results = {property_name: {} for property_name in properties} if show_math else None

    for property_name in properties:
        for theory_name, theory_details in micromechanics_theories[property_name].items():
            if theory_name == "unit":
                continue
            
            formula = theory_details["formula"]
            latex_formula = theory_details["latex"]
            math_formula = theory_details.get("math", None)

            result = formula(fiber, matrix, Vf, Vm)
            
            if theory_name not in results:
                results[theory_name] = []
            results[theory_name].append(result)

            latex_results[property_name][theory_name] = latex_formula

            if show_math and math_formula:
                math_results[property_name][theory_name] = math_formula(fiber, matrix, Vf, Vm)

    return results, latex_results, math_results
