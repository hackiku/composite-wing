import pandas as pd
import streamlit as st
from materials import fibers, matrices

def get_material_data():
    fiber_df = pd.DataFrame(fibers).transpose()
    matrix_df = pd.DataFrame(matrices).transpose()
    st.write("Fiber Materials Data")
    st.dataframe(fiber_df)
    st.write("Matrix Materials Data")
    st.dataframe(matrix_df)

def display_material_properties(fiber, matrix):
    fiber_properties = pd.DataFrame.from_dict(fibers[fiber], orient='index', columns=[fiber]).transpose()
    matrix_properties = pd.DataFrame.from_dict(matrices[matrix], orient='index', columns=[matrix]).transpose()
    st.write("Selected Fiber Material Properties:")
    st.dataframe(fiber_properties)
    st.write("Selected Matrix Material Properties:")
    st.dataframe(matrix_properties)