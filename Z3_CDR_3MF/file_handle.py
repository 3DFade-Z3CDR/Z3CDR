import zipfile
import os
import numpy as np
import trimesh
import xml.etree.ElementTree as ET
from pathlib import Path

def is_3mf_file(file_path):
    """
    Check if the file has a .3mf extension.

    :param file_path: File path (str or Path object)
    :return: True if it's a .3mf file, False otherwise
    """
    file = Path(file_path)  # Convert to Path object
    if not file.is_file():  # Verify path points to a file
        raise ValueError(f"{file_path} is not a valid file path")

    return file.suffix.lower() == ".3mf"

def unzip_3mf(file_path, output_dir):
    """
    Extract a 3MF file without parsing its internal format.

    :param file_path: Path to the 3MF file
    :param output_dir: Output directory for extracted files
    :raises FileExistsError: If input is not a valid 3MF file
    """
    if not is_3mf_file(file_path):
        raise FileExistsError("The file is not a valid 3MF file")

    if not zipfile.is_zipfile(file_path):
        print(f"{file_path} is not a valid 3MF file")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
    except Exception as e:
        print(f"Extraction error: {e}")

def merge_3mf(folder_path, output_path):
    """
    Compress a folder into a 3MF file.

    :param folder_path: Directory to compress
    :param output_path: Output path for the 3MF file
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def get_file_objects(filepath):
    """
    Extract objects section from an XML file.

    :param filepath: Path to the XML file
    :return: List of object elements
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    objects = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}object')
    return objects

def apply_transform(point, transform):
    """
    Apply a 3D transformation matrix to a point.

    Args:
        transform (list): 12-element transformation definition [a, b, c, d, e, f, g, h, i, tx, ty, tz]
        point (list/tuple): 3D point coordinates [x, y, z]

    Returns:
        list: Transformed point coordinates [x', y', z']

    Raises:
        ValueError: If input dimensions are invalid
    """
    if len(transform) != 12:
        raise ValueError("Transform must contain 12 elements")
    if len(point) != 3:
        raise ValueError("Point must contain 3 elements")

    # Construct 4x4 transformation matrix
    matrix = np.array([
        [transform[0], transform[1], transform[2], transform[9]],
        [transform[3], transform[4], transform[5], transform[10]],
        [transform[6], transform[7], transform[8], transform[11]],
        [0, 0, 0, 1]
    ])

    # Convert point to homogeneous coordinates [x, y, z, 1]
    point_homogeneous = np.array([point[0], point[1], point[2], 1])

    # Apply transformation
    transformed_point = np.dot(matrix, point_homogeneous)

    return transformed_point[:3].tolist()

def get_transform_mesh(obj, transform, status=1):
    """
    Extract and transform mesh data from an object element.

    Args:
        obj: XML object element containing mesh data
        transform: Transformation matrix to apply
        status: Optional status flag (default: 1)

    Returns:
        trimesh.Trimesh: Transformed mesh object
    """
    mesh = obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}mesh')

    if mesh is not None:
        # Process vertices
        vertices = []
        for vertex in mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}vertex'):
            x = float(vertex.attrib.get('x'))
            y = float(vertex.attrib.get('y'))
            z = float(vertex.attrib.get('z'))
            transformed_vert = apply_transform([x, y, z], transform)
            vertices.append(transformed_vert)
        vertices = np.array(vertices)

        # Process triangles
        triangles = []
        for triangle in mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangle'):
            triangles.append([
                triangle.attrib.get('v1'),
                triangle.attrib.get('v2'),
                triangle.attrib.get('v3')
            ])
        triangles = np.array(triangles)

        return trimesh.Trimesh(vertices=vertices, faces=triangles)

def get_file_items(filepath):
    """
    Extract items section from an XML file.

    :param filepath: Path to the XML file
    :return: List of item elements
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    items = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}item')
    return items

def indent(elem, level=0):
    """
    Recursively add line breaks and indentation to XML elements.

    :param elem: ET.Element to process
    :param level: Current indentation level
    """
    i = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i