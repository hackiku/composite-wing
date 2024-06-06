# composite_math/failure_theories.py
failure_theories = {
    "Tsai-Wu": {
        "unit": "-",  # Failure theories typically dimensionless
        "formula": lambda sigma, F: (
            F['F1'] * sigma['sigma1'] + 
            F['F2'] * sigma['sigma2'] + 
            F['F11'] * sigma['sigma1']**2 + 
            F['F22'] * sigma['sigma2']**2 + 
            2 * F['F12'] * sigma['sigma1'] * sigma['sigma2'] + 
            F['F66'] * sigma['tau12']**2
        ),
        "latex": r"F_1 \sigma_1 + F_2 \sigma_2 + F_{11} \sigma_1^2 + F_{22} \sigma_2^2 + 2 F_{12} \sigma_1 \sigma_2 + F_{66} \tau_{12}^2 = 1"
    },
    "Tsai-Hill": {
        "unit": "-",  # Failure theories typically dimensionless
        "formula": lambda sigma, F: (
            (sigma['sigma1'] / F['F1ft'])**2 - 
            sigma['sigma1'] * sigma['sigma2'] / F['F1ft']**2 + 
            (sigma['sigma2'] / F['F2t'])**2 + 
            (sigma['tau12'] / F['FmS'])**2
        ),
        "latex": r"\left( \frac{\sigma_1}{F_{1ft}} \right)^2 - \frac{\sigma_1 \sigma_2}{F_{1ft}^2} + \left( \frac{\sigma_2}{F_{2t}} \right)^2 + \left( \frac{\tau_{12}}{F_{6}} \right)^2 = 1"
    }
}

def calculate_failure_theories(sigma, F):
    results = {}
    latex_results = {}

    for theory_name, theory_details in failure_theories.items():
        formula = theory_details["formula"]
        result = formula(sigma, F)
        results[theory_name] = result
        latex_results[theory_name] = theory_details["latex"]

    return results, latex_results
