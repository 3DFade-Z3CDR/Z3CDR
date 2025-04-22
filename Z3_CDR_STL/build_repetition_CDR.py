from stl import mesh
import numpy as np
from collections import Counter


def equal_triangles(tri1, tri2):
    """
    Check if two triangles are identical (in [[x,y,z],[x,y,z],[x,y,z]] format)

    Args:
        tri1: First triangle (list of 3 vertices)
        tri2: Second triangle (list of 3 vertices)
    Returns:
        bool: True if triangles are identical, False otherwise
    Raises:
        EOFError: If triangles have different dimensions
    """

    def equal_vertices(v1, v2):
        """
        Check if two vertices are identical (flat lists only)

        Args:
            v1: First vertex [x,y,z]
            v2: Second vertex [x,y,z]
        Returns:
            bool: True if vertices are identical
        Raises:
            EOFError: If vertices have different lengths
        """
        if len(v1) != len(v2):
            raise EOFError("Vertices must have same dimensions")
        return all(v1[i] == v2[i] for i in range(len(v1)))

    if len(tri1) != len(tri2):
        raise EOFError("Triangles must have same vertex count")

    return all(equal_vertices(tri1[i], tri2[i]) for i in range(len(tri1)))


def is_triangle_unique(triangles, triangle):
    """
    Check if a triangle exists in a collection of triangles

    Args:
        triangles: List of triangles to search
        triangle: Target triangle to find
    Returns:
        bool: True if triangle exists in collection, False otherwise
    """
    return any(equal_triangles(triangle, t) for t in triangles)


def deep_tuple(nested_obj):
    """
    Recursively convert nested lists/arrays to immutable tuples

    Args:
        nested_obj: Input list, tuple or numpy array
    Returns:
        tuple: Fully nested tuple version of input
    """
    if isinstance(nested_obj, np.ndarray):
        nested_obj = nested_obj.tolist()
    return tuple(deep_tuple(sub) if isinstance(sub, (list, tuple, np.ndarray)) else sub
                 for sub in nested_obj)


def find_unique_triangle_indices(triangles):
    """
    Find indices of first occurrences of unique triangles

    Args:
        triangles: List of triangles to process
    Returns:
        list: Indices of first unique triangles
    """
    count = Counter(map(deep_tuple, triangles))
    seen = set()
    return [i for i, tri in enumerate(triangles)
            if not (deep_tuple(tri) in seen or seen.add(deep_tuple(tri)))]


def build_repetition_defense(input_file, output_file):
    """
    Remove duplicate triangles from STL file (defense against build_repetition/model_overlap attacks)

    Args:
        input_file: Path to input STL file
        output_file: Path for output STL file
    """
    in_mesh = mesh.Mesh.from_file(input_file)
    unique_indices = find_unique_triangle_indices(in_mesh.vectors)

    # Create new mesh with only unique triangles
    out_data = np.array([in_mesh.data[i] for i in unique_indices])
    out_mesh = mesh.Mesh(out_data.copy())
    out_mesh.save(output_file)

def build_repetition_dection(filepath):
    """
    Detect build_repetition/model_overlap attacks by checking for duplicate triangles
    """
    in_mesh=mesh.Mesh.from_file(filepath)
    count=Counter(map(deep_tuple, in_mesh.vectors))
    # Check if any sublist has more than 1 occurrence
    for cnt in count.values():
        if cnt > 1:
            return True  # If there is a duplicate sublist, return True
    return False  # If there is no repeated sublist, return False

