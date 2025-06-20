import numpy as np
import file_handle as fd
import xml.etree.ElementTree as ET
import re


def strip_namespace(tag):
    return re.sub(r'\{.*?\}', '', tag)


def strlist_calculate(strl1, strl2):
    # Check if two string lists represent the same set of float values
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
    # Compute the shortest distance from points to the mesh surface
    distances = mesh1.nearest.signed_distance(points)

    for distance in distances:
        if np.abs(distance) < tolerance:
            pass
        else:
            return False
    return True


def contains_meshes(mesh1, mesh2):
    # Determine whether mesh1 contains mesh2

    # First, check if all vertices of mesh2 are inside mesh1. If so, mesh1 contains mesh2
    ver_res = []
    for vertex in mesh2.vertices:
        if not mesh1.contains([vertex]):
            ver_res.append(vertex)
    if len(ver_res) == 0:
        return True
    else:
        # If some vertices are not strictly inside, check whether they lie on the surface of mesh1
        if contains_points_with_surface(mesh1, ver_res):
            return True
        else:
            return False


def matrix_mosaic_judge(trimeshes):
    """
    Determine embedding using a matrix-based method:
    - Perform matrix-like evaluation on the trimesh_objects using contains_meshes
    - Diagonal entries are set to False (an object cannot contain itself)
    - Each column indicates whether the object is contained by any other
    - A logical OR is applied across each column to determine if an object is embedded in another
    :param trimeshes: List of trimesh objects
    :return: List of booleans indicating whether each object is contained by others (True if contained)
    """
    judge_list = []  # Initialize result list
    trimesh_arr = np.array(trimeshes)  # Convert list to NumPy array
    arr_func = np.frompyfunc(contains_meshes, 2, 1)  # Vectorize contains_meshes for matrix application
    result = arr_func(trimesh_arr[:, None], trimesh_arr[None, :])  # Perform pairwise containment checks
    np.fill_diagonal(result, False)  # Set diagonal to False (self-containment not considered)

    for i in range(result.shape[0]):  # For each column, check if object is contained by any other
        judge_list.append(np.any(result[:, i], axis=0))

    return judge_list  # Return the list of containment results


def UI_disarm(filepath):
    """
    Select objects that are wrapped (embedded) by other objects and return their ID list
    :param filepath: Path to the 3D model file
    :return: A list of object IDs that need to be disarmed (i.e., removed or ignored)
    """
    # Locate all object elements and convert them into a dictionary {id: element}
    objs = fd.get_file_objects(filepath)
    objects = {obj.attrib.get('id', 'empty'): obj for obj in objs}

    # Locate all item elements
    items = fd.get_file_items(filepath)

    # Exception handling: objects or items are empty
    if len(objects) == 0:
        raise FileNotFoundError
    if len(items) == 0:
        raise FileNotFoundError

    # Extract object build info: id and associated transform matrix
    builds = []
    for index, item in enumerate(items):
        builds.append([
            item.get("objectid", "empty"),
            item.get("transform", "1 0 0 0 1 0 0 0 1 0 0 0"),
            index
        ])
    build_ids = [l[0] for l in builds]
    build_trans = [list(map(lambda x: round(float(x), 4), l[1].strip().split())) for l in builds]

    if "empty" in build_ids:
        # No valid object ID found in build list
        raise KeyError

    meshes = {}  # Dictionary to hold mesh objects transformed according to build transforms
    disarms = []  # List of object indices to be disarmed (i.e., objects embedded in others)

    trimeshes = []
    for ind in range(len(builds)):
        meshes[ind] = fd.get_transform_mesh(objects[build_ids[ind]], build_trans[ind])
    for values in meshes.values():
        trimeshes.append(values)

    disarms = matrix_mosaic_judge(trimeshes)

    return [ind for ind, res in enumerate(disarms) if res == True]  # Return indices of embedded objects


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