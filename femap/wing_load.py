# femap/wing_load.py

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def calc_wing_load(mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes):
    g = 9.80665
    total_force = mass * g * load_factor / 2
    total_nodes = int(nodes_between_ribs * num_ribs - (num_ribs - 2))  # Ensure total_nodes is an integer
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

def wing_load_ui():
    st.header("Wing Load Calculation")
    st.write("""
        This section calculates the load distribution along the wing and the distribution of concentrated forces on the front spar.
        Enter the necessary parameters and visualize the results below.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        mass = st.number_input('Mass of aircraft (kg)', value=1000.0, step=100.0)
        load_factor = st.number_input('Load Factor', value=3.0)
    with col2:
        nodes_between_ribs = st.number_input('Nodes between Ribs', value=15)
        num_ribs = st.number_input('Number of Ribs', value=12)
    with col3:
        wing_length = st.number_input('Wing Length (mm)', value=10000.0)
        num_nodes = st.number_input('Number of Nodes for Force Calculation', value=20)
    
    if st.button('Calculate Load'):
        calculate_wing_load(mass, load_factor, nodes_between_ribs, num_ribs, wing_length, num_nodes)

