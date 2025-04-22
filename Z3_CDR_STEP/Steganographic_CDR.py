import re
import random

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

def is_sorted_ascending(lst):
        # Check if a list is sorted in ascending order
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:  # If current element is greater than next, return False
                return False
        return True  # If no inversions found, list is sorted ascending

def recover_numbers(numbers):
    """
        function: Rewrite numbers, changing original [v2,v3,v1] or [v3,v1,v2] to [v1,v2,v3]
    """

    sorted_numbers = sorted(numbers)

    return sorted_numbers

def modify_edge_loop(match):
    # Only modify numbers in EDGE_LOOP and arrange them according to SGOP attack pattern
    numbers = re.findall(r"#\d+", match.group(1))  # Extract #57, #58, #59 vertex info
    reversed_numbers = ",".join(recover_numbers(numbers))  # SGOP arrangement

    return f"EDGE_LOOP('',({reversed_numbers}))"

def get_SGOP_defense_dict(data_list):
    """
    function: Return indices of edge_loop sections that will be modified
    """

    SGOP_defense_dict={}

    for index, line in enumerate(data_list):
        if line.find("EDGE_LOOP") != -1:  # Make changes to edge_loop sections

            # Extract # numbers
            match = re.search(r"EDGE_LOOP$'',\((.*?)$\)", line)
            if match:
                edge_numbers = list(map(int, re.findall(r"#(\d+)", match.group(1))))  # Extract numbers from edge_loop section

            if is_sorted_ascending(edge_numbers):  # If already sorted ascending, no processing needed
                pass
            else:  # If not sorted ascending, add to defense dictionary
                new_text = re.sub(r"EDGE_LOOP$'',\((.*?)$\)", modify_edge_loop, line)
                SGOP_defense_dict[index+7] = new_text+"\n"

    return SGOP_defense_dict

def Steganographic_defense(attackfilepath,defensefilepath):
    data_list = get_datalists_step(attackfilepath)
    SGOP_defense_dict = get_SGOP_defense_dict(data_list)

    # Write modifications to defense file
    with open(attackfilepath, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if index in SGOP_defense_dict.keys():
            lines[index] = SGOP_defense_dict[index]
    with open(defensefilepath, "w", encoding="utf-8") as file:
        file.writelines(lines)

def Steganographic_detection(infile):
    """
    Detect if SGOP attack exists in STEP file, return True if exists, False otherwise
    """
    data_list = get_datalists_step(infile)

    for index, line in enumerate(data_list):
        if line.find("EDGE_LOOP") != -1:  # Check edge_loop sections

            # Extract # numbers
            match = re.search(r"EDGE_LOOP$'',\((.*?)$\)", line)
            if match:
                edge_numbers = list(map(int, re.findall(r"#(\d+)", match.group(1))))  # Extract numbers from edge_loop section

            if is_sorted_ascending(edge_numbers):  # If sorted ascending, no processing
                pass
            else:  # If not sorted ascending, return true
                return True

    return False

def Decode_step(filepath,number):
    Decode_list=[]

    def is_sorted_ascending(lst):
        # Check if a list is sorted in ascending order
        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:  # If current element is greater than next, return False
                return False
        return True  # If no inversions found, list is sorted ascending

    data_list = get_datalists_step(filepath)

    for line in data_list:
        if line.find("EDGE_LOOP") != -1:  # Select edge_loop sections

            # Extract # numbers
            match = re.search(r"EDGE_LOOP$'',\((.*?)$\)", line)
            if match:
                edge_numbers = list(map(int, re.findall(r"#(\d+)", match.group(1))))  # Extract numbers from edge_loop section

            if is_sorted_ascending(edge_numbers):
                Decode_list.append(1)
            else:
                Decode_list.append(0)

    return Decode_list[:number]