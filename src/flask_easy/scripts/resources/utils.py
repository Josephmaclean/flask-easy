import os


def convert_to_camelcase(string: str):
    """
    Algorithm to convert snake_case to CamelCase
    """
    s = list(string)

    if s[-1] == "_":
        s[-1] = ""

    for i in range(len(s), 0, -1):
        if s[i - 1] == "_":
            s[i - 1] = ""
            s[i] = s[i].upper()
    s[0] = s[0].upper()

    return "".join(s)


def add_to_init(dir_path, file_name, class_name):
    with open(os.path.join(dir_path, "__init__.py"), "a") as w:
        w.write(f"from .{file_name} import {class_name}\n")


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
