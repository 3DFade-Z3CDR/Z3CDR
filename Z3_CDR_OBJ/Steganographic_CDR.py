import numpy as np
import trimesh


def equal_lists(lst1, lst2):
    """
    function: Check if two lists are exactly identical (nested lists not allowed)
    input: Two lists
    output: Comparison result - True if identical, False otherwise
    """
    if len(lst1) != len(lst2):
        raise EOFError
    else:
        length = len(lst1)
        for ind in range(0, length):
            if lst1[ind] != lst2[ind]:
                return False

        return True


def sel_ver(ver1, ver2):
    """
    function:
    Determine the order between ver1 and ver2 (ver1[x,y,z]:ver2[x,y,z])
    First compare the sum of x+y+z, return the ver with larger sum
    If sums are equal, compare x,y,z coordinates one by one, output the one with smaller coordinates
    input: Two 3D coordinate arrays
    output: The one that better matches the rules
    """

    # Verify if inputs are 3D coordinates
    if len(ver1) != len(ver2):
        raise EOFError

    # Calculate sum of coordinates and return the ver with larger sum
    sum1, sum2 = sum(ver1), sum(ver2)
    if sum1 > sum2:
        return ver1
    elif sum1 < sum2:
        return ver2

    # Compare x,y,z coordinates one by one, return the ver with smaller coordinates
    # Note: There shouldn't be two points with identical coordinates in a triangle face, otherwise it's an error
    else:
        if ver1[0] < ver2[0]:
            return ver1  # Compare x coordinate
        elif ver1[0] > ver2[0]:
            return ver2
        else:
            if ver1[1] < ver2[1]:  # Compare y coordinate
                return ver1
            elif ver1[1] > ver2[1]:
                return ver2
            else:
                if ver1[2] < ver2[2]:  # Compare z coordinate
                    return ver1
                elif ver1[2] > ver2[2]:
                    return ver2
                else:
                    raise EOFError("Identical coordinate values")


def Steganographic_Decrypt(filepath, Num_bit):
    """
    function: Perform bit-level analysis on file, return 1 if matches rules, 0 otherwise
    """
    temp_mesh = trimesh.load_mesh(filepath)

    Decryption = []
    for triangle in temp_mesh.triangles:
        res = equal_lists(triangle[0], sel_ver(triangle[0], sel_ver(triangle[1], triangle[2])))
        Decryption.append(int(res))

    return Decryption[:Num_bit]


def Steganographic_Defense(infilepath, outfilepath):
    # Defense against SGOP attack by modifying all v1.v2.v3 combinations to match encoding rule 1

    in_mesh = trimesh.load_mesh(infilepath)
    out_mesh = in_mesh.copy()
    triangles = in_mesh.triangles

    # Get triangle vertex indices (mesh.faces)
    faces = np.copy(in_mesh.faces)

    for ind, triangle in enumerate(triangles):
        sel_tri = sel_ver(triangle[0], sel_ver(triangle[1], triangle[2]))  # Select the largest vertex from [v0,v1,v2]
        if equal_lists(triangle[0], sel_tri):  # If v0 is already the largest, no change needed
            continue
        else:
            if equal_lists(triangle[1], sel_tri):  # If v1 is the largest vertex, reorder to [v1,v2,v0]
                faces[ind] = faces[ind][[1, 2, 0]]
            else:  # If v2 is the largest vertex, reorder to [v2,v0,v1]
                faces[ind] = faces[ind][[2, 0, 1]]

    out_mesh.faces = faces
    out_mesh.export(outfilepath)


def Steganographic_Dection(infile):
    # Detect SGOP attack by finding v1.v2.v3 combinations that don't match encoding rule 1
    # Returns True if found, False otherwise

    in_mesh = trimesh.load_mesh(infile)
    out_mesh = in_mesh.copy()
    triangles = in_mesh.triangles

    # Get triangle vertex indices (mesh.faces)
    faces = np.copy(in_mesh.faces)

    for ind, triangle in enumerate(triangles):
        sel_tri = sel_ver(triangle[0], sel_ver(triangle[1], triangle[2]))  # Select the largest vertex from [v0,v1,v2]
        if equal_lists(triangle[0], sel_tri):  # If v0 is already the largest, no operation needed
            pass
        else:
            return True

    return False