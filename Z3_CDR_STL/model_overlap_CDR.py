from stl import mesh
import numpy as np
from collections import Counter


def deep_tuple(nested_obj):
    """
    Recursively convert nested lists/arrays to hashable tuples

    Args:
        nested_obj: Input list, tuple or numpy array
    Returns:
        tuple: Immutable nested tuple representation
    """
    if isinstance(nested_obj, np.ndarray):
        nested_obj = nested_obj.tolist()
    return tuple(deep_tuple(sub) if isinstance(sub, (list, tuple, np.ndarray)) else sub
                 for sub in nested_obj)


def find_unique_triangle_indices(triangles):
    """
    Find indices of first occurrences of unique triangles

    Args:
        triangles: List of triangle vertices to process
    Returns:
        list: Indices of first unique triangles
    """
    # Count occurrences of each triangle pattern
    pattern_counts = Counter(map(deep_tuple, triangles))
    seen_patterns = set()
    unique_indices = []

    for idx, triangle in enumerate(triangles):
        pattern = deep_tuple(triangle)
        if pattern not in seen_patterns:
            unique_indices.append(idx)
            seen_patterns.add(pattern)

    return unique_indices


def remove_overlapping_triangles(input_path, output_path):
    """
    Remove duplicate triangles from STL file to prevent model overlap attacks

    Args:
        input_path: Path to input STL file
        output_path: Path for cleaned output STL file
    """
    # Load mesh and find unique triangles
    in_mesh = mesh.Mesh.from_file(input_path)
    unique_indices = find_unique_triangle_indices(in_mesh.vectors)

    # Create new mesh with only unique triangles
    out_data = np.array([in_mesh.data[i] for i in unique_indices],
                        dtype=in_mesh.data.dtype)
    out_mesh = mesh.Mesh(out_data)
    out_mesh.save(output_path)