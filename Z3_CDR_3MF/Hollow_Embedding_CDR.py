import numpy as np
import file_handle as fd
import xml.etree.ElementTree as ET
import re


# Calculate triangle area

# Process namespace before tags
def strip_namespace(tag):
    return re.sub(r'\{.*?\}', '', tag)


def strlist_calculate(strl1, strl2):
    # Check if two string lists have equal values
    list1 = list(map(float, strl1.strip().split()))
    list2 = list(map(float, strl2.strip().split()))

    if len(list1) != len(list2):
        raise Exception('list1 and list2 must have the same length')
    result = True
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            result = result and True
        else:
            result = result and False
            break
    return result


def contains_points_with_surface(mesh1, points, tolerance=1e-8):
    # Calculate shortest distance from points to mesh
    distances = mesh1.nearest.signed_distance(points)

    for distance in distances:
        if np.abs(distance) < tolerance:
            pass
        else:
            return False
    return True


def contains_meshes(mesh1, mesh2):
    # Check if mesh1 contains mesh2

    # First check if all vertices of mesh2 are inside mesh1
    ver_res = []
    for vertex in mesh2.vertices:
        if not mesh1.contains([vertex]):
            ver_res.append(vertex)
    if len(ver_res) == 0:
        return True
    else:
        # If vertices are on the surface of mesh1
        if contains_points_with_surface(mesh1, ver_res):
            return True
        else:
            return False


def UI_disarm(filepath):
    """
    Select objects wrapped by other objects and return their ID list

    :param filepath: Path to the file to be processed
    :return: List of object IDs that need to be removed
    """
    # Find all object elements and convert them to dictionary format
    objs = fd.get_file_objects(filepath)
    objects = {obj.attrib.get('id', 'empty'): obj for obj in objs}

    # Find all item elements
    items = fd.get_file_items(filepath)

    # Exception handling: objects or items is empty
    if len(objects) == 0:
        raise FileNotFoundError
    if len(items) == 0:
        raise FileNotFoundError

    # Find build object information including ID and corresponding transform
    builds = []
    for index, item in enumerate(items):
        builds.append([item.get("objectid", "empty"),
                       item.get("transform", "1 0 0 0 1 0 0 0 1 0 0 0"),
                       index])
    build_ids = [l[0] for l in builds]
    build_trans = [list(map(lambda x: round(float(x), 4), l[1].strip().split())) for l in builds]

    if "empty" in build_ids:
        # No ID was built, raise exception
        raise KeyError

    meshes = {}  # All meshes in build list
    disarms = []  # List of object IDs to be removed

    # Get all meshes processed by build_dos (transform-applied meshes)
    for ind in range(len(builds)):
        meshes[ind] = fd.get_transform_mesh(objects[build_ids[ind]], build_trans[ind])

    for cur in meshes:
        for other in meshes:
            if cur == other:
                pass
            else:
                if contains_meshes(meshes[other], meshes[cur]):
                    disarms.append(cur)
                else:
                    pass

    return disarms  # disarms contains indices in builds list


def Hollow_Embedding_defense(inputfile, outputfile, mosaic_ids):
    """
    Apply Hollow_Embedding defense to inputfile

    :param inputfile: Input file path
    :param outputfile: Output file path
    :param mosaic_ids: IDs of objects to be processed
    """
    if mosaic_ids is None:
        raise KeyError("Hollow_Embedding_ids is None")

    # Parse original XML file
    tree = ET.parse(inputfile)
    root = tree.getroot()

    to_remove = []
    for child in root:
        if strip_namespace(child.tag) == 'build':
            for index, item in enumerate(child):
                if index in mosaic_ids:
                    to_remove.append(item)
            for delte in to_remove:
                child.remove(delte)
        else:
            pass

    # Convert processed tree to XML file
    fd.indent(root)
    new_tree = ET.ElementTree(root)
    new_tree.write(outputfile, encoding="utf-8", xml_declaration=True)