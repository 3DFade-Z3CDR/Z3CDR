from pathlib import Path
import file_handle as fd


def exist_Content_Types_file(directory):

    folder = Path(directory)  # Convert to Path object

    if not folder.is_dir():  # Check if the path is a directory
        raise ValueError(f"{directory} is not a valid directory path")

    if (folder / "[Content_Types].xml").exists():
        return True
    else:
        raise FileNotFoundError("Cannot find [Content_Types].xml, please check your format")

def exist_3dmodel_file(directory):
    for dir_path in Path(directory).rglob("3D"):
        # Look for the 3dmodel.model file in the 3D folder
        model_file = dir_path / "3dmodel.model"
        if model_file.exists():
            return True
        else:
            raise FileNotFoundError(f"'3dmodel.model' file not found in '{dir_path}'")

    raise FileNotFoundError("No directory containing a '3D' folder found, or no '3dmodel.model' file in it. Please check your format")

def find_3dmodel_file(directory):
    if exist_3dmodel_file(directory):
        for dir_path in Path(directory).rglob("3D"):
            # Look for the 3dmodel.model file in the 3D folder
            model_file = dir_path / "3dmodel.model"
            if model_file.exists():
                return model_file

def exist_rels_file(directory):
    for dir_path in Path(directory).rglob("_rels"):
        rel_file = dir_path / ".rels"
        if rel_file.exists():
            return True
        else:
            raise FileNotFoundError(f"'3dmodel.model' file not found in '{dir_path}'")

    raise FileNotFoundError("No directory containing a '_rels' folder found, or no '.rels' file in it. Please check your format")

def check_3mf_format(filepath, outdir):
    fd.unzip_3mf(filepath, outdir)
    if exist_rels_file(outdir) and exist_3dmodel_file(outdir) and exist_rels_file(outdir):
         return True
