# material_math/hooke_law.py

import streamlit as st

def display_hooke_law_matrices():
    st.latex(r"""
    \begin{bmatrix}
    \frac{1}{E_1} & -\frac{\nu_{21}}{E_2} & -\frac{\nu_{31}}{E_3} & 0 & 0 & 0 \\
    -\frac{\nu_{12}}{E_1} & \frac{1}{E_2} & -\frac{\nu_{32}}{E_3} & 0 & 0 & 0 \\
    -\frac{\nu_{13}}{E_1} & -\frac{\nu_{23}}{E_2} & \frac{1}{E_3} & 0 & 0 & 0 \\
    0 & 0 & 0 & \frac{1}{G_{23}} & 0 & 0 \\
    0 & 0 & 0 & 0 & \frac{1}{G_{13}} & 0 \\
    0 & 0 & 0 & 0 & 0 & \frac{1}{G_{12}}
    \end{bmatrix}
    """)

    st.latex(r"""
    \begin{aligned}
    \nu_{12} &= \frac{\nu_{12}E_1}{E_2} \\
    \nu_{21} &= \frac{\nu_{21}E_2}{E_1} \\
    \nu_{13} &= \frac{\nu_{13}E_1}{E_3} \\
    \nu_{31} &= \frac{\nu_{31}E_3}{E_1} \\
    \nu_{23} &= \frac{\nu_{23}E_2}{E_3} \\
    \nu_{32} &= \frac{\nu_{32}E_3}{E_2}
    \end{aligned}
    """)

    st.latex(r"""
    \begin{aligned}
    \sigma_3 &= \tau_4 = \tau_5 = 0 \\
    \left[ \sigma \right] &= \left[ Q_{ij} \right] \left[ \epsilon \right] \\
    \left[ \epsilon \right] &= \left[ S_{ij} \right] \left[ \sigma \right] \\
    \end{aligned}
    """)

    st.latex(r"""
    \left[ S_{ij} \right] = 
    \begin{bmatrix}
    \frac{1}{E_1} & -\frac{\nu_{21}}{E_2} & 0 \\
    -\frac{\nu_{12}}{E_1} & \frac{1}{E_2} & 0 \\
    0 & 0 & \frac{1}{G_{12}}
    \end{bmatrix}
    """)

    st.latex(r"""
    \left[ Q_{ij} \right] =
    \begin{bmatrix}
    \frac{E_1}{1 - \nu_{12}\nu_{21}} & \frac{\nu_{12}E_2}{1 - \nu_{12}\nu_{21}} & 0 \\
    \frac{\nu_{21}E_1}{1 - \nu_{12}\nu_{21}} & \frac{E_2}{1 - \nu_{12}\nu_{21}} & 0 \\
    0 & 0 & G_{12}
    \end{bmatrix}
    """)

    st.latex(r"""
    \begin{aligned}
    N_x^k &= \int_{-t/2}^{t/2} \sigma_x \, dz \\
    N_y^k &= \int_{-t/2}^{t/2} \sigma_y \, dz \\
    N_s^k &= \int_{-t/2}^{t/2} \tau_{xy} \, dz \\
    M_x^k &= \int_{-t/2}^{t/2} \sigma_x z \, dz \\
    M_y^k &= \int_{-t/2}^{t/2} \sigma_y z \, dz \\
    M_s^k &= \int_{-t/2}^{t/2} \tau_{xy} z \, dz
    \end{aligned}
    """)

# In the homepage or wherever you want to display these matrices:
# display_hooke_law_matrices()
