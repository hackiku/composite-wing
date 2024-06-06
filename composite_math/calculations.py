# composite_math/calculations.py
from composite_math.micromechanics import calculate_micromechanics_properties
from composite_math.failure_theories import calculate_failure_theories

def calculate_properties(fiber_material, matrix_material, Vf, Vm, Vvoid, sigma, F, show_math=False):
    micromechanics_results, micromechanics_latex, micromechanics_math = calculate_micromechanics_properties(fiber_material, matrix_material, Vf, Vm, show_math)
    failure_results, failure_latex = calculate_failure_theories(sigma, F)

    # Combine the results
    results = {
        "Micromechanics": micromechanics_results,
        "Failure Theories": failure_results
    }
    latex_results = {
        "Micromechanics": micromechanics_latex,
        "Failure Theories": failure_latex
    }
    math_results = {
        "Micromechanics": micromechanics_math,
        "Failure Theories": failure_results 
    }

    return results, latex_results, math_results
