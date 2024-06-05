# wing_load_calculator.py

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def calculate_wing_load(mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes):
    g = 9.81
    total_force = mass * g * load_factor / 2
    total_nodes = nodes_between_ribs * num_ribs - (num_ribs - 2)
    y_positions = np.linspace(0, wing_length, total_nodes)
    dy_position = y_positions[1] - y_positions[0]
    p = round(wing_length / (dy_position * num_nodes))
    st.write(f'Forces are applied every {p-1} nodes.')
    dy = p * dy_position
    y_interpolated = np.arange(0, num_nodes * dy, dy)
    if y_interpolated[-1] > wing_length:
        y_interpolated = y_interpolated[:-1]

    a = 3 / 2 * total_force / wing_length
    y = np.linspace(0, wing_length, 1001)
    assumed_force_distribution = np.sqrt(a ** 2 / wing_length * (wing_length - y))

    interpolated_forces = np.interp(y_interpolated, y, assumed_force_distribution)

    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots()
        ax1.plot(y, assumed_force_distribution, label='Assumed Distribution', linewidth=2)
        ax1.plot(y_interpolated, interpolated_forces, '--', label='Interpolated', linewidth=2)
        ax1.legend()
        ax1.set_title('Load Distribution Along the Wing')
        ax1.set_xlabel('y [mm]')
        ax1.set_ylabel('F [N/mm]')
        st.pyplot(fig1)

    yk = np.zeros(len(y_interpolated))
    Fk = np.zeros(len(y_interpolated))
    yk[1:] = np.cumsum(np.full(len(y_interpolated)-1, dy))
    Fk[1:] = (interpolated_forces[1:] + interpolated_forces[:-1]) / 2 * dy
    total_interpolated_force = np.sum(Fk)

    with col2:
        fig2, ax2 = plt.subplots()
        ax2.stem(yk[1:], Fk[1:], basefmt=" ")
        ax2.set_title('Distribution of Concentrated Forces on the Front Spar')
        ax2.set_xlabel('y [mm]')
        ax2.set_ylabel('F [N]')
        st.pyplot(fig2)

    st.write(f'Relative error for normal force: {abs(100 - total_force / total_interpolated_force * 100):.2f} %.')

    st.latex(fr"""
    \sum F_l = \frac{{R_z}}{{2}} = \frac{{m_{{max}} \cdot g \cdot n}}{{2}} = \frac{{{mass} \cdot {g} \cdot {load_factor}}}{{2}} = {total_force / 1000:.2f} \, \text{{kN}}
    """)


