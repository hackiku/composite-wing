# latex_utils.py
def render_latex(description, formula, values):
    """
    Render LaTeX for a given description, formula, and values.
    
    :param description: Description of the formula (e.g., "Young's Modulus `E1`")
    :param formula: LaTeX formula (e.g., r"E_1 = E_{f}V_{f} + E_{m}V_{m}")
    :param values: Dictionary of values to substitute in the formula (e.g., {"Ef": 70, "Vf": 0.6, "Em": 3, "Vm": 0.4})
    :return: Formatted LaTeX string
    """
    try:
        rendered_values = formula.format(**values)
        return f"{description}\n\n{rendered_values}"
    except KeyError as e:
        return f"Error in rendering LaTeX: missing key {e}"