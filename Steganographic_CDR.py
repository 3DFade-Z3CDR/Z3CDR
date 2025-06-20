import xml.etree.ElementTree as ET
import copy

def equal_point(point1, point2):
    """
    Determine whether two points (in 3D coordinate space) are the same.
    Returns True if they are the same, otherwise returns False.
    :param point1: The first point, format [x1, y1, z1]
    :param point2: The second point, format [x2, y2, z2]
    :return: Comparison result. If the coordinates are exactly the same (including order), return True; otherwise, False.
    """
    # If the coordinate lengths differ, return False
    if len(point1) != len(point2):
        return False
    else:
        length = len(point1)
        for ind in range(length):  # Traverse both point arrays and compare element-wise
            if point1[ind] != point2[ind]:
                return False
        return True  # Return True if all coordinates match

def seq_point(point1, point2):
    """
    Select the more 'standardized' point from point1 and point2.
    The selection rules are as follows:
    1. Compare the sum of x + y + z. The one with the larger sum is more standardized.
        2. If equal, compare the x coordinate. The smaller one is more standardized.
            3. If equal, compare the y coordinate. The smaller one is more standardized.
                4. If equal, compare the z coordinate. The smaller one is more standardized.
    These rules are sequential: only proceed to the next if the current condition doesn't determine the result.
    Note: In theory, the same coordinates for both points should not happen. Such overlap is considered invalid (not discussed here).
    :param point1: First point [x1, y1, z1]
    :param point2: Second point [x2, y2, z2]
    :return: The point that best matches the rule
    """

    # Check if the coordinate dimensions match
    if len(point1) != len(point2):
        raise EOFError

    # Compute sum of coordinates and return the one with the greater sum
    sum1, sum2 = sum(point1), sum(point2)
    if sum1 > sum2:
        return point1
    elif sum2 > sum1:
        return point2
    else:
        # If sums are equal, compare x, y, z coordinates in order
        if point1[0] < point2[0]:
            return point1
        elif point1[0] > point2[0]:
            return point2
        else:
            if point1[1] < point2[1]:
                return point1
            elif point1[1] > point2[1]:
                return point2
            else:
                if point1[2] < point2[2]:
                    return point1
                elif point1[2] > point2[2]:
                    return point2
                else:
                    raise EOFError("The input points have identical coordinates")

def Decode(modelpath):
    """
    Decode the model file and extract triangle point sets from object elements.
    According to the rule in seq_point, determine whether triangle[0] is the most standardized point.
    If triangle[0] is the most standardized, encode as 1; otherwise, encode as 0.
    Return the final binary array as the decoding result of the model file.
    """
    # Load model file information
    tree = ET.parse(modelpath)
    root = tree.getroot()

    # Define the result list
    result = []

    # Define the namespace
    namespaces = {
        '': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    }

    # Extract object elements
    objs = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}object')

    # Iterate over objects for encoding
    for obj in objs:
        # Get mesh object
        mesh = obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}mesh')
        if mesh is not None:
            # Get vertex list in 3D coordinate format (order matters)
            Vertices = mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}vertex')
            vertices = []
            for vertex in Vertices:
                x = float(vertex.attrib.get('x'))
                y = float(vertex.attrib.get('y'))
                z = float(vertex.attrib.get('z'))
                vertice = [x, y, z]
                vertices.append(vertice)

            # Get triangle elements as index sequences, e.g., [0,1,2], [3,1,2]
            Triangles = mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangle')

            for triangle in Triangles:  # Iterate over triangles
                # Convert triangle to 3D coordinate format, shape 3x3
                triangle_points = [vertices[int(triangle.attrib.get(index))] for index in ["v1", "v2", "v3"]]
                # Determine whether triangle[0] is the most standardized and encode accordingly
                res = equal_point(triangle_points[0],
                                  seq_point(triangle_points[0], seq_point(triangle_points[1], triangle_points[2])))
                result.append(int(res))
    return result

def Steg_basic_CDR(modelpath, defense_model):
    """
    Apply countermeasure for Steg attack: remove and reconstruct content.
    This modifies all triangle encodings in the model file to 1 to destroy steganographic information.
    The encoding rule is: triangle[0] is the most standardized point => encode as 1.
    See the `seq_point` function for the definition of "most standardized".
    """

    # Load model file information
    tree = ET.parse(modelpath)
    root = tree.getroot()

    # Define the namespace
    namespaces = {
        '': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    }

    # Extract object elements
    objs = root.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}object')

    for obj in objs:  # Iterate over object elements
        mesh = obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}mesh')  # Get mesh element
        if mesh is None:
            continue
        else:
            # Get vertex list in 3D coordinate format (order matters)
            Vertices = mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}vertex')
            vertices = []
            for vertex in Vertices:
                x = float(vertex.attrib.get('x'))
                y = float(vertex.attrib.get('y'))
                z = float(vertex.attrib.get('z'))
                vertice = [x, y, z]
                vertices.append(vertice)

            # Get triangle elements as index sequences, e.g., [0,1,2], [3,1,2]
            Triangles = mesh.findall('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}triangle')
            for ind, triangle in enumerate(Triangles):
                triangle_t = copy.deepcopy(triangle)  # Must use deepcopy to avoid modifying original during editing
                # Convert triangle to 3D coordinate format, shape 3x3
                triangle_points = [vertices[int(triangle.attrib.get(index))] for index in ["v1", "v2", "v3"]]
                seq_max_point = seq_point(triangle_points[0],
                                          seq_point(triangle_points[1], triangle_points[2]))  # Get the most standardized point
                if equal_point(triangle_points[0], seq_max_point):  # Already encoded as 1, skip
                    continue
                else:  # Not encoded as 1, modify order to make it so
                    if equal_point(triangle_points[1], seq_max_point):  # triangle[1] is most standardized
                        triangle.attrib["v1"] = str(triangle_t.attrib["v2"])
                        triangle.attrib["v2"] = str(triangle_t.attrib["v3"])
                        triangle.attrib["v3"] = str(triangle_t.attrib["v1"])
                        continue
                    else:  # triangle[2] is most standardized
                        triangle.attrib["v1"] = str(triangle_t.attrib["v3"])
                        triangle.attrib["v2"] = str(triangle_t.attrib["v1"])
                        triangle.attrib["v3"] = str(triangle_t.attrib["v2"])
                        continue

    # Defense complete. Save the modified XML tree to the defense file.
    tree.write(defense_model, encoding="utf-8", xml_declaration=True)



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
            if list(key) == ["v1", "v2", "v3"]:
                return True
    return False