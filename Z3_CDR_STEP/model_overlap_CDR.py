import re
from collections import defaultdict


def Regulare_step(str):
    """
    function: Perform regex processing on str to get the number after #
    """
    return int(re.search(r"#(\d+)", str).group(1))

def Regulare_step_all(str):
    # Perform regex processing on a LINE string
    numbers = re.findall(r'#(\d+)', str)
    return [int(num) for num in numbers]

def get_line_car(line,car):
    # Get the car point index contained in LINE
    line_index=Regulare_step_all(line)
    for index in line_index:
        if index in car:
            return index

def get_datalists_step(stepfilepath):
    """
       function: Get datalists from step file
       datalistes: Data rows from step file
    """

    # Open step file and get its data
    step_file = open(stepfilepath)
    s = step_file.read()
    step_file.close()

    # Simple processing of s data, replacing original data
    s = s.replace('\r', '').replace('ISO-10303-21\n', '').replace('"END-ISO-10303-21\n"', '')

    # Extract DATA section
    data = s[s.index('DATA') + len('DATA') + 2:]
    # Split data section by newline
    data_list = data.split('\n')

    return data_list

def get_datalines_step(stepfilepath):
    """
    function: Get datalines from step file
    datalines: Dictionary of data section in step file: key(#x), value(following data)
    """

    data_lines = {}

    # Open step file and get its data
    step_file=open(stepfilepath)
    s = step_file.read()
    step_file.close()

    # Simple processing of s data, replacing original data
    s = s.replace('\r', '').replace('ISO-10303-21\n', '').replace('"END-ISO-10303-21\n"', '')

    # Extract DATA section
    data = s[s.index('DATA') + len('DATA') + 2:]
    # Split data section by newline
    data_list = data.split('\n')

    # Get data_lines
    for line in data_list:
        cut_pos = line.find('=')

        if cut_pos != -1:  # If equals sign exists
            key = line[:cut_pos].strip()  # Get key
            value = line[cut_pos + 1:].strip()  # Get value
            data_lines[key] = value

    return data_lines

def get_datashell_step(data_lines):
    """
    function: Get CLOSED_SHELL sequence from data_lines
    Format like: ['#50', '#72', '#94', '#116', '#138', '#160', '#182', '#204', '#226', '#248', '#270', '#292']
    """

    data_shell = []
    for key in data_lines.keys():
        # Get data section corresponding to key
        data_key=data_lines[key]

        cut_pos1=data_key.find("(")  # Use ( as separator between key_inside and data_inside
        cut_pos2=data_key.find(";")-1  # Use ; as end separator for data_inside

        if data_key.find("#") == -1: continue  # Skip data sections without #

        key_inside=data_key[:cut_pos1].strip()  # Extract keyword here, further split data_key

        if key_inside !="CLOSED_SHELL": continue  # Only extract parts with CLOSED_SHELL keyword

        data_inside=data_key[cut_pos1+1:cut_pos2].strip()  # Get data section after keyword

        data_inside1 = data_inside.split(',')  # Split data by comma

        for i in range(len(data_inside1)):
            cur=data_inside1[i].replace("(","").replace(")","").strip()  # Standardize string format
            if cur[0]=='#':
                data_shell.append(cur.strip())

    return data_shell

def get_ver_and_car_list(data_lines):
    # Get verpoint and carpoint sequence from data_lines
    res = []
    for key in data_lines.keys():
        # Get data section corresponding to key
        data_key = data_lines[key]

        cut_pos1 = data_key.find("(")  # Use ( as separator between key_inside and data_inside
        cut_pos2 = data_key.find(";") - 1  # Use ; as end separator for data_inside

        key_inside = data_key[:cut_pos1].strip()  # Extract keyword here, further split data_key
        if key_inside == "VERTEX_POINT" or key_inside == "CARTESIAN_POINT":
            res.append(key)

    return res

def get_ver_and_car_int_list(data_lines):
    # Get verpoint and carpoint sequence (as int) from data_lines
    res = get_ver_and_car_list(data_lines)
    res_ver = [Regulare_step(ind) for ind in res]

    return res_ver

def get_car_list(data_lines):
    # Get verpoint and carpoint sequence from data_lines
    res = []
    for key in data_lines.keys():
        # Get data section corresponding to key
        data_key = data_lines[key]

        cut_pos1 = data_key.find("(")  # Use ( as separator between key_inside and data_inside
        cut_pos2 = data_key.find(";") - 1  # Use ; as end separator for data_inside

        key_inside = data_key[:cut_pos1].strip()  # Extract keyword here, further split data_key
        if key_inside == "CARTESIAN_POINT":
            res.append(key)

    return res

def get_car_int_list(data_lines):
    # Get verpoint and carpoint sequence (as int) from data_lines
    res = get_car_list(data_lines)
    res_ver = [Regulare_step(ind) for ind in res]

    return res_ver

