import streamlit as st
import math
import inspect

st.image('./akeret.png')

# Use Streamlit's input widgets to capture parameters
d_l = st.number_input('Relativna debljina `d_l`:', value=0.10, format="%.2f")  # Relative thickness
alpha_deg = st.number_input('Napadni ugao [°] `alpha_deg`:', value=1.5, format="%.1f")  # Initial angle of attack in degrees
finesa_veca = st.number_input('Finesa veca za `finesa_veca`:', value=0.5, format="%.1f")  # lift to drag ratio larger by

def calculate_new_angle(d_l, alpha_deg, finesa_veca):
    # Compute angle of attack in radians
    alpha = alpha_deg * math.pi / 180

    # Compute B
    B = 4 * (d_l)**2

    # Compute initial F factors
    F_1 = (4 * alpha) / (4 * alpha**2 + B)
    F_2 = (1 + finesa_veca) * F_1

    # Initialization for iteration using Newton-Raphson method
    m_1 = [(1 + finesa_veca) * math.pi / 180]

    while True:
        fF2 = ((4 * m_1[-1]) / (4 * m_1[-1]**2 + B)) - F_2
        dfF2 = 4 * (B - 4 * m_1[-1]**2) / (4 * m_1[-1]**2 + B)**2
        new_m1 = m_1[-1] - fF2 / dfF2
        eps = abs(new_m1 - m_1[-1])
        m_1.append(new_m1)
        if eps < 1e-5:
            break

    # Calculate final angle of attack in degrees
    final_alpha_degrees = m_1[-1] * 180 / math.pi
    return final_alpha_degrees

# Execute the function and display the result
final_alpha_degrees = calculate_new_angle(d_l, alpha_deg, finesa_veca)

st.markdown('***')
st.write(f'Napadni ugao za {finesa_veca * 100}% vecu finesu:')
st.subheader(f'α = {final_alpha_degrees:.4f} [°]')

# Display the source code of the function
st.code(inspect.getsource(calculate_new_angle), language='python')
