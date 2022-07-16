"""
utils.py

Author: Joseph Maclean Arhin
"""

import os


def convert_to_camelcase(input_string: str):
    """
    Algorithm to convert snake_case to CamelCase
    """
    return "".join([string.capitalize() for string in input_string.split("_")])


def add_to_init(dir_path, file_name, class_name):
    """
    import class from file into an __init__ file
    :param dir_path:
    :param file_name:
    :param class_name:
    :return:
    """
    with open(os.path.join(dir_path, "__init__.py"), "a", encoding="UTF-8") as file:
        file.write(f"\nfrom .{file_name} import {class_name}")


def remove_suffix(string: str, suffix):
    """
    Remove suffix from string if its last characters are equal to
    the suffix passed.
    """
    suffix_length = len(suffix) - 1
    string_length = len(string) - 1
    cut_off_index = string_length - suffix_length

    if string_length <= suffix_length:
        final_string = string

    elif string[cut_off_index:] == suffix:
        final_string = string[:cut_off_index]

    else:
        final_string = string

    if final_string[-1] == "_":
        final_string = final_string[:-1]

    return final_string.lower()
