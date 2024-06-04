import os
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Extend.DataExchange import read_step_file
from OCC.Display.SimpleGui import init_display
import plotly.graph_objects as go
import numpy as np

def load_step_file(step_file_path):
    """Load and return the STEP file contents."""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(step_file_path)
    if status == STEPControl_Reader.IFSelect_RetDone:
        step_reader.TransferRoots()
        shape = step_reader.Shape()
        return shape
    else:
        raise ValueError(f"Error: Cannot read the STEP file {step_file_path}")

def extract_vertices_faces(shape):
    """Extract vertices and faces from the shape."""
    from OCC.Extend.TopologyUtils import TopologyExplorer
    vertices = []
    faces = []
    te = TopologyExplorer(shape)
    for face in te.faces():
        face_vertices = []
        for vertex in TopologyExplorer(face).vertices():
            pnt = vertex.Point()
            face_vertices.append((pnt.X(), pnt.Y(), pnt.Z()))
        if len(face_vertices) >= 3:
            for i in range(1, len(face_vertices) - 1):
                vertices.extend([face_vertices[0], face_vertices[i], face_vertices[i + 1]])
                faces.append((len(vertices) - 3, len(vertices) - 2, len(vertices) - 1))
    return np.array(vertices), np.array(faces)

def display_step_file_with_plotly(shape):
    """Visualize the STEP file contents with Plotly."""
    vertices, faces = extract_vertices_faces(shape)
    x, y, z = vertices.T
    i, j, k = faces.T

    fig = go.Figure(data=[go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        color='orange',
        opacity=0.50
    )])

    fig.update_layout(scene=dict(
        xaxis=dict(visible=True, backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="gray", showbackground=True, zerolinecolor="red", title="X"),
        yaxis=dict(visible=True, backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="gray", showbackground=True, zerolinecolor="green", title="Y"),
        zaxis=dict(visible=True, backgroundcolor="rgba(0, 0, 0, 0)", gridcolor="gray", showbackground=True, zerolinecolor="blue", title="Z")
    ), width=800, height=600)

    fig.show()

def get_step_files(directory='./models/'):
    """Get a list of STEP files from the specified directory."""
    return [f for f in os.listdir(directory) if f.endswith('.step') or f.endswith('.stp')]

def main():
    """Main function to load and display STEP files."""
    models_path = './models/'
    step_files = get_step_files(models_path)
    if not step_files:
        print(f"No STEP files found in the directory: {models_path}")
        return
    
    # For simplicity, we'll just load the first STEP file found
    step_file_path = os.path.join(models_path, step_files[0])
    try:
        shape = load_step_file(step_file_path)
        display_step_file_with_plotly(shape)
    except Exception as e:
        print(f"Error loading and displaying STEP file: {e}")

if __name__ == "__main__":
    main()