def find_duplicate_values(dictionary):
    """
    Identify how many duplicate values exist in dictionary and return keys for duplicate values
    :param dictionary: Input dictionary
    :return: Returns a dictionary where key is duplicate value (converted to tuple), value is corresponding key list
    """
    # Create defaultdict to store key list for each value
    value_to_keys = defaultdict(list)

    # Traverse dictionary, convert values to tuples, and record corresponding keys
    for key, value in dictionary.items():
        value_to_keys[tuple(value)].append(key)

    # Filter out duplicate values
    duplicates = {value: keys for value, keys in value_to_keys.items() if len(keys) > 1}

    return duplicates

def increment_step_numbers(step_text,exclude_numbers,inial_value,previous):
    def replace_match(match):
            number = int(match.group(1))  # Get number after #
            if number in exclude_numbers:
                return f"#{number}"  # If in exclude list (vertex indices), keep unchanged

            final_number=previous+1+number-inial_value  # Change subsequent indices to original number + insertion index - initial number
            return f"#{final_number}"  # Otherwise increment by specified value

    return re.sub(r"#\s*(\d+)", replace_match, step_text)

def remove_last_n_elements(input_str, n):
    # Find content inside parentheses
    start = input_str.find('(') + 1
    end = input_str.rfind('))')
    content = input_str[start:end]

    # Split content into list by comma
    elements = content.split(',')

    # Remove last n elements
    if n > len(elements):
        raise ValueError("n cannot be greater than list length")
    new_elements = elements[:-n]

    # Reconstruct string
    new_content = ','.join(new_elements)
    return input_str[:start] + new_content + input_str[end:]

def model_overlap_defense(filepath,attackfile):
    # Get basic file information:
    data_lines = get_datalines_step(filepath)
    data_list = get_datalists_step(filepath)
    car_list = get_car_int_list(data_lines)
    car_ver_int = get_ver_and_car_int_list(data_lines)
    data_shell = get_datashell_step(data_lines)

    data_shell_tuple = {}  # Shell index corresponding to # index range
    data_shell_point = {}  # Shell index corresponding to specific point set
    ivers = [Regulare_step(key) for key in data_lines.keys()]  # Get numeric version of all keys to find max
    spe_data_shell = data_shell[:]  # Get copy of data_shell
    spe_data_shell.append("#" + str(max(ivers) + 1))

    for ind, shell in enumerate(data_shell):
        inial = Regulare_step(spe_data_shell[ind])
        end = Regulare_step(spe_data_shell[ind + 1])
        data_shell_tuple[shell] = data_list[inial:end]
    for key, value in data_shell_tuple.items():
        key_point = []
        for line in value:
            if line.find("LINE") != -1:
                key_point.append(get_line_car(line, car_list))
        data_shell_point[key] = key_point
    res = find_duplicate_values(data_shell_point)  # Duplicate point sets

    keys_de = []  # Indices to delete
    for value in res.values():
        for key_de in [Regulare_step(val) for val in value][1:]:
            keys_de.append(key_de)
    line_de,lines_de = sorted([key_de + 6 for key_de in keys_de]),[]  # First index of rows to delete, row indices to delete
    for line in line_de:
        lines_de.extend(range(line-6, line+15+1))

    with open(filepath, 'r', encoding='utf-8') as file:  # Delete corresponding rows
        lines = file.readlines()
    lines_c = lines[0:line_de[0]]  # First copy header section
    for line in lines[lines_de[0]:]:
        if line.find("#") != -1:  # Only modify # index parts
            ind = Regulare_step(line)
            if ind in lines_de:
                pass
            else:
                lines_c.append(line)
        else:
            lines_c.append(line)  # Add end section

    previous = 0  # For files with deleted indices, process forward and delete corresponding closed_shell parts
    # Core algorithm:
    # We traverse the file with some indices deleted. When the next # index is not previous # index +1,
    # we can infer some parts were deleted in between.
    # Then we change the next # index to previous # index +1, and perform same operation on all subsequent indices (using loop)
    # previous records the last index, increment_step_numbers algorithm handles special cases when changing indices (not changing vertex indices)
    # After this processing, clearly for closed_shell we just need to delete the last len(keys_de) shell indices
    for ind, line in enumerate(lines_c):
        if line.find("CLOSED_SHELL") != -1:  # Modify closed_shell section
            new_line = remove_last_n_elements(line, len(keys_de))
            lines_c[ind] = new_line
        if line.find("#") != -1:
            if previous == Regulare_step(line) - 1:
                pass
            else:
                lines_c[ind] = increment_step_numbers(line, car_ver_int, Regulare_step(line), previous)
            previous = Regulare_step(lines_c[ind])

    with open(attackfile, "w", encoding="utf-8") as file:  # Write to file
        file.writelines(lines_c)
    print("Duplicate faces:",res.values())