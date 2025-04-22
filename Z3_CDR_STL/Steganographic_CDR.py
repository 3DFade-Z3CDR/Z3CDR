from stl import mesh


def swap_lists(lst1, lst2):
    """
    Swap the contents of two lists (deep copy)

    Args:
        lst1: First list to swap
        lst2: Second list to swap
    Note:
        Modifies the lists in-place and doesn't return anything
    """
    temp = lst1.copy()
    lst1[:] = lst2
    lst2[:] = temp


def equal_lists(lst1, lst2):
    """
    Check if two lists are exactly equal (doesn't support nested lists)

    Args:
        lst1: First list to compare
        lst2: Second list to compare
    Returns:
        bool: True if lists are identical, False otherwise
    Raises:
        EOFError: If lists have different lengths
    """
    if len(lst1) != len(lst2):
        raise EOFError("Lists must be of equal length")

    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            return False
    return True


def sel_ver(ver1, ver2):
    """
    Determine the order of two 3D vertices based on specific rules:
    1. Compare sum of coordinates (x+y+z), return vertex with larger sum
    2. If sums are equal, compare x, then y, then z coordinates
    3. Return the vertex that comes first in the ordering

    Args:
        ver1: First 3D vertex [x,y,z]
        ver2: Second 3D vertex [x,y,z]
    Returns:
        list: The selected vertex
    Raises:
        EOFError: If vertices have different dimensions or identical coordinates
    """
    if len(ver1) != len(ver2):
        raise EOFError("Vertices must have same dimensions")

    sum1, sum2 = sum(ver1), sum(ver2)
    if sum1 > sum2:
        return ver1
    elif sum1 < sum2:
        return ver2

    # Compare coordinates sequentially
    for i in range(3):
        if ver1[i] < ver2[i]:
            return ver1
        elif ver1[i] > ver2[i]:
            return ver2

    raise EOFError("Vertices have identical coordinates")


def Steganographic_Decrypt(filepath, Num_bit):
    """
    Perform bit-level analysis on STL file to detect steganography patterns

    Args:
        filepath: Path to STL file
        Num_bit: Number of bits to analyze
    Returns:
        list: Binary sequence indicating detected patterns (1 for match, 0 otherwise)
    """
    temp_mesh = mesh.Mesh.from_file(filepath)
    decryption = []

    for ver in temp_mesh.vectors:
        res = equal_lists(ver[0], sel_ver(ver[0], sel_ver(ver[1], ver[2])))
        decryption.append(int(res))

    return decryption[:Num_bit]


def Steganographic_Defense(infilepath, outfilepath):
    """
    Defend against SGOP attack by normalizing vertex ordering in triangles

    Args:
        infilepath: Input STL file path
        outfilepath: Output STL file path
    """
    temp_mesh = mesh.Mesh.from_file(infilepath)

    for ver in temp_mesh.vectors:
        # Check current vertex ordering
        if equal_lists(ver[0], sel_ver(ver[0], sel_ver(ver[1], ver[2]))):
            continue

        # Reorder vertices to match expected pattern
        if equal_lists(ver[1], sel_ver(ver[1], sel_ver(ver[0], ver[2]))):
            swap_lists(ver[0], ver[1])
            swap_lists(ver[1], ver[2])
        else:
            swap_lists(ver[0], ver[2])
            swap_lists(ver[1], ver[2])

    temp_mesh.save(outfilepath)


def Steganographic_detection(filepath):
    """
    Detect potential steganography in STL files

    Args:
        filepath: Path to STL file to analyze
    Returns:
        bool: True if steganography is detected, False otherwise
    """
    temp_mesh = mesh.Mesh.from_file(filepath)

    for ver in temp_mesh.vectors:
        if not equal_lists(ver[0], sel_ver(ver[0], sel_ver(ver[1], ver[2]))):
            return True
    return False