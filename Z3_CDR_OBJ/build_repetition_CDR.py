import trimesh

def build_repetition_defense(infile,outfile):
    """
    function: Defense against build repetition attacks by undo and rebuild
    1. Get the mesh from infile and copy it to out_mesh
    2. Remove duplicate triangles in out_mesh
    3. Save out_mesh to outfile

    infile: input file
    outfile: output file
    """

    # Get the mesh from infile and copy it to out_mesh
    in_mesh=trimesh.load_mesh(infile)
    out_mesh=in_mesh.copy()

    # Use update_faces to remove duplicate triangles
    out_mesh.update_faces(out_mesh.unique_faces())
    # Save out_mesh to file
    out_mesh.export(outfile)

def build_repetition_dection(infile):
    """
    Detect rebuild attacks: Check if there are non-unique faces (unique_faces()),
    return true if exists, false otherwise
    """
    in_mesh = trimesh.load_mesh(infile)
    unique_faces = all(in_mesh.unique_faces())

    return not unique_faces