import os
from steputils import p21

def read_step_file(file_path):
    """Read a STEP file and return vertices and faces."""
    try:
        stepfile = p21.readfile(file_path)
    except Exception as e:
        print(f"Error reading STEP file: {e}")
        return None, None

    vertices = []
    faces = []
    for entity in stepfile.data:
        if p21.is_simple_entity_instance(entity):
            entity = entity.entity
            if entity.name == 'VERTEX_POINT':
                point = entity.params[0].params[0]
                vertices.append((point[0], point[1], point[2]))
            elif entity.name == 'FACE_OUTER_BOUND':
                # Extract face vertices
                indices = [int(ref[1:]) - 1 for ref in entity.params[0].params]
                for i in range(1, len(indices) - 1):
                    faces.append((indices[0], indices[i], indices[i + 1]))

    return vertices, faces

def main():
    # Path to your STEP file
    file_path = './models/WIP.step'  # Update this to the path of your STEP file

    if not os.path.exists(file_path):
        print(f"STEP file not found at {file_path}")
        return
    
    vertices, faces = read_step_file(file_path)
    
    if vertices is None or faces is None:
        return
    
    # Print the vertices and faces
    print("Vertices:")
    for vertex in vertices:
        print(vertex)
    
    print("\nFaces:")
    for face in faces:
        print(face)

if __name__ == "__main__":
    main()
