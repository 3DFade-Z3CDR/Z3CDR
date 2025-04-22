import xml.etree.ElementTree as ET
import file_handle as fd
import catalog_examine as ce
import re

def strip_namespace(tag):
    return re.sub(r'\{.*?\}', '', tag)

def strlist_calculate(strl1, strl2):
    # Determine whether the values of two string lists are equal
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

def Build_repetition_dection(input_file):
    """
    function: Perform build repetition detection on input_file
    """
    # Find all object elements and convert them into dictionary format
    objs = fd.get_file_objects(input_file)
    objects = {obj.attrib.get('id', 'empty'): obj for obj in objs}
    # Find all item elements
    items = fd.get_file_items(input_file)

    # Exception handling: objects or items are empty
    if len(objects) == 0:
        raise FileNotFoundError
    if len(items) == 0:
        raise FileNotFoundError

    # Extract object-related content from build, including id and corresponding transform
    builds = []
    for index, item in enumerate(items):
        builds.append([item.get("objectid", "empty"), item.get("transform", "1 0 0 0 1 0 0 0 1 0 0 0"), index])
    build_ids = [l[0] for l in builds]
    build_trans = [list(map(lambda x: round(float(x), 4), l[1].strip().split())) for l in builds]

    # Perform DOS defense on build: return a list of IDs to be deleted
    dos = []
    for cur in range(len(builds)):
        for other in range(cur + 1, len(builds)):
            if builds[cur][0] == builds[other][0] and strlist_calculate(builds[cur][1], builds[other][1]):
                dos.append(other)
    dos = list(set(dos))

    return dos

def Build_repetition_defense(input_file, output_file):
    """
    function: Perform build repetition defense on input_file
    """
    dos = Build_repetition_dection(input_file)

    if len(dos) == 0:
        raise EOFError
    else:
        # Parse the original XML file
        tree = ET.parse(input_file)
        root = tree.getroot()

        to_remove = []
        for child in root:
            if strip_namespace(child.tag) == 'build':
                for index, item in enumerate(child):
                    if index in dos:
                        to_remove.append(item)
                for delte in to_remove:
                    child.remove(delte)
            else:
                pass

        # Convert the processed tree into an XML file
        fd.indent(root)
        new_tree = ET.ElementTree(root)
        new_tree.write(output_file, encoding="utf-8", xml_declaration=True)
