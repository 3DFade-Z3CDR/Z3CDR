import xml.etree.ElementTree as ET
import file_handle as fd
import re


def strip_namespace(tag):
    return re.sub(r'\{.*?\}', '', tag)


def Steganographic_defense_model(input_file, output_file):
    """
    Apply steganographic defense to 3D model file

    :param input_file: Input file path
    :param output_file: Output file path after defense
    :return: Path to the defended file
    """
    # Parse original XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    objs = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}object')

    # Process triangle tags - if they're not in (v1,v2,v3) format, convert them
    for obj in objs:
        mesh = obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}mesh')
        triangles = mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangle')

        for ind, triangle in enumerate(triangles):
            key = triangle.attrib.keys()
            if list(key) != ["v1", "v2", "v3"]:
                for t in ["v1", "v2", "v3"]:
                    triangles[ind].attrib[t] = triangles[ind].attrib.pop(t)

    # Modify the original root structure
    for child in range(len(root)):
        if root[child].tag == 'resources':
            for elem in range(len(root[child])):
                if root[child][elem].tag == 'object':
                    for mesh in range(len(root[child][elem])):
                        if root[child][elem][mesh].tag == 'mesh':
                            for part in range(len(root[child][elem][mesh])):
                                if root[child][elem][mesh][part].tag == 'triangles':
                                    root[child][elem][mesh][part] = triangles

    # Convert processed tree to XML file
    fd.indent(root)
    new_tree = ET.ElementTree(root)
    new_tree.write(output_file, encoding="utf-8", xml_declaration=True)

    return output_file


def Steganographic_detection_model(filepath):
    """
    Detect steganographic attacks in 3D model file

    :param filepath: Path to the file to be checked
    :return: True if steganographic attack is detected, False otherwise
    """
    # Parse original XML file
    tree = ET.parse(filepath)
    root = tree.getroot()

    objs = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}object')

    # Check triangle tags - if not in (v1,v2,v3) format, potential steganography
    for obj in objs:
        mesh = obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}mesh')
        if obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}components') is not None:
            continue  # Skip objects without triangles
        triangles = mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangle')
        for ind, triangle in enumerate(triangles):
            key = triangle.attrib.keys()
            if list(key) != ["v1", "v2", "v3"]:
                return True
    return False