import file_handle as fd

def build_tree_with_depth(tree, root, depth=1):
    """
    Build tree structure and calculate the minimum depth of each node.

    :param tree: Dictionary representing hierarchical relationships, e.g., {'2': ['1', '1'], ...}.
    :param root: Current root node of the tree.
    :param depth: Current node depth (recursion depth).
    :return: Tree structure including nodes and their minimum depths.
    """
    return {
        'id': root,
        'depth': depth,
        'children': [build_tree_with_depth(tree, child, depth + 1) for child in tree.get(root, [])]
    }

def depth_tree_node(tree, node_id):
    """
    Query the minimum depth of a specific node.

    :param tree: Constructed tree structure.
    :param node_id: Target node ID to query.
    :return: Minimum depth of the node.
    """
    if tree['id'] == node_id:
        return tree['depth']
    for child in tree.get('children', []):
        result = depth_tree_node(child, node_id)
        if result is not None:
            return result
    return 0  # Return 0 if node not found

def max_components_depth(filepath, node_id):
    """
    Calculate the maximum iteration count for a specific node.

    :param filepath: File path to process.
    :param node_id: Target node ID to calculate.
    :return: Maximum iteration count for the node.
    """
    # Initialize result array to store depth of each node
    res = []

    # Extract objects containing components from file and build tree_dict
    # tree_dict example: {'1': [], '2': ['1', '1'], '3': ['2', '1'], '4': ['3', '2'], '5': ['4', '3'], '6': []}
    # Where [] indicates no components
    objs = fd.get_file_objects(filepath)
    tree_dict = {}
    for obj in objs:
        obj_id = obj.get("id")
        tree_dict[obj_id] = []
        com = obj.find('.//{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}components')
        if com is not None:
            for child in com:
                tree_dict[obj_id].append(child.get("objectid", "empty"))

    # Build tree with specified node as root
    tree_res = build_tree_with_depth(tree_dict, node_id)

    # Get depth of all nodes and return the maximum value
    for id in tree_dict.keys():
        res.append(depth_tree_node(tree_res, id))

    return max(res)

def check_circular_reference_depth(filepath, max_depth=5):
    """
    Check if circular references exceed maximum allowed depth.

    :param filepath: File path to process.
    :param max_depth: Maximum allowed iteration count (default: 5).
    :return: False if exceeds max depth, True otherwise.
    """
    items = fd.get_file_items(filepath)

    # Find build object IDs
    builds = []
    for index, item in enumerate(items):
        builds.append([item.get("objectid", "empty"),
                      item.get("transform", "1 0 0 0 1 0 0 0 1 0 0 0"),
                      index])
    build_ids = [l[0] for l in builds]

    # Check if any node exceeds max iteration count
    for build_id in build_ids:
        res = max_components_depth(filepath, build_id)
        if res >= max_depth:
            return False  # Exceeds max iteration count

    return True  # Within allowed iteration count