# Text processing utilities
"""
Utility functions for text processing and manipulation.
"""


def split_list_by_newline(lst):
    """
    Splits a list into separate elements if there are newlines.
    
    Args:
        lst (list): List of strings that may contain newlines
    
    Returns:
        list: Expanded list with newline-split elements
    """
    result = []
    for item in lst:
        if '\n' in item:
            result.extend(item.split('\n'))
        else:
            result.append(item)
    return result


def replace_comma_with_period(text):
    """
    Replaces commas with periods in a given text.
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text with commas replaced by periods
    """
    return text.replace(",", ".")


def remove_vs(text):
    """
    Removes the "vs" part from a given text.
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text with "vs" removed
    """
    return text.replace("\nvs", "")


def remove_empty_elements(lst):
    """
    Strips empty or whitespace-only elements from the list.
    
    Args:
        lst (list): List that may contain empty elements
    
    Returns:
        list: List with empty elements removed
    """
    return [item for item in lst if item.strip()]


def find_first_non_tuple_index(lst):
    """
    Finds the index of the first non-tuple element in the list.
    
    Args:
        lst (list): List of mixed elements
    
    Returns:
        int: Index of the first non-tuple element
    """
    for index, element in enumerate(lst):
        if not isinstance(element, tuple):
            return index
    return len(lst) + 2